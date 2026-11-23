"""
VizArc Cloud Service Catalog & Structurizr Themes Metadata Library.
Maps cloud services (AWS, GCP, Azure, Kubernetes, Generic) to:
- Official Structurizr Theme Tags & Icon URLs (from https://playground.structurizr.com/themes)
- Brand Colors & Category Types
- 24x24 Standalone SVG Vector Path Glyphs for offline rendering
"""

from typing import Dict, Any, List, Optional

# Official Structurizr Prebuilt Themes (Playground & Static CDN)
# https://playground.structurizr.com/themes
STRUCTURIZR_THEMES = {
    "aws": "https://static.structurizr.com/themes/amazon-web-services-2023.01.31/theme.json",
    "azure": "https://static.structurizr.com/themes/microsoft-azure-2023.01.24/theme.json",
    "gcp": "https://static.structurizr.com/themes/google-cloud-platform-v1.5/theme.json",
    "kubernetes": "https://static.structurizr.com/themes/kubernetes-v0.3/theme.json",
    "oci": "https://static.structurizr.com/themes/oracle-cloud-infrastructure-2023.04/theme.json",
}

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

# 24x24 SVG Path Glyphs (Offline Standalone Vector Fallbacks)
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

# Structurizr Themes Catalog (Mappings from Keywords -> Structurizr Theme Tags & Icons)
# Rule format:
# (keywords, provider, s_type, icon_key, color, canonical_name, structurizr_tag, structurizr_icon)
SERVICE_RULES = [
    # --- AWS (Theme: amazon-web-services-2023.01.31) ---
    (
        ["lambda", "serverless function"],
        "aws", "compute", "bolt", "#FF9900", "AWS Lambda",
        "Amazon Web Services - AWS Lambda",
        "https://static.structurizr.com/themes/amazon-web-services-2023.01.31/Arch_AWS-Lambda_48.png"
    ),
    (
        ["s3", "blob storage", "bucket", "object storage"],
        "aws", "storage", "storage", "#569A31", "Amazon S3",
        "Amazon Web Services - Amazon Simple Storage Service S3",
        "https://static.structurizr.com/themes/amazon-web-services-2023.01.31/Arch_Amazon-Simple-Storage-Service_48.png"
    ),
    (
        ["dynamodb", "dynamo"],
        "aws", "database", "database", "#4053D6", "Amazon DynamoDB",
        "Amazon Web Services - Amazon DynamoDB",
        "https://static.structurizr.com/themes/amazon-web-services-2023.01.31/Arch_Amazon-DynamoDB_48.png"
    ),
    (
        ["rds", "aurora", "postgres", "postgresql", "mysql"],
        "aws", "database", "database", "#527FFF", "Amazon RDS / PostgreSQL",
        "Amazon Web Services - Amazon Relational Database Service",
        "https://static.structurizr.com/themes/amazon-web-services-2023.01.31/Arch_Amazon-RDS_48.png"
    ),
    (
        ["elasticache", "redis", "memorystore"],
        "generic", "cache", "cache", "#DC382D", "Redis / ElastiCache",
        "Amazon Web Services - Amazon ElastiCache",
        "https://static.structurizr.com/themes/amazon-web-services-2023.01.31/Arch_Amazon-ElastiCache_48.png"
    ),
    (
        ["cloudfront", "cdn", "edge cache"],
        "aws", "cdn", "globe", "#8C4FFF", "CloudFront CDN",
        "Amazon Web Services - Amazon CloudFront",
        "https://static.structurizr.com/themes/amazon-web-services-2023.01.31/Arch_Amazon-CloudFront_48.png"
    ),
    (
        ["api gateway", "apigateway", "kong", "traefik"],
        "aws", "networking", "cloud", "#E7157B", "Amazon API Gateway",
        "Amazon Web Services - Amazon API Gateway",
        "https://static.structurizr.com/themes/amazon-web-services-2023.01.31/Arch_Amazon-API-Gateway_48.png"
    ),
    (
        ["sns", "notification service"],
        "aws", "messaging", "queue", "#FF4F8B", "Amazon SNS",
        "Amazon Web Services - Amazon Simple Notification Service SNS",
        "https://static.structurizr.com/themes/amazon-web-services-2023.01.31/Arch_Amazon-Simple-Notification-Service_48.png"
    ),
    (
        ["sqs", "rabbitmq", "queue", "message queue"],
        "aws", "queue", "queue", "#FF4F8B", "Amazon SQS",
        "Amazon Web Services - Amazon Simple Queue Service SQS",
        "https://static.structurizr.com/themes/amazon-web-services-2023.01.31/Arch_Amazon-Simple-Queue-Service_48.png"
    ),
    (
        ["eventbridge", "event bus", "pubsub", "pub/sub"],
        "aws", "messaging", "queue", "#FF4F8B", "Amazon EventBridge",
        "Amazon Web Services - Amazon EventBridge",
        "https://static.structurizr.com/themes/amazon-web-services-2023.01.31/Arch_Amazon-EventBridge_48.png"
    ),
    (
        ["kafka", "msk"],
        "generic", "messaging", "queue", "#231F20", "Apache Kafka (MSK)",
        "Amazon Web Services - Amazon Managed Streaming for Apache Kafka",
        "https://static.structurizr.com/themes/amazon-web-services-2023.01.31/Arch_Amazon-Managed-Streaming-for-Apache-Kafka_48.png"
    ),
    (
        ["ecs", "fargate", "container service"],
        "aws", "container", "cube", "#FF9900", "Amazon ECS / Fargate",
        "Amazon Web Services - Amazon Elastic Container Service",
        "https://static.structurizr.com/themes/amazon-web-services-2023.01.31/Arch_Amazon-Elastic-Container-Service_48.png"
    ),
    (
        ["ec2", "virtual machine", "vm", "monolith"],
        "aws", "compute", "server", "#FF9900", "Amazon EC2",
        "Amazon Web Services - Amazon Elastic Compute Cloud",
        "https://static.structurizr.com/themes/amazon-web-services-2023.01.31/Arch_Amazon-Elastic-Compute-Cloud_48.png"
    ),
    (
        ["cloudwatch", "datadog", "grafana", "prometheus", "monitoring"],
        "aws", "monitoring", "eye", "#64748B", "Amazon CloudWatch",
        "Amazon Web Services - Amazon CloudWatch",
        "https://static.structurizr.com/themes/amazon-web-services-2023.01.31/Arch_Amazon-CloudWatch_48.png"
    ),
    (
        ["bedrock", "sagemaker", "llm", "ai", "openai", "gemini", "claude"],
        "aws", "ai", "ai", "#A855F7", "Amazon SageMaker / Bedrock",
        "Amazon Web Services - Amazon SageMaker",
        "https://static.structurizr.com/themes/amazon-web-services-2023.01.31/Arch_Amazon-SageMaker_48.png"
    ),
    (
        ["kinesis", "streaming"],
        "aws", "analytics", "queue", "#8C4FFF", "Amazon Kinesis",
        "Amazon Web Services - Amazon Kinesis",
        "https://static.structurizr.com/themes/amazon-web-services-2023.01.31/Arch_Amazon-Kinesis_48.png"
    ),
    (
        ["opensearch", "elasticsearch", "vector db", "vectordb"],
        "aws", "database", "database", "#005276", "Amazon OpenSearch",
        "Amazon Web Services - Amazon OpenSearch Service",
        "https://static.structurizr.com/themes/amazon-web-services-2023.01.31/Arch_Amazon-OpenSearch-Service_48.png"
    ),
    (
        ["step functions", "orchestrator", "workflow"],
        "aws", "compute", "cube", "#FF9900", "AWS Step Functions",
        "Amazon Web Services - AWS Step Functions",
        "https://static.structurizr.com/themes/amazon-web-services-2023.01.31/Arch_AWS-Step-Functions_48.png"
    ),
    (
        ["iot", "iot core", "devices"],
        "aws", "networking", "cloud", "#E7157B", "AWS IoT Core",
        "Amazon Web Services - AWS IoT Core",
        "https://static.structurizr.com/themes/amazon-web-services-2023.01.31/Arch_AWS-IoT-Core_48.png"
    ),
    (
        ["glue", "etl"],
        "aws", "analytics", "cube", "#8C4FFF", "AWS Glue",
        "Amazon Web Services - AWS Glue",
        "https://static.structurizr.com/themes/amazon-web-services-2023.01.31/Arch_AWS-Glue_48.png"
    ),
    (
        ["redshift", "data warehouse"],
        "aws", "analytics", "database", "#8C4FFF", "Amazon Redshift",
        "Amazon Web Services - Amazon Redshift",
        "https://static.structurizr.com/themes/amazon-web-services-2023.01.31/Arch_Amazon-Redshift_48.png"
    ),

    # --- Microsoft Azure (Theme: microsoft-azure-2023.01.24) ---
    (
        ["azure function", "functions"],
        "azure", "compute", "bolt", "#0089D6", "Azure Functions",
        "Microsoft Azure - Azure Functions",
        "https://static.structurizr.com/themes/microsoft-azure-2023.01.24/Azure-Functions.png"
    ),
    (
        ["azure sql", "sql database"],
        "azure", "database", "database", "#0089D6", "Azure SQL Database",
        "Microsoft Azure - SQL Database",
        "https://static.structurizr.com/themes/microsoft-azure-2023.01.24/Azure-SQL-Database.png"
    ),
    (
        ["cosmos", "cosmosdb"],
        "azure", "database", "database", "#0089D6", "Azure Cosmos DB",
        "Microsoft Azure - Azure Cosmos DB",
        "https://static.structurizr.com/themes/microsoft-azure-2023.01.24/Azure-Cosmos-DB.png"
    ),
    (
        ["azure storage", "blob"],
        "azure", "storage", "storage", "#0089D6", "Azure Blob Storage",
        "Microsoft Azure - Storage Accounts",
        "https://static.structurizr.com/themes/microsoft-azure-2023.01.24/Azure-Storage-Accounts.png"
    ),
    (
        ["service bus"],
        "azure", "messaging", "queue", "#0089D6", "Azure Service Bus",
        "Microsoft Azure - Service Bus",
        "https://static.structurizr.com/themes/microsoft-azure-2023.01.24/Azure-Service-Bus.png"
    ),
    (
        ["aks"],
        "azure", "container", "cube", "#0089D6", "Azure Kubernetes Service",
        "Microsoft Azure - Azure Kubernetes Service",
        "https://static.structurizr.com/themes/microsoft-azure-2023.01.24/Azure-Kubernetes-Service.png"
    ),

    # --- Google Cloud Platform (Theme: google-cloud-platform-v1.5) ---
    (
        ["gke", "google kubernetes engine"],
        "gcp", "container", "cube", "#4285F4", "Google Kubernetes Engine (GKE)",
        "Google Cloud Platform - Google Kubernetes Engine",
        "https://static.structurizr.com/themes/google-cloud-platform-v1.5/google-kubernetes-engine.png"
    ),
    (
        ["cloud function", "google cloud function"],
        "gcp", "compute", "bolt", "#4285F4", "Google Cloud Functions",
        "Google Cloud Platform - Cloud Functions",
        "https://static.structurizr.com/themes/google-cloud-platform-v1.5/google-cloud-functions.png"
    ),
    (
        ["cloud sql", "bigquery"],
        "gcp", "database", "database", "#4285F4", "Google Cloud SQL / BigQuery",
        "Google Cloud Platform - Cloud SQL",
        "https://static.structurizr.com/themes/google-cloud-platform-v1.5/google-cloud-sql.png"
    ),
    (
        ["cloud storage", "gcs"],
        "gcp", "storage", "storage", "#4285F4", "Google Cloud Storage",
        "Google Cloud Platform - Cloud Storage",
        "https://static.structurizr.com/themes/google-cloud-platform-v1.5/google-cloud-storage.png"
    ),
    (
        ["pub/sub", "pubsub"],
        "gcp", "messaging", "queue", "#4285F4", "Google Cloud Pub/Sub",
        "Google Cloud Platform - PubSub",
        "https://static.structurizr.com/themes/google-cloud-platform-v1.5/google-pub-sub.png"
    ),

    # --- Kubernetes (Theme: kubernetes-v0.3) ---
    (
        ["k8s pod", "pod"],
        "kubernetes", "container", "cube", "#326CE5", "Kubernetes Pod",
        "Kubernetes - Pod",
        "https://static.structurizr.com/themes/kubernetes-v0.3/k8s-pod.png"
    ),
    (
        ["k8s service", "service"],
        "kubernetes", "container", "cube", "#326CE5", "Kubernetes Service",
        "Kubernetes - Service",
        "https://static.structurizr.com/themes/kubernetes-v0.3/k8s-svc.png"
    ),
    (
        ["ingress", "load balancer", "alb", "elb"],
        "kubernetes", "networking", "globe", "#326CE5", "Kubernetes Ingress / LB",
        "Kubernetes - Ingress",
        "https://static.structurizr.com/themes/kubernetes-v0.3/k8s-ing.png"
    ),
    (
        ["deployment"],
        "kubernetes", "container", "cube", "#326CE5", "Kubernetes Deployment",
        "Kubernetes - Deployment",
        "https://static.structurizr.com/themes/kubernetes-v0.3/k8s-deploy.png"
    ),
    (
        ["configmap", "config"],
        "kubernetes", "storage", "cube", "#326CE5", "Kubernetes ConfigMap",
        "Kubernetes - ConfigMap",
        "https://static.structurizr.com/themes/kubernetes-v0.3/k8s-cm.png"
    ),

    # --- Web & Frontend ---
    (
        ["next.js", "react", "vue", "frontend", "spa", "client", "web app", "vercel"],
        "generic", "frontend", "frontend", "#0EA5E9", "Web Application",
        "Web Browser",
        "https://static.structurizr.com/themes/amazon-web-services-2023.01.31/Arch_Amazon-CloudFront_48.png"
    ),
    (
        ["mobile", "ios", "android"],
        "generic", "frontend", "frontend", "#0EA5E9", "Mobile App",
        "Mobile App",
        "https://static.structurizr.com/themes/amazon-web-services-2023.01.31/Arch_Amazon-CloudFront_48.png"
    ),
]


def infer_service_metadata(label: str, tech: str = "", tier: str = "services") -> Dict[str, Any]:
    """
    Infers cloud provider, category, icon glyph, brand color, and
    Structurizr theme tags/icons (from https://playground.structurizr.com/themes).
    """
    search_text = f"{label} {tech} {tier}".lower()

    for item in SERVICE_RULES:
        keywords = item[0]
        provider = item[1]
        s_type = item[2]
        icon_key = item[3]
        color = item[4]
        canonical_name = item[5]
        structurizr_tag = item[6]
        structurizr_icon = item[7]

        if any(kw in search_text for kw in keywords):
            return {
                "provider": provider,
                "type": s_type,
                "icon": ICON_PATHS.get(icon_key, ICON_PATHS["cube"]),
                "icon_name": icon_key,
                "brand_color": color,
                "service_name": canonical_name,
                "structurizr_tag": structurizr_tag,
                "structurizr_icon": structurizr_icon,
                "structurizr_theme": STRUCTURIZR_THEMES.get(provider, STRUCTURIZR_THEMES["aws"])
            }

    # Fallback based on tier
    fallback_map = {
        "client": ("generic", "frontend", "frontend", "#0EA5E9", "Client / UI", "Web Browser"),
        "gateway": ("generic", "networking", "cloud", "#8B5CF6", "API Gateway", "Amazon Web Services - Amazon API Gateway"),
        "services": ("generic", "compute", "server", "#3B82F6", "Service Container", "Microservice"),
        "data": ("generic", "database", "database", "#10B981", "Database Storage", "Database")
    }

    prov, s_type, icon_key, color, s_name, s_tag = fallback_map.get(tier, ("generic", "compute", "cube", "#6366F1", "Component", "Microservice"))
    return {
        "provider": prov,
        "type": s_type,
        "icon": ICON_PATHS.get(icon_key, ICON_PATHS["cube"]),
        "icon_name": icon_key,
        "brand_color": color,
        "service_name": s_name,
        "structurizr_tag": s_tag,
        "structurizr_icon": "",
        "structurizr_theme": STRUCTURIZR_THEMES.get(prov, "")
    }
