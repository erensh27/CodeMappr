from codemappr.models import DirectoryNode, ProjectProfile

def test_directory_node_init():
    node = DirectoryNode(
        name="test",
        path="test",
        is_dir=True,
        size=100,
        extension="",
        depth=0
    )
    assert node.name == "test"
    assert node.children == []

def test_project_profile_init():
    profile = ProjectProfile(
        project_type="python",
        language_stack=["python", "typer"],
        description="A test project",
        root_path="/tmp/test",
        total_files=10,
        total_dirs=2,
        total_size_bytes=1024
    )
    assert profile.project_type == "python"
    assert profile.framework is None
