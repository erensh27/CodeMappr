import os
from rich.console import Console
from typer.testing import CliRunner
import codemappr.display
import codemappr.cli
from codemappr.cli import app

def generate_terminal_screenshot():
    console = Console(record=True, width=100, force_terminal=True)

    # Patch consoles
    codemappr.display.console = console
    codemappr.cli.console = console

    runner = CliRunner()
    # Run scan
    runner.invoke(app, ["scan", "."])

    # Save HTML
    console.save_html("docs/screenshots/terminal_output.html", theme=None) # Default dark theme

if __name__ == "__main__":
    os.makedirs("docs/screenshots", exist_ok=True)
    generate_terminal_screenshot()
