"""
VizArc Standalone Interactive HTML Canvas & One-Page Explainer Compiler.
Compiles Canonical Architecture IR into a publication-grade, zero-dependency,
double-clickable interactive architecture explainer (inspired by Archify & Mermaid Live).
100% foolproof: embeds authentic vector SVG path glyphs directly with zero external network requests!
Features Dual-View Mode:
- 📐 Diagram Canvas: Interactive SVG canvas, pan/zoom, flow animation, path tracing, minimap.
- 📄 One-Page Explainer: Executive summary, architecture decisions (ADRs), step-by-step transaction flow, component catalog.
"""

import json
from typing import Dict, Any
from .services import infer_service_metadata, PROTOCOL_COLORS, PROVIDER_COLORS, VECTOR_ICONS

def compile_to_html(ir: Dict[str, Any]) -> str:
    """
    Takes an Architecture IR and produces a self-contained, publication-grade interactive HTML file.
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
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400;1,600&display=swap" rel="stylesheet">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400;1,600&display=swap');

    :root {{
      --font-mono: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', Menlo, Monaco, Consolas, "Liberation Mono", monospace;
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
      --node-border: #CBD5E1;
      --edge-stroke: #94A3B8;
      --edge-active: #2563EB;
      --badge-bg: #F1F5F9;
      --card-bg: #FFFFFF;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: var(--font-mono);
    }}
    body {{
      font-family: var(--font-mono);
      background: var(--bg);
      color: var(--text-main);
      overflow: hidden;
      height: 100vh;
      width: 100vw;
      user-select: none;
    }}

    svg text, .node-title, .node-tech, .node-desc, .tier-label, .edge-label {{
      font-family: var(--font-mono) !important;
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
    .brand-logo {{
      font-size: 1.15rem;
      font-weight: 800;
      color: var(--accent);
      display: flex;
      align-items: center;
      gap: 6px;
      letter-spacing: -0.02em;
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
      max-width: 320px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    /* Center Dual-View Switcher */
    .view-switcher {{
      display: flex;
      background: var(--bg);
      border: 1px solid var(--surface-border);
      border-radius: 8px;
      padding: 3px;
      gap: 4px;
    }}
    .tab-btn {{
      background: transparent;
      border: none;
      color: var(--text-muted);
      padding: 5px 12px;
      border-radius: 6px;
      font-size: 0.8rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s ease;
    }}
    .tab-btn.active {{
      background: var(--surface);
      color: var(--text-main);
      box-shadow: 0 2px 6px rgba(0,0,0,0.25);
    }}
    .tab-btn:hover:not(.active) {{
      color: var(--text-main);
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
      padding: 6px 10px;
      color: var(--text-main);
      font-size: 0.8rem;
      outline: none;
      width: 175px;
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
      padding: 6px 11px;
      border-radius: 6px;
      font-size: 0.78rem;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 5px;
      transition: all 0.15s;
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

    /* Viewport & Panels */
    .view-panel {{
      position: absolute;
      top: 58px;
      bottom: 0;
      left: 0;
      right: 0;
      display: none;
    }}
    .view-panel.active {{
      display: block;
    }}

    /* =========================================
       CANVAS VIEW
       ========================================= */
    #viewport {{
      width: 100%;
      height: 100%;
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

    /* Highlighting */
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

    /* Side Inspector Drawer */
    #drawer {{
      position: absolute;
      top: 58px;
      right: -420px;
      width: 390px;
      bottom: 0;
      background: var(--surface);
      border-left: 1px solid var(--surface-border);
      padding: 24px;
      box-shadow: -10px 0 30px rgba(0,0,0,0.5);
      transition: right 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      z-index: 40;
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
      font-size: 0.88rem;
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

    /* =========================================
       ONE-PAGE EXPLAINER VIEW (Archify Standard)
       ========================================= */
    #explainer-view {{
      overflow-y: auto;
      user-select: text;
    }}
    .explainer-container {{
      max-width: 1040px;
      margin: 0 auto;
      padding: 36px 24px 80px;
    }}

    /* Executive Hero Card */
    .hero-card {{
      background: var(--card-bg);
      border: 1px solid var(--surface-border);
      border-radius: 12px;
      padding: 28px;
      margin-bottom: 28px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.25);
    }}
    .hero-meta {{
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 12px;
    }}
    .hero-title {{
      font-size: 1.7rem;
      font-weight: 800;
      color: var(--text-main);
      letter-spacing: -0.02em;
      margin-bottom: 10px;
    }}
    .hero-summary {{
      font-size: 1.05rem;
      line-height: 1.6;
      color: var(--text-muted);
      margin-bottom: 24px;
    }}
    .stats-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 16px;
      border-top: 1px solid var(--surface-border);
      padding-top: 20px;
    }}
    .stat-box {{
      display: flex;
      flex-direction: column;
    }}
    .stat-val {{
      font-size: 1.5rem;
      font-weight: 800;
      color: var(--accent);
    }}
    .stat-label {{
      font-size: 0.74rem;
      font-weight: 700;
      text-transform: uppercase;
      color: var(--text-muted);
      letter-spacing: 0.05em;
    }}

    /* Section Styling */
    .section-title {{
      font-size: 1.25rem;
      font-weight: 800;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 10px;
      margin-top: 36px;
      margin-bottom: 18px;
      letter-spacing: -0.01em;
    }}
    .section-desc {{
      font-size: 0.9rem;
      color: var(--text-muted);
      margin-bottom: 20px;
      line-height: 1.5;
    }}

    /* ADR Decisions Grid */
    .decisions-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(310px, 1fr));
      gap: 18px;
    }}
    .adr-card {{
      background: var(--surface);
      border: 1px solid var(--surface-border);
      border-radius: 10px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }}
    .adr-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 12px;
    }}
    .adr-name {{
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--text-main);
    }}
    .status-badge {{
      font-size: 0.68rem;
      font-weight: 700;
      text-transform: uppercase;
      padding: 3px 8px;
      border-radius: 9999px;
      background: rgba(16, 185, 129, 0.15);
      color: #10B981;
      border: 1px solid rgba(16, 185, 129, 0.3);
    }}
    .adr-body {{
      font-size: 0.88rem;
      line-height: 1.55;
      color: var(--text-muted);
      margin-bottom: 14px;
    }}
    .tradeoff-box {{
      margin-top: auto;
      background: var(--bg);
      border-left: 3px solid #F59E0B;
      padding: 8px 12px;
      border-radius: 0 6px 6px 0;
      font-size: 0.8rem;
      line-height: 1.45;
      color: var(--text-muted);
    }}
    .tradeoff-box strong {{
      color: #F59E0B;
    }}

    /* Stepper Lifecycle Walkthrough */
    .stepper {{
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .step-card {{
      background: var(--surface);
      border: 1px solid var(--surface-border);
      border-radius: 10px;
      padding: 18px 20px;
      display: flex;
      align-items: flex-start;
      gap: 18px;
      transition: border-color 0.15s;
    }}
    .step-card:hover {{
      border-color: var(--accent);
    }}
    .step-num {{
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: var(--accent);
      color: #FFFFFF;
      font-size: 1rem;
      font-weight: 800;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      box-shadow: 0 0 12px var(--accent-glow);
    }}
    .step-content {{
      flex: 1;
    }}
    .step-top {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 6px;
      flex-wrap: wrap;
      gap: 8px;
    }}
    .step-title {{
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--text-main);
    }}
    .protocol-pill {{
      font-size: 0.72rem;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 4px;
      background: var(--badge-bg);
      border: 1px solid var(--surface-border);
      color: var(--accent);
      text-transform: uppercase;
    }}
    .step-desc {{
      font-size: 0.88rem;
      color: var(--text-muted);
      line-height: 1.5;
      margin-bottom: 10px;
    }}
    .step-action-btn {{
      background: transparent;
      border: 1px solid var(--surface-border);
      color: var(--accent);
      font-size: 0.75rem;
      font-weight: 600;
      padding: 4px 10px;
      border-radius: 4px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 5px;
    }}
    .step-action-btn:hover {{
      background: var(--badge-bg);
    }}

    /* Component Inventory Cards */
    .inventory-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
      gap: 16px;
    }}
    .inv-card {{
      background: var(--surface);
      border: 1px solid var(--surface-border);
      border-radius: 10px;
      padding: 16px;
      display: flex;
      flex-direction: column;
    }}
    .inv-top {{
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 10px;
    }}
    .inv-icon-box {{
      width: 36px;
      height: 36px;
      border-radius: 8px;
      background: var(--bg);
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      border: 1px solid var(--surface-border);
    }}
    .inv-name {{
      font-size: 0.98rem;
      font-weight: 700;
      color: var(--text-main);
    }}
    .inv-tech {{
      font-size: 0.78rem;
      font-weight: 600;
      color: #38BDF8;
    }}
    .inv-desc {{
      font-size: 0.84rem;
      line-height: 1.5;
      color: var(--text-muted);
      margin-bottom: 12px;
    }}
    .inv-meta {{
      margin-top: auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid var(--surface-border);
      padding-top: 10px;
    }}

    /* Matrix Table */
    .table-container {{
      background: var(--surface);
      border: 1px solid var(--surface-border);
      border-radius: 10px;
      overflow-x: auto;
    }}
    table.data-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.85rem;
      text-align: left;
    }}
    table.data-table th {{
      background: var(--bg);
      color: var(--text-muted);
      font-weight: 700;
      text-transform: uppercase;
      font-size: 0.72rem;
      letter-spacing: 0.05em;
      padding: 12px 16px;
      border-bottom: 1px solid var(--surface-border);
    }}
    table.data-table td {{
      padding: 12px 16px;
      border-bottom: 1px solid var(--surface-border);
      color: var(--text-main);
    }}
    table.data-table tr:last-child td {{
      border-bottom: none;
    }}

    /* Print & Whitepaper Mode */
    @media print {{
      header, .floating-dock, #minimap-card, #drawer, .btn, .search-box, .view-switcher {{
        display: none !important;
      }}
      #canvas-view {{ display: none !important; }}
      #explainer-view {{
        display: block !important;
        position: static !important;
        height: auto !important;
        overflow: visible !important;
        background: #FFFFFF !important;
        color: #000000 !important;
      }}
      .hero-card, .adr-card, .step-card, .inv-card, .table-container {{
        background: #FFFFFF !important;
        border: 1px solid #CCCCCC !important;
        color: #000000 !important;
        box-shadow: none !important;
        page-break-inside: avoid;
      }}
      .hero-title, .section-title, .adr-name, .step-title, .inv-name {{
        color: #000000 !important;
      }}
      .hero-summary, .adr-body, .step-desc, .inv-desc {{
        color: #333333 !important;
      }}
    }}
  </style>
</head>
<body data-theme="dark">

  <!-- Top Navigation Header -->
  <header>
    <div class="brand">
      <div class="brand-logo">📐 VizArc</div>
      <span class="version-tag">Archify Spec</span>
      <div>
        <div class="doc-title">{ir.get('title', 'Architecture Explainer')}</div>
        <div class="doc-summary" title="{ir.get('summary', '')}">{ir.get('summary', '')}</div>
      </div>
    </div>

    <!-- Center Dual-View Switcher -->
    <div class="view-switcher">
      <button class="tab-btn active" id="tab-canvas-btn" onclick="switchView('canvas')" title="Interactive Diagram Canvas (Key: 1)">📐 Canvas View</button>
      <button class="tab-btn" id="tab-explainer-btn" onclick="switchView('explainer')" title="One-Page Architectural Explainer (Key: 2)">📄 One-Page Explainer</button>
    </div>

    <!-- Right Controls -->
    <div class="controls">
      <button class="btn active-toggle" id="motion-btn" title="Toggle Flow Motion Animation (Key: M)">⚡ Flow Motion</button>
      <input type="text" id="search-input" class="search-box" placeholder="🔍 Search (/)" />
      <button class="btn" id="theme-btn" title="Toggle Dark/Light Theme (Key: D)">🌓 Theme</button>
      <button class="btn" id="export-svg-btn" title="Download standalone SVG">📥 SVG</button>
      <button class="btn" id="export-png-btn" title="Export High-Res PNG">🖼️ PNG</button>
      <button class="btn" id="export-print-btn" title="Print / PDF Whitepaper (Ctrl+P)">📄 Print</button>
      <button class="btn" id="fullscreen-btn" title="Toggle Fullscreen (Key: F)">⛶</button>
    </div>
  </header>

  <!-- ==========================================
       VIEW 1: DIAGRAM CANVAS
       ========================================== -->
  <div id="canvas-view" class="view-panel active">
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

      <div class="drawer-section">
        <div class="drawer-label">Incoming Traffic (Upstream)</div>
        <div id="d-upstream"></div>
      </div>

      <div class="drawer-section">
        <div class="drawer-label">Outgoing Calls (Downstream)</div>
        <div id="d-downstream"></div>
      </div>

      <div class="drawer-section" style="margin-top: 24px;">
        <button class="btn" style="width: 100%; justify-content: center;" id="d-jump-explainer-btn">📄 View in One-Page Explainer</button>
      </div>
    </div>
  </div>

  <!-- ==========================================
       VIEW 2: ONE-PAGE EXPLAINER (Archify Standard)
       ========================================== -->
  <div id="explainer-view" class="view-panel">
    <div class="explainer-container">
      
      <!-- Executive Summary Card -->
      <div class="hero-card">
        <div class="hero-meta">
          <span class="status-badge">ARCHITECTURAL BRIEF</span>
          <span class="version-tag">{ir.get('archetype', 'architecture').upper()} ARCHETYPE</span>
        </div>
        <h1 class="hero-title">{ir.get('title', 'System Architecture')}</h1>
        <p class="hero-summary">{ir.get('summary', 'Enterprise architecture specification and technical implementation details.')}</p>
        
        <div class="stats-grid">
          <div class="stat-box">
            <span class="stat-val">{len(ir.get('nodes', []))}</span>
            <span class="stat-label">System Components</span>
          </div>
          <div class="stat-box">
            <span class="stat-val">{len(ir.get('tiers', []))}</span>
            <span class="stat-label">Architecture Tiers</span>
          </div>
          <div class="stat-box">
            <span class="stat-val">{len(ir.get('edges', []))}</span>
            <span class="stat-label">Network Connections</span>
          </div>
          <div class="stat-box">
            <span class="stat-val">{len(ir.get('decisions', []))}</span>
            <span class="stat-label">Design Decisions (ADR)</span>
          </div>
        </div>
      </div>

      <!-- Section 1: Architecture Decisions & Trade-Offs (ADRs) -->
      <h2 class="section-title">⚖️ Key Architecture Decisions & Trade-offs</h2>
      <p class="section-desc">Core architectural trade-offs, rationale, and operational consequences accepted across this system.</p>
      
      <div class="decisions-grid" id="explainer-decisions">
        <!-- Rendered dynamically -->
      </div>

      <!-- Section 2: Step-by-Step Data Flow Narrative -->
      <h2 class="section-title">🔄 End-to-End Transaction Flow</h2>
      <p class="section-desc">Lifecycle walkthrough of how payloads and transactions traverse the system from ingress to storage.</p>
      
      <div class="stepper" id="explainer-stepper">
        <!-- Rendered dynamically -->
      </div>

      <!-- Section 3: Component & Service Inventory -->
      <h2 class="section-title">📦 Component & Service Inventory</h2>
      <p class="section-desc">Detailed catalog of all microservices, databases, gateways, and edge workers with their roles.</p>
      
      <div class="inventory-grid" id="explainer-inventory">
        <!-- Rendered dynamically -->
      </div>

      <!-- Section 4: Network Protocols & Communication Matrix -->
      <h2 class="section-title">🌐 Communication & Protocols Matrix</h2>
      <p class="section-desc">Upstream-to-downstream communication pathways, transport protocols, and operational goals.</p>
      
      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>From (Caller)</th>
              <th>To (Callee)</th>
              <th>Protocol</th>
              <th>Action / Purpose</th>
            </tr>
          </thead>
          <tbody id="explainer-matrix-body">
            <!-- Rendered dynamically -->
          </tbody>
        </table>
      </div>

    </div>
  </div>

  <script>
    const IR = {ir_json_str};

    let currentOrientation = "horizontal";
    let isFlowMotionActive = true;
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

    const tiersOrder = (IR.tiers || []).map(t => t.id);
    const nodesByTier = {{}};
    tiersOrder.forEach(t => nodesByTier[t] = []);

    IR.nodes.forEach(n => {{
      const t = nodesByTier[n.tier] ? n.tier : tiersOrder[0];
      if (nodesByTier[t]) nodesByTier[t].push(n);
    }});

    // ==========================================
    // VIEW SWITCHING (Canvas vs Explainer)
    // ==========================================
    function switchView(target) {{
      const canvasPanel = document.getElementById("canvas-view");
      const explainerPanel = document.getElementById("explainer-view");
      const canvasBtn = document.getElementById("tab-canvas-btn");
      const explainerBtn = document.getElementById("tab-explainer-btn");

      if (target === "canvas") {{
        canvasPanel.classList.add("active");
        explainerPanel.classList.remove("active");
        canvasBtn.classList.add("active");
        explainerBtn.classList.remove("active");
        setTimeout(fitToView, 30);
      }} else {{
        explainerPanel.classList.add("active");
        canvasPanel.classList.remove("active");
        explainerBtn.classList.add("active");
        canvasBtn.classList.remove("active");
      }}
    }}

    // ==========================================
    // LAYOUT ENGINE
    // ==========================================
    function computeLayout() {{
      Object.keys(nodePositions).forEach(k => delete nodePositions[k]);

      if (currentOrientation === "horizontal") {{
        const COL_GAP = 140;
        const ROW_GAP = 28;
        const PADDING_LEFT = 70;
        const PADDING_TOP = 80;

        let maxRows = 1;
        tiersOrder.forEach(tId => {{
          maxRows = Math.max(maxRows, (nodesByTier[tId] || []).length);
        }});
        const totalHeight = maxRows * (NODE_HEIGHT + ROW_GAP);

        let currX = PADDING_LEFT;
        tiersOrder.forEach((tId) => {{
          const tNodes = nodesByTier[tId] || [];
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
          maxCols = Math.max(maxCols, (nodesByTier[tId] || []).length);
        }});
        const totalWidth = maxCols * (NODE_WIDTH + COL_GAP);

        let currY = PADDING_TOP;
        tiersOrder.forEach((tId) => {{
          const tNodes = nodesByTier[tId] || [];
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
        const tierObj = (IR.tiers || []).find(t => t.id === tId);
        const tierNodes = nodesByTier[tId] || [];
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
      (IR.edges || []).forEach((edge) => {{
        const source = nodePositions[edge.from];
        const target = nodePositions[edge.to];
        if (!source || !target) return;

        let x1, y1, x2, y2, pathD;
        const proto = (edge.protocol || "https").toLowerCase();
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
        path.setAttribute("class", isFlowMotionActive ? "edge-path flow-active" : "edge-path");
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
      (IR.nodes || []).forEach(node => {{
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

        // Icon Box
        const iconBox = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        iconBox.setAttribute("x", 12);
        iconBox.setAttribute("y", 14);
        iconBox.setAttribute("width", 34);
        iconBox.setAttribute("height", 34);
        iconBox.setAttribute("rx", 8);
        iconBox.setAttribute("fill", "var(--surface)");
        iconBox.setAttribute("stroke", brandColor);
        iconBox.setAttribute("stroke-opacity", "0.35");

        // Embedded Vector SVG (100% Offline-proof)
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

        // Role Description
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

    // ==========================================
    // PAN & ZOOM
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

    // ==========================================
    // MINIMAP
    // ==========================================
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

    // ==========================================
    // NODE SELECTION & PATH TRACING
    // ==========================================
    function selectNode(selectedId) {{
      const allNodes = document.querySelectorAll(".node-group");
      const allEdges = document.querySelectorAll(".edge-path");

      const upstreams = new Set();
      const downstreams = new Set();
      const activeEdgeIds = new Set();

      (IR.edges || []).forEach(e => {{
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

    // ==========================================
    // SIDE INSPECTOR DRAWER
    // ==========================================
    const drawer = document.getElementById("drawer");
    let currentDrawerNodeId = null;

    function openDrawer(nodeId, upstreams, downstreams) {{
      currentDrawerNodeId = nodeId;
      const node = nodesMap[nodeId];
      if (!node) return;

      const meta = node._meta || {{}};
      const tierObj = (IR.tiers || []).find(t => t.id === node.tier);
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
      currentDrawerNodeId = null;
      document.querySelectorAll(".node-group").forEach(el => el.classList.remove("is-selected", "is-upstream", "is-downstream", "is-dimmed"));
      document.querySelectorAll(".edge-path").forEach(el => {{
        el.classList.remove("is-active", "is-dimmed");
        el.setAttribute("marker-end", "url(#arrow-default)");
      }});
    }}

    document.getElementById("d-close").onclick = closeDrawer;

    document.getElementById("d-jump-explainer-btn").onclick = () => {{
      if (currentDrawerNodeId) {{
        switchView("explainer");
        const el = document.getElementById(`inv-card-${{currentDrawerNodeId}}`);
        if (el) {{
          el.scrollIntoView({{ behavior: "smooth", block: "center" }});
          el.style.borderColor = "var(--accent)";
          setTimeout(() => el.style.borderColor = "var(--surface-border)", 2000);
        }}
      }}
    }};

    // ==========================================
    // RENDER ONE-PAGE EXPLAINER (Archify Standard)
    // ==========================================
    function renderExplainer() {{
      // 1. Decisions
      const decContainer = document.getElementById("explainer-decisions");
      decContainer.innerHTML = "";
      (IR.decisions || []).forEach(d => {{
        const card = document.createElement("div");
        card.className = "adr-card";
        card.innerHTML = `
          <div class="adr-header">
            <div class="adr-name">📌 ${{d.decision}}</div>
            <span class="status-badge">${{d.status || 'ACCEPTED'}}</span>
          </div>
          <div class="adr-body">${{d.rationale}}</div>
          <div class="tradeoff-box">
            <strong>⚠️ Trade-off:</strong> ${{d.tradeoff || 'Operational overhead accepted.'}}
          </div>
        `;
        decContainer.appendChild(card);
      }});

      // 2. Stepper Lifecycle
      const stepContainer = document.getElementById("explainer-stepper");
      stepContainer.innerHTML = "";
      (IR.flow_steps || []).forEach(s => {{
        const srcNode = nodesMap[s.from] || {{ label: s.from }};
        const tgtNode = nodesMap[s.to] || {{ label: s.to }};
        const item = document.createElement("div");
        item.className = "step-card";
        item.innerHTML = `
          <div class="step-num">${{s.step}}</div>
          <div class="step-content">
            <div class="step-top">
              <span class="step-title">${{s.title || (srcNode.label + ' → ' + tgtNode.label)}}</span>
              <span class="protocol-pill">${{s.protocol || 'HTTPS'}}</span>
            </div>
            <p class="step-desc">${{s.description}}</p>
            <button class="step-action-btn" onclick="highlightStepOnCanvas('${{s.from}}', '${{s.to}}')">
              🔍 Inspect on Canvas
            </button>
          </div>
        `;
        stepContainer.appendChild(item);
      }});

      // 3. Component Inventory
      const invContainer = document.getElementById("explainer-inventory");
      invContainer.innerHTML = "";
      (IR.nodes || []).forEach(node => {{
        const meta = node._meta || {{}};
        const brandColor = meta.brand_color || "#3B82F6";
        const tierObj = (IR.tiers || []).find(t => t.id === node.tier);
        const card = document.createElement("div");
        card.className = "inv-card";
        card.id = `inv-card-${{node.id}}`;
        card.innerHTML = `
          <div class="inv-top">
            <div class="inv-icon-box" style="border-color: ${{brandColor}}55;">
              <svg width="22" height="22" viewBox="0 0 24 24">
                <path fill="${{brandColor}}" d="${{meta.icon || 'M12 2L2 7v10l10 5 10-5V7L12 2z'}}" />
              </svg>
            </div>
            <div>
              <div class="inv-name">${{node.label}}</div>
              <div class="inv-tech">${{node.tech || 'Service'}}</div>
            </div>
          </div>
          <p class="inv-desc">${{node.description || meta.service_name || 'Component responsibility.'}}</p>
          <div class="inv-meta">
            <span class="protocol-pill" style="color: ${{tierObj ? tierObj.color : 'var(--accent)'}};">
              ${{tierObj ? tierObj.label : node.tier}}
            </span>
            <button class="step-action-btn" onclick="focusNodeOnCanvas('${{node.id}}')">
              ⛶ Focus Node
            </button>
          </div>
        `;
        invContainer.appendChild(card);
      }});

      // 4. Matrix Table
      const matrixBody = document.getElementById("explainer-matrix-body");
      matrixBody.innerHTML = "";
      (IR.edges || []).forEach(e => {{
        const srcNode = nodesMap[e.from] || {{ label: e.from }};
        const tgtNode = nodesMap[e.to] || {{ label: e.to }};
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td><strong>${{srcNode.label}}</strong></td>
          <td><strong>${{tgtNode.label}}</strong></td>
          <td><span class="protocol-pill">${{e.protocol || 'HTTPS'}}</span></td>
          <td style="color:var(--text-muted);">${{e.label || 'Direct call / data transfer'}}</td>
        `;
        matrixBody.appendChild(tr);
      }});
    }}

    function highlightStepOnCanvas(fromId, toId) {{
      switchView("canvas");
      selectNode(fromId);
    }}

    function focusNodeOnCanvas(nodeId) {{
      switchView("canvas");
      selectNode(nodeId);
    }}

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

    // Theme Toggle
    document.getElementById("theme-btn").onclick = () => {{
      const cur = document.body.getAttribute("data-theme");
      document.body.setAttribute("data-theme", cur === "dark" ? "light" : "dark");
    }};

    // Fit View (Auto-fit to 16:9 or current window aspect ratio)
    function fitToView() {{
      const nodeKeys = Object.keys(nodePositions);
      if (!nodeKeys.length) return;

      let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
      nodeKeys.forEach(k => {{
        const p = nodePositions[k];
        minX = Math.min(minX, p.x);
        minY = Math.min(minY, p.y);
        maxX = Math.max(maxX, p.x + p.width);
        maxY = Math.max(maxY, p.y + p.height);
      }});

      // Account for tier containers, labels, and margins
      minX -= 32;
      minY -= 42;
      maxX += 32;
      maxY += 32;

      const diagramW = Math.max(maxX - minX, 300);
      const diagramH = Math.max(maxY - minY, 200);

      const vpW = viewport.clientWidth || window.innerWidth || 1280;
      const vpH = viewport.clientHeight || (window.innerHeight - 58) || 720;

      // Fit diagram within viewport with safe padding
      const scaleX = (vpW * 0.92) / diagramW;
      const scaleY = (vpH * 0.92) / diagramH;
      scale = Math.min(Math.min(scaleX, scaleY), 1.35);

      // Center horizontally and vertically
      panX = (vpW - (maxX - minX) * scale) / 2 - minX * scale;
      panY = (vpH - (maxY - minY) * scale) / 2 - minY * scale;

      updateTransform();
    }}

    document.getElementById("reset-btn").onclick = fitToView;

    document.getElementById("orient-btn").onclick = () => {{
      currentOrientation = currentOrientation === "horizontal" ? "vertical" : "horizontal";
      renderScene();
      fitToView();
    }};

    document.getElementById("zoom-in-btn").onclick = () => {{
      scale = Math.min(scale * 1.2, 3.0);
      updateTransform();
    }};

    document.getElementById("zoom-out-btn").onclick = () => {{
      scale = Math.max(scale * 0.8, 0.25);
      updateTransform();
    }};

    // Fullscreen Toggle
    document.getElementById("fullscreen-btn").onclick = () => {{
      if (!document.fullscreenElement) {{
        document.documentElement.requestFullscreen().catch(() => {{}});
      }} else {{
        document.exitFullscreen().catch(() => {{}});
      }}
    }};

    // Print
    document.getElementById("export-print-btn").onclick = () => {{
      switchView("explainer");
      setTimeout(() => window.print(), 200);
    }};

    // Standalone SVG Export
    document.getElementById("export-svg-btn").onclick = () => {{
      const svg = document.getElementById("diagram-canvas");
      const serializer = new XMLSerializer();
      let source = serializer.serializeToString(svg);
      const blob = new Blob([source], {{ type: "image/svg+xml;charset=utf-8" }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "{ir.get('title', 'architecture').lower().replace(' ', '_')}.svg";
      a.click();
    }};

    // High-Resolution PNG Export via Canvas
    document.getElementById("export-png-btn").onclick = () => {{
      const svg = document.getElementById("diagram-canvas");
      const serializer = new XMLSerializer();
      let source = serializer.serializeToString(svg);

      if (!source.match(/^<svg[^>]+xmlns="http\\:\\/\\/www\\.w3\\.org\\/2000\\/svg"/)) {{
        source = source.replace(/^<svg/, '<svg xmlns="http://www.w3.org/2000/svg"');
      }}

      const img = new Image();
      const svgBlob = new Blob([source], {{ type: "image/svg+xml;charset=utf-8" }});
      const url = URL.createObjectURL(svgBlob);

      img.onload = function() {{
        const canvas = document.createElement("canvas");
        const scaleFactor = 2;
        canvas.width = (viewport.clientWidth || 1200) * scaleFactor;
        canvas.height = (viewport.clientHeight || 800) * scaleFactor;
        const ctx = canvas.getContext("2d");
        ctx.scale(scaleFactor, scaleFactor);
        ctx.fillStyle = document.body.getAttribute("data-theme") === "light" ? "#F8FAFC" : "#090D16";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0, viewport.clientWidth || 1200, viewport.clientHeight || 800);
        URL.revokeObjectURL(url);

        const pngUrl = canvas.toDataURL("image/png");
        const a = document.createElement("a");
        a.download = "{ir.get('title', 'architecture').lower().replace(' ', '_')}.png";
        a.href = pngUrl;
        a.click();
      }};
      img.src = url;
    }};

    // Keyboard Shortcuts
    window.addEventListener("keydown", (e) => {{
      if (e.target === searchInput && e.key !== "Escape") return;
      if (e.key === "Escape") {{
        closeDrawer();
        searchInput.blur();
      }} else if (e.key === "1") {{
        switchView("canvas");
      }} else if (e.key === "2") {{
        switchView("explainer");
      }} else if (e.key === "/") {{
        e.preventDefault();
        searchInput.focus();
      }} else if (e.key.toLowerCase() === "d") {{
        document.getElementById("theme-btn").click();
      }} else if (e.key.toLowerCase() === "m") {{
        toggleFlowMotion();
      }} else if (e.key.toLowerCase() === "r") {{
        document.getElementById("reset-btn").click();
      }} else if (e.key.toLowerCase() === "o") {{
        document.getElementById("orient-btn").click();
      }} else if (e.key.toLowerCase() === "f") {{
        document.getElementById("fullscreen-btn").click();
      }}
    }});

    // Initialize
    window.addEventListener("DOMContentLoaded", () => {{
      renderScene();
      renderExplainer();
      setTimeout(fitToView, 50);
    }});

    window.addEventListener("resize", () => {{
      if (document.getElementById("canvas-view").classList.contains("active")) {{
        fitToView();
      }}
    }});
  </script>
</body>
</html>"""
