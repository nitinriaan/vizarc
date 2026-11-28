"""
VizArc Visual Architecture Diff Renderer:
Compiles Before / Delta / After comparison between two Canonical IR models
into a self-contained interactive HTML diff report.
"""

import json
from typing import Any, Dict
from .logo_data import FAVICON_URI, LOGO_DARK_URI, LOGO_LIGHT_URI


def render_visual_diff_html(
    base_ir: Dict[str, Any],
    head_ir: Dict[str, Any],
    diff_result: Dict[str, Any],
) -> str:
    """Render an interactive Before / Delta / After visual diff HTML page."""
    payload = json.dumps(
        {
            "base": base_ir,
            "head": head_ir,
            "summary": diff_result.get("summary", ""),
            "delta": diff_result.get("delta", {}),
        },
        indent=2,
    )

    base_title = diff_result.get("base_title", base_ir.get("title", "Base"))
    head_title = diff_result.get("head_title", head_ir.get("title", "Head"))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Architecture Diff: {base_title} → {head_title} — VizArc</title>
  <link rel="icon" type="image/png" href="{FAVICON_URI}">
  <style>
    :root {{
      --bg: #090D16; --surface: #0F172A; --border: #1E293B;
      --text: #F8FAFC; --muted: #94A3B8; --accent: #3B82F6;
      --added: #10B981; --removed: #EF4444; --modified: #F59E0B;
    }}
    [data-theme="light"] {{
      --bg: #F8FAFC; --surface: #FFFFFF; --border: #E2E8F0;
      --text: #0F172A; --muted: #64748B; --accent: #2563EB;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
    body {{ background: var(--bg); color: var(--text); min-height: 100vh; }}
    header {{
      height: 58px; background: var(--surface); border-bottom: 1px solid var(--border);
      display: flex; align-items: center; justify-content: space-between; padding: 0 20px; gap: 12px;
    }}
    .brand {{ display: flex; align-items: center; gap: 12px; }}
    .brand img {{ height: 28px; }}
    body[data-theme="dark"] .logo-light {{ display: none; }}
    body[data-theme="light"] .logo-dark {{ display: none; }}
    .controls {{ display: flex; gap: 8px; align-items: center; }}
    .btn {{
      border: 1px solid var(--border); background: var(--surface); color: var(--text);
      padding: 6px 12px; border-radius: 6px; font-size: 0.78rem; font-weight: 700; cursor: pointer;
    }}
    .btn.active {{ background: var(--accent); border-color: var(--accent); color: #FFF; }}
    main {{ max-width: 1240px; margin: 0 auto; padding: 24px 20px 60px; display: flex; flex-direction: column; gap: 20px; }}
    .kpis {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; }}
    .kpi {{
      background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 14px 16px;
    }}
    .kpi-num {{ font-size: 1.5rem; font-weight: 800; }}
    .kpi-lbl {{ font-size: 0.72rem; text-transform: uppercase; color: var(--muted); font-weight: 700; }}
    .canvas-card {{
      background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 16px; overflow-x: auto;
    }}
    .legend {{ display: flex; gap: 14px; flex-wrap: wrap; font-size: 0.78rem; margin-bottom: 12px; }}
    .dot {{ display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 5px; }}
    .delta-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 14px; }}
    .delta-card {{
      background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 14px;
    }}
    .delta-card h3 {{ font-size: 0.9rem; margin-bottom: 10px; }}
    .delta-item {{
      padding: 8px 10px; border-radius: 6px; background: var(--bg); border: 1px solid var(--border);
      margin-bottom: 8px; font-size: 0.82rem; line-height: 1.45;
    }}
  </style>
</head>
<body data-theme="dark">
  <header>
    <div class="brand">
      <img class="logo-dark" src="{LOGO_DARK_URI}" alt="VizArc" />
      <img class="logo-light" src="{LOGO_LIGHT_URI}" alt="VizArc" />
      <div>
        <div style="font-weight:800; font-size:0.95rem;">Architecture Diff: {base_title} → {head_title}</div>
        <div style="font-size:0.75rem; color:var(--muted);">{diff_result.get('summary', '')}</div>
      </div>
    </div>
    <div class="controls">
      <button class="btn active" data-mode="delta">Delta View</button>
      <button class="btn" data-mode="before">Before</button>
      <button class="btn" data-mode="after">After</button>
      <button class="btn" id="theme-toggle">🌓 Theme</button>
    </div>
  </header>

  <main>
    <div class="kpis" id="kpi-bar"></div>
    <div class="canvas-card">
      <div class="legend">
        <span><i class="dot" style="background:var(--added)"></i>Added</span>
        <span><i class="dot" style="background:var(--removed)"></i>Removed</span>
        <span><i class="dot" style="background:var(--modified)"></i>Modified</span>
        <span><i class="dot" style="background:#64748B"></i>Unchanged</span>
      </div>
      <svg id="diff-svg" width="100%" height="440"></svg>
    </div>
    <div class="delta-grid" id="delta-lists"></div>
  </main>

  <script>
    const DIFF = {payload};
    let viewMode = "delta";

    function esc(s) {{
      return String(s ?? "").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
    }}

    function renderKPIs() {{
      const d = DIFF.delta;
      const items = [
        {{ n: (d.added_nodes || []).length, l: "Added Nodes", c: "var(--added)" }},
        {{ n: (d.removed_nodes || []).length, l: "Removed Nodes", c: "var(--removed)" }},
        {{ n: (d.modified_nodes || []).length, l: "Modified Nodes", c: "var(--modified)" }},
        {{ n: (d.added_edges || []).length, l: "Added Edges", c: "var(--added)" }},
        {{ n: (d.removed_edges || []).length, l: "Removed Edges", c: "var(--removed)" }}
      ];
      document.getElementById("kpi-bar").innerHTML = items.map(i => `
        <div class="kpi">
          <div class="kpi-num" style="color:${{i.c}}">${{i.n}}</div>
          <div class="kpi-lbl">${{i.l}}</div>
        </div>
      `).join("");
    }}

    function renderGraph() {{
      const svg = document.getElementById("diff-svg");
      const d = DIFF.delta;
      const addedSet = new Set((d.added_nodes || []).map(n => n.id));
      const removedSet = new Set((d.removed_nodes || []).map(n => n.id));
      const modSet = new Set((d.modified_nodes || []).map(n => n.id));

      let nodes = [];
      let edges = [];
      if (viewMode === "before") {{
        nodes = (DIFF.base.nodes || []).map(n => ({{ ...n, _status: removedSet.has(n.id) ? "removed" : (modSet.has(n.id) ? "modified" : "same") }}));
        edges = (DIFF.base.edges || []).map(e => ({{ ...e, _status: "same" }}));
      }} else if (viewMode === "after") {{
        nodes = (DIFF.head.nodes || []).map(n => ({{ ...n, _status: addedSet.has(n.id) ? "added" : (modSet.has(n.id) ? "modified" : "same") }}));
        edges = (DIFF.head.edges || []).map(e => ({{ ...e, _status: "same" }}));
      }} else {{
        const headMap = new Map((DIFF.head.nodes || []).map(n => [n.id, n]));
        (DIFF.head.nodes || []).forEach(n => nodes.push({{ ...n, _status: addedSet.has(n.id) ? "added" : (modSet.has(n.id) ? "modified" : "same") }}));
        (d.removed_nodes || []).forEach(n => {{ if (!headMap.has(n.id)) nodes.push({{ ...n, _status: "removed" }}); }});

        const addedEdges = new Set((d.added_edges || []).map(e => `${{e.from}}->${{e.to}}`));
        const removedEdges = new Set((d.removed_edges || []).map(e => `${{e.from}}->${{e.to}}`));
        (DIFF.head.edges || []).forEach(e => edges.push({{ ...e, _status: addedEdges.has(`${{e.from}}->${{e.to}}`) ? "added" : "same" }}));
        (d.removed_edges || []).forEach(e => edges.push({{ ...e, _status: "removed" }}));
      }}

      const tiers = ((viewMode === "before" ? DIFF.base.tiers : DIFF.head.tiers) || []);
      const tierIds = tiers.map(t => t.id);
      const groups = {{}};
      tierIds.forEach(id => groups[id] = []);
      nodes.forEach(n => {{
        const t = groups[n.tier] ? n.tier : (tierIds[0] || "default");
        if (!groups[t]) groups[t] = [];
        groups[t].push(n);
      }});

      const orderedTiers = Object.keys(groups).filter(k => groups[k].length > 0);
      const NW = 210, NH = 74, CG = 70, RG = 22;
      const pos = {{}};
      let maxRows = 1;
      orderedTiers.forEach(t => {{ if (groups[t].length > maxRows) maxRows = groups[t].length; }});
      const W = Math.max(760, orderedTiers.length * (NW + CG) + 40);
      const H = Math.max(360, maxRows * (NH + RG) + 80);
      svg.setAttribute("viewBox", `0 0 ${{W}} ${{H}}`);

      let out = "";
      orderedTiers.forEach((tid, colIdx) => {{
        const x = 30 + colIdx * (NW + CG);
        out += `<text x="${{x}}" y="26" fill="#94A3B8" font-size="11" font-weight="700">${{esc(tid.toUpperCase())}}</text>`;
        groups[tid].forEach((n, rowIdx) => {{
          const y = 44 + rowIdx * (NH + RG);
          pos[n.id] = {{ x, y }};
          const color = n._status === "added" ? "#10B981" : (n._status === "removed" ? "#EF4444" : (n._status === "modified" ? "#F59E0B" : "#334155"));
          const dash = n._status === "removed" ? 'stroke-dasharray="6 4"' : "";
          const tag = n._status === "same" ? "" : n._status.toUpperCase();
          out += `
            <g>
              <rect x="${{x}}" y="${{y}}" width="${{NW}}" height="${{NH}}" rx="10" fill="#131B2E" stroke="${{color}}" stroke-width="2" ${{dash}}/>
              <text x="${{x + 12}}" y="${{y + 26}}" fill="#F8FAFC" font-size="13" font-weight="700">${{esc(n.label)}}</text>
              <text x="${{x + 12}}" y="${{y + 45}}" fill="#38BDF8" font-size="10">${{esc(n.tech || '')}}</text>
              ${{tag ? `<text x="${{x + NW - 12}}" y="${{y + 62}}" fill="${{color}}" font-size="9.5" font-weight="800" text-anchor="end">${{tag}}</text>` : ""}}
            </g>
          `;
        }});
      }});

      let edgeSvg = "";
      edges.forEach(e => {{
        const p1 = pos[e.from], p2 = pos[e.to];
        if (!p1 || !p2) return;
        const sx = p1.x + NW, sy = p1.y + NH / 2, tx = p2.x, ty = p2.y + NH / 2;
        const dx = Math.max(40, Math.abs(tx - sx) * 0.45);
        const color = e._status === "added" ? "#10B981" : (e._status === "removed" ? "#EF4444" : "#475569");
        const dash = e._status === "removed" ? 'stroke-dasharray="5 4"' : "";
        edgeSvg += `<path d="M ${{sx}} ${{sy}} C ${{sx + dx}} ${{sy}}, ${{tx - dx}} ${{ty}}, ${{tx}} ${{ty}}" fill="none" stroke="${{color}}" stroke-width="2" ${{dash}}/>`;
      }});
      svg.innerHTML = edgeSvg + out;
    }}

    function renderLists() {{
      const d = DIFF.delta;
      const cards = [
        {{ title: "➕ Added Components & Edges", items: [...(d.added_nodes || []).map(n => `+ Node: <strong>${{esc(n.label)}}</strong> (${{esc(n.tech || n.tier)}})`), ...(d.added_edges || []).map(e => `+ Edge: ${{esc(e.from)}} → ${{esc(e.to)}} [${{esc(e.protocol)}}]`)] }},
        {{ title: "➖ Removed Components & Edges", items: [...(d.removed_nodes || []).map(n => `- Node: <strong>${{esc(n.label)}}</strong>`), ...(d.removed_edges || []).map(e => `- Edge: ${{esc(e.from)}} → ${{esc(e.to)}}`)] }},
        {{ title: "✏️ Modified Components", items: (d.modified_nodes || []).map(n => `<strong>${{esc(n.label)}}</strong><br/>` + Object.entries(n.changes || {{}}).map(([k, v]) => `<span style="color:var(--muted)">${{esc(k)}}:</span> ${{esc(v.before)}} → ${{esc(v.after)}}`).join("<br/>")) }}
      ];
      document.getElementById("delta-lists").innerHTML = cards.map(c => `
        <div class="delta-card">
          <h3>${{c.title}}</h3>
          ${{c.items.length ? c.items.map(i => `<div class="delta-item">${{i}}</div>`).join("") : '<div style="color:var(--muted); font-size:0.82rem;">None</div>'}}
        </div>
      `).join("");
    }}

    document.querySelectorAll("[data-mode]").forEach(btn => {{
      btn.onclick = () => {{
        viewMode = btn.dataset.mode;
        document.querySelectorAll("[data-mode]").forEach(b => b.classList.toggle("active", b === btn));
        renderGraph();
      }};
    }});
    document.getElementById("theme-toggle").onclick = () => {{
      document.body.setAttribute("data-theme", document.body.getAttribute("data-theme") === "dark" ? "light" : "dark");
    }};

    renderKPIs();
    renderGraph();
    renderLists();
  </script>
</body>
</html>
"""
