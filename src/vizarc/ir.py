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
  "archetype": "architecture|workflow|dataflow|sequence",
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
