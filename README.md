# 📐 VizArc: Universal Software Architecture Compiler

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=Streamlit&logoColor=white)](https://streamlit.io)
[![Built for AI Agents](https://img.shields.io/badge/Agent%20Skill-Claude%20%7C%20Antigravity%20%7C%20Cursor-purple.svg)](#-using-as-an-ai-agent-skill)

> **The "Pandoc of Software Architecture"**  
> Turn any prompt, plan, or codebase into a **Canonical Architecture Model (JSON IR)**, and deterministically compile it into **Interactive HTML, D2 Lang, Structurizr C4, Mermaid, PlantUML, Graphviz (DOT), Excalidraw, and ASCII** in one single pass.

---

## 🏛️ The Architecture: Universal Compiler Pattern

VizArc uses the same decoupled compiler architecture as **LLVM** and **Pandoc**. The AI analyzes your codebase or system requirements **once** to generate a single structured Canonical Model (AST/IR). Dedicated deterministic rendering adapters then compile that model into any visual format with **zero syntax hallucinations and zero extra LLM calls**.

```
                   User Prompt / Codebase Scan
                                │
                                ▼
                   [AI Architecture Analyzer]
                                │ (1 Single LLM Call)
                                ▼
               ┌─────────────────────────────────┐
               │    Canonical Architecture IR    │
               │         (Pure JSON AST)         │
               └────────────────┬────────────────┘
                                │
    ┌───────────┬───────────┬───┴───────┬───────────┬────────────┬─────────────┐
    ▼           ▼           ▼           ▼           ▼            ▼             ▼
[Interactive]  [D2]     [Mermaid]  [Structurizr] [PlantUML]  [Graphviz]  [Excalidraw]  [ASCII]
   HTML                    (C4)       (DOT)
```

---

## 🎨 Supported Rendering Engines

| Format / Engine | Best Use | Visual Quality | File Output |
| :--- | :--- | :--- | :--- |
| **✨ Interactive HTML** | Deep system exploration, upstream/downstream link tracing, search & node drawer | Exceptional (Vector) | `.html` |
| **⚡ D2 Lang** | Modern declarative system architecture, container grouping, cloud topologies | Excellent | `.d2` |
| **🏛️ Structurizr DSL** | Professional **C4 architecture models** (Context, Container, Component) | Excellent | `.dsl` |
| **🧜‍♂️ Mermaid.js** | GitHub READMEs, Notion, pull request markdown, GitLab | Good | `.mmd` / `.md` |
| **📐 PlantUML** | Classical enterprise UML and sequence component diagrams | Good | `.puml` |
| **🕸️ Graphviz (DOT)** | Dependency trees, high-density relationship mapping | Good | `.dot` |
| **🎨 Excalidraw** | Hand-drawn whiteboard diagrams, team collaborative sketches | Distinctive | `.excalidraw.mmd` |
| **📟 ASCII / Unicode** | Monospaced terminal outputs, code docstrings, git commit notes | Terminal-native | `.txt` |

---

## 🌟 Flagship: Interactive One-Page Explainer

When compiling to HTML (`architecture.html`), VizArc generates a single, self-contained file that runs in any browser with **zero dependencies**:

* **🔍 Interactive Canvas:** Infinite pan & smooth zoom.
* **🎯 Upstream & Downstream Link Tracing:** Click any service (e.g. `Auth Service`), and VizArc:
  * Highlights every component that calls it (**green Upstream badge**).
  * Highlights every service it calls (**orange Downstream badge**).
  * Causes connecting data flow paths to glow while dimming unrelated nodes.
* **📋 Component Detail Drawer:** Click to inspect role descriptions, tech stack tags, connected files, and API endpoints.
* **🔎 Live Component Search:** Filter and locate any component in real time.
* **🌓 Dark & Light Modes + SVG Export:** Built-in theme switcher and one-click SVG export.

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
git clone https://github.com/nitinriaan/vizarc.git
cd vizarc
pip install -r requirements.txt
```

### 2. (Optional) Configure Free Gemini API Key
Get your free API key from [Google AI Studio](https://aistudio.google.com/):
```bash
cp .env.example .env
# Edit .env and paste: GEMINI_API_KEY=your_key_here
```
*(Note: VizArc has a built-in offline engine, so you can test and explore immediately without an API key!)*

---

## 💻 CLI Usage

### Compile to All 8 Formats in One Shot
```bash
# Compiles HTML, D2, Structurizr C4, Mermaid, PlantUML, Graphviz, Excalidraw, and ASCII
python cli.py generate "Microservices payment platform with Stripe, Kafka, and Postgres" --format all --output ./dist
```

### Compile to a Specific Format
```bash
# Interactive HTML Explainer (default)
python cli.py generate "E-commerce system" --format html --open

# Modern D2 Lang
python cli.py generate "AWS cloud topology with ECS and Aurora" --format d2

# Structurizr C4 Architecture DSL
python cli.py generate "Banking system architecture" --format structurizr

# Terminal ASCII diagram
python cli.py generate "OAuth2 Authorization Flow" --format ascii
```

### Scan a Local Codebase & Compile
```bash
# Automatically detects frameworks, routes, models, and Docker configs
python cli.py scan . --format all --output ./architecture_docs
```

---

## 🌐 Free Web Playground (Streamlit)

Launch the multi-renderer studio locally or deploy for $0 on Hugging Face Spaces:

```bash
streamlit run app.py
```

* Multi-tab viewer: Switch between **Interactive Canvas, D2, Structurizr C4, Mermaid, PlantUML, Graphviz, Excalidraw, ASCII, and Canonical JSON IR** with zero latency.
* Preset gallery (*E-Commerce, OAuth2, WebSockets, SaaS Billing*).
* One-click download for Standalone HTML Explainers.

---

## 🤖 Using as an AI Agent Skill (Claude Code & Antigravity)

VizArc is built from the ground up as a native **Agent Skill**:
1. Copy [`SKILL.md`](./SKILL.md) into your project's `.agents/skills/vizarc/` (or Claude Code skill directory).
2. Ask your AI coding assistant:
   > *"VizArc this repository into an interactive explainer and C4 architecture"*  
   > *"Export our service dependencies to D2 and Structurizr"*

The agent will generate the Canonical IR and compile it into whichever format you prefer.

---

## 📦 Project Layout

```text
vizarc/
├── src/
│   └── vizarc/              # Core Python package (Standard src layout)
│       ├── __init__.py
│       ├── engine.py        # Universal Architecture Compiler orchestration
│       ├── ir.py            # Canonical Architecture Model (JSON AST)
│       ├── compiler.py      # Standalone Interactive HTML Canvas Compiler
│       ├── analyzer.py      # Local repository scanner
│       └── adapters/        # 8 Deterministic Rendering Adapters
│           ├── base.py
│           ├── html_adapter.py        # Interactive HTML with link tracing
│           ├── d2_adapter.py          # D2 Lang
│           ├── structurizr_adapter.py # Structurizr C4 DSL
│           ├── mermaid_adapter.py     # Mermaid.js
│           ├── plantuml_adapter.py    # PlantUML Component/C4
│           ├── graphviz_adapter.py    # Graphviz DOT
│           ├── excalidraw_adapter.py  # Excalidraw
│           └── ascii_adapter.py       # Terminal Unicode Boxes
├── app.py                   # Streamlit Multi-Renderer Playground
├── cli.py                   # CLI tool (generate & scan commands)
├── SKILL.md                 # Agent Skill definition (Claude Code & Antigravity)
├── requirements.txt
├── .env.example
└── README.md
```

---

## 📄 License

MIT License. Free to use for personal projects, enterprise architecture, and open-source documentation!
