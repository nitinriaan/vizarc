---
name: vizarc
description: Turn any idea, plan, or codebase into a beautiful interactive architecture diagram and one-page explainer. An agent skill for Claude Code, Antigravity, Codex, and Cursor.
---

# VizArc: Interactive Architecture Explainer & Diagram Skill

`vizarc` turns codebases, system requirements, and complex workflows into polished, self-contained **interactive HTML explainers** and diagrams. It features typed JSON Intermediate Representation (IR), live pan & zoom, **upstream/downstream link tracing**, node detail inspection drawers, and component search.

---

## When to Use This Skill

Activate this skill when:
- The user asks to **"visualize the codebase"**, create an architecture map, or plan a system.
- The user wants an **interactive diagram or one-page explainer** to explore service dependencies.
- The user needs to inspect **upstream/downstream dependencies** (which service calls what).
- The user requests diagrams in **HTML**, **D2**, **Mermaid**, **ASCII art** (for terminal/PRs), or **Excalidraw**.

---

## Agent Execution Instructions

When the user requests an architecture diagram or system explainer:

### 1. Default Mode: Interactive HTML Explainer (`architecture.html`)
Unless the user explicitly asks for raw markdown or Mermaid:
1. Scan the project structure or analyze the system requirements.
2. Structure components into logical tiers:
   - **Client Tier**: Web, Mobile, CLI
   - **Ingress / Gateway**: API Gateway, Reverse Proxy, Load Balancer
   - **Services Layer**: Microservices, Auth, Queues, Background Workers
   - **Data Layer**: Databases, Redis Caches, S3/Object storage
3. Run `python cli.py scan . --format html --output architecture.html` or `python cli.py generate "..." --format html --output architecture.html`.
4. Tell the user: *"Generated interactive architecture explainer in `architecture.html`. Double-click to open in your browser to trace dependencies, search components, and view node details."*

### 2. Markdown / GitHub Mode (`--format mermaid`)
If the user wants an inline diagram for a GitHub `README.md` or PR comment:
1. Generate using `--format mermaid` or `--format ascii`.
2. Follow strict Mermaid quotation rules (`id["Label (Info)"]`) to avoid syntax crashes.

---

## CLI Quick Reference

```bash
# Generate interactive HTML architecture explainer
python cli.py generate "Microservices payment gateway with Stripe and Kafka" --output architecture.html

# Scan local codebase and generate an interactive architecture explainer
python cli.py scan . --format html --output architecture.html

# Generate D2 cloud architecture
python cli.py generate "AWS serverless topology with Lambda and DynamoDB" --format d2

# Generate ASCII diagram for PR comments or code comments
python cli.py generate "OAuth2 Auth Flow" --format ascii

# Launch the interactive web playground
streamlit run app.py
```

---

## Key Interactive Features

Inside the generated `.html` file:
* **Interactive Canvas**: Drag to pan, scroll to zoom, click center to reset.
* **Upstream & Downstream Link Tracing**: Click any service to highlight all callers (upstream) and all outgoing calls (downstream) with glowing paths; unrelated nodes dim.
* **Node Detail Drawer**: Displays technology stack, role description, and associated code files.
* **Component Search**: Instant live filtering.
* **Zero Dependencies**: Fully self-contained SVG + CSS + JS; runs 100% offline in any browser.
