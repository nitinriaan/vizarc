"""
Universal Adapter Registry: compiles Canonical Architecture IR to any target format.
"""

from typing import Dict, Any
from .base import BaseAdapter
from .d2_adapter import D2Adapter
from .mermaid_adapter import MermaidAdapter
from .structurizr_adapter import StructurizrAdapter
from .plantuml_adapter import PlantUMLAdapter
from .graphviz_adapter import GraphvizAdapter
from .excalidraw_adapter import ExcalidrawAdapter
from .ascii_adapter import ASCIIAdapter
from .html_adapter import HTMLAdapter

ADAPTERS = {
    "html": HTMLAdapter(),
    "d2": D2Adapter(),
    "mermaid": MermaidAdapter(),
    "structurizr": StructurizrAdapter(),
    "plantuml": PlantUMLAdapter(),
    "graphviz": GraphvizAdapter(),
    "dot": GraphvizAdapter(),
    "excalidraw": ExcalidrawAdapter(),
    "ascii": ASCIIAdapter()
}

def render_ir(ir: Dict[str, Any], target_format: str = "html") -> str:
    """Renders a Canonical Architecture IR to the specified format."""
    fmt = target_format.lower().strip()
    adapter = ADAPTERS.get(fmt, ADAPTERS["html"])
    return adapter.render(ir)

def render_all_formats(ir: Dict[str, Any]) -> Dict[str, str]:
    """Renders a Canonical Architecture IR to all supported formats in one pass."""
    return {
        fmt_name: adapter.render(ir)
        for fmt_name, adapter in ADAPTERS.items()
        if fmt_name != "dot" # avoid duplicate graphviz
    }
