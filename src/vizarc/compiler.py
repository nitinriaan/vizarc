"""
VizArc Standalone Interactive HTML Canvas Compiler.
Compiles Canonical Architecture IR into a publication-grade, zero-dependency,
double-clickable interactive architecture explainer (inspired by Archify & Mermaid Live).
100% foolproof: embeds authentic vector SVG path glyphs directly with zero external network requests!
"""

import json
from typing import Dict, Any
from .services import infer_service_metadata, PROTOCOL_COLORS, PROVIDER_COLORS, VECTOR_ICONS

def compile_to_html(ir: Dict[str, Any]) -> str:
    """
    Takes an Architecture IR and produces a self-contained, interactive HTML file.
    """
    enriched_ir = dict(ir)
    enriched_nodes = []
    for n in ir.get("nodes", []):
        node_copy = dict(n)
        meta = infer_service_metadata(n.get("label", ""), n.get("tech", ""), n.get("tier", ""))
        node_copy["_meta"] = meta
        enriched_nodes.append(node_copy)
    enriched_ir["nodes"] = enriched_nodes

    ir_json_str = json.dumps(enriched_ir, indent=2)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{ir.get('title', 'Architecture Explainer')} — VizArc</title>
  <style>
    :root {{
      --bg: #090D16;
      --surface: #0F172A;
      --surface-border: #1E293B;
      --text-main: #F8FAFC;
      --text-muted: #94A3B8;
      --accent: #3B82F6;
      --accent-glow: rgba(59, 130, 246, 0.45);
      --node-bg: #131B2E;
      --node-border: #1E293B;
      --edge-stroke: #475569;
      --edge-active: #60A5FA;
      --badge-bg: #1E293B;
    }}

    [data-theme="light"] {{
      --bg: #F8FAFC;
      --surface: #FFFFFF;
      --surface-border: #E2E8F0;
      --text-main: #0F172A;
      --text-muted: #64748B;
      --accent: #2563EB;
      --accent-glow: rgba(37, 99, 235, 0.25);
      --node-bg: #FFFFFF;
      --node-border: #CBD5E1;
      --edge-stroke: #94A3B8;
      --edge-active: #2563EB;
      --badge-bg: #F1F5F9;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      background: var(--bg);
      color: var(--text-main);
      overflow: hidden;
      height: 100vh;
      width: 100vw;
      user-select: none;
    }}

    /* Top Bar */
    header {{
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 58px;
      background: var(--surface);
      border-bottom: 1px solid var(--surface-border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 20px;
      z-index: 20;
    }}

    .brand {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .brand-logo {{
      font-size: 1.25rem;
      font-weight: 800;
      color: var(--accent);
      display: flex;
      align-items: center;
      gap: 6px;
      letter-spacing: -0.02em;
    }}
    .doc-title {{
      font-size: 0.95rem;
      font-weight: 700;
      color: var(--text-main);
    }}
    .doc-summary {{
      font-size: 0.78rem;
      color: var(--text-muted);
      max-width: 440px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    .controls {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .search-box {{
      background: var(--bg);
      border: 1px solid var(--surface-border);
      border-radius: 6px;
      padding: 6px 12px;
      color: var(--text-main);
      font-size: 0.82rem;
      outline: none;
      width: 210px;
      transition: all 0.2s;
    }}
    .search-box:focus {{
      border-color: var(--accent);
      box-shadow: 0 0 0 2px var(--accent-glow);
    }}

    .btn {{
      background: var(--surface);
      border: 1px solid var(--surface-border);
      color: var(--text-main);
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 0.8rem;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s;
    }}
    .btn:hover {{
      background: var(--badge-bg);
      border-color: var(--accent);
    }}

    /* Main Viewport & Dot Grid */
    #viewport {{
      position: absolute;
      top: 58px;
      bottom: 0;
      left: 0;
      right: 0;
      cursor: grab;
      overflow: hidden;
      background-color: var(--bg);
      background-image: radial-gradient(rgba(255, 255, 255, 0.08) 1px, transparent 1px);
      background-size: 24px 24px;
    }}
    [data-theme="light"] #viewport {{
      background-image: radial-gradient(rgba(0, 0, 0, 0.08) 1px, transparent 1px);
    }}
    #viewport:active {{ cursor: grabbing; }}

    svg#diagram-canvas {{
      width: 100%;
      height: 100%;
      display: block;
    }}

    /* Graph Tiers */
    .tier-box {{
      fill: var(--surface);
      fill-opacity: 0.3;
      stroke-dasharray: 5 5;
      stroke-width: 1.5;
      rx: 14;
    }}
    .tier-label {{
      font-size: 10px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }}

    /* Node Cards */
    .node-group {{
      cursor: pointer;
      transition: transform 0.15s ease, opacity 0.25s ease;
    }}
    .node-rect {{
      fill: var(--node-bg);
      stroke: var(--node-border);
      stroke-width: 1.5;
      rx: 10;
      transition: all 0.2s ease;
      filter: drop-shadow(0 4px 12px rgba(0,0,0,0.3));
    }}
    .node-group:hover .node-rect {{
      stroke: var(--accent);
      filter: drop-shadow(0 0 16px var(--accent-glow));
    }}
    .node-title {{
      font-size: 12.5px;
      font-weight: 700;
      fill: var(--text-main);
      letter-spacing: -0.01em;
    }}
    .node-tech {{
      font-size: 9.5px;
      font-weight: 600;
      fill: #38BDF8;
    }}
    .node-desc {{
      font-size: 8.5px;
      fill: var(--text-muted);
    }}

    /* Path Tracing Highlights */
    .node-group.is-selected .node-rect {{
      stroke: var(--accent) !important;
      stroke-width: 2.5;
      filter: drop-shadow(0 0 20px var(--accent-glow));
    }}
    .node-group.is-upstream .node-rect {{
      stroke: #10B981 !important;
      stroke-width: 2.2;
      filter: drop-shadow(0 0 14px rgba(16, 185, 129, 0.45));
    }}
    .node-group.is-downstream .node-rect {{
      stroke: #F59E0B !important;
      stroke-width: 2.2;
      filter: drop-shadow(0 0 14px rgba(245, 158, 11, 0.45));
    }}
    .node-group.is-dimmed {{
      opacity: 0.12;
    }}

    /* Edges */
    .edge-path {{
      fill: none;
      stroke-width: 2;
      transition: all 0.25s ease;
    }}
    .edge-path.is-active {{
      stroke: var(--edge-active) !important;
      stroke-width: 3.2;
      filter: drop-shadow(0 0 10px var(--accent-glow));
    }}
    .edge-path.is-dimmed {{
      opacity: 0.08;
    }}

    .edge-label {{
      font-size: 8.5px;
      font-weight: 700;
      fill: var(--text-main);
      text-anchor: middle;
      pointer-events: none;
    }}
    .edge-label-bg {{
      fill: var(--bg);
      rx: 4;
      stroke-width: 1;
    }}

    /* Floating Navigation Controls (Bottom-Left) */
    .floating-dock {{
      position: absolute;
      bottom: 24px;
      left: 24px;
      background: var(--surface);
      border: 1px solid var(--surface-border);
      border-radius: 8px;
      padding: 4px;
      display: flex;
      gap: 4px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.4);
      z-index: 25;
    }}
    .dock-btn {{
      background: transparent;
      border: none;
      color: var(--text-main);
      font-size: 0.85rem;
      padding: 6px 10px;
      border-radius: 6px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 4px;
      transition: all 0.15s;
    }}
    .dock-btn:hover {{
      background: var(--badge-bg);
      color: var(--accent);
    }}

    /* Side Detail Drawer */
    #drawer {{
      position: absolute;
      top: 58px;
      right: -400px;
      width: 380px;
      bottom: 0;
      background: var(--surface);
      border-left: 1px solid var(--surface-border);
      padding: 24px;
      box-shadow: -10px 0 30px rgba(0,0,0,0.5);
      transition: right 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      z-index: 30;
      overflow-y: auto;
    }}
    #drawer.open {{
      right: 0;
    }}
    .drawer-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 16px;
    }}
    .drawer-title {{
      font-size: 1.2rem;
      font-weight: 700;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .drawer-close {{
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 1.3rem;
      cursor: pointer;
      padding: 4px;
    }}
    .drawer-badge {{
      display: inline-block;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 0.72rem;
      font-weight: 700;
      margin-bottom: 8px;
      text-transform: uppercase;
    }}
    .drawer-section {{
      margin-top: 18px;
    }}
    .drawer-label {{
      font-size: 0.74rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      margin-bottom: 6px;
    }}
    .drawer-text {{
      font-size: 0.9rem;
      line-height: 1.5;
      color: var(--text-main);
    }}
    .connection-pill {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 7px 10px;
      background: var(--bg);
      border: 1px solid var(--surface-border);
      border-radius: 6px;
      font-size: 0.8rem;
      margin-bottom: 6px;
      cursor: pointer;
    }}
    .connection-pill:hover {{
      border-color: var(--accent);
    }}

    /* MiniMap in Bottom-Right Corner */
    #minimap-card {{
      position: absolute;
      bottom: 24px;
      right: 24px;
      width: 170px;
      height: 110px;
      background: var(--surface);
      border: 1px solid var(--surface-border);
      border-radius: 8px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.3);
      z-index: 25;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }}
    .minimap-header {{
      font-size: 8.5px;
      font-weight: 700;
      text-transform: uppercase;
      color: var(--text-muted);
      padding: 4px 8px;
      background: var(--bg);
      border-bottom: 1px solid var(--surface-border);
      display: flex;
      justify-content: space-between;
    }}
    #minimap-canvas {{
      width: 100%;
      height: 100%;
    }}
    .minimap-node {{
      fill: var(--accent);
      opacity: 0.7;
      rx: 2;
    }}
    .minimap-viewport-rect {{
      fill: rgba(59, 130, 246, 0.15);
      stroke: var(--accent);
      stroke-width: 1;
    }}
  </style>
</head>
<body data-theme="dark">

  <header>
    <div class="brand">
      <div class="brand-logo">📐 VizArc</div>
      <div>
        <div class="doc-title">{ir.get('title', 'Architecture Diagram')}</div>
        <div class="doc-summary">{ir.get('summary', '')}</div>
      </div>
    </div>
    <div class="controls">
      <input type="text" id="search-input" class="search-box" placeholder="🔍 Search components... (/)" />
      <button class="btn" id="theme-btn" title="Toggle Theme (D)">🌓 Theme</button>
      <button class="btn" id="export-svg-btn" title="Download standalone SVG">📥 SVG</button>
    </div>
  </header>

  <div id="viewport">
    <svg id="diagram-canvas">
      <defs>
        <marker id="arrow-default" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="var(--edge-stroke)" />
        </marker>
        <marker id="arrow-active" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="var(--edge-active)" />
        </marker>
        <filter id="shadowFilter" x="-10%" y="-10%" width="120%" height="120%">
          <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000" flood-opacity="0.4"/>
        </filter>
      </defs>
      <g id="scene-root">
        <g id="tiers-layer"></g>
        <g id="edges-layer"></g>
        <g id="nodes-layer"></g>
      </g>
    </svg>
  </div>

  <!-- Floating Navigation Dock (Archify Style) -->
  <div class="floating-dock">
    <button class="dock-btn" id="zoom-in-btn" title="Zoom In">+</button>
    <button class="dock-btn" id="zoom-out-btn" title="Zoom Out">-</button>
    <button class="dock-btn" id="reset-btn" title="Fit to View">⛶ Fit</button>
    <button class="dock-btn" id="orient-btn" title="Toggle Orientation (O)">↔️ Flip</button>
  </div>

  <!-- MiniMap -->
  <div id="minimap-card">
    <div class="minimap-header">
      <span>Overview</span>
      <span id="minimap-stats">{len(ir.get('nodes', []))} Nodes</span>
    </div>
    <svg id="minimap-canvas">
      <g id="minimap-elements"></g>
      <rect id="minimap-viewport" class="minimap-viewport-rect" x="0" y="0" width="0" height="0"></rect>
    </svg>
  </div>

  <!-- Side Detail Drawer -->
  <div id="drawer">
    <div class="drawer-header">
      <div>
        <span class="drawer-badge" id="d-badge">Service</span>
        <div class="drawer-title" id="d-title">Node Title</div>
      </div>
      <button class="drawer-close" id="d-close">&times;</button>
    </div>
    
    <div class="drawer-section">
      <div class="drawer-label">Cloud Provider / Role</div>
      <div class="drawer-text" id="d-service" style="color: var(--accent); font-weight:700;">Service Name</div>
    </div>

    <div class="drawer-section">
      <div class="drawer-label">Structurizr C4 Theme Tag</div>
      <div class="drawer-text" id="d-structurizr" style="font-family:monospace; color:var(--accent); font-size:0.8rem;">🏷️ Tag</div>
    </div>

    <div class="drawer-section">
      <div class="drawer-label">Tech Stack</div>
      <div class="drawer-text" id="d-tech">Node Tech</div>
    </div>

    <div class="drawer-section">
      <div class="drawer-label">Description</div>
      <div class="drawer-text" id="d-desc">Description text...</div>
    </div>

    <div class="drawer-section">
      <div class="drawer-label">Incoming Traffic (Upstream)</div>
      <div id="d-upstream"></div>
    </div>

    <div class="drawer-section">
      <div class="drawer-label">Outgoing Calls (Downstream)</div>
      <div id="d-downstream"></div>
    </div>
  </div>

  <script>
    const IR = {ir_json_str};

    let currentOrientation = "horizontal";
    const NODE_WIDTH = 230;
    const NODE_HEIGHT = 92;

    const PROTOCOL_COLORS = {json.dumps(PROTOCOL_COLORS)};
    const nodePositions = {{}};
    const nodesMap = {{}};
    IR.nodes.forEach(n => nodesMap[n.id] = n);

    const scene = document.getElementById("scene-root");
    const tiersLayer = document.getElementById("tiers-layer");
    const edgesLayer = document.getElementById("edges-layer");
    const nodesLayer = document.getElementById("nodes-layer");

    const tiersOrder = IR.tiers.map(t => t.id);
    const nodesByTier = {{}};
    tiersOrder.forEach(t => nodesByTier[t] = []);

    IR.nodes.forEach(n => {{
      const t = nodesByTier[n.tier] ? n.tier : tiersOrder[0];
      nodesByTier[t].push(n);
    }});

    function computeLayout() {{
      Object.keys(nodePositions).forEach(k => delete nodePositions[k]);

      if (currentOrientation === "horizontal") {{
        const COL_GAP = 140;
        const ROW_GAP = 28;
        const PADDING_LEFT = 70;
        const PADDING_TOP = 80;

        let maxRows = 1;
        tiersOrder.forEach(tId => {{
          maxRows = Math.max(maxRows, nodesByTier[tId].length);
        }});
        const totalHeight = maxRows * (NODE_HEIGHT + ROW_GAP);

        let currX = PADDING_LEFT;
        tiersOrder.forEach((tId) => {{
          const tNodes = nodesByTier[tId];
          const nH = tNodes.length * (NODE_HEIGHT + ROW_GAP) - (ROW_GAP ? ROW_GAP : 0);
          const startY = PADDING_TOP + Math.max(0, (totalHeight - nH) / 2);

          tNodes.forEach((node, idx) => {{
            const x = currX;
            const y = startY + idx * (NODE_HEIGHT + ROW_GAP);
            nodePositions[node.id] = {{ x, y, width: NODE_WIDTH, height: NODE_HEIGHT }};
          }});

          currX += NODE_WIDTH + COL_GAP;
        }});
      }} else {{
        const ROW_GAP = 120;
        const COL_GAP = 28;
        const PADDING_TOP = 80;
        const PADDING_LEFT = 60;

        let maxCols = 1;
        tiersOrder.forEach(tId => {{
          maxCols = Math.max(maxCols, nodesByTier[tId].length);
        }});
        const totalWidth = maxCols * (NODE_WIDTH + COL_GAP);

        let currY = PADDING_TOP;
        tiersOrder.forEach((tId) => {{
          const tNodes = nodesByTier[tId];
          const nW = tNodes.length * (NODE_WIDTH + COL_GAP) - (COL_GAP ? COL_GAP : 0);
          const startX = PADDING_LEFT + Math.max(0, (totalWidth - nW) / 2);

          tNodes.forEach((node, idx) => {{
            const x = startX + idx * (NODE_WIDTH + COL_GAP);
            const y = currY;
            nodePositions[node.id] = {{ x, y, width: NODE_WIDTH, height: NODE_HEIGHT }};
          }});

          currY += NODE_HEIGHT + ROW_GAP;
        }});
      }}
    }}

    function renderScene() {{
      computeLayout();
      tiersLayer.innerHTML = "";
      edgesLayer.innerHTML = "";
      nodesLayer.innerHTML = "";

      // 1. Tiers
      tiersOrder.forEach((tId) => {{
        const tierObj = IR.tiers.find(t => t.id === tId);
        const tierNodes = nodesByTier[tId];
        if (!tierNodes.length) return;

        let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
        tierNodes.forEach(n => {{
          const p = nodePositions[n.id];
          if (p) {{
            minX = Math.min(minX, p.x);
            minY = Math.min(minY, p.y);
            maxX = Math.max(maxX, p.x + p.width);
            maxY = Math.max(maxY, p.y + p.height);
          }}
        }});

        const pad = 16;
        const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        rect.setAttribute("class", "tier-box");
        rect.setAttribute("x", minX - pad);
        rect.setAttribute("y", minY - pad - 16);
        rect.setAttribute("width", (maxX - minX) + pad * 2);
        rect.setAttribute("height", (maxY - minY) + pad * 2 + 20);
        rect.setAttribute("stroke", tierObj ? tierObj.color : "#4B5563");
        rect.setAttribute("stroke-opacity", "0.25");
        tiersLayer.appendChild(rect);

        const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
        text.setAttribute("class", "tier-label");
        text.setAttribute("x", minX - pad + 10);
        text.setAttribute("y", minY - pad);
        text.setAttribute("fill", tierObj ? tierObj.color : "#94A3B8");
        text.textContent = tierObj ? tierObj.label : tId;
        tiersLayer.appendChild(text);
      }});

      // 2. Edges
      IR.edges.forEach((edge) => {{
        const source = nodePositions[edge.from];
        const target = nodePositions[edge.to];
        if (!source || !target) return;

        let x1, y1, x2, y2, pathD;
        const proto = (edge.protocol || "https").lower ? (edge.protocol || "https").toLowerCase() : "https";
        const strokeColor = PROTOCOL_COLORS[proto] || "var(--edge-stroke)";

        if (currentOrientation === "horizontal") {{
          x1 = source.x + source.width;
          y1 = source.y + source.height / 2;
          x2 = target.x;
          y2 = target.y + target.height / 2;
          const dx = Math.abs(x2 - x1) * 0.5;
          pathD = `M ${{x1}} ${{y1}} C ${{x1 + dx}} ${{y1}}, ${{x2 - dx}} ${{y2}}, ${{x2}} ${{y2}}`;
        }} else {{
          x1 = source.x + source.width / 2;
          y1 = source.y + source.height;
          x2 = target.x + target.width / 2;
          y2 = target.y;
          const dy = Math.abs(y2 - y1) * 0.5;
          pathD = `M ${{x1}} ${{y1}} C ${{x1}} ${{y1 + dy}}, ${{x2}} ${{y2 - dy}}, ${{x2}} ${{y2}}`;
        }}

        const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
        path.setAttribute("id", `edge-${{edge.from}}-${{edge.to}}`);
        path.setAttribute("class", "edge-path");
        path.setAttribute("d", pathD);
        path.setAttribute("stroke", strokeColor);
        path.setAttribute("marker-end", "url(#arrow-default)");
        path.dataset.from = edge.from;
        path.dataset.to = edge.to;
        edgesLayer.appendChild(path);

        if (edge.label) {{
          const midX = (x1 + x2) / 2;
          const midY = (y1 + y2) / 2;

          const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
          const bg = document.createElementNS("http://www.w3.org/2000/svg", "rect");
          const lbl = document.createElementNS("http://www.w3.org/2000/svg", "text");
          
          lbl.setAttribute("class", "edge-label");
          lbl.setAttribute("x", midX);
          lbl.setAttribute("y", midY + 3.5);
          lbl.textContent = edge.label;

          const estWidth = edge.label.length * 5.8 + 10;
          bg.setAttribute("class", "edge-label-bg");
          bg.setAttribute("x", midX - estWidth/2);
          bg.setAttribute("y", midY - 8);
          bg.setAttribute("width", estWidth);
          bg.setAttribute("height", 16);
          bg.setAttribute("stroke", strokeColor);
          bg.setAttribute("stroke-opacity", "0.4");

          g.appendChild(bg);
          g.appendChild(lbl);
          edgesLayer.appendChild(g);
        }}
      }});

      // 3. Nodes (Foolproof Vector SVG Glyphs)
      IR.nodes.forEach(node => {{
        const pos = nodePositions[node.id];
        if (!pos) return;

        const meta = node._meta || {{ provider: "generic", brand_color: "#3B82F6", icon: "", service_name: "Service" }};
        const brandColor = meta.brand_color || "#3B82F6";
        const providerName = (meta.provider || "generic").toUpperCase();

        const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
        g.setAttribute("class", "node-group");
        g.setAttribute("id", `node-${{node.id}}`);
        g.setAttribute("transform", `translate(${{pos.x}}, ${{pos.y}})`);
        g.dataset.id = node.id;

        // Card Base
        const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        rect.setAttribute("class", "node-rect");
        rect.setAttribute("width", pos.width);
        rect.setAttribute("height", pos.height);

        // Top Stripe
        const stripe = document.createElementNS("http://www.w3.org/2000/svg", "path");
        stripe.setAttribute("d", `M 0 10 Q 0 0 10 0 L ${{pos.width - 10}} 0 Q ${{pos.width}} 0 ${{pos.width}} 10 L ${{pos.width}} 4 L 0 4 Z`);
        stripe.setAttribute("fill", brandColor);

        // Icon Container Box
        const iconBox = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        iconBox.setAttribute("x", 12);
        iconBox.setAttribute("y", 14);
        iconBox.setAttribute("width", 34);
        iconBox.setAttribute("height", 34);
        iconBox.setAttribute("rx", 8);
        iconBox.setAttribute("fill", "var(--surface)");
        iconBox.setAttribute("stroke", brandColor);
        iconBox.setAttribute("stroke-opacity", "0.35");

        // Embedded Vector SVG (100% Foolproof, Never Fails)
        const iconSvg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
        iconSvg.setAttribute("x", 17);
        iconSvg.setAttribute("y", 19);
        iconSvg.setAttribute("width", 24);
        iconSvg.setAttribute("height", 24);
        iconSvg.setAttribute("viewBox", "0 0 24 24");
        
        const iconPath = document.createElementNS("http://www.w3.org/2000/svg", "path");
        iconPath.setAttribute("d", meta.icon || "M12 2L2 7v10l10 5 10-5V7L12 2z");
        iconPath.setAttribute("fill", brandColor);
        iconSvg.appendChild(iconPath);

        // Provider Badge Pill
        const provBg = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        provBg.setAttribute("x", pos.width - 60);
        provBg.setAttribute("y", 14);
        provBg.setAttribute("width", 48);
        provBg.setAttribute("height", 17);
        provBg.setAttribute("rx", 8.5);
        provBg.setAttribute("fill", "var(--bg)");
        provBg.setAttribute("stroke", brandColor);
        provBg.setAttribute("stroke-opacity", "0.5");

        const provTxt = document.createElementNS("http://www.w3.org/2000/svg", "text");
        provTxt.setAttribute("x", pos.width - 36);
        provTxt.setAttribute("y", 25.5);
        provTxt.setAttribute("fill", brandColor);
        provTxt.setAttribute("font-size", "8px");
        provTxt.setAttribute("font-weight", "700");
        provTxt.setAttribute("text-anchor", "middle");
        provTxt.textContent = providerName;

        // Title
        const title = document.createElementNS("http://www.w3.org/2000/svg", "text");
        title.setAttribute("class", "node-title");
        title.setAttribute("x", 54);
        title.setAttribute("y", 32);
        title.textContent = node.label.length > 18 ? node.label.slice(0, 17) + '..' : node.label;

        // Tech Subtitle
        const tech = document.createElementNS("http://www.w3.org/2000/svg", "text");
        tech.setAttribute("class", "node-tech");
        tech.setAttribute("x", 14);
        tech.setAttribute("y", 62);
        const techStr = node.tech || "Service";
        tech.textContent = techStr.length > 28 ? techStr.slice(0, 27) + '..' : techStr;

        // Role / Description
        const desc = document.createElementNS("http://www.w3.org/2000/svg", "text");
        desc.setAttribute("class", "node-desc");
        desc.setAttribute("x", 14);
        desc.setAttribute("y", 78);
        const descStr = node.description || meta.service_name || "";
        desc.textContent = descStr.length > 34 ? descStr.slice(0, 33) + '..' : descStr;

        g.appendChild(rect);
        g.appendChild(stripe);
        g.appendChild(iconBox);
        g.appendChild(iconSvg);
        g.appendChild(provBg);
        g.appendChild(provTxt);
        g.appendChild(title);
        g.appendChild(tech);
        g.appendChild(desc);

        g.addEventListener("click", () => selectNode(node.id));
        nodesLayer.appendChild(g);
      }});

      updateMiniMap();
    }}

    // Pan & Zoom
    let scale = 0.95;
    let panX = 40;
    let panY = 30;
    let isDragging = false;
    let startX = 0;
    let startY = 0;

    const viewport = document.getElementById("viewport");
    function updateTransform() {{
      scene.setAttribute("transform", `translate(${{panX}}, ${{panY}}) scale(${{scale}})`);
      updateMiniMapViewport();
    }}

    viewport.addEventListener("mousedown", e => {{
      if (e.target.closest(".node-group")) return;
      isDragging = true;
      startX = e.clientX - panX;
      startY = e.clientY - panY;
    }});

    window.addEventListener("mousemove", e => {{
      if (!isDragging) return;
      panX = e.clientX - startX;
      panY = e.clientY - startY;
      updateTransform();
    }});

    window.addEventListener("mouseup", () => isDragging = false);

    viewport.addEventListener("wheel", e => {{
      e.preventDefault();
      const zoomFactor = e.deltaY < 0 ? 1.08 : 0.92;
      const newScale = Math.min(Math.max(scale * zoomFactor, 0.25), 3.0);
      
      const mouseX = e.clientX;
      const mouseY = e.clientY - 58;
      panX = mouseX - (mouseX - panX) * (newScale / scale);
      panY = mouseY - (mouseY - panY) * (newScale / scale);
      scale = newScale;
      updateTransform();
    }});

    // MiniMap
    function updateMiniMap() {{
      const miniEl = document.getElementById("minimap-elements");
      miniEl.innerHTML = "";

      let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
      Object.values(nodePositions).forEach(p => {{
        minX = Math.min(minX, p.x);
        minY = Math.min(minY, p.y);
        maxX = Math.max(maxX, p.x + p.width);
        maxY = Math.max(maxY, p.y + p.height);
      }});

      const sceneW = (maxX - minX) || 800;
      const sceneH = (maxY - minY) || 500;
      const mmW = 170;
      const mmH = 90;
      const scaleX = (mmW - 20) / sceneW;
      const scaleY = (mmH - 20) / sceneH;
      const mmScale = Math.min(scaleX, scaleY);

      Object.values(nodePositions).forEach(p => {{
        const r = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        r.setAttribute("class", "minimap-node");
        r.setAttribute("x", 10 + (p.x - minX) * mmScale);
        r.setAttribute("y", 10 + (p.y - minY) * mmScale);
        r.setAttribute("width", Math.max(4, p.width * mmScale));
        r.setAttribute("height", Math.max(3, p.height * mmScale));
        miniEl.appendChild(r);
      }});

      window._miniMeta = {{ minX, minY, mmScale }};
      updateMiniMapViewport();
    }}

    function updateMiniMapViewport() {{
      if (!window._miniMeta) return;
      const {{ minX, minY, mmScale }} = window._miniMeta;
      const vpRect = document.getElementById("minimap-viewport");
      
      const vpW = window.innerWidth;
      const vpH = window.innerHeight - 58;
      const visibleW = vpW / scale;
      const visibleH = vpH / scale;
      const visibleX = -panX / scale;
      const visibleY = -panY / scale;

      vpRect.setAttribute("x", 10 + (visibleX - minX) * mmScale);
      vpRect.setAttribute("y", 10 + (visibleY - minY) * mmScale);
      vpRect.setAttribute("width", Math.max(10, visibleW * mmScale));
      vpRect.setAttribute("height", Math.max(8, visibleH * mmScale));
    }}

    // Node Selection & Path Tracing
    function selectNode(selectedId) {{
      const allNodes = document.querySelectorAll(".node-group");
      const allEdges = document.querySelectorAll(".edge-path");

      const upstreams = new Set();
      const downstreams = new Set();
      const activeEdgeIds = new Set();

      IR.edges.forEach(e => {{
        if (e.to === selectedId) {{
          upstreams.add(e.from);
          activeEdgeIds.add(`edge-${{e.from}}-${{e.to}}`);
        }}
        if (e.from === selectedId) {{
          downstreams.add(e.to);
          activeEdgeIds.add(`edge-${{e.from}}-${{e.to}}`);
        }}
      }});

      allNodes.forEach(el => {{
        const id = el.dataset.id;
        el.classList.remove("is-selected", "is-upstream", "is-downstream", "is-dimmed");
        if (id === selectedId) {{
          el.classList.add("is-selected");
        }} else if (upstreams.has(id)) {{
          el.classList.add("is-upstream");
        }} else if (downstreams.has(id)) {{
          el.classList.add("is-downstream");
        }} else {{
          el.classList.add("is-dimmed");
        }}
      }});

      allEdges.forEach(el => {{
        el.classList.remove("is-active", "is-dimmed");
        if (activeEdgeIds.has(el.id)) {{
          el.classList.add("is-active");
          el.setAttribute("marker-end", "url(#arrow-active)");
        }} else {{
          el.classList.add("is-dimmed");
          el.setAttribute("marker-end", "url(#arrow-default)");
        }}
      }});

      openDrawer(selectedId, upstreams, downstreams);
    }}

    // Side Drawer Details
    const drawer = document.getElementById("drawer");
    function openDrawer(nodeId, upstreams, downstreams) {{
      const node = nodesMap[nodeId];
      if (!node) return;

      const meta = node._meta || {{}};
      const tierObj = IR.tiers.find(t => t.id === node.tier);
      const badge = document.getElementById("d-badge");
      badge.textContent = tierObj ? tierObj.label : node.tier;
      badge.style.background = tierObj ? tierObj.color + "22" : "#3B82F622";
      badge.style.color = tierObj ? tierObj.color : "#3B82F6";

      document.getElementById("d-title").textContent = node.label;
      document.getElementById("d-service").textContent = `${{(meta.provider || "GENERIC").toUpperCase()}} • ${{meta.service_name || node.label}}`;
      document.getElementById("d-structurizr").textContent = `🏷️ ${{meta.structurizr_tag || "Microservice"}}`;
      document.getElementById("d-tech").textContent = node.tech || "None specified";
      document.getElementById("d-desc").textContent = node.description || "No detailed description provided.";

      const upContainer = document.getElementById("d-upstream");
      upContainer.innerHTML = "";
      if (upstreams.size) {{
        upstreams.forEach(uId => {{
          const uNode = nodesMap[uId];
          const div = document.createElement("div");
          div.className = "connection-pill";
          div.innerHTML = `<span>⬆️ ${{uNode ? uNode.label : uId}}</span> <span style="font-size:0.7rem; color:var(--text-muted)">Upstream</span>`;
          div.onclick = () => selectNode(uId);
          upContainer.appendChild(div);
        }});
      }} else {{
        upContainer.innerHTML = `<span style="font-size:0.8rem; color:var(--text-muted)">None (Ingress root)</span>`;
      }}

      const downContainer = document.getElementById("d-downstream");
      downContainer.innerHTML = "";
      if (downstreams.size) {{
        downstreams.forEach(dId => {{
          const dNode = nodesMap[dId];
          const div = document.createElement("div");
          div.className = "connection-pill";
          div.innerHTML = `<span>⬇️ ${{dNode ? dNode.label : dId}}</span> <span style="font-size:0.7rem; color:var(--text-muted)">Downstream</span>`;
          div.onclick = () => selectNode(dId);
          downContainer.appendChild(div);
        }});
      }} else {{
        downContainer.innerHTML = `<span style="font-size:0.8rem; color:var(--text-muted)">None (Leaf node)</span>`;
      }}

      drawer.classList.add("open");
    }}

    function closeDrawer() {{
      drawer.classList.remove("open");
      document.querySelectorAll(".node-group").forEach(el => el.classList.remove("is-selected", "is-upstream", "is-downstream", "is-dimmed"));
      document.querySelectorAll(".edge-path").forEach(el => {{
        el.classList.remove("is-active", "is-dimmed");
        el.setAttribute("marker-end", "url(#arrow-default)");
      }});
    }}

    document.getElementById("d-close").onclick = closeDrawer;

    // Search Filtering
    const searchInput = document.getElementById("search-input");
    searchInput.addEventListener("input", e => {{
      const query = e.target.value.toLowerCase().trim();
      if (!query) {{
        document.querySelectorAll(".node-group").forEach(el => el.classList.remove("is-dimmed"));
        return;
      }}
      document.querySelectorAll(".node-group").forEach(el => {{
        const node = nodesMap[el.dataset.id];
        const match = node && (node.label.toLowerCase().includes(query) || (node.tech && node.tech.toLowerCase().includes(query)));
        el.classList.toggle("is-dimmed", !match);
      }});
    }});

    // Controls
    document.getElementById("theme-btn").onclick = () => {{
      const cur = document.body.getAttribute("data-theme");
      document.body.setAttribute("data-theme", cur === "dark" ? "light" : "dark");
    }};

    document.getElementById("orient-btn").onclick = () => {{
      currentOrientation = currentOrientation === "horizontal" ? "vertical" : "horizontal";
      renderScene();
      updateTransform();
    }};

    document.getElementById("reset-btn").onclick = () => {{
      scale = 0.95;
      panX = 40;
      panY = 30;
      updateTransform();
    }};

    document.getElementById("zoom-in-btn").onclick = () => {{
      scale = Math.min(scale * 1.2, 3.0);
      updateTransform();
    }};

    document.getElementById("zoom-out-btn").onclick = () => {{
      scale = Math.max(scale * 0.8, 0.25);
      updateTransform();
    }};

    document.getElementById("export-svg-btn").onclick = () => {{
      const svg = document.getElementById("diagram-canvas");
      const serializer = new XMLSerializer();
      const source = serializer.serializeToString(svg);
      const blob = new Blob([source], {{ type: "image/svg+xml;charset=utf-8" }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "{ir.get('title', 'architecture').lower().replace(' ', '_')}.svg";
      a.click();
    }};

    // Keyboard Shortcuts
    window.addEventListener("keydown", (e) => {{
      if (e.target === searchInput && e.key !== "Escape") return;
      if (e.key === "Escape") {{
        closeDrawer();
        searchInput.blur();
      }} else if (e.key === "/") {{
        e.preventDefault();
        searchInput.focus();
      }} else if (e.key.toLowerCase() === "d") {{
        document.getElementById("theme-btn").click();
      }} else if (e.key.toLowerCase() === "r") {{
        document.getElementById("reset-btn").click();
      }} else if (e.key.toLowerCase() === "o") {{
        document.getElementById("orient-btn").click();
      }}
    }});

    window.addEventListener("DOMContentLoaded", () => {{
      renderScene();
      updateTransform();
    }});
  </script>
</body>
</html>"""
