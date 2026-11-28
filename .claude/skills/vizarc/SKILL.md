---
name: vizarc
description: Turn any idea, plan, or codebase into an interactive dual-view HTML explainer, pure vector SVG, or declarative diagram (D2, Mermaid, Structurizr C4, PlantUML, Graphviz DOT, Excalidraw, ASCII). Use when the user asks to visualize a codebase, create an architecture diagram, document system trade-offs, trace service dependencies, compare architecture diffs, or render preset cloud topologies.
license: MIT
compatibility: Requires Python 3.12+ and the vizarc CLI installed (`pip install -e .`). Works offline without API keys via `vizarc compile` and `vizarc template`.
argument-hint: "[prompt, path, or output format]"
allowed-tools: Bash(vizarc *), Read, Glob, Grep, Write
metadata:
  author: nitinriaan
  version: "0.4.0"
---

# VizArc — Universal Architecture Compiler & Explainer (Claude Code)

VizArc compiles a single **Canonical Architecture Model (JSON IR)** deterministically into:
- **Interactive HTML (`html`)**: Dual-view canvas (pan/zoom, animated flow motion, 188+ embedded cloud icons, upstream/downstream tracing, minimap) + One-Page Architectural Explainer (executive summary, ADRs, transaction stepper, protocol matrix).
- **Pure Vector SVG (`svg`)**: Publication-grade vector diagram for READMEs, PRs, and slides (`--orientation horizontal|vertical`).
- **Declarative & Text Formats**: `d2`, `mermaid`, `structurizr` (C4 DSL), `plantuml`, `graphviz` (DOT), `excalidraw`, `ascii`, `ir` (normalized JSON), or `all`.

## Primary Workflow (Zero External API Key Needed)

When running inside Claude Code, **you** analyze the codebase or prompt directly, author a Canonical Architecture IR JSON, and compile it deterministically with `vizarc compile`:

1. **Inspect the codebase or requirements**:
   - Use `Glob`, `Grep`, and `Read` to map entrypoints, services, queues, databases, external APIs, and real file paths.
   - Optionally run `vizarc diagnose .` to detect circular dependencies, fan-in/fan-out coupling hotspots, and the recommended archetype.
2. **Author the Canonical Architecture IR JSON**:
   - Read [ir-schema.md](../../../shared/references/ir-schema.md) for the exact IR schema, 10 archetypes (`architecture`, `workflow`, `sequence`, `dataflow`, `lifecycle`, `erd`, `class`, `tree`, `timeline`, `waterfall`), tier IDs, and static lint rules.
   - Include `decisions` (ADRs), `flow_steps`, `tiers`, `nodes` (with `files`), and `edges` (with explicit `protocol` values like `HTTPS`, `gRPC`, `REST`, `SQL`, `Kafka`, `Redis`).
3. **Compile & validate deterministically**:
   ```bash
   vizarc compile arch_ir.json --format html --strict -o architecture.html
   vizarc compile arch_ir.json --format svg --orientation horizontal -o architecture.svg
   vizarc compile arch_ir.json --format all -o ./vizarc_out
   ```
   - Clean up temporary IR JSON files if the user only requested the rendered diagram.
4. **Report results**:
   - Share the output file path(s), run `vizarc validate architecture.html` (static + SVG layout collision checks) and `vizarc browser-check architecture.html` when validating HTML, and note that `.html` files run 100% offline in any browser (`1` Canvas, `2` One-Page Explainer, `M` Motion, `O` Flip Orientation, `🎥 Story` WebM video export, `🖨️ PDF` print).

## Alternative CLI Workflows

- **13 Offline Preset Architectures**: `vizarc templates` and `vizarc template <id> --format html -o out.html`
- **Automated Repo Scan / Prompt Generation** (uses `GEMINI_API_KEY` if set): `vizarc scan .`, `vizarc generate "..."`, `vizarc guide "..."`
- **Validate, Browser QA & Visual Diffs**: `vizarc validate architecture.html`, `vizarc browser-check architecture.html`, and `vizarc compare base.html head.html --format html -o diff.html`
- **Environment Diagnostic**: `vizarc doctor`
