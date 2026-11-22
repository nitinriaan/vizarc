"""
Base Adapter class for all VizArc architecture rendering backends.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAdapter(ABC):
    @abstractmethod
    def render(self, ir: Dict[str, Any]) -> str:
        """Transforms Canonical Architecture IR into the target diagram format."""
        pass
