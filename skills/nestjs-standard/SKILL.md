---
name: nestjs-standard
description: Standards and workflows for implementing, reviewing, debugging, and refactoring NestJS applications. Use when working on NestJS modules, controllers, services, DTOs, guards, interceptors, pipes, Prisma or TypeORM data access, REST APIs, authentication, validation, tests, migrations, or production hardening. Prefer this skill for NestJS code changes in existing repositories where the agent must follow local architecture and avoid framework-pattern overreach.
---

# NestJS Standard

Use this skill to make practical, codebase-aware NestJS changes. The goal is not to impose a generic architecture; it is to read the current project, preserve its conventions, and apply NestJS patterns only where they solve the task.

## Operating Rules

1. Inspect the existing app before editing: package manager, NestJS version, module layout, ORM, validation setup, auth setup, test runner, and local naming conventions.
2. Prefer existing project patterns over new abstractions. Add repositories, injection tokens, interceptors, event buses, or lazy modules only when the local codebase already uses them or the task clearly needs them.
3. Keep changes scoped to the requested feature or defect. Avoid broad module reshuffles unless the request is explicitly architectural.
4. Validate inputs at DTO or pipe boundaries, enforce authorization in guards/policies, and keep business rules in services or domain helpers.
5. Match the detected ORM. Do not introduce TypeORM into Prisma projects, Prisma into TypeORM projects, or a repository layer into simple CRUD code without a concrete benefit.
6. Run the narrowest useful verification available: unit tests for service logic, e2e/request tests for API behavior, lint/typecheck/build for shared contracts, and migration generation checks for schema work.

## Discovery Checklist

Before changing NestJS code, quickly discover:

- `package.json`: NestJS version, scripts, ORM, test tools, validation/security packages.
- Entry points: `src/main.ts`, root module, global pipes, filters, interceptors, guards, prefix/versioning.
- Feature shape: whether modules are grouped by feature, layer, bounded context, or generated CRUD.
- Data access: Prisma service/client, TypeORM repositories, MikroORM, Sequelize, raw SQL, or external API clients.
- Existing examples: nearest similar module/controller/service/DTO/spec.

## Reference Routing

Read only the reference files needed for the task:

- `references/architecture.md`: modules, DI, providers, boundaries, circular dependencies, lifecycle hooks.
- `references/api-validation-security.md`: controllers, DTOs, pipes, serialization, auth, guards, rate limits, file uploads.
- `references/data-access.md`: Prisma, TypeORM, transactions, migrations, N+1 prevention, query placement.
- `references/testing.md`: unit, integration, e2e, mocks, test modules, database tests.
- `references/review-refactor.md`: code review checklist and safe refactor workflow.

Do not read every reference by default. Load the smallest relevant set, then inspect source files around the change.

## Implementation Workflow

1. Locate the closest existing implementation and mirror its structure.
2. Define or update DTOs first for API inputs and outputs when request/response contracts change.
3. Update controller methods only as thin request adapters: parse, validate, authorize, call service, return typed result.
4. Put business behavior in services or existing domain classes. Keep database calls behind the local data-access pattern.
5. Update module providers/imports/exports only when a dependency boundary requires it.
6. Add focused tests for changed behavior, especially authorization, validation, transactions, and error paths.
7. Run the repository's existing verification commands and report any command that cannot run.

## Review Workflow

For NestJS reviews, prioritize findings in this order:

1. Security and authorization bypasses.
2. Input validation gaps and unsafe file handling.
3. Broken DI/module exports, circular dependencies, and request-scope leaks.
4. Transaction consistency, N+1 queries, and migration risks.
5. API contract regressions and missing tests for changed behavior.

Give file and line references for findings. Avoid style-only comments unless they hide a maintainability or behavior risk.
