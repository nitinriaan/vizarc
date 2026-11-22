# 📐 VizArc

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=Streamlit&logoColor=white)](https://streamlit.io)
[![Built for AI Agents](https://img.shields.io/badge/Agent%20Skill-Claude%20%7C%20Antigravity%20%7C%20Cursor-purple.svg)](#-using-as-an-ai-agent-skill)

> **Turn any idea, plan, or codebase into a beautiful interactive architecture diagram and one-page explainer.**  
> An agent skill and developer tool that compiles complex systems into self-contained, interactive `.html` files featuring **upstream/downstream link tracing**, **component search**, **pan & zoom**, and **node detail drawers**.

---

## ⚡ Why VizArc?

| Feature | Standard LLMs (Mermaid/Text) | Graphify | **VizArc** |
| :--- | :--- | :--- | :--- |
| **Output Type** | Static text strings (often broken) | Generic AST node graph | **✨ Standalone Interactive HTML Canvas** |
| **Link Tracing** | ❌ None | ❌ None | ✅ **Upstream & downstream dependency tracing** |
| **Inspection Drawer** | ❌ None | ❌ None | ✅ **Click nodes to view tech stack, role & files** |
| **Component Search** | ❌ None | ❌ None | ✅ **Instant live filtering & node highlighting** |
| **Multi-Format** | Mermaid only | Node graph only | ✅ **HTML, Mermaid, D2 Lang, ASCII, Excalidraw** |
| **Zero-Budget Hosting** | Paid subscriptions | Self-hosted servers | ✅ **100% Free: Single `.html` file or Streamlit on HF** |

---

## 🌟 Interactive Features (Inside `architecture.html`)

When you run VizArc, it generates a single, standalone `.html` file that opens in any browser with **zero build steps and zero dependencies**:

1. **🔍 Interactive Canvas:** Drag to pan around large system topologies, scroll to zoom in/out smoothly.
2. **🎯 Upstream & Downstream Link Tracing:** Click any service (e.g. `Auth Service`), and VizArc highlights every component that calls it (green) and every service it calls (orange) with glowing paths, while dimming unrelated nodes.
3. **📋 Component Detail Drawer:** Click any service to inspect its description, tech stack badge (e.g., `FastAPI`, `PostgreSQL`), associated source code files, and connection endpoints.
4. **🔎 Live Component Search:** Search for any database, cache, or service name in the top bar to instantly highlight it on the canvas.
5. **🌓 Dark & Light Modes + SVG Export:** Built-in theme switcher and one-click SVG export for documentation.

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

### Generate an Interactive HTML Explainer from a Description
```bash
# Generates architecture.html and opens it in your browser
python cli.py generate "Microservices payment platform with Stripe, Kafka, and Postgres" --open
```

### Scan a Local Repository & Compile Architecture Map
```bash
# Automatically detects frameworks, routes, and Docker configs
python cli.py scan . --format html --output architecture.html
```

### Export to Other Formats
```bash
# Cloud architecture in D2 Lang
python cli.py generate "AWS serverless topology with Lambda and DynamoDB" --format d2

# Terminal ASCII diagram for PR comments or code comments
python cli.py generate "OAuth2 Auth Flow" --format ascii

# Standard Mermaid syntax for GitHub READMEs
python cli.py generate "E-Commerce System" --format mermaid
```

---

## 🌐 Free Web Playground (Streamlit)

Test prompts and explore interactive diagrams directly in your browser:

```bash
streamlit run app.py
```

* Includes preloaded templates (*E-Commerce Microservices*, *OAuth2 Auth*, *Real-time WebSockets*, *SaaS ERD*).
* Interactive iframe canvas with full pan/zoom and link tracing.
* One-click "Download Standalone HTML Explainer" button.

---

## 🤖 Using as an AI Agent Skill (Claude Code & Antigravity)

VizArc is built from the ground up as a native **Agent Skill**:
1. Copy [`SKILL.md`](./SKILL.md) into your project's `.agents/skills/vizarc/` (or Claude Code skill directory).
2. Now, whenever you tell your agent:
   > *"VizArc this codebase's architecture into an interactive explainer"*  
   > *"Explain the data flow of our payment pipeline"*
   
   The agent automatically compiles a structured JSON IR and outputs `architecture.html` for you to double-click and explore!

---

## 📦 Project Layout

```text
vizarc/
├── src/
│   └── vizarc/              # Core Python package (Standard src layout)
│       ├── __init__.py
│       ├── engine.py        # Gemini Flash orchestration + offline demo
│       ├── ir.py            # Typed JSON Intermediate Representation (IR)
│       ├── compiler.py      # Standalone Interactive HTML Compiler Engine
│       ├── analyzer.py      # Local repository scanner
│       └── formats/
│           ├── mermaid.py   # Mermaid generator & self-healing sanitizer
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

MIT License. Free to use for personal projects, team documentation, and open-source workflows!
