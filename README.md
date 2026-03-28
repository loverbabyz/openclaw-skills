# OpenClaw Skills

A collection of Claude AI skills for the OpenClaw project — enabling badge generation, semantic memory, and automated documentation.

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
```
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

## Repository Structure

```
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

## Getting Started

### Prerequisites

- Python 3.8+ (for add-badges and readme-generator)
- For memory-local: `sentence-transformers` and `faiss-cpu`

```bash
pip install sentence-transformers faiss-cpu
```

### Using Skills in Claude Code

Each skill can be invoked directly from Claude Code:

```
Use the add-badges skill to add badges to my README
Use the memory-local skill to remember my preferences
Use the readme-generator skill to create a README
```

## License

MIT License
