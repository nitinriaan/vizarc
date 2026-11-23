# 📐 VizArc: Universal Software Architecture Compiler

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=Streamlit&logoColor=white)](https://streamlit.io)
[![Built for AI Agents](https://img.shields.io/badge/Agent%20Skill-Claude%20%7C%20Antigravity%20%7C%20Cursor-purple.svg)](#-using-as-an-ai-agent-skill)
[![GitHub Action](https://img.shields.io/badge/GitHub%20Action-PR%20Diagrams-black?logo=github)](.github/workflows/vizarc-diagram.yml)

> **The "Pandoc of Software Architecture"**  
> Turn any prompt, plan, or codebase into a **Canonical Architecture Model (JSON IR)**, and deterministically compile it into **Interactive HTML, Pure Vector SVG, D2 Lang, Structurizr C4, Mermaid, PlantUML, Graphviz (DOT), Excalidraw, and ASCII** in one single pass.

---

## 🚀 What Makes VizArc Different?

Unlike tools that rely on the LLM to write syntax for every format independently (causing syntax bugs, missing tags, and inconsistent diagrams), VizArc implements the **Universal Compiler Pattern** (inspired by LLVM, Pandoc, and tools like [Archify](https://archify.si/) & [VizArch](https://github.com/hemv-857/vizarch)):

* 🧠 **Single Source of Truth**: The AI analyzes your codebase or system requirements **once** to produce a typed, validated **Canonical Architecture Model (JSON AST/IR)**.
* ⚡ **Deterministic Multi-Renderer Compilation**: 9 specialized adapters transform the IR into any diagram language with **zero extra LLM calls and zero hallucinated syntax**.
* ☁️ **188+ Cloud Service Icons**: Automatic cloud provider detection (AWS, GCP, Azure, Kubernetes, Generic) with official brand colors, 24x24 SVG path glyphs, and [Structurizr Themes Playground](https://playground.structurizr.com/themes) tags & icons.
* 🏛️ **Full Structurizr Themes Integration**: Automatically applies C4 tags and imports prebuilt themes (`amazon-web-services-2023.01`, `google-cloud-platform-v1.5`, `microsoft-azure-2023.01`, `kubernetes-v0.3`).
* 📦 **13 Built-in Architecture Presets**: Instant offline templates for RAG Systems, Serverless AWS, Kafka Event Streaming, Kubernetes Platforms, Microservices, and more.
* 🤖 **GitHub Actions Automation**: Auto-generates architecture diagrams and posts SVG comments directly to your Pull Requests.

---

## 🏛️ Compiler Pipeline

```
                     User Prompt / Codebase Scan / Preset
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
     ┌───────────┬───────────┬────────┼───────────┬───────────┬────────────┬─────────────┬───────────┐
     ▼           ▼           ▼        ▼           ▼           ▼            ▼             ▼           ▼
[Interactive]  [Pure]      [D2]   [Mermaid]  [Structurizr] [PlantUML]  [Graphviz]  [Excalidraw]  [ASCII]
    HTML       Vector SVG   Lang                 (C4)       (Component)  (DOT)      (Hand-drawn)  (Box Art)
```

---

## 🎨 Supported Rendering Engines

| Format / Engine | Best Use | Visual Quality | File Output |
| :--- | :--- | :--- | :--- |
| **✨ Interactive HTML** | Interactive exploration, upstream/downstream link tracing, search, minimap & drawer | Exceptional (Web Canvas) | `.html` |
| **🖼️ Pure Vector SVG** | Standalone vector graphic with cloud badges, protocol colors, and Sugiyama layout | Publication Grade | `.svg` |
| **⚡ D2 Lang** | Modern declarative system architecture, cloud topologies, and container grouping | Excellent | `.d2` |
| **🏛️ Structurizr DSL** | Professional **C4 architecture models** with official [Structurizr Themes](https://playground.structurizr.com/themes) (AWS, Azure, GCP, K8s) | Excellent | `.dsl` |
| **🧜‍♂️ Mermaid.js** | GitHub READMEs, Notion, pull request markdown, GitLab | Good | `.mmd` / `.md` |
| **📐 PlantUML** | Classical enterprise UML and sequence component diagrams | Good | `.puml` |
| **🕸️ Graphviz (DOT)** | Dependency trees, automated graph layout, high-density relationship mapping | Good | `.dot` |
| **🎨 Excalidraw** | Hand-drawn whiteboard diagrams, collaborative team sketches | Distinctive | `.excalidraw.mmd` |
| **📟 ASCII / Unicode** | Monospaced terminal outputs, code docstrings, git commit notes | Terminal-native | `.txt` |

---

## 🌟 Flagship Features

### 1. Interactive One-Page HTML Explainer
A zero-dependency, double-clickable interactive canvas that runs in any web browser:
* **🔍 Pan & Smooth Zoom**: Infinite viewport navigation.
* **↔️ Directional Layout Toggle**: Flip between Horizontal (LR) and Vertical (TB) with `O`.
* **🎯 Upstream & Downstream Link Tracing**: Click any node to light up incoming callers (**green**) and outgoing calls (**orange**), with glowing connection paths while dimming unrelated nodes.
* **🗺️ Live MiniMap**: Floating overview in the bottom-right corner.
* **📋 Component Drawer**: Displays provider badges, tech stack tags, role descriptions, and source files.
* **⌨️ Keyboard Shortcuts**: `/` to search, `D` for theme, `R` to center, `O` to toggle layout, `?` for help.

### 2. Standalone Pure SVG Vector Renderer
Clean, responsive SVG generated with zero external runtime dependencies:
* Embedded provider badges (AWS `#FF9900`, GCP `#4285F4`, Azure `#0089D6`, K8s `#326CE5`).
* Vector glyph paths for storage, compute, database, cache, queues, AI, and gateways.
* Color-coded protocol connectors (HTTPS `#3B82F6`, SQL `#10B981`, Kafka `#F97316`, Redis `#EF4444`).
* Ready to embed in GitHub READMEs, Notion, Figma, or presentation decks.

### 3. 13 Production Architecture Presets
Instant offline access to production-grade architecture blueprints:
1. `serverless-aws`: CloudFront → API Gateway → Lambda → DynamoDB + S3 + SNS
2. `rag-system`: Chat UI → Gateway → Orchestrator → Bedrock LLM + Vector DB + S3
3. `microservices-gke`: Cloud LB → GKE Cluster → Microservices → Cloud SQL + Pub/Sub
4. `fullstack-nextjs`: Vercel Frontend → Next.js API Routes → PostgreSQL + Redis + Stripe
5. `event-streaming-kafka`: Producer API → Kafka Cluster → Analytics + Notifications + Audit
6. `monolith-aws`: CloudFront → ALB → EC2 Monolith → RDS + ElastiCache + S3
7. `k8s-platform`: Ingress → Web & API Services → Deployments → PVC + ConfigMaps
8. `event-driven-aws`: API Gateway → Lambda → EventBridge → SQS → Worker → DynamoDB
9. `data-lakehouse`: Kinesis Stream → Lambda Ingest → S3 Lake → Glue ETL → Redshift + Athena
10. `ml-pipeline`: S3 Data → Step Functions → SageMaker Job → Model Registry → Inference API
11. `ecommerce-platform`: CloudFront → ALB → Microservices → PostgreSQL + Redis + Stripe
12. `iot-platform`: IoT Devices → AWS IoT Core → Kinesis → Lambda → DynamoDB + SNS Alerts
13. `web3-blockchain`: dApp Frontend → Cloudflare CDN → RPC Node → Smart Contract + Graph Indexer

---

## 🚀 Quick Start

### 1. Install
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
*(Note: VizArc includes a built-in offline engine and 13 presets, so you can run it immediately without an API key!)*

---

## 💻 CLI Usage

### View & Render Presets (100% Offline)
```bash
# List all 13 preset architectures
python cli.py templates

# Render preset to SVG
python cli.py template rag-system --format svg -o rag.svg

# Render preset to Interactive HTML and open in browser
python cli.py template serverless-aws --format html --open

# Compile preset into all 9 formats
python cli.py template microservices-gke --format all -o ./gke_export
```

### Compile from Prompt to All Formats
```bash
# Compiles HTML, SVG, D2, Structurizr C4, Mermaid, PlantUML, Graphviz, Excalidraw, and ASCII
python cli.py generate "Microservices payment platform with Stripe, Kafka, and Postgres" --format all --output ./dist
```

### Generate Standalone SVG Vector
```bash
python cli.py generate "AWS serverless topology with Lambda and DynamoDB" --format svg --orientation horizontal -o arch.svg
```

### Scan a Local Codebase & Compile
```bash
# Automatically detects frameworks, routes, models, and Docker configs
python cli.py scan . --format all --output ./architecture_docs
```

---

## 🌐 Free Web Playground (Streamlit)

Launch the multi-renderer studio locally:

```bash
streamlit run app.py
```

* Multi-tab viewer: Switch between **Interactive Canvas, Pure SVG Vector, D2, Structurizr C4, Mermaid, PlantUML, Graphviz, Excalidraw, ASCII, and Canonical JSON IR** with zero latency.
* Preset gallery: Instant selection of all 13 architecture templates.
* Download buttons: One-click export for standalone HTML explainers and vector SVGs.

---

## 🤖 GitHub Action: Automated PR Diagram Comments

VizArc includes a ready-to-use GitHub Action workflow (`.github/workflows/vizarc-diagram.yml`).

When a contributor opens a Pull Request with a ```vizarc block in their PR description:
````markdown
```vizarc
Microservices architecture with API Gateway, Auth Service, Order Service, and PostgreSQL database
```
````

The GitHub Action automatically:
1. Runs VizArc to compile the Canonical Model.
2. Renders publication-grade SVG and HTML artifacts.
3. Posts the architecture diagram as a comment directly on the PR!

---

## 📦 Project Layout

```text
vizarc/
├── .github/workflows/
│   └── vizarc-diagram.yml   # GitHub Action for PR comment diagrams
├── src/
│   └── vizarc/              # Core Python package (Standard src layout)
│       ├── __init__.py
│       ├── engine.py        # Universal Architecture Compiler orchestration
│       ├── ir.py            # Canonical Architecture Model (JSON AST)
│       ├── services.py      # 188+ Cloud Service catalog, icons & brand colors
│       ├── templates.py     # 13 Built-in preset architecture templates
│       ├── compiler.py      # Interactive HTML Canvas Compiler (minimap, shortcuts)
│       ├── analyzer.py      # Local repository scanner
│       └── adapters/        # 9 Deterministic Rendering Adapters
│           ├── base.py
│           ├── html_adapter.py        # Interactive HTML with link tracing
│           ├── svg_adapter.py         # Pure standalone Vector SVG builder
│           ├── d2_adapter.py          # D2 Lang
│           ├── structurizr_adapter.py # Structurizr C4 DSL
│           ├── mermaid_adapter.py     # Mermaid.js
│           ├── plantuml_adapter.py    # PlantUML Component
│           ├── graphviz_adapter.py    # Graphviz DOT
│           ├── excalidraw_adapter.py  # Excalidraw
│           └── ascii_adapter.py       # Terminal Unicode Boxes
├── app.py                   # Streamlit Multi-Renderer Playground
├── cli.py                   # CLI tool (generate, scan, template, templates)
├── SKILL.md                 # Agent Skill definition (Claude Code & Antigravity)
├── requirements.txt
├── .env.example
└── README.md
```

---

## 📄 License

MIT License. Free to use for personal projects, enterprise architecture, and open-source documentation!
