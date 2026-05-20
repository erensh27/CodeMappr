from codemappr.walker import scan_directory
from codemappr.detector import detect_project
from codemappr.explainer import explain_project

def test_summary_not_empty(mock_react_project):
    node = scan_directory(str(mock_react_project))
    profile = detect_project(node, str(mock_react_project))
    explanation = explain_project(profile, node)

    assert explanation["summary"]
    assert isinstance(explanation["summary"], str)

def test_folder_purposes(mock_python_package):
    node = scan_directory(str(mock_python_package))
    profile = detect_project(node, str(mock_python_package))
    explanation = explain_project(profile, node)

    # Check if 'src' and 'tests' are recognized
    assert explanation["structure"]["src"] == "Main source code"
    assert explanation["structure"]["tests"] == "Test suite"

def test_entry_points_detected(mock_django_project):
    node = scan_directory(str(mock_django_project))
    profile = detect_project(node, str(mock_django_project))
    explanation = explain_project(profile, node)

    assert "manage.py" in explanation["entry_points"]

def test_notable_files_detected(mock_react_project):
    node = scan_directory(str(mock_react_project))
    profile = detect_project(node, str(mock_react_project))
    explanation = explain_project(profile, node)

    assert "package.json" in explanation["notable_files"]
