"""
Core VizArc Engine: implements the Universal Architecture Compiler Pattern.
Calls AI once to produce the Canonical Architecture Model (JSON IR),
then deterministically compiles it into D2, Mermaid, Structurizr C4, PlantUML,
Graphviz DOT, Excalidraw, ASCII, and Interactive HTML.
"""

import os
import json
import re
from typing import Optional, Dict, Any
from dotenv import load_dotenv

from .ir import IR_SCHEMA_PROMPT, validate_ir, get_demo_ir
from .adapters import render_ir, render_all_formats, ADAPTERS

load_dotenv()

class VizArcEngine:
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-3.8-flash"):
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

    def generate_ir(self, prompt: str, codebase_context: Optional[str] = None) -> Dict[str, Any]:
        """
        Generates a validated Canonical Architecture JSON Intermediate Representation (IR).
        """
        if not self._client_initialized:
            return get_demo_ir()

        full_prompt = (
            f"{IR_SCHEMA_PROMPT}\n\n---\n"
            f"USER SPECIFICATION:\n{prompt}\n"
        )
        if codebase_context:
            full_prompt += f"\nCODEBASE CONTEXT:\n{codebase_context}\n"

        try:
            response = self.model.generate_content(
                full_prompt,
                generation_config={"temperature": 0.2, "response_mime_type": "application/json"}
            )
            raw_text = response.text or "{}"
            cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw_text.strip(), flags=re.MULTILINE)
            parsed = json.loads(cleaned)
            return validate_ir(parsed)
        except Exception:
            # Fallback to demo IR if parsing fails
            return get_demo_ir()

    def generate(
        self,
        prompt: str,
        diagram_format: str = "html",
        archetype: str = "architecture",
        codebase_context: Optional[str] = None
    ) -> str:
        """
        1. Analyzes prompt/codebase to produce the Canonical IR (1 LLM call).
        2. Compiles IR to the target format deterministically via adapters.
        """
        ir = self.generate_ir(prompt=prompt, codebase_context=codebase_context)
        return render_ir(ir, target_format=diagram_format)

    def generate_all(
        self,
        prompt: str,
        codebase_context: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Produces the Canonical IR once and compiles into all 8 formats simultaneously.
        """
        ir = self.generate_ir(prompt=prompt, codebase_context=codebase_context)
        results = render_all_formats(ir)
        results["ir"] = json.dumps(ir, indent=2)
        return results
