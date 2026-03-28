# OpenClaw 技能集合

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub repo](https://img.shields.io/badge/GitHub-loverbabyz%2Fopenclaw--skills-blue?logo=github)](https://github.com/loverbabyz/openclaw-skills)
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)

🇺🇸 [English Version](../README.md)

---

## 概览

OpenClaw Skills 是一套精心设计的 AI 技能集合，旨在增强 Claude Code 的能力。本仓库提供三个专用技能：自动生成 README 徽章、本地语义记忆系统，以及全面的 README 文档生成工具。

无论您是在维护文档密集型项目、需要跨对话持久化上下文，还是想要专业级的 README 文件，这些技能都能以最少的配置简化您的工作流程。

## 技能

### add-badges

检测项目技术栈并通过 shields.io 实时端点生成 README 徽章。

**功能特点:**

- 自动化检测编程语言、框架、CI/CD 和基础设施
- 通过 shields.io 端点获取动态徽章（版本、覆盖率、下载量）
- 支持 `--profile` 预设配置（new/active/mature/enterprise）
- 深色模式与布局自定义
- 文件修改前的预览模式

**使用方法:**

```bash
uv run python skills/add-badges/scripts/detect.py <path>
```

### memory-local

基于 sentence-transformers + FAISS 向量数据库的完全本地化语义记忆系统。无需 API Key。

**功能特点:**

- 通过 `all-MiniLM-L6-v2` 实现 384 维向量嵌入
- 带相关性评分的语义搜索
- 基于分类组织（偏好/习惯/项目/决策/事实）
- 持久化存储于 `~/.openclaw-memory/`

**命令:**

```bash
# 存储记忆
python3 memory_tool.py store --text "用户偏好中文交流" --category preference --importance 0.8

# 搜索记忆
python3 memory_tool.py search --query "用户的工作习惯" --limit 5

# 列出记忆
python3 memory_tool.py list --limit 20
```

### readme-generator

为 GitHub 仓库生成符合最佳实践的全面的 README.md 文件。

**功能特点:**

- 自动为检测到的技术生成徽章
- 站点指标收集与展示
- 遵循 GitHub 最佳实践
- 包含快速上手、项目结构、联系方式等章节
- README 验证脚本

## 站点状态与指标

| 指标 | 数量 |
|------|------|
| Markdown 文件 | 9 |
| 技能数量 | 3 |
| Python 脚本 | 4 |

## 快速上手

### 安装

- Python 3.8+（用于 add-badges 和 readme-generator）
- memory-local 依赖：`sentence-transformers` 和 `faiss-cpu`

```bash
pip install sentence-transformers faiss-cpu
```

### 克隆仓库

```bash
git clone https://github.com/loverbabyz/openclaw-skills.git
cd openclaw-skills
```

### 在 Claude Code 中使用技能

每个技能可直接在 Claude Code 中调用：

```text
Use the add-badges skill to add badges to my README
Use the memory-local skill to remember my preferences
Use the readme-generator skill to create a README
```

## 项目结构

```text
openclaw-skills/
├── add-badges/                   # README 徽章生成技能
│   ├── SKILL.md                  # 技能定义
│   ├── scripts/
│   │   ├── detect.py            # 技术栈检测脚本
│   │   └── validate-badges.py   # 徽章 URL 验证器
│   ├── references/
│   │   ├── badge-catalog-core.md
│   │   ├── badge-catalog-extended.md
│   │   └── style-guide.md
│   └── evals/
│       ├── badge-detection.json
│       └── readme-insertion.json
│
├── memory-local/                 # 本地语义记忆系统
│   ├── SKILL.md                  # 技能定义
│   └── memory_tool.py            # 命令行工具
│
└── readme-generator/             # README 生成技能
    ├── SKILL.md                  # 技能定义
    ├── README.md                 # 技能文档
    ├── scripts/
    │   ├── collect-site-metrics.py
    │   └── validate-readme.py
    └── references/
        └── badges.md
```

## 报告问题

发现 bug 或有建议？请报告：

[GitHub Issues](https://github.com/loverbabyz/openclaw-skills/issues)

报告时请提供：

- 问题或建议的描述
- 复现步骤（如为 bug）
- 预期与实际行为对比
- 截图（如适用）

## 贡献

欢迎贡献！参与方式：

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 发起 Pull Request

## 许可证

本项目采用 MIT 许可证。

**您可以：**

- 分享 — 复制和分发素材
- 改编 — 混合、转换并基于素材构建

**须遵守以下条款：**

- **署名** — 提供原始链接并给予适当 credited
- **相同方式共享** — 以相同许可证分发贡献

## 致谢

本项目建立在开源社区巨人的肩膀之上：

- **[shields.io](https://shields.io/)** - README 元数据徽章端点服务
- **[sentence-transformers](https://www.sbert.net/)** - 最先进的句子嵌入库
- **[FAISS](https://github.com/facebookresearch/faiss)** - Meta 高效相似度搜索库
- **[Python](https://www.python.org/)** - 驱动脚本的编程语言
- **[GitHub](https://github.com/)** - 托管仓库和 CI/CD 的平台

## 联系方式

**OpenClaw 项目**

- GitHub: [@loverbabyz](https://github.com/loverbabyz)
- 仓库: [loverbabyz/openclaw-skills](https://github.com/loverbabyz/openclaw-skills)

问题、建议或合作机会？欢迎在 GitHub 上提交 issue 或联系。
