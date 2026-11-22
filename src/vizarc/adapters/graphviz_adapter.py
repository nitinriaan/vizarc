"""
Graphviz (DOT) Adapter: transforms Canonical Architecture IR into Graphviz DOT syntax.
"""

from typing import Dict, Any
from .base import BaseAdapter

class GraphvizAdapter(BaseAdapter):
    def render(self, ir: Dict[str, Any]) -> str:
        title = ir.get("title", "Architecture")
        tiers = ir.get("tiers", [])
        nodes = ir.get("nodes", [])
        edges = ir.get("edges", [])

        lines = [
            f'digraph "{title.replace(" ", "_")}" {{',
            '  rankdir=TB;',
            '  compound=true;',
            '  newrank=true;',
            '  node [shape=box, style="rounded,filled", fontname="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto", fontsize=11, fillcolor="#F8FAFC", color="#CBD5E1", penwidth=1.5];',
            '  edge [color="#64748B", fontname="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto", fontsize=9, fontcolor="#475569"];',
            ''
        ]

        # Group by tiers
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

            color = tier.get("color", "#64748B")
            lines.append(f'  subgraph cluster_{t_id} {{')
            lines.append(f'    label = "{tier.get("label", t_id)}";')
            lines.append('    style = "dashed,rounded";')
            lines.append(f'    color = "{color}";')
            lines.append(f'    fontcolor = "{color}";')
            lines.append('    fontname = "Helvetica-Bold";')
            lines.append('    fontsize = 12;')
            lines.append('    margin = 16;')

            for node in tier_nodes:
                n_id = node["id"]
                label = node.get("label", n_id)
                tech = f'\\n[{node["tech"]}]' if node.get("tech") else ""
                shape = "cylinder" if t_id == "data" else ("ellipse" if t_id == "client" else "box")
                lines.append(f'    {n_id} [label="{label}{tech}", shape={shape}];')

            lines.append('  }')
            lines.append('')

        lines.append('  # Edges')
        for edge in edges:
            from_id = edge["from"]
            to_id = edge["to"]
            label = edge.get("label", "")
            if label:
                lines.append(f'  {from_id} -> {to_id} [label=" {label} "];')
            else:
                lines.append(f'  {from_id} -> {to_id};')

        lines.append('}')
        return "\n".join(lines).strip()
