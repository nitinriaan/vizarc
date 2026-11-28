"""
VizArc JSON Intermediate Representation (IR) Schema and Validator.
Follows the structured architecture model for interactive diagram compilation.
"""

import json
from typing import Dict, Any, List, Optional

IR_SCHEMA_PROMPT = """You are an expert software architect.
Transform the user's specification or codebase into a structured JSON Intermediate Representation (IR).

CRITICAL SCHEMA RULES:
1. Output ONLY a valid JSON object. No markdown backticks (no ```json). No preamble.
2. Structure must strictly adhere to this schema:
{
  "title": "System Architecture Title",
  "summary": "Clear, publication-grade executive summary of the architecture and key design objectives.",
  "archetype": "architecture|workflow|sequence|dataflow|lifecycle|erd|class|tree|timeline|waterfall",
  "decisions": [
    {
      "decision": "Architecture Decision Name (e.g. Asynchronous Event-Driven Messaging)",
      "rationale": "Why this design choice was selected and the specific benefits it delivers.",
      "tradeoff": "Consequences, operational complexities, or trade-offs accepted.",
      "status": "Accepted"
    }
  ],
  "flow_steps": [
    {
      "step": 1,
      "title": "Ingress & Edge Routing",
      "from": "source_node_id",
      "to": "target_node_id",
      "protocol": "HTTPS",
      "description": "What happens during this phase of the transaction lifecycle."
    }
  ],
  "tiers": [
    {"id": "client", "label": "Client / Frontend", "color": "#3B82F6"},
    {"id": "gateway", "label": "Ingress & API Gateway", "color": "#8B5CF6"},
    {"id": "services", "label": "Core Services", "color": "#10B981"},
    {"id": "data", "label": "Data & Caching Layer", "color": "#F59E0B"}
  ],
  "nodes": [
    {
      "id": "unique_alphanumeric_id",
      "label": "Component Name",
      "tier": "client|gateway|services|data",
      "tech": "Framework / Language / Tool (e.g. Next.js, Go, Redis)",
      "description": "What this component does.",
      "files": ["optional/file/path.py"]
    }
  ],
  "edges": [
    {
      "from": "source_node_id",
      "to": "target_node_id",
      "label": "Action / Message (e.g. Authenticate, Query)",
      "protocol": "HTTPS|gRPC|REST|SQL|WebSocket|Kafka"
    }
  ]
}
3. Ensure every node has a valid 'tier' that matches one of the defined tiers.
4. Ensure all edge 'from' and 'to' IDs exist in 'nodes'.
5. Order tiers logically from ingress/client at the top to storage/data at the bottom.
"""

def _auto_generate_decisions(nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Synthesizes high-level architectural decisions and trade-offs when not provided."""
    decisions = []
    nodes_tech_str = " ".join((n.get("tech", "") + " " + n.get("label", "")).lower() for n in nodes)

    if any(k in nodes_tech_str for k in ["redis", "memcached", "cache"]):
        decisions.append({
            "decision": "Distributed In-Memory Caching",
            "rationale": "Sub-millisecond read access for high-frequency user sessions and catalog lookups, offloading 85%+ read load from primary storage.",
            "tradeoff": "Requires strict TTL and cache invalidation policies; transient risk of serving stale data during rapid updates.",
            "status": "Accepted"
        })

    if any(k in nodes_tech_str for k in ["kafka", "sqs", "sns", "pubsub", "eventbridge", "queue", "rabbitmq"]):
        decisions.append({
            "decision": "Event-Driven Asynchronous Backbone",
            "rationale": "Decouples write-heavy downstream processing (notifications, payments, analytics) from synchronous API latency.",
            "tradeoff": "Embraces eventual consistency; requires idempotency tokens and dead-letter queues (DLQs) to handle failed events.",
            "status": "Accepted"
        })

    if any(k in nodes_tech_str for k in ["cloudfront", "cloudflare", "cdn", "edge", "waf"]):
        decisions.append({
            "decision": "Edge Acceleration & Perimeter Security",
            "rationale": "Terminates TLS, absorbs Layer 7 DDoS attacks, and caches static assets globally close to users.",
            "tradeoff": "Requires coordinated cache purging pipelines and edge routing synchronization on deployments.",
            "status": "Accepted"
        })

    if any(k in nodes_tech_str for k in ["postgres", "mysql", "rds", "aurora", "sql"]):
        decisions.append({
            "decision": "ACID Relational Core for Financial State",
            "rationale": "Guarantees strict atomicity and transactional integrity for billing, account ledgers, and order checkout.",
            "tradeoff": "Horizontal scaling requires read replicas or connection pooling (PgBouncer); bounded write throughput per primary instance.",
            "status": "Accepted"
        })

    if not decisions:
        decisions.append({
            "decision": "Tiered Microservice Architecture",
            "rationale": "Decomposes monolithic responsibilities into isolated, independently deployable domain services.",
            "tradeoff": "Introduces distributed tracing overhead, inter-service network latency, and version contract governance.",
            "status": "Accepted"
        })

    decisions.append({
        "decision": "Unified API Gateway & Ingress Boundary",
        "rationale": "Centralizes authentication, rate limiting, SSL termination, and protocol routing in a single managed perimeter.",
        "tradeoff": "Represents a single point of ingress requiring high-availability multi-AZ deployment and circuit breaking.",
        "status": "Accepted"
    })
    return decisions

def _auto_generate_flow_steps(nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Synthesizes step-by-step transaction flow narrative from graph edges."""
    steps = []
    node_map = {n["id"]: n for n in nodes}
    for idx, e in enumerate(edges[:8], start=1):
        src = node_map.get(e["from"], {})
        tgt = node_map.get(e["to"], {})
        src_label = src.get("label", e["from"])
        tgt_label = tgt.get("label", e["to"])
        action = e.get("label") or "Forward Request"
        proto = e.get("protocol") or "HTTPS"
        steps.append({
            "step": idx,
            "title": f"{src_label} → {tgt_label}",
            "from": e["from"],
            "to": e["to"],
            "protocol": proto.upper(),
            "description": f"Payload transmitted via {proto.upper()} ({action}) from {src_label} to {tgt_label} for validation and processing."
        })
    return steps

def validate_ir(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates and normalizes the Architecture IR dictionary.
    Guarantees publication-grade explainer metadata (decisions, flow steps, archetype).
    """
    if not isinstance(data, dict):
        raise ValueError("IR data must be a dictionary.")

    title = data.get("title", "Software Architecture")
    summary = data.get("summary", "Interactive system architecture map.")
    archetype = data.get("archetype", "architecture")
    tiers = data.get("tiers", [])
    nodes = data.get("nodes", [])
    edges = data.get("edges", [])
    decisions = data.get("decisions", [])
    flow_steps = data.get("flow_steps", [])

    if not tiers:
        tiers = [
            {"id": "client", "label": "Client Tier", "color": "#3B82F6"},
            {"id": "gateway", "label": "Gateway / Ingress", "color": "#8B5CF6"},
            {"id": "services", "label": "Services Layer", "color": "#10B981"},
            {"id": "data", "label": "Data Storage", "color": "#F59E0B"}
        ]

    tier_ids = {t["id"] for t in tiers}
    validated_nodes = []
    node_ids = set()

    for node in nodes:
        node_id = str(node.get("id", "")).strip().replace(" ", "_").lower()
        if not node_id:
            continue
        tier = node.get("tier", "services")
        if tier not in tier_ids:
            tier = list(tier_ids)[0]

        validated_nodes.append({
            "id": node_id,
            "label": node.get("label", node_id),
            "tier": tier,
            "tech": node.get("tech", "General"),
            "description": node.get("description", ""),
            "files": node.get("files", [])
        })
        node_ids.add(node_id)

    validated_edges = []
    for edge in edges:
        from_id = str(edge.get("from", "")).strip().replace(" ", "_").lower()
        to_id = str(edge.get("to", "")).strip().replace(" ", "_").lower()
        if from_id in node_ids and to_id in node_ids:
            validated_edges.append({
                "from": from_id,
                "to": to_id,
                "label": edge.get("label", ""),
                "protocol": edge.get("protocol", "TCP/HTTP")
            })

    # Validate or auto-generate decisions
    if not decisions or not isinstance(decisions, list):
        decisions = _auto_generate_decisions(validated_nodes, validated_edges)

    # Validate or auto-generate flow steps
    if not flow_steps or not isinstance(flow_steps, list):
        flow_steps = _auto_generate_flow_steps(validated_nodes, validated_edges)

    return {
        "title": title,
        "summary": summary,
        "archetype": archetype,
        "decisions": decisions,
        "flow_steps": flow_steps,
        "tiers": tiers,
        "nodes": validated_nodes,
        "edges": validated_edges
    }

def get_demo_ir() -> Dict[str, Any]:
    """Provides a realistic fallback IR for offline testing."""
    return {
        "title": "E-Commerce Microservices Platform",
        "summary": "Distributed event-driven architecture with dedicated services, caching, and async queues designed for high concurrency.",
        "archetype": "architecture",
        "decisions": [
            {
                "decision": "Event-Driven Asynchronous Decoupling",
                "rationale": "Decouples order checkout from payment processing, shipping dispatch, and analytics via Kafka, guaranteeing sub-100ms API response times.",
                "tradeoff": "Embraces eventual consistency and necessitates idempotency tokens and dead-letter queues (DLQs) for failed delivery.",
                "status": "Accepted"
            },
            {
                "decision": "Redis Read & Session Caching",
                "rationale": "Absorbs 90%+ read traffic for user sessions, carts, and active catalog items, protecting PostgreSQL from connection exhaustion.",
                "tradeoff": "Requires proactive cache invalidation on order mutation and memory pressure eviction governance.",
                "status": "Accepted"
            },
            {
                "decision": "Independent Microservice Boundaries",
                "rationale": "Isolates Auth, Orders, and Payments into autonomous services that scale independently across differing traffic shapes.",
                "tradeoff": "Network boundary hops introduce ~5-15ms inter-service latency and require distributed telemetry tracing.",
                "status": "Accepted"
            }
        ],
        "flow_steps": [
            {
                "step": 1,
                "title": "Client Ingress & TLS Termination",
                "from": "web_app",
                "to": "api_gw",
                "protocol": "HTTPS",
                "description": "User browser dispatches checkout request; API Gateway terminates TLS and verifies rate limits."
            },
            {
                "step": 2,
                "title": "Authentication & Token Validation",
                "from": "api_gw",
                "to": "auth_svc",
                "protocol": "gRPC",
                "description": "Gateway issues high-speed gRPC call to Auth Service to validate JWT bearer claims."
            },
            {
                "step": 3,
                "title": "Session Cache Verification",
                "from": "auth_svc",
                "to": "redis_cache",
                "protocol": "TCP",
                "description": "Auth service validates user session token in low-latency Redis cache."
            },
            {
                "step": 4,
                "title": "Order Ingestion & Validation",
                "from": "api_gw",
                "to": "order_svc",
                "protocol": "REST",
                "description": "Gateway forwards authenticated payload to Order Service for inventory allocation."
            },
            {
                "step": 5,
                "title": "Transactional Persistence",
                "from": "order_svc",
                "to": "orders_db",
                "protocol": "SQL",
                "description": "Order records committed to primary PostgreSQL database with ACID guarantees."
            },
            {
                "step": 6,
                "title": "Payment Authorization",
                "from": "order_svc",
                "to": "payment_svc",
                "protocol": "HTTPS",
                "description": "Order Service initiates payment authorization token exchange with Payment Gateway."
            },
            {
                "step": 7,
                "title": "Asynchronous Event Broadcast",
                "from": "order_svc",
                "to": "event_broker",
                "protocol": "Kafka",
                "description": "Publishes 'OrderPlaced' event onto Kafka topic for shipping, emails, and warehouse workers."
            }
        ],
        "tiers": [
            {"id": "client", "label": "Client Layer", "color": "#3B82F6"},
            {"id": "gateway", "label": "API & Ingress", "color": "#8B5CF6"},
            {"id": "services", "label": "Microservices", "color": "#10B981"},
            {"id": "data", "label": "Data & Caching", "color": "#F59E0B"}
        ],
        "nodes": [
            {
                "id": "web_app",
                "label": "Next.js Web Store",
                "tier": "client",
                "tech": "Next.js / React / TypeScript",
                "description": "User-facing e-commerce storefront with server-side rendering.",
                "files": ["src/app/*", "src/components/*"]
            },
            {
                "id": "mobile_app",
                "label": "Mobile App",
                "tier": "client",
                "tech": "React Native / Expo",
                "description": "iOS and Android client application.",
                "files": ["mobile/src/*"]
            },
            {
                "id": "api_gw",
                "label": "API Gateway",
                "tier": "gateway",
                "tech": "Envoy / Traefik",
                "description": "Handles TLS termination, rate limiting, and reverse proxy routing.",
                "files": ["infra/gateway/envoy.yaml"]
            },
            {
                "id": "auth_svc",
                "label": "Auth Service",
                "tier": "services",
                "tech": "Go / OAuth2 / JWT",
                "description": "Issues tokens, manages sessions, and verifies user authorization.",
                "files": ["services/auth/main.go"]
            },
            {
                "id": "order_svc",
                "label": "Order Service",
                "tier": "services",
                "tech": "FastAPI / Python 3.12",
                "description": "Processes purchases, updates inventory, and orchestrates fulfillment.",
                "files": ["services/orders/app.py"]
            },
            {
                "id": "payment_svc",
                "label": "Payment Service",
                "tier": "services",
                "tech": "Node.js / Express",
                "description": "Integrates with Stripe API and processes transaction webhooks.",
                "files": ["services/payments/index.js"]
            },
            {
                "id": "redis_cache",
                "label": "Redis Session Cache",
                "tier": "data",
                "tech": "Redis 7.2",
                "description": "High-throughput in-memory cache for user sessions and rate limits.",
                "files": []
            },
            {
                "id": "orders_db",
                "label": "Orders Database",
                "tier": "data",
                "tech": "PostgreSQL 16",
                "description": "ACID transactional database storing customer orders and line items.",
                "files": ["db/migrations/orders.sql"]
            },
            {
                "id": "event_broker",
                "label": "Kafka Event Bus",
                "tier": "data",
                "tech": "Apache Kafka",
                "description": "Asynchronous event streaming bus for order updates and shipping notices.",
                "files": ["events/topics.json"]
            }
        ],
        "edges": [
            {"from": "web_app", "to": "api_gw", "label": "HTTPS / GraphQL", "protocol": "HTTPS"},
            {"from": "mobile_app", "to": "api_gw", "label": "HTTPS / REST", "protocol": "HTTPS"},
            {"from": "api_gw", "to": "auth_svc", "label": "gRPC Token Check", "protocol": "gRPC"},
            {"from": "api_gw", "to": "order_svc", "label": "Dispatch Order", "protocol": "REST"},
            {"from": "auth_svc", "to": "redis_cache", "label": "Read Session", "protocol": "TCP"},
            {"from": "order_svc", "to": "payment_svc", "label": "Trigger Charge", "protocol": "HTTPS"},
            {"from": "order_svc", "to": "orders_db", "label": "Insert Order", "protocol": "SQL"},
            {"from": "order_svc", "to": "event_broker", "label": "Publish 'OrderPlaced'", "protocol": "Kafka"}
        ]
    }


# ==============================================================================
# 10 ARCHIFY DIAGRAM ARCHETYPES & GUIDANCE ENGINE
# ==============================================================================

ARCHETYPES: Dict[str, Dict[str, Any]] = {
    "architecture": {
        "name": "System Architecture",
        "description": "Multi-tier services, cloud infra, microservices, component topology",
        "default_tiers": [
            {"id": "client", "label": "Client / Edge", "color": "#3B82F6"},
            {"id": "gateway", "label": "API Gateway & Ingress", "color": "#8B5CF6"},
            {"id": "services", "label": "Core Services", "color": "#10B981"},
            {"id": "data", "label": "Data & Persistence", "color": "#F59E0B"}
        ],
        "keywords": ["architecture", "microservices", "cloud", "aws", "gcp", "azure", "docker", "k8s", "kubernetes", "api", "backend", "frontend", "serverless"]
    },
    "workflow": {
        "name": "Process Workflow",
        "description": "Step-by-step human/system processes, approval chains, CI/CD automation",
        "default_tiers": [
            {"id": "trigger", "label": "Trigger / Initiation", "color": "#3B82F6"},
            {"id": "execution", "label": "Processing & Verification", "color": "#10B981"},
            {"id": "approval", "label": "Approval & Review", "color": "#8B5CF6"},
            {"id": "completion", "label": "Completion / Output", "color": "#06B6D4"}
        ],
        "keywords": ["workflow", "pipeline", "ci/cd", "automation", "approval", "human", "step", "process", "onboarding", "dispatch"]
    },
    "sequence": {
        "name": "Sequence & Handshake",
        "description": "Chronological messaging, API handshakes, auth protocols, request-response lifecycles",
        "default_tiers": [
            {"id": "initiator", "label": "Initiator / Client", "color": "#3B82F6"},
            {"id": "mediator", "label": "Mediator / Proxy", "color": "#8B5CF6"},
            {"id": "target", "label": "Target Service", "color": "#10B981"},
            {"id": "vault", "label": "Identity / Token Store", "color": "#F59E0B"}
        ],
        "keywords": ["sequence", "handshake", "oauth", "jwt", "auth", "chronological", "callback", "redirect", "token exchange"]
    },
    "dataflow": {
        "name": "Data Flow & Streaming",
        "description": "Streaming pipelines, ETL jobs, event ingestion, batch transformation, analytics storage",
        "default_tiers": [
            {"id": "sources", "label": "Data Sources", "color": "#3B82F6"},
            {"id": "ingest", "label": "Ingestion / Streaming", "color": "#8B5CF6"},
            {"id": "transform", "label": "Processing & Enrichment", "color": "#10B981"},
            {"id": "lakehouse", "label": "Data Warehouse / Lake", "color": "#F59E0B"}
        ],
        "keywords": ["dataflow", "data flow", "etl", "streaming", "kafka", "pipeline", "spark", "flink", "bigquery", "snowflake", "lakehouse", "ingestion"]
    },
    "lifecycle": {
        "name": "State Machine / Lifecycle",
        "description": "Entity lifecycle states, state transitions, event hooks, terminal states",
        "default_tiers": [
            {"id": "initial", "label": "Initial / Created", "color": "#3B82F6"},
            {"id": "pending", "label": "Pending / In-Progress", "color": "#F59E0B"},
            {"id": "active", "label": "Active / Fulfilled", "color": "#10B981"},
            {"id": "terminal", "label": "Terminal / Archived", "color": "#EF4444"}
        ],
        "keywords": ["lifecycle", "state machine", "status", "transition", "state", "draft", "active", "cancelled", "settled", "refunded"]
    },
    "erd": {
        "name": "Entity Relationship (ERD)",
        "description": "Database entities, relational schemas, primary/foreign keys, cardinality",
        "default_tiers": [
            {"id": "identity_schema", "label": "Users & Identity Schema", "color": "#3B82F6"},
            {"id": "core_entities", "label": "Transactional Entities", "color": "#10B981"},
            {"id": "catalog_entities", "label": "Domain Catalog Entities", "color": "#8B5CF6"},
            {"id": "audit_entities", "label": "Audit & Analytics Entities", "color": "#F59E0B"}
        ],
        "keywords": ["erd", "database", "schema", "table", "foreign key", "primary key", "cardinality", "relational", "entities", "columns", "sql"]
    },
    "class": {
        "name": "Class Hierarchy",
        "description": "Object-oriented class structures, interfaces, inheritance, member methods & attributes",
        "default_tiers": [
            {"id": "interfaces", "label": "Core Interfaces / Abstract", "color": "#8B5CF6"},
            {"id": "base_classes", "label": "Base Implementations", "color": "#3B82F6"},
            {"id": "services", "label": "Concrete Domain Classes", "color": "#10B981"},
            {"id": "models", "label": "Data Value Objects", "color": "#F59E0B"}
        ],
        "keywords": ["class", "oop", "inheritance", "interface", "abstract", "polymorphism", "classes", "methods", "hierarchy"]
    },
    "tree": {
        "name": "Hierarchy Tree",
        "description": "Taxonomy, tree decomposition, nested organizational / directory structure",
        "default_tiers": [
            {"id": "root", "label": "Root Category", "color": "#3B82F6"},
            {"id": "branches", "label": "Primary Modules / Branches", "color": "#8B5CF6"},
            {"id": "submodules", "label": "Sub-systems", "color": "#10B981"},
            {"id": "leaves", "label": "Leaf Packages / Assets", "color": "#06B6D4"}
        ],
        "keywords": ["tree", "hierarchy", "taxonomy", "directory", "organization", "nested", "breakdown", "wbs", "package tree"]
    },
    "timeline": {
        "name": "Roadmap Timeline",
        "description": "Milestone delivery, release phases, quarterly roadmap, sprint progress",
        "default_tiers": [
            {"id": "phase1", "label": "Phase 1: Foundation (Q1)", "color": "#3B82F6"},
            {"id": "phase2", "label": "Phase 2: Core Platform (Q2)", "color": "#8B5CF6"},
            {"id": "phase3", "label": "Phase 3: Scale & Multi-Region (Q3)", "color": "#10B981"},
            {"id": "phase4", "label": "Phase 4: Autonomous AI (Q4)", "color": "#F59E0B"}
        ],
        "keywords": ["timeline", "roadmap", "milestone", "release", "phases", "quarter", "sprint", "schedule", "delivery"]
    },
    "waterfall": {
        "name": "Waterfall Stages",
        "description": "Sequential dependency stages, stage-gate reviews, transition criteria",
        "default_tiers": [
            {"id": "discovery", "label": "1. Discovery & Design", "color": "#3B82F6"},
            {"id": "build", "label": "2. Construction & Verification", "color": "#10B981"},
            {"id": "validation", "label": "3. Audit & Security Gate", "color": "#F59E0B"},
            {"id": "deployment", "label": "4. Production Handover", "color": "#06B6D4"}
        ],
        "keywords": ["waterfall", "stage-gate", "sequential", "gate", "handover", "compliance gate", "sign-off", "audit stage"]
    }
}

def detect_archetype(prompt: str) -> str:
    """Auto-detects the best diagram archetype from prompt text."""
    p_lower = prompt.lower()
    scores = {}
    for arch_id, meta in ARCHETYPES.items():
        score = 0
        for kw in meta["keywords"]:
            if kw in p_lower:
                score += (3 if kw == arch_id else 1)
        scores[arch_id] = score

    best_arch = max(scores, key=scores.get)
    return best_arch if scores[best_arch] > 0 else "architecture"

def guide_archetype(prompt: str) -> Dict[str, Any]:
    """Provides archetype selection guidance and an optimized prompt suggestion."""
    detected = detect_archetype(prompt)
    meta = ARCHETYPES.get(detected, ARCHETYPES["architecture"])
    
    tier_labels = " -> ".join([t["label"] for t in meta["default_tiers"]])
    suggested_prompt = (
        f"Create a {meta['name']} diagram: {prompt.strip()}. "
        f"Structure across the tiers: [{tier_labels}]. "
        f"Specify explicit communication protocols and data payloads on all connections."
    )

    return {
        "detected_archetype": detected,
        "archetype_name": meta["name"],
        "description": meta["description"],
        "recommended_tiers": meta["default_tiers"],
        "suggested_prompt": suggested_prompt,
        "all_archetypes": [
            {"id": k, "name": v["name"], "description": v["description"]}
            for k, v in ARCHETYPES.items()
        ]
    }

def lint_ir(ir: Dict[str, Any]) -> Dict[str, Any]:
    """
    Performs machine-readable static architectural linting of an IR graph.
    Returns structured diagnostics adhering to the Archify validation spec.
    """
    diagnostics = []
    nodes = ir.get("nodes", [])
    edges = ir.get("edges", [])
    tiers = ir.get("tiers", [])
    archetype = ir.get("archetype", "architecture")
    tier_ids = {t.get("id") for t in tiers}

    node_ids = {n.get("id") for n in nodes}
    in_degree = {nid: 0 for nid in node_ids}
    out_degree = {nid: 0 for nid in node_ids}
    adj = {nid: [] for nid in node_ids}

    for edge in edges:
        src = edge.get("from")
        tgt = edge.get("to")
        if src in node_ids and tgt in node_ids:
            out_degree[src] = out_degree.get(src, 0) + 1
            in_degree[tgt] = in_degree.get(tgt, 0) + 1
            adj[src].append(tgt)
        
        # Check missing or vague protocol
        proto = (edge.get("protocol") or "").strip()
        if not proto or proto.lower() in ("generic", "api", "tcp/http", "link"):
            diagnostics.append({
                "ruleCode": "WARN_UNSPECIFIED_PROTOCOL",
                "severity": "warning",
                "edge": f"{src}->{tgt}",
                "message": f"Edge from '{src}' to '{tgt}' lacks an explicit protocol (e.g. HTTPS, gRPC, SQL, Kafka).",
                "supportedFixes": ["specify_protocol"]
            })

    for node in nodes:
        nid = node.get("id")
        ntier = node.get("tier")
        label = node.get("label", nid)

        # Tier validity
        if ntier not in tier_ids:
            diagnostics.append({
                "ruleCode": "ERR_INVALID_TIER",
                "severity": "error",
                "nodeId": nid,
                "message": f"Node '{label}' is assigned to unknown tier '{ntier}'.",
                "supportedFixes": ["reassign_tier", "define_tier"]
            })

        # Orphan node check
        if in_degree.get(nid, 0) == 0 and out_degree.get(nid, 0) == 0:
            diagnostics.append({
                "ruleCode": "ERR_ORPHAN_NODE",
                "severity": "error",
                "nodeId": nid,
                "message": f"Node '{label}' is completely disconnected (0 inbound, 0 outbound connections).",
                "supportedFixes": ["connect_to_upstream", "connect_to_downstream", "remove_node"]
            })

        # Dead-end check (inbound but no outbound in non-terminal tiers)
        is_terminal = ntier in ("data", "completion", "vault", "lakehouse", "terminal", "audit_entities", "leaves", "phase4", "deployment")
        if in_degree.get(nid, 0) > 0 and out_degree.get(nid, 0) == 0 and not is_terminal:
            diagnostics.append({
                "ruleCode": "WARN_DEAD_END_NODE",
                "severity": "warning",
                "nodeId": nid,
                "message": f"Node '{label}' in tier '{ntier}' has inbound traffic but no outgoing connections.",
                "supportedFixes": ["connect_to_downstream", "mark_as_sink"]
            })

        # Empty description
        if not (node.get("description") or "").strip():
            diagnostics.append({
                "ruleCode": "INFO_EMPTY_DESCRIPTION",
                "severity": "info",
                "nodeId": nid,
                "message": f"Node '{label}' does not have an architectural responsibility description.",
                "supportedFixes": ["add_description"]
            })

        # SPOF check: high centrality
        total_deg = in_degree.get(nid, 0) + out_degree.get(nid, 0)
        if total_deg >= 4 and len(nodes) > 4:
            diagnostics.append({
                "ruleCode": "WARN_POTENTIAL_SPOF",
                "severity": "warning",
                "nodeId": nid,
                "message": f"Node '{label}' has high connection density ({total_deg} connections) and represents a potential Single Point of Failure (SPOF).",
                "supportedFixes": ["add_redundancy", "split_responsibilities"]
            })

    # Cycle detection for acyclic archetypes
    if archetype in ("workflow", "dataflow", "waterfall", "timeline"):
        visited = {}
        rec_stack = {}
        has_cycle = False
        cycle_edges = []

        def dfs(u):
            nonlocal has_cycle
            visited[u] = True
            rec_stack[u] = True
            for v in adj.get(u, []):
                if not visited.get(v, False):
                    if dfs(v):
                        return True
                elif rec_stack.get(v, False):
                    has_cycle = True
                    cycle_edges.append(f"{u}->{v}")
                    return True
            rec_stack[u] = False
            return False

        for nid in node_ids:
            if not visited.get(nid, False):
                if dfs(nid):
                    break

        if has_cycle:
            diagnostics.append({
                "ruleCode": "ERR_DIRECTED_CYCLE",
                "severity": "error",
                "message": f"Cyclic dependency detected in {archetype} diagram around {cycle_edges}. Pipelines should be directed acyclic graphs (DAGs).",
                "supportedFixes": ["break_cycle", "switch_archetype_to_architecture"]
            })

    errors = [d for d in diagnostics if d["severity"] == "error"]
    warnings = [d for d in diagnostics if d["severity"] == "warning"]

    return {
        "valid": len(errors) == 0,
        "archetype": archetype,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "error_count": len(errors),
        "warning_count": len(warnings),
        "info_count": len(diagnostics) - len(errors) - len(warnings),
        "diagnostics": diagnostics
    }

def compare_architectures(base_ir: Dict[str, Any], head_ir: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculates architectural delta between base and head IR models (Archify compare spec).
    Detects added, removed, and modified nodes and edges.
    """
    base_nodes = {n["id"]: n for n in base_ir.get("nodes", [])}
    head_nodes = {n["id"]: n for n in head_ir.get("nodes", [])}

    base_edges = {(e["from"], e["to"]): e for e in base_ir.get("edges", [])}
    head_edges = {(e["from"], e["to"]): e for e in head_ir.get("edges", [])}

    added_nodes = [head_nodes[nid] for nid in head_nodes if nid not in base_nodes]
    removed_nodes = [base_nodes[nid] for nid in base_nodes if nid not in head_nodes]
    
    modified_nodes = []
    for nid in base_nodes:
        if nid in head_nodes:
            b = base_nodes[nid]
            h = head_nodes[nid]
            changes = {}
            for field in ["label", "tier", "tech", "description"]:
                if b.get(field) != h.get(field):
                    changes[field] = {"before": b.get(field), "after": h.get(field)}
            if changes:
                modified_nodes.append({
                    "id": nid,
                    "label": h.get("label", nid),
                    "changes": changes
                })

    added_edges = [head_edges[k] for k in head_edges if k not in base_edges]
    removed_edges = [base_edges[k] for k in base_edges if k not in head_edges]

    summary_parts = []
    if added_nodes:
        summary_parts.append(f"+{len(added_nodes)} nodes added")
    if removed_nodes:
        summary_parts.append(f"-{len(removed_nodes)} nodes removed")
    if modified_nodes:
        summary_parts.append(f"~{len(modified_nodes)} nodes modified")
    if added_edges:
        summary_parts.append(f"+{len(added_edges)} connections added")
    if removed_edges:
        summary_parts.append(f"-{len(removed_edges)} connections removed")

    summary = ", ".join(summary_parts) if summary_parts else "No structural differences detected."

    return {
        "base_title": base_ir.get("title", "Base Architecture"),
        "head_title": head_ir.get("title", "Head Architecture"),
        "summary": summary,
        "delta": {
            "added_nodes": added_nodes,
            "removed_nodes": removed_nodes,
            "modified_nodes": modified_nodes,
            "added_edges": added_edges,
            "removed_edges": removed_edges
        }
    }
