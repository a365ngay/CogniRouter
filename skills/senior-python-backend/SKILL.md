---
name: senior-python-backend
description: Use when designing, implementing, debugging, reviewing, or refactoring Python web backends with FastAPI, Django, Django REST Framework, or Flask, including routing, Pydantic or serializer validation, ORM queries (SQLAlchemy, Django ORM), migrations, auth, async I/O, background tasks (Celery, RQ), and API tests. For general Python code standards also see python-standard.
---

# Senior Python Backend

## Role

Build Python web services with validated contracts, efficient ORM access, correct async boundaries, safe migrations, and enforced authorization.

## Before Editing

1. Inspect framework and version, project layout, settings and environment handling, ORM and migration tool (Alembic, Django migrations), validation layer (Pydantic, DRF serializers, marshmallow), auth mechanism, task queue, dependency manager, and test setup (pytest, pytest-django, httpx/TestClient).
2. Trace the endpoint from router/view through dependencies or middleware, validation, permissions, service logic, ORM queries, external calls, and response schema.
3. Reuse existing patterns; do not add a new framework layer, repository abstraction, or library for one endpoint.

## Implementation Rules

- Validate all input with the project's schema layer and declare response models so internal fields never leak.
- Enforce authentication and object-level permissions in dependencies, permission classes, or decorators before side effects.
- Avoid N+1 queries (`select_related`/`prefetch_related`, SQLAlchemy `selectinload`/`joinedload`), paginate lists, and keep transactions short and explicit (`transaction.atomic`, session scope).
- In async frameworks, never call blocking I/O (sync DB drivers, `requests`, heavy CPU) inside `async def` handlers; use async clients, a threadpool, or a sync route.
- Write migrations that are safe for existing data and deployments: add nullable columns or defaults first, backfill separately, avoid long table locks.
- Keep secrets in environment or a secret store; set timeouts and retries on outbound HTTP; make background tasks idempotent with retry limits.
- Map errors to the project's error contract; never return raw tracebacks or ORM errors to clients.

## Testing and Verification

Run the project's formatter/linter (ruff, black, flake8), type checker (mypy/pyright) if configured, and pytest including API tests for changed endpoints. Run migrations against a disposable database and check generated SQL for changed queries.

## Review Checklist

- Are input and output schemas explicit, and is authorization object-level?
- Are queries bounded and free of N+1 behavior?
- Is async code free of blocking calls?
- Are migrations reversible or safe to roll forward under load?
