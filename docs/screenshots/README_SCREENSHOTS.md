# README Screenshots
This directory contains screenshots used in the main README.md.

## How to regenerate screenshots
To regenerate these screenshots after UI changes, follow these steps:

1.  **Terminal View**:
    Run `codemappr scan .` in a terminal that supports Rich output (iTerm2, Windows Terminal, Kitty) and take a screenshot of the output.
2.  **Markdown Export**:
    Run `codemappr scan . --format md` and capture the terminal confirmation. Then, open `CODEMAPPR.md` in a Markdown viewer or GitHub preview and take a screenshot.
3.  **HTML Export**:
    Run `codemappr scan . --format html` and open the generated `CODEMAPPR.html` in a browser.
4.  **All formats**:
    Run `codemappr scan . --format all` and capture the terminal output showing file generation.

Recommended tools for high-quality screenshots:
- iTerm2 (macOS)
- Windows Terminal (Windows)
- Kitty (Linux/macOS)
- Playwright (Automated regeneration)
