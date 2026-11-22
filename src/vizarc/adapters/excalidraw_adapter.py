"""
Excalidraw Adapter: transforms Canonical Architecture IR into Excalidraw-compatible format.
"""

from typing import Dict, Any
from .base import BaseAdapter
from .mermaid_adapter import MermaidAdapter

class ExcalidrawAdapter(BaseAdapter):
    def render(self, ir: Dict[str, Any]) -> str:
        # Excalidraw's official tool imports standard Mermaid syntax via 'Mermaid to Excalidraw'
        mermaid_code = MermaidAdapter().render(ir)
        return (
            f"%% Excalidraw-Optimized Diagram\n"
            f"%% Paste this into Excalidraw (More Tools > Mermaid to Excalidraw)\n"
            f"{mermaid_code}"
        )
