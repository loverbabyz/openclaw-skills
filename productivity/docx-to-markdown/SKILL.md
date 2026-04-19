---
name: docx-to-markdown
description: 将 Word DOCX 文档转换为 Markdown 格式，保留标题层级、表格、列表、段落格式。适用于中文技术文档。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [docx, word, markdown, document, conversion]
    related_skills: [ocr-and-documents, nano-pdf]
---

# DOCX → Markdown 转换器

将 Word DOCX 文档转换为 Markdown 格式，保留文档结构。

## 核心特性

- **标题层级识别**：通过正则匹配章节编号（如 `1. 变更履历`、`2.1.3 自动车控`）自动识别 H1-H4
- **表格支持**：GFM Markdown 表格，多行内容用 `<br>` 保留换行
- **格式保留**：粗体、斜体、下划线、删除线
- **目录提取**：DOCX 内置目录（TOC）单格表格特殊处理

## 依赖

```bash
pip install python-docx
```

## 使用方法

### 基本用法

```bash
python scripts/docx_to_md.py <输入.docx> <输出.md>
```

### 示例

```bash
python scripts/docx_to_md.py "/path/to/文档.docx" "/path/to/文档.md"
```

## 工作原理

1. **标题识别**：文档中所有段落样式均为 `None`，章节编号完全靠文本内容本身。通过正则 `^(\d+(?:\.\d+)*)\.?\s+(.+)$` 匹配编号模式：
   - `X. 标题` → H1
   - `X.Y 标题` → H2
   - `X.Y.Z 标题` → H3
   - `X.Y.Z.W 标题` → H4

2. **表格处理**：GFM Markdown 表格，多段落单元格用 `<br>` 保留换行

3. **目录处理**：Word TOC 为 1×1 单格表格，包含多个段落，特殊处理直接提取段落文本

## 已知限制

- 图片：DOCX 内嵌图片暂未提取（如需图片，请用 `ocr-and-documents` skill 处理 PDF 版本）
- Word 内置样式：文档中段落样式均为 None，完全依赖文本内容判断标题
- 部分合并单元格（vMerge）可能渲染不完美

## 适用场景

- 中文技术文档规范从 Word 迁移到 Markdown
- 产品需求规格说明书（PRD）转换
- 技术设计文档转换
