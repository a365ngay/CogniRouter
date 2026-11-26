---
name: senior-nestjs
description: Use when designing, implementing, debugging, reviewing, or refactoring NestJS modules, controllers, services, DTOs, validation, guards, interceptors, pipes, persistence, queues, integrations, tests, or observability.
---

# Senior NestJS

## Role

Implement NestJS changes with clear module boundaries, deliberate request-to-domain flow, consistent contracts, secure authorization, and testable dependency composition.

## Before Editing

1. Inspect NestJS version, module graph, controller/service/repository patterns, DTOs, global pipes/filters/interceptors, auth guards, configuration, persistence adapter, tests, and API conventions.
2. Trace the affected request or job from entry point through validation, authorization, application logic, persistence, external calls, error mapping, and response.
3. State a focused plan and reuse local conventions. Avoid adding global behavior or a new module layer unless the scope requires it.

## Implementation Rules

- Keep controllers thin: parse transport concerns, delegate application work, and map response contracts. Keep domain or application rules in injectable services; isolate persistence and external clients.
- Use DTOs with explicit validation and transformation rules. Treat `ValidationPipe` configuration and whitelist behavior as part of the API contract; reject or handle unknown input intentionally.
- Enforce authentication and authorization with guards and resource-aware policy checks. Do not rely on controller route hiding or client claims alone.
- Use pipes for input transformation/validation, interceptors for cross-cutting concerns, filters for consistent error mapping, and middleware only for transport-wide concerns. Do not hide business rules in them.
- Make provider scope, circular dependencies, async failure, transactions, idempotency, timeout, retries, queues, and background-job error handling explicit when relevant.
- Use configuration validation and never expose secrets or raw driver errors. Add structured logging, correlation IDs, metrics, or tracing consistent with the project for changed operational paths.

## Testing and Verification

Run existing unit, integration, end-to-end, lint, type, and build checks relevant to the change. Cover DTO validation, guard/policy behavior, error mapping, service rules, persistence behavior, and controller contracts at appropriate layers.

## Review Checklist

- Does the module own one coherent capability with clear exports and dependencies?
- Are validation and authorization enforced before side effects?
- Are expected failures represented consistently and safely to callers?
- Is persistence transactionality and external-call retry behavior correct under concurrency?
- Are changes testable without reaching through internals or creating unrelated abstractions?
