import os
from datetime import datetime
from typing import Dict, Any
from .models import DirectoryNode, ProjectProfile
from .display import format_size

def _generate_ascii_tree(node: DirectoryNode, prefix: str = "") -> str:
    """Generates an ASCII representation of the directory tree."""
    lines = []
    children = node.children
    for i, child in enumerate(children):
        is_last = (i == len(children) - 1)
        connector = "└── " if is_last else "├── "
        icon = "📁 " if child.is_dir else "📄 "
        lines.append(f"{prefix}{connector}{icon}{child.name}")

        if child.is_dir:
            extension = "    " if is_last else "│   "
            lines.append(_generate_ascii_tree(child, prefix + extension))

    return "\n".join(filter(None, lines))

def export_markdown(node: DirectoryNode, profile: ProjectProfile, explanation: Dict[str, Any], output_path: str) -> None:
    """Generates a CODEMAPPR.md report."""
    project_name = os.path.basename(os.path.abspath(profile.root_path))
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        f"# CodeMappr Report — {project_name}",
        f"> Generated on {date_str} by CodeMappr v1.0.0",
        "",
        "## Project Profile",
        "| Field | Value |",
        "| :--- | :--- |",
        f"| Type | {profile.project_type} |",
        f"| Stack | {', '.join(profile.language_stack)} |",
        f"| Framework | {profile.framework or '—'} |",
        f"| Files | {profile.total_files} |",
        f"| Directories | {profile.total_dirs} |",
        f"| Size | {format_size(profile.total_size_bytes)} |",
        "",
        "## Architecture Summary",
        explanation["summary"],
        "",
        "## Folder Structure",
        "| Folder | Purpose |",
        "| :--- | :--- |"
    ]

    for folder, purpose in explanation["structure"].items():
        lines.append(f"| {folder} | {purpose} |")

    lines.extend([
        "",
        "## Entry Points",
    ])
    for ep in explanation["entry_points"]:
        lines.append(f"- {ep}")

    lines.extend([
        "",
        "## Notable Files",
    ])
    for nf in explanation["notable_files"]:
        lines.append(f"- {nf}")

    lines.extend([
        "",
        "## Directory Tree",
        "```text",
        f"📁 {node.name}",
        _generate_ascii_tree(node),
        "```"
    ])

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def _render_html_tree(node: DirectoryNode) -> str:
    """Recursively renders the directory tree as HTML."""
    if not node.is_dir:
        icon = "📄"
        if node.extension == ".py": icon = "🐍"
        elif node.extension in [".js", ".ts", ".jsx", ".tsx"]: icon = "⚡"
        elif node.extension in [".json", ".toml", ".yaml", ".yml"]: icon = "⚙️"
        return f'<div class="file">{icon} {node.name}</div>'

    html = f'<div class="folder">'
    html += f'<div class="folder-header" onclick="toggleFolder(this)">'
    html += f'<span class="toggle-icon">▼</span> 📁 {node.name}'
    html += f'</div>'
    html += f'<div class="folder-content">'
    for child in sorted(node.children, key=lambda x: (not x.is_dir, x.name)):
        html += _render_html_tree(child)
    html += f'</div>'
    html += f'</div>'
    return html

def export_html(node: DirectoryNode, profile: ProjectProfile, explanation: Dict[str, Any], output_path: str) -> None:
    """Generates a self-contained CODEMAPPR.html report."""
    project_name = os.path.basename(os.path.abspath(profile.root_path))
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CodeMappr Report — {project_name}</title>
    <style>
        :root {{
            --bg-color: #0d1117;
            --card-bg: #161b22;
            --border-color: #30363d;
            --text-main: #c9d1d9;
            --text-dim: #8b949e;
            --accent: #58a6ff;
            --success: #238636;
            --folder-color: #7d8590;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            line-height: 1.6;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
        }}
        header {{
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 30px;
            padding-bottom: 20px;
        }}
        h1 {{ color: var(--accent); margin-bottom: 5px; }}
        .meta {{ color: var(--text-dim); font-size: 0.9em; }}

        .grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }}
        @media (max-width: 768px) {{
            .grid {{ grid-template-columns: 1fr; }}
        }}

        .card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 20px;
        }}
        .card h2 {{
            margin-top: 0;
            font-size: 1.2em;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 10px;
            margin-bottom: 15px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        td {{
            padding: 8px 0;
            border-bottom: 1px solid var(--border-color);
        }}
        td:first-child {{ font-weight: bold; width: 40%; color: var(--text-dim); }}

        .summary-card {{ margin-bottom: 30px; }}

        .list-items {{
            list-style: none;
            padding: 0;
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .badge {{
            background: var(--border-color);
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 0.85em;
            font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace;
        }}

        .tree-container {{
            background: #010409;
            padding: 20px;
            border-radius: 6px;
            border: 1px solid var(--border-color);
            font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace;
            font-size: 14px;
            overflow-x: auto;
        }}

        .folder {{ margin-left: 15px; }}
        .folder-header {{
            cursor: pointer;
            user-select: none;
            padding: 2px 5px;
            border-radius: 3px;
        }}
        .folder-header:hover {{ background: #1f242c; }}
        .toggle-icon {{
            display: inline-block;
            width: 1em;
            transition: transform 0.2s;
            color: var(--text-dim);
        }}
        .folder.collapsed > .folder-header .toggle-icon {{
            transform: rotate(-90deg);
        }}
        .folder.collapsed > .folder-content {{
            display: none;
        }}
        .file {{
            margin-left: 20px;
            padding: 2px 5px;
            color: var(--text-main);
        }}

        footer {{
            margin-top: 50px;
            text-align: center;
            color: var(--text-dim);
            font-size: 0.8em;
            border-top: 1px solid var(--border-color);
            padding-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>CodeMappr Report — {project_name}</h1>
            <div class="meta">Generated on {date_str} by CodeMappr v1.0.0</div>
        </header>

        <div class="grid">
            <div class="card">
                <h2>Project Profile</h2>
                <table>
                    <tr><td>Type</td><td><span style="color: var(--success); font-weight: bold;">{profile.project_type}</span></td></tr>
                    <tr><td>Stack</td><td>{', '.join(profile.language_stack)}</td></tr>
                    <tr><td>Framework</td><td>{profile.framework or '—'}</td></tr>
                    <tr><td>Files</td><td>{profile.total_files}</td></tr>
                    <tr><td>Directories</td><td>{profile.total_dirs}</td></tr>
                    <tr><td>Size</td><td>{format_size(profile.total_size_bytes)}</td></tr>
                    <tr><td>Confidence</td><td>{profile.confidence}</td></tr>
                </table>
            </div>

            <div class="card">
                <h2>Key Structure</h2>
                <table>
                    {" ".join([f"<tr><td>{folder}</td><td>{purpose}</td></tr>" for folder, purpose in explanation["structure"].items()])}
                </table>
            </div>
        </div>

        <div class="card summary-card">
            <h2>Architecture Summary</h2>
            <p>{explanation["summary"]}</p>
        </div>

        <div class="grid">
            <div class="card">
                <h2>Entry Points</h2>
                <div class="list-items">
                    {" ".join([f'<span class="badge" style="color: #3fb950;">{ep}</span>' for ep in explanation["entry_points"]])}
                </div>
            </div>
            <div class="card">
                <h2>Notable Files</h2>
                <div class="list-items">
                    {" ".join([f'<span class="badge" style="color: #d29922;">{nf}</span>' for nf in explanation["notable_files"]])}
                </div>
            </div>
        </div>

        <div class="card">
            <h2>Directory Tree</h2>
            <div class="tree-container">
                {_render_html_tree(node)}
            </div>
        </div>

        <footer>
            Generated by CodeMappr v1.0.0 · github.com/yourusername/codemappr
        </footer>
    </div>

    <script>
        function toggleFolder(element) {{
            const folder = element.parentElement;
            folder.classList.toggle('collapsed');
        }}
    </script>
</body>
</html>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
