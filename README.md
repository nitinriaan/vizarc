# 📐 VizArc

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=Streamlit&logoColor=white)](https://streamlit.io)
[![Built for AI Agents](https://img.shields.io/badge/Agent%20Skill-Claude%20%7C%20Antigravity-purple.svg)](#-using-as-an-ai-agent-skill)

> **AI-Powered Software Architecture & System Diagram Engine for Developers & AI Coding Agents.**  
> Transform complex ideas, SQL schemas, and local codebases into production-grade **Mermaid.js**, **D2 Lang**, **ASCII**, and **Excalidraw** diagrams with self-healing syntax validation.

---

## ⚡ Why VizArc? (VizArc vs. Graphify)

| Feature | Graphify | Vanilla LLMs (ChatGPT/Claude) | **VizArc** |
| :--- | :--- | :--- | :--- |
| **Output Formats** | Generic node graph only | Mermaid (frequently breaks) | **Mermaid, D2, ASCII, Excalidraw** |
| **Self-Healing Engine** | ❌ None | ❌ None (syntax errors crash render) | ✅ **Auto-sanitizes unescaped characters & quotes** |
| **Codebase Scanning** | Basic file tree linking | ❌ Needs manual copy-paste | ✅ **Scans framework, routes, models & infra** |
| **Agent Skill Support** | ❌ No | ❌ No | ✅ **Drop-in `SKILL.md` for Claude & Antigravity** |
| **Zero-Budget Hosting** | Needs server setup | Web subscription | ✅ **$0 Free deployment on Hugging Face / Streamlit** |

---

## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/your-username/vizarc.git
cd vizarc
pip install -r requirements.txt
```

### 2. Configure Free Gemini API Key
Get your free API key from [Google AI Studio](https://aistudio.google.com/):
```bash
cp .env.example .env
# Edit .env and paste: GEMINI_API_KEY=your_key_here
```
*(Note: VizArc also includes a built-in offline demo mode if no key is provided!)*

---

## 💻 CLI Usage

### Generate from a Description
```bash
# Architecture diagram in Mermaid (default)
python cli.py generate "Microservices payment system with Stripe, Kafka, and Postgres"

# Cloud architecture in D2 Lang
python cli.py generate "AWS serverless stack with Lambda, DynamoDB, and API Gateway" --format d2

# Terminal ASCII diagram for PR comments
python cli.py generate "OAuth2 Authorization Flow" --format ascii

# Sequence diagram
python cli.py generate "User signup with email verification" --archetype sequence
```

### Scan a Local Repository & Generate Architecture
VizArc automatically discovers frameworks, routes, models, and Docker configs in your project:
```bash
# Scans current directory and outputs ARCHITECTURE.md
python cli.py scan . --format mermaid --output ARCHITECTURE.md
```

---

## 🌐 Free Web Playground (Streamlit)

Run the interactive browser interface locally or deploy it to Hugging Face Spaces for $0:

```bash
streamlit run app.py
```

Features:
- **Two-Column Real-Time Studio**: Type or paste requirements on the left, watch live diagram render on the right.
- **Preset Gallery**: One-click load templates (E-Commerce Microservices, OAuth2, Real-time Chat, SaaS ERD).
- **GitHub Markdown Export**: One-click copy code block for your project's `README.md`.

---

## 🤖 Using as an AI Agent Skill (Claude Code & Antigravity)

VizArc is built from the ground up as a native **Agent Skill**:
1. Copy [`SKILL.md`](./SKILL.md) into your project's `.agents/skills/vizarc/` (or Claude Code skill directory).
2. Now, whenever you tell your agent:
   > *"VizArc this repository's backend architecture"*  
   > *"Generate a D2 diagram for this new auth service"*
   
   The agent will invoke the skill's instructions, ensuring error-free syntax, proper subgraph grouping, and clean component boundaries.

---

## 📦 Project Layout

```text
vizarc/
├── src/
│   └── vizarc/              # Core Python package (Standard src layout)
│       ├── __init__.py
│       ├── engine.py        # Gemini Flash orchestration
│       ├── analyzer.py      # Local repository scanner
│       └── formats/
│           ├── mermaid.py   # Mermaid.js generator & sanitizer
│           ├── d2.py        # D2 Lang formatter
│           ├── ascii.py     # Unicode/ASCII box diagram generator
│           └── excalidraw.py# Excalidraw-compatible schema builder
├── app.py                   # Streamlit Web Playground
├── cli.py                   # CLI tool (generate & scan commands)
├── SKILL.md                 # Agent Skill definition (Claude Code & Antigravity)
├── requirements.txt
├── .env.example
└── README.md
```

---

## 📄 License

MIT License. Feel free to use in personal projects, commercial setups, or open-source tools!
