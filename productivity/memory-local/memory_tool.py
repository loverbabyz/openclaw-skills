#!/usr/bin/env python3
"""
memory-local: 本地语义记忆工具
使用 sentence-transformers (all-MiniLM-L6-v2) + FAISS 实现完全本地的向量搜索
无需 API Key，完全离线运行
"""

import os
import sys
import json
import uuid
import argparse
import time
from pathlib import Path

import numpy as np
import faiss

# 尝试延迟导入 transformer 以加快启动速度
_model = None
_tokenizer = None

MEMORY_DIR = Path.home() / ".openclaw-memory"
MEMORY_FILE = MEMORY_DIR / "memories.jsonl"
INDEX_FILE = MEMORY_DIR / "index.faiss"
DIM_FILE = MEMORY_DIR / "dim.txt"
DIM = 384  # all-MiniLM-L6-v2 embedding dimension

# 轻量缓存，避免重复加载模型
_cache_dir = MEMORY_DIR / ".model_cache"
_cache_dir.mkdir(parents=True, exist_ok=True)


def get_model():
    global _model, _tokenizer
    if _model is None:
        from sentence_transformers import SentenceTransformer
        # all-MiniLM-L6-v2: 90MB, 384维, 速度极快
        _model = SentenceTransformer("all-MiniLM-L6-v2", cache_folder=str(_cache_dir))
    return _model


def ensure_dir():
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)


def load_index():
    if INDEX_FILE.exists() and DIM_FILE.exists():
        dim = int(DIM_FILE.read_text().strip())
        index = faiss.read_index(str(INDEX_FILE))
        memories = []
        if MEMORY_FILE.exists():
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        memories.append(json.loads(line))
        return index, memories
    return None, []


def save_index(index, memories):
    ensure_dir()
    faiss.write_index(index, str(INDEX_FILE))
    DIM_FILE.write_text(str(DIM))
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        for m in memories:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")


def embed(texts):
    model = get_model()
    if isinstance(texts, str):
        texts = [texts]
    embeddings = model.encode(texts, convert_to_numpy=True)
    # 手动归一化
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms = np.where(norms == 0, 1, norms)
    embeddings = embeddings / norms
    return embeddings.astype(np.float32)


def do_store(text, category="general", importance=0.5):
    ensure_dir()
    index, memories = load_index()

    mem_id = str(uuid.uuid4())
    ts = time.time()

    emb = embed(text)[0]

    if index is None:
        index = faiss.IndexFlatIP(DIM)
        # 第一次存入时写入 dim
        ensure_dir()
        DIM_FILE.write_text(str(DIM))

    # importance 加权（简单做法：乘以 importance 系数）
    weighted_emb = emb * (0.5 + importance * 0.5)
    faiss.normalize_L2(np.array([weighted_emb], dtype=np.float32))
    index.add(np.array([weighted_emb], dtype=np.float32))

    memory = {
        "id": mem_id,
        "text": text,
        "category": category,
        "importance": importance,
        "created_at": ts,
        "vector": emb.tolist()
    }
    memories.append(memory)
    save_index(index, memories)

    return {"id": mem_id, "text": text[:80], "category": category, "importance": importance}


def do_search(query, limit=5, category=None):
    memories = []
    if MEMORY_FILE.exists():
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    memories.append(json.loads(line))

    if not memories:
        return []

    # 过滤 category
    if category:
        memories = [m for m in memories if m.get("category") == category]

    if not memories:
        return []

    # 向量搜索
    query_emb = embed(query)[0]
    weighted_q = query_emb * 1.0
    faiss.normalize_L2(np.array([weighted_q], dtype=np.float32))

    # 构建临时索引做搜索
    vectors = np.array([m["vector"] for m in memories], dtype=np.float32)
    faiss.normalize_L2(vectors)
    temp_index = faiss.IndexFlatIP(DIM)
    temp_index.add(vectors)

    scores, indices = temp_index.search(np.array([weighted_q], dtype=np.float32), min(limit, len(memories)))

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx < len(memories):
            m = memories[idx]
            results.append({
                "id": m["id"],
                "text": m["text"],
                "category": m.get("category", "general"),
                "importance": m.get("importance", 0.5),
                "created_at": m.get("created_at", 0),
                "score": float(score)
            })

    return results


def do_forget(memory_id=None, query=None, limit=1):
    if memory_id is None and query is None:
        return {"error": "需要提供 memory_id 或 query"}

    index, memories = load_index()
    if not memories:
        return {"forgotten": 0}

    ids_to_remove = set()

    if memory_id:
        ids_to_remove.add(memory_id)

    if query:
        search_results = do_search(query, limit=limit)
        for r in search_results:
            ids_to_remove.add(r["id"])

    original_count = len(memories)
    memories = [m for m in memories if m["id"] not in ids_to_remove]

    if len(memories) == original_count:
        return {"forgotten": 0, "message": "未找到匹配的记忆"}

    # 重建索引
    if memories:
        vectors = np.array([m["vector"] for m in memories], dtype=np.float32)
        faiss.normalize_L2(vectors)
        new_index = faiss.IndexFlatIP(DIM)
        new_index.add(vectors)
        save_index(new_index, memories)
    else:
        # 全删了
        if INDEX_FILE.exists():
            INDEX_FILE.unlink()
        if MEMORY_FILE.exists():
            MEMORY_FILE.unlink()

    return {"forgotten": len(ids_to_remove)}


def do_list(limit=20, category=None):
    memories = []
    if MEMORY_FILE.exists():
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    memories.append(json.loads(line))

    if category:
        memories = [m for m in memories if m.get("category") == category]

    memories.sort(key=lambda m: m.get("created_at", 0), reverse=True)

    return memories[:limit]


def main():
    parser = argparse.ArgumentParser(description="memory-local: 本地语义记忆")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_store = sub.add_parser("store", help="存储记忆")
    p_store.add_argument("--text", required=True, help="记忆内容")
    p_store.add_argument("--category", default="general", help="分类")
    p_store.add_argument("--importance", type=float, default=0.5, help="重要程度 0-1")

    p_search = sub.add_parser("search", help="搜索记忆")
    p_search.add_argument("--query", required=True, help="搜索query")
    p_search.add_argument("--limit", type=int, default=5, help="返回数量")
    p_search.add_argument("--category", help="限定分类")

    p_forget = sub.add_parser("forget", help="删除记忆")
    p_forget.add_argument("--id", help="记忆ID")
    p_forget.add_argument("--query", help="通过搜索匹配删除")
    p_forget.add_argument("--limit", type=int, default=1, help="搜索删除时最多删几条")

    p_list = sub.add_parser("list", help="列出记忆")
    p_list.add_argument("--limit", type=int, default=20)
    p_list.add_argument("--category")

    args = parser.parse_args()

    if args.cmd == "store":
        result = do_store(args.text, args.category, args.importance)
        print(json.dumps(result, ensure_ascii=False))

    elif args.cmd == "search":
        result = do_search(args.query, args.limit, args.category)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.cmd == "forget":
        result = do_forget(args.id, args.query, args.limit)
        print(json.dumps(result, ensure_ascii=False))

    elif args.cmd == "list":
        result = do_list(args.limit, args.category)
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
