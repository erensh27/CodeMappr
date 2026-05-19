import os
import shutil
import tempfile
import pytest
from codemappr.walker import scan_directory
from codemappr.detector import detect_project

@pytest.fixture
def temp_dir():
    d = tempfile.mkdtemp()
    yield d
    shutil.rmtree(d)

def test_detect_python_package(temp_dir):
    # Create a dummy Python package structure
    with open(os.path.join(temp_dir, "pyproject.toml"), "w") as f:
        f.write("[project]\nname='test'")
    os.makedirs(os.path.join(temp_dir, "src"))
    with open(os.path.join(temp_dir, "src", "main.py"), "w") as f:
        f.write("print('hello')")

    node = scan_directory(temp_dir)
    profile = detect_project(node, temp_dir)

    assert profile.project_type == "Python Package/Library"
    assert "Python" in profile.language_stack
    assert profile.confidence in ["medium", "high"]

def test_detect_react_project(temp_dir):
    # Create a dummy React structure
    with open(os.path.join(temp_dir, "package.json"), "w") as f:
        f.write('{"dependencies": {"react": "18.0.0"}}')
    os.makedirs(os.path.join(temp_dir, "src"))
    with open(os.path.join(temp_dir, "src", "App.js"), "w") as f:
        f.write("function App() {}")

    node = scan_directory(temp_dir)
    profile = detect_project(node, temp_dir)

    assert profile.project_type == "React/Next.js"
    assert profile.framework == "React"
    assert "JavaScript" in profile.language_stack
    assert profile.confidence == "high"

def test_detect_django_project(temp_dir):
    # Create dummy Django structure
    with open(os.path.join(temp_dir, "manage.py"), "w") as f:
        f.write("# django manage.py")
    os.makedirs(os.path.join(temp_dir, "myproject"))
    with open(os.path.join(temp_dir, "myproject", "settings.py"), "w") as f:
        f.write("DEBUG=True")
    with open(os.path.join(temp_dir, "myproject", "urls.py"), "w") as f:
        f.write("urlpatterns=[]")

    node = scan_directory(temp_dir)
    profile = detect_project(node, temp_dir)

    assert profile.project_type == "Python Django"
    assert profile.framework == "Django"
    assert "Python" in profile.language_stack
    assert profile.confidence == "high"
