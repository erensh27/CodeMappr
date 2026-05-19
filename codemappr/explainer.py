from typing import List, Dict
from .models import DirectoryNode, ProjectProfile

FOLDER_PURPOSE_MAP = {
    "src": "Main source code",
    "app": "Application core logic",
    "lib": "Library files or external dependencies",
    "core": "Core system components",
    "utils": "Utility functions and helpers",
    "helpers": "Helper functions",
    "tests": "Test suite",
    "test": "Test suite",
    "spec": "Specification or test files",
    "docs": "Project documentation",
    "public": "Publicly accessible assets",
    "static": "Static assets (CSS, JS, images)",
    "assets": "Media and static assets",
    "config": "Configuration files",
    "scripts": "Automation and maintenance scripts",
    "migrations": "Database migration files",
    "components": "Reusable UI components",
    "pages": "Application pages or routes",
    "api": "API endpoints and logic",
    "routes": "URL routing definitions",
    "models": "Data models or database schema",
    "views": "Presentation logic or templates",
    "controllers": "Business logic and request handling",
    "services": "External service integrations",
    "middleware": "Request/response middleware",
    "hooks": "Lifecycle hooks or custom React hooks",
}

ENTRY_POINTS = [
    "main.py", "app.py", "manage.py", "index.js", "server.js",
    "index.ts", "main.ts", "app.js", "main.go", "Cargo.toml"
]

NOTABLE_FILES = [
    "package.json", "pyproject.toml", "requirements.txt", "Dockerfile",
    "docker-compose.yml", ".env.example", ".gitignore", "README.md",
    "LICENSE", "Makefile", "setup.py", "pom.xml", "go.mod"
]

def explain_project(profile: ProjectProfile, node: DirectoryNode) -> dict:
    """
    Architecture explainer that provides a summary and structural overview.
    """
    # 1. Summary
    stack_str = ", ".join(profile.language_stack) if profile.language_stack else "various languages"
    framework_str = f" using the {profile.framework} framework" if profile.framework else ""
    summary = (
        f"This project is a {profile.project_type} application developed in {stack_str}{framework_str}. "
        f"It consists of {profile.total_files} files across {profile.total_dirs} directories. "
        f"The codebase structure suggests it follows standard conventions for {profile.project_type} development."
    )

    # 2. Structure
    structure = {}
    for child in node.children:
        if child.is_dir and child.name in FOLDER_PURPOSE_MAP:
            structure[child.name] = FOLDER_PURPOSE_MAP[child.name]

    # 3. Entry Points & Notable Files
    detected_entry_points = []
    detected_notable_files = []

    # Check only root for entry points and notable files for simplicity and accuracy
    root_file_names = {child.name for child in node.children if not child.is_dir}

    for ep in ENTRY_POINTS:
        if ep in root_file_names:
            detected_entry_points.append(ep)

    for nf in NOTABLE_FILES:
        if nf in root_file_names:
            detected_notable_files.append(nf)

    return {
        "summary": summary,
        "structure": structure,
        "entry_points": detected_entry_points,
        "notable_files": detected_notable_files
    }
