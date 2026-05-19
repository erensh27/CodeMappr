import typer
from typing import Optional
from rich.console import Console
from codemappr.walker import scan_directory

app = typer.Typer(help="CodeMappr: Instantly understand any codebase.")
console = Console()

@app.command()
def scan(
    path: str = typer.Argument(".", help="Path to scan"),
    depth: Optional[int] = typer.Option(None, "--depth", help="Maximum depth to scan (None for unlimited)"),
    ignore: Optional[str] = typer.Option(None, "--ignore", help="Additional patterns to ignore (comma separated)")
):
    """
    Scan a directory and build a codebase map.
    """
    ignore_patterns = None
    if ignore:
        ignore_patterns = [p.strip() for p in ignore.split(",")]

    scan_directory(path, depth=depth, ignore_patterns=ignore_patterns)
    console.print("[green]Scan complete[/green]")

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        console.print("CodeMappr CLI")
        console.print("Use --help for usage")

if __name__ == "__main__":
    app()
