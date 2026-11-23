"""
VizArc Architecture Template Library.
Includes 13 production-grade preset architecture templates (inspired by vizarch).
"""

from typing import Dict, Any, List, Optional

TEMPLATES: List[Dict[str, Any]] = [
    {
        "id": "serverless-aws",
        "name": "Serverless (AWS)",
        "description": "CloudFront → API Gateway → Lambda → DynamoDB + S3 + SNS",
        "text": "React frontend on CloudFront CDN, API Gateway, Lambda compute, DynamoDB database, S3 storage, SNS notifications, CloudWatch monitoring",
        "ir": {
            "title": "Serverless AWS Infrastructure",
            "summary": "Event-driven serverless architecture with CloudFront CDN, API Gateway, Lambda, and DynamoDB.",
            "tiers": [
                {"id": "client", "label": "Client Layer", "color": "#0EA5E9"},
                {"id": "gateway", "label": "Edge & API Gateway", "color": "#8C4FFF"},
                {"id": "services", "label": "Serverless Compute", "color": "#FF9900"},
                {"id": "data", "label": "Data & Events", "color": "#10B981"}
            ],
            "nodes": [
                {"id": "spa_app", "label": "React SPA", "tier": "client", "tech": "React / TypeScript", "description": "Client SPA hosted in S3 and accelerated via CloudFront."},
                {"id": "cloudfront", "label": "CloudFront CDN", "tier": "gateway", "tech": "Amazon CloudFront", "description": "Global edge caching and TLS termination."},
                {"id": "api_gw", "label": "API Gateway", "tier": "gateway", "tech": "Amazon API Gateway", "description": "REST API routing and request throttling."},
                {"id": "lambda_fn", "label": "Lambda Functions", "tier": "services", "tech": "AWS Lambda (Node.js/Python)", "description": "Serverless business logic execution."},
                {"id": "dynamodb", "label": "DynamoDB", "tier": "data", "tech": "Amazon DynamoDB", "description": "Single-digit millisecond NoSQL database."},
                {"id": "s3_bucket", "label": "S3 Storage", "tier": "data", "tech": "Amazon S3", "description": "Object storage for user uploads and assets."},
                {"id": "sns_topic", "label": "SNS Notifications", "tier": "data", "tech": "Amazon SNS", "description": "Pub/Sub message fan-out for notifications."}
            ],
            "edges": [
                {"from": "spa_app", "to": "cloudfront", "label": "HTTPS", "protocol": "https"},
                {"from": "cloudfront", "to": "api_gw", "label": "Forward API Requests", "protocol": "https"},
                {"from": "api_gw", "to": "lambda_fn", "label": "Invoke", "protocol": "https"},
                {"from": "lambda_fn", "to": "dynamodb", "label": "CRUD", "protocol": "sql"},
                {"from": "lambda_fn", "to": "s3_bucket", "label": "PutObject", "protocol": "https"},
                {"from": "lambda_fn", "to": "sns_topic", "label": "Publish Event", "protocol": "event"}
            ]
        }
    },
    {
        "id": "rag-system",
        "name": "RAG & AI Agent System",
        "description": "Chat UI → API Gateway → Orchestrator → Bedrock LLM + Vector DB + S3",
        "text": "Chat UI, API Gateway, Orchestrator Lambda, Bedrock LLM, SageMaker Embeddings, OpenSearch Vector DB, S3 Documents, DynamoDB Sessions",
        "ir": {
            "title": "Retrieval-Augmented Generation (RAG) Architecture",
            "summary": "Enterprise AI agent workflow with hybrid semantic search, document ingestion, and LLM inference.",
            "tiers": [
                {"id": "client", "label": "User Interface", "color": "#0EA5E9"},
                {"id": "gateway", "label": "API Layer", "color": "#8C4FFF"},
                {"id": "services", "label": "AI Agent Orchestration", "color": "#A855F7"},
                {"id": "data", "label": "Vector & Knowledge Store", "color": "#10B981"}
            ],
            "nodes": [
                {"id": "chat_ui", "label": "Chat Assistant UI", "tier": "client", "tech": "Next.js / Tailwind", "description": "Streaming conversational interface."},
                {"id": "api_gw", "label": "API Gateway", "tier": "gateway", "tech": "WebSocket / REST API", "description": "Manages streaming connections."},
                {"id": "agent_core", "label": "Agent Orchestrator", "tier": "services", "tech": "Python / LangChain / LangGraph", "description": "Coordinates tool calling, context retrieval, and prompt synthesis."},
                {"id": "bedrock_llm", "label": "Claude 3.5 / Bedrock", "tier": "services", "tech": "Foundation LLM", "description": "Performs reasoning and final response generation."},
                {"id": "vector_db", "label": "OpenSearch Vector DB", "tier": "data", "tech": "OpenSearch / k-NN", "description": "Dense vector index for semantic retrieval."},
                {"id": "doc_store", "label": "S3 Knowledge Base", "tier": "data", "tech": "Amazon S3", "description": "Raw PDFs, markdown docs, and parsed chunks."},
                {"id": "session_store", "label": "DynamoDB Memory", "tier": "data", "tech": "Amazon DynamoDB", "description": "Stores user chat history and session context."}
            ],
            "edges": [
                {"from": "chat_ui", "to": "api_gw", "label": "WebSocket Streaming", "protocol": "websocket"},
                {"from": "api_gw", "to": "agent_core", "label": "Invoke Agent", "protocol": "https"},
                {"from": "agent_core", "to": "session_store", "label": "Load History", "protocol": "sql"},
                {"from": "agent_core", "to": "vector_db", "label": "Vector Search", "protocol": "grpc"},
                {"from": "vector_db", "to": "doc_store", "label": "Fetch Source Chunks", "protocol": "https"},
                {"from": "agent_core", "to": "bedrock_llm", "label": "Inference with Context", "protocol": "https"}
            ]
        }
    },
    {
        "id": "microservices-gke",
        "name": "Microservices (GKE)",
        "description": "Cloud LB → GKE Cluster → Microservices → Cloud SQL + Pub/Sub",
        "text": "Web App on GCP Load Balancer, GKE cluster with Auth, Orders, and Payments services, Cloud SQL Postgres, Pub/Sub, Memorystore Redis",
        "ir": {
            "title": "Google Cloud GKE Microservices",
            "summary": "Containerized microservice architecture on Kubernetes with managed Google Cloud databases.",
            "tiers": [
                {"id": "client", "label": "Clients", "color": "#0EA5E9"},
                {"id": "gateway", "label": "Ingress & LB", "color": "#4285F4"},
                {"id": "services", "label": "GKE Microservices", "color": "#326CE5"},
                {"id": "data", "label": "Google Cloud Data", "color": "#10B981"}
            ],
            "nodes": [
                {"id": "web_client", "label": "Web Client", "tier": "client", "tech": "Next.js", "description": "Web app consumer."},
                {"id": "gcp_lb", "label": "Cloud Load Balancing", "tier": "gateway", "tech": "GCP External HTTP(S) LB", "description": "Global traffic distribution."},
                {"id": "auth_svc", "label": "Auth Service", "tier": "services", "tech": "Go / GKE Pod", "description": "Handles authentication."},
                {"id": "order_svc", "label": "Orders Service", "tier": "services", "tech": "FastAPI / GKE Pod", "description": "Manages order lifecycle."},
                {"id": "payment_svc", "label": "Payments Service", "tier": "services", "tech": "Node.js / GKE Pod", "description": "Processes payments."},
                {"id": "cloud_sql", "label": "Cloud SQL Postgres", "tier": "data", "tech": "Managed PostgreSQL", "description": "Relational transactional database."},
                {"id": "pubsub", "label": "Cloud Pub/Sub", "tier": "data", "tech": "Google Pub/Sub", "description": "Asynchronous messaging backbone."},
                {"id": "memorystore", "label": "Memorystore Redis", "tier": "data", "tech": "In-Memory Redis", "description": "Low-latency cache."}
            ],
            "edges": [
                {"from": "web_client", "to": "gcp_lb", "label": "HTTPS", "protocol": "https"},
                {"from": "gcp_lb", "to": "auth_svc", "label": "Route /auth", "protocol": "grpc"},
                {"from": "gcp_lb", "to": "order_svc", "label": "Route /orders", "protocol": "grpc"},
                {"from": "auth_svc", "to": "memorystore", "label": "Session Cache", "protocol": "redis"},
                {"from": "order_svc", "to": "cloud_sql", "label": "Store Order", "protocol": "sql"},
                {"from": "order_svc", "to": "pubsub", "label": "Publish 'OrderCreated'", "protocol": "event"},
                {"from": "pubsub", "to": "payment_svc", "label": "Consume Event", "protocol": "event"}
            ]
        }
    },
    {
        "id": "fullstack-nextjs",
        "name": "Fullstack (Next.js)",
        "description": "Vercel Frontend → Next.js API Routes → PostgreSQL + Redis + Stripe",
        "text": "Vercel Hosting, Next.js Frontend, Next.js API Routes, PostgreSQL, Redis Cache, Stripe, GitHub Actions, Sentry",
        "ir": {
            "title": "Modern Fullstack Architecture",
            "summary": "Next.js App Router fullstack platform with serverless edge functions and third-party SaaS integrations.",
            "tiers": [
                {"id": "client", "label": "Edge & Client", "color": "#0EA5E9"},
                {"id": "gateway", "label": "Vercel Platform", "color": "#000000"},
                {"id": "services", "label": "Backend Functions", "color": "#6366F1"},
                {"id": "data", "label": "Databases & External", "color": "#10B981"}
            ],
            "nodes": [
                {"id": "browser", "label": "User Browser", "tier": "client", "tech": "Modern Browser", "description": "Interacts with SSR/CSR web app."},
                {"id": "vercel_edge", "label": "Vercel Edge Network", "tier": "gateway", "tech": "Vercel CDN", "description": "Edge caching and routing."},
                {"id": "next_app", "label": "Next.js App Router", "tier": "services", "tech": "React Server Components", "description": "Server-side rendering."},
                {"id": "api_routes", "label": "Route Handlers", "tier": "services", "tech": "Serverless Node.js", "description": "API endpoints and webhooks."},
                {"id": "postgres", "label": "Neon / Supabase Postgres", "tier": "data", "tech": "PostgreSQL via Prisma", "description": "Primary transactional database."},
                {"id": "upstash_redis", "label": "Upstash Redis", "tier": "data", "tech": "Serverless Redis", "description": "Rate limiting and KV cache."},
                {"id": "stripe", "label": "Stripe Payments", "tier": "data", "tech": "Stripe API", "description": "Subscription billing."}
            ],
            "edges": [
                {"from": "browser", "to": "vercel_edge", "label": "HTTPS Request", "protocol": "https"},
                {"from": "vercel_edge", "to": "next_app", "label": "SSR Page", "protocol": "https"},
                {"from": "vercel_edge", "to": "api_routes", "label": "/api/* calls", "protocol": "https"},
                {"from": "api_routes", "to": "postgres", "label": "Prisma ORM", "protocol": "sql"},
                {"from": "api_routes", "to": "upstash_redis", "label": "Rate Limit", "protocol": "redis"},
                {"from": "api_routes", "to": "stripe", "label": "Create Checkout", "protocol": "https"}
            ]
        }
    },
    {
        "id": "event-streaming-kafka",
        "name": "Event Streaming (Kafka)",
        "description": "Producer API → Kafka Cluster → Analytics + Notifications + Audit Consumers",
        "text": "Producer API, Kafka Cluster, Analytics Consumer, Notifications Consumer, Audit Consumer, Elasticsearch, PostgreSQL, Grafana, Prometheus",
        "ir": {
            "title": "Real-Time Event Streaming Architecture",
            "summary": "High-throughput event streaming architecture using Apache Kafka for real-time stream processing.",
            "tiers": [
                {"id": "client", "label": "Ingress API", "color": "#0EA5E9"},
                {"id": "gateway", "label": "Message Backbone", "color": "#231F20"},
                {"id": "services", "label": "Consumer Services", "color": "#10B981"},
                {"id": "data", "label": "Sinks & Analytics", "color": "#F59E0B"}
            ],
            "nodes": [
                {"id": "producer_api", "label": "Event Producer API", "tier": "client", "tech": "Go / FastAPI", "description": "Ingests telemetry and user actions."},
                {"id": "kafka_cluster", "label": "Kafka Event Broker", "tier": "gateway", "tech": "Apache Kafka (3 Brokers)", "description": "Distributed log topic partitioner."},
                {"id": "analytics_worker", "label": "Analytics Worker", "tier": "services", "tech": "Apache Flink / Python", "description": "Real-time rolling aggregations."},
                {"id": "notify_worker", "label": "Notification Worker", "tier": "services", "tech": "Node.js Consumer", "description": "Dispatches push alerts."},
                {"id": "audit_worker", "label": "Audit Consumer", "tier": "services", "tech": "Rust Consumer", "description": "Immutable compliance logger."},
                {"id": "elasticsearch", "label": "Elasticsearch", "tier": "data", "tech": "Elastic 8", "description": "Log search and analytics."},
                {"id": "postgres", "label": "PostgreSQL", "tier": "data", "tech": "PostgreSQL 16", "description": "Aggregated stats store."}
            ],
            "edges": [
                {"from": "producer_api", "to": "kafka_cluster", "label": "Produce Events", "protocol": "kafka"},
                {"from": "kafka_cluster", "to": "analytics_worker", "label": "Consume Stream", "protocol": "kafka"},
                {"from": "kafka_cluster", "to": "notify_worker", "label": "Consume Alerts", "protocol": "kafka"},
                {"from": "kafka_cluster", "to": "audit_worker", "label": "Consume Audit", "protocol": "kafka"},
                {"from": "analytics_worker", "to": "postgres", "label": "Write Metrics", "protocol": "sql"},
                {"from": "audit_worker", "to": "elasticsearch", "label": "Index Logs", "protocol": "https"}
            ]
        }
    },
    {
        "id": "monolith-aws",
        "name": "Monolith (AWS)",
        "description": "CloudFront → ALB → EC2 Monolith → RDS + ElastiCache + S3",
        "text": "React Frontend, CloudFront, ALB, EC2 Monolith, RDS Postgres, ElastiCache Redis, S3, CloudWatch",
        "ir": {
            "title": "Classic AWS Modular Monolith",
            "summary": "Proven multi-tier web application architecture with load-balanced EC2 instances.",
            "tiers": [
                {"id": "client", "label": "Client Layer", "color": "#0EA5E9"},
                {"id": "gateway", "label": "Load Balancer", "color": "#8C4FFF"},
                {"id": "services", "label": "Application Tier", "color": "#FF9900"},
                {"id": "data", "label": "Database & Assets", "color": "#10B981"}
            ],
            "nodes": [
                {"id": "browser", "label": "Web Browser", "tier": "client", "tech": "Client", "description": "End-user web traffic."},
                {"id": "alb", "label": "Application Load Balancer", "tier": "gateway", "tech": "AWS ALB", "description": "Distributes traffic across EC2 autoscaling group."},
                {"id": "ec2_app", "label": "EC2 Monolith (Django / Rails)", "tier": "services", "tech": "Python / Ruby on Rails", "description": "Handles web traffic, templates, and background tasks."},
                {"id": "rds_postgres", "label": "Amazon RDS Postgres", "tier": "data", "tech": "PostgreSQL (Multi-AZ)", "description": "Primary transactional storage with read replica."},
                {"id": "elasticache", "label": "ElastiCache Redis", "tier": "data", "tech": "Redis 7", "description": "Session cache and background job queues."},
                {"id": "s3_assets", "label": "S3 Static Assets", "tier": "data", "tech": "Amazon S3", "description": "User uploaded images and files."}
            ],
            "edges": [
                {"from": "browser", "to": "alb", "label": "HTTPS", "protocol": "https"},
                {"from": "alb", "to": "ec2_app", "label": "Forward Port 8000", "protocol": "http"},
                {"from": "ec2_app", "to": "rds_postgres", "label": "ORM Queries", "protocol": "sql"},
                {"from": "ec2_app", "to": "elasticache", "label": "Cache Lookups", "protocol": "redis"},
                {"from": "ec2_app", "to": "s3_assets", "label": "Upload Media", "protocol": "https"}
            ]
        }
    },
    {
        "id": "k8s-platform",
        "name": "K8s Platform",
        "description": "Ingress → Web & API Services → Deployments → PVC + ConfigMaps",
        "text": "Kubernetes Ingress, Web Service, API Service, Web Deployment, API Deployment, Worker Deployment, PVC, Secrets, ConfigMap, Prometheus",
        "ir": {
            "title": "Cloud-Native Kubernetes Platform",
            "summary": "Standard Kubernetes cluster architecture with Ingress controllers, deployments, and persistent volumes.",
            "tiers": [
                {"id": "client", "label": "Ingress Controller", "color": "#326CE5"},
                {"id": "gateway", "label": "K8s Services (ClusterIP)", "color": "#2563EB"},
                {"id": "services", "label": "K8s Deployments & Pods", "color": "#10B981"},
                {"id": "data", "label": "Storage & Config", "color": "#F59E0B"}
            ],
            "nodes": [
                {"id": "k8s_ingress", "label": "Nginx Ingress", "tier": "client", "tech": "Ingress Controller", "description": "SSL termination and host-based routing."},
                {"id": "web_svc", "label": "Web Service", "tier": "gateway", "tech": "ClusterIP:80", "description": "Internal DNS service abstraction."},
                {"id": "api_svc", "label": "API Service", "tier": "gateway", "tech": "ClusterIP:8080", "description": "API service abstraction."},
                {"id": "web_deploy", "label": "Web Pods (3 Replicas)", "tier": "services", "tech": "Next.js Container", "description": "Frontend pod deployment."},
                {"id": "api_deploy", "label": "API Pods (5 Replicas)", "tier": "services", "tech": "Go Container", "description": "Stateless backend pods."},
                {"id": "pvc_data", "label": "PersistentVolumeClaim", "tier": "data", "tech": "EBS / Ceph Storage", "description": "Persistent disk mount."},
                {"id": "k8s_secrets", "label": "Secrets & ConfigMaps", "tier": "data", "tech": "K8s Secrets", "description": "Mounted environment credentials."}
            ],
            "edges": [
                {"from": "k8s_ingress", "to": "web_svc", "label": "Route /", "protocol": "http"},
                {"from": "k8s_ingress", "to": "api_svc", "label": "Route /api", "protocol": "http"},
                {"from": "web_svc", "to": "web_deploy", "label": "Load Balance", "protocol": "tcp"},
                {"from": "api_svc", "to": "api_deploy", "label": "Load Balance", "protocol": "tcp"},
                {"from": "api_deploy", "to": "pvc_data", "label": "Mount Disk", "protocol": "tcp"},
                {"from": "api_deploy", "to": "k8s_secrets", "label": "Read Env", "protocol": "tcp"}
            ]
        }
    },
    {
        "id": "event-driven-aws",
        "name": "Event-Driven (AWS)",
        "description": "API Gateway → Lambda → EventBridge → SQS → Worker Lambda → DynamoDB",
        "text": "React App, API Gateway, Order Lambda, EventBridge, SQS Queue, Worker Lambda, DynamoDB, S3 Audit, SES Email, CloudWatch",
        "ir": {
            "title": "AWS EventBridge & SQS Decoupled Architecture",
            "summary": "Asynchronous event-driven pipeline using Amazon EventBridge for event routing and SQS for resilient buffering.",
            "tiers": [
                {"id": "client", "label": "Ingress", "color": "#0EA5E9"},
                {"id": "gateway", "label": "Event Routing", "color": "#FF4F8B"},
                {"id": "services", "label": "Processing Workers", "color": "#FF9900"},
                {"id": "data", "label": "State & Notifications", "color": "#10B981"}
            ],
            "nodes": [
                {"id": "api_gw", "label": "API Gateway", "tier": "client", "tech": "Amazon API Gateway", "description": "Public entry point for orders."},
                {"id": "order_lambda", "label": "Order Handler Lambda", "tier": "client", "tech": "AWS Lambda", "description": "Validates request and publishes event."},
                {"id": "eventbridge", "label": "Amazon EventBridge", "tier": "gateway", "tech": "Serverless Event Bus", "description": "Matches rules and routes events to targets."},
                {"id": "order_queue", "label": "SQS Order Queue", "tier": "gateway", "tech": "Amazon SQS FIFO", "description": "Buffers order processing with DLQ."},
                {"id": "worker_lambda", "label": "Fulfillment Lambda", "tier": "services", "tech": "AWS Lambda", "description": "Consumes batches and triggers shipping."},
                {"id": "dynamodb", "label": "DynamoDB Table", "tier": "data", "tech": "Amazon DynamoDB", "description": "Stores state updates."},
                {"id": "ses", "label": "Amazon SES", "tier": "data", "tech": "Simple Email Service", "description": "Sends customer confirmation emails."}
            ],
            "edges": [
                {"from": "api_gw", "to": "order_lambda", "label": "POST /order", "protocol": "https"},
                {"from": "order_lambda", "to": "eventbridge", "label": "PutEvents", "protocol": "event"},
                {"from": "eventbridge", "to": "order_queue", "label": "Rule Match", "protocol": "event"},
                {"from": "order_queue", "to": "worker_lambda", "label": "Batch Trigger", "protocol": "event"},
                {"from": "worker_lambda", "to": "dynamodb", "label": "Update Status", "protocol": "sql"},
                {"from": "worker_lambda", "to": "ses", "label": "Send Email", "protocol": "https"}
            ]
        }
    },
    {
        "id": "data-lakehouse",
        "name": "Data Lakehouse",
        "description": "Kinesis Stream → Lambda Ingest → S3 Data Lake → Glue ETL → Redshift + Athena",
        "text": "Kinesis Stream, Ingest Lambda, S3 Data Lake, Glue ETL, Redshift Warehouse, Athena Query, QuickSight BI, CloudWatch",
        "ir": {
            "title": "AWS Modern Data Lakehouse",
            "summary": "Streaming ingestion and analytical data platform with Apache Iceberg/Parquet on S3.",
            "tiers": [
                {"id": "client", "label": "Ingestion", "color": "#FF9900"},
                {"id": "gateway", "label": "Raw Lake & ETL", "color": "#569A31"},
                {"id": "services", "label": "Analytical Query", "color": "#4053D6"},
                {"id": "data", "label": "BI & Dashboards", "color": "#0EA5E9"}
            ],
            "nodes": [
                {"id": "kinesis", "label": "Kinesis Data Stream", "tier": "client", "tech": "Amazon Kinesis", "description": "Real-time streaming event ingestion."},
                {"id": "ingest_lambda", "label": "Ingest Lambda", "tier": "client", "tech": "AWS Lambda", "description": "Micro-batching and schema validation."},
                {"id": "s3_lake", "label": "S3 Data Lake (Bronze/Silver)", "tier": "gateway", "tech": "Amazon S3 (Parquet)", "description": "Immutable raw and curated object storage."},
                {"id": "glue_etl", "label": "AWS Glue ETL", "tier": "gateway", "tech": "Apache Spark Serverless", "description": "Data cataloging and transformation."},
                {"id": "redshift", "label": "Amazon Redshift", "tier": "services", "tech": "Redshift Serverless", "description": "High-performance columnar data warehouse."},
                {"id": "athena", "label": "Amazon Athena", "tier": "services", "tech": "Presto / Trino", "description": "Ad-hoc SQL querying on S3."},
                {"id": "quicksight", "label": "QuickSight BI", "tier": "data", "tech": "Amazon QuickSight", "description": "Executive reporting dashboards."}
            ],
            "edges": [
                {"from": "kinesis", "to": "ingest_lambda", "label": "Stream Record", "protocol": "event"},
                {"from": "ingest_lambda", "to": "s3_lake", "label": "Parquet Write", "protocol": "https"},
                {"from": "glue_etl", "to": "s3_lake", "label": "Crawl & Transform", "protocol": "https"},
                {"from": "glue_etl", "to": "redshift", "label": "Load Gold Tier", "protocol": "sql"},
                {"from": "athena", "to": "s3_lake", "label": "Query Lake", "protocol": "sql"},
                {"from": "quicksight", "to": "redshift", "label": "SQL Queries", "protocol": "sql"}
            ]
        }
    },
    {
        "id": "ml-pipeline",
        "name": "ML Training & Inference",
        "description": "S3 Training Data → Step Functions → SageMaker Job → Model Registry → Inference API",
        "text": "S3 Training Data, ECR Container, Step Functions, SageMaker Training, Model Registry, Inference Endpoint, API Gateway, CloudWatch",
        "ir": {
            "title": "End-to-End MLOps Pipeline",
            "summary": "Automated machine learning training, evaluation, model registration, and real-time inference.",
            "tiers": [
                {"id": "client", "label": "Data & Triggers", "color": "#0EA5E9"},
                {"id": "gateway", "label": "ML Workflow", "color": "#FF9900"},
                {"id": "services", "label": "Model Registry & Training", "color": "#A855F7"},
                {"id": "data", "label": "Serving & Monitoring", "color": "#10B981"}
            ],
            "nodes": [
                {"id": "s3_data", "label": "S3 Training Dataset", "tier": "client", "tech": "Amazon S3", "description": "Annotated training features."},
                {"id": "step_fn", "label": "AWS Step Functions", "tier": "gateway", "tech": "ML Pipeline State Machine", "description": "Orchestrates preprocessing and training."},
                {"id": "sm_train", "label": "SageMaker Training Job", "tier": "services", "tech": "GPU EC2 (PyTorch)", "description": "Distributed model training."},
                {"id": "sm_registry", "label": "SageMaker Model Registry", "tier": "services", "tech": "Model Governance", "description": "Versioned model artifacts with approval gates."},
                {"id": "sm_endpoint", "label": "SageMaker Real-Time Endpoint", "tier": "data", "tech": "Autoscaling Serving Pods", "description": "Sub-20ms inference latency."},
                {"id": "api_gw", "label": "API Gateway", "tier": "data", "tech": "Amazon API Gateway", "description": "Client inference API."}
            ],
            "edges": [
                {"from": "s3_data", "to": "step_fn", "label": "Trigger on S3 Upload", "protocol": "event"},
                {"from": "step_fn", "to": "sm_train", "label": "Launch Training", "protocol": "https"},
                {"from": "sm_train", "to": "sm_registry", "label": "Register Model", "protocol": "https"},
                {"from": "sm_registry", "to": "sm_endpoint", "label": "Deploy Validated Model", "protocol": "https"},
                {"from": "api_gw", "to": "sm_endpoint", "label": "Predict Request", "protocol": "https"}
            ]
        }
    },
    {
        "id": "ecommerce-platform",
        "name": "E-Commerce Platform",
        "description": "CloudFront → ALB → Product/Cart/Order Microservices → PostgreSQL + Redis + Stripe",
        "text": "Storefront, CloudFront, Load Balancer, Product Service, Cart Service, Order Service, PostgreSQL, Redis Cache, Elasticsearch, Stripe Payments, S3 Assets, CloudWatch",
        "ir": {
            "title": "High-Volume E-Commerce Platform",
            "summary": "Scalable retail architecture with decoupled cart, checkout, payment, and inventory services designed for global flash sales.",
            "archetype": "architecture",
            "decisions": [
                {
                    "decision": "Decoupled Microservice Domain Boundaries",
                    "rationale": "Separates high-frequency read catalog operations from write-heavy shopping cart and payment checkout flows, ensuring isolated autoscaling.",
                    "tradeoff": "Requires distributed tracing and eventual consistency handling across services.",
                    "status": "Accepted"
                },
                {
                    "decision": "In-Memory Session Caching with Redis",
                    "rationale": "Buffers active shopping carts and user sessions with sub-millisecond read/write latency, reducing database query overhead by 90%.",
                    "tradeoff": "Requires cart serialization and scheduled persistent backup to avoid session loss.",
                    "status": "Accepted"
                },
                {
                    "decision": "PCI-DSS Compliant Stripe Offloading",
                    "rationale": "Delegates card tokenization and sensitive fraud detection directly to Stripe, reducing regulatory compliance surface area.",
                    "tradeoff": "Introduces third-party dependency on Stripe API availability and webhook delivery.",
                    "status": "Accepted"
                }
            ],
            "flow_steps": [
                {
                    "step": 1,
                    "title": "Storefront Ingress & TLS Termination",
                    "from": "storefront",
                    "to": "cloudfront",
                    "protocol": "HTTPS",
                    "description": "User requests route to the nearest CloudFront Edge PoP for SSL handshake termination and static asset caching."
                },
                {
                    "step": 2,
                    "title": "Catalog Discovery & Search",
                    "from": "cloudfront",
                    "to": "product_svc",
                    "protocol": "HTTPS",
                    "description": "Catalog queries dispatched to Go Product Catalog Service with sub-10ms Elasticsearch faceted filtering."
                },
                {
                    "step": 3,
                    "title": "In-Memory Cart Mutation",
                    "from": "cloudfront",
                    "to": "cart_svc",
                    "protocol": "HTTPS",
                    "description": "Item additions and quantities updated immediately in low-latency Redis-backed session store."
                },
                {
                    "step": 4,
                    "title": "Checkout Submission & Validation",
                    "from": "cloudfront",
                    "to": "order_svc",
                    "protocol": "HTTPS",
                    "description": "Cart finalized; checkout request routed to Order Service to reserve stock and validate inventory."
                },
                {
                    "step": 5,
                    "title": "Payment Token Authorization",
                    "from": "order_svc",
                    "to": "stripe",
                    "protocol": "HTTPS",
                    "description": "Secure API exchange authorizes customer payment method via Stripe REST API."
                },
                {
                    "step": 6,
                    "title": "Transactional ACID Commit",
                    "from": "order_svc",
                    "to": "postgres",
                    "protocol": "SQL",
                    "description": "Order records, line items, and invoice state atomically persisted in Aurora PostgreSQL cluster."
                }
            ],
            "tiers": [
                {"id": "client", "label": "Storefront", "color": "#0EA5E9"},
                {"id": "gateway", "label": "Routing & CDN", "color": "#8C4FFF"},
                {"id": "services", "label": "Retail Services", "color": "#FF9900"},
                {"id": "data", "label": "Persistence & External", "color": "#10B981"}
            ],
            "nodes": [
                {"id": "storefront", "label": "Web & Mobile Store", "tier": "client", "tech": "Next.js / React", "description": "Customer catalog browsing and checkout."},
                {"id": "cloudfront", "label": "CloudFront & WAF", "tier": "gateway", "tech": "AWS Edge Security", "description": "DDoS protection and static caching."},
                {"id": "product_svc", "label": "Product Catalog Service", "tier": "services", "tech": "Go / Elasticsearch", "description": "High-speed faceted product search."},
                {"id": "cart_svc", "label": "Shopping Cart Service", "tier": "services", "tech": "Node.js / Redis", "description": "In-memory shopping cart sessions."},
                {"id": "order_svc", "label": "Order & Checkout Service", "tier": "services", "tech": "FastAPI / Python", "description": "Manages payments and order creation."},
                {"id": "postgres", "label": "PostgreSQL Cluster", "tier": "data", "tech": "Aurora PostgreSQL", "description": "Transactional order records."},
                {"id": "stripe", "label": "Stripe Payments API", "tier": "data", "tech": "Stripe REST API", "description": "Credit card processing and fraud detection."}
            ],
            "edges": [
                {"from": "storefront", "to": "cloudfront", "label": "HTTPS", "protocol": "https"},
                {"from": "cloudfront", "to": "product_svc", "label": "GET /products", "protocol": "https"},
                {"from": "cloudfront", "to": "cart_svc", "label": "PUT /cart", "protocol": "https"},
                {"from": "cloudfront", "to": "order_svc", "label": "POST /checkout", "protocol": "https"},
                {"from": "order_svc", "to": "postgres", "label": "Insert Order", "protocol": "sql"},
                {"from": "order_svc", "to": "stripe", "label": "Charge Card", "protocol": "https"}
            ]
        }
    },
    {
        "id": "iot-platform",
        "name": "IoT Platform",
        "description": "IoT Devices → AWS IoT Core → Kinesis → Lambda → DynamoDB + S3 + SNS Alerts",
        "text": "IoT Devices, AWS IoT Core, Kinesis Stream, Processor Lambda, DynamoDB State, S3 Raw Data, SNS Alerts, Elasticsearch, Grafana",
        "ir": {
            "title": "Industrial IoT Telemetry Platform",
            "summary": "MQTT-based IoT ingestion processing millions of device sensor readings per second.",
            "tiers": [
                {"id": "client", "label": "Sensors & Edge", "color": "#06B6D4"},
                {"id": "gateway", "label": "MQTT Broker", "color": "#FF9900"},
                {"id": "services", "label": "Stream Processing", "color": "#10B981"},
                {"id": "data", "label": "Time Series & Storage", "color": "#F59E0B"}
            ],
            "nodes": [
                {"id": "iot_devices", "label": "Edge IoT Sensors", "tier": "client", "tech": "Embedded C / FreeRTOS", "description": "Temperature and pressure telemetry."},
                {"id": "iot_core", "label": "AWS IoT Core", "tier": "gateway", "tech": "MQTT / TLS Gateway", "description": "Device shadow and mutual TLS authentication."},
                {"id": "kinesis_stream", "label": "Kinesis Telemetry Stream", "tier": "services", "tech": "Amazon Kinesis", "description": "High-throughput ordered sensor buffer."},
                {"id": "proc_lambda", "label": "Anomaly Detection Lambda", "tier": "services", "tech": "AWS Lambda (Rust)", "description": "Real-time threshold and anomaly checks."},
                {"id": "dynamodb", "label": "DynamoDB Device State", "tier": "data", "tech": "Amazon DynamoDB", "description": "Latest device status shadow."},
                {"id": "sns_alerts", "label": "SNS Emergency Alerts", "tier": "data", "tech": "Amazon SNS", "description": "PagerDuty and SMS notifications for anomalies."}
            ],
            "edges": [
                {"from": "iot_devices", "to": "iot_core", "label": "MQTT over TLS", "protocol": "tcp"},
                {"from": "iot_core", "to": "kinesis_stream", "label": "Rule Action", "protocol": "event"},
                {"from": "kinesis_stream", "to": "proc_lambda", "label": "Process Batch", "protocol": "event"},
                {"from": "proc_lambda", "to": "dynamodb", "label": "Update Shadow", "protocol": "sql"},
                {"from": "proc_lambda", "to": "sns_alerts", "label": "Alert on Anomaly", "protocol": "event"}
            ]
        }
    },
    {
        "id": "web3-blockchain",
        "name": "Web3 & Blockchain dApp",
        "description": "dApp Frontend → Cloudflare CDN → RPC Node → Smart Contract + Graph Indexer",
        "text": "dApp Frontend, Cloudflare CDN, IPFS Gateway, Smart Contract, RPC Node, Graph Indexer, Redis Cache, Event Log Postgres, Metamask",
        "ir": {
            "title": "Decentralized Web3 Application (dApp)",
            "summary": "Hybrid Web3 architecture combining decentralized smart contracts with indexers and caching.",
            "tiers": [
                {"id": "client", "label": "Wallet & Frontend", "color": "#F59E0B"},
                {"id": "gateway", "label": "Web3 RPC Gateway", "color": "#8B5CF6"},
                {"id": "services", "label": "Smart Contract & Chain", "color": "#3B82F6"},
                {"id": "data", "label": "Indexers & Event Logs", "color": "#10B981"}
            ],
            "nodes": [
                {"id": "dapp_ui", "label": "dApp Web Frontend", "tier": "client", "tech": "Ethers.js / Wagmi / React", "description": "User interface connecting to web3 wallet."},
                {"id": "wallet", "label": "Browser Wallet (MetaMask)", "tier": "client", "tech": "ECDSA Key Signer", "description": "Signs blockchain transactions."},
                {"id": "rpc_node", "label": "JSON-RPC Node (Alchemy/Infura)", "tier": "gateway", "tech": "EVM RPC Endpoint", "description": "Gateway to Ethereum / Polygon network."},
                {"id": "smart_contract", "label": "EVM Smart Contract", "tier": "services", "tech": "Solidity (EVM)", "description": "On-chain state execution and token logic."},
                {"id": "graph_indexer", "label": "The Graph Subgraph", "tier": "data", "tech": "The Graph Protocol", "description": "Indexes on-chain events into a GraphQL schema."},
                {"id": "postgres_cache", "label": "Off-chain Cache & Analytics", "tier": "data", "tech": "PostgreSQL 16", "description": "Fast read cache for historical transactions."}
            ],
            "edges": [
                {"from": "dapp_ui", "to": "wallet", "label": "Request Signature", "protocol": "direct"},
                {"from": "wallet", "to": "rpc_node", "label": "eth_sendRawTransaction", "protocol": "https"},
                {"from": "rpc_node", "to": "smart_contract", "label": "EVM Execution", "protocol": "tcp"},
                {"from": "smart_contract", "to": "graph_indexer", "label": "Emit Event Log", "protocol": "event"},
                {"from": "graph_indexer", "to": "postgres_cache", "label": "Sync Blocks", "protocol": "sql"},
                {"from": "dapp_ui", "to": "graph_indexer", "label": "Query GraphQL", "protocol": "https"}
            ]
        }
    }
]

def get_template(template_id: str) -> Optional[Dict[str, Any]]:
    """Fetches template by ID or returns None."""
    for t in TEMPLATES:
        if t["id"] == template_id:
            return t
    return None

def list_templates() -> List[Dict[str, str]]:
    """Returns list of template summaries."""
    return [{"id": t["id"], "name": t["name"], "description": t["description"]} for t in TEMPLATES]
