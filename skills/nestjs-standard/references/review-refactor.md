# Review And Refactor

Use this reference for NestJS code reviews, bug hunts, and safe refactors.

## Review Checklist

Prioritize behavioral risks over style preferences.

Security and auth:

- Are routes protected with the right guards?
- Is object-level authorization enforced for user-owned resources?
- Are sensitive fields excluded from responses and logs?
- Are file uploads constrained by size and type?

Validation and contracts:

- Are body, query, and params validated before service use?
- Are numeric and boolean query params transformed intentionally?
- Does the response shape match existing API conventions?
- Are errors expressed with appropriate Nest exceptions?

DI and modules:

- Are providers declared in exactly one owning module?
- Are exported providers intentionally public to other modules?
- Are imports creating circular dependencies?
- Is request scope used only where necessary?

Data and consistency:

- Are multi-step writes wrapped in transactions?
- Are external side effects coordinated with database state?
- Are queries protected against N+1 behavior?
- Are migrations safe for existing data?

Tests:

- Is changed behavior covered at the right level?
- Are authorization, validation, and error paths covered when relevant?
- Do tests use realistic mocks for external boundaries?

## Safe Refactor Workflow

1. Characterize the current behavior with existing tests, a focused new test, or a small manual reproduction.
2. Move code without changing behavior first when possible.
3. Keep public route contracts stable unless the request says to change them.
4. Preserve module exports/imports until consumers are updated.
5. Run tests/typecheck/build after each meaningful step when the refactor is broad.

## Adding Abstractions

Add an abstraction only when it has a clear job:

- It removes meaningful duplication.
- It isolates an external dependency.
- It centralizes a policy used in several places.
- It matches an established local pattern.
- It improves testability for complex behavior.

Avoid abstractions that only rename a framework primitive. For example, a repository wrapping every one-line Prisma call usually adds noise unless the project already uses repositories.

## Migration Review

For schema changes, check:

- Required columns on non-empty tables need defaults, backfills, or staged migrations.
- Renames may be generated as drop/add and can lose data.
- Unique indexes can fail on existing duplicate data.
- Relation changes can affect cascade behavior.
- Generated ORM client/types must be refreshed.

Mention migration risks clearly in the final response if they require operator action.

## Performance Review

Look for:

- Query per item loops.
- Unbounded list endpoints.
- Missing pagination on mobile/admin list screens.
- Large `include`/relation graphs returned directly to clients.
- Heavy startup work in lifecycle hooks.
- Synchronous CPU-heavy work in request handlers.

Prefer simple fixes first: pagination, `select`, batching, indexes, queueing slow jobs.
