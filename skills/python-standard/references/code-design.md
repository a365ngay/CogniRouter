# Python Code Design

Use this reference for module design, typing, error handling, async, data models, and I/O boundaries.

## Module Boundaries

Keep pure logic separate from I/O when practical:

- Pure functions/classes: business rules, parsing, transformation, validation.
- Adapters: HTTP clients, databases, files, subprocesses, queues.
- Entry points: CLI, web routes, workers.

Avoid importing web framework objects deep into domain logic unless the project already does.

## Typing

Use type hints in changed code when the project is typed. Prefer precise types for public functions and boundaries.

Use `Protocol` for structural interfaces only when there are multiple implementations or tests benefit from the boundary.

Avoid broad `Any` unless integrating with untyped libraries and the value is narrowed quickly.

## Data Models

Choose the local model style:

- `dataclasses` for lightweight internal records.
- Pydantic for validation/serialization boundaries, especially FastAPI or config.
- Django ORM/SQLAlchemy models for persisted entities.
- Plain dicts only when the existing API/data layer expects them.

Do not introduce Pydantic or dataclasses into a codebase that already has a clear model layer unless it solves the task.

## Errors

Raise specific exceptions with actionable messages. Preserve exception types that callers already catch.

Do not swallow exceptions silently. If retrying or falling back, log enough context without leaking secrets.

## Async And Concurrency

Do not block the event loop in async code. Use async clients or move blocking work to a thread/process when necessary.

Always close clients, files, sessions, and subprocesses. Prefer context managers.

Be careful with shared mutable state in concurrent code. Use locks/queues or avoid shared state.

## Security Basics

Avoid:

- `eval`/`exec` on untrusted input.
- `pickle` for untrusted data.
- `shell=True` with user-controlled strings.
- Path joins that allow traversal outside intended directories.
- Logging secrets or full auth headers.

Validate external input at boundaries and encode/escape output in the layer that renders it.
