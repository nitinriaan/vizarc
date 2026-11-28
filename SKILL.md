---
name: vizarc
description: Turn any idea, plan, or codebase into a beautiful interactive diagram, vector SVG, and one-page explainer. An agent skill for Claude Code, Antigravity, Codex, Cursor, and Copilot (inspired by Archify).
---

# VizArc: Universal Architecture Compiler & Explainer Skill

`vizarc` turns codebases, system requirements, and complex cloud topologies into publication-grade **interactive HTML explainers**, **pure vector SVGs**, and declarative diagrams (**D2, Mermaid, Structurizr C4, PlantUML, Graphviz DOT, Excalidraw, ASCII**).

Inspired by [Archify](https://archify.si/) (`tt-a1i/archify`), VizArc features a **Dual-View Architecture**:
1. **📐 Diagram Canvas View:** Interactive vector canvas with smooth pan & zoom, animated flow motion, authentic cloud service icons (AWS, GCP, Azure, K8s), upstream/downstream path tracing, minimap, and side inspector drawer.
2. **📄 One-Page Explainer View:** Conclusion-first executive whitepaper containing an Executive Summary, Architecture Decisions & Trade-Offs (ADRs), End-to-End Transaction Stepper, Service Catalog, and Communication Protocol Matrix.

---

## When to Use This Skill

Activate this skill when:
- The user asks to **"visualize the codebase"**, create an architecture diagram, or design a system topology.
- The user wants an **interactive diagram or one-page explainer** like Archify to document architecture trade-offs and data flow.
- The user asks for a **standalone vector SVG diagram** for GitHub READMEs, technical RFCs, or presentations.
- The user needs to inspect **upstream/downstream dependencies** (which service calls what).
- The user requests diagrams in **HTML**, **SVG**, **D2**, **Mermaid**, **Structurizr C4**, **PlantUML**, **ASCII**, or **Excalidraw**.
- The user wants a standard preset architecture (e.g. RAG system, serverless AWS, microservices, Kafka streaming, e-commerce platform).

---

## Agent Execution Instructions

When the user requests an architecture diagram or system explainer:

### 1. Default Mode: Interactive Dual-View Explainer (`architecture.html`)
Unless the user explicitly asks for raw markdown or SVG:
1. Scan the project structure or analyze the system requirements.
2. Structure components into logical tiers:
   - **Client Tier**: Web SPA, Mobile Apps, CLI
   - **Ingress / Gateway**: API Gateway, Reverse Proxy, CloudFront/Cloudflare
   - **Services Layer**: Microservices, Lambda, Queues, Background Workers
   - **Data Layer**: PostgreSQL, DynamoDB, Redis Caches, S3 Buckets
3. Either write a Canonical Architecture IR JSON file and compile deterministically (zero external LLM calls needed):
   ```bash
   vizarc compile arch_ir.json --format html --strict --output architecture.html
   ```
   Or run the CLI analyzer/generator directly:
   ```bash
   vizarc generate "..." --format html --output architecture.html
   ```
4. Tell the user: *"Generated interactive architecture explainer in `architecture.html`. Double-click to open in your browser to explore the interactive canvas, animate flow paths, or toggle the One-Page Architectural Explainer."*

### 2. Standalone Vector SVG Mode (`--format svg`)
When the user wants a crisp, publication-grade image for a GitHub README or PR:
```bash
vizarc generate "..." --format svg --orientation horizontal -o architecture.svg
```

### 3. Preset Architectures (100% Offline)
To instantly generate any of the 13 built-in production architectures:
```bash
# List all 13 preset templates
vizarc templates

# Render preset directly (no API key needed)
vizarc template ecommerce-platform --format html -o ecommerce.html
vizarc template serverless-aws --format svg -o serverless.svg
```

---

## CLI Quick Reference

```bash
# Compile a Canonical Architecture IR JSON file directly (zero API key required)
vizarc compile arch_ir.json --format html --strict -o architecture.html

# Generate interactive HTML architecture canvas + one-page explainer
vizarc generate "Microservices payment gateway with Stripe and Kafka" --output architecture.html

# Generate standalone SVG vector graphic with embedded cloud service icons
vizarc generate "AWS serverless topology with Lambda and DynamoDB" --format svg -o arch.svg

# Scan local codebase and generate an interactive architecture explainer
vizarc scan . --format html --output architecture.html

# Diagnose codebase cycles & coupling hotspots, or validate/compare architectures
vizarc diagnose .
vizarc validate architecture.html
vizarc compare base_arch.html head_arch.html

# Compile into ALL 9 formats simultaneously (HTML, SVG, D2, C4, Mermaid, PlantUML, DOT, Excalidraw, ASCII)
vizarc generate "RAG AI Agent system" --format all -o ./dist

# Render preset template
vizarc template microservices-gke --format html

# Install VizArc as a global Claude Code skill (~/.claude/skills/vizarc)
vizarc install-skill

# Launch the Mermaid-style Live Architecture Studio (or visit https://vizarc.streamlit.app)
streamlit run app.py
```

---

## Supported Output Formats

| Format | Extension | Best Use |
| :--- | :--- | :--- |
| **Interactive HTML** | `.html` | Dual-view interactive canvas + one-page explainer (Archify standard) |
| **Pure Vector SVG** | `.svg` | Crisp vector graphic with embedded cloud provider glyphs |
| **D2 Lang** | `.d2` | Modern declarative architecture diagrams |
| **Structurizr C4** | `.dsl` | Industry-standard C4 enterprise container & component diagrams |
| **Mermaid** | `.mmd` | Native GitHub markdown flowcharts |
| **PlantUML** | `.puml` | Component and sequence diagrams |
| **Graphviz** | `.dot` | Automated graph layouts & dependency trees |
| **Excalidraw** | `.excalidraw` | Whiteboard hand-drawn style |
| **ASCII** | `.txt` | Terminal output and code comment headers |

---

## Key Interactive Features

Inside the generated `.html` file:
* **Dual-View Switcher**: Toggle between `[📐 Diagram Canvas]` and `[📄 One-Page Explainer]` with keys `1` and `2`.
* **Animated Flow Motion**: Real-time flowing dash animation along active edges (`⚡ Flow Motion` / key `M`).
* **One-Page Explainer (ADR & Stepper)**:
  - Executive summary and key architectural drivers.
  - Architectural Decisions & Trade-offs (ADRs with rationale & consequences).
  - Step-by-step transaction lifecycle with clickable "Inspect on Canvas" shortcuts.
  - Comprehensive Component & Service catalog.
  - Upstream-to-downstream communication protocol matrix.
* **Authentic Embedded Vector Icons**: 188+ official AWS, GCP, Azure, and K8s icons embedded inline — 100% offline-proof.
* **Upstream & Downstream Link Tracing**: Click any service to highlight all callers (upstream, green) and outgoing calls (downstream, amber) with glowing paths.
* **MiniMap**: Live viewport tracker in the bottom-right corner.
* **Node Detail Drawer**: Displays technology stack, role description, and associated code files with a deep link to the explainer view.
* **Client-Side Export**: Instant download of standalone `.svg`, high-DPI `.png` rasterization, or clean print/PDF whitepaper (`Ctrl+P`).
* **Keyboard Shortcuts**: `1` (Canvas), `2` (Explainer), `/` (Search), `D` (Theme), `M` (Flow Motion), `O` (Flip Layout), `R` (Fit to View), `F` (Fullscreen).
* **Zero Dependencies**: Fully self-contained SVG + CSS + JS; runs 100% offline in any browser.
