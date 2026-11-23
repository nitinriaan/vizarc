"""
Structurizr DSL (C4 Model) Adapter: transforms Canonical Architecture IR into Structurizr C4 DSL.
Full integration with official Structurizr Themes (https://playground.structurizr.com/themes).
Applies official cloud provider tags and imports theme assets for AWS, Azure, GCP, and Kubernetes.
"""

from typing import Dict, Any, Set
from .base import BaseAdapter
from ..services import infer_service_metadata, STRUCTURIZR_THEMES

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

        # Separate client/actors from internal system containers
        client_nodes = [n for n in nodes if n.get("tier") == "client"]
        system_nodes = [n for n in nodes if n.get("tier") != "client"]

        providers_used: Set[str] = set()

        # 1. Actors / People & External Clients
        for client in client_nodes:
            c_id = client["id"]
            label = client.get("label", c_id)
            desc = client.get("description", "")
            meta = infer_service_metadata(label, client.get("tech", ""), "client")
            tag = meta.get("structurizr_tag", "Web Browser")
            
            # If it's a person/user, treat as person; otherwise as client container
            if any(term in label.lower() for term in ["user", "customer", "admin", "actor", "person"]):
                lines.append(f'        {c_id} = person "{label}" "{desc}"')
            else:
                lines.append(f'        {c_id} = softwareSystem "{label}" "{desc}" "{tag}"')
            
            if meta.get("provider") and meta["provider"] != "generic":
                providers_used.add(meta["provider"])

        # 2. Software System & Containers
        lines.append('        enterprise "Core Platform" {')
        lines.append('            system = softwareSystem "System Architecture" {')

        for node in system_nodes:
            n_id = node["id"]
            label = node.get("label", n_id)
            tech = node.get("tech", "Service")
            desc = node.get("description", "")
            tier = node.get("tier", "services")
            
            meta = infer_service_metadata(label, tech, tier)
            tag = meta.get("structurizr_tag", "Microservice")
            
            if meta.get("provider") and meta["provider"] != "generic":
                providers_used.add(meta["provider"])

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

        # 4. Views & Structurizr Themes Integration
        # Themes from https://playground.structurizr.com/themes
        lines.append('    views {')
        lines.append('        container system "Containers" {')
        lines.append('            include *')
        lines.append('            autolayout lr')
        lines.append('        }')
        lines.append('')
        lines.append('        # Structurizr Themes (https://playground.structurizr.com/themes)')
        lines.append('        theme default')

        # Inject themes corresponding to the cloud providers detected
        theme_urls = []
        # If no specific provider detected, default to AWS theme for rich iconography
        active_providers = providers_used if providers_used else {"aws"}
        for prov in sorted(active_providers):
            if prov in STRUCTURIZR_THEMES:
                theme_urls.append(f'"{STRUCTURIZR_THEMES[prov]}"')

        if theme_urls:
            lines.append(f'        themes {" ".join(theme_urls)}')

        lines.append('    }')
        lines.append('}')

        return "\n".join(lines).strip()
