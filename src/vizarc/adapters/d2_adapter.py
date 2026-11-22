"""
Deterministic D2 Lang Adapter: transforms Canonical Architecture IR into D2.
"""

from typing import Dict, Any
from .base import BaseAdapter

SHAPE_MAP = {
    "data": "cylinder",
    "client": "person",
    "gateway": "hexagon",
    "services": "rectangle"
}

class D2Adapter(BaseAdapter):
    def render(self, ir: Dict[str, Any]) -> str:
        lines = [
            f"# {ir.get('title', 'Architecture Diagram')}",
            f"# {ir.get('summary', '')}",
            ""
        ]

        # Group nodes by tier containers
        tiers = ir.get("tiers", [])
        nodes = ir.get("nodes", [])
        edges = ir.get("edges", [])

        nodes_by_tier = {t["id"]: [] for t in tiers}
        for n in nodes:
            tier_id = n.get("tier", "services")
            if tier_id in nodes_by_tier:
                nodes_by_tier[tier_id].append(n)
            else:
                nodes_by_tier.setdefault("services", []).append(n)

        # 1. Render Containers & Nodes
        for tier in tiers:
            t_id = tier["id"]
            tier_nodes = nodes_by_tier.get(t_id, [])
            if not tier_nodes:
                continue

            lines.append(f"{t_id}: {tier.get('label', t_id)} {{")
            for node in tier_nodes:
                n_id = node["id"]
                label = node.get("label", n_id)
                shape = SHAPE_MAP.get(t_id, "rectangle")
                lines.append(f"  {n_id}: \"{label}\" {{")
                lines.append(f"    shape: {shape}")
                if node.get("tech"):
                    lines.append(f"    tooltip: \"Tech: {node['tech']}\"")
                lines.append("  }")
            lines.append("}")
            lines.append("")

        # 2. Render Connections
        lines.append("# Connections")
        for edge in edges:
            from_id = edge["from"]
            to_id = edge["to"]
            label = edge.get("label", "")

            # Resolve container scoping
            from_tier = next((n.get("tier") for n in nodes if n["id"] == from_id), None)
            to_tier = next((n.get("tier") for n in nodes if n["id"] == to_id), None)

            from_ref = f"{from_tier}.{from_id}" if from_tier else from_id
            to_ref = f"{to_tier}.{to_id}" if to_tier else to_id

            if label:
                lines.append(f"{from_ref} -> {to_ref}: \"{label}\"")
            else:
                lines.append(f"{from_ref} -> {to_ref}")

        return "\n".join(lines).strip()
