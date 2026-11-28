"""Offline unit and integration tests for VizArc compiler, QA, diff, and CLI."""

import json
import sys
from pathlib import Path

from click.testing import CliRunner

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from vizarc.adapters import render_all_formats
from vizarc.cli import main as cli_main
from vizarc.engine import VizArcEngine
from vizarc.ir import get_demo_ir, validate_ir
from vizarc.qa import check_svg_layout, run_browser_check


def test_all_adapters_render_cleanly():
    ir = validate_ir(get_demo_ir())
    renders = render_all_formats(ir)
    expected = {"html", "svg", "d2", "mermaid", "structurizr", "plantuml", "graphviz", "excalidraw", "ascii"}
    assert expected.issubset(renders.keys())
    for fmt, output in renders.items():
        assert isinstance(output, str) and len(output.strip()) > 0, f"Empty output for {fmt}"


def test_html_contains_dual_view_and_story_video():
    ir = validate_ir(get_demo_ir())
    html_out = render_all_formats(ir)["html"]
    for marker in (
        'id="tab-canvas"',
        'id="tab-explainer"',
        'id="explainer-view"',
        'id="explainer-root"',
        'id="export-video-btn"',
        'id="print-btn"',
        'id="story-caption-bar"',
        'id="d-files-section"',
    ):
        assert marker in html_out, f"Missing {marker} in compiled HTML"


def test_layout_qa_detects_no_node_overlaps_on_demo():
    ir = validate_ir(get_demo_ir())
    diags = check_svg_layout(ir, orientation="horizontal")
    errors = [d for d in diags if d["severity"] == "error"]
    assert errors == []


def test_visual_diff_html_generation():
    engine = VizArcEngine()
    base_ir = validate_ir(get_demo_ir())
    head_ir = validate_ir({
        **base_ir,
        "nodes": [
            *base_ir["nodes"],
            {
                "id": "audit_svc",
                "label": "Audit Service",
                "tier": "services",
                "tech": "Rust / Tonic",
                "description": "Immutable compliance ledger.",
            },
        ],
        "edges": [
            *base_ir["edges"],
            {"from": "order_svc", "to": "audit_svc", "label": "Log Event", "protocol": "gRPC"},
        ],
    })
    diff_html = engine.compare_html(base_ir, head_ir)
    assert "Audit Service" in diff_html
    assert "Added Nodes" in diff_html


def test_cli_compile_validate_browser_check_and_compare(tmp_path: Path):
    runner = CliRunner()
    ir_file = tmp_path / "arch.json"
    ir_file.write_text(json.dumps(get_demo_ir()), encoding="utf-8")

    html_file = tmp_path / "arch.html"
    res = runner.invoke(cli_main, ["compile", str(ir_file), "--format", "html", "--strict", "-o", str(html_file)])
    assert res.exit_code == 0, res.output
    assert html_file.exists()

    res_val = runner.invoke(cli_main, ["validate", str(html_file)])
    assert res_val.exit_code == 0, res_val.output

    qa_report = run_browser_check(str(html_file))
    assert qa_report["passed"], qa_report["issues"]

    diff_file = tmp_path / "diff.html"
    res_cmp = runner.invoke(cli_main, ["compare", str(ir_file), str(html_file), "--format", "html", "-o", str(diff_file)])
    assert res_cmp.exit_code == 0, res_cmp.output
    assert diff_file.exists()


def test_cli_install_skill_project_scope(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    res = runner.invoke(cli_main, ["install-skill", "--platform", "all", "--scope", "project"])
    assert res.exit_code == 0, res.output
    for rel in (
        ".claude/skills/vizarc/SKILL.md",
        ".agent/skills/vizarc/SKILL.md",
        ".agents/skills/vizarc/SKILL.md",
        ".cursor/skills/vizarc/SKILL.md",
        ".github/skills/vizarc/SKILL.md",
        ".opencode/skills/vizarc/SKILL.md",
    ):
        assert (tmp_path / rel).exists(), f"Missing installed skill: {rel}"
        assert (tmp_path / rel).parent.joinpath("references/ir-schema.md").exists()


def test_claude_marketplace_and_plugin_manifests():
    repo_root = Path(__file__).resolve().parent.parent
    plugin = json.loads((repo_root / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    mkt = json.loads((repo_root / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))

    assert plugin["name"] == "vizarc"
    assert (repo_root / plugin["skills"][0] / "SKILL.md").exists()
    assert mkt["name"] == "vizarc"
    assert mkt["plugins"][0]["name"] == "vizarc"
    assert mkt["plugins"][0]["source"] == "./"
