# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-05-20
### Added
- Core scanning engine with `.gitignore` support and manual path traversal.
- Heuristic-based project type and language stack detection for 20+ project types.
- Architectural explainer mapping directory structures to their purpose.
- Rich terminal dashboard featuring project profile, architecture summary, and directory tree.
- Markdown export (`CODEMAPPR.md`) with ASCII directory trees.
- Interactive HTML export (`CODEMAPPR.html`) with dark theme and collapsible trees.
- CLI flags for recursion depth (`--depth`), custom ignore patterns (`--ignore`), and multiple output formats (`--format`).
- Comprehensive test suite and GitHub Actions CI workflow.
- Standardized documentation and PyPI-ready metadata.
