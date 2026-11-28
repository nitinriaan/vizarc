<p align="center">
  <a href="https://github.com/nitinriaan/vizarc">
    <img src="assets/logos/vizarc-horizontal-light.png#gh-light-mode-only" alt="VizArc - Architecture, Visualized" width="680">
    <!--<img src="assets/logos/vizarc-horizontal-dark.png#gh-dark-mode-only" alt="VizArc - Architecture, Visualized" width="680">-->
  </a>
</p>

<p align="center">
  <a href="https://vizarc.streamlit.app/"><img src="https://img.shields.io/badge/Streamlit%20Cloud-Live%20Studio-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit Cloud"/></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.12+-blue.svg" alt="Python 3.12+"/></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"/></a>
  <a href="#-agent-skill-integration"><img src="https://img.shields.io/badge/Agent%20Skill-Claude%20%7C%20Antigravity%20%7C%20Cursor%20%7C%20Copilot-purple.svg" alt="Built for AI Agents"/></a>
  <a href=".github/workflows/vizarc-diagram.yml"><img src="https://img.shields.io/badge/GitHub%20Action-PR%20Diagrams-black?logo=github" alt="GitHub Action"/></a>
</p>

<p align="center">
  <strong>The "Pandoc & Archify of Software Architecture"</strong><br/>
  Turn any prompt, plan, or codebase into a <strong>Canonical Architecture Model (JSON IR)</strong>, and deterministically compile it into a <strong>Dual-View Interactive Canvas & One-Page Explainer (HTML)</strong>, <strong>Publication-Grade Vector SVG</strong>, <strong>D2 Lang</strong>, <strong>Structurizr C4</strong>, <strong>Mermaid</strong>, <strong>PlantUML</strong>, <strong>Graphviz (DOT)</strong>, <strong>Excalidraw</strong>, and <strong>ASCII</strong> in one single pass.
</p>

<p align="center">
  🚀 <strong>Live Cloud Studio:</strong> <a href="https://vizarc.streamlit.app/"><strong>VizArc - Architecture Studio · Streamlit</strong></a>
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

**Prerequisites:** **Python 3.12+** and **Git**

### Path 1: Install as an AI Agent Skill (Claude Code, Google Antigravity, OpenAI Codex)
*(Recommended — works across all your repositories with **zero external API keys**; the agent authors the Canonical IR and `vizarc compile` renders deterministically offline.)*

#### 1. Clone, Install CLI & Register Skill
```bash
git clone https://github.com/nitinriaan/vizarc.git
cd vizarc
pip install -e .
vizarc install-skill --platform all --scope global
```

Or install selectively for a single platform:
```bash
vizarc install-skill --platform claude       # -> ~/.claude/skills/vizarc/
vizarc install-skill --platform antigravity  # -> ~/.gemini/antigravity/skills/vizarc/
vizarc install-skill --platform codex        # -> ~/.codex/skills/vizarc/
```

| Platform | Project-Local Path (Auto-Discovered) | User-Global Path | Alternative / Plugin |
| :--- | :--- | :--- | :--- |
| **Claude Code** | `.claude/skills/vizarc/SKILL.md` | `~/.claude/skills/vizarc/SKILL.md` | `claude --plugin-dir /path/to/vizarc` |
| **Google Antigravity** | `.agent/skills/vizarc/SKILL.md` | `~/.gemini/antigravity/skills/vizarc/SKILL.md` | Also supports `.agents/skills/vizarc/` |
| **OpenAI Codex** | `.agents/skills/vizarc/SKILL.md` | `~/.codex/skills/vizarc/SKILL.md` | Invoke via `$vizarc` or prompt |

#### 2. Verify Installation
```bash
# Validate YAML frontmatter, metadata constraints, and relative links for all 3 platforms
python shared/scripts/validate_skills.py

# Check Python dependencies, presets, and installed global skills
vizarc doctor

# Smoke-test offline IR compilation & static architecture linting
vizarc template ecommerce-platform --format html -o test_arch.html
vizarc validate test_arch.html
```

Then open any repository in Claude Code, Antigravity, or Codex and ask:
> *"Use VizArc to visualize this codebase's architecture into `architecture.html`."*

---

### Path 2: Full Standalone CLI (Terminal & CI)
If you want to run VizArc directly from the command line or CI pipelines without an AI coding agent:

1. **Install the CLI** (after cloning the repo):
   ```bash
   pip install -e .
   ```
2. **(Optional) Configure a Free Gemini API Key** from [Google AI Studio](https://aistudio.google.com/) for `vizarc generate` and `vizarc scan`:
   ```bash
   cp .env.example .env
   # Edit .env and paste: GEMINI_API_KEY=your_key_here
   ```
   *(Note: `vizarc compile`, `vizarc template`, `vizarc validate`, `vizarc compare`, and `vizarc diagnose` work 100% offline with no API key!)*

---

## 💻 CLI Usage

### Compile Agent-Authored IR (Zero API Key)
```bash
# Compile a Canonical Architecture IR JSON file into Interactive HTML, SVG, or all 9 formats
vizarc compile arch_ir.json --format html --strict -o architecture.html
vizarc compile arch_ir.json --format svg --orientation horizontal -o architecture.svg
vizarc compile arch_ir.json --format all -o ./vizarc_out
```

### View & Render Presets (100% Offline)
```bash
# List all 13 preset architectures
vizarc templates

# Render preset to Interactive Dual-View HTML
vizarc template ecommerce-platform --format html -o ecommerce.html

# Render preset to Vector SVG
vizarc template serverless-aws --format svg -o serverless.svg

# Compile preset into all 9 formats simultaneously
vizarc template microservices-gke --format all -o ./gke_export
```

### Compile from Prompt, Scan, Diagnose & Validate
```bash
# Compiles HTML, SVG, D2, Structurizr C4, Mermaid, PlantUML, Graphviz, Excalidraw, and ASCII
vizarc generate "Microservices payment platform with Stripe, Kafka, and Postgres" --format all --output ./dist

# Scan a local codebase & compile
vizarc scan . --format all --output ./architecture_docs

# Diagnose cycles & coupling hotspots, validate graphs, or diff two architectures
vizarc diagnose .
vizarc validate architecture.html
vizarc compare base_arch.html head_arch.html
```

---

## 🌐 Live Demo (Streamlit Studio)

Want a quick browser demo before installing locally? Try the hosted Streamlit studio:
👉 **[VizArc - Architecture Studio · Streamlit](https://vizarc.streamlit.app/)**

Or run the demo UI locally:

```bash
streamlit run app.py
```

* **Left Pane (~19%)**: Official VizArc brand logo, system specification input, 🚀 **Generate Canvas**, ⚡ **Load Preset**, direct **📥 SVG** and **📥 HTML** downloads, and collapsible ⚙️ **Presets & Layout** (13 built-in presets, Horizontal LR / Vertical TB orientation).
* **Right Pane (~81%)**: Pure 16:9 full-bleed interactive canvas & one-page explainer with dual-view switcher, live flow motion animation, live path tracing, minimap, authentic vector cloud icons, and an on-demand format exporter for D2, Structurizr C4, Mermaid, PlantUML, DOT, Excalidraw, and ASCII.

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
