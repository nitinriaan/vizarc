"""
VizArc Standalone Interactive HTML Compiler.
Compiles Canonical Architecture IR into a single, zero-dependency,
double-clickable interactive architecture explainer with cloud icon glyphs,
orientation toggles, minimap, and keyboard shortcuts (inspired by vizarch & archify).
"""

import json
from typing import Dict, Any
from .services import infer_service_metadata, PROTOCOL_COLORS, PROVIDER_COLORS, ICON_PATHS

def compile_to_html(ir: Dict[str, Any]) -> str:
    """
    Takes an Architecture IR and produces a self-contained, interactive HTML file.
    """
    # Enrich nodes with cloud service metadata
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
      --bg: #0B0F19;
      --surface: #111827;
      --surface-border: #1F2937;
      --text-main: #F3F4F6;
      --text-muted: #9CA3AF;
      --accent: #3B82F6;
      --accent-glow: rgba(59, 130, 246, 0.4);
      --node-bg: #1F2937;
      --node-border: #374151;
      --edge-stroke: #4B5563;
      --edge-active: #60A5FA;
      --badge-bg: #374151;
    }}

    [data-theme="light"] {{
      --bg: #F8FAFC;
      --surface: #FFFFFF;
      --surface-border: #E2E8F0;
      --text-main: #0F172A;
      --text-muted: #64748B;
      --accent: #2563EB;
      --accent-glow: rgba(37, 99, 235, 0.2);
      --node-bg: #FFFFFF;
      --node-border: #CBD5E1;
      --edge-stroke: #94A3B8;
      --edge-active: #2563EB;
      --badge-bg: #E2E8F0;
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
      height: 60px;
      background: var(--surface);
      border-bottom: 1px solid var(--surface-border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 24px;
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
      font-weight: 600;
      color: var(--text-main);
    }}
    .doc-summary {{
      font-size: 0.78rem;
      color: var(--text-muted);
      max-width: 420px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    .controls {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .search-box {{
      background: var(--bg);
      border: 1px solid var(--surface-border);
      border-radius: 8px;
      padding: 6px 12px;
      color: var(--text-main);
      font-size: 0.85rem;
      outline: none;
      width: 200px;
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
      font-size: 0.82rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }}
    .btn:hover {{
      background: var(--badge-bg);
      border-color: var(--text-muted);
    }}

    /* Main Viewport */
    #viewport {{
      position: absolute;
      top: 60px;
      bottom: 0;
      left: 0;
      right: 0;
      cursor: grab;
      overflow: hidden;
    }}
    #viewport:active {{ cursor: grabbing; }}

    svg#diagram-canvas {{
      width: 100%;
      height: 100%;
      display: block;
    }}

    /* Graph Elements */
    .tier-box {{
      fill: none;
      stroke-dasharray: 4 4;
      stroke-width: 1.5;
      rx: 12;
    }}
    .tier-label {{
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }}

    .node-group {{
      cursor: pointer;
      transition: transform 0.15s ease, opacity 0.25s ease;
    }}
    .node-rect {{
      fill: var(--node-bg);
      stroke: var(--node-border);
      stroke-width: 1.5;
      rx: 8;
      transition: all 0.2s ease;
      filter: drop-shadow(0 4px 6px rgba(0,0,0,0.18));
    }}
    .node-group:hover .node-rect {{
      stroke: var(--accent);
      filter: drop-shadow(0 0 12px var(--accent-glow));
    }}
    .node-title {{
      font-size: 12.5px;
      font-weight: 700;
      fill: var(--text-main);
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
      stroke: var(--accent);
      stroke-width: 2.5;
      filter: drop-shadow(0 0 16px var(--accent-glow));
    }}
    .node-group.is-upstream .node-rect {{
      stroke: #10B981;
      stroke-width: 2;
      filter: drop-shadow(0 0 10px rgba(16, 185, 129, 0.4));
    }}
    .node-group.is-downstream .node-rect {{
      stroke: #F59E0B;
      stroke-width: 2;
      filter: drop-shadow(0 0 10px rgba(245, 158, 11, 0.4));
    }}
    .node-group.is-dimmed {{
      opacity: 0.15;
    }}

    /* Edges */
    .edge-path {{
      fill: none;
      stroke: var(--edge-stroke);
      stroke-width: 1.8;
      transition: all 0.25s ease;
    }}
    .edge-path.is-active {{
      stroke: var(--edge-active) !important;
      stroke-width: 2.8;
      filter: drop-shadow(0 0 8px var(--accent-glow));
    }}
    .edge-path.is-dimmed {{
      opacity: 0.08;
    }}

    .edge-label {{
      font-size: 9px;
      font-weight: 600;
      fill: var(--text-main);
      text-anchor: middle;
      pointer-events: none;
    }}
    .edge-label-bg {{
      fill: var(--surface);
      rx: 4;
      stroke-width: 1;
    }}

    /* Side Detail Drawer */
    #drawer {{
      position: absolute;
      top: 60px;
      right: -380px;
      width: 360px;
      bottom: 0;
      background: var(--surface);
      border-left: 1px solid var(--surface-border);
      padding: 24px;
      box-shadow: -8px 0 24px rgba(0,0,0,0.3);
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
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--text-main);
    }}
    .drawer-close {{
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 1.2rem;
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
      font-size: 0.75rem;
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
    .file-tag {{
      display: inline-block;
      font-family: monospace;
      font-size: 0.75rem;
      background: var(--badge-bg);
      color: var(--accent);
      padding: 3px 6px;
      border-radius: 4px;
      margin: 2px 4px 2px 0;
    }}
    .connection-pill {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 6px 10px;
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
      bottom: 20px;
      right: 20px;
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
      font-size: 9px;
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

    /* Modal Help */
    .modal-overlay {{
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0, 0, 0, 0.7);
      backdrop-filter: blur(4px);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 100;
    }}
    .modal-overlay.open {{ display: flex; }}
    .modal-card {{
      background: var(--surface);
      border: 1px solid var(--surface-border);
      border-radius: 12px;
      width: 440px;
      padding: 24px;
      box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    }}
    .modal-card h3 {{
      font-size: 1.1rem;
      margin-bottom: 12px;
      color: var(--text-main);
    }}
    .key-row {{
      display: flex;
      justify-content: space-between;
      padding: 6px 0;
      border-bottom: 1px solid var(--surface-border);
      font-size: 0.85rem;
    }}
    .kbd-key {{
      background: var(--bg);
      border: 1px solid var(--surface-border);
      padding: 2px 6px;
      border-radius: 4px;
      font-family: monospace;
      font-weight: 700;
      color: var(--accent);
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
      <button class="btn" id="orient-btn" title="Toggle Layout (O)">↔️ LR / TB</button>
      <button class="btn" id="theme-btn" title="Toggle Theme (D)">🌓 Theme</button>
      <button class="btn" id="reset-btn" title="Reset View (R)">🎯 Center</button>
      <button class="btn" id="help-btn" title="Keyboard Shortcuts (?)">❓ Keys</button>
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
        <!-- Drop Shadow Filter -->
        <filter id="shadowFilter" x="-10%" y="-10%" width="120%" height="120%">
          <feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#000" flood-opacity="0.3"/>
        </filter>
      </defs>
      <g id="scene-root">
        <g id="tiers-layer"></g>
        <g id="edges-layer"></g>
        <g id="nodes-layer"></g>
      </g>
    </svg>
  </div>

  <!-- MiniMap -->
  <div id="minimap-card">
    <div class="minimap-header">
      <span>Overview</span>
      <span id="minimap-stats">Nodes: {len(ir.get('nodes', []))}</span>
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
      <div class="drawer-text" id="d-service" style="color: var(--accent); font-weight:600;">Service Name</div>
    </div>

    <div class="drawer-section">
      <div class="drawer-label">Structurizr Theme Tag (C4)</div>
      <div class="drawer-text" id="d-structurizr" style="font-family:monospace; color:var(--accent); font-size:0.8rem;">Tag Name</div>
    </div>

    <div class="drawer-section">
      <div class="drawer-label">Tech Stack</div>
      <div class="drawer-text" id="d-tech">Node Tech</div>
    </div>

    <div class="drawer-section">
      <div class="drawer-label">Description</div>
      <div class="drawer-text" id="d-desc">Description text...</div>
    </div>

    <div class="drawer-section" id="d-files-sec">
      <div class="drawer-label">Key Source Files</div>
      <div id="d-files"></div>
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

  <!-- Keyboard Shortcuts Modal -->
  <div class="modal-overlay" id="help-modal">
    <div class="modal-card">
      <h3>⌨️ Keyboard Shortcuts</h3>
      <div class="key-row"><span>Search components</span> <span class="kbd-key">/</span></div>
      <div class="key-row"><span>Toggle Orientation (LR / TB)</span> <span class="kbd-key">O</span></div>
      <div class="key-row"><span>Toggle Dark / Light Theme</span> <span class="kbd-key">D</span></div>
      <div class="key-row"><span>Reset Zoom & Center</span> <span class="kbd-key">R</span></div>
      <div class="key-row"><span>Close drawer / modal</span> <span class="kbd-key">Esc</span></div>
      <div class="key-row"><span>Show this help menu</span> <span class="kbd-key">?</span></div>
      <div style="text-align: right; margin-top: 18px;">
        <button class="btn" id="modal-close-btn">Close</button>
      </div>
    </div>
  </div>

  <script>
    const IR = {ir_json_str};

    // Layout configuration
    let currentOrientation = "horizontal"; // "horizontal" (LR) or "vertical" (TB)
    const NODE_WIDTH = 220;
    const NODE_HEIGHT = 80;

    const PROTOCOL_COLORS = {json.dumps(PROTOCOL_COLORS)};
    const nodePositions = {{}};
    const nodesMap = {{}};
    IR.nodes.forEach(n => nodesMap[n.id] = n);

    const scene = document.getElementById("scene-root");
    const tiersLayer = document.getElementById("tiers-layer");
    const edgesLayer = document.getElementById("edges-layer");
    const nodesLayer = document.getElementById("nodes-layer");

    // Group nodes by tier
    const tiersOrder = IR.tiers.map(t => t.id);
    const nodesByTier = {{}};
    tiersOrder.forEach(t => nodesByTier[t] = []);

    IR.nodes.forEach(n => {{
      const t = nodesByTier[n.tier] ? n.tier : tiersOrder[0];
      nodesByTier[t].push(n);
    }});

    function computeLayout() {{
      // Clear positions
      Object.keys(nodePositions).forEach(k => delete nodePositions[k]);

      if (currentOrientation === "horizontal") {{
        // Columns = Tiers (LR), Rows = Nodes in tier
        const COL_GAP = 130;
        const ROW_GAP = 30;
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
        // Rows = Tiers (TB), Cols = Nodes in tier
        const ROW_GAP = 120;
        const COL_GAP = 30;
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

      // 1. Render Tier Group Boxes
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
        rect.setAttribute("stroke-opacity", "0.35");
        tiersLayer.appendChild(rect);

        const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
        text.setAttribute("class", "tier-label");
        text.setAttribute("x", minX - pad + 10);
        text.setAttribute("y", minY - pad);
        text.setAttribute("fill", tierObj ? tierObj.color : "#9CA3AF");
        text.textContent = tierObj ? tierObj.label : tId;
        tiersLayer.appendChild(text);
      }});

      // 2. Render Edges (Smooth Bezier Curves)
      IR.edges.forEach((edge) => {{
        const source = nodePositions[edge.from];
        const target = nodePositions[edge.to];
        if (!source || !target) return;

        let x1, y1, x2, y2, pathD;
        const proto = (edge.protocol || "https").toLowerCase();
        const strokeColor = PROTOCOL_COLORS[proto] || "var(--edge-stroke)";

        if (currentOrientation === "horizontal") {{
          // Exit right, enter left
          x1 = source.x + source.width;
          y1 = source.y + source.height / 2;
          x2 = target.x;
          y2 = target.y + target.height / 2;
          const dx = Math.abs(x2 - x1) * 0.5;
          pathD = `M ${{x1}} ${{y1}} C ${{x1 + dx}} ${{y1}}, ${{x2 - dx}} ${{y2}}, ${{x2}} ${{y2}}`;
        }} else {{
          // Exit bottom, enter top
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

        // Edge label badge
        if (edge.label) {{
          const midX = (x1 + x2) / 2;
          const midY = (y1 + y2) / 2;

          const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
          const bg = document.createElementNS("http://www.w3.org/2000/svg", "rect");
          const lbl = document.createElementNS("http://www.w3.org/2000/svg", "text");
          
          lbl.setAttribute("class", "edge-label");
          lbl.setAttribute("x", midX);
          lbl.setAttribute("y", midY + 3);
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

      // 3. Render Nodes with Cloud Icons & Provider Badges
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
        stripe.setAttribute("d", `M 0 6 Q 0 0 6 0 L ${{pos.width - 6}} 0 Q ${{pos.width}} 0 ${{pos.width}} 6 L ${{pos.width}} 3 L 0 3 Z`);
        stripe.setAttribute("fill", brandColor);

        // Provider Badge
        const provBg = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        provBg.setAttribute("x", pos.width - 56);
        provBg.setAttribute("y", 10);
        provBg.setAttribute("width", 46);
        provBg.setAttribute("height", 14);
        provBg.setAttribute("rx", 3);
        provBg.setAttribute("fill", "var(--bg)");
        provBg.setAttribute("stroke", brandColor);
        provBg.setAttribute("stroke-opacity", "0.6");

        const provTxt = document.createElementNS("http://www.w3.org/2000/svg", "text");
        provTxt.setAttribute("x", pos.width - 33);
        provTxt.setAttribute("y", 20);
        provTxt.setAttribute("fill", brandColor);
        provTxt.setAttribute("font-size", "7.5px");
        provTxt.setAttribute("font-weight", "700");
        provTxt.setAttribute("text-anchor", "middle");
        provTxt.textContent = providerName;

        // Structurizr Theme Icon with Vector Fallback
        if (meta.structurizr_icon) {{
          const img = document.createElementNS("http://www.w3.org/2000/svg", "image");
          img.setAttribute("x", 12);
          img.setAttribute("y", 14);
          img.setAttribute("width", 20);
          img.setAttribute("height", 20);
          img.setAttribute("href", meta.structurizr_icon);
          g.appendChild(img);
        }} else {{
          const iconSvg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
          iconSvg.setAttribute("x", 10);
          iconSvg.setAttribute("y", 12);
          iconSvg.setAttribute("width", 20);
          iconSvg.setAttribute("height", 20);
          iconSvg.setAttribute("viewBox", "0 0 24 24");
          
          const iconPath = document.createElementNS("http://www.w3.org/2000/svg", "path");
          iconPath.setAttribute("d", meta.icon || "M12 2 3 7v10l9 5 9-5V7l-9-5z");
          iconPath.setAttribute("fill", "none");
          iconPath.setAttribute("stroke", brandColor);
          iconPath.setAttribute("stroke-width", "2");
          iconPath.setAttribute("stroke-linecap", "round");
          iconPath.setAttribute("stroke-linejoin", "round");
          iconSvg.appendChild(iconPath);
          g.appendChild(iconSvg);
        }}

        // Title
        const title = document.createElementNS("http://www.w3.org/2000/svg", "text");
        title.setAttribute("class", "node-title");
        title.setAttribute("x", 36);
        title.setAttribute("y", 25);
        title.textContent = node.label.length > 17 ? node.label.slice(0, 16) + '..' : node.label;

        // Tech Subtitle
        const tech = document.createElementNS("http://www.w3.org/2000/svg", "text");
        tech.setAttribute("class", "node-tech");
        tech.setAttribute("x", 12);
        tech.setAttribute("y", 50);
        const techStr = node.tech || "Service";
        tech.textContent = techStr.length > 27 ? techStr.slice(0, 26) + '..' : techStr;

        // Role / Description
        const desc = document.createElementNS("http://www.w3.org/2000/svg", "text");
        desc.setAttribute("class", "node-desc");
        desc.setAttribute("x", 12);
        desc.setAttribute("y", 68);
        const descStr = node.description || meta.service_name || "";
        desc.textContent = descStr.length > 32 ? descStr.slice(0, 31) + '..' : descStr;

        g.appendChild(rect);
        g.appendChild(stripe);
        g.appendChild(provBg);
        g.appendChild(provTxt);
        g.appendChild(iconSvg);
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
      const mouseY = e.clientY - 60;
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
      const vpH = window.innerHeight - 60;
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

      const filesContainer = document.getElementById("d-files");
      filesContainer.innerHTML = "";
      if (node.files && node.files.length) {{
        node.files.forEach(f => {{
          const sp = document.createElement("span");
          sp.className = "file-tag";
          sp.textContent = f;
          filesContainer.appendChild(sp);
        }});
        document.getElementById("d-files-sec").style.display = "block";
      }} else {{
        document.getElementById("d-files-sec").style.display = "none";
      }}

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

    // Keyboard Shortcuts Modal
    const helpModal = document.getElementById("help-modal");
    document.getElementById("help-btn").onclick = () => helpModal.classList.add("open");
    document.getElementById("modal-close-btn").onclick = () => helpModal.classList.remove("open");
    helpModal.onclick = (e) => {{ if (e.target === helpModal) helpModal.classList.remove("open"); }};

    window.addEventListener("keydown", (e) => {{
      if (e.target === searchInput && e.key !== "Escape") return;

      if (e.key === "Escape") {{
        closeDrawer();
        helpModal.classList.remove("open");
        searchInput.blur();
      }} else if (e.key === "/") {{
        e.preventDefault();
        searchInput.focus();
      }} else if (e.key === "?" || (e.shiftKey && e.key === "/")) {{
        helpModal.classList.toggle("open");
      }} else if (e.key.toLowerCase() === "d") {{
        document.getElementById("theme-btn").click();
      }} else if (e.key.toLowerCase() === "r") {{
        document.getElementById("reset-btn").click();
      }} else if (e.key.toLowerCase() === "o") {{
        document.getElementById("orient-btn").click();
      }}
    }});

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

    // Initial render
    window.addEventListener("DOMContentLoaded", () => {{
      renderScene();
      updateTransform();
    }});
  </script>
</body>
</html>"""
