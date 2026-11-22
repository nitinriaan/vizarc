---
name: vizarc
description: AI-powered software architecture and system diagram generator. Use when the user asks to visualize a codebase, design system architectures, map out microservices, create sequence diagrams, or export diagrams in Mermaid, D2, ASCII, or Excalidraw formats.
---

# VizArc: Architecture & Diagramming Skill

`vizarc` transforms codebases, system requirements, and complex workflows into clean, production-grade architecture diagrams. It supports multiple formats (**Mermaid.js**, **D2 Lang**, **ASCII/Unicode**, and **Excalidraw**) with self-healing syntax validation.

---

## When to Use This Skill

Activate this skill when:
- The user asks to **"visualize the codebase"** or map out project architecture.
- The user wants a **flowchart**, **sequence diagram**, **C4 architecture**, or **database ERD**.
- The user requests diagrams in **D2**, **Mermaid**, **ASCII art** (for terminal/READMEs), or **Excalidraw**.
- The user needs an architecture diagram to accompany a PR, RFC, or documentation.

---

## Agent Execution Instructions

When invoked to generate or update architecture diagrams:

### 1. Codebase Analysis Mode
If the user wants to diagram an existing project:
1. Scan the repository structure (directory tree, key framework configs like `package.json`, `requirements.txt`, `docker-compose.yml`, route files, database schemas).
2. Identify core boundaries:
   - **Frontend / Client tier** (Web, Mobile, CLI)
   - **Gateway / Ingress tier** (Nginx, API Gateway, Load Balancer)
   - **Application / Services tier** (Microservices, Background Workers, Auth)
   - **Data / Storage tier** (Databases, Redis caches, S3/Object storage)
3. Execute the CLI analyzer or generate the diagram matching the requested format.

### 2. Prompt / Specification Mode
If the user describes a system from scratch (e.g., *"Design an event-driven notification service with Kafka and Redis"*):
1. Clarify component roles, data flow directions, and protocols (gRPC, REST, WebSocket, Pub/Sub).
2. Choose the best diagram format:
   - **Mermaid**: Recommended for GitHub markdown files and documentation.
   - **D2**: Recommended for deep system architectures with container grouping and modern styling.
   - **ASCII**: Recommended for code comments, terminal displays, or commit messages.
   - **Excalidraw**: Recommended when the user wants an editable whiteboard mockup.

---

## CLI Quick Reference

```bash
# Generate architecture from a description
python cli.py generate "Microservice payment processing with Stripe and Kafka" --format mermaid

# Generate D2 architecture diagram
python cli.py generate "E-commerce cloud topology on AWS" --format d2

# Scan a local codebase and output an architecture diagram
python cli.py scan ./src --format mermaid --output ARCHITECTURE.md

# Generate ASCII diagram for terminal or PR comments
python cli.py generate "OAuth2 Authorization Code Flow" --format ascii

# Launch the interactive web playground
streamlit run app.py
```

---

## Syntax & Formatting Rules

To avoid broken diagrams, enforce these rules:

### Mermaid Rules:
1. Always wrap node labels containing parentheses, spaces, or brackets in double quotes:
   `User["Client (Web App)"] --> API["API Gateway (Port 8080)"]`
2. Explicitly specify direction (`flowchart TD` or `sequenceDiagram` or `erDiagram`).
3. Keep node IDs alphanumeric and simple (`auth_svc`, `db_pg`).

### D2 Rules:
1. Use semantic container definitions:
   ```d2
   cloud: Cloud Provider {
     api: API Gateway
     db: PostgreSQL
     api -> db: Read/Write
   }
   ```
2. Keep styling clean and use standard connections (`->`, `<->`, `<-`).

### ASCII Rules:
1. Use Unicode box-drawing characters (`┌─┐`, `│ │`, `└─┘`, `▲`, `▼`, `◄`, `►`).
2. Align arrows neatly with consistent spacing.
