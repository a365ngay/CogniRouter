---
name: senior-dotnet
description: Use when designing, implementing, debugging, reviewing, or refactoring C# and .NET applications, ASP.NET Core APIs or minimal APIs, Entity Framework Core, dependency injection, async code, configuration, authentication, background services, Blazor, tests, or performance.
---

# Senior .NET

## Role

Deliver .NET code with clean dependency injection, correct async and EF Core behavior, consistent API contracts, and secure configuration.

## Before Editing

1. Inspect target framework, solution/project layout, nullable reference types setting, API style (controllers vs minimal APIs), MediatR/CQRS usage, EF Core version and migrations, auth setup, options/config pattern, and test projects (xUnit/NUnit, WebApplicationFactory).
2. Trace the request from endpoint through model binding, validation, authorization, handlers/services, DbContext, external clients, and response mapping.
3. Keep to the solution's existing architecture; do not add a new layer, mediator, or mapping library for one feature.

## Implementation Rules

- Use async all the way: no `.Result`, `.Wait()`, or `async void` (except event handlers); pass `CancellationToken` through to EF Core and HTTP calls.
- Register services with the correct lifetime; never inject scoped services (such as `DbContext`) into singletons or hosted services without creating a scope.
- In EF Core, project to DTOs with `Select`, use `AsNoTracking` for reads, avoid N+1 and client-side evaluation, paginate, and generate migrations deliberately and review their SQL.
- Validate input (DataAnnotations or FluentValidation as the project does) and return the project's error contract (`ProblemDetails`).
- Enforce authorization with policies and resource checks; keep secrets in user-secrets, environment variables, or a vault, never `appsettings.json` in source.
- Use `IHttpClientFactory`, typed options with validation, structured logging (`ILogger` message templates), and health checks for changed operational paths.
- Respect nullable annotations; do not silence warnings with `!` unless the value is proven non-null.

## Testing and Verification

Run `dotnet build` with warnings reviewed, `dotnet test`, and integration tests via `WebApplicationFactory` or Testcontainers where the project has them. Check EF Core generated SQL for changed queries.

## Review Checklist

- Is async code non-blocking and cancellable?
- Are DI lifetimes and DbContext usage correct?
- Are queries efficient, bounded, and migrations safe for existing data?
- Are validation, authorization, and error mapping consistent with the rest of the API?
