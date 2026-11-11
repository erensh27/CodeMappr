import codemappr
from codemappr import display
from codemappr.walker import scan_directory
from codemappr.detector import detect_project
from codemappr.explainer import explain_project
from codemappr.exporter import export_markdown, export_html
from codemappr.cli import VERSION


def _build(project):
    node = scan_directory(str(project))
    profile = detect_project(node, str(project))
    return node, profile, explain_project(profile, node)


def test_version_single_source():
    assert VERSION == codemappr.__version__


def test_terminal_footer_has_real_repo_and_version(mock_react_project, capsys):
    from rich.console import Console
    display.console = Console(width=120)
    node, profile, explanation = _build(mock_react_project)
    display.render_terminal(node, profile, explanation)
    out = capsys.readouterr().out
    assert "yourusername" not in out
    assert codemappr.REPO_URL in out
    assert f"v{codemappr.__version__}" in out


def test_exports_have_real_repo_and_version(mock_react_project, tmp_path):
    node, profile, explanation = _build(mock_react_project)
    md, html = tmp_path / "r.md", tmp_path / "r.html"
    export_markdown(node, profile, explanation, str(md))
    export_html(node, profile, explanation, str(html))
    assert f"v{codemappr.__version__}" in md.read_text()
    content = html.read_text()
    assert "yourusername" not in content
    assert codemappr.REPO_URL in content
    assert f"v{codemappr.__version__}" in content
