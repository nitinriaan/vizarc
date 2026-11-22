"""
VizArc CLI: Universal Architecture Compiler & Explainer Engine.
Compiles from a single Canonical Architecture Model into 8 formats:
HTML (Interactive), D2, Structurizr C4, Mermaid, PlantUML, Graphviz DOT, Excalidraw, and ASCII.
"""

import sys
import webbrowser
from pathlib import Path
import click
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

# Ensure src/ is on sys.path for local execution
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from vizarc.engine import VizArcEngine
from vizarc.analyzer import CodebaseAnalyzer

console = Console()

FORMAT_EXTENSIONS = {
    "html": "html",
    "d2": "d2",
    "mermaid": "mmd",
    "structurizr": "dsl",
    "plantuml": "puml",
    "graphviz": "dot",
    "excalidraw": "excalidraw.mmd",
    "ascii": "txt"
}

@click.group()
@click.version_option(version="0.3.0")
def main():
    """VizArc: Universal Architecture Compiler & Explainer Engine."""
    pass

@main.command()
@click.argument("prompt", required=True)
@click.option(
    "--format", "-f",
    type=click.Choice(["html", "d2", "mermaid", "structurizr", "plantuml", "graphviz", "excalidraw", "ascii", "all"], case_sensitive=False),
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
    "--open", "open_browser",
    is_flag=True,
    default=False,
    help="Open generated HTML in browser."
)
def generate(prompt: str, format: str, output: str, open_browser: bool):
    """Generate architecture diagrams from a prompt specification."""
    engine = VizArcEngine()

    if format == "all":
        out_dir = Path(output or "./vizarc_out")
        out_dir.mkdir(parents=True, exist_ok=True)
        console.print(f"[bold cyan]VizArc[/bold cyan] compiling [bold green]all 8 formats[/bold green] to {out_dir.resolve()}...")

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
    if not output and format == "html":
        output = "architecture.html"

    result = engine.generate(prompt=prompt, diagram_format=format)

    if output:
        output_path = Path(output)
        output_path.write_text(result, encoding="utf-8")
        console.print(f"[bold green]✔ Saved to:[/bold green] {output_path.resolve()}")
        if format == "html" and open_browser:
            webbrowser.open(f"file://{output_path.resolve()}")
    else:
        # Display in terminal
        if format == "ascii":
            console.print(Panel(result, title="VizArc Architecture (ASCII)", border_style="green"))
        else:
            syntax_lang = "python" if format == "structurizr" else ("bash" if format in ("d2", "dot", "graphviz") else format)
            console.print(Panel(Syntax(result, syntax_lang, theme="monokai"), title=f"VizArc {format.upper()}", border_style="cyan"))

@main.command()
@click.argument("path", default=".", type=click.Path(exists=True))
@click.option(
    "--format", "-f",
    type=click.Choice(["html", "d2", "mermaid", "structurizr", "plantuml", "graphviz", "ascii", "all"], case_sensitive=False),
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

if __name__ == "__main__":
    main()
