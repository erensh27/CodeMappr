from codemappr.walker import scan_directory
from codemappr.detector import detect_project

def test_detect_react(mock_react_project):
    node = scan_directory(str(mock_react_project))
    profile = detect_project(node, str(mock_react_project))

    assert profile.project_type == "React/Next.js"
    assert profile.framework == "React"
    assert "JavaScript" in profile.language_stack

def test_detect_django(mock_django_project):
    node = scan_directory(str(mock_django_project))
    profile = detect_project(node, str(mock_django_project))

    assert profile.project_type == "Python Django"
    assert profile.framework == "Django"
    assert "Python" in profile.language_stack

def test_detect_rust(mock_rust_project):
    node = scan_directory(str(mock_rust_project))
    profile = detect_project(node, str(mock_rust_project))

    assert profile.project_type == "Rust"
    assert "Rust" in profile.language_stack

def test_detect_monorepo(mock_monorepo):
    node = scan_directory(str(mock_monorepo))
    profile = detect_project(node, str(mock_monorepo))

    assert profile.project_type == "Monorepo"

def test_detect_unknown(mock_empty_dir):
    node = scan_directory(str(mock_empty_dir))
    profile = detect_project(node, str(mock_empty_dir))

    assert profile.project_type == "Unknown"

def test_language_stack(mock_react_project):
    # Add a python file to check multi-language
    (mock_react_project / "script.py").write_text("print(1)")

    node = scan_directory(str(mock_react_project))
    profile = detect_project(node, str(mock_react_project))

    assert "JavaScript" in profile.language_stack
    assert "Python" in profile.language_stack
