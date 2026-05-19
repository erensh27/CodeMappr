import os
from typing import List, Set, Optional
from .models import DirectoryNode, ProjectProfile

def _get_root_files(node: DirectoryNode) -> Set[str]:
    return {child.name for child in node.children if not child.is_dir}

def _get_root_dirs(node: DirectoryNode) -> Set[str]:
    return {child.name for child in node.children if child.is_dir}

def _has_file_anywhere(node: DirectoryNode, filename: str) -> bool:
    if not node.is_dir:
        return node.name == filename
    for child in node.children:
        if _has_file_anywhere(child, filename):
            return True
    return False

def _has_extension_anywhere(node: DirectoryNode, extension: str) -> bool:
    if not node.is_dir:
        return node.extension == extension
    for child in node.children:
        if _has_extension_anywhere(child, extension):
            return True
    return False

def _count_files_by_name(node: DirectoryNode, filename: str) -> int:
    count = 1 if not node.is_dir and node.name == filename else 0
    for child in node.children:
        count += _count_files_by_name(child, filename)
    return count

def _collect_extensions(node: DirectoryNode, extensions: Set[str]) -> None:
    if not node.is_dir and node.extension:
        extensions.add(node.extension)
    for child in node.children:
        _collect_extensions(child, extensions)

def _get_stats(node: DirectoryNode) -> tuple[int, int, int]:
    total_files = 0
    total_dirs = 0
    total_size = 0

    stack = [node]
    while stack:
        curr = stack.pop()
        if curr.is_dir:
            total_dirs += 1
        else:
            total_files += 1
        total_size += curr.size
        stack.extend(curr.children)

    return total_files, total_dirs, total_size

def detect_project(node: DirectoryNode, root_path: str) -> ProjectProfile:
    """
    Heuristics-based project type detector.

    Detection is purely based on presence of specific files, folders, and naming patterns.
    Zero external APIs.
    """
    total_files, total_dirs, total_size = _get_stats(node)

    root_files = _get_root_files(node)
    root_dirs = _get_root_dirs(node)

    all_extensions = set()
    _collect_extensions(node, all_extensions)

    ext_to_lang = {
        ".py": "Python",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".jsx": "JavaScript",
        ".tsx": "TypeScript",
        ".vue": "Vue",
        ".go": "Go",
        ".rs": "Rust",
        ".java": "Java",
        ".kt": "Kotlin",
        ".rb": "Ruby",
        ".php": "PHP",
        ".dart": "Dart",
        ".html": "HTML",
        ".css": "CSS",
        ".ipynb": "Jupyter Notebook",
        ".c": "C",
        ".cpp": "C++",
        ".cs": "C#",
        ".sh": "Shell",
        ".swift": "Swift",
        ".sql": "SQL",
    }

    language_stack = sorted(list({ext_to_lang[ext] for ext in all_extensions if ext in ext_to_lang}))

    project_type = "Unknown"
    framework = None
    confidence = "low"

    def read_root_file(filename: str) -> str:
        try:
            target = os.path.join(root_path, filename)
            if os.path.isfile(target):
                with open(target, "r", errors="ignore", encoding="utf-8") as f:
                    return f.read()
        except:
            pass
        return ""

    # 1. Monorepo
    monorepo_dirs = {"packages", "apps", "libs"}
    if (monorepo_dirs & root_dirs) and (_count_files_by_name(node, "package.json") > 1 or _count_files_by_name(node, "pyproject.toml") > 1):
        project_type = "Monorepo"
        confidence = "high"

    # 2. React/Next.js
    if project_type == "Unknown" and "package.json" in root_files and "src" in root_dirs:
        pkg_content = read_root_file("package.json")
        if "next" in pkg_content or "next.config.js" in root_files:
            project_type = "React/Next.js"
            framework = "Next.js"
            confidence = "high"
        elif "react" in pkg_content:
            project_type = "React/Next.js"
            framework = "React"
            confidence = "high"

    # 3. Vue.js
    if project_type == "Unknown" and "package.json" in root_files:
        if "vue.config.js" in root_files or _has_file_anywhere(node, "App.vue"):
            project_type = "Vue.js"
            framework = "Vue"
            confidence = "high"

    # 4. Angular
    if project_type == "Unknown" and "angular.json" in root_files:
        src_node = next((c for c in node.children if c.name == "src" and c.is_dir), None)
        if src_node and any(c.name == "app" and c.is_dir for c in src_node.children):
            project_type = "Angular"
            framework = "Angular"
            confidence = "high"

    # 5. Node.js API
    if project_type == "Unknown" and "package.json" in root_files:
        if any(f in root_files for f in ["index.js", "server.js", "app.js"]):
            project_type = "Node.js API"
            confidence = "medium"

    # 6. Python Django
    if project_type == "Unknown" and "manage.py" in root_files:
        if _has_file_anywhere(node, "settings.py") and _has_file_anywhere(node, "urls.py"):
            project_type = "Python Django"
            framework = "Django"
            confidence = "high"

    # 7. Python FastAPI/Flask
    if project_type == "Unknown" and ("main.py" in root_files or "app.py" in root_files):
        combined = read_root_file("requirements.txt") + read_root_file("pyproject.toml")
        if "fastapi" in combined.lower():
            project_type = "Python FastAPI/Flask"
            framework = "FastAPI"
            confidence = "high"
        elif "flask" in combined.lower():
            project_type = "Python FastAPI/Flask"
            framework = "Flask"
            confidence = "high"

    # 8. Python Package/Library
    if project_type == "Unknown" and ("pyproject.toml" in root_files or "setup.py" in root_files):
        project_type = "Python Package/Library"
        confidence = "medium"

    # 9. Rust
    if project_type == "Unknown" and "Cargo.toml" in root_files:
        project_type = "Rust"
        confidence = "high"

    # 10. Go
    if project_type == "Unknown" and "go.mod" in root_files:
        project_type = "Go"
        confidence = "high"

    # 11. Java/Spring
    if project_type == "Unknown" and ("pom.xml" in root_files or "build.gradle" in root_files):
        project_type = "Java/Spring"
        confidence = "high"

    # 12. Android
    if project_type == "Unknown" and _has_file_anywhere(node, "AndroidManifest.xml"):
        project_type = "Android"
        confidence = "high"

    # 13. Flutter/Dart
    if project_type == "Unknown" and "pubspec.yaml" in root_files:
        project_type = "Flutter/Dart"
        confidence = "high"

    # 14. Ruby on Rails
    if project_type == "Unknown" and "Gemfile" in root_files and "app" in root_dirs:
        config_node = next((c for c in node.children if c.name == "config" and c.is_dir), None)
        if config_node and any(c.name == "routes.rb" for c in config_node.children):
            project_type = "Ruby on Rails"
            framework = "Rails"
            confidence = "high"

    # 15. PHP/Laravel
    if project_type == "Unknown" and "composer.json" in root_files and "artisan" in root_files:
        project_type = "PHP/Laravel"
        framework = "Laravel"
        confidence = "high"

    # 16. Docker-based
    if project_type == "Unknown" and ("Dockerfile" in root_files or "docker-compose.yml" in root_files):
        project_type = "Docker-based"
        confidence = "medium"

    # 17. Data Science/ML
    if project_type == "Unknown" and (_has_extension_anywhere(node, ".ipynb") or "notebooks" in root_dirs):
        reqs = (read_root_file("requirements.txt") + read_root_file("pyproject.toml")).lower()
        if any(lib in reqs for lib in ["pandas", "numpy", "sklearn", "scikit-learn"]):
            project_type = "Data Science/ML"
            confidence = "high"
        else:
            project_type = "Data Science/ML"
            confidence = "medium"

    # 18. Static Site
    if project_type == "Unknown" and "index.html" in root_files:
        project_type = "Static Site"
        confidence = "medium"

    # Fallbacks
    if project_type == "Unknown":
        if "Python" in language_stack:
            project_type = "Generic Python"
            confidence = "low"
        elif "JavaScript" in language_stack or "TypeScript" in language_stack:
            project_type = "Generic JS/TS"
            confidence = "low"

    return ProjectProfile(
        project_type=project_type,
        language_stack=language_stack,
        description=f"A {project_type} project.",
        root_path=root_path,
        total_files=total_files,
        total_dirs=total_dirs,
        total_size_bytes=total_size,
        confidence=confidence,
        framework=framework
    )
