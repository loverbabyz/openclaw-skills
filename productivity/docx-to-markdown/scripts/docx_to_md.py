#!/usr/bin/env python3
"""
DOCX → Markdown 转换器 - 基于 python-docx
专为中文技术文档设计，保留：标题层级、表格、列表、段落格式（粗体/斜体）

核心策略：Word 文档中所有段落样式均为 None（无样式），
通过正则匹配编号模式来识别标题层级。
"""

import sys
import re
from typing import Optional, Tuple, List
from docx import Document


# ---------------------------------------------------------------
# 标题层级识别
# ---------------------------------------------------------------
# 匹配: "1. 变更履历", "2.1 整体系统架构", "2.8.1 主模块", "3.1.2.1 车控"
HEADING_PATTERN = re.compile(r'^(\d+(?:\.\d+)*)\.?\s+(.+)$')

def get_heading_level(text: str) -> Optional[Tuple[int, str]]:
    """识别章节标题及层级。返回 (level, title) 或 None。"""
    m = HEADING_PATTERN.match(text.strip())
    if not m:
        return None

    number_part = m.group(1)
    title_text = m.group(2).strip()

    # 过滤非章节标题关键词
    skip_keywords = [
        "版本号", "修订人", "修订日期", "修订内容",
        "ECU最大响应时间", "Function ID", "Action ID",
        "Bit Offset", "Bit Value", "描述", "建议处理方式", "提示语参考",
    ]
    for kw in skip_keywords:
        if title_text.startswith(kw):
            return None

    parts = [p for p in number_part.split(".") if p]
    if not parts:
        return None

    level = {1: 1, 2: 2, 3: 3}.get(len(parts), 4 if len(parts) >= 4 else 1)
    return level, title_text


# ---------------------------------------------------------------
# 文本格式化
# ---------------------------------------------------------------

def get_paragraph_text(para, strip_formatting: bool = False) -> str:
    """获取段落文本。
    
    Args:
        para: 段落对象
        strip_formatting: 若为 True，则忽略粗体/斜体标记，用于标题和文档标题。
    """
    result = ""
    for run in para.runs:
        text = run.text
        if not text:
            continue
        if strip_formatting:
            # 标题/文档名：去掉所有格式标记
            pass
        else:
            if run.font.underline:
                text = f"<u>{text}</u>"
            if run.font.strike:
                text = f"~~{text}~~"
            if run.bold and run.italic:
                text = f"***{text}***"
            elif run.bold:
                text = f"**{text}**"
            elif run.italic:
                text = f"*{text}*"
        result += text
    return result


# ---------------------------------------------------------------
# 表格转换
# ---------------------------------------------------------------

def extract_table_markdown(table) -> str:
    """将 Word 表格转为 Markdown 表格"""
    rows = table.rows
    if not rows:
        return ""

    col_count = max(len(row.cells) for row in rows)
    lines = []

    for row_idx, row in enumerate(rows):
        cells = row.cells
        cell_texts = []
        for cell in cells:
            # 直接用 cell.text，将换行转为 <br>（GFM 表格支持 HTML）
            cell_text = cell.text.replace("\r", "").replace("|", "\\|").replace("\n", "<br>")
            cell_texts.append(cell_text)

        # 补齐 / 截断到统一列数
        while len(cell_texts) < col_count:
            cell_texts.append("")
        cell_texts = cell_texts[:col_count]

        if row_idx == 0:
            lines.append("| " + " | ".join(cell_texts) + " |")
            lines.append("| " + " | ".join(["---"] * col_count) + " |")
        else:
            lines.append("| " + " | ".join(cell_texts) + " |")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------
# 建立 doc.tables element → table 对象的映射
# ---------------------------------------------------------------

def build_table_map(doc: Document):
    """建立 table element id → table 对象的映射"""
    return {id(t._element): t for t in doc.tables}


# ---------------------------------------------------------------
# 主转换逻辑
# ---------------------------------------------------------------

def convert_docx_to_markdown(doc_path: str, output_path: str):
    doc = Document(doc_path)
    table_map = build_table_map(doc)

    md_lines: List[str] = []
    blank_count = 0

    for elem in doc.element.body:
        tag = elem.tag.split("}")[-1]

        if tag == "p":
            # 找对应段落
            para = None
            for p in doc.paragraphs:
                if p._element is elem:
                    para = p
                    break
            if para is None:
                continue

            text = get_paragraph_text(para).strip()
            if not text:
                blank_count = 0
                continue

            # 文档第一行（标题）
            if para is doc.paragraphs[0]:
                md_lines.append(text + "\n")
                continue

            heading_info = get_heading_level(text)
            if heading_info:
                level, title = heading_info
                md_lines.append("#" * level + " " + title + "\n")
                prev_was_heading = True
            else:
                style_name = para.style.name if para.style and para.style.name else ""
                if "List" in style_name or "Numbering" in style_name:
                    md_lines.append("- " + text + "\n")
                else:
                    md_lines.append(text + "\n")
                prev_was_heading = False

        elif tag == "tbl":
            table = table_map.get(id(elem))
            if table:
                # 单格表格 = 目录，提取其段落文本而非渲染表格
                if len(table.rows) == 1 and len(table.rows[0].cells) == 1:
                    for p in table.rows[0].cells[0].paragraphs:
                        t = get_paragraph_text(p).strip()
                        if t:
                            md_lines.append(t + "\n")
                    blank_count = 0
                    continue

                md_lines.append(extract_table_markdown(table))
                md_lines.append("\n")
                blank_count = 0

        elif tag == "bookmarkStart":
            # 忽略书签标记
            continue

    # 清理连续空行（最多保留2个）
    cleaned = []
    blank_count = 0
    for line in md_lines:
        if not line.strip():
            blank_count += 1
            if blank_count <= 2:
                cleaned.append("")
        else:
            blank_count = 0
            cleaned.append(line.rstrip())

    md_content = "\n".join(cleaned)

    # 去掉标题中多余的 ** 包裹（如 "# **变更履历**" → "# 变更履历"）
    lines = md_content.split("\n")
    fixed = []
    for line in lines:
        # Markdown 标题行: 前面是 # ，中间是 **xxx**，去掉 ** 
        m = re.match(r'^(#{1,6})\s+\*\*(.+)\*\*$', line)
        if m:
            line = m.group(1) + " " + m.group(2)
        # 文档标题行: **T68...** → T68...
        m2 = re.match(r'^\*\*T68.+?\*\*$', line)
        if m2:
            line = line.strip("*")
        fixed.append(line)
    md_content = "\n".join(fixed)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    # 统计
    h1 = sum(1 for l in md_lines if l.startswith("# ") and not l.startswith("## "))
    h2 = sum(1 for l in md_lines if l.startswith("## ") and not l.startswith("### "))
    h3 = sum(1 for l in md_lines if l.startswith("### ") and not l.startswith("#### "))
    h4 = sum(1 for l in md_lines if l.startswith("#### "))
    table_blocks = sum(1 for l in md_lines if l.startswith("|") and "---" not in l)

    print(f"转换完成：{output_path}")
    print(f"H1: {h1}, H2: {h2}, H3: {h3}, H4: {h4}, 表格: {table_blocks}")
    print(f"总字符: {len(md_content):,}, 总行数: {md_content.count(chr(10)) + 1:,}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python docx_to_md.py <输入.docx> <输出.md>")
        sys.exit(1)
    convert_docx_to_markdown(sys.argv[1], sys.argv[2])
