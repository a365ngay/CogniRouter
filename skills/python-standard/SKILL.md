---
name: python-standard
description: Standards and workflows for implementing, reviewing, debugging, packaging, testing, and refactoring Python code. Use when working on Python applications, scripts, libraries, APIs, CLIs, data processing jobs, async code, dependency management, pyproject/setup files, pytest tests, type checking, linting, or production hardening. Prefer this skill for existing Python repositories where the agent must detect the runtime, package manager, framework, and local conventions before changing code.
---

# Python Standard

Use this skill to make Python changes that fit the repository's runtime, packaging, typing, and test conventions. Do not impose a framework or toolchain before discovering what the project already uses.

## Operating Rules

1. Inspect the project before editing: Python version, package manager, framework, test runner, type checker, linter/formatter, and entry points.
2. Prefer existing patterns over new abstractions. Add dataclasses, Pydantic models, async APIs, dependency injection, or package restructuring only when the task benefits from them.
3. Keep public APIs, CLI flags, serialized schemas, database migrations, and file formats backward-compatible unless the request says otherwise.
4. Use type hints for new or changed code when the project is typed. Do not perform noisy whole-repo typing conversions during small fixes.
5. Separate pure logic from I/O where it improves testability. Keep scripts executable and libraries importable.
6. Verify with the narrowest useful command: targeted pytest, typecheck, lint/format check, package build, or the repo's own scripts.

## Discovery Checklist

Before changing Python code, identify:

- Python version from `.python-version`, `pyproject.toml`, `runtime.txt`, Dockerfile, CI, or README.
- Package manager: `uv`, Poetry, PDM, Hatch, pip-tools, pip/venv, Conda.
- Framework: FastAPI, Django, Flask, Typer/Click, Celery/RQ, pandas, notebooks, plain scripts.
- Test stack: pytest, unittest, tox, nox, coverage, hypothesis.
- Quality tools: ruff, black, isort, mypy, pyright, pylint, pre-commit.
- Config files: `pyproject.toml`, `setup.cfg`, `tox.ini`, `.pre-commit-config.yaml`, CI workflows.

## Reference Routing

Read only what the task needs:

- `references/project-environment.md`: packaging, dependencies, environments, entry points, config.
- `references/code-design.md`: Python design, typing, dataclasses/Pydantic, errors, async, I/O boundaries.
- `references/testing-quality.md`: pytest, mocks, fixtures, coverage, type/lint/format verification.

## Implementation Workflow

1. Find the closest existing module/test and mirror its style.
2. Make the smallest behavioral change first.
3. Add or update tests around changed behavior, especially edge cases and error paths.
4. Update dependency/config files only when required, using the repo's package manager.
5. Run focused verification and report any command that cannot run.

## Review Workflow

Prioritize findings in this order:

1. Incorrect behavior, data loss, security issues, unsafe deserialization, path traversal, command injection, or secret leaks.
2. Broken async/concurrency behavior, resource leaks, file/socket/session cleanup gaps.
3. Public API, CLI, schema, or migration regressions.
4. Missing tests for changed behavior and brittle tests that mock the wrong boundary.
5. Typing, lint, and maintainability issues that hide real defects.
