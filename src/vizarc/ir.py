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
  "summary": "Brief 1-2 sentence high-level summary of the architecture.",
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

def validate_ir(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates and normalizes the Architecture IR dictionary.
    """
    if not isinstance(data, dict):
        raise ValueError("IR data must be a dictionary.")

    title = data.get("title", "Software Architecture")
    summary = data.get("summary", "Interactive system architecture map.")
    tiers = data.get("tiers", [])
    nodes = data.get("nodes", [])
    edges = data.get("edges", [])

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

    return {
        "title": title,
        "summary": summary,
        "tiers": tiers,
        "nodes": validated_nodes,
        "edges": validated_edges
    }

def get_demo_ir() -> Dict[str, Any]:
    """Provides a realistic fallback IR for offline testing."""
    return {
        "title": "E-Commerce Microservices Platform",
        "summary": "Distributed event-driven architecture with dedicated services, caching, and async queues.",
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
