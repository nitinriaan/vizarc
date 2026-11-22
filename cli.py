"""
VizArc CLI: Generate interactive architecture explainers, diagrams, and codebase maps.
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

@click.group()
@click.version_option(version="0.2.0")
def main():
    """VizArc: AI-powered interactive architecture explainer & diagram engine."""
    pass

@main.command()
@click.argument("prompt", required=True)
@click.option(
    "--format", "-f",
    type=click.Choice(["html", "mermaid", "d2", "ascii", "excalidraw"], case_sensitive=False),
    default="html",
    help="Target format: 'html' (interactive explainer), 'mermaid', 'd2', 'ascii', 'excalidraw'."
)
@click.option(
    "--archetype", "-a",
    type=click.Choice(["architecture", "sequence", "flowchart", "erd"], case_sensitive=False),
    default="architecture",
    help="Diagram structure / archetype (default: architecture)."
)
@click.option(
    "--output", "-o",
    type=click.Path(writable=True),
    default=None,
    help="Output file path (default: architecture.html for HTML, or terminal display)."
)
@click.option(
    "--open", "open_browser",
    is_flag=True,
    default=False,
    help="Automatically open the interactive HTML in your default browser."
)
def generate(prompt: str, format: str, archetype: str, output: str, open_browser: bool):
    """Generate an architecture explainer or diagram from a prompt specification."""
    console.print(f"[bold cyan]VizArc[/bold cyan] generating [green]{format.upper()}[/green] ({archetype})...")

    if format == "html" and not output:
        output = "architecture.html"

    engine = VizArcEngine()
    try:
        result = engine.generate(prompt=prompt, diagram_format=format, archetype=archetype)
    except Exception as e:
        console.print(f"[bold red]Generation Error:[/bold red] {e}")
        sys.exit(1)

    if output:
        output_path = Path(output)
        output_path.write_text(result, encoding="utf-8")
        console.print(f"[bold green]✔ Saved to:[/bold green] {output_path.resolve()}")
        if format == "html":
            console.print("[dim]Double-click the HTML file to open the interactive canvas with link tracing & search![/dim]")
            if open_browser:
                webbrowser.open(f"file://{output_path.resolve()}")
    else:
        # Display in terminal if text-based
        if format == "ascii":
            console.print(Panel(result, title=f"VizArc Output ({archetype})", border_style="green"))
        else:
            syntax = Syntax(result, format if format != "d2" else "bash", theme="monokai", line_numbers=True)
            console.print(Panel(syntax, title=f"VizArc {format.upper()}", border_style="cyan"))

@main.command()
@click.argument("path", default=".", type=click.Path(exists=True))
@click.option(
    "--format", "-f",
    type=click.Choice(["html", "mermaid", "d2", "ascii"], case_sensitive=False),
    default="html",
    help="Output format (default: html)."
)
@click.option(
    "--output", "-o",
    type=click.Path(writable=True),
    default=None,
    help="File path to save the explainer (default: architecture.html)."
)
@click.option(
    "--open", "open_browser",
    is_flag=True,
    default=False,
    help="Automatically open the interactive HTML in your browser."
)
def scan(path: str, format: str, output: str, open_browser: bool):
    """Scan a local directory/codebase and compile an interactive architecture explainer."""
    console.print(f"[bold cyan]VizArc scanning repository:[/bold cyan] {path}...")
    
    analyzer = CodebaseAnalyzer(path)
    analysis = analyzer.analyze()
    context = analyzer.format_summary_for_prompt(analysis)

    frameworks = ", ".join(analysis["detected_frameworks"]) or "None detected"
    console.print(f"[dim]Frameworks found: {frameworks}[/dim]")

    if not output:
        output = "architecture.html" if format == "html" else "ARCHITECTURE.md"

    prompt = f"Map the architectural components, service layers, and data flow for the {analysis['root_name']} project."
    
    engine = VizArcEngine()
    result = engine.generate(
        prompt=prompt,
        diagram_format=format,
        archetype="architecture",
        codebase_context=context
    )

    content_to_save = result
    if output.endswith(".md") and format == "mermaid":
        content_to_save = f"# Architecture: {analysis['root_name']}\n\n```mermaid\n{result}\n```\n"

    output_path = Path(output)
    output_path.write_text(content_to_save, encoding="utf-8")
    console.print(f"[bold green]✔ Successfully generated:[/bold green] {output_path.resolve()}")
    
    if format == "html":
        console.print("[dim]Double-click the HTML file to explore interactive link tracing, search, and details![/dim]")
        if open_browser:
            webbrowser.open(f"file://{output_path.resolve()}")

if __name__ == "__main__":
    main()
