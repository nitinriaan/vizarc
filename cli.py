"""
VizArc CLI: Universal Architecture Compiler & Explainer Engine.
Compiles from a single Canonical Architecture Model into 9 formats:
HTML (Interactive), SVG (Vector), D2, Structurizr C4, Mermaid, PlantUML, Graphviz DOT, Excalidraw, and ASCII.
"""

import sys
import webbrowser
from pathlib import Path
import click
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

# Ensure src/ is on sys.path for local execution
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from vizarc.engine import VizArcEngine
from vizarc.analyzer import CodebaseAnalyzer
from vizarc.templates import TEMPLATES, get_template, list_templates
from vizarc.adapters import render_ir, render_all_formats
from vizarc.adapters.svg_adapter import render_svg_diagram

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
    "ascii": "txt"
}

ALL_FORMATS = ["html", "svg", "d2", "mermaid", "structurizr", "plantuml", "graphviz", "excalidraw", "ascii", "all"]

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
    help="Target diagram format, or 'all' to compile into all formats simultaneously."
)
@click.option(
    "--output", "-o",
    type=click.Path(writable=True),
    default=None,
    help="Output file path (or output directory if --format=all)."
)
@click.option(
    "--orientation", "-O",
    type=click.Choice(["horizontal", "vertical"], case_sensitive=False),
    default="horizontal",
    help="Layout direction for SVG renderer (horizontal LR vs vertical TB)."
)
@click.option(
    "--open", "open_browser",
    is_flag=True,
    default=False,
    help="Open generated HTML/SVG in browser."
)
def generate(prompt: str, format: str, output: str, orientation: str, open_browser: bool):
    """Generate architecture diagrams from a prompt specification."""
    engine = VizArcEngine()

    if format == "all":
        out_dir = Path(output or "./vizarc_out")
        out_dir.mkdir(parents=True, exist_ok=True)
        console.print(f"[bold cyan]VizArc[/bold cyan] compiling [bold green]all 9 formats[/bold green] to {out_dir.resolve()}...")

        all_renders = engine.generate_all(prompt)
        for fmt, content in all_renders.items():
            ext = FORMAT_EXTENSIONS.get(fmt, "txt") if fmt != "ir" else "json"
            file_path = out_dir / f"architecture.{ext}"
            file_path.write_text(content, encoding="utf-8")
            console.print(f"  ✔ [dim]{fmt.upper():<12}[/dim] -> {file_path.name}")

        html_file = out_dir / "architecture.html"
        console.print(f"[bold green]✔ All formats compiled successfully![/bold green]")
        if open_browser and html_file.exists():
            webbrowser.open(f"file://{html_file.resolve()}")
        return

    # Single format
    console.print(f"[bold cyan]VizArc[/bold cyan] compiling to [green]{format.upper()}[/green]...")
    if not output:
        if format == "html":
            output = "architecture.html"
        elif format == "svg":
            output = "architecture.svg"

    ir = engine.generate_ir(prompt=prompt)
    if format == "svg":
        result = render_svg_diagram(ir, orientation=orientation)
    else:
        result = render_ir(ir, target_format=format)

    if output:
        output_path = Path(output)
        output_path.write_text(result, encoding="utf-8")
        console.print(f"[bold green]✔ Saved to:[/bold green] {output_path.resolve()}")
        if format in ("html", "svg") and open_browser:
            webbrowser.open(f"file://{output_path.resolve()}")
    else:
        # Display in terminal
        if format == "ascii":
            console.print(Panel(result, title="VizArc Architecture (ASCII)", border_style="green"))
        else:
            syntax_lang = "python" if format == "structurizr" else ("xml" if format == "svg" else ("bash" if format in ("d2", "dot", "graphviz") else format))
            console.print(Panel(Syntax(result, syntax_lang, theme="monokai"), title=f"VizArc {format.upper()}", border_style="cyan"))

@main.command()
@click.argument("path", default=".", type=click.Path(exists=True))
@click.option(
    "--format", "-f",
    type=click.Choice(ALL_FORMATS, case_sensitive=False),
    default="html",
    help="Target format (default: html)."
)
@click.option(
    "--output", "-o",
    type=click.Path(writable=True),
    default=None,
    help="File path to save output."
)
@click.option(
    "--open", "open_browser",
    is_flag=True,
    default=False,
    help="Automatically open HTML in browser."
)
def scan(path: str, format: str, output: str, open_browser: bool):
    """Scan a local directory/codebase and compile architecture diagrams."""
    console.print(f"[bold cyan]VizArc scanning repository:[/bold cyan] {path}...")
    analyzer = CodebaseAnalyzer(path)
    analysis = analyzer.analyze()
    context = analyzer.format_summary_for_prompt(analysis)

    frameworks = ", ".join(analysis["detected_frameworks"]) or "None detected"
    console.print(f"[dim]Frameworks found: {frameworks}[/dim]")

    prompt = f"Map the architectural components, service layers, and data flow for the {analysis['root_name']} project."
    engine = VizArcEngine()

    if format == "all":
        out_dir = Path(output or "./vizarc_out")
        out_dir.mkdir(parents=True, exist_ok=True)
        all_renders = engine.generate_all(prompt, codebase_context=context)
        for fmt, content in all_renders.items():
            ext = FORMAT_EXTENSIONS.get(fmt, "txt") if fmt != "ir" else "json"
            (out_dir / f"architecture.{ext}").write_text(content, encoding="utf-8")
        console.print(f"[bold green]✔ All formats compiled to:[/bold green] {out_dir.resolve()}")
        if open_browser:
            webbrowser.open(f"file://{(out_dir / 'architecture.html').resolve()}")
        return

    if not output:
        output = "architecture.html" if format == "html" else f"ARCHITECTURE.{FORMAT_EXTENSIONS.get(format, 'txt')}"

    result = engine.generate(prompt=prompt, diagram_format=format, codebase_context=context)
    output_path = Path(output)
    output_path.write_text(result, encoding="utf-8")
    console.print(f"[bold green]✔ Saved to:[/bold green] {output_path.resolve()}")
    if format == "html" and open_browser:
        webbrowser.open(f"file://{output_path.resolve()}")

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
    console.print("[dim]Render any template with: [bold cyan]python cli.py template <id> [--format svg|html|all][/bold cyan][/dim]")

@main.command()
@click.argument("template_id", required=True)
@click.option(
    "--format", "-f",
    type=click.Choice(ALL_FORMATS, case_sensitive=False),
    default="html",
    help="Target format (html, svg, d2, mermaid, all, etc.)."
)
@click.option(
    "--output", "-o",
    type=click.Path(writable=True),
    default=None,
    help="Output file path (or folder if --format=all)."
)
@click.option(
    "--orientation", "-O",
    type=click.Choice(["horizontal", "vertical"], case_sensitive=False),
    default="horizontal",
    help="Orientation for SVG renderer (horizontal LR vs vertical TB)."
)
@click.option(
    "--open", "open_browser",
    is_flag=True,
    default=False,
    help="Open generated diagram in browser."
)
def template(template_id: str, format: str, output: str, orientation: str, open_browser: bool):
    """Render a preset architecture template directly (100% offline)."""
    tpl = get_template(template_id)
    if not tpl:
        console.print(f"[bold red]Error:[/bold red] Template '{template_id}' not found.")
        console.print("Run [bold cyan]python cli.py templates[/bold cyan] to see available IDs.")
        sys.exit(1)

    ir = tpl["ir"]
    console.print(f"[bold cyan]Rendering template:[/bold cyan] [bold white]{tpl['name']}[/bold white] to [green]{format.upper()}[/green]...")

    if format == "all":
        out_dir = Path(output or f"./template_{template_id}")
        out_dir.mkdir(parents=True, exist_ok=True)
        all_renders = render_all_formats(ir)
        for fmt, content in all_renders.items():
            ext = FORMAT_EXTENSIONS.get(fmt, "txt")
            (out_dir / f"{template_id}.{ext}").write_text(content, encoding="utf-8")
            console.print(f"  ✔ [dim]{fmt.upper():<12}[/dim] -> {template_id}.{ext}")
        console.print(f"[bold green]✔ All formats compiled to:[/bold green] {out_dir.resolve()}")
        if open_browser:
            webbrowser.open(f"file://{(out_dir / f'{template_id}.html').resolve()}")
        return

    if not output:
        output = f"{template_id}.{FORMAT_EXTENSIONS.get(format, 'txt')}"

    if format == "svg":
        result = render_svg_diagram(ir, orientation=orientation)
    else:
        result = render_ir(ir, target_format=format)

    output_path = Path(output)
    output_path.write_text(result, encoding="utf-8")
    console.print(f"[bold green]✔ Saved to:[/bold green] {output_path.resolve()}")
    if open_browser and format in ("html", "svg"):
        webbrowser.open(f"file://{output_path.resolve()}")

if __name__ == "__main__":
    main()
