"""
HTML Adapter: wraps compiler.py to produce the standalone interactive canvas.
"""

from typing import Dict, Any
from .base import BaseAdapter
from ..compiler import compile_to_html

class HTMLAdapter(BaseAdapter):
    def render(self, ir: Dict[str, Any]) -> str:
        return compile_to_html(ir)
