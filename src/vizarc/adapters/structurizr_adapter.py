"""
Structurizr DSL (C4 Model) Adapter: transforms Canonical Architecture IR into Structurizr C4 DSL.
"""

from typing import Dict, Any
from .base import BaseAdapter

class StructurizrAdapter(BaseAdapter):
    def render(self, ir: Dict[str, Any]) -> str:
        title = ir.get("title", "Software Architecture")
        summary = ir.get("summary", "System Architecture Overview")
        nodes = ir.get("nodes", [])
        edges = ir.get("edges", [])

        lines = [
            f'workspace "{title}" "{summary}" {{',
            '    model {',
        ]

        # Separate client/actors from containers
        client_nodes = [n for n in nodes if n.get("tier") == "client"]
        system_nodes = [n for n in nodes if n.get("tier") != "client"]

        # 1. Actors / People
        for client in client_nodes:
            c_id = client["id"]
            label = client.get("label", c_id)
            desc = client.get("description", "")
            lines.append(f'        {c_id} = person "{label}" "{desc}"')

        # 2. Software System & Containers
        lines.append('        enterprise "Core Platform" {')
        lines.append('            system = softwareSystem "System Services" {')

        for node in system_nodes:
            n_id = node["id"]
            label = node.get("label", n_id)
            tech = node.get("tech", "Service")
            desc = node.get("description", "")
            tag = "Database" if node.get("tier") == "data" else "Microservice"
            lines.append(f'                {n_id} = container "{label}" "{desc}" "{tech}" "{tag}"')

        lines.append('            }')
        lines.append('        }')
        lines.append('')

        # 3. Relationships
        lines.append('        # Relationships')
        for edge in edges:
            from_id = edge["from"]
            to_id = edge["to"]
            label = edge.get("label", "interacts with")
            protocol = edge.get("protocol", "")
            if protocol:
                lines.append(f'        {from_id} -> {to_id} "{label}" "{protocol}"')
            else:
                lines.append(f'        {from_id} -> {to_id} "{label}"')

        lines.append('    }')
        lines.append('')
        lines.append('    views {')
        lines.append('        container system "Containers" {')
        lines.append('            include *')
        lines.append('            autolayout lr')
        lines.append('        }')
        lines.append('        theme default')
        lines.append('    }')
        lines.append('}')

        return "\n".join(lines).strip()
