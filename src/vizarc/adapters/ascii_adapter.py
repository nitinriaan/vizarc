"""
ASCII Adapter: deterministically transforms Canonical Architecture IR into terminal Unicode boxes.
"""

from typing import Dict, Any
from .base import BaseAdapter

class ASCIIAdapter(BaseAdapter):
    def render(self, ir: Dict[str, Any]) -> str:
        tiers = ir.get("tiers", [])
        nodes = ir.get("nodes", [])
        edges = ir.get("edges", [])

        title = ir.get("title", "Architecture Diagram")
        lines = [
            f"=== {title.upper()} ===",
            ""
        ]

        # Group by tier
        nodes_by_tier = {t["id"]: [] for t in tiers}
        for n in nodes:
            tier_id = n.get("tier", "services")
            if tier_id in nodes_by_tier:
                nodes_by_tier[tier_id].append(n)
            else:
                nodes_by_tier.setdefault("services", []).append(n)

        for idx, tier in enumerate(tiers):
            t_id = tier["id"]
            tier_nodes = nodes_by_tier.get(t_id, [])
            if not tier_nodes:
                continue

            lines.append(f"┌─[ {tier.get('label', t_id).upper()} ]" + "─" * 40)
            for node in tier_nodes:
                tech = f" [{node['tech']}]" if node.get("tech") else ""
                lines.append(f"│  • {node.get('label', node['id'])}{tech}")
                # List outgoing connections
                outgoings = [e for e in edges if e["from"] == node["id"]]
                for e in outgoings:
                    lines.append(f"│      └──► {e['to']} ({e.get('label', 'calls')})")
            lines.append("└" + "─" * 56)
            
            if idx < len(tiers) - 1:
                lines.append("                       │")
                lines.append("                       ▼")

        return "\n".join(lines).strip()
