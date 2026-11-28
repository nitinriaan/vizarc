<p align="center">
  <a href="https://github.com/nitinriaan/vizarc">
    <img src="assets/logos/vizarc-horizontal-light.png#gh-light-mode-only" alt="VizArc - Architecture, Visualized" width="680">
  </a>
</p>

<p align="center">
  <a href="#path-1-install-as-an-ai-agent-skill-claude-code-google-antigravity-openai-codex"><img src="https://img.shields.io/badge/Agent%20Skill-Claude%20%7C%20Antigravity%20%7C%20Codex-purple.svg" alt="Agent Skill"/></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.12+-blue.svg" alt="Python 3.12+"/></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"/></a>
  <a href=".github/workflows/vizarc-diagram.yml"><img src="https://img.shields.io/badge/GitHub%20Action-PR%20Diagrams-black?logo=github" alt="GitHub Action"/></a>
  <a href="https://vizarc.streamlit.app/"><img src="https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit Demo"/></a>
</p>

<p align="center">
  <strong>The "Pandoc & Archify of Software Architecture"</strong><br/>
  Compile any codebase, prompt, or plan into a single <strong>Canonical Architecture IR</strong>, then deterministically render an <strong>Interactive Dual-View HTML Explainer</strong>, <strong>Vector SVG</strong>, <strong>D2</strong>, <strong>Structurizr C4</strong>, <strong>Mermaid</strong>, <strong>PlantUML</strong>, <strong>Graphviz</strong>, <strong>Excalidraw</strong>, and <strong>ASCII</strong> in one pass.
</p>

---

## 🚀 Why VizArc?

Instead of letting an LLM hallucinate diagram syntax separately for every format, VizArc uses a **Universal Compiler Pattern**:

* **Single Source of Truth**: Analyze a system once into a typed, validated **Canonical Architecture Model (JSON IR)**—authored directly by your AI coding agent (zero extra API keys) or via `vizarc scan` / `vizarc generate`.
* **Deterministic Multi-Format Compilation**: 9 adapters compile the same IR into interactive HTML, vector SVG, and declarative formats with zero extra LLM calls.
* **188+ Offline Cloud Icons**: Embedded inline SVG glyphs for AWS, GCP, Azure, Kubernetes, databases, and queues—works 100% offline.
* **Static & Visual QA**: Built-in graph linting + SVG bounding-box collision checks (`vizarc validate`), headless browser verification (`vizarc browser-check`), cycle/coupling diagnostics (`vizarc diagnose`), and interactive Before/Delta/After visual diffs (`vizarc compare --format html`).

---

## 🏛️ Compiler Pipeline

```text
  Agent (Claude / Antigravity / Codex)  ─┐
  Codebase Scan / Prompt / 13 Presets    ├─▶  [Canonical Architecture IR (JSON)]
                                         ┘                    │
         ┌──────────┬──────────┬──────────┬──────────┬────────┴─────────┬──────────┬──────────┐
         ▼          ▼          ▼          ▼          ▼                  ▼          ▼          ▼
     [HTML UI]   [SVG]       [D2]    [Mermaid]  [C4 DSL]          [PlantUML]   [DOT]    [Excalidraw / ASCII]
```

---

## 🎨 Supported Rendering Engines

| Format | Best For | Output |
| :--- | :--- | :--- |
| **Interactive HTML** | Dual-view canvas + one-page explainer, flow animation, link tracing | `.html` |
| **Pure Vector SVG** | READMEs, technical RFCs, slides with cloud badges & protocol colors | `.svg` |
| **D2 Lang** | Declarative system architecture and container grouping | `.d2` |
| **Structurizr C4** | Enterprise C4 models with official AWS, GCP, Azure & K8s themes | `.dsl` |
| **Mermaid.js** | GitHub/GitLab markdown, PRs, Notion | `.mmd` |
| **PlantUML** | Enterprise UML component and sequence diagrams | `.puml` |
| **Graphviz (DOT)** | Automated dependency graphs and high-density trees | `.dot` |
| **Excalidraw** | Hand-drawn whiteboard sketches | `.excalidraw.mmd` |
| **ASCII** | Terminal output and inline code documentation | `.txt` |

---

## 🌟 Flagship Features

* **Dual-View Interactive HTML**: Zero-dependency offline file with pan/zoom, animated edge flow (`M`), Live Flow Route Player with narrative captions, LR/TB layout flip (`O`), upstream/downstream path tracing, live minimap, node inspector drawer, and one-click `.svg` / `.png` / **`.webm` Story Video** / PDF (`Ctrl+P`) export—paired with an executive **One-Page Explainer** (ADRs, interactive transaction stepper, service catalog, protocol matrix). Shortcuts: `1` Canvas, `2` Explainer, `/` Search, `D` Theme, `R` Reset, `F` Fullscreen.
* **Standalone Vector SVG**: Crisp Sugiyama-layered vector diagrams with embedded AWS/GCP/Azure/K8s badges and color-coded protocol connectors (`HTTPS`, `SQL`, `Kafka`, `Redis`).
* **13 Offline Production Presets**: `ecommerce-platform`, `serverless-aws`, `rag-system`, `microservices-gke`, `fullstack-nextjs`, `event-streaming-kafka`, `monolith-aws`, `k8s-platform`, `event-driven-aws`, `data-lakehouse`, `ml-pipeline`, `iot-platform`, `web3-blockchain`.

---

## 🚀 Quick Start

**Prerequisites:** **Python 3.12+** and **Git**

### Path 1: Install as an AI Agent Skill (Claude Code, Google Antigravity, Codex, Cursor, Copilot, OpenCode)
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
vizarc install-skill --platform cursor       # -> ~/.cursor/skills/vizarc/
vizarc install-skill --platform copilot      # -> ~/.copilot/skills/vizarc/
vizarc install-skill --platform opencode     # -> ~/.config/opencode/skills/vizarc/
```

| Platform | Project-Local Path (Auto-Discovered) | User-Global Path | Alternative / Plugin |
| :--- | :--- | :--- | :--- |
| **Claude Code** | `.claude/skills/vizarc/SKILL.md` | `~/.claude/skills/vizarc/SKILL.md` | `claude --plugin-dir /path/to/vizarc` |
| **Google Antigravity** | `.agent/skills/vizarc/SKILL.md` | `~/.gemini/antigravity/skills/vizarc/SKILL.md` | Also supports `.agents/skills/vizarc/` |
| **OpenAI Codex** | `.agents/skills/vizarc/SKILL.md` | `~/.codex/skills/vizarc/SKILL.md` | Invoke via `$vizarc` or prompt |
| **Cursor / Copilot / OpenCode** | `.agents/skills/vizarc/SKILL.md` | `~/.cursor/`, `~/.copilot/`, `~/.config/opencode/` | `vizarc install-skill --scope project` |

#### 2. Verify Installation
```bash
# Validate YAML frontmatter, metadata constraints, and relative links across platforms
python shared/scripts/validate_skills.py

# Check Python dependencies, presets, and installed global skills
vizarc doctor

# Smoke-test offline IR compilation, layout QA & browser rendering
vizarc template ecommerce-platform --format html -o test_arch.html
vizarc validate test_arch.html
vizarc browser-check test_arch.html
```

Open any repository in Claude Code, Antigravity, or Codex and ask:
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
   *(Note: `vizarc compile`, `vizarc template`, `vizarc validate`, `vizarc compare`, and `vizarc diagnose` work 100% offline with no API key.)*

---

## 💻 CLI Usage

### Compile Agent-Authored IR (Zero API Key)
```bash
vizarc compile arch_ir.json --format html --strict -o architecture.html
vizarc compile arch_ir.json --format svg --orientation horizontal -o architecture.svg
vizarc compile arch_ir.json --format all -o ./vizarc_out
```

### Render Presets (100% Offline)
```bash
vizarc templates
vizarc template ecommerce-platform --format html -o ecommerce.html
vizarc template serverless-aws --format svg -o serverless.svg
vizarc template microservices-gke --format all -o ./gke_export
```

### Generate, Scan, Diagnose, QA & Visual Diff
```bash
vizarc generate "Microservices payment platform with Stripe, Kafka, and Postgres" --format all --output ./dist
vizarc scan . --format all --output ./architecture_docs
vizarc diagnose .
vizarc validate architecture.html
vizarc browser-check architecture.html
vizarc compare base_arch.html head_arch.html --format html -o architecture_diff.html
```

---

## 🌐 Live Demo (Streamlit Studio)

Try the interactive browser demo without installing locally:
👉 **[VizArc - Architecture Studio · Streamlit](https://vizarc.streamlit.app/)**

Or run the demo UI locally:
```bash
streamlit run app.py
```

---

## 🤖 GitHub Action: Automated PR Diagram Comments

VizArc includes `.github/workflows/vizarc-diagram.yml`. Add a `vizarc` code block in a Pull Request description to auto-generate and post diagrams as a PR comment:

````markdown
```vizarc
Microservices architecture with API Gateway, Auth Service, Order Service, and PostgreSQL database
```
````
