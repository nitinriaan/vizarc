<p align="center">
  <a href="https://github.com/nitinriaan/vizarc">
    <img src="assets/logo-dark.png#gh-dark-mode-only" alt="VizArc - Architecture, Visualized" width="680">
  </a>
</p>

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python 3.10+"/></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"/></a>
  <a href="https://streamlit.io"><img src="https://img.shields.io/badge/Streamlit-FF4B4B?logo=Streamlit&logoColor=white" alt="Streamlit"/></a>
  <a href="#-agent-skill-integration"><img src="https://img.shields.io/badge/Agent%20Skill-Claude%20%7C%20Antigravity%20%7C%20Cursor%20%7C%20Copilot-purple.svg" alt="Built for AI Agents"/></a>
  <a href=".github/workflows/vizarc-diagram.yml"><img src="https://img.shields.io/badge/GitHub%20Action-PR%20Diagrams-black?logo=github" alt="GitHub Action"/></a>
</p>

<p align="center">
  <strong>The "Pandoc & Archify of Software Architecture"</strong><br/>
  Turn any prompt, plan, or codebase into a <strong>Canonical Architecture Model (JSON IR)</strong>, and deterministically compile it into a <strong>Dual-View Interactive Canvas & One-Page Explainer (HTML)</strong>, <strong>Publication-Grade Vector SVG</strong>, <strong>D2 Lang</strong>, <strong>Structurizr C4</strong>, <strong>Mermaid</strong>, <strong>PlantUML</strong>, <strong>Graphviz (DOT)</strong>, <strong>Excalidraw</strong>, and <strong>ASCII</strong> in one single pass.
</p>

---

## 🚀 What Makes VizArc Different?

Unlike tools that rely on the LLM to write syntax for every format independently (causing syntax errors, missing tags, and inconsistent diagrams), VizArc implements the **Universal Compiler Pattern** (inspired by LLVM, Pandoc, and [Archify](https://archify.si/)):

* 🧠 **Single Source of Truth**: The AI analyzes your codebase or system requirements **once** to produce a typed, validated **Canonical Architecture Model (JSON AST/IR)**.
* 📄 **Dual-View Interactive Explainer (Archify Spec)**:
  - **📐 Diagram Canvas**: Interactive vector canvas with pan/zoom, live animated edge flow motion, authentic cloud service icons, upstream/downstream link tracing, and a live minimap.
  - **📄 One-Page Architectural Explainer**: Conclusion-first executive whitepaper containing an Executive Summary, Architecture Decisions & Trade-Offs (ADRs), End-to-End Stepper Lifecycle, Component Inventory, and Network Communication Matrix.
* ⚡ **Deterministic Multi-Renderer Compilation**: 9 specialized adapters transform the IR into any diagram language with **zero extra LLM calls and zero hallucinated syntax**.
* ☁️ **188+ Cloud Service Icons (100% Offline-Proof)**: Embedded authentic 24x24 SVG vector paths for AWS, GCP, Azure, Kubernetes, PostgreSQL, Redis, Kafka, Docker, and more. Never fails in offline environments or `file:///` downloads!
* 🏛️ **Full Structurizr Themes Integration**: Automatically applies C4 tags and imports prebuilt themes (`amazon-web-services-2023.01`, `google-cloud-platform-v1.5`, `microsoft-azure-2023.01`, `kubernetes-v0.3`).
* 📦 **13 Built-in Architecture Presets**: Instant offline templates for RAG Systems, Serverless AWS, Kafka Event Streaming, Kubernetes Platforms, Microservices, and E-Commerce.
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
                     │    (Decisions, Stepper, AST)    │
                     └────────────────┬────────────────┘
                                      │
     ┌───────────┬───────────┬────────┼───────────┬───────────┬────────────┬─────────────┬───────────┐
     ▼           ▼           ▼        ▼           ▼           ▼            ▼             ▼           ▼
[Interactive]  [Pure]      [D2]   [Mermaid]  [Structurizr] [PlantUML]  [Graphviz]  [Excalidraw]  [ASCII]
  Dual-View  Vector SVG    Lang                 (C4)       (Component)  (DOT)      (Hand-drawn)  (Box Art)
(Canvas+Doc)
```

---

## 🎨 Supported Rendering Engines

| Format / Engine | Best Use | Visual Quality | File Output |
| :--- | :--- | :--- | :--- |
| **✨ Interactive HTML** | Dual-view canvas + one-page explainer, flow motion, link tracing, search, minimap & drawer | Exceptional (Web Canvas) | `.html` |
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

### 1. Dual-View Mode: Interactive Canvas + One-Page Explainer
A zero-dependency, double-clickable file that runs locally in any web browser (`file:///...`):
* **📐 Canvas Mode**:
  - **🔍 Pan & Smooth Zoom**: Infinite viewport navigation with mousewheel or gestures.
  - **⚡ Animated Flow Motion**: Real-time flowing dashes along active edges (`M` shortcut).
  - **↔️ Directional Layout Toggle**: Flip between Horizontal (LR) and Vertical (TB) with `O`.
  - **🎯 Upstream & Downstream Link Tracing**: Click any node to light up incoming callers (**green**) and outgoing calls (**amber**), with glowing connection paths while dimming unrelated nodes.
  - **🗺️ Live MiniMap**: Floating overview with live viewport tracking.
  - **📋 Component Drawer**: Displays provider badges, tech stack tags, role descriptions, and upstream/downstream connection pills.
* **📄 One-Page Explainer Mode**:
  - **Executive Summary**: High-level verdict and system characteristics.
  - **Architecture Decisions & Trade-Offs (ADRs)**: What was chosen, why it was chosen, and accepted trade-offs.
  - **End-to-End Stepper**: Step-by-step transaction walkthrough with clickable "Inspect on Canvas" shortcuts.
  - **Component Inventory**: Detailed service cards with embedded vector icons.
  - **Protocols Matrix**: Clean table of all inter-service communications.
* **Export Options**: One-click download of standalone `.svg`, high-resolution `.png` (canvas rasterization), or clean print/PDF whitepaper (`Ctrl+P`).
* **⌨️ Keyboard Shortcuts**: `1` (Canvas), `2` (Explainer), `/` (Search), `D` (Theme), `M` (Flow Motion), `R` (Center), `O` (Layout), `F` (Fullscreen).

### 2. Standalone Pure SVG Vector Renderer
Clean, responsive SVG generated with zero external runtime dependencies:
* Embedded provider badges (AWS `#FF9900`, GCP `#4285F4`, Azure `#0089D6`, K8s `#326CE5`).
* Vector glyph paths for storage, compute, database, cache, queues, AI, and gateways.
* Color-coded protocol connectors (HTTPS `#3B82F6`, SQL `#10B981`, Kafka `#F97316`, Redis `#EF4444`).
* Ready to embed in GitHub READMEs, Notion, Figma, or presentation decks.

### 3. 13 Production Architecture Presets
Instant offline access to production-grade architecture blueprints:
1. `ecommerce-platform`: CloudFront → ALB → Microservices → PostgreSQL + Redis + Stripe
2. `serverless-aws`: CloudFront → API Gateway → Lambda → DynamoDB + S3 + SNS
3. `rag-system`: Chat UI → Gateway → Orchestrator → Bedrock LLM + Vector DB + S3
4. `microservices-gke`: Cloud LB → GKE Cluster → Microservices → Cloud SQL + Pub/Sub
5. `fullstack-nextjs`: Vercel Frontend → Next.js API Routes → PostgreSQL + Redis + Stripe
6. `event-streaming-kafka`: Producer API → Kafka Cluster → Analytics + Notifications + Audit
7. `monolith-aws`: CloudFront → ALB → EC2 Monolith → RDS + ElastiCache + S3
8. `k8s-platform`: Ingress → Web & API Services → Deployments → PVC + ConfigMaps
9. `event-driven-aws`: API Gateway → Lambda → EventBridge → SQS → Worker → DynamoDB
10. `data-lakehouse`: Kinesis Stream → Lambda Ingest → S3 Lake → Glue ETL → Redshift + Athena
11. `ml-pipeline`: S3 Data → Step Functions → SageMaker Job → Model Registry → Inference API
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

# Render preset to Interactive Dual-View HTML
python cli.py template ecommerce-platform --format html -o ecommerce.html

# Render preset to Vector SVG
python cli.py template serverless-aws --format svg -o serverless.svg

# Compile preset into all 9 formats simultaneously
python cli.py template microservices-gke --format all -o ./gke_export
```

### Compile from Prompt to All Formats
```bash
# Compiles HTML, SVG, D2, Structurizr C4, Mermaid, PlantUML, Graphviz, Excalidraw, and ASCII
python cli.py generate "Microservices payment platform with Stripe, Kafka, and Postgres" --format all --output ./dist
```

### Scan a Local Codebase & Compile
```bash
# Automatically detects frameworks, routes, models, and Docker configs
python cli.py scan . --format all --output ./architecture_docs
```

---

## 🌐 Live Architecture Studio (Streamlit)

Launch the Mermaid-style two-pane studio:

```bash
streamlit run app.py
```

* **Left Pane**: System specification input, 🚀 Generate Canvas, ⚡ Load Preset, and collapsible ⚙️ Settings (Gemini API key, 13 presets, layout orientation).
* **Right Pane**: Primary interactive canvas with dual-view switcher, live flow motion, instant top-corner SVG & HTML downloads, and on-demand format exporter for D2, Structurizr C4, Mermaid, PlantUML, DOT, Excalidraw, and ASCII.

---

## 🤖 GitHub Action: Automated PR Diagram Comments

VizArc includes a ready-to-use GitHub Action workflow (`.github/workflows/vizarc-diagram.yml`).

When a contributor opens a Pull Request with a ```vizarc block in their PR description:
````markdown
```vizarc
Microservices architecture with API Gateway, Auth Service, Order Service, and PostgreSQL database
```
````

The GitHub Action automatically runs VizArc to compile the architecture and posts publication-grade diagrams directly as a comment on the PR!

---

## 📄 License

MIT License. Free to use for personal projects, enterprise architecture, and open-source documentation!
