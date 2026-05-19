from codemappr.models import DirectoryNode, ProjectProfile
from codemappr.explainer import explain_project

def test_explain_project_basic():
    profile = ProjectProfile(
        project_type="Python Django",
        language_stack=["Python"],
        description="A Python Django project.",
        root_path="/tmp/test",
        total_files=10,
        total_dirs=2,
        total_size_bytes=1024,
        confidence="high",
        framework="Django"
    )

    node = DirectoryNode(
        name="test",
        path=".",
        is_dir=True,
        size=1024,
        extension="",
        depth=0,
        children=[
            DirectoryNode("manage.py", "./manage.py", False, 100, ".py", 1),
            DirectoryNode("src", "./src", True, 924, "", 1),
            DirectoryNode("README.md", "./README.md", False, 50, ".md", 1)
        ]
    )

    explanation = explain_project(profile, node)

    assert "Python Django" in explanation["summary"]
    assert "Django" in explanation["summary"]
    assert explanation["structure"]["src"] == "Main source code"
    assert "manage.py" in explanation["entry_points"]
    assert "README.md" in explanation["notable_files"]

def test_explain_project_empty():
    profile = ProjectProfile(
        project_type="Unknown",
        language_stack=[],
        description="A Unknown project.",
        root_path="/tmp/test",
        total_files=0,
        total_dirs=1,
        total_size_bytes=0,
        confidence="low"
    )

    node = DirectoryNode("test", ".", True, 0, "", 0)

    explanation = explain_project(profile, node)

    assert "Unknown" in explanation["summary"]
    assert explanation["structure"] == {}
    assert explanation["entry_points"] == []
    assert explanation["notable_files"] == []
