---
name: vizarc
description: Turn any idea, plan, or codebase into a beautiful interactive diagram, vector SVG, and one-page explainer. An agent skill for Claude Code, Antigravity, Codex, and Cursor.
---

# VizArc: Universal Architecture Compiler & Explainer Skill

`vizarc` turns codebases, system requirements, and complex cloud topologies into publication-grade **interactive HTML explainers**, **pure vector SVGs**, and declarative diagrams (**D2, Mermaid, Structurizr C4, PlantUML, Graphviz DOT, Excalidraw, ASCII**).

It features a Canonical Architecture Intermediate Representation (JSON IR), 188+ cloud service icons (AWS, GCP, Azure, K8s), 13 production presets, live pan & zoom, **upstream/downstream link tracing**, node detail inspection drawers, minimap, and GitHub Actions PR comment automation.

---

## When to Use This Skill

Activate this skill when:
- The user asks to **"visualize the codebase"**, create an architecture map, or plan a system topology.
- The user wants a **vector SVG diagram** for GitHub READMEs, documentation, or slides.
- The user wants an **interactive diagram or one-page explainer** to explore service dependencies.
- The user needs to inspect **upstream/downstream dependencies** (which service calls what).
- The user requests diagrams in **HTML**, **SVG**, **D2**, **Mermaid**, **Structurizr C4**, **PlantUML**, **ASCII**, or **Excalidraw**.
- The user wants a standard preset architecture (e.g. RAG system, serverless AWS, microservices, Kafka streaming).

---

## Agent Execution Instructions

When the user requests an architecture diagram or system explainer:

### 1. Default Mode: Interactive HTML Explainer (`architecture.html`)
Unless the user explicitly asks for raw markdown or SVG:
1. Scan the project structure or analyze the system requirements.
2. Structure components into logical tiers:
   - **Client Tier**: Web SPA, Mobile Apps, CLI
   - **Ingress / Gateway**: API Gateway, Reverse Proxy, CloudFront/Cloudflare
   - **Services Layer**: Microservices, Lambda, Queues, Background Workers
   - **Data Layer**: PostgreSQL, DynamoDB, Redis Caches, S3 Buckets
3. Run:
   ```bash
   python cli.py generate "..." --format html --output architecture.html
   ```
4. Tell the user: *"Generated interactive architecture explainer in `architecture.html`. Double-click to open in your browser to trace dependencies, search components, and view node details."*

### 2. Standalone Vector SVG Mode (`--format svg`)
When the user wants a crisp image for a GitHub README or PR:
```bash
python cli.py generate "..." --format svg --orientation horizontal -o architecture.svg
```

### 3. Preset Architectures (100% Offline)
To instantly generate any of the 13 built-in production architectures:
```bash
# List all 13 preset templates
python cli.py templates

# Render preset directly (no API key needed)
python cli.py template rag-system --format svg -o rag-architecture.svg
python cli.py template serverless-aws --format html -o serverless.html
```

---

## CLI Quick Reference

```bash
# Generate interactive HTML architecture explainer
python cli.py generate "Microservices payment gateway with Stripe and Kafka" --output architecture.html

# Generate standalone SVG vector graphic with cloud service icons
python cli.py generate "AWS serverless topology with Lambda and DynamoDB" --format svg -o arch.svg

# Scan local codebase and generate an interactive architecture explainer
python cli.py scan . --format html --output architecture.html

# Compile into ALL 9 formats simultaneously
python cli.py generate "RAG AI Agent system" --format all -o ./dist

# Render preset template
python cli.py template microservices-gke --format svg

# Launch the interactive web playground
streamlit run app.py
```

---

## Supported Output Formats

| Format | Extension | Best Use |
| :--- | :--- | :--- |
| **Interactive HTML** | `.html` | Double-clickable 3D/canvas explainer with path tracing & drawer |
| **Pure Vector SVG** | `.svg` | Crisp vector graphic with cloud provider badges & protocol colors |
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
* **Interactive Canvas**: Drag to pan, scroll to zoom, click center to reset.
* **Layout Direction Toggle**: Switch between Horizontal (LR) and Vertical (TB) with `O`.
* **Cloud Service Badges**: Official AWS, GCP, Azure, and K8s icons and brand colors.
* **Upstream & Downstream Link Tracing**: Click any service to highlight all callers (upstream) and outgoing calls (downstream) with glowing paths.
* **MiniMap**: Live viewport tracker in the bottom-right corner.
* **Node Detail Drawer**: Displays technology stack, role description, and associated code files.
* **Keyboard Shortcuts**: `/` to search, `D` for theme, `R` to center, `O` to flip orientation, `?` for help.
* **Zero Dependencies**: Fully self-contained SVG + CSS + JS; runs 100% offline in any browser.
