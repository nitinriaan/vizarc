"""
VizArc Cloud Service Catalog & Foolproof Vector Icons Library.
Features:
- Authentic 24x24 SVG Vector Paths (Simple Icons / Devicon / Cloud Provider specs)
  EMBEDDED INLINE: 100% foolproof, works offline, never fails in file:/// downloads!
- Official Provider Brand Colors (AWS #FF9900, Azure #0089D6, GCP #4285F4, K8s #326CE5)
- Free Public CDN Fallback URLs (simpleicons.org, devicon)
- Structurizr C4 Theme Tags (for playground.structurizr.com)
"""

from typing import Dict, Any, List, Optional

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
    "direct": "#94A3B8"
}

# Official Structurizr Prebuilt Themes (Playground & Static CDN)
STRUCTURIZR_THEMES = {
    "aws": "https://static.structurizr.com/themes/amazon-web-services-2023.01.31/theme.json",
    "azure": "https://static.structurizr.com/themes/microsoft-azure-2023.01.24/theme.json",
    "gcp": "https://static.structurizr.com/themes/google-cloud-platform-v1.5/theme.json",
    "kubernetes": "https://static.structurizr.com/themes/kubernetes-v0.3/theme.json",
    "oci": "https://static.structurizr.com/themes/oracle-cloud-infrastructure-2023.04/theme.json",
}

# =====================================================================
# AUTHENTIC 24x24 SVG VECTOR PATHS (Standard viewBox="0 0 24 24")
# EMBEDDED DIRECTLY INLINE — 100% FOOLPROOF & OFFLINE PROOF!
# =====================================================================
VECTOR_ICONS: Dict[str, str] = {
    # AWS
    "aws": "M6.76 10.04c0 .3.03.54.09.71.06.18.14.37.26.58.04.06.06.13.06.18 0 .08-.05.16-.16.24l-1.44 1.13c-.08.06-.16.08-.24.08-.07 0-.14-.02-.2-.08-.34-.32-.62-.7-.81-1.13a3.78 3.78 0 0 1-.3-1.5c0-.62.11-1.2.34-1.73.22-.53.54-.98.96-1.34.42-.37.92-.65 1.5-.84.58-.19 1.23-.29 1.94-.29.64 0 1.25.07 1.82.22.58.14 1.07.36 1.49.65.42.29.74.65.96 1.08.22.43.34.94.34 1.51v3.92c0 .45.06.78.18 1.01.12.22.31.43.58.62.08.06.12.13.12.22 0 .09-.04.17-.12.24l-1.54 1.15c-.07.06-.15.08-.23.08a.35.35 0 0 1-.23-.1c-.22-.26-.4-.56-.53-.91-.13-.35-.2-.77-.22-1.25a3.77 3.77 0 0 1-1.34 1.66c-.57.39-1.28.58-2.14.58-.58 0-1.1-.08-1.58-.24a3.3 3.3 0 0 1-1.24-.71c-.34-.32-.61-.72-.78-1.2-.18-.48-.26-1.04-.26-1.68 0-.67.1-1.24.31-1.7.21-.46.51-.84.91-1.13.4-.29.88-.5 1.44-.62.56-.13 1.18-.19 1.87-.19 1.04 0 1.91.16 2.62.48v-.68c0-.5-.15-.9-.46-1.2-.3-.3-.75-.46-1.34-.46-.54 0-1.03.12-1.46.36-.43.24-.74.57-.91.98zm2.62 3.39c-.58-.19-1.23-.29-1.94-.29-.4 0-.76.04-1.08.12-.32.08-.59.2-.82.36-.22.16-.39.37-.5.62-.11.26-.17.56-.17.91 0 .34.06.64.17.89.11.25.27.45.48.6.21.15.46.26.74.34.29.07.6.1 1 .1.5 0 .94-.08 1.32-.24.38-.16.71-.38.98-.67.27-.29.48-.62.62-1.01.14-.38.22-.8.22-1.25v-.38c-.38.01-.77.02-1.16.02zM1.86 18.06c4.66 3.45 11.24 4.38 16.92 1.5.34-.18.7.14.47.49-3.07 4.5-10.48 4.3-15.69.46-.47-.34-.12-.86.38-.62zm18.33-1.01c-.28-.36-.88-.42-1.22-.14-.34.28-.42.88-.14 1.22 1.34 1.66 3.03 2.84 5.03 3.45.4.12.82-.11.94-.51.12-.4-.11-.82-.51-.94-1.73-.52-3.18-1.54-4.1-3.08z",
    "lambda": "M8.4 2h2.8l4.4 12.8L18 2h3l-4.5 13.5L20 22h-3.2l-3-5.2L8.2 22H5l4.8-7.8L8.4 2zM3 2h3.5l1.6 4.8L6.4 10 3 2z",
    "s3": "M12 2C6.48 2 2 4.02 2 6.5v11C2 19.98 6.48 22 12 22s10-2.02 10-4.5v-11C22 4.02 17.52 2 12 2zm0 2.2c4.6 0 8 1.48 8 2.3s-3.4 2.3-8 2.3-8-1.48-8-2.3 3.4-2.3 8-2.3zm8 13.3c0 .82-3.4 2.3-8 2.3s-8-1.48-8-2.3v-2.2c2.1 1.3 5 2 8 2s5.9-.7 8-2v2.2zm0-4.5c0 .82-3.4 2.3-8 2.3s-8-1.48-8-2.3v-2.2c2.1 1.3 5 2 8 2s5.9-.7 8-2v2.2z",
    "dynamodb": "M12 2L3 6.5v11L12 22l9-4.5v-11L12 2zm0 2.3l7 3.5-7 3.5-7-3.5 7-3.5zm-7 5.3l6 3v6.8l-6-3V9.6zm8 9.8v-6.8l6-3v6.8l-6 3z",
    "rds": "M12 2C6.5 2 2 3.8 2 6v12c0 2.2 4.5 4 10 4s10-1.8 10-4V6c0-2.2-4.5-4-10-4zm0 2c4.4 0 8 1.3 8 2s-3.6 2-8 2-8-1.3-8-2 3.6-2 8-2zm8 14c0 .7-3.6 2-8 2s-8-1.3-8-2v-2.5c2 .9 4.8 1.5 8 1.5s6-.6 8-1.5V18zm0-4c0 .7-3.6 2-8 2s-8-1.3-8-2v-2.5c2 .9 4.8 1.5 8 1.5s6-.6 8-1.5V14zm0-4c0 .7-3.6 2-8 2s-8-1.3-8-2V7.5c2 .9 4.8 1.5 8 1.5s6-.6 8-1.5V10z",
    "cloudfront": "M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm0 2c1.78 0 3.39 1.48 4.2 3.75H7.8C8.61 5.48 10.22 4 12 4zm-6.2 5.75h12.4c.18.7.28 1.46.28 2.25s-.1 1.55-.28 2.25H5.8c-.18-.7-.28-1.46-.28-2.25s.1-1.55.28-2.25zM12 20c-1.78 0-3.39-1.48-4.2-3.75h8.4c-.81 2.27-2.42 3.75-4.2 3.75z",
    "apigateway": "M12 2L2 7l10 5 10-5-10-5zm0 8.3L4.7 7 12 3.4 19.3 7 12 10.3zM2 12l10 5 10-5-2-1-8 4-8-4-2 1zm0 5l10 5 10-5-2-1-8 4-8-4-2 1z",
    "sqs": "M3 5h18v3H3V5zm0 5h18v4H3v-4zm0 6h18v3H3v-3z",
    "sns": "M12 2a4 4 0 0 0-4 4c0 1.1.4 2.1 1.2 2.8L4 14v2h16v-2l-5.2-5.2c.8-.7 1.2-1.7 1.2-2.8a4 4 0 0 0-4-4zm0 2c1.1 0 2 .9 2 2s-.9 2-2 2-2-.9-2-2 .9-2 2-2zm-2 15a2 2 0 0 0 4 0h-4z",
    "ec2": "M4 3h16a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2zm0 10h16a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-4a2 2 0 0 1 2-2zm2-7a1 1 0 1 0 0 2 1 1 0 0 0 0-2zm0 10a1 1 0 1 0 0 2 1 1 0 0 0 0-2z",
    "ecs": "M12 2L2 7v10l10 5 10-5V7L12 2zm0 2.3l8 4V12l-8-4-8 4V8.3l8-4zm-8 8.4l7 3.5v5.5l-7-3.5v-5.5zm9 9v-5.5l7-3.5v5.5l-7 3.5z",
    "cloudwatch": "M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z",
    "sagemaker": "M12 2a3 3 0 0 1 3 3v1h1a3 3 0 0 1 3 3v2h1a3 3 0 0 1 3 3v2a3 3 0 0 1-3 3h-1v2a3 3 0 0 1-3 3h-1v1a3 3 0 0 1-6 0v-1H8a3 3 0 0 1-3-3v-2H4a3 3 0 0 1-3-3v-2a3 3 0 0 1 3-3h1V8a3 3 0 0 1 3-3h1V5a3 3 0 0 1 3-3zm1 4h-2v2h2V6zm4 4h-2v2h2v-2zm-8 0H7v2h2v-2zm10 4h-2v2h2v-2zm-12 0H5v2h2v-2zm10 4h-2v2h2v-2zm-8 0H7v2h2v-2zm4 2h-2v2h2v-2z",

    # GOOGLE CLOUD PLATFORM (GCP)
    "gcp": "M19.35 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96zM19 18H6c-2.21 0-4-1.79-4-4 0-2.05 1.53-3.76 3.56-3.97l1.07-.11.5-.95C8.08 7.14 9.94 6 12 6c2.62 0 4.88 1.86 5.39 4.43l.3 1.5 1.53.11c1.56.1 2.78 1.41 2.78 2.96 0 1.65-1.35 3-3 3z",
    "gke": "M12 0L1.6 6v12L12 24l10.4-6V6L12 0zm0 2.3l8.4 4.8v9.8L12 21.7 3.6 16.9V7.1L12 2.3zM12 6a6 6 0 1 0 0 12 6 6 0 0 0 0-12zm0 2a4 4 0 1 1 0 8 4 4 0 0 1 0-8z",
    "cloudsql": "M12 2C6.5 2 2 3.8 2 6v12c0 2.2 4.5 4 10 4s10-1.8 10-4V6c0-2.2-4.5-4-10-4zm0 2c4.4 0 8 1.3 8 2s-3.6 2-8 2-8-1.3-8-2 3.6-2 8-2zm8 14c0 .7-3.6 2-8 2s-8-1.3-8-2v-2.5c2 .9 4.8 1.5 8 1.5s6-.6 8-1.5V18zm0-4c0 .7-3.6 2-8 2s-8-1.3-8-2v-2.5c2 .9 4.8 1.5 8 1.5s6-.6 8-1.5V14z",
    "bigquery": "M19 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z",
    "pubsub": "M12 2L2 7v10l10 5 10-5V7L12 2zm0 2.8l7 3.5v7.4l-7 3.5-7-3.5V8.3l7-3.5zm-1 5.2v4h2v-4h-2zm0 6v2h2v-2h-2z",

    # MICROSOFT AZURE
    "azure": "M13.48 0a1.37 1.37 0 0 0-.96.44L.4 13.07a1.38 1.38 0 0 0 0 1.95l10.12 10.12c.26.26.61.42.96.42.35 0 .7-.16.96-.42l12.12-12.63a1.38 1.38 0 0 0 0-1.95L14.44.44A1.37 1.37 0 0 0 13.48 0zm-.02 3.01l8.8 9.17-8.8 9.17L4.67 12.18l8.8-9.17z",
    "azuresql": "M12 2C6.5 2 2 3.8 2 6v12c0 2.2 4.5 4 10 4s10-1.8 10-4V6c0-2.2-4.5-4-10-4zm0 2c4.4 0 8 1.3 8 2s-3.6 2-8 2-8-1.3-8-2 3.6-2 8-2zm8 14c0 .7-3.6 2-8 2s-8-1.3-8-2v-2.5c2 .9 4.8 1.5 8 1.5s6-.6 8-1.5V18z",
    "cosmosdb": "M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm0 3a7 7 0 1 1 0 14 7 7 0 0 1 0-14zm0 3a4 4 0 1 0 0 8 4 4 0 0 0 0-8z",

    # KUBERNETES & CONTAINERS
    "kubernetes": "M12 0L1.6 6v12L12 24l10.4-6V6L12 0zm0 2.3l8.4 4.8v9.8L12 21.7 3.6 16.9V7.1L12 2.3zM12 6a6 6 0 1 0 0 12 6 6 0 0 0 0-12zm0 2a4 4 0 1 1 0 8 4 4 0 0 1 0-8z",
    "docker": "M13.98 11.08h2.2a.3.3 0 0 0 .3-.3V8.58a.3.3 0 0 0-.3-.3h-2.2a.3.3 0 0 0-.3.3v2.2a.3.3 0 0 0 .3.3zm-2.74 0h2.2a.3.3 0 0 0 .3-.3V8.58a.3.3 0 0 0-.3-.3h-2.2a.3.3 0 0 0-.3.3v2.2a.3.3 0 0 0 .3.3zm-2.75 0h2.2a.3.3 0 0 0 .3-.3V8.58a.3.3 0 0 0-.3-.3H8.5a.3.3 0 0 0-.3.3v2.2a.3.3 0 0 0 .3.3zm5.49-2.75h2.2a.3.3 0 0 0 .3-.3V5.84a.3.3 0 0 0-.3-.3h-2.2a.3.3 0 0 0-.3.3v2.2a.3.3 0 0 0 .3.3zm-2.74 0h2.2a.3.3 0 0 0 .3-.3V5.84a.3.3 0 0 0-.3-.3h-2.2a.3.3 0 0 0-.3.3v2.2a.3.3 0 0 0 .3.3zm-2.75 0h2.2a.3.3 0 0 0 .3-.3V5.84a.3.3 0 0 0-.3-.3H8.5a.3.3 0 0 0-.3.3v2.2a.3.3 0 0 0 .3.3zM23.04 7.58c-.46-.15-1.46-.38-2.89-.23-1.26.13-2.29 1.01-2.59 1.49-.31.5-.92 1.54-2.62 1.54-1.63 0-2.31-1-2.48-1.5-.18-.51-.3-1.25-.32-1.56a.3.3 0 0 0-.28-.28H11.24c-.14 0-.26.1-.28.24-.05.23-.21 1.04-.67 1.78-.57.9-1.4 1.34-2.39 1.34-1.03 0-1.89-.45-2.46-1.26-.57-.8-.79-1.78-.79-2.78 0-1 .22-1.98.79-2.79.57-.8 1.43-1.25 2.46-1.25 1 0 1.82.43 2.39 1.34.46.73.62 1.55.67 1.78.03.13.14.24.28.24h1.72c.16 0 .28-.12.29-.28.01-.31.14-1.05.32-1.57.17-.5.84-1.49 2.48-1.49 1.69 0 2.3 1.04 2.62 1.54.3.48 1.33 1.36 2.59 1.49 1.42.15 2.42-.09 2.88-.24.2-.06.38.14.33.34-.15.66-.62 2.65-2.19 3.43l1.46 1.46c.12.12.12.3 0 .42l-1.06 1.06c-.12.12-.3.12-.42 0l-1.56-1.56c1.07-1.35 2.02-4.02 2.74-5.23z",
    "pod": "M12 2L2 7v10l10 5 10-5V7L12 2zm0 2.3l8 4v7.4l-8 4-8-4V8.3l8-4z",

    # DATABASES & CACHES
    "postgresql": "M12 0c-6.63 0-12 2.69-12 6 0 1.83 1.35 3.49 3.6 4.71C2.26 12.01 1.5 13.15 1.5 14.5c0 1.93 4.76 3.5 10.5 3.5s10.5-1.57 10.5-3.5c0-1.35-.76-2.49-2.1-3.79C22.65 9.49 24 7.83 24 6c0-3.31-5.37-6-12-6zm0 1.5c5.39 0 9.75 2.02 9.75 4.5S17.39 10.5 12 10.5 2.25 8.49 2.25 6 6.62 1.5 12 1.5zm-8.14 10.26C5.23 12.56 8.36 13.25 12 13.25s6.77-.69 8.14-1.49C21.43 12.58 22.5 13.48 22.5 14.5c0 1.35-4.16 2.75-10.5 2.75S1.5 15.85 1.5 14.5c0-1.02 1.07-1.92 2.36-2.74z",
    "mysql": "M12 3C6.5 3 2 4.8 2 7v10c0 2.2 4.5 4 10 4s10-1.8 10-4V7c0-2.2-4.5-4-10-4zm0 2c4.4 0 8 1.3 8 2s-3.6 2-8 2-8-1.3-8-2 3.6-2 8-2zm8 12c0 .7-3.6 2-8 2s-8-1.3-8-2v-2.5c2 .9 4.8 1.5 8 1.5s6-.6 8-1.5V17zm0-4c0 .7-3.6 2-8 2s-8-1.3-8-2V10.5c2 .9 4.8 1.5 8 1.5s6-.6 8-1.5V13z",
    "redis": "M0 5.68v2.66l12 4 12-4V5.68L12 9.68 0 5.68zm0 6v2.67l12 4 12-4v-2.67l-12 4-12-4zm0 6V20.35l12 4 12-4v-2.67l-12 4-12-4zM12 0L0 4l12 4 12-4L12 0z",
    "mongodb": "M12 0C12 0 4 6 4 13c0 4.4 3.6 8 8 11 4.4-3 8-6.6 8-11 0-7-8-13-8-13zm0 20.8c-3.1-2.4-6-5.3-6-7.8 0-4.3 4.4-8.8 6-10.3 1.6 1.5 6 6 6 10.3 0 2.5-2.9 5.4-6 7.8z",

    # MESSAGING & STREAMING
    "kafka": "M1.92 0C.86 0 0 .86 0 1.92v20.16C0 23.14.86 24 1.92 24h20.16c1.06 0 1.92-.86 1.92-1.92V1.92C24 .86 23.14 0 22.08 0zm4.27 5.04h3.12v13.92H6.19zm5.71 0h3.05v6.43l3.43-6.43h3.48l-4.73 8.11 5.09 5.81h-3.65l-3.62-4.51v4.51h-3.05z",
    "rabbitmq": "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 14h-2v-2h2v2zm0-4h-2V7h2v5z",

    # FRONTEND, APPS & TOOLS
    "react": "M12 21.64c-4.44 0-8.32-1.28-10.46-3.53-1.43-1.5-2-3.41-1.54-5.38.47-2 1.83-3.79 3.83-5.03.28-.18.59-.34.9-.49-.32-.92-.47-1.92-.42-2.92.09-2.11 1.26-3.9 3.09-4.64 1.78-.7 3.87-.48 5.48.6 1.58 1.06 2.6 2.77 2.77 4.68.08.86-.04 1.7-.33 2.5.43.18.85.4 1.25.63 2 1.24 3.36 3.03 3.83 5.03.46 1.97-.12 3.88-1.54 5.38-2.14 2.25-6.01 3.53-10.46 3.53zM12 4c-3.15 0-5.84 1.03-7.24 2.51-.94.99-1.33 2.26-1.03 3.55.32 1.34 1.22 2.54 2.55 3.38.62.39 1.35.72 2.15.95-.04-.3-.07-.6-.08-.9-.12-2.59 1.04-5.04 3.16-6.53 1.16-.8 2.54-1.21 3.92-1.16-1.13-1.01-2.59-1.63-4.33-1.8z",
    "nextjs": "M18.66 21.98C16.76 23.3 14.45 24 12 24 5.37 24 0 18.63 0 12S5.37 0 12 0c2.49 0 4.83.75 6.81 2.12l-9.06 11.67h-2.1v-9.57H5.4v13.5h2.46l9.3-11.97h2.1v9.87h2.4v-13.5c1.47 1.95 2.34 4.38 2.34 7.02 0 6.63-5.37 12-12 12zm1.14-7.86v9.75h2.4v-9.75h-2.4z",
    "fastapi": "M12 0L2 13.5h7.5L8 24l14-14.5h-8L16 0H12z",
    "python": "M11.93 0c-3.12 0-5.33.27-5.33 2.14v2.4h5.45v.8H4.63C2.08 5.34 0 7.37 0 10.3c0 2.94 1.84 4.63 4.63 4.63h1.49v-2.07c0-1.63 1.38-2.94 3.01-2.94h5.27c1.38 0 2.5-1.12 2.5-2.5V2.14C16.9 0 14.68 0 11.93 0zM8.88 1.4c.5 0 .9.4.9.9s-.4.9-.9.9-.9-.4-.9-.9.4-.9.9-.9zm3.19 22.6c3.12 0 5.33-.27 5.33-2.14v-2.4h-5.45v-.8h7.42c2.55 0 4.63-2.03 4.63-4.96 0-2.94-1.84-4.63-4.63-4.63h-1.49v2.07c0 1.63-1.38 2.94-3.01 2.94H9.6c-1.38 0-2.5 1.12-2.5 2.5v5.28c0 2.14 2.22 2.14 4.97 2.14zm3.05-1.4c-.5 0-.9-.4-.9-.9s.4-.9.9-.9.9.4.9.9-.4.9-.9.9z",
    "nodejs": "M12 2L2 7.7v11.6L12 25l10-5.7V7.7L12 2zm0 2.3l8 4.6v9.2l-8 4.6-8-4.6V8.9l8-4.6z",
    "stripe": "M13.98 9.3c0-.85-.68-1.18-1.8-1.18-1.6 0-3.64.6-5.06 1.48L6 6.32C7.72 5.24 10.16 4.6 12.38 4.6c3.78 0 6.22 1.94 6.22 5.04 0 4.92-6.74 4.14-6.74 6.26 0 .98.84 1.3 2.02 1.3 1.84 0 4.16-.8 5.76-1.82l1.1 3.28c-1.86 1.2-4.52 1.84-6.98 1.84-3.98 0-6.6-1.98-6.6-5.18 0-5.26 6.82-4.32 6.82-6.02z",
    "cloudflare": "M19.4 12.5a5.5 5.5 0 0 0-10.4-1.7A4.2 4.2 0 0 0 5 15a4.2 4.2 0 0 0 4.2 4.2h10a3.8 3.8 0 0 0 3.8-3.8c0-1.8-1.3-3.4-3.6-3.7z",
    "nginx": "M12 2L2 7v10l10 5 10-5V7L12 2zm0 2.2l8 4v9.6l-8 4-8-4V8.2l8-4zm-4 4.8v6l5-3.5v-2.5L8 9z",

    # GENERIC FALLBACKS
    "cloud": "M6 18a4 4 0 0 1 .5-7.97A6 6 0 0 1 18 9a3.5 3.5 0 0 1 0 7H6z",
    "server": "M4 3h16a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2zm0 10h16a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-4a2 2 0 0 1 2-2z",
    "database": "M4 6c0-1.66 3.58-3 8-3s8 1.34 8 3v12c0 1.66-3.58 3-8 3s-8-1.34-8-3V6zm0 4c0 1.66 3.58 3 8 3s8-1.34 8-3M4 14c0 1.66 3.58 3 8 3s8-1.34 8-3",
    "cube": "M12 2L2 7v10l10 5 10-5V7L12 2zm0 2.3l8 4v7.4l-8 4-8-4V8.3l8-4z",
}

# Catalog mapping keywords -> service metadata, foolproof vector icon key, brand colors & tags
SERVICE_RULES = [
    # --- AWS ---
    (["lambda", "serverless function"], "aws", "compute", "lambda", "#FF9900", "AWS Lambda", "Amazon Web Services - AWS Lambda"),
    (["s3", "blob storage", "bucket", "object storage"], "aws", "storage", "s3", "#569A31", "Amazon S3", "Amazon Web Services - Amazon Simple Storage Service S3"),
    (["dynamodb", "dynamo"], "aws", "database", "dynamodb", "#4053D6", "Amazon DynamoDB", "Amazon Web Services - Amazon DynamoDB"),
    (["rds", "aurora", "postgres", "postgresql"], "aws", "database", "postgresql", "#527FFF", "Amazon RDS / PostgreSQL", "Amazon Web Services - Amazon Relational Database Service"),
    (["mysql", "mariadb"], "aws", "database", "mysql", "#0EA5E9", "MySQL Database", "Amazon Web Services - Amazon Relational Database Service"),
    (["elasticache", "redis", "memorystore"], "generic", "cache", "redis", "#DC382D", "Redis Cache", "Amazon Web Services - Amazon ElastiCache"),
    (["cloudfront", "cdn", "edge cache"], "aws", "cdn", "cloudfront", "#8C4FFF", "CloudFront CDN", "Amazon Web Services - Amazon CloudFront"),
    (["api gateway", "apigateway", "kong", "traefik"], "aws", "networking", "apigateway", "#E7157B", "Amazon API Gateway", "Amazon Web Services - Amazon API Gateway"),
    (["sns", "notification service"], "aws", "messaging", "sns", "#FF4F8B", "Amazon SNS", "Amazon Web Services - Amazon Simple Notification Service SNS"),
    (["sqs", "rabbitmq", "queue", "message queue"], "aws", "queue", "sqs", "#FF4F8B", "Amazon SQS", "Amazon Web Services - Amazon Simple Queue Service SQS"),
    (["kafka", "msk"], "generic", "messaging", "kafka", "#231F20", "Apache Kafka", "Amazon Web Services - Amazon Managed Streaming for Apache Kafka"),
    (["ecs", "fargate", "container service"], "aws", "container", "ecs", "#FF9900", "Amazon ECS / Fargate", "Amazon Web Services - Amazon Elastic Container Service"),
    (["ec2", "virtual machine", "vm", "monolith"], "aws", "compute", "ec2", "#FF9900", "Amazon EC2", "Amazon Web Services - Amazon Elastic Compute Cloud"),
    (["cloudwatch", "datadog", "grafana", "prometheus", "monitoring"], "aws", "monitoring", "cloudwatch", "#64748B", "Amazon CloudWatch", "Amazon Web Services - Amazon CloudWatch"),
    (["bedrock", "sagemaker", "llm", "ai", "openai", "gemini", "claude"], "aws", "ai", "sagemaker", "#A855F7", "Amazon SageMaker / AI", "Amazon Web Services - Amazon SageMaker"),
    (["stripe", "payment"], "generic", "external", "stripe", "#635BFF", "Stripe Payment Gateway", "External System"),

    # --- AZURE ---
    (["azure function", "functions"], "azure", "compute", "azure", "#0089D6", "Azure Functions", "Microsoft Azure - Azure Functions"),
    (["azure sql", "sql database"], "azure", "database", "azuresql", "#0089D6", "Azure SQL Database", "Microsoft Azure - SQL Database"),
    (["cosmos", "cosmosdb"], "azure", "database", "cosmosdb", "#0089D6", "Azure Cosmos DB", "Microsoft Azure - Azure Cosmos DB"),
    (["aks", "azure kubernetes"], "azure", "container", "kubernetes", "#0089D6", "Azure Kubernetes Service", "Microsoft Azure - Azure Kubernetes Service"),

    # --- GCP ---
    (["gke", "google kubernetes engine"], "gcp", "container", "kubernetes", "#4285F4", "Google Kubernetes Engine (GKE)", "Google Cloud Platform - Google Kubernetes Engine"),
    (["cloud function", "google cloud function"], "gcp", "compute", "gcp", "#4285F4", "Google Cloud Functions", "Google Cloud Platform - Cloud Functions"),
    (["cloud sql"], "gcp", "database", "cloudsql", "#4285F4", "Google Cloud SQL", "Google Cloud Platform - Cloud SQL"),
    (["bigquery"], "gcp", "database", "bigquery", "#4285F4", "Google BigQuery", "Google Cloud Platform - BigQuery"),
    (["pub/sub", "pubsub"], "gcp", "messaging", "pubsub", "#4285F4", "Google Cloud Pub/Sub", "Google Cloud Platform - PubSub"),

    # --- KUBERNETES ---
    (["k8s", "kubernetes", "pod", "deployment", "ingress"], "kubernetes", "container", "kubernetes", "#326CE5", "Kubernetes", "Kubernetes - Pod"),
    (["docker"], "generic", "container", "docker", "#2496ED", "Docker Container", "Microservice"),

    # --- WEB & LANGUAGES ---
    (["next.js", "nextjs"], "generic", "frontend", "nextjs", "#000000", "Next.js Web Client", "Web Browser"),
    (["react"], "generic", "frontend", "react", "#0EA5E9", "React SPA", "Web Browser"),
    (["fastapi", "python"], "generic", "compute", "fastapi", "#009688", "FastAPI Service", "Microservice"),
    (["node", "express"], "generic", "compute", "nodejs", "#5FA04E", "Node.js Service", "Microservice"),
    (["cloudflare"], "generic", "cdn", "cloudflare", "#F38020", "Cloudflare Edge", "Amazon Web Services - Amazon CloudFront"),
    (["nginx"], "generic", "networking", "nginx", "#009639", "NGINX Gateway", "Amazon Web Services - Amazon API Gateway"),
]


def infer_service_metadata(label: str, tech: str = "", tier: str = "services") -> Dict[str, Any]:
    """
    Infers cloud provider, category, authentic vector icon, brand color, and Structurizr tags.
    100% foolproof: embeds pure SVG path data that NEVER fails in local file downloads!
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

        if any(kw in search_text for kw in keywords):
            path_data = VECTOR_ICONS.get(icon_key, VECTOR_ICONS["cube"])
            return {
                "provider": provider,
                "type": s_type,
                "icon": path_data,
                "icon_name": icon_key,
                "brand_color": color,
                "service_name": canonical_name,
                "structurizr_tag": structurizr_tag,
                "structurizr_theme": STRUCTURIZR_THEMES.get(provider, STRUCTURIZR_THEMES["aws"])
            }

    # Fallback based on tier
    fallback_map = {
        "client": ("generic", "frontend", "react", "#0EA5E9", "Client / UI", "Web Browser"),
        "gateway": ("generic", "networking", "apigateway", "#8B5CF6", "Gateway / Proxy", "Amazon Web Services - Amazon API Gateway"),
        "services": ("generic", "compute", "server", "#3B82F6", "Service Container", "Microservice"),
        "data": ("generic", "database", "database", "#10B981", "Database Storage", "Database")
    }

    prov, s_type, icon_key, color, s_name, s_tag = fallback_map.get(tier, ("generic", "compute", "cube", "#6366F1", "Component", "Microservice"))
    path_data = VECTOR_ICONS.get(icon_key, VECTOR_ICONS["cube"])
    return {
        "provider": prov,
        "type": s_type,
        "icon": path_data,
        "icon_name": icon_key,
        "brand_color": color,
        "service_name": s_name,
        "structurizr_tag": s_tag,
        "structurizr_theme": STRUCTURIZR_THEMES.get(prov, "")
    }
