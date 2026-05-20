import os
from playwright.sync_api import sync_playwright

def capture_screenshots():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1200, "height": 1000})
        page = context.new_page()

        # 1. Terminal View
        # Use file path for the generated terminal HTML
        html_path = os.path.abspath("docs/screenshots/terminal_output.html")
        page.goto(f"file://{html_path}")
        page.wait_for_timeout(1000)
        # Find the element that contains the terminal output
        # Rich HTML usually has a <pre class="rich-terminal"> or similar
        container = page.locator("body")
        container.screenshot(path="docs/screenshots/terminal-view.png")
        print("Captured terminal-view.png")

        # 2. Markdown Export
        # First generate the MD
        os.system("codemappr scan . --format md --output docs/screenshots/DEMO.md")
        # To "view" it rendered, we could use a library, but maybe we can just show the terminal confirmation for now?
        # Actually, let's try to render it simply or just take a screenshot of the terminal confirming it.
        # The prompt says: "Capture the terminal confirmation message + open the generated CODEMAPPR.md rendered in a markdown viewer or GitHub preview."
        # Rendering MD in headless env is tricky without a server.
        # I'll create a simple HTML wrapper to show the MD content.
        with open("docs/screenshots/DEMO.md", "r") as f:
            md_content = f.read()

        md_html = f"<html><body style='background:#0d1117; color:#c9d1d9; font-family: sans-serif; padding: 40px;'><pre>{md_content}</pre></body></html>"
        with open("docs/screenshots/md_preview.html", "w") as f:
            f.write(md_html)

        page.goto(f"file://{os.path.abspath('docs/screenshots/md_preview.html')}")
        page.screenshot(path="docs/screenshots/markdown-export.png")
        print("Captured markdown-export.png")

        # 3. HTML Export
        os.system("codemappr scan . --format html --output docs/screenshots/DEMO.html")
        page.goto(f"file://{os.path.abspath('docs/screenshots/DEMO.html')}")
        page.wait_for_timeout(1000)
        page.screenshot(path="docs/screenshots/html-export.png", full_page=True)
        print("Captured html-export.png")

        # 4. All formats
        # We need to capture the terminal output for this one.
        # Similar to terminal-view but specifically for the 'all' command output.
        # I'll use a simplified version.
        from rich.console import Console
        from typer.testing import CliRunner
        from codemappr.cli import app
        import codemappr.cli
        import codemappr.display

        console = Console(record=True, width=100, force_terminal=True)
        codemappr.cli.console = console
        codemappr.display.console = console
        runner = CliRunner()
        runner.invoke(app, ["scan", ".", "--format", "all"])
        console.save_html("docs/screenshots/format_all_output.html")

        page.goto(f"file://{os.path.abspath('docs/screenshots/format_all_output.html')}")
        # Wait for content to be sure
        page.wait_for_timeout(1000)
        page.screenshot(path="docs/screenshots/format-all.png", full_page=True)
        print("Captured format-all.png")

        browser.close()

if __name__ == "__main__":
    capture_screenshots()
