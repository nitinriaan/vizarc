"""
Excalidraw diagram generator and exporter.
Excalidraw natively imports Mermaid diagrams and can also parse structured scene elements.
"""

from .mermaid import MERMAID_SYSTEM_PROMPT, sanitize_mermaid

EXCALIDRAW_SYSTEM_PROMPT = """You are an expert system designer generating diagrams intended for Excalidraw.
Excalidraw natively imports standard Mermaid flowchart and sequence syntax.
Generate an architecture diagram optimized for visual whiteboard clarity with clear subgraphs and clean component names.

Output ONLY valid Mermaid flowchart or sequence syntax without code fences.
"""

def prepare_for_excalidraw(raw_output: str) -> str:
    """
    Cleans and prepares Mermaid syntax specifically tested for Excalidraw import.
    Users can paste this directly into Excalidraw (More Tools > Mermaid to Excalidraw).
    """
    return sanitize_mermaid(raw_output)
