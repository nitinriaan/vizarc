"""
VizArc Standalone Interactive Architecture Canvas Compiler.
Compiles Canonical Architecture IR into a publication-grade, zero-dependency,
double-clickable interactive vector canvas (inspired by Archify & Mermaid Live).
100% foolproof: embeds authentic vector SVG path glyphs directly with zero external network requests!
Features Dynamic Workflow Route Tracing with Live Node State Updates:
- 📐 Pure Interactive Canvas: SVG canvas, pan/zoom, flow motion, dynamic node updates, minimap.
- ⚡ Live Flow Route Player: Dynamically updates what each node is sending, receiving, and processing at each phase.
- 🔍 Node Inspector Drawer: Upstream/downstream dependency breakdown & participating lifecycle steps.
"""

import json
from typing import Dict, Any
from .services import infer_service_metadata, PROTOCOL_COLORS, PROVIDER_COLORS, VECTOR_ICONS
from .logo_data import LOGO_LIGHT_URI, LOGO_DARK_URI, FAVICON_URI

def compile_to_html(ir: Dict[str, Any]) -> str:
    """
    Takes an Architecture IR and produces a self-contained, publication-grade interactive canvas HTML file.
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
  <link rel="icon" type="image/png" href="{FAVICON_URI}">
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
      --card-bg: rgba(19, 27, 46, 0.7);
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
      --node-border: #E2E8F0;
      --edge-stroke: #94A3B8;
      --edge-active: #2563EB;
      --badge-bg: #EFF6FF;
      --card-bg: rgba(255, 255, 255, 0.95);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      -webkit-font-smoothing: antialiased;
    }}

    html, body {{
      width: 100vw;
      height: 100vh;
      overflow: hidden;
      background-color: var(--bg);
      color: var(--text-main);
      user-select: none;
    }}

    /* Top Navigation Bar */
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
      padding: 0 18px;
      z-index: 50;
    }}

    .brand {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .brand-logo-link {{
      display: flex;
      align-items: center;
      text-decoration: none;
    }}
    .brand-logo-img {{
      height: 32px;
      width: auto;
      max-width: 160px;
      object-fit: contain;
      display: block;
    }}
    body[data-theme="dark"] .brand-logo-img.logo-light {{
      display: none !important;
    }}
    body[data-theme="dark"] .brand-logo-img.logo-dark {{
      display: block !important;
    }}
    body[data-theme="light"] .brand-logo-img.logo-dark {{
      display: none !important;
    }}
    body[data-theme="light"] .brand-logo-img.logo-light {{
      display: block !important;
    }}
    .version-tag {{
      font-size: 0.68rem;
      font-weight: 700;
      color: var(--accent);
      background: var(--badge-bg);
      padding: 2px 6px;
      border-radius: 4px;
      border: 1px solid var(--surface-border);
      text-transform: uppercase;
    }}
    .doc-title {{
      font-size: 0.92rem;
      font-weight: 700;
      color: var(--text-main);
    }}
    .doc-summary {{
      font-size: 0.74rem;
      color: var(--text-muted);
      max-width: 420px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    /* Right Controls */
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
      font-size: 0.8rem;
      color: var(--text-main);
      width: 170px;
      outline: none;
      transition: all 0.2s;
    }}
    .search-box:focus {{
      border-color: var(--accent);
      width: 220px;
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
      gap: 5px;
      transition: all 0.15s ease;
    }}
    .btn:hover {{
      background: var(--badge-bg);
      border-color: var(--accent);
    }}
    .btn.active-toggle {{
      background: var(--accent);
      color: #FFFFFF;
      border-color: var(--accent);
    }}

    /* Main Canvas Viewport */
    #canvas-view {{
      position: absolute;
      top: 58px;
      bottom: 0;
      left: 0;
      right: 0;
      width: 100vw;
      height: calc(100vh - 58px);
      overflow: hidden;
      background-color: var(--bg);
    }}

    #viewport {{
      width: 100%;
      height: 100%;
      cursor: grab;
      overflow: hidden;
      background-color: var(--bg);
      background-image: 
        radial-gradient(var(--surface-border) 1px, transparent 1px);
      background-size: 24px 24px;
    }}
    #viewport.dragging {{
      cursor: grabbing;
    }}
    #diagram-canvas {{
      width: 100%;
      height: 100%;
      display: block;
    }}

    /* Tiers / Swimlanes */
    .tier-rect {{
      fill: var(--card-bg);
      stroke: var(--surface-border);
      stroke-width: 1;
      stroke-dasharray: 4 4;
      rx: 12;
      transition: all 0.2s ease;
    }}
    .tier-label {{
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      fill: var(--text-muted);
    }}

    /* Node Cards */
    .node-group {{
      cursor: pointer;
      transition: transform 0.18s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.25s ease;
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
      font-weight: 750;
      fill: var(--text-main);
      letter-spacing: -0.01em;
    }}
    .node-tech {{
      font-size: 9.5px;
      font-weight: 600;
      fill: #38BDF8;
      transition: fill 0.2s ease;
    }}
    .node-desc {{
      font-size: 8.5px;
      fill: var(--text-muted);
      transition: fill 0.2s ease;
    }}

    /* Dynamic Node States during Flow Tracing */
    .node-group.is-selected .node-rect {{
      stroke: #00C8F2 !important;
      stroke-width: 2.8;
      filter: drop-shadow(0 0 22px rgba(0, 200, 242, 0.65));
      animation: pulseGlowCyan 2s infinite;
    }}
    .node-group.is-downstream .node-rect {{
      stroke: #10B981 !important;
      stroke-width: 2.8;
      filter: drop-shadow(0 0 22px rgba(16, 185, 129, 0.65));
      animation: pulseGlowGreen 2s infinite;
    }}
    .node-group.is-upstream .node-rect {{
      stroke: #60A5FA !important;
      stroke-width: 2.2;
      filter: drop-shadow(0 0 14px rgba(96, 165, 250, 0.45));
    }}
    .node-group.is-dimmed {{
      opacity: 0.14;
    }}

    @keyframes pulseGlowCyan {{
      0% {{ filter: drop-shadow(0 0 14px rgba(0, 200, 242, 0.45)); }}
      50% {{ filter: drop-shadow(0 0 26px rgba(0, 200, 242, 0.85)); }}
      100% {{ filter: drop-shadow(0 0 14px rgba(0, 200, 242, 0.45)); }}
    }}
    @keyframes pulseGlowGreen {{
      0% {{ filter: drop-shadow(0 0 14px rgba(16, 185, 129, 0.45)); }}
      50% {{ filter: drop-shadow(0 0 26px rgba(16, 185, 129, 0.85)); }}
      100% {{ filter: drop-shadow(0 0 14px rgba(16, 185, 129, 0.45)); }}
    }}

    /* Edges */
    .edge-path {{
      fill: none;
      stroke-width: 2;
      transition: all 0.25s ease;
    }}
    .edge-path.flow-active {{
      stroke-dasharray: 6 6;
      animation: flowDash 1.2s linear infinite;
    }}
    @keyframes flowDash {{
      from {{ stroke-dashoffset: 24; }}
      to {{ stroke-dashoffset: 0; }}
    }}

    .edge-path.is-active {{
      stroke: var(--edge-active) !important;
      stroke-width: 3.5;
      filter: drop-shadow(0 0 12px var(--accent-glow));
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

    /* Floating Dock */
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

    /* MiniMap */
    #minimap-card {{
      position: absolute;
      bottom: 24px;
      right: 24px;
      width: 190px;
      height: 125px;
      background: var(--surface);
      border: 1px solid var(--surface-border);
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 8px 24px rgba(0,0,0,0.4);
      z-index: 25;
      display: flex;
      flex-direction: column;
    }}
    .minimap-header {{
      padding: 4px 8px;
      font-size: 0.65rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      border-bottom: 1px solid var(--surface-border);
      display: flex;
      justify-content: space-between;
    }}
    #minimap-canvas {{
      flex: 1;
      width: 100%;
      height: 100%;
    }}
    .minimap-viewport-rect {{
      fill: rgba(59, 130, 246, 0.15);
      stroke: var(--accent);
      stroke-width: 1.2;
    }}

    /* Floating Workflow Route Player (Archify Workflow Standard) */
    .flow-player-dock {{
      position: absolute;
      bottom: 24px;
      left: 50%;
      transform: translateX(-50%);
      background: var(--surface);
      border: 1px solid var(--surface-border);
      border-radius: 30px;
      padding: 4px 8px;
      display: flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.45);
      z-index: 30;
      backdrop-filter: blur(10px);
    }}
    .player-btn {{
      background: transparent;
      border: none;
      color: var(--text-main);
      padding: 6px 10px;
      border-radius: 20px;
      font-size: 0.8rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 4px;
      transition: all 0.15s ease;
    }}
    .player-btn:hover {{
      background: var(--badge-bg);
      color: var(--accent);
    }}
    .player-btn.player-play {{
      background: var(--accent);
      color: #FFFFFF;
      padding: 6px 14px;
    }}
    .player-btn.player-play:hover {{
      filter: brightness(1.1);
    }}
    .player-info {{
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 0 8px;
      font-size: 0.8rem;
      border-left: 1px solid var(--surface-border);
      border-right: 1px solid var(--surface-border);
    }}
    .player-badge {{
      font-size: 0.65rem;
      font-weight: 800;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      padding: 2px 6px;
      border-radius: 4px;
      background: rgba(59, 130, 246, 0.2);
      color: #38BDF8;
    }}
    .player-step-desc {{
      color: var(--text-muted);
      font-size: 0.76rem;
      max-width: 320px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    /* Side Inspector Drawer */
    #drawer {{
      position: absolute;
      top: 58px;
      right: -360px;
      width: 360px;
      bottom: 0;
      background: var(--surface);
      border-left: 1px solid var(--surface-border);
      box-shadow: -8px 0 28px rgba(0,0,0,0.45);
      transition: right 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      z-index: 40;
      display: flex;
      flex-direction: column;
      padding: 20px;
      overflow-y: auto;
    }}
    #drawer.open {{
      right: 0;
    }}
    .drawer-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 18px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--surface-border);
    }}
    .drawer-title {{
      font-size: 1.15rem;
      font-weight: 750;
      color: var(--text-main);
    }}
    .drawer-badge {{
      font-size: 0.7rem;
      font-weight: 700;
      color: var(--accent);
      background: var(--badge-bg);
      padding: 2px 6px;
      border-radius: 4px;
      display: inline-block;
      margin-bottom: 6px;
    }}
    .drawer-close {{
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 1.3rem;
      cursor: pointer;
      line-height: 1;
    }}
    .drawer-close:hover {{
      color: var(--text-main);
    }}
    .drawer-section {{
      margin-bottom: 16px;
    }}
    .drawer-label {{
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      margin-bottom: 6px;
    }}
    .drawer-text {{
      font-size: 0.85rem;
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
      transition: border-color 0.15s ease;
    }}
    .connection-pill:hover {{
      border-color: var(--accent);
    }}
    .flow-step-pill {{
      display: flex;
      flex-direction: column;
      gap: 3px;
      padding: 8px 10px;
      background: var(--bg);
      border: 1px solid var(--surface-border);
      border-radius: 6px;
      font-size: 0.8rem;
      margin-bottom: 6px;
      cursor: pointer;
      transition: all 0.15s ease;
    }}
    .flow-step-pill:hover {{
      border-color: var(--accent);
      background: var(--badge-bg);
    }}

    /* Dual-View Switcher & One-Page Explainer */
    .view-switcher {{
      display: inline-flex;
      background: var(--bg);
      border: 1px solid var(--surface-border);
      border-radius: 8px;
      padding: 2px;
      gap: 2px;
    }}
    .view-tab {{
      border: none;
      background: transparent;
      color: var(--text-muted);
      font-size: 0.75rem;
      font-weight: 700;
      padding: 5px 10px;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.15s ease;
    }}
    .view-tab.active {{
      background: var(--accent);
      color: #FFFFFF;
    }}
    #story-caption-bar {{
      position: absolute;
      top: 16px;
      left: 50%;
      transform: translateX(-50%);
      max-width: min(720px, 88vw);
      background: rgba(15, 23, 42, 0.92);
      backdrop-filter: blur(12px);
      border: 1px solid var(--accent);
      border-radius: 10px;
      padding: 10px 16px;
      z-index: 32;
      display: none;
      box-shadow: 0 10px 28px rgba(0,0,0,0.45);
    }}
    [data-theme="light"] #story-caption-bar {{
      background: rgba(255, 255, 255, 0.95);
    }}
    .story-caption-title {{
      font-size: 0.82rem;
      font-weight: 750;
      color: var(--accent);
      margin-bottom: 2px;
    }}
    .story-caption-body {{
      font-size: 0.78rem;
      color: var(--text-main);
      line-height: 1.4;
    }}
    #explainer-view {{
      position: absolute;
      top: 58px;
      bottom: 0;
      left: 0;
      right: 0;
      overflow-y: auto;
      background: var(--bg);
      padding: 28px 24px 60px;
      user-select: text;
    }}
    .exp-container {{
      max-width: 1080px;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      gap: 24px;
    }}
    .exp-hero {{
      background: var(--surface);
      border: 1px solid var(--surface-border);
      border-radius: 14px;
      padding: 24px;
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 20px;
      flex-wrap: wrap;
    }}
    .exp-hero h1 {{
      font-size: 1.55rem;
      font-weight: 800;
      margin: 6px 0 8px;
      color: var(--text-main);
    }}
    .exp-hero p {{
      font-size: 0.95rem;
      line-height: 1.6;
      color: var(--text-muted);
      max-width: 720px;
    }}
    .exp-stats {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }}
    .exp-stat {{
      background: var(--bg);
      border: 1px solid var(--surface-border);
      border-radius: 10px;
      padding: 10px 14px;
      min-width: 86px;
      text-align: center;
    }}
    .exp-stat-num {{
      font-size: 1.25rem;
      font-weight: 800;
      color: var(--accent);
    }}
    .exp-stat-lbl {{
      font-size: 0.68rem;
      text-transform: uppercase;
      color: var(--text-muted);
      font-weight: 700;
    }}
    .exp-section-title {{
      font-size: 1.05rem;
      font-weight: 750;
      color: var(--text-main);
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .exp-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 14px;
    }}
    .exp-card {{
      background: var(--surface);
      border: 1px solid var(--surface-border);
      border-radius: 12px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    .exp-card-head {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 8px;
    }}
    .exp-pill {{
      font-size: 0.68rem;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 999px;
      background: var(--badge-bg);
      color: var(--accent);
      border: 1px solid var(--surface-border);
    }}
    .exp-table {{
      width: 100%;
      border-collapse: collapse;
      background: var(--surface);
      border: 1px solid var(--surface-border);
      border-radius: 12px;
      overflow: hidden;
      font-size: 0.84rem;
    }}
    .exp-table th, .exp-table td {{
      padding: 10px 14px;
      border-bottom: 1px solid var(--surface-border);
      text-align: left;
    }}
    .exp-table th {{
      font-size: 0.72rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      background: var(--bg);
    }}
    .file-tag {{
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      font-size: 0.72rem;
      background: var(--bg);
      border: 1px solid var(--surface-border);
      border-radius: 4px;
      padding: 2px 6px;
      color: var(--text-muted);
      display: inline-block;
      margin: 2px 4px 2px 0;
    }}
    @media print {{
      html, body {{ overflow: visible !important; height: auto !important; background: #FFFFFF !important; color: #0F172A !important; }}
      header, #canvas-view {{ display: none !important; }}
      #explainer-view {{ display: block !important; position: static !important; padding: 0 !important; background: #FFFFFF !important; }}
      .exp-card, .exp-hero, .exp-table {{ break-inside: avoid; border-color: #CBD5E1 !important; background: #FFFFFF !important; }}
    }}
  </style>
</head>
<body data-theme="dark">

  <!-- Top Navigation Header -->
  <header>
    <div class="brand">
      <a href="https://github.com/nitinriaan/vizarc" target="_blank" rel="noopener" class="brand-logo-link" title="VizArc - Architecture, Visualized">
        <img class="brand-logo-img logo-dark" src="{LOGO_DARK_URI}" alt="VizArc" />
        <img class="brand-logo-img logo-light" src="{LOGO_LIGHT_URI}" alt="VizArc" />
      </a>
      <div class="view-switcher" role="tablist" aria-label="View Mode">
        <button class="view-tab active" id="tab-canvas" title="Diagram Canvas (Key: 1)">📐 Canvas</button>
        <button class="view-tab" id="tab-explainer" title="One-Page Architectural Explainer (Key: 2)">📄 Explainer</button>
      </div>
      <div>
        <div class="doc-title">{ir.get('title', 'Architecture Canvas')}</div>
        <div class="doc-summary" title="{ir.get('summary', '')}">{ir.get('summary', '')}</div>
      </div>
    </div>

    <!-- Right Controls -->
    <div class="controls">
      <button class="btn active-toggle" id="motion-btn" title="Toggle Flow Motion Animation (Key: M)">⚡ Motion</button>
      <input type="text" id="search-input" class="search-box" placeholder="🔍 Search (/)" />
      <button class="btn" id="theme-btn" title="Toggle Dark/Light Theme (Key: D)">🌓 Theme</button>
      <button class="btn" id="export-svg-btn" title="Download standalone SVG">📥 SVG</button>
      <button class="btn" id="export-png-btn" title="Export High-Res PNG">🖼️ PNG</button>
      <button class="btn" id="export-video-btn" title="Record & download animated Story Video (.webm)">🎥 Story</button>
      <button class="btn" id="print-btn" title="Print / Export One-Page PDF (Ctrl+P)">🖨️ PDF</button>
      <button class="btn" id="fullscreen-btn" title="Toggle Fullscreen (Key: F)">⛶</button>
    </div>
  </header>

  <!-- ==========================================
       MAIN INTERACTIVE DIAGRAM CANVAS
       ========================================== -->
  <div id="canvas-view">
    <div id="viewport">
      <svg id="diagram-canvas">
        <defs>
          <marker id="arrow-default" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="var(--edge-stroke)" />
          </marker>
          <marker id="arrow-active" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="var(--edge-active)" />
          </marker>
        </defs>
        <g id="scene-root">
          <g id="tiers-layer"></g>
          <g id="edges-layer"></g>
          <g id="nodes-layer"></g>
        </g>
      </svg>
    </div>

    <!-- Floating Dock -->
    <div class="floating-dock">
      <button class="dock-btn" id="zoom-in-btn" title="Zoom In">+</button>
      <button class="dock-btn" id="zoom-out-btn" title="Zoom Out">-</button>
      <button class="dock-btn" id="reset-btn" title="Fit to View (Key: R)">⛶ Fit</button>
      <button class="dock-btn" id="orient-btn" title="Toggle Orientation (Key: O)">↔️ Flip</button>
      <button class="dock-btn" id="dock-motion-btn" title="Toggle Flow Animation">⚡ Motion</button>
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

    <!-- Story Mode Narrative Caption -->
    <div id="story-caption-bar">
      <div class="story-caption-title" id="story-caption-title"></div>
      <div class="story-caption-body" id="story-caption-body"></div>
    </div>

    <!-- Floating Workflow Route Player (Archify Workflow Standard) -->
    <div id="flow-player-dock" class="flow-player-dock">
      <button class="player-btn" id="player-prev-btn" title="Previous Phase (Left Arrow)">◀</button>
      <div class="player-info" id="player-info-pill">
        <span class="player-badge">WORKFLOW TRACE</span>
        <span id="player-step-label">Step 1 / {len(ir.get('flow_steps', []))}</span>
        <span id="player-step-desc" class="player-step-desc">Click ▶ to trace route</span>
      </div>
      <button class="player-btn" id="player-next-btn" title="Next Phase (Right Arrow / Space)">▶</button>
      <button class="player-btn player-play" id="player-play-btn" title="Auto-Play Route Animation">▶ Auto</button>
      <button class="player-btn" id="player-reset-btn" title="Clear Trace (Esc)">✕</button>
    </div>

    <!-- Side Inspector Drawer -->
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

      <div class="drawer-section" id="d-flow-section" style="display: none;">
        <div class="drawer-label">Participating Flow Steps</div>
        <div id="d-flow-steps"></div>
      </div>

      <div class="drawer-section" id="d-files-section" style="display: none;">
        <div class="drawer-label">Source Files</div>
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
  </div>

  <!-- ==========================================
       ONE-PAGE ARCHITECTURAL EXPLAINER VIEW
       ========================================== -->
  <section id="explainer-view" style="display: none;">
    <div class="exp-container" id="explainer-root"></div>
  </section>

  <script>
    const IR = {ir_json_str};

    let currentOrientation = "horizontal";
    let isFlowMotionActive = true;
    const NODE_WIDTH = 240;
    const NODE_HEIGHT = 98;

    const PROTOCOL_COLORS = {json.dumps(PROTOCOL_COLORS)};
    const nodePositions = {{}};
    const nodesMap = {{}};
    (IR.nodes || []).forEach(n => nodesMap[n.id] = n);

    const scene = document.getElementById("scene-root");
    const tiersLayer = document.getElementById("tiers-layer");
    const edgesLayer = document.getElementById("edges-layer");
    const nodesLayer = document.getElementById("nodes-layer");

    const tiersOrder = (IR.tiers || []).map(t => t.id);
    const nodesByTier = {{}};
    tiersOrder.forEach(t => nodesByTier[t] = []);

    (IR.nodes || []).forEach(n => {{
      const t = nodesByTier[n.tier] ? n.tier : tiersOrder[0];
      if (nodesByTier[t]) nodesByTier[t].push(n);
    }});

    // ==========================================
    // LAYOUT ENGINE (Horizontal LR & Vertical TB)
    // ==========================================
    function calculateLayout() {{
      const tierPositions = {{}};
      const COL_GAP = 90;
      const ROW_GAP = 32;
      const PADDING = 28;

      if (currentOrientation === "horizontal") {{
        let currX = 50;
        let maxRows = 1;
        tiersOrder.forEach(t => {{
          const count = (nodesByTier[t] || []).length;
          if (count > maxRows) maxRows = count;
        }});

        const totalHeight = maxRows * (NODE_HEIGHT + ROW_GAP);

        tiersOrder.forEach(tierId => {{
          const tNodes = nodesByTier[tierId] || [];
          if (!tNodes.length) return;

          const nH = tNodes.length * (NODE_HEIGHT + ROW_GAP) - (ROW_GAP ? ROW_GAP : 0);
          const startY = 60 + Math.max(0, (totalHeight - nH) / 2);

          tierPositions[tierId] = {{ x: currX - PADDING, y: 30, width: NODE_WIDTH + PADDING*2, height: totalHeight + PADDING*2 + 40 }};

          tNodes.forEach((node, idx) => {{
            const x = currX;
            const y = startY + idx * (NODE_HEIGHT + ROW_GAP);
            nodePositions[node.id] = {{ x, y, width: NODE_WIDTH, height: NODE_HEIGHT }};
          }});

          currX += NODE_WIDTH + COL_GAP;
        }});
      }} else {{
        let currY = 50;
        let maxCols = 1;
        tiersOrder.forEach(t => {{
          const count = (nodesByTier[t] || []).length;
          if (count > maxCols) maxCols = count;
        }});

        const totalWidth = maxCols * (NODE_WIDTH + COL_GAP);

        tiersOrder.forEach(tierId => {{
          const tNodes = nodesByTier[tierId] || [];
          if (!tNodes.length) return;

          const nW = tNodes.length * (NODE_WIDTH + COL_GAP) - (COL_GAP ? COL_GAP : 0);
          const startX = 60 + Math.max(0, (totalWidth - nW) / 2);

          tierPositions[tierId] = {{ x: 30, y: currY - PADDING, width: totalWidth + PADDING*2 + 40, height: NODE_HEIGHT + PADDING*2 + 30 }};

          tNodes.forEach((node, idx) => {{
            const x = startX + idx * (NODE_WIDTH + COL_GAP);
            const y = currY;
            nodePositions[node.id] = {{ x, y, width: NODE_WIDTH, height: NODE_HEIGHT }};
          }});

          currY += NODE_HEIGHT + ROW_GAP + 24;
        }});
      }}

      return {{ tierPositions }};
    }}

    // ==========================================
    // RENDER SCENE WITH DYNAMIC NODE STATUS BARS
    // ==========================================
    function renderScene() {{
      tiersLayer.innerHTML = "";
      edgesLayer.innerHTML = "";
      nodesLayer.innerHTML = "";

      const {{ tierPositions }} = calculateLayout();

      // 1. Tiers
      tiersOrder.forEach(tId => {{
        const pos = tierPositions[tId];
        if (!pos) return;

        const tierObj = (IR.tiers || []).find(t => t.id === tId) || {{ label: tId }};
        const g = document.createElementNS("http://www.w3.org/2000/svg", "g");

        const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        rect.setAttribute("class", "tier-rect");
        rect.setAttribute("x", pos.x);
        rect.setAttribute("y", pos.y);
        rect.setAttribute("width", pos.width);
        rect.setAttribute("height", pos.height);

        const lbl = document.createElementNS("http://www.w3.org/2000/svg", "text");
        lbl.setAttribute("class", "tier-label");
        lbl.setAttribute("x", pos.x + 16);
        lbl.setAttribute("y", pos.y + 22);
        lbl.textContent = tierObj.label;

        g.appendChild(rect);
        g.appendChild(lbl);
        tiersLayer.appendChild(g);
      }});

      // 2. Edges
      (IR.edges || []).forEach(edge => {{
        const p1 = nodePositions[edge.from];
        const p2 = nodePositions[edge.to];
        if (!p1 || !p2) return;

        let x1, y1, x2, y2;
        if (currentOrientation === "horizontal") {{
          x1 = p1.x + p1.width;
          y1 = p1.y + p1.height / 2;
          x2 = p2.x;
          y2 = p2.y + p2.height / 2;
        }} else {{
          x1 = p1.x + p1.width / 2;
          y1 = p1.y + p1.height;
          x2 = p2.x + p2.width / 2;
          y2 = p2.y;
        }}

        const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
        const dx = Math.abs(x2 - x1) * 0.45;
        const dy = Math.abs(y2 - y1) * 0.45;
        
        let d = "";
        if (currentOrientation === "horizontal") {{
          d = `M ${{x1}} ${{y1}} C ${{x1 + dx}} ${{y1}}, ${{x2 - dx}} ${{y2}}, ${{x2}} ${{y2}}`;
        }} else {{
          d = `M ${{x1}} ${{y1}} C ${{x1}} ${{y1 + dy}}, ${{x2}} ${{y2 - dy}}, ${{x2}} ${{y2}}`;
        }}

        const strokeColor = PROTOCOL_COLORS[(edge.protocol || "").toUpperCase()] || "var(--edge-stroke)";
        path.setAttribute("d", d);
        path.setAttribute("class", "edge-path" + (isFlowMotionActive ? " flow-active" : ""));
        path.setAttribute("id", `edge-${{edge.from}}-${{edge.to}}`);
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

      // 3. Nodes with Embedded Authentic Vector Icons & Dynamic Status Bar
      (IR.nodes || []).forEach(node => {{
        const pos = nodePositions[node.id];
        if (!pos) return;

        const meta = node._meta || {{ provider: "generic", brand_color: "#3B82F6", icon: "", service_name: "Service" }};
        const brandColor = meta.brand_color || "#3B82F6";
        const providerName = (meta.provider || "generic").toUpperCase();
        const tier = (IR.tiers || []).find(t => t.id === node.tier);
        const tierName = tier ? tier.label : (node.tier || "Service Component");

        const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
        g.setAttribute("class", "node-group");
        g.setAttribute("id", `node-${{node.id}}`);
        g.setAttribute("transform", `translate(${{pos.x}}, ${{pos.y}})`);
        g.dataset.id = node.id;
        g.dataset.width = pos.width;
        g.dataset.height = pos.height;

        // Card Base
        const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        rect.setAttribute("class", "node-rect");
        rect.setAttribute("id", `node-rect-${{node.id}}`);
        rect.setAttribute("width", pos.width);
        rect.setAttribute("height", pos.height);

        // Top Brand Stripe
        const stripe = document.createElementNS("http://www.w3.org/2000/svg", "path");
        stripe.setAttribute("d", `M 0 10 Q 0 0 10 0 L ${{pos.width - 10}} 0 Q ${{pos.width}} 0 ${{pos.width}} 10 L ${{pos.width}} 4 L 0 4 Z`);
        stripe.setAttribute("fill", brandColor);

        // Provider Badge Pill (Top Right)
        const provBg = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        provBg.setAttribute("id", `node-prov-bg-${{node.id}}`);
        provBg.setAttribute("x", pos.width - 64);
        provBg.setAttribute("y", 12);
        provBg.setAttribute("width", 52);
        provBg.setAttribute("height", 16);
        provBg.setAttribute("rx", 8);
        provBg.setAttribute("fill", "var(--bg)");
        provBg.setAttribute("stroke", brandColor);
        provBg.setAttribute("stroke-opacity", "0.5");

        const provTxt = document.createElementNS("http://www.w3.org/2000/svg", "text");
        provTxt.setAttribute("id", `node-prov-txt-${{node.id}}`);
        provTxt.setAttribute("x", pos.width - 38);
        provTxt.setAttribute("y", 23);
        provTxt.setAttribute("fill", brandColor);
        provTxt.setAttribute("font-size", "7.5px");
        provTxt.setAttribute("font-weight", "700");
        provTxt.setAttribute("text-anchor", "middle");
        provTxt.textContent = providerName;

        // Title (Archify Clean Typographic Card)
        const title = document.createElementNS("http://www.w3.org/2000/svg", "text");
        title.setAttribute("class", "node-title");
        title.setAttribute("id", `node-title-${{node.id}}`);
        title.setAttribute("x", 16);
        title.setAttribute("y", 27);
        title.textContent = node.label.length > 22 ? node.label.slice(0, 21) + '..' : node.label;

        // Tech Subtitle
        const tech = document.createElementNS("http://www.w3.org/2000/svg", "text");
        tech.setAttribute("class", "node-tech");
        tech.setAttribute("id", `node-tech-${{node.id}}`);
        tech.setAttribute("x", 16);
        tech.setAttribute("y", 43);
        const techStr = node.tech || meta.service_name || "Service";
        tech.textContent = techStr.length > 28 ? techStr.slice(0, 27) + '..' : techStr;

        // Role Description
        const desc = document.createElementNS("http://www.w3.org/2000/svg", "text");
        desc.setAttribute("class", "node-desc");
        desc.setAttribute("id", `node-desc-${{node.id}}`);
        desc.setAttribute("x", 16);
        desc.setAttribute("y", 63);
        const descStr = node.description || meta.service_name || "";
        desc.textContent = descStr.length > 38 ? descStr.slice(0, 37) + '..' : descStr;

        // Bottom Dynamic Status Bar
        const statusBg = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        statusBg.setAttribute("id", `node-status-bg-${{node.id}}`);
        statusBg.setAttribute("x", 1);
        statusBg.setAttribute("y", pos.height - 21);
        statusBg.setAttribute("width", pos.width - 2);
        statusBg.setAttribute("height", 20);
        statusBg.setAttribute("rx", 9);
        statusBg.setAttribute("fill", "rgba(255, 255, 255, 0.03)");
        statusBg.setAttribute("stroke", "var(--surface-border)");
        statusBg.setAttribute("stroke-width", "0.5");

        const statusTxt = document.createElementNS("http://www.w3.org/2000/svg", "text");
        statusTxt.setAttribute("id", `node-status-txt-${{node.id}}`);
        statusTxt.setAttribute("x", 16);
        statusTxt.setAttribute("y", pos.height - 7.5);
        statusTxt.setAttribute("fill", "var(--text-muted)");
        statusTxt.setAttribute("font-size", "8.2px");
        statusTxt.setAttribute("font-weight", "650");
        statusTxt.textContent = `📍 ${{tierName}}`;

        g.appendChild(rect);
        g.appendChild(stripe);
        g.appendChild(provBg);
        g.appendChild(provTxt);
        g.appendChild(title);
        g.appendChild(tech);
        g.appendChild(desc);
        g.appendChild(statusBg);
        g.appendChild(statusTxt);

        g.addEventListener("click", () => selectNode(node.id));
        nodesLayer.appendChild(g);
      }});

      updateMiniMap();
    }}

    // ==========================================
    // PAN & ZOOM CONTROLLER
    // ==========================================
    let scale = 0.95;
    let panX = 40;
    let panY = 30;
    let isDragging = false;
    let startX = 0;
    let startY = 0;

    const viewport = document.getElementById("viewport");
    function updateTransform() {{
      scene.setAttribute("transform", `translate(${{panX}}, ${{panY}}) scale(${{scale}})`);
      updateMiniMap();
    }}

    viewport.addEventListener("mousedown", e => {{
      if (e.target.closest(".node-group")) return;
      isDragging = true;
      startX = e.clientX - panX;
      startY = e.clientY - panY;
      viewport.classList.add("dragging");
    }});

    window.addEventListener("mousemove", e => {{
      if (!isDragging) return;
      panX = e.clientX - startX;
      panY = e.clientY - startY;
      updateTransform();
    }});

    window.addEventListener("mouseup", () => {{
      isDragging = false;
      viewport.classList.remove("dragging");
    }});

    viewport.addEventListener("wheel", e => {{
      e.preventDefault();
      const zoomFactor = 1.1;
      const mouseX = e.clientX - viewport.getBoundingClientRect().left;
      const mouseY = e.clientY - viewport.getBoundingClientRect().top;

      let newScale = e.deltaY < 0 ? scale * zoomFactor : scale / zoomFactor;
      newScale = Math.min(Math.max(0.3, newScale), 3.0);

      panX = mouseX - (mouseX - panX) * (newScale / scale);
      panY = mouseY - (mouseY - panY) * (newScale / scale);
      scale = newScale;
      updateTransform();
    }}, {{ passive: false }});

    function fitToView() {{
      const b = scene.getBBox();
      if (!b || b.width === 0 || b.height === 0) return;
      const vw = viewport.clientWidth;
      const vh = viewport.clientHeight;
      const padding = 80;

      const scaleX = (vw - padding * 2) / b.width;
      const scaleY = (vh - padding * 2) / b.height;
      scale = Math.min(Math.max(Math.min(scaleX, scaleY), 0.4), 1.6);

      panX = (vw - b.width * scale) / 2 - b.x * scale;
      panY = (vh - b.height * scale) / 2 - b.y * scale;
      updateTransform();
    }}

    document.getElementById("zoom-in-btn").onclick = () => {{ scale = Math.min(scale * 1.2, 3.0); updateTransform(); }};
    document.getElementById("zoom-out-btn").onclick = () => {{ scale = Math.max(scale / 1.2, 0.3); updateTransform(); }};
    document.getElementById("reset-btn").onclick = fitToView;
    document.getElementById("orient-btn").onclick = () => {{
      currentOrientation = currentOrientation === "horizontal" ? "vertical" : "horizontal";
      renderScene();
      fitToView();
    }};

    // ==========================================
    // MINIMAP ENGINE
    // ==========================================
    function updateMiniMap() {{
      const b = scene.getBBox();
      if (!b || b.width === 0 || b.height === 0) return;

      const mmW = 190;
      const mmH = 95;
      const s = Math.min(mmW / (b.width + 120), mmH / (b.height + 120));
      const offX = (mmW - b.width * s) / 2 - b.x * s;
      const offY = (mmH - b.height * s) / 2 - b.y * s;

      const mmElements = document.getElementById("minimap-elements");
      mmElements.innerHTML = "";

      // Mini Nodes
      (IR.nodes || []).forEach(n => {{
        const pos = nodePositions[n.id];
        if (!pos) return;
        const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        rect.setAttribute("x", pos.x * s + offX);
        rect.setAttribute("y", pos.y * s + offY);
        rect.setAttribute("width", Math.max(pos.width * s, 6));
        rect.setAttribute("height", Math.max(pos.height * s, 3));
        rect.setAttribute("rx", 2);
        rect.setAttribute("fill", "var(--accent)");
        rect.setAttribute("opacity", "0.6");
        mmElements.appendChild(rect);
      }});

      // Viewport Rectangle
      const vw = viewport.clientWidth;
      const vh = viewport.clientHeight;
      const vx = (-panX) / scale;
      const vy = (-panY) / scale;
      const vwS = vw / scale;
      const vhS = vh / scale;

      const vpRect = document.getElementById("minimap-viewport");
      vpRect.setAttribute("x", vx * s + offX);
      vpRect.setAttribute("y", vy * s + offY);
      vpRect.setAttribute("width", Math.max(vwS * s, 10));
      vpRect.setAttribute("height", Math.max(vhS * s, 8));
    }}

    // ==========================================
    // NODE INSPECTOR DRAWER WITH FLOW STEPS
    // ==========================================
    const drawer = document.getElementById("drawer");
    const dClose = document.getElementById("d-close");
    dClose.onclick = closeDrawer;

    function selectNode(selectedId) {{
      const node = nodesMap[selectedId];
      if (!node) return;

      const meta = node._meta || {{}};
      const brandColor = meta.brand_color || "#3B82F6";

      // Find incoming & outgoing edges
      const inEdges = (IR.edges || []).filter(e => e.to === selectedId);
      const outEdges = (IR.edges || []).filter(e => e.from === selectedId);
      const upIds = new Set(inEdges.map(e => e.from));
      const downIds = new Set(outEdges.map(e => e.to));

      // Update Node Text & Highlights
      (IR.nodes || []).forEach(n => {{
        const el = document.getElementById(`node-${{n.id}}`);
        if (!el) return;

        const provTxt = document.getElementById(`node-prov-txt-${{n.id}}`);
        const statusTxt = document.getElementById(`node-status-txt-${{n.id}}`);
        const statusBg = document.getElementById(`node-status-bg-${{n.id}}`);

        el.classList.remove("is-selected", "is-upstream", "is-downstream", "is-dimmed");

        if (n.id === selectedId) {{
          el.classList.add("is-selected");
          if (provTxt) provTxt.textContent = "SELECTED";
          if (statusTxt) {{
            statusTxt.textContent = `🎯 ACTIVE (${{inEdges.length}} In, ${{outEdges.length}} Out)`;
            statusTxt.setAttribute("fill", "#00C8F2");
          }}
          if (statusBg) statusBg.setAttribute("fill", "rgba(0, 200, 242, 0.18)");
        }} else if (upIds.has(n.id)) {{
          el.classList.add("is-upstream");
          if (provTxt) provTxt.textContent = "UPSTREAM";
          if (statusTxt) {{
            statusTxt.textContent = `⬅️ SENDS TO ${{node.label.slice(0, 16)}}`;
            statusTxt.setAttribute("fill", "#60A5FA");
          }}
          if (statusBg) statusBg.setAttribute("fill", "rgba(96, 165, 250, 0.15)");
        }} else if (downIds.has(n.id)) {{
          el.classList.add("is-downstream");
          if (provTxt) provTxt.textContent = "DOWNSTREAM";
          if (statusTxt) {{
            statusTxt.textContent = `➡️ RECEIVES FROM ${{node.label.slice(0, 16)}}`;
            statusTxt.setAttribute("fill", "#10B981");
          }}
          if (statusBg) statusBg.setAttribute("fill", "rgba(16, 185, 129, 0.15)");
        }} else {{
          el.classList.add("is-dimmed");
        }}
      }});

      // Edges highlighting
      document.querySelectorAll(".edge-path").forEach(el => {{
        const isConn = (el.dataset.to === selectedId || el.dataset.from === selectedId);
        el.classList.toggle("is-active", isConn);
        el.classList.toggle("is-dimmed", !isConn);
        el.setAttribute("marker-end", isConn ? "url(#arrow-active)" : "url(#arrow-default)");
      }});

      // Populate Drawer
      document.getElementById("d-badge").textContent = (meta.provider || "Service").toUpperCase();
      document.getElementById("d-title").textContent = node.label;
      document.getElementById("d-service").textContent = `${{meta.service_name || node.label}} (${{meta.provider || 'cloud'}})`;
      document.getElementById("d-structurizr").textContent = `🏷️ ${{meta.structurizr_tag || 'Element'}}`;
      document.getElementById("d-tech").textContent = node.tech || "Service Tech Stack";
      document.getElementById("d-desc").textContent = node.description || "Component responsibility in system design.";

      // Participating Flow Steps in Drawer
      const flowStepsContainer = document.getElementById("d-flow-steps");
      const flowSection = document.getElementById("d-flow-section");
      const participatingSteps = (IR.flow_steps || []).map((s, idx) => ({{ step: s, index: idx }}))
        .filter(item => item.step.from === selectedId || item.step.to === selectedId);

      if (participatingSteps.length > 0) {{
        flowSection.style.display = "block";
        flowStepsContainer.innerHTML = "";
        participatingSteps.forEach(item => {{
          const isSender = item.step.from === selectedId;
          const pill = document.createElement("div");
          pill.className = "flow-step-pill";
          pill.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span style="font-weight:700; color:${{isSender ? '#00C8F2' : '#10B981'}};">
                ${{isSender ? '📤 Send Step' : '📥 Receive Step'}} ${{item.step.step || (item.index + 1)}}
              </span>
              <span style="font-size:0.7rem; color:var(--accent);">[${{item.step.protocol || 'API'}}]</span>
            </div>
            <div style="font-size:0.78rem; color:var(--text-main); font-weight:600;">${{item.step.title || ''}}</div>
            <div style="font-size:0.72rem; color:var(--text-muted);">${{item.step.description || ''}}</div>
          `;
          pill.onclick = () => highlightFlowStep(item.index);
          flowStepsContainer.appendChild(pill);
        }});
      }} else {{
        flowSection.style.display = "none";
      }}

      // Source Files in Drawer
      const filesSec = document.getElementById("d-files-section");
      const filesBox = document.getElementById("d-files");
      if (filesSec && filesBox) {{
        const nodeFiles = Array.isArray(node.files) ? node.files.filter(Boolean) : [];
        if (nodeFiles.length > 0) {{
          filesSec.style.display = "block";
          filesBox.innerHTML = "";
          nodeFiles.forEach(fp => {{
            const tag = document.createElement("span");
            tag.className = "file-tag";
            tag.textContent = fp;
            filesBox.appendChild(tag);
          }});
        }} else {{
          filesSec.style.display = "none";
        }}
      }}

      // Upstream list
      const upContainer = document.getElementById("d-upstream");
      upContainer.innerHTML = inEdges.length ? "" : "<span style='color:var(--text-muted); font-size:0.8rem;'>No incoming calls (Ingress node)</span>";
      inEdges.forEach(e => {{
        const src = nodesMap[e.from] || {{ label: e.from }};
        const p = document.createElement("div");
        p.className = "connection-pill";
        p.innerHTML = `<span><strong>${{src.label}}</strong></span><span style="color:var(--accent); font-size:0.75rem;">[${{e.protocol || 'API'}}] ${{e.label || ''}}</span>`;
        p.onclick = () => selectNode(e.from);
        upContainer.appendChild(p);
      }});

      // Downstream list
      const downContainer = document.getElementById("d-downstream");
      downContainer.innerHTML = outEdges.length ? "" : "<span style='color:var(--text-muted); font-size:0.8rem;'>No outgoing calls (Terminal storage/sink)</span>";
      outEdges.forEach(e => {{
        const tgt = nodesMap[e.to] || {{ label: e.to }};
        const p = document.createElement("div");
        p.className = "connection-pill";
        p.innerHTML = `<span><strong>${{tgt.label}}</strong></span><span style="color:var(--accent); font-size:0.75rem;">[${{e.protocol || 'API'}}] ${{e.label || ''}}</span>`;
        p.onclick = () => selectNode(e.to);
        downContainer.appendChild(p);
      }});

      drawer.classList.add("open");
    }}

    function closeDrawer() {{
      drawer.classList.remove("open");
      resetRouteTrace();
    }}

    // ==========================================
    // DYNAMIC WORKFLOW ROUTE TRACE CONTROLLER
    // Updates what each node shows as flow changes!
    // ==========================================
    let currentStepIndex = -1;
    let autoPlayTimer = null;
    const flowSteps = IR.flow_steps || [];

    function highlightFlowStep(index) {{
      if (!flowSteps.length) return;
      if (index < 0) index = 0;
      if (index >= flowSteps.length) index = flowSteps.length - 1;
      currentStepIndex = index;

      const step = flowSteps[index];
      const stepLabel = document.getElementById("player-step-label");
      const stepDesc = document.getElementById("player-step-desc");
      if (stepLabel) stepLabel.textContent = `Phase ${{step.step || (index + 1)}} / ${{flowSteps.length}}`;
      if (stepDesc) {{
        stepDesc.textContent = `${{step.title || (step.from + ' → ' + step.to)}} [${{step.protocol || 'HTTPS'}}]`;
        stepDesc.title = step.description || "";
      }}
      const capBar = document.getElementById("story-caption-bar");
      const capTitle = document.getElementById("story-caption-title");
      const capBody = document.getElementById("story-caption-body");
      if (capBar && capTitle && capBody) {{
        capBar.style.display = "block";
        capTitle.textContent = `Step ${{step.step || (index + 1)}}/${{flowSteps.length}} · ${{step.title || (step.from + ' → ' + step.to)}} [${{step.protocol || 'HTTPS'}}]`;
        capBody.textContent = step.description || "Executing transition along active dependency edge.";
      }}

      const targetEdgeId = `edge-${{step.from}}-${{step.to}}`;
      const reverseEdgeId = `edge-${{step.to}}-${{step.from}}`;

      // Dynamically update EVERY node's visible text and status
      (IR.nodes || []).forEach(node => {{
        const el = document.getElementById(`node-${{node.id}}`);
        if (!el) return;

        const provTxt = document.getElementById(`node-prov-txt-${{node.id}}`);
        const provBg = document.getElementById(`node-prov-bg-${{node.id}}`);
        const techTxt = document.getElementById(`node-tech-${{node.id}}`);
        const descTxt = document.getElementById(`node-desc-${{node.id}}`);
        const statusBg = document.getElementById(`node-status-bg-${{node.id}}`);
        const statusTxt = document.getElementById(`node-status-txt-${{node.id}}`);

        const meta = node._meta || {{}};
        const brandColor = meta.brand_color || "#3B82F6";
        const defaultProv = (meta.provider || "generic").toUpperCase();
        const tier = (IR.tiers || []).find(t => t.id === node.tier);
        const tierName = tier ? tier.label : (node.tier || "Service");

        el.classList.remove("is-selected", "is-upstream", "is-downstream", "is-dimmed");

        if (node.id === step.from) {{
          // ⚡ SENDER NODE: Dynamically display what it is sending!
          el.classList.add("is-selected");
          if (provTxt) {{
            provTxt.textContent = `⚡ SENDER`;
            provTxt.setAttribute("fill", "#00C8F2");
          }}
          if (provBg) {{
            provBg.setAttribute("width", "54");
            provBg.setAttribute("x", el.dataset.width - 66);
            provBg.setAttribute("stroke", "#00C8F2");
            provBg.setAttribute("fill", "rgba(0, 200, 242, 0.18)");
          }}
          if (techTxt) {{
            techTxt.textContent = `📤 Sending [${{step.protocol || 'API'}}]: ${{(step.title || 'Payload').slice(0, 22)}}`;
            techTxt.setAttribute("fill", "#00C8F2");
            techTxt.setAttribute("font-weight", "750");
          }}
          if (descTxt) {{
            descTxt.textContent = (step.description || node.description || "").slice(0, 36) + '..';
            descTxt.setAttribute("fill", "var(--text-main)");
          }}
          if (statusTxt) {{
            const tgtNode = nodesMap[step.to] || {{ label: step.to }};
            statusTxt.textContent = `▶ OUTBOUND ➔ ${{tgtNode.label.slice(0, 18)}}`;
            statusTxt.setAttribute("fill", "#00C8F2");
          }}
          if (statusBg) {{
            statusBg.setAttribute("fill", "rgba(0, 200, 242, 0.2)");
            statusBg.setAttribute("stroke", "#00C8F2");
          }}
        }} else if (node.id === step.to) {{
          // 📥 RECEIVER NODE: Dynamically display what it is receiving and processing!
          el.classList.add("is-downstream");
          if (provTxt) {{
            provTxt.textContent = `📥 RECEIVER`;
            provTxt.setAttribute("fill", "#10B981");
          }}
          if (provBg) {{
            provBg.setAttribute("width", "60");
            provBg.setAttribute("x", el.dataset.width - 72);
            provBg.setAttribute("stroke", "#10B981");
            provBg.setAttribute("fill", "rgba(16, 185, 129, 0.18)");
          }}
          if (techTxt) {{
            techTxt.textContent = `📥 Ingesting [${{step.protocol || 'API'}}]: ${{(step.title || 'Processing').slice(0, 20)}}`;
            techTxt.setAttribute("fill", "#10B981");
            techTxt.setAttribute("font-weight", "750");
          }}
          if (descTxt) {{
            descTxt.textContent = (step.description || node.description || "").slice(0, 36) + '..';
            descTxt.setAttribute("fill", "var(--text-main)");
          }}
          if (statusTxt) {{
            const srcNode = nodesMap[step.from] || {{ label: step.from }};
            statusTxt.textContent = `◀ RECEIVED FROM: ${{srcNode.label.slice(0, 18)}}`;
            statusTxt.setAttribute("fill", "#10B981");
          }}
          if (statusBg) {{
            statusBg.setAttribute("fill", "rgba(16, 185, 129, 0.2)");
            statusBg.setAttribute("stroke", "#10B981");
          }}
        }} else {{
          // 💤 IDLE NODE IN THIS PHASE
          el.classList.add("is-dimmed");
          if (provTxt) {{
            provTxt.textContent = defaultProv;
            provTxt.setAttribute("fill", brandColor);
          }}
          if (provBg) {{
            provBg.setAttribute("width", "50");
            provBg.setAttribute("x", el.dataset.width - 62);
            provBg.setAttribute("stroke", brandColor);
            provBg.setAttribute("fill", "var(--bg)");
          }}
          if (techTxt) {{
            techTxt.textContent = (node.tech || "Service").slice(0, 25);
            techTxt.setAttribute("fill", "#38BDF8");
            techTxt.setAttribute("font-weight", "600");
          }}
          if (descTxt) {{
            descTxt.textContent = (node.description || meta.service_name || "").slice(0, 36);
            descTxt.setAttribute("fill", "var(--text-muted)");
          }}
          if (statusTxt) {{
            statusTxt.textContent = `📍 ${{tierName}} (Idle)`;
            statusTxt.setAttribute("fill", "var(--text-muted)");
          }}
          if (statusBg) {{
            statusBg.setAttribute("fill", "rgba(255, 255, 255, 0.03)");
            statusBg.setAttribute("stroke", "var(--surface-border)");
          }}
        }}
      }});

      // Edge highlighting
      document.querySelectorAll(".edge-path").forEach(el => {{
        el.classList.remove("is-active", "is-dimmed");
        if (el.id === targetEdgeId || el.id === reverseEdgeId) {{
          el.classList.add("is-active");
          el.setAttribute("marker-end", "url(#arrow-active)");
        }} else {{
          el.classList.add("is-dimmed");
          el.setAttribute("marker-end", "url(#arrow-default)");
        }}
      }});
    }}

    function resetRouteTrace() {{
      currentStepIndex = -1;
      if (autoPlayTimer) {{
        clearInterval(autoPlayTimer);
        autoPlayTimer = null;
        const playBtn = document.getElementById("player-play-btn");
        if (playBtn) {{
          playBtn.textContent = "▶ Auto";
          playBtn.classList.remove("player-play");
        }}
      }}

      const stepLabel = document.getElementById("player-step-label");
      const stepDesc = document.getElementById("player-step-desc");
      if (stepLabel) stepLabel.textContent = `Flow Steps: ${{flowSteps.length}}`;
      if (stepDesc) stepDesc.textContent = "Click ▶ or ▶ Auto to animate transaction flow";
      const capBar = document.getElementById("story-caption-bar");
      if (capBar) capBar.style.display = "none";

      // Restore all nodes to default state
      (IR.nodes || []).forEach(node => {{
        const el = document.getElementById(`node-${{node.id}}`);
        if (!el) return;
        el.classList.remove("is-selected", "is-upstream", "is-downstream", "is-dimmed");

        const provTxt = document.getElementById(`node-prov-txt-${{node.id}}`);
        const provBg = document.getElementById(`node-prov-bg-${{node.id}}`);
        const techTxt = document.getElementById(`node-tech-${{node.id}}`);
        const descTxt = document.getElementById(`node-desc-${{node.id}}`);
        const statusTxt = document.getElementById(`node-status-txt-${{node.id}}`);
        const statusBg = document.getElementById(`node-status-bg-${{node.id}}`);

        const meta = node._meta || {{}};
        const brandColor = meta.brand_color || "#3B82F6";
        const tier = (IR.tiers || []).find(t => t.id === node.tier);
        const tierName = tier ? tier.label : (node.tier || "Service Layer");

        if (provTxt) {{
          provTxt.textContent = (meta.provider || "generic").toUpperCase();
          provTxt.setAttribute("fill", brandColor);
        }}
        if (provBg) {{
          provBg.setAttribute("width", "50");
          provBg.setAttribute("x", el.dataset.width - 62);
          provBg.setAttribute("stroke", brandColor);
          provBg.setAttribute("fill", "var(--bg)");
        }}
        if (techTxt) {{
          techTxt.textContent = (node.tech || meta.service_name || "Service").slice(0, 25);
          techTxt.setAttribute("fill", "#38BDF8");
          techTxt.setAttribute("font-weight", "600");
        }}
        if (descTxt) {{
          descTxt.textContent = (node.description || meta.service_name || "").slice(0, 37);
          descTxt.setAttribute("fill", "var(--text-muted)");
        }}
        if (statusTxt) {{
          statusTxt.textContent = `📍 ${{tierName}}`;
          statusTxt.setAttribute("fill", "var(--text-muted)");
        }}
        if (statusBg) {{
          statusBg.setAttribute("fill", "rgba(255, 255, 255, 0.03)");
          statusBg.setAttribute("stroke", "var(--surface-border)");
        }}
      }});

      document.querySelectorAll(".edge-path").forEach(el => {{
        el.classList.remove("is-active", "is-dimmed");
        el.setAttribute("marker-end", "url(#arrow-default)");
      }});
    }}

    function nextStep() {{
      highlightFlowStep(currentStepIndex + 1);
    }}

    function prevStep() {{
      highlightFlowStep(currentStepIndex - 1);
    }}

    function toggleAutoPlay() {{
      const playBtn = document.getElementById("player-play-btn");
      if (autoPlayTimer) {{
        clearInterval(autoPlayTimer);
        autoPlayTimer = null;
        if (playBtn) {{
          playBtn.textContent = "▶ Auto";
          playBtn.classList.remove("player-play");
        }}
      }} else {{
        if (playBtn) {{
          playBtn.textContent = "⏸ Pause";
          playBtn.classList.add("player-play");
        }}
        if (currentStepIndex >= flowSteps.length - 1) currentStepIndex = -1;
        nextStep();
        autoPlayTimer = setInterval(() => {{
          if (currentStepIndex >= flowSteps.length - 1) {{
            toggleAutoPlay();
          }} else {{
            nextStep();
          }}
        }}, 2200);
      }}
    }}

    document.getElementById("player-next-btn").onclick = nextStep;
    document.getElementById("player-prev-btn").onclick = prevStep;
    document.getElementById("player-play-btn").onclick = toggleAutoPlay;
    document.getElementById("player-reset-btn").onclick = resetRouteTrace;

    // ==========================================
    // SEARCH & CONTROLS
    // ==========================================
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

    // Flow Motion Toggle
    function toggleFlowMotion() {{
      isFlowMotionActive = !isFlowMotionActive;
      const btn = document.getElementById("motion-btn");
      const dockBtn = document.getElementById("dock-motion-btn");
      
      btn.classList.toggle("active-toggle", isFlowMotionActive);
      dockBtn.style.color = isFlowMotionActive ? "var(--accent)" : "inherit";

      document.querySelectorAll(".edge-path").forEach(p => {{
        p.classList.toggle("flow-active", isFlowMotionActive);
      }});
    }}

    document.getElementById("motion-btn").onclick = toggleFlowMotion;
    document.getElementById("dock-motion-btn").onclick = toggleFlowMotion;

    // Dark/Light Theme Toggle
    document.getElementById("theme-btn").onclick = () => {{
      const cur = document.body.getAttribute("data-theme");
      document.body.setAttribute("data-theme", cur === "dark" ? "light" : "dark");
    }};

    // Fullscreen Toggle
    document.getElementById("fullscreen-btn").onclick = () => {{
      if (!document.fullscreenElement) {{
        document.documentElement.requestFullscreen().catch(() => {{}});
      }} else {{
        document.exitFullscreen();
      }}
    }};

    // SVG Export
    document.getElementById("export-svg-btn").onclick = () => {{
      const b = scene.getBBox();
      const pad = 40;
      const svgW = b.width + pad * 2;
      const svgH = b.height + pad * 2;
      
      const clone = document.getElementById("diagram-canvas").cloneNode(true);
      clone.setAttribute("viewBox", `${{b.x - pad}} ${{b.y - pad}} ${{svgW}} ${{svgH}}`);
      clone.setAttribute("width", svgW);
      clone.setAttribute("height", svgH);

      const blob = new Blob([clone.outerHTML], {{ type: "image/svg+xml;charset=utf-8" }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${{(IR.title || 'architecture').toLowerCase().replace(/\\s+/g, '_')}}.svg`;
      a.click();
      URL.revokeObjectURL(url);
    }};

    // High-Res PNG Export
    document.getElementById("export-png-btn").onclick = () => {{
      const b = scene.getBBox();
      const pad = 40;
      const svgW = b.width + pad * 2;
      const svgH = b.height + pad * 2;
      
      const clone = document.getElementById("diagram-canvas").cloneNode(true);
      clone.setAttribute("viewBox", `${{b.x - pad}} ${{b.y - pad}} ${{svgW}} ${{svgH}}`);
      clone.setAttribute("width", svgW);
      clone.setAttribute("height", svgH);

      const svgData = new XMLSerializer().serializeToString(clone);
      const canvas = document.createElement("canvas");
      const dpr = 2;
      canvas.width = svgW * dpr;
      canvas.height = svgH * dpr;
      const ctx = canvas.getContext("2d");
      ctx.scale(dpr, dpr);
      ctx.fillStyle = document.body.getAttribute("data-theme") === "light" ? "#F8FAFC" : "#090D16";
      ctx.fillRect(0, 0, svgW, svgH);

      const img = new Image();
      img.onload = () => {{
        ctx.drawImage(img, 0, 0);
        const a = document.createElement("a");
        a.download = `${{(IR.title || 'architecture').toLowerCase().replace(/\\s+/g, '_')}}.png`;
        a.href = canvas.toDataURL("image/png");
        a.click();
      }};
      img.src = "data:image/svg+xml;base64," + btoa(unescape(encodeURIComponent(svgData)));
    }};

    // ==========================================
    // DUAL-VIEW EXPLAINER & STORY VIDEO ENGINE
    // ==========================================
    function escapeHtml(str) {{
      return String(str ?? "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;");
    }}

    function switchView(mode) {{
      const canvasEl = document.getElementById("canvas-view");
      const expEl = document.getElementById("explainer-view");
      const tabC = document.getElementById("tab-canvas");
      const tabE = document.getElementById("tab-explainer");
      if (!canvasEl || !expEl) return;

      const showExp = mode === "explainer";
      canvasEl.style.display = showExp ? "none" : "block";
      expEl.style.display = showExp ? "block" : "none";
      if (tabC) tabC.classList.toggle("active", !showExp);
      if (tabE) tabE.classList.toggle("active", showExp);
      if (!showExp) setTimeout(fitToView, 40);
    }}

    function renderExplainer() {{
      const root = document.getElementById("explainer-root");
      if (!root) return;

      const nodes = IR.nodes || [];
      const edges = IR.edges || [];
      const tiers = IR.tiers || [];
      const decisions = IR.decisions || [];
      const steps = IR.flow_steps || [];

      const adrsHtml = decisions.length
        ? decisions.map((d, i) => `
            <div class="exp-card">
              <div class="exp-card-head">
                <strong>${{i + 1}}. ${{escapeHtml(d.decision || 'Architecture Decision')}}</strong>
                <span class="exp-pill">${{escapeHtml(d.status || 'Accepted')}}</span>
              </div>
              <div style="font-size:0.84rem; color:var(--text-main); line-height:1.5;">
                <strong>Rationale:</strong> ${{escapeHtml(d.rationale || '')}}
              </div>
              <div style="font-size:0.82rem; color:var(--text-muted); line-height:1.5;">
                <strong>Trade-offs:</strong> ${{escapeHtml(d.tradeoff || '')}}
              </div>
            </div>
          `).join("")
        : `<div class="exp-card"><span style="color:var(--text-muted);">No architectural decisions recorded in IR.</span></div>`;

      const stepperHtml = steps.length
        ? steps.map((s, idx) => `
            <div class="exp-card">
              <div class="exp-card-head">
                <strong>Step ${{s.step || (idx + 1)}}: ${{escapeHtml(s.title || (s.from + ' → ' + s.to))}}</strong>
                <span class="exp-pill">${{escapeHtml((s.protocol || 'API').toUpperCase())}}</span>
              </div>
              <div style="font-size:0.8rem; color:var(--accent); font-weight:600;">
                ${{escapeHtml((nodesMap[s.from] || {{label: s.from}}).label)}} → ${{escapeHtml((nodesMap[s.to] || {{label: s.to}}).label)}}
              </div>
              <div style="font-size:0.83rem; color:var(--text-muted); line-height:1.5;">${{escapeHtml(s.description || '')}}</div>
              <div>
                <button class="btn" onclick="inspectStepOnCanvas(${{idx}})" style="font-size:0.75rem; padding:4px 10px;">
                  📐 Inspect on Canvas →
                </button>
              </div>
            </div>
          `).join("")
        : `<div class="exp-card"><span style="color:var(--text-muted);">No flow steps defined.</span></div>`;

      const catalogHtml = nodes.map(n => {{
        const meta = n._meta || {{}};
        const files = (n.files || []).map(f => `<span class="file-tag">${{escapeHtml(f)}}</span>`).join("");
        return `
          <div class="exp-card">
            <div class="exp-card-head">
              <strong>${{escapeHtml(n.label)}}</strong>
              <span class="exp-pill">${{escapeHtml((meta.provider || n.tier || 'service').toUpperCase())}}</span>
            </div>
            <div style="font-size:0.78rem; color:#38BDF8; font-weight:600;">${{escapeHtml(n.tech || meta.service_name || '')}}</div>
            <div style="font-size:0.83rem; color:var(--text-muted); line-height:1.45;">${{escapeHtml(n.description || '')}}</div>
            ${{files ? `<div>${{files}}</div>` : ""}}
          </div>
        `;
      }}).join("");

      const matrixRows = edges.map(e => {{
        const src = (nodesMap[e.from] || {{label: e.from}}).label;
        const tgt = (nodesMap[e.to] || {{label: e.to}}).label;
        return `
          <tr>
            <td><strong>${{escapeHtml(src)}}</strong></td>
            <td><strong>${{escapeHtml(tgt)}}</strong></td>
            <td>${{escapeHtml(e.label || 'Request')}}</td>
            <td><span class="exp-pill">${{escapeHtml((e.protocol || 'HTTPS').toUpperCase())}}</span></td>
          </tr>
        `;
      }}).join("");

      root.innerHTML = `
        <div class="exp-hero">
          <div>
            <span class="exp-pill">${{escapeHtml((IR.archetype || 'architecture').toUpperCase())}} EXPLAINER</span>
            <h1>${{escapeHtml(IR.title || 'System Architecture')}}</h1>
            <p>${{escapeHtml(IR.summary || '')}}</p>
          </div>
          <div class="exp-stats">
            <div class="exp-stat"><div class="exp-stat-num">${{nodes.length}}</div><div class="exp-stat-lbl">Components</div></div>
            <div class="exp-stat"><div class="exp-stat-num">${{edges.length}}</div><div class="exp-stat-lbl">Edges</div></div>
            <div class="exp-stat"><div class="exp-stat-num">${{tiers.length}}</div><div class="exp-stat-lbl">Tiers</div></div>
            <div class="exp-stat"><div class="exp-stat-num">${{decisions.length}}</div><div class="exp-stat-lbl">ADRs</div></div>
          </div>
        </div>

        <div>
          <div class="exp-section-title">⚖️ Architecture Decisions & Trade-Offs (ADRs)</div>
          <div class="exp-grid">${{adrsHtml}}</div>
        </div>

        <div>
          <div class="exp-section-title">⚡ End-to-End Transaction Stepper</div>
          <div class="exp-grid">${{stepperHtml}}</div>
        </div>

        <div>
          <div class="exp-section-title">🧩 Component & Service Catalog</div>
          <div class="exp-grid">${{catalogHtml}}</div>
        </div>

        <div>
          <div class="exp-section-title">🔌 Communication Protocol Matrix</div>
          <table class="exp-table">
            <thead><tr><th>Source</th><th>Target</th><th>Interaction</th><th>Protocol</th></tr></thead>
            <tbody>${{matrixRows || '<tr><td colspan="4">No edges defined.</td></tr>'}}</tbody>
          </table>
        </div>
      `;
    }}

    window.inspectStepOnCanvas = (idx) => {{
      switchView("canvas");
      setTimeout(() => highlightFlowStep(idx), 60);
    }};

    document.getElementById("tab-canvas").onclick = () => switchView("canvas");
    document.getElementById("tab-explainer").onclick = () => switchView("explainer");
    document.getElementById("print-btn").onclick = () => {{
      switchView("explainer");
      setTimeout(() => window.print(), 120);
    }};

    async function recordStoryVideo() {{
      const btn = document.getElementById("export-video-btn");
      if (typeof MediaRecorder === "undefined" || !HTMLCanvasElement.prototype.captureStream) {{
        alert("Story video recording requires a modern browser with MediaRecorder & Canvas captureStream support.");
        return;
      }}
      switchView("canvas");
      fitToView();

      const W = 1280, H = 720;
      const offCanvas = document.createElement("canvas");
      offCanvas.width = W;
      offCanvas.height = H;
      const ctx = offCanvas.getContext("2d");

      const mimeType = ["video/webm;codecs=vp9", "video/webm;codecs=vp8", "video/webm"].find(t => MediaRecorder.isTypeSupported(t)) || "video/webm";
      const stream = offCanvas.captureStream(30);
      const chunks = [];
      const recorder = new MediaRecorder(stream, {{ mimeType }});
      recorder.ondataavailable = ev => {{ if (ev.data && ev.data.size > 0) chunks.push(ev.data); }};

      const donePromise = new Promise(resolve => {{
        recorder.onstop = () => {{
          const blob = new Blob(chunks, {{ type: mimeType }});
          const url = URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.href = url;
          a.download = `${{(IR.title || 'architecture').toLowerCase().replace(/\\s+/g, '_')}}_story.webm`;
          a.click();
          URL.revokeObjectURL(url);
          resolve();
        }};
      }});

      const prevLabel = btn.textContent;
      btn.textContent = "⏺ Recording...";
      btn.disabled = true;
      recorder.start(100);

      const drawFrame = (titleText, bodyText, progressRatio) => new Promise(resolve => {{
        const b = scene.getBBox();
        const pad = 40;
        const svgW = Math.max(b.width + pad * 2, 100);
        const svgH = Math.max(b.height + pad * 2, 100);
        const clone = document.getElementById("diagram-canvas").cloneNode(true);
        const cloneScene = clone.querySelector("#scene-root");
        if (cloneScene) cloneScene.removeAttribute("transform");
        clone.setAttribute("xmlns", "http://www.w3.org/2000/svg");
        clone.setAttribute("viewBox", `${{b.x - pad}} ${{b.y - pad}} ${{svgW}} ${{svgH}}`);
        clone.setAttribute("width", svgW);
        clone.setAttribute("height", svgH);

        const svgData = new XMLSerializer().serializeToString(clone);
        const img = new Image();
        img.onload = () => {{
          const isLight = document.body.getAttribute("data-theme") === "light";
          ctx.fillStyle = isLight ? "#F8FAFC" : "#090D16";
          ctx.fillRect(0, 0, W, H);

          const diagramH = H - 120;
          const fitScale = Math.min((W - 80) / svgW, (diagramH - 40) / svgH);
          const drawW = svgW * fitScale;
          const drawH = svgH * fitScale;
          ctx.drawImage(img, (W - drawW) / 2, (diagramH - drawH) / 2 + 12, drawW, drawH);

          // Lower-third narrative bar
          ctx.fillStyle = isLight ? "rgba(255,255,255,0.96)" : "rgba(15,23,42,0.95)";
          ctx.fillRect(0, H - 110, W, 110);
          ctx.fillStyle = "#3B82F6";
          ctx.fillRect(0, H - 110, Math.round(W * progressRatio), 4);
          ctx.font = "bold 20px -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif";
          ctx.fillStyle = isLight ? "#0F172A" : "#F8FAFC";
          ctx.fillText(titleText.slice(0, 95), 36, H - 68);
          ctx.font = "15px -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif";
          ctx.fillStyle = isLight ? "#475569" : "#94A3B8";
          ctx.fillText(bodyText.slice(0, 130), 36, H - 36);
          resolve();
        }};
        img.onerror = () => resolve();
        img.src = "data:image/svg+xml;base64," + btoa(unescape(encodeURIComponent(svgData)));
      }});

      try {{
        resetRouteTrace();
        await drawFrame(IR.title || "Architecture Story", IR.summary || "System overview", 0.05);
        await new Promise(r => setTimeout(r, 1100));

        const total = flowSteps.length;
        for (let i = 0; i < total; i++) {{
          highlightFlowStep(i);
          const s = flowSteps[i];
          await drawFrame(
            `Step ${{s.step || (i + 1)}}/${{total}}: ${{s.title || (s.from + ' → ' + s.to)}} [${{s.protocol || 'API'}}]`,
            s.description || "",
            (i + 1) / Math.max(total, 1)
          );
          await new Promise(r => setTimeout(r, 1300));
        }}
      }} finally {{
        recorder.stop();
        await donePromise;
        resetRouteTrace();
        btn.textContent = prevLabel;
        btn.disabled = false;
      }}
    }}

    document.getElementById("export-video-btn").onclick = recordStoryVideo;

    // ==========================================
    // KEYBOARD SHORTCUTS
    // ==========================================
    window.addEventListener("keydown", e => {{
      if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA") return;
      const k = e.key.toLowerCase();
      if (k === "1") switchView("canvas");
      if (k === "2") switchView("explainer");
      if (k === "r") fitToView();
      if (k === "m") toggleFlowMotion();
      if (k === "d") document.getElementById("theme-btn").click();
      if (k === "f") document.getElementById("fullscreen-btn").click();
      if (k === "o") document.getElementById("orient-btn").click();
      if (e.key === "ArrowRight" || e.key === " ") {{ e.preventDefault(); nextStep(); }}
      if (e.key === "ArrowLeft") {{ e.preventDefault(); prevStep(); }}
      if (k === "escape") {{ closeDrawer(); resetRouteTrace(); }}
      if (k === "/") {{ e.preventDefault(); searchInput.focus(); }}
    }});

    // Initial Launch
    renderScene();
    renderExplainer();
    setTimeout(fitToView, 60);
  </script>
</body>
</html>
"""
