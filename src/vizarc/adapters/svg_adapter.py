"""
VizArc Standalone SVG Vector Renderer.
Generates publication-grade, self-contained SVG architecture diagrams
from Canonical Architecture IR (inspired by vizarch & Archify).
100% foolproof: embeds authentic vector SVG paths directly, with zero external network requests!
"""

from typing import Dict, Any, List, Tuple, Optional
import html
from .base import BaseAdapter
from ..services import infer_service_metadata, PROTOCOL_COLORS, PROVIDER_COLORS, VECTOR_ICONS

class SVGAdapter(BaseAdapter):
    def __init__(self, orientation: str = "horizontal"):
        self.orientation = orientation

    def render(self, ir: Dict[str, Any], orientation: Optional[str] = None) -> str:
        orient = orientation or self.orientation
        return render_svg_diagram(ir, orientation=orient)


def render_svg_diagram(ir: Dict[str, Any], orientation: str = "horizontal") -> str:
    """
    Renders Canonical IR to a standalone publication-grade SVG vector diagram.
    """
    title = ir.get("title", "System Architecture")
    summary = ir.get("summary", "")
    tiers = ir.get("tiers", [])
    nodes = ir.get("nodes", [])
    edges = ir.get("edges", [])

    if not tiers:
        detected_tiers = []
        for n in nodes:
            t = n.get("tier", "services")
            if t not in detected_tiers:
                detected_tiers.append(t)
        tier_names = {
            "client": "Client Layer",
            "gateway": "Edge & API Gateway",
            "services": "Core Services",
            "data": "Data & Storage"
        }
        tiers = [{"id": t, "label": tier_names.get(t, t.capitalize()), "color": "#3B82F6"} for t in detected_tiers]

    nodes_by_tier: Dict[str, List[Dict[str, Any]]] = {t["id"]: [] for t in tiers}
    
    for node in nodes:
        t_id = node.get("tier", "services")
        if t_id not in nodes_by_tier:
            nodes_by_tier[t_id] = []
        nodes_by_tier[t_id].append(node)

    # Geometry Constants
    NODE_WIDTH = 230
    NODE_HEIGHT = 92
    PADDING_X = 50
    PADDING_Y = 50
    HEADER_HEIGHT = 95
    FOOTER_HEIGHT = 45

    node_positions: Dict[str, Tuple[float, float]] = {}
    tier_rects: Dict[str, Tuple[float, float, float, float]] = {}

    providers_used = set()
    for n in nodes:
        meta = infer_service_metadata(n.get("label", ""), n.get("tech", ""), n.get("tier", ""))
        n["_meta"] = meta
        providers_used.add(meta["provider"])

    if orientation == "horizontal":
        # Columns = Tiers (Left to Right), Rows = Nodes in tier
        COL_GAP = 140
        ROW_GAP = 28
        
        max_rows = max([len(nlist) for nlist in nodes_by_tier.values()] or [1])
        canvas_height = max(560, HEADER_HEIGHT + max_rows * (NODE_HEIGHT + ROW_GAP) + FOOTER_HEIGHT + 50)
        
        curr_x = PADDING_X + 20
        for t in tiers:
            t_id = t["id"]
            t_nodes = nodes_by_tier.get(t_id, [])
            n_count = len(t_nodes)
            
            tier_content_h = n_count * (NODE_HEIGHT + ROW_GAP) - (ROW_GAP if n_count > 0 else 0)
            col_start_y = HEADER_HEIGHT + max(20, (canvas_height - HEADER_HEIGHT - FOOTER_HEIGHT - tier_content_h) / 2)
            
            t_x = curr_x - 16
            t_y = col_start_y - 36
            t_w = NODE_WIDTH + 32
            t_h = max(180, tier_content_h + 55)
            tier_rects[t_id] = (t_x, t_y, t_w, t_h)

            for idx, node in enumerate(t_nodes):
                n_x = curr_x
                n_y = col_start_y + idx * (NODE_HEIGHT + ROW_GAP)
                node_positions[node["id"]] = (n_x, n_y)

            curr_x += NODE_WIDTH + COL_GAP

        canvas_width = curr_x - COL_GAP + NODE_WIDTH + PADDING_X + 20
    else:
        # Vertical (TB): Rows = Tiers, Cols = Nodes in tier
        ROW_GAP = 120
        COL_GAP = 28

        max_cols = max([len(nlist) for nlist in nodes_by_tier.values()] or [1])
        canvas_width = max(820, PADDING_X * 2 + max_cols * (NODE_WIDTH + COL_GAP) + 30)
        
        curr_y = HEADER_HEIGHT + 30
        for t in tiers:
            t_id = t["id"]
            t_nodes = nodes_by_tier.get(t_id, [])
            n_count = len(t_nodes)

            tier_content_w = n_count * (NODE_WIDTH + COL_GAP) - (COL_GAP if n_count > 0 else 0)
            row_start_x = max(PADDING_X, (canvas_width - tier_content_w) / 2)

            t_x = row_start_x - 16
            t_y = curr_y - 25
            t_w = tier_content_w + 32
            t_h = NODE_HEIGHT + 45
            tier_rects[t_id] = (t_x, t_y, t_w, t_h)

            for idx, node in enumerate(t_nodes):
                n_x = row_start_x + idx * (NODE_WIDTH + COL_GAP)
                n_y = curr_y
                node_positions[node["id"]] = (n_x, n_y)

            curr_y += NODE_HEIGHT + ROW_GAP

        canvas_height = curr_y - ROW_GAP + NODE_HEIGHT + FOOTER_HEIGHT + 35

    svg_parts = []
    svg_parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {int(canvas_width)} {int(canvas_height)}" width="100%" height="100%" style="background-color: #090D16; font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, Helvetica, Arial, sans-serif;">')

    # Definitions: Blueprint Dots Pattern, Shadows, Markers
    defs = [
        '<defs>',
        '  <!-- Blueprint Dot Grid Pattern -->',
        '  <pattern id="dotGrid" width="24" height="24" patternUnits="userSpaceOnUse">',
        '    <circle cx="2" cy="2" r="1" fill="#1E293B" opacity="0.6"/>',
        '  </pattern>',
        '  <!-- Card Shadow Filter -->',
        '  <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="120%">',
        '    <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.45"/>',
        '  </filter>',
        '  <!-- Default Marker -->',
        '  <marker id="arrow-default" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">',
        '    <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#64748B"/>',
        '  </marker>'
    ]

    for proto, color in PROTOCOL_COLORS.items():
        defs.append(f'  <marker id="arrow-{proto}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">')
        defs.append(f'    <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="{color}"/>')
        defs.append('  </marker>')

    defs.append('</defs>')
    svg_parts.extend(defs)

    # 0. Blueprint Background Grid
    svg_parts.append('  <!-- Background Grid -->\n  <rect width="100%" height="100%" fill="url(#dotGrid)" />')

    # 1. Header Banner
    safe_title = html.escape(title)
    safe_summary = html.escape(summary)
    
    header_svg = f"""  <!-- Header -->
  <g id="header" transform="translate({PADDING_X}, 30)">
    <rect x="-10" y="-12" width="{int(canvas_width - PADDING_X*2 + 20)}" height="62" rx="10" fill="#0F172A" stroke="#1E293B" stroke-width="1.2"/>
    <circle cx="12" cy="18" r="8" fill="#3B82F6" opacity="0.9"/>
    <circle cx="12" cy="18" r="3.5" fill="#FFFFFF"/>
    <text x="32" y="16" fill="#F8FAFC" font-size="15" font-weight="700" letter-spacing="-0.01em">{safe_title}</text>
    <text x="32" y="33" fill="#94A3B8" font-size="10.5">{safe_summary[:115] + ('...' if len(safe_summary) > 115 else '')}</text>
    
    <!-- Meta Badges -->
    <g transform="translate({int(canvas_width - PADDING_X*2 - 180)}, 8)">
      <rect x="0" y="0" width="80" height="22" rx="11" fill="#1E293B" stroke="#334155" stroke-width="1"/>
      <text x="40" y="15" fill="#38BDF8" font-size="9.5" font-weight="700" text-anchor="middle">{len(nodes)} NODES</text>
      
      <rect x="90" y="0" width="80" height="22" rx="11" fill="#1E293B" stroke="#334155" stroke-width="1"/>
      <text x="130" y="15" fill="#A855F7" font-size="9.5" font-weight="700" text-anchor="middle">{len(edges)} EDGES</text>
    </g>
  </g>"""
    svg_parts.append(header_svg)

    # 2. Tiers Group (Boundary Boxes)
    svg_parts.append('  <!-- Tiers -->\n  <g id="tiers">')
    for t in tiers:
        t_id = t["id"]
        if t_id not in tier_rects:
            continue
        tx, ty, tw, th = tier_rects[t_id]
        t_color = t.get("color", "#3B82F6")
        t_label = html.escape(t.get("label", t_id).upper())

        tier_box = f"""    <g id="tier-{t_id}">
      <rect x="{int(tx)}" y="{int(ty)}" width="{int(tw)}" height="{int(th)}" rx="14" fill="#0F172A" fill-opacity="0.3" stroke="{t_color}" stroke-opacity="0.25" stroke-width="1.5" stroke-dasharray="5 5"/>
      <rect x="{int(tx + 12)}" y="{int(ty - 11)}" width="{len(t_label)*7.5 + 16}" height="20" rx="5" fill="#090D16" stroke="{t_color}" stroke-opacity="0.5" stroke-width="1"/>
      <text x="{int(tx + 20)}" y="{int(ty + 3.5)}" fill="{t_color}" font-size="9.5" font-weight="700" letter-spacing="0.08em">{t_label}</text>
    </g>"""
        svg_parts.append(tier_box)
    svg_parts.append('  </g>')

    # 3. Edges Group
    svg_parts.append('  <!-- Edges / Connectors -->\n  <g id="edges">')
    for edge in edges:
        u = edge.get("from")
        v = edge.get("to")
        if u not in node_positions or v not in node_positions:
            continue

        x1, y1 = node_positions[u]
        x2, y2 = node_positions[v]
        proto = (edge.get("protocol") or "https").lower()
        color = PROTOCOL_COLORS.get(proto, "#64748B")
        marker_id = f"arrow-{proto}" if proto in PROTOCOL_COLORS else "arrow-default"
        edge_label = html.escape(edge.get("label", ""))

        if orientation == "horizontal":
            sx = x1 + NODE_WIDTH
            sy = y1 + NODE_HEIGHT / 2
            tx = x2
            ty = y2 + NODE_HEIGHT / 2

            dx = abs(tx - sx) * 0.5
            path_d = f"M {sx} {sy} C {sx + dx} {sy}, {tx - dx} {ty}, {tx} {ty}"
            mid_x = (sx + tx) / 2
            mid_y = (sy + ty) / 2
        else:
            sx = x1 + NODE_WIDTH / 2
            sy = y1 + NODE_HEIGHT
            tx = x2 + NODE_WIDTH / 2
            ty = y2

            dy = abs(ty - sy) * 0.5
            path_d = f"M {sx} {sy} C {sx} {sy + dy}, {tx} {ty - dy}, {tx} {ty}"
            mid_x = (sx + tx) / 2
            mid_y = (sy + ty) / 2

        edge_svg = f"""    <g class="edge">
      <path d="{path_d}" fill="none" stroke="{color}" stroke-width="2" stroke-opacity="0.85" marker-end="url(#{marker_id})"/>"""

        if edge_label:
            lbl_w = max(42, len(edge_label) * 5.8 + 12)
            edge_svg += f"""
      <rect x="{int(mid_x - lbl_w/2)}" y="{int(mid_y - 9)}" width="{int(lbl_w)}" height="18" rx="4" fill="#090D16" stroke="{color}" stroke-opacity="0.5" stroke-width="1"/>
      <text x="{int(mid_x)}" y="{int(mid_y + 3.5)}" fill="#E2E8F0" font-size="8.5" font-weight="600" text-anchor="middle">{edge_label}</text>"""

        edge_svg += "\n    </g>"
        svg_parts.append(edge_svg)
    svg_parts.append('  </g>')

    # 4. Nodes Group (Foolproof Inline Vector Glyphs)
    svg_parts.append('  <!-- Nodes -->\n  <g id="nodes">')
    for node in nodes:
        n_id = node.get("id")
        if n_id not in node_positions:
            continue
        nx, ny = node_positions[n_id]
        meta = node.get("_meta", infer_service_metadata(node.get("label", ""), node.get("tech", ""), node.get("tier", "")))
        
        provider = meta.get("provider", "generic").upper()
        brand_color = meta.get("brand_color", "#3B82F6")
        icon_path = meta.get("icon", VECTOR_ICONS["cube"])
        label = html.escape(node.get("label", n_id))
        tech = html.escape(node.get("tech", ""))
        desc = html.escape(node.get("description", ""))

        node_svg = f"""    <g id="node-{n_id}" transform="translate({int(nx)}, {int(ny)})" filter="url(#cardShadow)">
      <!-- Card Base -->
      <rect x="0" y="0" width="{NODE_WIDTH}" height="{NODE_HEIGHT}" rx="10" fill="#131B2E" stroke="#1E293B" stroke-width="1.5"/>
      
      <!-- Top Brand Color Stripe -->
      <path d="M 0 10 Q 0 0 10 0 L {NODE_WIDTH - 10} 0 Q {NODE_WIDTH} 0 {NODE_WIDTH} 10 L {NODE_WIDTH} 4 L 0 4 Z" fill="{brand_color}"/>
      
      <!-- Icon Container Badge -->
      <rect x="12" y="14" width="34" height="34" rx="8" fill="#1E293B" stroke="{brand_color}" stroke-opacity="0.35" stroke-width="1"/>
      <!-- Foolproof Inline SVG Vector Glyph (Never fails to render offline or in file://) -->
      <g transform="translate(17, 19) scale(0.95)">
        <svg width="24" height="24" viewBox="0 0 24 24">
          <path d="{icon_path}" fill="{brand_color}"/>
        </svg>
      </g>
      
      <!-- Provider Pill -->
      <rect x="{NODE_WIDTH - 60}" y="14" width="48" height="17" rx="8.5" fill="#090D16" stroke="{brand_color}" stroke-opacity="0.5" stroke-width="1"/>
      <text x="{NODE_WIDTH - 36}" y="25.5" fill="{brand_color}" font-size="8" font-weight="700" text-anchor="middle">{provider}</text>

      <!-- Node Title -->
      <text x="54" y="32" fill="#F8FAFC" font-size="12.5" font-weight="700">{label[:18] + ('..' if len(label) > 18 else '')}</text>
      
      <!-- Tech Stack -->
      <text x="14" y="62" fill="#38BDF8" font-size="9.5" font-weight="600">{tech[:28] + ('..' if len(tech) > 28 else '')}</text>

      <!-- Description / Role -->
      <text x="14" y="78" fill="#94A3B8" font-size="8.5">{desc[:34] + ('..' if len(desc) > 34 else '')}</text>
    </g>"""
        svg_parts.append(node_svg)
    svg_parts.append('  </g>')

    # 5. Footer with branding
    footer_y = canvas_height - 22
    providers_list = " • ".join([p.upper() for p in sorted(providers_used)])
    footer_svg = f"""  <!-- Footer -->
  <g id="footer" transform="translate({PADDING_X}, {int(footer_y)})">
    <text x="0" y="0" fill="#64748B" font-size="9.5">Generated with <tspan fill="#3B82F6" font-weight="600">VizArc</tspan> — Foolproof Vector Architecture</text>
    <text x="{int(canvas_width - PADDING_X*2)}" y="0" fill="#64748B" font-size="9.5" text-anchor="end">Stack: {providers_list}</text>
  </g>
</svg>"""
    svg_parts.append(footer_svg)

    return "\n".join(svg_parts)
