import os
from codemappr.walker import scan_directory
from codemappr.models import DirectoryNode

def test_basic_scan(mock_react_project):
    node = scan_directory(str(mock_react_project))

    assert isinstance(node, DirectoryNode)
    assert node.name == "mock_react_project"
    assert node.is_dir is True

    child_names = [child.name for child in node.children]
    assert "package.json" in child_names
    assert "src" in child_names
    assert "public" in child_names

    src_node = next(c for c in node.children if c.name == "src")
    assert any(c.name == "App.js" for c in src_node.children)

def test_gitignore_respected(tmp_path):
    project_dir = tmp_path / "test_gitignore"
    project_dir.mkdir()

    (project_dir / "node_modules").mkdir()
    (project_dir / "node_modules" / "some_lib").mkdir()
    (project_dir / "src").mkdir()
    (project_dir / "src" / "main.py").write_text("print(1)")

    # Create .gitignore
    (project_dir / ".gitignore").write_text("node_modules/\n")

    node = scan_directory(str(project_dir))
    child_names = [child.name for child in node.children]

    assert "src" in child_names
    assert "node_modules" not in child_names

def test_depth_limit(mock_deep_nested):
    # Depth 3 means: root (0), level1 (1), level2 (2), level3 (3)
    # The scan_directory implementation might interpret depth differently.
    # Looking at walker.py (from memory/previous knowledge), depth usually limits recursion.

    node = scan_directory(str(mock_deep_nested), depth=3)

    # Check level 3 exists
    level1 = next(c for c in node.children if c.name == "level1")
    level2 = next(c for c in level1.children if c.name == "level2")
    level3 = next(c for c in level2.children if c.name == "level3")

    # Level 3 should have no children if depth=3 is the limit of traversal
    assert len(level3.children) == 0

def test_empty_directory(mock_empty_dir):
    node = scan_directory(str(mock_empty_dir))
    assert node.name == "mock_empty_dir"
    assert len(node.children) == 0

def test_default_ignores(tmp_path):
    project_dir = tmp_path / "test_default_ignores"
    project_dir.mkdir()

    (project_dir / ".git").mkdir()
    (project_dir / "__pycache__").mkdir()
    (project_dir / "node_modules").mkdir()
    (project_dir / "src").mkdir()

    node = scan_directory(str(project_dir))
    child_names = [child.name for child in node.children]

    assert "src" in child_names
    assert ".git" not in child_names
    assert "__pycache__" not in child_names
    assert "node_modules" not in child_names
