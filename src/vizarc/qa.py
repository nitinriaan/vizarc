"""
VizArc Visual Quality Assurance:
1. Deterministic SVG layout clearance & bounding-box collision checks.
2. Headless browser DOM/rendering verification for generated HTML explainers.
"""

import html as html_lib
import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def _boxes_overlap(a: Tuple[float, float, float, float], b: Tuple[float, float, float, float], pad: float = 0.0) -> bool:
    """Return True if two (x1, y1, x2, y2) bounding boxes overlap within padding."""
    return not (a[2] + pad <= b[0] or b[2] + pad <= a[0] or a[3] + pad <= b[1] or b[3] + pad <= a[1])


def check_svg_layout(ir: Dict[str, Any], orientation: str = "horizontal") -> List[Dict[str, Any]]:
    """
    Checks SVG layout geometry for node overlaps, edge-label collisions, and viewBox overflow.
    """
    from .adapters.svg_adapter import render_svg_diagram

    svg_text = render_svg_diagram(ir, orientation=orientation)
    diagnostics: List[Dict[str, Any]] = []

    vb_match = re.search(r'viewBox="0 0 (\d+) (\d+)"', svg_text)
    vb_w = float(vb_match.group(1)) if vb_match else 1200.0
    vb_h = float(vb_match.group(2)) if vb_match else 800.0

    # Parse node cards: <g id="node-<id>" transform="translate(x, y)">
    node_boxes: Dict[str, Tuple[float, float, float, float]] = {}
    node_w, node_h = 230.0, 92.0
    for match in re.finditer(r'<g id="node-([^"]+)" transform="translate\(([^,]+),\s*([^)]+)\)"', svg_text):
        nid = match.group(1)
        nx, ny = float(match.group(2)), float(match.group(3))
        box = (nx, ny, nx + node_w, ny + node_h)
        node_boxes[nid] = box
        if nx < 0 or ny < 0 or nx + node_w > vb_w or ny + node_h > vb_h:
            diagnostics.append({
                "ruleCode": "WARN_VIEWBOX_OVERFLOW",
                "severity": "warning",
                "nodeId": nid,
                "message": f"Node '{nid}' extends outside SVG viewBox ({int(vb_w)}x{int(vb_h)}).",
                "supportedFixes": ["adjust_orientation", "increase_canvas_padding"],
            })

    node_ids = list(node_boxes.keys())
    for i in range(len(node_ids)):
        for j in range(i + 1, len(node_ids)):
            a_id, b_id = node_ids[i], node_ids[j]
            if _boxes_overlap(node_boxes[a_id], node_boxes[b_id], pad=4.0):
                diagnostics.append({
                    "ruleCode": "ERR_NODE_OVERLAP",
                    "severity": "error",
                    "nodeId": f"{a_id},{b_id}",
                    "message": f"Layout collision detected between nodes '{a_id}' and '{b_id}'.",
                    "supportedFixes": ["increase_tier_spacing", "switch_orientation"],
                })

    # Parse edge label pills inside <g class="edge">
    label_boxes: List[Tuple[str, Tuple[float, float, float, float]]] = []
    for edge_block in re.findall(r'<g class="edge">(.*?)</g>', svg_text, re.DOTALL):
        rect_m = re.search(r'<rect x="([^"]+)" y="([^"]+)" width="([^"]+)" height="([^"]+)"', edge_block)
        text_m = re.search(r'<text[^>]*>([^<]+)</text>', edge_block)
        if rect_m and text_m:
            lx = float(rect_m.group(1))
            ly = float(rect_m.group(2))
            lw = float(rect_m.group(3))
            lh = float(rect_m.group(4))
            lbl = html_lib.unescape(text_m.group(1))
            lbox = (lx, ly, lx + lw, ly + lh)

            for nid, nbox in node_boxes.items():
                if _boxes_overlap(lbox, nbox, pad=0.0):
                    diagnostics.append({
                        "ruleCode": "WARN_LABEL_NODE_COLLISION",
                        "severity": "warning",
                        "edge": lbl,
                        "message": f"Edge label '{lbl}' overlaps node '{nid}'.",
                        "supportedFixes": ["shorten_edge_label", "increase_tier_gap"],
                    })

            for prev_lbl, prev_box in label_boxes:
                if _boxes_overlap(lbox, prev_box, pad=2.0):
                    diagnostics.append({
                        "ruleCode": "WARN_LABEL_COLLISION",
                        "severity": "warning",
                        "edge": f"{prev_lbl} / {lbl}",
                        "message": f"Edge labels '{prev_lbl}' and '{lbl}' overlap.",
                        "supportedFixes": ["shorten_edge_label", "adjust_tier_ordering"],
                    })
            label_boxes.append((lbl, lbox))

    return diagnostics


def _find_headless_browser() -> Optional[Tuple[str, str]]:
    """Locate an installed Chromium-based browser for headless DOM inspection."""
    candidates = [
        ("chrome", "google-chrome"),
        ("chrome", "chromium"),
        ("chrome", "chromium-browser"),
        ("chrome", "chrome"),
        ("msedge", "msedge"),
    ]
    for kind, exe in candidates:
        found = shutil.which(exe)
        if found:
            return kind, found

    win_paths = [
        ("chrome", Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")),
        ("chrome", Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")),
        ("msedge", Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")),
        ("msedge", Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe")),
    ]
    for kind, path in win_paths:
        if path.exists():
            return kind, str(path)
    return None


def run_browser_check(html_path: str) -> Dict[str, Any]:
    """
    Verifies a generated VizArc HTML file via structural checks and, when available,
    a real headless Chromium/Edge DOM render pass.
    """
    target = Path(html_path).resolve()
    if not target.exists():
        raise FileNotFoundError(f"HTML file not found: {target}")

    content = target.read_text(encoding="utf-8")
    issues: List[Dict[str, str]] = []

    required_ids = [
        "diagram-canvas",
        "canvas-view",
        "explainer-view",
        "explainer-root",
        "flow-player-dock",
        "export-video-btn",
        "nodes-layer",
        "edges-layer",
    ]
    for elem_id in required_ids:
        if f'id="{elem_id}"' not in content:
            issues.append({
                "severity": "error",
                "check": "DOM_STRUCTURE",
                "message": f"Missing required element '#{elem_id}' in HTML output.",
            })

    ir_match = re.search(r"const\s+IR\s*=\s*(\{.*?\});", content, re.DOTALL)
    expected_nodes = 0
    expected_edges = 0
    if not ir_match:
        issues.append({
            "severity": "error",
            "check": "EMBEDDED_IR",
            "message": "Embedded Canonical IR JSON payload not found in HTML.",
        })
    else:
        try:
            parsed_ir = json.loads(ir_match.group(1))
            expected_nodes = len(parsed_ir.get("nodes", []))
            expected_edges = len(parsed_ir.get("edges", []))
        except json.JSONDecodeError as exc:
            issues.append({
                "severity": "error",
                "check": "EMBEDDED_IR",
                "message": f"Invalid embedded IR JSON: {exc}",
            })

    browser_used = "static-only"
    rendered_nodes = None
    rendered_edges = None
    explainer_rendered = None

    browser = _find_headless_browser()
    if browser:
        kind, exe = browser
        file_url = target.as_uri()
        cmd = [
            exe,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--virtual-time-budget=2500",
            "--dump-dom",
            file_url,
        ]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=20, encoding="utf-8", errors="replace")
            if proc.returncode == 0 and proc.stdout:
                browser_used = kind
                dom = proc.stdout
                rendered_nodes = len(re.findall(r'class="node-group"', dom))
                rendered_edges = len(re.findall(r'class="edge-path', dom))
                explainer_rendered = 'class="exp-hero"' in dom

                if expected_nodes > 0 and rendered_nodes != expected_nodes:
                    issues.append({
                        "severity": "error",
                        "check": "BROWSER_NODES",
                        "message": f"Expected {expected_nodes} rendered SVG nodes, got {rendered_nodes}.",
                    })
                if expected_edges > 0 and rendered_edges != expected_edges:
                    issues.append({
                        "severity": "error",
                        "check": "BROWSER_EDGES",
                        "message": f"Expected {expected_edges} rendered SVG edges, got {rendered_edges}.",
                    })
                if not explainer_rendered:
                    issues.append({
                        "severity": "error",
                        "check": "BROWSER_EXPLAINER",
                        "message": "One-Page Explainer DOM failed to render in headless browser.",
                    })
        except (subprocess.SubprocessError, OSError):
            browser_used = "static-only"

    errors = [i for i in issues if i["severity"] == "error"]
    return {
        "passed": len(errors) == 0,
        "target": str(target),
        "browser": browser_used,
        "expected_nodes": expected_nodes,
        "expected_edges": expected_edges,
        "rendered_nodes": rendered_nodes,
        "rendered_edges": rendered_edges,
        "explainer_rendered": explainer_rendered,
        "issues": issues,
    }
