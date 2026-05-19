import os
import shutil
import tempfile
import pytest
from codemappr.walker import scan_directory, parse_gitignore, should_ignore
from codemappr.models import DirectoryNode

@pytest.fixture
def temp_project():
    # Create a temporary directory structure
    temp_dir = tempfile.mkdtemp()

    # Create some files and directories
    os.makedirs(os.path.join(temp_dir, "src"))
    os.makedirs(os.path.join(temp_dir, "tests"))
    os.makedirs(os.path.join(temp_dir, ".git"))

    with open(os.path.join(temp_dir, "README.md"), "w") as f:
        f.write("# Test Project")

    with open(os.path.join(temp_dir, "src", "main.py"), "w") as f:
        f.write("print('hello')")

    with open(os.path.join(temp_dir, "src", "utils.py"), "w") as f:
        f.write("def add(a, b): return a + b")

    with open(os.path.join(temp_dir, ".gitignore"), "w") as f:
        f.write("*.log\n")
        f.write("ignored_dir/\n")

    os.makedirs(os.path.join(temp_dir, "ignored_dir"))
    with open(os.path.join(temp_dir, "ignored_dir", "secret.txt"), "w") as f:
        f.write("secret")

    with open(os.path.join(temp_dir, "test.log"), "w") as f:
        f.write("log data")

    yield temp_dir

    # Cleanup
    shutil.rmtree(temp_dir)

def test_parse_gitignore(temp_project):
    patterns = parse_gitignore(temp_project)
    assert "*.log" in patterns
    assert "ignored_dir/" in patterns

def test_should_ignore(temp_project):
    patterns = ["*.log", "ignored_dir/"]

    # Should ignore based on .gitignore patterns
    assert should_ignore(os.path.join(temp_project, "test.log"), patterns, temp_project) is True
    assert should_ignore(os.path.join(temp_project, "ignored_dir"), patterns, temp_project) is True
    assert should_ignore(os.path.join(temp_project, "ignored_dir", "secret.txt"), patterns, temp_project) is True

    # Should ignore based on ALWAYS_IGNORE
    assert should_ignore(os.path.join(temp_project, ".git"), patterns, temp_project) is True

    # Should NOT ignore valid files
    assert should_ignore(os.path.join(temp_project, "src", "main.py"), patterns, temp_project) is False
    assert should_ignore(os.path.join(temp_project, "README.md"), patterns, temp_project) is False

def test_scan_directory(temp_project):
    node = scan_directory(temp_project)

    assert isinstance(node, DirectoryNode)
    assert node.is_dir is True

    # Check children (src, tests, README.md, .gitignore)
    # .git, test.log, ignored_dir should be ignored
    child_names = [child.name for child in node.children]
    assert "src" in child_names
    assert "tests" in child_names
    assert "README.md" in child_names
    assert ".gitignore" in child_names

    assert ".git" not in child_names
    assert "test.log" not in child_names
    assert "ignored_dir" not in child_names

    # Check depth
    node_depth_1 = scan_directory(temp_project, depth=1)
    for child in node_depth_1.children:
        if child.is_dir:
            assert len(child.children) == 0

def test_nested_ignore(temp_project):
    # Create a nested directory that should be ignored
    os.makedirs(os.path.join(temp_project, "src", "ignored_dir"))
    with open(os.path.join(temp_project, "src", "ignored_dir", "nested.txt"), "w") as f:
        f.write("nested")

    patterns = ["ignored_dir/"]
    assert should_ignore(os.path.join(temp_project, "src", "ignored_dir"), patterns, temp_project) is True

def test_directory_node_size(temp_project):
    node = scan_directory(temp_project)

    # Total size should be sum of children
    total_size = sum(os.path.getsize(os.path.join(temp_project, f)) for f in ["README.md", ".gitignore"])
    total_size += os.path.getsize(os.path.join(temp_project, "src", "main.py"))
    total_size += os.path.getsize(os.path.join(temp_project, "src", "utils.py"))
    # tests/ is empty, so size 0 (or whatever os.listdir adds, but we sum file sizes)

    assert node.size == total_size
