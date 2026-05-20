import os
import fnmatch
from typing import List, Optional
from .models import DirectoryNode

# Always ignored patterns as per requirements
ALWAYS_IGNORE = {
    ".git/", "__pycache__/", "node_modules/", ".venv/",
    "dist/", "build/", "*.pyc", ".DS_Store"
}

def parse_gitignore(root_path: str) -> List[str]:
    """
    Manually parses the .gitignore file in the root directory.
    Returns a list of patterns to ignore.
    """
    gitignore_path = os.path.join(root_path, ".gitignore")
    patterns = []
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    patterns.append(line)
    return patterns

def should_ignore(path: str, patterns: List[str], root_path: str) -> bool:
    """
    Determines if a path should be ignored based on patterns.
    """
    rel_path = os.path.relpath(path, root_path)
    # Convert to forward slashes for consistency if on Windows
    rel_path = rel_path.replace(os.sep, "/")

    # Always check ALWAYS_IGNORE
    for pattern in ALWAYS_IGNORE:
        if pattern.endswith("/"):
            # It's a directory pattern
            dir_pattern = pattern.rstrip("/")
            if rel_path == dir_pattern or rel_path.startswith(f"{dir_pattern}/") or \
               f"/{dir_pattern}/" in f"/{rel_path}/":
                return True
        else:
            if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(os.path.basename(rel_path), pattern):
                return True

    # Check .gitignore patterns
    for pattern in patterns:
        if not pattern:
            continue

        # Simple fnmatch for basic support.
        # Note: .gitignore parsing can be very complex, this is a basic implementation.

        # Handle directory-only patterns (ending in /)
        if pattern.endswith("/"):
            dir_pattern = pattern.rstrip("/")
            # Standard Git: if it doesn't have a leading slash, it matches at any depth
            if pattern.startswith("/"):
                # Matches only from root
                root_dir_pattern = dir_pattern.lstrip("/")
                if rel_path == root_dir_pattern or rel_path.startswith(f"{root_dir_pattern}/"):
                    return True
            else:
                # Matches anywhere in the tree
                if rel_path == dir_pattern or rel_path.startswith(f"{dir_pattern}/") or \
                   f"/{dir_pattern}/" in f"/{rel_path}/":
                    return True
        else:
            # File or directory pattern (not ending in /)
            if pattern.startswith("/"):
                root_pattern = pattern.lstrip("/")
                if fnmatch.fnmatch(rel_path, root_pattern):
                    return True
            else:
                if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(os.path.basename(rel_path), pattern):
                    return True

    return False

def scan_directory(path: str, depth: Optional[int] = None, ignore_patterns: Optional[List[str]] = None, root_path: Optional[str] = None, current_depth: int = 0) -> DirectoryNode:
    """
    Recursively scans a directory and returns a DirectoryNode tree.

    Args:
        path: Path to scan.
        depth: Maximum depth to scan (None for unlimited).
        ignore_patterns: Additional patterns to ignore.
        root_path: Root path of the scan (used for relative path calculation).
        current_depth: Current recursion depth.
    """
    if root_path is None:
        root_path = os.path.abspath(path)

    actual_path = os.path.abspath(path)
    name = os.path.basename(actual_path)
    if not name and actual_path == root_path:
        # For root path like "." or "/", basename might be empty
        name = os.path.basename(os.getcwd()) if actual_path == os.getcwd() else actual_path

    rel_path = os.path.relpath(actual_path, root_path)
    is_dir = os.path.isdir(actual_path)

    # Get extension
    if is_dir:
        extension = ""
    else:
        _, extension = os.path.splitext(name)

    # Get gitignore patterns if at root
    if ignore_patterns is None and current_depth == 0:
        ignore_patterns = parse_gitignore(root_path)
    elif ignore_patterns is None:
        ignore_patterns = []

    node = DirectoryNode(
        name=name,
        path=rel_path,
        is_dir=is_dir,
        size=0,
        extension=extension,
        depth=current_depth,
        children=[]
    )

    if not is_dir:
        node.size = os.path.getsize(actual_path)
        return node

    # If it's a directory, and we haven't reached max depth
    if depth is None or current_depth < depth:
        try:
            items = os.listdir(actual_path)
            for item in sorted(items):
                item_path = os.path.join(actual_path, item)

                # Check if it should be ignored
                if should_ignore(item_path, ignore_patterns, root_path):
                    continue

                try:
                    child_node = scan_directory(
                        item_path,
                        depth=depth,
                        ignore_patterns=ignore_patterns,
                        root_path=root_path,
                        current_depth=current_depth + 1
                    )
                    node.children.append(child_node)
                    node.size += child_node.size
                except PermissionError:
                    # Warn and skip that subtree
                    print(f"Warning: Permission denied for {item_path}. Skipping.")
        except PermissionError:
            # Skip directories we can't access
            print(f"Warning: Permission denied for {actual_path}. Skipping.")

    return node
