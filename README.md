# OpenClaw Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub repo](https://img.shields.io/badge/GitHub-loverbabyz%2Fopenclaw--skills-blue?logo=github)](https://github.com/loverbabyz/openclaw-skills)
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)

🇨🇳 [中文版本](README_zh.md)

---

## Overview

OpenClaw Skills is a curated collection of AI-powered skills designed to enhance Claude Code's capabilities. This repository provides three specialized skills: automatic badge generation for README files, a fully local semantic memory system, and comprehensive README documentation generation.

Whether you're maintaining a documentation-heavy project, need persistent context across conversations, or want professional-quality README files, these skills streamline your workflow with minimal setup.

## Skills

### add-badges

Detect project stack and generate shields.io README badges with live endpoints.

**Features:**

- Automatic detection of languages, frameworks, CI/CD, and infrastructure
- Dynamic badges (versions, coverage, downloads) via shields.io endpoints
- Support for `--profile` presets (new/active/mature/enterprise)
- Dark mode and layout customization
- Dry-run mode for preview before modifying files

**Usage:**

```bash
uv run python skills/add-badges/scripts/detect.py <path>
```

### memory-local

Fully local semantic memory system using sentence-transformers + FAISS vector database. No API keys required.

**Features:**

- 384-dimensional embeddings via `all-MiniLM-L6-v2`
- Semantic search with relevance scoring
- Category-based organization (preference/habit/project/decision/fact)
- Persistent storage in `~/.openclaw-memory/`

**Commands:**

```bash
# Store a memory
python3 memory_tool.py store --text "用户偏好中文交流" --category preference --importance 0.8

# Search memories
python3 memory_tool.py search --query "用户的工作习惯" --limit 5

# List memories
python3 memory_tool.py list --limit 20
```

### readme-generator

Generate comprehensive, best-practice README.md files for GitHub repositories.

**Features:**

- Automatic badge generation for detected technologies
- Site metrics collection and display
- GitHub best practices compliance
- Getting started, structure, and contact sections
- README validation scripts

## Site Status and Metrics

| Metric | Count |
|--------|-------|
| Markdown Files | 9 |
| Skills | 3 |
| Python Scripts | 4 |

## Getting Started

### Installation

- Python 3.8+ (for add-badges and readme-generator)
- For memory-local: `sentence-transformers` and `faiss-cpu`

```bash
pip install sentence-transformers faiss-cpu
```

### Clone the Repository

```bash
git clone https://github.com/loverbabyz/openclaw-skills.git
cd openclaw-skills
```

### Using Skills in Claude Code

Each skill can be invoked directly from Claude Code:

```text
Use the add-badges skill to add badges to my README
Use the memory-local skill to remember my preferences
Use the readme-generator skill to create a README
```

## Repository Structure

```text
openclaw-skills/
├── add-badges/                   # README badge generator skill
│   ├── SKILL.md                  # Skill definition
│   ├── scripts/
│   │   ├── detect.py            # Stack detection script
│   │   └── validate-badges.py   # Badge URL validator
│   ├── references/
│   │   ├── badge-catalog-core.md
│   │   ├── badge-catalog-extended.md
│   │   └── style-guide.md
│   └── evals/
│       ├── badge-detection.json
│       └── readme-insertion.json
│
├── memory-local/                 # Local semantic memory system
│   ├── SKILL.md                  # Skill definition
│   └── memory_tool.py            # CLI tool (store/search/list/forget)
│
└── readme-generator/             # README.md generator skill
    ├── SKILL.md                  # Skill definition
    ├── README.md                 # Skill documentation
    ├── scripts/
    │   ├── collect-site-metrics.py
    │   └── validate-readme.py
    └── references/
        └── badges.md
```

## Reporting Issues

Found a bug or have a suggestion? Please report it:

[GitHub Issues](https://github.com/loverbabyz/openclaw-skills/issues)

When reporting issues, please include:

- Description of the problem or suggestion
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Screenshots (if applicable)

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

**You are free to:**

- Share — copy and redistribute the material
- Adapt — remix, transform, and build upon the material

**Under the following terms:**

- **Attribution** — Give appropriate credit with a link to the original
- **ShareAlike** — Distribute contributions under the same license

## Acknowledgements

This project is built on the shoulders of giants in the open source community:

- **[shields.io](https://shields.io/)** - Badge endpoint service for README metadata
- **[sentence-transformers](https://www.sbert.net/)** - State-of-the-art sentence embeddings
- **[FAISS](https://github.com/facebookresearch/faiss)** - Efficient similarity search library by Meta
- **[Python](https://www.python.org/)** - Programming language powering the scripts
- **[GitHub](https://github.com/)** - Platform hosting the repository and CI/CD

## Contact

**OpenClaw Project**

- GitHub: [@loverbabyz](https://github.com/loverbabyz)
- Repository: [loverbabyz/openclaw-skills](https://github.com/loverbabyz/openclaw-skills)

Questions, suggestions, or collaboration opportunities? Feel free to open an issue or reach out on GitHub.
