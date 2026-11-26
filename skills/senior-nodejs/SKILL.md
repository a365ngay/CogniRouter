---
name: senior-nodejs
description: Use when designing, implementing, debugging, reviewing, or refactoring Node.js backends and tooling with Express, Fastify, Koa, or Hono in JavaScript or TypeScript, including middleware, validation, async error handling, streams, workers, ORMs (Prisma, Drizzle, TypeORM, Sequelize), package management, tests, or performance. For NestJS use senior-nestjs.
---

# Senior Node.js

## Role

Build Node.js services that never block the event loop, handle every async failure, validate input at the edge, and shut down cleanly.

## Before Editing

1. Inspect Node version, module system (ESM/CommonJS), TypeScript config, framework, middleware order, validation library (zod, joi, ajv, TypeBox), ORM, logging (pino, winston), package manager and lockfile, and test runner (Vitest, Jest, node:test).
2. Trace the request from route through middleware, validation, auth, handler, data access, external calls, and error handler.
3. Follow existing structure; do not add a framework, DI container, or new ORM for one change.

## Implementation Rules

- Handle async errors on every path: await promises, forward errors to the framework's error handler (Express 4 needs `next(err)` or a wrapper), and never leave floating promises.
- Do not block the event loop: avoid sync fs/crypto in request paths, large `JSON.parse` on hot paths, and CPU-heavy work without worker threads or a queue.
- Validate and type request input with a schema at the boundary; never trust `req.body`, query, or headers.
- Use parameterized queries or the ORM's safe APIs; avoid N+1 queries and unbounded result sets.
- Set timeouts on outbound HTTP (`AbortSignal.timeout`), limit body sizes, apply rate limiting and security headers where the service is exposed.
- Read configuration from validated environment at startup; never commit secrets. Handle `SIGTERM` with graceful shutdown that drains connections.
- Use structured logging with request IDs; never log tokens, passwords, or personal data.

## Testing and Verification

Run type check, lint, unit tests, and API tests (supertest or framework inject). Use `npm audit` or the project's dependency check for changed dependencies. Measure with `--cpu-prof` or clinic for performance changes.

## Review Checklist

- Is every promise awaited or deliberately handled, with errors reaching the error handler?
- Can any request block the event loop?
- Is input validated and output shaped before leaving the service?
- Are dependencies, lockfile, and module format changes intentional?
