import typer
import os
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from codemappr.walker import scan_directory
from codemappr.detector import detect_project
from codemappr.explainer import explain_project
from codemappr.display import render_terminal
from codemappr.exporter import export_markdown, export_html

app = typer.Typer(help="CodeMappr: Instantly understand any codebase.")
console = Console()
VERSION = "1.0.0"

def version_callback(value: bool):
    if value:
        console.print(f"CodeMappr v{VERSION}")
        raise typer.Exit()

@app.command()
def scan(
    path: str = typer.Argument(".", help="Path to scan"),
    depth: Optional[int] = typer.Option(None, "--depth", help="Maximum directory depth (default: unlimited)"),
    ignore: Optional[str] = typer.Option(None, "--ignore", help="Comma-separated patterns to ignore (adds to defaults)"),
    output: Optional[str] = typer.Option(None, "--output", help="Export file path (auto-detects format from extension: .md or .html)"),
    format: str = typer.Option("terminal", "--format", help='Force format: "terminal", "md", "html", "all" (default: "terminal")'),
    no_tree: bool = typer.Option(False, "--no-tree", help="Skip directory tree in output"),
    quiet: bool = typer.Option(False, "--quiet", help="Suppress terminal output (for CI use)"),
    version: Optional[bool] = typer.Option(None, "--version", callback=version_callback, is_eager=True, help="Show version and exit")
):
    """
    Scan a directory and build a codebase map.
    """
    # Error Handling: Path doesn't exist
    if not os.path.exists(path):
        console.print(Panel(f"[bold red]Error:[/bold red] Path [yellow]{path}[/yellow] does not exist.", border_style="red"))
        raise typer.Exit(code=1)

    ignore_patterns = []
    if ignore:
        ignore_patterns = [p.strip() for p in ignore.split(",")]

    try:
        node = scan_directory(path, depth=depth, ignore_patterns=ignore_patterns)

        # Error Handling: Empty directory
        if node.is_dir and not node.children:
             console.print(Panel(f"[bold yellow]Warning:[/bold yellow] Directory [yellow]{path}[/yellow] is empty.", border_style="yellow"))

        profile = detect_project(node, path)
        explanation = explain_project(profile, node)
    except Exception as e:
        console.print(Panel(f"[bold red]Error:[/bold red] {str(e)}", border_style="red"))
        raise typer.Exit(code=1)

    # Determine formats to export
    formats = [format.lower()]
    if format.lower() == "all":
        formats = ["terminal", "md", "html"]

    # Handle auto-detection of format from output extension
    if output and format == "terminal":
        if output.endswith(".md"):
            formats = ["md"]
        elif output.endswith(".html"):
            formats = ["html"]

    # Render Terminal
    if "terminal" in formats and not quiet:
        # We might need to temporarily modify 'node' if --no-tree is passed,
        # but render_terminal handles its own tree building.
        # Actually, let's pass a flag or handle it in display.py if we were to modify it.
        # Requirement: --no-tree Skip directory tree in output.
        # I'll modify render_terminal to accept show_tree if needed, or just clear children.
        if no_tree:
            original_children = node.children
            node.children = []
            render_terminal(node, profile, explanation)
            node.children = original_children
        else:
            render_terminal(node, profile, explanation)

    # Handle --no-tree for exports
    original_children = None
    if no_tree:
        original_children = node.children
        node.children = []

    # Export MD
    if "md" in formats or (format.lower() == "all"):
        out_path = output if (output and output.endswith(".md")) else "CODEMAPPR.md"
        export_markdown(node, profile, explanation, out_path)
        if not quiet:
            console.print(f"[bold green]✓[/bold green] Exported Markdown report to: [cyan]{out_path}[/cyan]")

    # Export HTML
    if "html" in formats or (format.lower() == "all"):
        out_path = output if (output and output.endswith(".html")) else "CODEMAPPR.html"
        export_html(node, profile, explanation, out_path)
        if not quiet:
            console.print(f"[bold green]✓[/bold green] Exported HTML report to: [cyan]{out_path}[/cyan]")

    # Restore children if they were cleared
    if original_children is not None:
        node.children = original_children

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        console.print("[bold cyan]CodeMappr CLI[/bold cyan]")
        console.print("Use [yellow]codemappr scan --help[/yellow] for usage")

if __name__ == "__main__":
    app()
