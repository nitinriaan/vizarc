"""
VizArc CLI: Generate architecture diagrams from prompts or local codebases.
"""

import sys
from pathlib import Path

# Ensure src/ is on sys.path for local execution
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import click
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from vizarc.analyzer import CodebaseAnalyzer
from vizarc.engine import VizArcEngine

console = Console()

@click.group()
@click.version_option(version="0.1.0")
def main():
    """VizArc: AI-powered software architecture and diagram engine."""

@main.command()
@click.argument("prompt", required=True)
@click.option(
    "--format", "-f",
    type=click.Choice(["mermaid", "d2", "ascii", "excalidraw"], case_sensitive=False),
    default="mermaid",
    help="Target diagram format (default: mermaid)."
)
@click.option(
    "--archetype", "-a",
    type=click.Choice(["architecture", "sequence", "flowchart", "erd"], case_sensitive=False),
    default="architecture",
    help="Diagram type / structure (default: architecture)."
)
@click.option(
    "--output", "-o",
    type=click.Path(writable=True),
    default=None,
    help="Optional file path to save the generated diagram."
)
def generate(prompt: str, format: str, archetype: str, output: str):
    """Generate an architecture diagram from a prompt specification."""
    console.print(f"[bold cyan]VizArc[/bold cyan] generating [green]{format.upper()}[/green] ({archetype})...")

    engine = VizArcEngine()
    try:
        diagram = engine.generate(prompt=prompt, diagram_format=format, archetype=archetype)
    except (RuntimeError, ValueError, OSError) as e:
        console.print(f"[bold red]Generation Error:[/bold red] {e}")
        sys.exit(1)

    # Render output to terminal
    if format == "ascii":
        console.print(Panel(diagram, title=f"VizArc Output ({archetype})", border_style="green"))
    else:
        syntax = Syntax(diagram, format if format != "d2" else "bash", theme="monokai", line_numbers=True)
        console.print(Panel(syntax, title=f"VizArc {format.upper()} Diagram", border_style="cyan"))

    if output:
        output_path = Path(output)
        output_path.write_text(diagram, encoding="utf-8")
        console.print(f"[bold green]Saved diagram to:[/bold green] {output_path.resolve()}")

@main.command()
@click.argument("path", default=".", type=click.Path(exists=True))
@click.option(
    "--format", "-f",
    type=click.Choice(["mermaid", "d2", "ascii", "excalidraw"], case_sensitive=False),
    default="mermaid",
    help="Target diagram format."
)
@click.option(
    "--output", "-o",
    type=click.Path(writable=True),
    default="ARCHITECTURE.md",
    help="File path to save the diagram (default: ARCHITECTURE.md)."
)
def scan(path: str, format: str, output: str):
    """Scan a local directory/codebase and generate its system architecture diagram."""
    console.print(f"[bold cyan]VizArc scanning directory:[/bold cyan] {path}...")
    
    analyzer = CodebaseAnalyzer(path)
    analysis = analyzer.analyze()
    context = analyzer.format_summary_for_prompt(analysis)

    frameworks = ", ".join(analysis["detected_frameworks"]) or "None detected"
    console.print(f"[dim]Frameworks found: {frameworks}[/dim]")

    prompt = f"Map the architectural components, service layers, and data flow for the {analysis['root_name']} project."
    
    engine = VizArcEngine()
    diagram = engine.generate(
        prompt=prompt,
        diagram_format=format,
        archetype="architecture",
        codebase_context=context
    )

    content_to_save = diagram
    if output.endswith(".md") and format == "mermaid":
        content_to_save = f"# Architecture: {analysis['root_name']}\n\n```mermaid\n{diagram}\n```\n"

    output_path = Path(output)
    output_path.write_text(content_to_save, encoding="utf-8")
    console.print(f"[bold green]Successfully generated architecture diagram in:[/bold green] {output_path.resolve()}")

if __name__ == "__main__":
    main()
