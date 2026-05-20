import pytest
import os

@pytest.fixture
def mock_react_project(tmp_path):
    project_dir = tmp_path / "mock_react_project"
    project_dir.mkdir()

    package_json = project_dir / "package.json"
    package_json.write_text('{"dependencies": {"react": "^18.2.0"}}')

    src_dir = project_dir / "src"
    src_dir.mkdir()
    (src_dir / "App.js").write_text("function App() { return <div>Hello</div>; }")

    public_dir = project_dir / "public"
    public_dir.mkdir()
    (public_dir / "index.html").write_text("<!DOCTYPE html><html></html>")

    return project_dir

@pytest.fixture
def mock_django_project(tmp_path):
    project_dir = tmp_path / "mock_django_project"
    project_dir.mkdir()

    (project_dir / "manage.py").write_text("# Django manage.py")

    app_dir = project_dir / "myproject"
    app_dir.mkdir()
    (app_dir / "settings.py").write_text("DEBUG = True")
    (app_dir / "urls.py").write_text("urlpatterns = []")

    (project_dir / "requirements.txt").write_text("django==4.2")

    return project_dir

@pytest.fixture
def mock_rust_project(tmp_path):
    project_dir = tmp_path / "mock_rust_project"
    project_dir.mkdir()

    (project_dir / "Cargo.toml").write_text('[package]\nname = "mock_rust"')

    src_dir = project_dir / "src"
    src_dir.mkdir()
    (src_dir / "main.rs").write_text("fn main() {}")

    return project_dir

@pytest.fixture
def mock_python_package(tmp_path):
    project_dir = tmp_path / "mock_python_package"
    project_dir.mkdir()

    (project_dir / "pyproject.toml").write_text("[project]\nname = 'mock_python'")

    src_dir = project_dir / "src"
    src_dir.mkdir()
    (src_dir / "__init__.py").write_text("")

    tests_dir = project_dir / "tests"
    tests_dir.mkdir()
    (tests_dir / "__init__.py").write_text("")

    return project_dir

@pytest.fixture
def mock_monorepo(tmp_path):
    project_dir = tmp_path / "mock_monorepo"
    project_dir.mkdir()

    (project_dir / "package.json").write_text('{"workspaces": ["packages/*"]}')

    packages_dir = project_dir / "packages"
    packages_dir.mkdir()

    app1_dir = packages_dir / "app1"
    app1_dir.mkdir()
    (app1_dir / "package.json").write_text('{"name": "app1"}')

    app2_dir = packages_dir / "app2"
    app2_dir.mkdir()
    (app2_dir / "package.json").write_text('{"name": "app2"}')

    return project_dir

@pytest.fixture
def mock_empty_dir(tmp_path):
    project_dir = tmp_path / "mock_empty_dir"
    project_dir.mkdir()
    return project_dir

@pytest.fixture
def mock_deep_nested(tmp_path):
    project_dir = tmp_path / "mock_deep_nested"
    project_dir.mkdir()

    current = project_dir
    for i in range(1, 11):
        current = current / f"level{i}"
        current.mkdir()
        (current / f"file{i}.txt").write_text(f"content{i}")

    return project_dir
