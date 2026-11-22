"""
PlantUML Adapter: transforms Canonical Architecture IR into PlantUML Component diagrams.
"""

from typing import Dict, Any
from .base import BaseAdapter

class PlantUMLAdapter(BaseAdapter):
    def render(self, ir: Dict[str, Any]) -> str:
        title = ir.get("title", "Architecture Diagram")
        tiers = ir.get("tiers", [])
        nodes = ir.get("nodes", [])
        edges = ir.get("edges", [])

        lines = [
            "@startuml",
            f"title {title}",
            "skinparam shadowing false",
            "skinparam roundcorner 8",
            "skinparam linetype ortho",
            "skinparam defaultFontName -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto",
            ""
        ]

        # Group by tiers
        nodes_by_tier = {t["id"]: [] for t in tiers}
        for n in nodes:
            tier_id = n.get("tier", "services")
            if tier_id in nodes_by_tier:
                nodes_by_tier[tier_id].append(n)
            else:
                nodes_by_tier.setdefault("services", []).append(n)

        # Nodes
        for tier in tiers:
            t_id = tier["id"]
            tier_nodes = nodes_by_tier.get(t_id, [])
            if not tier_nodes:
                continue

            lines.append(f'package "{tier.get("label", t_id)}" {{')
            for node in tier_nodes:
                n_id = node["id"]
                label = node.get("label", n_id)
                tech = f"\\n[{node['tech']}]" if node.get("tech") else ""
                
                if t_id == "data":
                    lines.append(f'  database "{label}{tech}" as {n_id}')
                elif t_id == "client":
                    lines.append(f'  actor "{label}{tech}" as {n_id}')
                else:
                    lines.append(f'  component "{label}{tech}" as {n_id}')
            lines.append("}")
            lines.append("")

        # Edges
        lines.append("' Connections")
        for edge in edges:
            from_id = edge["from"]
            to_id = edge["to"]
            label = edge.get("label", "")
            if label:
                lines.append(f'{from_id} --> {to_id} : "{label}"')
            else:
                lines.append(f'{from_id} --> {to_id}')

        lines.append("")
        lines.append("@enduml")
        return "\n".join(lines).strip()
