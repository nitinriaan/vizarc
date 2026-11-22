"""
Core VizArc Engine: connects to Gemini Flash API and manages diagram synthesis.
"""

import os
from typing import Optional
from dotenv import load_dotenv

from .formats.mermaid import MERMAID_SYSTEM_PROMPT, sanitize_mermaid
from .formats.d2 import D2_SYSTEM_PROMPT, sanitize_d2
from .formats.ascii import ASCII_SYSTEM_PROMPT, sanitize_ascii
from .formats.excalidraw import EXCALIDRAW_SYSTEM_PROMPT, prepare_for_excalidraw

load_dotenv()

ARCHETYPE_INSTRUCTIONS = {
    "architecture": "Focus on high-level system architecture, client tiers, API gateways, microservices, caches, and database storage.",
    "sequence": "Focus on the step-by-step sequence of requests, responses, authentication checks, and asynchronous events between actors.",
    "flowchart": "Focus on business logic, decision trees, conditional branches, and user decision paths.",
    "erd": "Focus on database tables, entities, fields, primary keys, and foreign key relationships.",
}

class VizArcEngine:
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-1.5-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = model_name
        self._client_initialized = False

        if self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(self.model_name)
                self._client_initialized = True
            except Exception as e:
                self._client_initialized = False
                self.init_error = str(e)

    def generate(
        self,
        prompt: str,
        diagram_format: str = "mermaid",
        archetype: str = "architecture",
        codebase_context: Optional[str] = None
    ) -> str:
        """
        Generates a diagram using Gemini or returns a structured demo response.
        """
        diagram_format = diagram_format.lower()
        archetype = archetype.lower()

        # Select prompt and sanitizer based on format
        if diagram_format == "d2":
            system_prompt = D2_SYSTEM_PROMPT
            sanitizer = sanitize_d2
        elif diagram_format == "ascii":
            system_prompt = ASCII_SYSTEM_PROMPT
            sanitizer = sanitize_ascii
        elif diagram_format == "excalidraw":
            system_prompt = EXCALIDRAW_SYSTEM_PROMPT
            sanitizer = prepare_for_excalidraw
        else: # default mermaid
            system_prompt = MERMAID_SYSTEM_PROMPT
            sanitizer = sanitize_mermaid

        archetype_note = ARCHETYPE_INSTRUCTIONS.get(archetype, ARCHETYPE_INSTRUCTIONS["architecture"])

        user_content = f"DIAGRAM TYPE: {archetype.upper()}\nGOAL: {archetype_note}\n\n"
        if codebase_context:
            user_content += f"CODEBASE ARCHITECTURE CONTEXT:\n{codebase_context}\n\n"
        user_content += f"USER SPECIFICATION / REQUIREMENTS:\n{prompt}\n"

        if not self._client_initialized:
            # Fallback mock template if no API key is configured yet
            return self._generate_fallback(diagram_format, prompt)

        full_prompt = f"{system_prompt}\n\n---\n{user_content}"
        
        response = self.model.generate_content(
            full_prompt,
            generation_config={"temperature": 0.2}
        )
        
        raw_text = response.text or ""
        return sanitizer(raw_text)

    def _generate_fallback(self, diagram_format: str, prompt: str) -> str:
        """Demo response returned when GEMINI_API_KEY is not yet supplied."""
        if diagram_format == "d2":
            return (
                "# (Demo Mode - Set GEMINI_API_KEY for live generation)\n"
                "client: Web Application {\n"
                "  shape: person\n"
                "}\n"
                "gateway: API Gateway\n"
                "services: Backend Services {\n"
                "  auth: Auth Service\n"
                "  core: Core Engine\n"
                "}\n"
                "db: PostgreSQL Database {\n"
                "  shape: cylinder\n"
                "}\n"
                "client -> gateway: HTTPS / API\n"
                "gateway -> services.auth: Authenticate\n"
                "services.auth -> db: Query Credentials\n"
                "gateway -> services.core: Process Request\n"
            )
        elif diagram_format == "ascii":
            return (
                "┌────────────────┐       HTTPS        ┌─────────────┐\n"
                "│  Web / Mobile  ├───────────────────►│ API Gateway │\n"
                "└────────────────┘                    └──────┬──────┘\n"
                "                                             │\n"
                "                         ┌───────────────────┴───────────────────┐\n"
                "                         ▼                                       ▼\n"
                "               ┌───────────────────┐                   ┌───────────────────┐\n"
                "               │   Auth Service    │                   │   Core Services   │\n"
                "               └─────────┬─────────┘                   └─────────┬─────────┘\n"
                "                         │                                       │\n"
                "                         ▼                                       ▼\n"
                "               ┌───────────────────┐                   ┌───────────────────┐\n"
                "               │ Redis Session DB  │                   │ PostgreSQL (Data) │\n"
                "               └───────────────────┘                   └───────────────────┘"
            )
        else: # mermaid
            return (
                "flowchart TD\n"
                '    User["Client (Web / Mobile)"] -->|HTTPS| APIGW["API Gateway"]\n'
                '    subgraph Core Services\n'
                '        AuthSvc["Auth Service"]\n'
                '        AppSvc["Core App Engine"]\n'
                '    end\n'
                '    subgraph Data Layer\n'
                '        Cache[("Redis Cache")]\n'
                '        DB[("PostgreSQL DB")]\n'
                '    end\n'
                '    APIGW --> AuthSvc\n'
                '    APIGW --> AppSvc\n'
                '    AuthSvc --> Cache\n'
                '    AppSvc --> DB'
            )

