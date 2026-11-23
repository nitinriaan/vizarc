"""
VizArc Cloud Service Catalog & Icon Metadata Library.
Inspired by vizarch: maps cloud services (AWS, GCP, Azure, K8s, Generic)
to brand colors, categories, and 24x24 SVG icon glyphs.
"""

from typing import Dict, Any, Optional

# Provider Brand Colors
PROVIDER_COLORS = {
    "aws": "#FF9900",
    "gcp": "#4285F4",
    "azure": "#0089D6",
    "kubernetes": "#326CE5",
    "generic": "#6366F1",
}

# Category Colors
TYPE_COLORS = {
    "compute": "#3B82F6",
    "container": "#2563EB",
    "database": "#10B981",
    "cache": "#EF4444",
    "storage": "#F59E0B",
    "cdn": "#8B5CF6",
    "messaging": "#EC4899",
    "queue": "#F97316",
    "networking": "#06B6D4",
    "analytics": "#14B8A6",
    "monitoring": "#64748B",
    "security": "#84CC16",
    "ai": "#A855F7",
    "frontend": "#0EA5E9",
    "external": "#6B7280",
}

# Protocol Line Colors
PROTOCOL_COLORS = {
    "https": "#3B82F6",
    "http": "#3B82F6",
    "grpc": "#8B5CF6",
    "sql": "#10B981",
    "postgres": "#10B981",
    "mysql": "#0EA5E9",
    "redis": "#EF4444",
    "kafka": "#F97316",
    "event": "#EC4899",
    "websocket": "#06B6D4",
    "tcp": "#64748B",
}

# 24x24 SVG Path Glyphs for Crisp Vector Badges
ICON_PATHS = {
    "cloud": "M6 18a4 4 0 0 1 .5-7.97A6 6 0 0 1 18 9a3.5 3.5 0 0 1 0 7H6z",
    "server": "M5 4h14a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1zm0 8h14a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1zM7 6.5h.01M7 14.5h.01",
    "database": "M4 6c0-1.66 3.58-3 8-3s8 1.34 8 3v12c0 1.66-3.58 3-8 3s-8-1.34-8-3V6zm0 4c0 1.66 3.58 3 8 3s8-1.34 8-3M4 14c0 1.66 3.58 3 8 3s8-1.34 8-3",
    "cache": "M13 2 4 14h6l-1 8 9-12h-6l1-8z",
    "cube": "M12 2 3 7v10l9 5 9-5V7l-9-5zm0 0v20M3 7l9 5 9-5",
    "storage": "M3 7l9-4 9 4v10l-9 4-9-4V7z",
    "queue": "M4 6h16M4 12h16M4 18h16",
    "globe": "M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm0 0c3 3 4.5 6.5 4.5 10S15 19 12 22M12 2c-3 3-4.5 6.5-4.5 10S9 19 12 22M2 12h20",
    "shield": "M12 2 4 6v6c0 5 3.5 9 8 10 4.5-1 8-5 8-10V6l-8-4z",
    "eye": "M2 12s4-7 10-7 10 7 10 7-4 7-10 7-10-7-10-7zm10 3a3 3 0 1 0 0-6 3 3 0 0 0 0 6z",
    "ai": "M12 2a3 3 0 0 1 3 3v1h1a3 3 0 0 1 3 3v2h1a3 3 0 0 1 3 3v2a3 3 0 0 1-3 3h-1v2a3 3 0 0 1-3 3h-1v1a3 3 0 0 1-6 0v-1H8a3 3 0 0 1-3-3v-2H4a3 3 0 0 1-3-3v-2a3 3 0 0 1 3-3h1V8a3 3 0 0 1 3-3h1V5a3 3 0 0 1 3-3z",
    "frontend": "M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zM4 9h16",
}

# Catalog mapping keywords to service metadata
SERVICE_RULES = [
    # AWS
    (["lambda", "serverless function"], "aws", "compute", "bolt", "#FF9900", "AWS Lambda"),
    (["s3", "blob storage", "bucket"], "aws", "storage", "storage", "#569A31", "Amazon S3"),
    (["dynamodb", "dynamo"], "aws", "database", "database", "#4053D6", "Amazon DynamoDB"),
    (["rds", "aurora", "postgres", "postgresql"], "aws", "database", "database", "#527FFF", "Amazon RDS / PostgreSQL"),
    (["elasticache", "redis", "memorystore"], "generic", "cache", "cache", "#DC382D", "Redis Cache"),
    (["cloudfront", "cdn", "cloudflare"], "aws", "cdn", "globe", "#8C4FFF", "CloudFront CDN"),
    (["api gateway", "apigateway", "kong", "traefik"], "aws", "networking", "cloud", "#E7157B", "API Gateway"),
    (["sns", "eventbridge", "pubsub", "pub/sub"], "aws", "messaging", "queue", "#FF4F8B", "Event Bus / SNS"),
    (["sqs", "rabbitmq", "queue"], "aws", "queue", "queue", "#FF4F8B", "SQS Queue"),
    (["kafka"], "generic", "messaging", "queue", "#231F20", "Apache Kafka"),
    (["ecs", "fargate", "container"], "aws", "container", "cube", "#FF9900", "Amazon ECS"),
    (["ec2", "virtual machine", "vm"], "aws", "compute", "server", "#FF9900", "Amazon EC2"),
    (["cloudwatch", "datadog", "grafana", "prometheus"], "generic", "monitoring", "eye", "#64748B", "Monitoring"),
    (["bedrock", "sagemaker", "llm", "openai", "gemini", "claude"], "generic", "ai", "ai", "#A855F7", "AI / LLM Service"),
    # GCP & Kubernetes
    (["gke", "k8s", "kubernetes"], "kubernetes", "container", "cube", "#326CE5", "Kubernetes / GKE"),
    (["cloud sql", "bigquery"], "gcp", "database", "database", "#4285F4", "Google Cloud SQL"),
    (["load balancer", "alb", "elb", "ingress"], "generic", "networking", "globe", "#0089D6", "Load Balancer"),
    # Frontend
    (["next.js", "react", "vue", "frontend", "spa", "client", "web app", "vercel"], "generic", "frontend", "frontend", "#0EA5E9", "Web Application"),
]

def infer_service_metadata(label: str, tech: str = "", tier: str = "services") -> Dict[str, Any]:
    """
    Infers cloud provider, category, icon glyph, and brand color from node text.
    """
    search_text = f"{label} {tech} {tier}".lower()

    for keywords, provider, s_type, icon_key, color, canonical_name in SERVICE_RULES:
        if any(kw in search_text for kw in keywords):
            return {
                "provider": provider,
                "type": s_type,
                "icon": ICON_PATHS.get(icon_key, ICON_PATHS["cube"]),
                "icon_name": icon_key,
                "brand_color": color,
                "service_name": canonical_name
            }

    # Fallback based on tier
    fallback_map = {
        "client": ("generic", "frontend", "frontend", "#0EA5E9", "Client / UI"),
        "gateway": ("generic", "networking", "cloud", "#8B5CF6", "Gateway"),
        "services": ("generic", "compute", "server", "#3B82F6", "Service"),
        "data": ("generic", "database", "database", "#10B981", "Database Storage")
    }

    prov, s_type, icon_key, color, s_name = fallback_map.get(tier, ("generic", "compute", "cube", "#6366F1", "Component"))
    return {
        "provider": prov,
        "type": s_type,
        "icon": ICON_PATHS.get(icon_key, ICON_PATHS["cube"]),
        "icon_name": icon_key,
        "brand_color": color,
        "service_name": s_name
    }
