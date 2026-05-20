import os
from codemappr.walker import scan_directory
from codemappr.detector import detect_project
from codemappr.explainer import explain_project
from codemappr.exporter import export_markdown, export_html

def test_markdown_export(mock_react_project, tmp_path):
    node = scan_directory(str(mock_react_project))
    profile = detect_project(node, str(mock_react_project))
    explanation = explain_project(profile, node)

    output_path = tmp_path / "REPORT.md"
    export_markdown(node, profile, explanation, str(output_path))

    assert output_path.exists()
    content = output_path.read_text()
    assert "# CodeMappr Report" in content
    assert "## Project Profile" in content
    assert "## Directory Tree" in content
    assert "## Architecture Summary" in content

def test_html_export(mock_react_project, tmp_path):
    node = scan_directory(str(mock_react_project))
    profile = detect_project(node, str(mock_react_project))
    explanation = explain_project(profile, node)

    output_path = tmp_path / "REPORT.html"
    export_html(node, profile, explanation, str(output_path))

    assert output_path.exists()
    content = output_path.read_text()
    assert "<html" in content
    assert "CodeMappr Report" in content
    # Verify no external CDN links (basic check)
    assert "https://cdn" not in content
    assert "http://cdn" not in content

def test_output_path_respected(mock_python_package, tmp_path):
    node = scan_directory(str(mock_python_package))
    profile = detect_project(node, str(mock_python_package))
    explanation = explain_project(profile, node)

    custom_dir = tmp_path / "custom_reports"
    custom_dir.mkdir()
    output_path = custom_dir / "my_report.md"

    export_markdown(node, profile, explanation, str(output_path))

    assert output_path.exists()
