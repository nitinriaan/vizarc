"""
VizArc CLI: Universal Architecture Compiler & Explainer Engine.
Compiles from a single Canonical Architecture Model into 9 formats:
HTML (Interactive), SVG (Vector), D2, Structurizr C4, Mermaid, PlantUML, Graphviz DOT, Excalidraw, and ASCII.
"""

import json
import os
import re
import shutil
import sys
import webbrowser
from pathlib import Path
from typing import Any, Dict, Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

from vizarc.adapters import render_all_formats, render_ir
from vizarc.adapters.svg_adapter import render_svg_diagram
from vizarc.analyzer import CodebaseAnalyzer
from vizarc.engine import VizArcEngine
from vizarc.ir import lint_ir, validate_ir
from vizarc.templates import TEMPLATES, get_template

console = Console()

FORMAT_EXTENSIONS = {
    "html": "html",
    "svg": "svg",
    "d2": "d2",
    "mermaid": "mmd",
    "structurizr": "dsl",
    "plantuml": "puml",
    "graphviz": "dot",
    "excalidraw": "excalidraw.mmd",
    "ascii": "txt",
    "ir": "json",
}

ALL_FORMATS = [
    "html", "svg", "d2", "mermaid", "structurizr",
    "plantuml", "graphviz", "excalidraw", "ascii", "ir", "all",
]


def _load_ir_payload(source: str) -> Dict[str, Any]:
    """Loads Canonical Architecture IR from a JSON file, HTML file, or '-' (stdin)."""
    if source == "-":
        raw = sys.stdin.read()
    else:
        raw = Path(source).read_text(encoding="utf-8")

    txt = raw.strip()
    if txt.startswith("{"):
        return json.loads(txt)

    match = re.search(r"const\s+IR\s*=\s*(\{.*?\});", txt, re.DOTALL)
    if match:
        return json.loads(match.group(1))

    raise ValueError(f"No Canonical Architecture IR JSON found in '{source}'.")


def _render_single(ir: Dict[str, Any], fmt: str, orientation: str) -> str:
    """Renders a validated IR into a single target format."""
    if fmt == "svg":
        return render_svg_diagram(ir, orientation=orientation)
    if fmt == "ir":
        return json.dumps(ir, indent=2)
    return render_ir(ir, target_format=fmt)


def _write_or_print_output(
    ir: Dict[str, Any],
    fmt: str,
    output: Optional[str],
    orientation: str,
    open_browser: bool,
    default_file_stem: str = "architecture",
    default_all_dir: str = "./vizarc_out",
    include_ir_in_all: bool = True,
) -> None:
    """Compiles IR to the requested format(s) and writes files or prints to console."""
    fmt = fmt.lower()

    if fmt == "all":
        out_dir = Path(output or default_all_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        console.print(
            f"[bold cyan]VizArc[/bold cyan] compiling [bold green]all 9 formats[/bold green] to {out_dir.resolve()}..."
        )
        all_renders = render_all_formats(ir)
        if include_ir_in_all:
            all_renders["ir"] = json.dumps(ir, indent=2)

        for target_fmt, content in all_renders.items():
            ext = FORMAT_EXTENSIONS.get(target_fmt, "txt")
            file_path = out_dir / f"{default_file_stem}.{ext}"
            file_path.write_text(content, encoding="utf-8")
            console.print(f"  ✔ [dim]{target_fmt.upper():<12}[/dim] -> {file_path.name}")

        html_file = out_dir / f"{default_file_stem}.html"
        console.print("[bold green]✔ All formats compiled successfully![/bold green]")
        if open_browser and html_file.exists():
            webbrowser.open(f"file://{html_file.resolve()}")
        return

    if not output and fmt in ("html", "svg"):
        output = f"{default_file_stem}.{FORMAT_EXTENSIONS[fmt]}"

    result = _render_single(ir, fmt, orientation)

    if output:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(result, encoding="utf-8")
        console.print(f"[bold green]✔ Saved to:[/bold green] {output_path.resolve()}")
        if fmt in ("html", "svg") and open_browser:
            webbrowser.open(f"file://{output_path.resolve()}")
        return

    if fmt == "ascii":
        console.print(Panel(result, title="VizArc Architecture (ASCII)", border_style="green"))
    else:
        syntax_lang = (
            "python"
            if fmt == "structurizr"
            else (
                "xml"
                if fmt == "svg"
                else ("json" if fmt == "ir" else ("bash" if fmt in ("d2", "dot", "graphviz") else fmt))
            )
        )
        console.print(Panel(Syntax(result, syntax_lang, theme="monokai"), title=f"VizArc {fmt.upper()}", border_style="cyan"))


@click.group()
@click.version_option(version="0.4.0")
def main():
    """VizArc: Universal Architecture Compiler & Explainer Engine."""
    pass


@main.command()
@click.argument("prompt", required=True)
@click.option(
    "--format", "-f",
    type=click.Choice(ALL_FORMATS, case_sensitive=False),
    default="html",
    help="Target diagram format, or 'all' to compile into all formats simultaneously.",
)
@click.option(
    "--type", "-t", "archetype",
    type=click.Choice([
        "architecture", "workflow", "sequence", "dataflow", "lifecycle",
        "erd", "class", "tree", "timeline", "waterfall",
    ], case_sensitive=False),
    default=None,
    help="Diagram archetype (auto-detected from prompt if omitted).",
)
@click.option(
    "--output", "-o",
    type=click.Path(writable=True),
    default=None,
    help="Output file path (or output directory if --format=all).",
)
@click.option(
    "--orientation", "-O",
    type=click.Choice(["horizontal", "vertical"], case_sensitive=False),
    default="horizontal",
    help="Layout direction for SVG renderer (horizontal LR vs vertical TB).",
)
@click.option(
    "--open", "open_browser",
    is_flag=True,
    default=False,
    help="Open generated HTML/SVG in browser.",
)
def generate(prompt: str, format: str, archetype: Optional[str], output: Optional[str], orientation: str, open_browser: bool):
    """Generate architecture diagrams from a prompt specification."""
    engine = VizArcEngine()
    console.print(f"[bold cyan]VizArc[/bold cyan] compiling to [green]{format.upper()}[/green]...")
    ir = engine.generate_ir(prompt=prompt, archetype=archetype)
    _write_or_print_output(ir, format, output, orientation, open_browser)


@main.command(name="compile")
@click.argument("ir_source", required=True)
@click.option(
    "--format", "-f",
    type=click.Choice(ALL_FORMATS, case_sensitive=False),
    default="html",
    help="Target diagram format, or 'all' to compile into all formats simultaneously.",
)
@click.option(
    "--output", "-o",
    type=click.Path(writable=True),
    default=None,
    help="Output file path (or output directory if --format=all).",
)
@click.option(
    "--orientation", "-O",
    type=click.Choice(["horizontal", "vertical"], case_sensitive=False),
    default="horizontal",
    help="Layout direction for SVG renderer (horizontal LR vs vertical TB).",
)
@click.option(
    "--strict",
    is_flag=True,
    default=False,
    help="Abort with exit code 1 if static architecture validation finds errors.",
)
@click.option(
    "--open", "open_browser",
    is_flag=True,
    default=False,
    help="Open generated HTML/SVG in browser.",
)
def compile_ir(ir_source: str, format: str, output: Optional[str], orientation: str, strict: bool, open_browser: bool):
    """Compile a Canonical Architecture IR JSON file (or '-' for stdin) deterministically with zero LLM calls."""
    try:
        raw_ir = _load_ir_payload(ir_source)
        ir = validate_ir(raw_ir)
    except Exception as exc:
        console.print(f"[bold red]Compile Error:[/bold red] {exc}")
        sys.exit(1)

    lint = lint_ir(ir)
    if lint["error_count"] > 0:
        for diag in lint["diagnostics"]:
            if diag["severity"] == "error":
                console.print(f"[bold red]✖ {diag['ruleCode']}:[/bold red] {diag['message']}")
        if strict:
            sys.exit(1)

    _write_or_print_output(ir, format, output, orientation, open_browser)


@main.command()
@click.argument("path", default=".", type=click.Path(exists=True))
@click.option(
    "--format", "-f",
    type=click.Choice(ALL_FORMATS, case_sensitive=False),
    default="html",
    help="Target format (default: html).",
)
@click.option(
    "--output", "-o",
    type=click.Path(writable=True),
    default=None,
    help="File path to save output.",
)
@click.option(
    "--orientation", "-O",
    type=click.Choice(["horizontal", "vertical"], case_sensitive=False),
    default="horizontal",
    help="Layout direction for SVG renderer (horizontal LR vs vertical TB).",
)
@click.option(
    "--open", "open_browser",
    is_flag=True,
    default=False,
    help="Automatically open HTML in browser.",
)
def scan(path: str, format: str, output: Optional[str], orientation: str, open_browser: bool):
    """Scan a local directory/codebase and compile architecture diagrams."""
    console.print(f"[bold cyan]VizArc scanning repository:[/bold cyan] {path}...")
    analyzer = CodebaseAnalyzer(path)
    analysis = analyzer.analyze()
    context = analyzer.format_summary_for_prompt(analysis)

    frameworks = ", ".join(analysis["detected_frameworks"]) or "None detected"
    console.print(f"[dim]Frameworks found: {frameworks}[/dim]")

    prompt = f"Map the architectural components, service layers, and data flow for the {analysis['root_name']} project."
    engine = VizArcEngine()
    ir = engine.generate_ir(prompt=prompt, codebase_context=context)

    if not output and format not in ("all", "html", "svg"):
        output = f"ARCHITECTURE.{FORMAT_EXTENSIONS.get(format, 'txt')}"

    _write_or_print_output(ir, format, output, orientation, open_browser)


@main.command()
def templates():
    """List all 13 built-in production architecture templates (vizarch presets)."""
    table = Table(title="📐 VizArc Preset Architecture Templates", border_style="cyan")
    table.add_column("Template ID", style="bold green")
    table.add_column("Name", style="bold white")
    table.add_column("Description", style="dim")

    for t in TEMPLATES:
        table.add_row(t["id"], t["name"], t["description"])

    console.print(table)
    console.print("[dim]Render any template with: [bold cyan]vizarc template <id> [--format svg|html|all][/bold cyan][/dim]")


@main.command()
@click.argument("template_id", required=True)
@click.option(
    "--format", "-f",
    type=click.Choice(ALL_FORMATS, case_sensitive=False),
    default="html",
    help="Target format (html, svg, d2, mermaid, all, etc.).",
)
@click.option(
    "--output", "-o",
    type=click.Path(writable=True),
    default=None,
    help="Output file path (or folder if --format=all).",
)
@click.option(
    "--orientation", "-O",
    type=click.Choice(["horizontal", "vertical"], case_sensitive=False),
    default="horizontal",
    help="Orientation for SVG renderer (horizontal LR vs vertical TB).",
)
@click.option(
    "--open", "open_browser",
    is_flag=True,
    default=False,
    help="Open generated diagram in browser.",
)
def template(template_id: str, format: str, output: Optional[str], orientation: str, open_browser: bool):
    """Render a preset architecture template directly (100% offline)."""
    tpl = get_template(template_id)
    if not tpl:
        console.print(f"[bold red]Error:[/bold red] Template '{template_id}' not found.")
        console.print("Run [bold cyan]vizarc templates[/bold cyan] to see available IDs.")
        sys.exit(1)

    ir = tpl["ir"]
    console.print(f"[bold cyan]Rendering template:[/bold cyan] [bold white]{tpl['name']}[/bold white] to [green]{format.upper()}[/green]...")

    if not output and format not in ("all", "html", "svg"):
        output = f"{template_id}.{FORMAT_EXTENSIONS.get(format, 'txt')}"

    _write_or_print_output(
        ir,
        format,
        output,
        orientation,
        open_browser,
        default_file_stem=template_id,
        default_all_dir=f"./template_{template_id}",
        include_ir_in_all=False,
    )


@main.command()
@click.argument("prompt", required=True)
def guide(prompt: str):
    """Recommend the optimal diagram archetype and generate an optimized prompt specification."""
    engine = VizArcEngine()
    analysis = engine.guide(prompt)

    console.print(Panel(
        f"[bold white]{analysis['archetype_name']}[/bold white] ([cyan]{analysis['detected_archetype']}[/cyan])\n"
        f"[dim]{analysis['description']}[/dim]",
        title="🎯 Recommended Archetype",
        border_style="cyan",
    ))

    table = Table(title="Recommended Layer Hierarchy", border_style="dim")
    table.add_column("Tier ID", style="cyan")
    table.add_column("Layer Name", style="bold white")
    table.add_column("Accent Color", style="yellow")
    for tier in analysis["recommended_tiers"]:
        table.add_row(tier["id"], tier["label"], tier["color"])
    console.print(table)

    console.print(Panel(
        analysis["suggested_prompt"],
        title="✨ Optimized Prompt (Ready to Compile)",
        border_style="green",
    ))

    console.print(
        f"[dim]Run directly: [bold cyan]vizarc generate \"{analysis['suggested_prompt']}\" --type {analysis['detected_archetype']}[/bold cyan][/dim]"
    )


@main.command()
@click.argument("target", required=True, type=click.Path(exists=True))
@click.option(
    "--orientation", "-O",
    type=click.Choice(["horizontal", "vertical"], case_sensitive=False),
    default="horizontal",
    help="Orientation used for SVG layout collision checking.",
)
@click.option(
    "--no-layout",
    is_flag=True,
    default=False,
    help="Skip SVG bounding-box & label-clearance checks.",
)
def validate(target: str, orientation: str, no_layout: bool):
    """Machine-readable architectural static and layout clearance analysis."""
    engine = VizArcEngine()
    content = Path(target).read_text(encoding="utf-8")

    try:
        results = engine.validate(content, check_layout=not no_layout, orientation=orientation)
    except Exception as e:
        console.print(f"[bold red]Validation Error:[/bold red] Failed to parse {target}: {e}")
        sys.exit(1)

    console.print(f"\n[bold cyan]VizArc Static & Layout Validator[/bold cyan] -> {target}")
    console.print(
        f"  Archetype: [bold green]{results['archetype']}[/bold green] | Nodes: {results['node_count']} | Edges: {results['edge_count']}"
    )
    console.print(
        f"  Errors: [bold {'red' if results['error_count'] else 'green'}]{results['error_count']}[/] | Warnings: [bold {'yellow' if results['warning_count'] else 'dim'}]{results['warning_count']}[/]\n"
    )

    if not results["diagnostics"]:
        console.print("[bold green]✔ Architecture passed all static & layout validation checks! 100% compliant.[/bold green]\n")
        return

    table = Table(title="Architectural Diagnostics", border_style="cyan")
    table.add_column("Severity", style="bold")
    table.add_column("Rule Code", style="dim")
    table.add_column("Target", style="cyan")
    table.add_column("Message", style="white")
    table.add_column("Fixes", style="dim")

    for d in results["diagnostics"]:
        sev = d["severity"].upper()
        sev_style = "bold red" if sev == "ERROR" else ("bold yellow" if sev == "WARNING" else "dim")
        tgt = d.get("nodeId") or d.get("edge") or "Graph"
        fixes = ", ".join(d.get("supportedFixes", []))
        table.add_row(f"[{sev_style}]{sev}[/]", d["ruleCode"], tgt, d["message"], fixes)

    console.print(table)
    if results["error_count"] > 0:
        sys.exit(1)


@main.command(name="browser-check")
@click.argument("target", required=True, type=click.Path(exists=True))
def browser_check(target: str):
    """Verify generated VizArc HTML rendering via DOM & headless browser checks."""
    engine = VizArcEngine()
    report = engine.browser_check(target)

    console.print(f"\n[bold cyan]VizArc Browser QA Check[/bold cyan] -> {target}")
    console.print(f"  Engine: [bold]{report['browser']}[/bold] | Expected: {report['expected_nodes']} nodes, {report['expected_edges']} edges")
    if report["rendered_nodes"] is not None:
        console.print(
            f"  Rendered DOM: {report['rendered_nodes']} nodes, {report['rendered_edges']} edges | Explainer: {'✔' if report['explainer_rendered'] else '✖'}"
        )

    if report["issues"]:
        for issue in report["issues"]:
            console.print(f"  [bold red]✖ [{issue['check']}][/bold red] {issue['message']}")
        sys.exit(1)

    console.print("[bold green]✔ HTML explainer passed browser QA checks![/bold green]\n")


@main.command()
@click.argument("base_path", required=True, type=click.Path(exists=True))
@click.argument("head_path", required=True, type=click.Path(exists=True))
@click.option(
    "--format", "-f",
    type=click.Choice(["terminal", "html", "json"], case_sensitive=False),
    default="terminal",
    help="Output format: terminal summary, interactive Before/Delta/After HTML, or JSON.",
)
@click.option(
    "--output", "-o",
    type=click.Path(writable=True),
    default=None,
    help="Output file path (defaults to architecture_diff.html for --format html).",
)
@click.option(
    "--open", "open_browser",
    is_flag=True,
    default=False,
    help="Open generated HTML diff in browser.",
)
def compare(base_path: str, head_path: str, format: str, output: Optional[str], open_browser: bool):
    """Architecture delta and visual diff analyzer (terminal, JSON, or Before/Delta/After HTML)."""
    engine = VizArcEngine()

    try:
        base_ir = _load_ir_payload(base_path)
        head_ir = _load_ir_payload(head_path)
    except Exception as e:
        console.print(f"[bold red]Compare Error:[/bold red] {e}")
        sys.exit(1)

    fmt = format.lower()
    if fmt == "html":
        html_out = engine.compare_html(base_ir, head_ir)
        out_path = Path(output or "architecture_diff.html")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html_out, encoding="utf-8")
        console.print(f"[bold green]✔ Visual architecture diff saved to:[/bold green] {out_path.resolve()}")
        if open_browser:
            webbrowser.open(f"file://{out_path.resolve()}")
        return

    diff = engine.compare(base_ir, head_ir)
    if fmt == "json":
        payload = json.dumps(diff, indent=2)
        if output:
            Path(output).write_text(payload, encoding="utf-8")
            console.print(f"[bold green]✔ JSON diff saved to:[/bold green] {Path(output).resolve()}")
        else:
            console.print(payload)
        return

    delta = diff["delta"]

    console.print(Panel(
        f"[bold white]{diff['summary']}[/bold white]",
        title=f"📐 Architecture Delta: {Path(base_path).name} ➔ {Path(head_path).name}",
        border_style="cyan",
    ))

    if delta["added_nodes"]:
        table = Table(title="➕ Added Nodes", border_style="green")
        table.add_column("ID", style="cyan")
        table.add_column("Label", style="bold white")
        table.add_column("Tier", style="yellow")
        table.add_column("Tech", style="dim")
        for n in delta["added_nodes"]:
            table.add_row(n["id"], n["label"], n["tier"], n.get("tech", ""))
        console.print(table)

    if delta["removed_nodes"]:
        table = Table(title="➖ Removed Nodes", border_style="red")
        table.add_column("ID", style="cyan")
        table.add_column("Label", style="bold white")
        table.add_column("Tier", style="yellow")
        for n in delta["removed_nodes"]:
            table.add_row(n["id"], n["label"], n["tier"])
        console.print(table)

    if delta["modified_nodes"]:
        table = Table(title="✏️ Modified Nodes", border_style="yellow")
        table.add_column("ID", style="cyan")
        table.add_column("Changes", style="white")
        for n in delta["modified_nodes"]:
            ch_str = "; ".join([f"{k}: {v['before']} ➔ {v['after']}" for k, v in n["changes"].items()])
            table.add_row(n["id"], ch_str)
        console.print(table)


@main.command()
@click.argument("path", default=".", type=click.Path(exists=True))
def diagnose(path: str):
    """Deep codebase architecture diagnosis: cycles, coupling hotspots, and archetypes."""
    engine = VizArcEngine()
    results = engine.diagnose(path)

    console.print(Panel(
        f"[bold white]{results['summary']}[/bold white]\n"
        f"Recommended Archetype: [bold green]{results['recommended_archetype'].upper()}[/bold green]",
        title=f"🔍 Codebase Architecture Diagnosis: {results['root_name']}",
        border_style="cyan",
    ))

    if results["circular_dependencies"]:
        console.print("[bold red]⚠️ Circular Dependencies Detected:[/bold red]")
        for c in results["circular_dependencies"]:
            console.print(f"  🔄 [red]{c}[/red]")
    else:
        console.print("[bold green]✔ Zero circular dependencies detected across internal modules.[/bold green]")

    if results["coupling_hotspots"]:
        table = Table(title="🔥 Architectural Coupling Hotspots (Fan-In / Fan-Out)", border_style="yellow")
        table.add_column("Module", style="bold white")
        table.add_column("Fan-In (Callers)", style="green")
        table.add_column("Fan-Out (Dependencies)", style="yellow")
        table.add_column("Total Coupling", style="cyan")
        for h in results["coupling_hotspots"]:
            table.add_row(h["module"], str(h["fan_in"]), str(h["fan_out"]), str(h["total"]))
        console.print(table)


SKILL_PLATFORMS = {
    "claude": {
        "label": "Claude Code",
        "repo_rel": Path(".claude") / "skills" / "vizarc",
        "global_dir": Path.home() / ".claude" / "skills" / "vizarc",
        "project_dir": Path(".claude") / "skills" / "vizarc",
    },
    "antigravity": {
        "label": "Google Antigravity",
        "repo_rel": Path(".agent") / "skills" / "vizarc",
        "global_dir": Path.home() / ".gemini" / "antigravity" / "skills" / "vizarc",
        "project_dir": Path(".agent") / "skills" / "vizarc",
    },
    "codex": {
        "label": "OpenAI Codex",
        "repo_rel": Path(".agents") / "skills" / "vizarc",
        "global_dir": Path.home() / ".codex" / "skills" / "vizarc",
        "project_dir": Path(".agents") / "skills" / "vizarc",
    },
    "cursor": {
        "label": "Cursor",
        "repo_rel": Path(".agents") / "skills" / "vizarc",
        "global_dir": Path.home() / ".cursor" / "skills" / "vizarc",
        "project_dir": Path(".cursor") / "skills" / "vizarc",
    },
    "copilot": {
        "label": "GitHub Copilot",
        "repo_rel": Path(".agents") / "skills" / "vizarc",
        "global_dir": Path.home() / ".copilot" / "skills" / "vizarc",
        "project_dir": Path(".github") / "skills" / "vizarc",
    },
    "opencode": {
        "label": "OpenCode",
        "repo_rel": Path(".agents") / "skills" / "vizarc",
        "global_dir": Path.home() / ".config" / "opencode" / "skills" / "vizarc",
        "project_dir": Path(".opencode") / "skills" / "vizarc",
    },
}


@main.command(name="install-skill")
@click.option(
    "--platform", "-p",
    type=click.Choice(["claude", "antigravity", "codex", "cursor", "copilot", "opencode", "all"], case_sensitive=False),
    default="all",
    help="Target AI coding platform (or 'all').",
)
@click.option(
    "--scope", "-s",
    type=click.Choice(["global", "project", "both"], case_sensitive=False),
    default="global",
    help="Install globally (~/.claude, ~/.gemini/antigravity, ~/.codex), project-locally, or both.",
)
def install_skill(platform: str, scope: str):
    """Install the VizArc skill for Claude Code, Google Antigravity, and/or OpenAI Codex."""
    repo_root = Path(__file__).resolve().parent.parent.parent
    shared_refs = repo_root / "shared" / "references"
    if not shared_refs.exists():
        console.print(f"[bold red]Error:[/bold red] Shared references directory not found at {shared_refs}")
        sys.exit(1)

    selected = list(SKILL_PLATFORMS.keys()) if platform.lower() == "all" else [platform.lower()]

    for plat in selected:
        cfg = SKILL_PLATFORMS[plat]
        source_skill_file = repo_root / cfg["repo_rel"] / "SKILL.md"
        if not source_skill_file.exists():
            console.print(f"[bold red]Error:[/bold red] Missing {cfg['label']} SKILL.md at {source_skill_file}")
            sys.exit(1)

        targets = []
        if scope in ("global", "both"):
            targets.append(cfg["global_dir"])
        if scope in ("project", "both"):
            targets.append(Path.cwd() / cfg["project_dir"])

        skill_content = source_skill_file.read_text(encoding="utf-8").replace(
            "../../../shared/references/ir-schema.md",
            "references/ir-schema.md",
        )

        for dest in targets:
            if dest.resolve() == source_skill_file.parent.resolve():
                console.print(f"[dim]Skipping identical repo directory for {cfg['label']}: {dest}[/dim]")
                continue
            dest.mkdir(parents=True, exist_ok=True)
            (dest / "SKILL.md").write_text(skill_content, encoding="utf-8")
            shutil.copytree(shared_refs, dest / "references", dirs_exist_ok=True)
            console.print(f"[bold green]✔ Installed {cfg['label']} skill to:[/bold green] {dest}")


@main.command()
def doctor():
    """Verify environment setup, Gemini API key, Python version, and asset integrity."""
    import platform

    console.print("[bold cyan]🩺 VizArc Doctor: System & Environment Diagnostic[/bold cyan]\n")

    py_ver = platform.python_version()
    major, minor = sys.version_info[:2]
    py_ok = (major, minor) >= (3, 12)
    console.print(f"  [{'green' if py_ok else 'red'}]{'✔' if py_ok else '✖'}[/] Python Version: {py_ver} (>= 3.12 required)")

    deps = ["streamlit", "rich", "click", "google.generativeai", "dotenv", "PIL"]
    for d in deps:
        try:
            __import__(d)
            console.print(f"  [green]✔[/green] Dependency '{d}': installed")
        except ImportError:
            console.print(f"  [red]✖[/red] Dependency '{d}': missing")

    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        masked = api_key[:6] + "..." + api_key[-4:] if len(api_key) > 10 else "SET"
        console.print(f"  [green]✔[/green] GEMINI_API_KEY: Configured ({masked})")
    else:
        console.print("  [yellow]![/yellow] GEMINI_API_KEY: Not set (agent IR compilation & presets work offline)")

    repo_root = Path(__file__).resolve().parent.parent.parent
    assets_dir = Path.cwd() / "assets"
    if not assets_dir.exists():
        assets_dir = repo_root / "assets"
    universal_logo = assets_dir / "social" / "github-social-preview-dark.png"
    if universal_logo.exists():
        console.print(f"  [green]✔[/green] Universal README Banner: Found ({universal_logo.stat().st_size} bytes)")
    else:
        console.print(f"  [yellow]![/yellow] Universal README Banner: Not found at {universal_logo}")

    console.print(f"  [green]✔[/green] Built-in Architecture Presets: {len(TEMPLATES)} templates loaded")

    for cfg in SKILL_PLATFORMS.values():
        global_skill = cfg["global_dir"] / "SKILL.md"
        if global_skill.exists():
            console.print(f"  [green]✔[/green] {cfg['label']} Global Skill: Installed ({global_skill})")
        else:
            console.print(f"  [yellow]![/yellow] {cfg['label']} Global Skill: Not installed (run 'vizarc install-skill')")

    console.print("\n[bold green]Doctor check complete![/bold green]")


if __name__ == "__main__":
    main()
