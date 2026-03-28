---
name: memory-local
description: 完全本地的语义记忆系统。使用 sentence-transformers (all-MiniLM-L6-v2) + FAISS 向量数据库实现，无需 API Key，完全离线运行。在 Agent 启动时读取 MEMORY.md 并主动注入相关记忆。
version: 1.0.0
tags: [memory, semantic-search, local, embeddings, faiss, vector-db, context, no-api-key]
metadata:
  openclaw:
    requires:
      bins: [python3]
---

# memory-local

**使用场景**：当需要让 Agent 跨对话记忆用户偏好、项目背景、决策历史等关键信息时使用。

**核心能力**：本地语义向量搜索，无需任何 API Key，不依赖外部服务。

## 功能特性

- ✅ **完全本地**：sentence-transformers (all-MiniLM-L6-v2) 384维向量嵌入，FAISS 向量索引
- ✅ **零 API Key**：不依赖任何第三方服务
- ✅ **持久化存储**：`~/.openclaw-memory/memories.jsonl` + FAISS 索引文件
- ✅ **语义搜索**：支持自然语言查询，返回相关性评分
- ✅ **分类管理**：支持按 category 分类存储和过滤
- ✅ **重要性加权**：importance 0-1 影响搜索权重

## 存储路径

```
~/.openclaw-memory/
├── memories.jsonl   # 记忆原始数据（每行一条JSON）
├── index.faiss     # FAISS 向量索引
├── dim.txt         # 向量维度标记
└── .model_cache/   # sentence-transformers 模型缓存
```

## 命令行工具

### 存储记忆

```bash
python3 ~/.openclaw/workspace/skills/memory-local/memory_tool.py store \
  --text "用户喜欢用中文交流" \
  --category "preference" \
  --importance 0.8
```

**参数**：
- `--text`：记忆内容（必填）
- `--category`：分类标签，默认 `general`（可选：preference/habit/project/decision/fact）
- `--importance`：重要程度 0.0-1.0，默认 0.5

**返回**：JSON `{"id": "...", "text": "...", "category": "...", "importance": ...}`

### 语义搜索

```bash
python3 ~/.openclaw/workspace/skills/memory-local/memory_tool.py search \
  --query "用户的工作习惯" \
  --limit 5 \
  --category "preference"
```

**参数**：
- `--query`：搜索query（必填）
- `--limit`：返回数量，默认 5
- `--category`：限定分类（可选）

**返回**：JSON 数组，每项包含 `id/text/category/importance/created_at/score`

### 删除记忆

```bash
# 按ID删除
python3 ~/.openclaw/workspace/skills/memory-local/memory_tool.py forget --id "uuid-here"

# 按搜索匹配删除（删除最相关的1条）
python3 ~/.openclaw/workspace/skills/memory-local/memory_tool.py forget --query "要删除的记忆" --limit 1
```

### 列出记忆

```bash
python3 ~/.openclaw/workspace/skills/memory-local/memory_tool.py list --limit 20 --category "preference"
```

## Agent 记忆注入流程

在每次 Agent 启动时，读取 `~/.openclaw/workspace/MEMORY.md` 和 `memory_local` 中的相关记忆，注入到上下文中：

1. 解析 MEMORY.md 中的关键字段（用户偏好、近期项目、设置）
2. 将关键信息存储到 memory-local（可选，需要时调用 store）
3. 当用户问及"我的偏好是什么"、"之前那个项目是关于什么的"等时，调用 search 注入相关记忆

## 分类建议

| category | 用途 |
|----------|------|
| `preference` | 用户偏好（语言、工具、时间习惯） |
| `habit` | 行为习惯 |
| `project` | 项目背景和进展 |
| `decision` | 重要决策记录 |
| `fact` | 事实性信息 |
| `general` | 默认分类 |

## 技术架构

- **Embedding 模型**：sentence-transformers `all-MiniLM-L6-v2`（90MB，384维，Apple Silicon 优化）
- **向量索引**：FAISS `IndexFlatIP`（内积度量，支持归一化向量余弦相似度）
- **存储格式**：JSON Lines（每行一条记忆，含向量）
- **Python 环境**：系统 Python 3（需已安装 sentence-transformers + faiss）

## 首次使用

首次运行时自动下载模型（约90MB），存储到 `~/.openclaw-memory/.model_cache/`，后续无需再次下载。

```bash
# 验证安装
python3 ~/.openclaw/workspace/skills/memory-local/memory_tool.py list --limit 1
```

## 依赖安装

如遇依赖缺失，执行：

```bash
pip3 install sentence-transformers faiss-cpu --break-system-packages
```
