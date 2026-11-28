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

from .ir import (
    IR_SCHEMA_PROMPT,
    validate_ir,
    get_demo_ir,
    detect_archetype,
    guide_archetype,
    lint_ir,
    compare_architectures,
    ARCHETYPES
)
from .analyzer import CodebaseAnalyzer
from .adapters import render_ir, render_all_formats, ADAPTERS

load_dotenv()

AVAILABLE_MODELS = [
    "gemini-3.5-flash",
    "gemini-flash-latest",
    "gemini-3.7-flash",
    "gemini-3.8-flash"
]

class VizArcEngine:
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-3.5-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = model_name
        self._client_initialized = False
        self.last_error = None
        self.last_model_used = None

        if self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.genai = genai
                self._client_initialized = True
            except Exception as e:
                self._client_initialized = False
                self.init_error = str(e)
                self.last_error = str(e)

    def generate_ir(
        self,
        prompt: str,
        archetype: Optional[str] = None,
        codebase_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generates a validated Canonical Architecture JSON Intermediate Representation (IR).
        Includes automatic model failover across supported Gemini models.
        """
        if not self._client_initialized:
            self.last_error = "Gemini API client not initialized. Please verify your GEMINI_API_KEY."
            demo = get_demo_ir()
            if archetype:
                demo["archetype"] = archetype
            return demo

        detected_arch = archetype or detect_archetype(prompt)
        arch_meta = ARCHETYPES.get(detected_arch, ARCHETYPES["architecture"])

        full_prompt = (
            f"{IR_SCHEMA_PROMPT}\n\n---\n"
            f"TARGET ARCHETYPE: {detected_arch} ({arch_meta['name']}: {arch_meta['description']})\n"
            f"RECOMMENDED TIERS:\n{json.dumps(arch_meta['default_tiers'], indent=2)}\n\n"
            f"USER SPECIFICATION:\n{prompt}\n"
        )
        if codebase_context:
            full_prompt += f"\nCODEBASE CONTEXT:\n{codebase_context}\n"

        models_to_try = [self.model_name] + [m for m in AVAILABLE_MODELS if m != self.model_name]
        last_exception = None

        for m_name in models_to_try:
            try:
                model = self.genai.GenerativeModel(m_name)
                response = model.generate_content(
                    full_prompt,
                    generation_config={"temperature": 0.2, "response_mime_type": "application/json"}
                )
                raw_text = response.text or "{}"
                cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw_text.strip(), flags=re.MULTILINE)
                parsed = json.loads(cleaned)
                parsed["archetype"] = detected_arch
                self.last_model_used = m_name
                self.last_error = None
                return validate_ir(parsed)
            except Exception as e:
                last_exception = e
                continue

        self.last_error = f"API error across candidate models: {last_exception}"
        demo = get_demo_ir()
        demo["archetype"] = detected_arch
        return demo

    def generate(
        self,
        prompt: str,
        diagram_format: str = "html",
        archetype: Optional[str] = None,
        codebase_context: Optional[str] = None
    ) -> str:
        """
        1. Analyzes prompt/codebase to produce the Canonical IR (1 LLM call).
        2. Compiles IR to the target format deterministically via adapters.
        """
        ir = self.generate_ir(prompt=prompt, archetype=archetype, codebase_context=codebase_context)
        return render_ir(ir, target_format=diagram_format)

    def generate_all(
        self,
        prompt: str,
        archetype: Optional[str] = None,
        codebase_context: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Produces the Canonical IR once and compiles into all formats simultaneously.
        """
        ir = self.generate_ir(prompt=prompt, archetype=archetype, codebase_context=codebase_context)
        results = render_all_formats(ir)
        results["ir"] = json.dumps(ir, indent=2)
        return results

    def guide(self, prompt: str) -> Dict[str, Any]:
        """
        Archetype guidance engine (Archify guide spec):
        Analyzes prompt and returns recommended archetype, tiers, and an optimized prompt.
        """
        return guide_archetype(prompt)

    def validate(self, ir_data: Any) -> Dict[str, Any]:
        """
        Machine-readable architectural static analysis (Archify validate spec):
        Performs rule-based verification and returns structured diagnostics.
        """
        if isinstance(ir_data, str):
            # Attempt to parse as JSON or extract embedded IR from HTML
            cleaned = ir_data.strip()
            if cleaned.startswith("{"):
                ir_data = json.loads(cleaned)
            elif "const IR = " in ir_data:
                m = re.search(r"const\s+IR\s*=\s*(\{.*?\});", ir_data, re.DOTALL)
                if m:
                    ir_data = json.loads(m.group(1))
                else:
                    raise ValueError("Could not find embedded IR in provided HTML.")
            else:
                raise ValueError("Input string is neither valid JSON nor contains embedded IR.")

        return lint_ir(ir_data)

    def compare(self, base_ir: Dict[str, Any], head_ir: Dict[str, Any]) -> Dict[str, Any]:
        """
        Architecture delta and diff analyzer (Archify compare spec):
        Computes changes between two architecture specifications.
        """
        return compare_architectures(base_ir, head_ir)

    def diagnose(self, codebase_path: str = ".") -> Dict[str, Any]:
        """
        Codebase architecture diagnostic engine (Archify diagnose spec):
        Scans code, finds dependency cycles, calculates coupling hotspots, and recommends archetypes.
        """
        analyzer = CodebaseAnalyzer(codebase_path)
        return analyzer.diagnose()
