# Python Project And Environment

Use this reference for package managers, dependencies, virtual environments, entry points, and config files.

## Package Manager Detection

Follow the lockfile and config already present:

- `uv.lock` / `pyproject.toml`: use `uv` commands.
- `poetry.lock`: use Poetry.
- `pdm.lock`: use PDM.
- `requirements*.txt`: use pip or pip-tools based on nearby scripts.
- `environment.yml`: use Conda/Mamba.

Do not rewrite package management during feature work.

## Dependency Changes

Add dependencies only when the task clearly needs them and the standard library/local code is not enough.

Use the repo's workflow:

```bash
uv add <package>
poetry add <package>
pip install -r requirements.txt
pip-compile
```

Pin or constrain versions according to local style. Update lockfiles when the manager expects it.

## Entry Points

Find real entry points before changing behavior:

- CLI scripts in `pyproject.toml` `[project.scripts]` or Click/Typer modules.
- Web app factories such as `create_app()`, FastAPI `app`, Django `manage.py`.
- Worker entry points, scheduled jobs, notebooks, or Docker commands.

Keep modules import-safe. Avoid running application work at import time unless it is the established script pattern.

## Configuration

Prefer explicit config models and environment variables over hardcoded paths/secrets.

Do not log secrets. Treat tokens, passwords, private keys, database URLs, and signed URLs as sensitive.

For path handling, use `pathlib.Path` and resolve untrusted paths carefully before file operations.
