# VizArc Canonical Architecture IR Reference

## 1. JSON Schema

```json
{
  "title": "System Architecture Title",
  "summary": "Conclusion-first executive summary of the system and design goals.",
  "archetype": "architecture",
  "decisions": [
    {
      "decision": "Architecture Decision Name",
      "rationale": "Why this choice was made and what it enables.",
      "tradeoff": "Accepted operational cost or complexity.",
      "status": "Accepted"
    }
  ],
  "flow_steps": [
    {
      "step": 1,
      "title": "Client Ingress",
      "from": "web_app",
      "to": "api_gw",
      "protocol": "HTTPS",
      "description": "What happens during this step."
    }
  ],
  "tiers": [
    {"id": "client", "label": "Client / Edge", "color": "#3B82F6"},
    {"id": "gateway", "label": "API Gateway & Ingress", "color": "#8B5CF6"},
    {"id": "services", "label": "Core Services", "color": "#10B981"},
    {"id": "data", "label": "Data & Persistence", "color": "#F59E0B"}
  ],
  "nodes": [
    {
      "id": "web_app",
      "label": "Web App",
      "tier": "client",
      "tech": "Next.js / TypeScript",
      "description": "Customer-facing frontend application.",
      "files": ["src/app/page.tsx"]
    }
  ],
  "edges": [
    {
      "from": "web_app",
      "to": "api_gw",
      "label": "API Request",
      "protocol": "HTTPS"
    }
  ]
}
```

### Normalization Rules (`validate_ir`)
- `node.id` and edge `from`/`to` are normalized via `.strip().replace(" ", "_").lower()`.
- Every `node.tier` must match an `id` in `tiers` (otherwise reassigned or flagged by `lint_ir`).
- Every edge `from` and `to` must reference an existing `node.id`.
- If `decisions` or `flow_steps` are omitted, VizArc synthesizes defaults, but explicit domain-specific entries produce richer One-Page Explainers.

## 2. Supported Archetypes & Default Tiers

| Archetype | Use For | Default Tier IDs (Top → Bottom) |
| :--- | :--- | :--- |
| `architecture` | Multi-tier services, cloud infra, microservices | `client`, `gateway`, `services`, `data` |
| `workflow` | Approval chains, CI/CD, process automation (acyclic) | `trigger`, `execution`, `approval`, `completion` |
| `sequence` | Handshakes, OAuth/JWT flows, request lifecycles | `initiator`, `mediator`, `target`, `vault` |
| `dataflow` | Streaming, ETL, event ingestion, analytics (acyclic) | `sources`, `ingest`, `transform`, `lakehouse` |
| `lifecycle` | State machines, entity status transitions | `initial`, `pending`, `active`, `terminal` |
| `erd` | Relational database schemas, tables, keys | `identity_schema`, `core_entities`, `catalog_entities`, `audit_entities` |
| `class` | OOP interfaces, inheritance, domain models | `interfaces`, `base_classes`, `services`, `models` |
| `tree` | Taxonomies, org charts, package trees | `root`, `branches`, `submodules`, `leaves` |
| `timeline` | Roadmaps, release phases, quarterly milestones (acyclic) | `phase1`, `phase2`, `phase3`, `phase4` |
| `waterfall` | Stage-gate delivery, audit & sign-off stages (acyclic) | `discovery`, `build`, `validation`, `deployment` |

## 3. Built-in Offline Templates (`vizarc template <id>`)

`serverless-aws`, `rag-system`, `microservices-gke`, `fullstack-nextjs`, `event-streaming-kafka`, `monolith-aws`, `k8s-platform`, `event-driven-aws`, `data-lakehouse`, `ml-pipeline`, `ecommerce-platform`, `iot-platform`, `web3-blockchain`.

## 4. Static Validation Rules (`vizarc validate` / `--strict`)

- `ERR_INVALID_TIER`: Node assigned to a tier ID not present in `tiers`.
- `ERR_ORPHAN_NODE`: Node has 0 incoming and 0 outgoing edges.
- `ERR_DIRECTED_CYCLE`: Cycle detected in an acyclic archetype (`workflow`, `dataflow`, `waterfall`, `timeline`).
- `WARN_UNSPECIFIED_PROTOCOL`: Edge has empty or generic protocol (`generic`, `api`, `tcp/http`, `link`). Prefer explicit protocols (`HTTPS`, `gRPC`, `REST`, `SQL`, `Kafka`, `Redis`, `WebSocket`, `AMQP`).
- `WARN_DEAD_END_NODE`: Non-terminal tier node has inbound edges but no outbound edges.
- `WARN_POTENTIAL_SPOF`: Node has `>= 4` total connections in graphs with `> 4` nodes.
- `INFO_EMPTY_DESCRIPTION`: Node lacks a `description`.

## 5. Output Formats (`--format`)

| Value | Extension | Notes |
| :--- | :--- | :--- |
| `html` | `.html` | Default; self-contained interactive canvas + one-page explainer |
| `svg` | `.svg` | Pure vector SVG; supports `--orientation horizontal\|vertical` |
| `d2` | `.d2` | D2 declarative diagram |
| `mermaid` | `.mmd` | Mermaid flowchart |
| `structurizr` | `.dsl` | Structurizr C4 DSL with cloud themes |
| `plantuml` | `.puml` | PlantUML component diagram |
| `graphviz` | `.dot` | Graphviz DOT graph |
| `excalidraw` | `.excalidraw.mmd` | Excalidraw-compatible diagram syntax |
| `ascii` | `.txt` | Terminal box diagram |
| `ir` | `.json` | Validated/normalized Canonical IR JSON |
| `all` | directory | Writes all formats simultaneously |
