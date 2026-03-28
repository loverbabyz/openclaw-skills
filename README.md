# OpenClaw Skills | OpenClaw 技能集合

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub repo](https://img.shields.io/badge/GitHub-loverbabyz%2Fopenclaw--skills-blue?logo=github)](https://github.com/loverbabyz/openclaw-skills)
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)

---

## Overview | 概览

OpenClaw Skills is a curated collection of AI-powered skills designed to enhance Claude Code's capabilities. This repository provides three specialized skills: automatic badge generation for README files, a fully local semantic memory system, and comprehensive README documentation generation.

OpenClaw Skills 是一套精心设计的 AI 技能集合，旨在增强 Claude Code 的能力。本仓库提供三个专用技能：自动生成 README 徽章、本地语义记忆系统，以及全面的 README 文档生成工具。

Whether you're maintaining a documentation-heavy project, need persistent context across conversations, or want professional-quality README files, these skills streamline your workflow with minimal setup.

无论您是在维护文档密集型项目、需要跨对话持久化上下文，还是想要专业级的 README 文件，这些技能都能以最少的配置简化您的工作流程。

---

## Skills | 技能

### add-badges

Detect project stack and generate shields.io README badges with live endpoints.

检测项目技术栈并通过 shields.io 实时端点生成 README 徽章。

**Features | 功能特点:**

- Automatic detection of languages, frameworks, CI/CD, and infrastructure
- 自动化检测编程语言、框架、CI/CD 和基础设施
- Dynamic badges (versions, coverage, downloads) via shields.io endpoints
- 通过 shields.io 端点获取动态徽章（版本、覆盖率、下载量）
- Support for `--profile` presets (new/active/mature/enterprise)
- 支持 `--profile` 预设配置（new/active/mature/enterprise）
- Dark mode and layout customization
- 深色模式与布局自定义
- Dry-run mode for preview before modifying files
- 文件修改前的预览模式

**Usage | 使用方法:**

```bash
uv run python skills/add-badges/scripts/detect.py <path>
```

---

### memory-local

Fully local semantic memory system using sentence-transformers + FAISS vector database. No API keys required.

基于 sentence-transformers + FAISS 向量数据库的完全本地化语义记忆系统。无需 API Key。

**Features | 功能特点:**

- 384-dimensional embeddings via `all-MiniLM-L6-v2`
- 通过 `all-MiniLM-L6-v2` 实现 384 维向量嵌入
- Semantic search with relevance scoring
- 带相关性评分的语义搜索
- Category-based organization (preference/habit/project/decision/fact)
- 基于分类组织（偏好/习惯/项目/决策/事实）
- Persistent storage in `~/.openclaw-memory/`
- 持久化存储于 `~/.openclaw-memory/`

**Commands | 命令:**

```bash
# Store a memory | 存储记忆
python3 memory_tool.py store --text "用户偏好中文交流" --category preference --importance 0.8

# Search memories | 搜索记忆
python3 memory_tool.py search --query "用户的工作习惯" --limit 5

# List memories | 列出记忆
python3 memory_tool.py list --limit 20
```

---

### readme-generator

Generate comprehensive, best-practice README.md files for GitHub repositories.

为 GitHub 仓库生成符合最佳实践的全面的 README.md 文件。

**Features | 功能特点:**

- Automatic badge generation for detected technologies
- 自动为检测到的技术生成徽章
- Site metrics collection and display
- 站点指标收集与展示
- GitHub best practices compliance
- 遵循 GitHub 最佳实践
- Getting started, structure, and contact sections
- 包含快速上手、项目结构、联系方式等章节
- README validation scripts
- README 验证脚本

---

## Site Status and Metrics | 站点状态与指标

| Metric | Count |
|--------|-------|
| Markdown Files | 9 |
| Skills | 3 |
| Python Scripts | 4 |

---

## Getting Started | 快速上手

### Installation | 安装

- Python 3.8+ (for add-badges and readme-generator)
- Python 3.8+（用于 add-badges 和 readme-generator）
- For memory-local: `sentence-transformers` and `faiss-cpu`
- memory-local 依赖：`sentence-transformers` 和 `faiss-cpu`

```bash
pip install sentence-transformers faiss-cpu
```

### Clone the Repository | 克隆仓库

```bash
git clone https://github.com/loverbabyz/openclaw-skills.git
cd openclaw-skills
```

### Using Skills in Claude Code | 在 Claude Code 中使用技能

Each skill can be invoked directly from Claude Code:

每个技能可直接在 Claude Code 中调用：

```text
Use the add-badges skill to add badges to my README
Use the memory-local skill to remember my preferences
Use the readme-generator skill to create a README
```

---

## Repository Structure | 项目结构

```text
openclaw-skills/
├── add-badges/                   # README badge generator skill | README徽章生成技能
│   ├── SKILL.md                  # Skill definition | 技能定义
│   ├── scripts/
│   │   ├── detect.py            # Stack detection script | 技术栈检测脚本
│   │   └── validate-badges.py   # Badge URL validator | 徽章URL验证器
│   ├── references/
│   │   ├── badge-catalog-core.md
│   │   ├── badge-catalog-extended.md
│   │   └── style-guide.md
│   └── evals/
│       ├── badge-detection.json
│       └── readme-insertion.json
│
├── memory-local/                 # Local semantic memory system | 本地语义记忆系统
│   ├── SKILL.md                  # Skill definition | 技能定义
│   └── memory_tool.py            # CLI tool | 命令行工具
│
└── readme-generator/             # README.md generator skill | README生成技能
    ├── SKILL.md                  # Skill definition | 技能定义
    ├── README.md                 # Skill documentation | 技能文档
    ├── scripts/
    │   ├── collect-site-metrics.py
    │   └── validate-readme.py
    └── references/
        └── badges.md
```

---

## Reporting Issues | 报告问题

Found a bug or have a suggestion? Please report it:

发现 bug 或有建议？请报告：

[GitHub Issues](https://github.com/loverbabyz/openclaw-skills/issues)

When reporting issues, please include:

报告时请提供：

- Description of the problem or suggestion | 问题或建议的描述
- Steps to reproduce (for bugs) | 复现步骤（如为 bug）
- Expected vs actual behavior | 预期与实际行为对比
- Screenshots (if applicable) | 截图（如适用）

---

## Contributing | 贡献

Contributions are welcome! To contribute:

欢迎贡献！参与方式：

1. Fork the repository | Fork 本仓库
2. Create a feature branch (`git checkout -b feature/amazing-feature`) | 创建功能分支
3. Commit your changes (`git commit -m 'Add amazing feature'`) | 提交更改
4. Push to the branch (`git push origin feature/amazing-feature`) | 推送分支
5. Open a Pull Request | 发起 Pull Request

---

## License | 许可证

This project is licensed under the MIT License.

本项目采用 MIT 许可证。

**You are free to:** | 您可以：

- Share — copy and redistribute the material | 分享 — 复制和分发素材
- Adapt — remix, transform, and build upon the material | 改编 — 混合、转换并基于素材构建

**Under the following terms:** | 须遵守以下条款：

- **Attribution** — Give appropriate credit with a link to the original
  **署名** — 提供原始链接并给予适当 credited
- **ShareAlike** — Distribute contributions under the same license
  **相同方式共享** — 以相同许可证分发贡献

---

## Acknowledgements | 致谢

This project is built on the shoulders of giants in the open source community:

本项目建立在开源社区巨人的肩膀之上：

- **[shields.io](https://shields.io/)** - Badge endpoint service for README metadata | README 元数据徽章端点服务
- **[sentence-transformers](https://www.sbert.net/)** - State-of-the-art sentence embeddings |最先进的句子嵌入库
- **[FAISS](https://github.com/facebookresearch/faiss)** - Efficient similarity search library by Meta | Meta 高效相似度搜索库
- **[Python](https://www.python.org/)** - Programming language powering the scripts | 驱动脚本的编程语言
- **[GitHub](https://github.com/)** - Platform hosting the repository and CI/CD | 托管仓库和 CI/CD 的平台

---

## Contact | 联系方式

**OpenClaw Project**

- GitHub: [@loverbabyz](https://github.com/loverbabyz)
- Repository: [loverbabyz/openclaw-skills](https://github.com/loverbabyz/openclaw-skills)

Questions, suggestions, or collaboration opportunities? Feel free to open an issue or reach out on GitHub.

问题、建议或合作机会？欢迎在 GitHub 上提交 issue 或联系。
