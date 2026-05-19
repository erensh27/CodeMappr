from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class DirectoryNode:
    """
    Represents a node in the directory tree.
    """
    name: str
    path: str
    is_dir: bool
    size: int
    extension: str
    depth: int
    children: List["DirectoryNode"] = field(default_factory=list)

@dataclass
class ProjectProfile:
    """
    Represents high-level information about the project.
    """
    project_type: str
    language_stack: List[str]
    description: str
    root_path: str
    total_files: int
    total_dirs: int
    total_size_bytes: int
    framework: Optional[str] = None
