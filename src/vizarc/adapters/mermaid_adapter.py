"""
Mermaid Adapter: deterministically transforms Canonical Architecture IR into valid Mermaid.js flowchart.
"""

from typing import Dict, Any
from .base import BaseAdapter

class MermaidAdapter(BaseAdapter):
    def render(self, ir: Dict[str, Any]) -> str:
        tiers = ir.get("tiers", [])
        nodes = ir.get("nodes", [])
        edges = ir.get("edges", [])

        lines = ["flowchart TD"]

        # Group by tiers
        nodes_by_tier = {t["id"]: [] for t in tiers}
        for n in nodes:
            tier_id = n.get("tier", "services")
            if tier_id in nodes_by_tier:
                nodes_by_tier[tier_id].append(n)
            else:
                nodes_by_tier.setdefault("services", []).append(n)

        # Subgraphs
        for tier in tiers:
            t_id = tier["id"]
            tier_nodes = nodes_by_tier.get(t_id, [])
            if not tier_nodes:
                continue

            lines.append(f'    subgraph {t_id} ["{tier.get("label", t_id)}"]')
            for node in tier_nodes:
                n_id = node["id"]
                label = node.get("label", n_id)
                tech = f" ({node['tech']})" if node.get("tech") else ""
                
                # Shape based on tier
                if t_id == "data":
                    lines.append(f'        {n_id}[("{label}{tech}")]')
                elif t_id == "client":
                    lines.append(f'        {n_id}(["{label}{tech}"])')
                else:
                    lines.append(f'        {n_id}["{label}{tech}"]')
            lines.append("    end")

        # Connections
        for edge in edges:
            from_id = edge["from"]
            to_id = edge["to"]
            label = edge.get("label", "")
            if label:
                lines.append(f'    {from_id} -->|"{label}"| {to_id}')
            else:
                lines.append(f'    {from_id} --> {to_id}')

        return "\n".join(lines).strip()
