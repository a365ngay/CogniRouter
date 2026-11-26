---
name: senior-go
description: Use when designing, implementing, debugging, reviewing, or refactoring Go services, CLIs, or libraries, including packages and interfaces, error handling, context, goroutines and channels, concurrency, HTTP or gRPC servers, database access, modules, tests, benchmarks, or profiling.
---

# Senior Go

## Role

Write idiomatic Go: small packages with clear APIs, explicit error handling, context-aware and leak-free concurrency, and code that `go vet` and the race detector accept.

## Before Editing

1. Inspect Go version, module layout (`cmd/`, `internal/`, `pkg/`), HTTP/gRPC framework, database layer (database/sql, sqlx, pgx, GORM, sqlc), configuration, logging (`slog`, zap, zerolog), linters (`golangci-lint`), and test conventions.
2. Trace the request or job from handler through context, validation, service logic, storage, and external calls.
3. Follow the existing structure; do not add a framework, DI container, or abstraction layer for one change.

## Implementation Rules

- Return errors, do not panic, in library and request paths. Wrap with context (`fmt.Errorf("load user %d: %w", id, err)`) and check with `errors.Is`/`errors.As`. Never ignore an error silently.
- Accept `context.Context` as the first parameter for request-scoped work; respect cancellation and deadlines in I/O and loops.
- Every goroutine needs a clear owner and exit path. Use `errgroup`, `sync.WaitGroup`, or channels with defined close semantics; protect shared state with mutexes or confine it to one goroutine.
- Define small interfaces where they are consumed, not where implemented. Keep exported API surface minimal and documented.
- Close resources (`defer rows.Close()`, response bodies) and check `rows.Err()`. Set timeouts on HTTP clients and servers.
- Use parameterized queries, validate input, and never log secrets. Use structured logging consistent with the project.

## Testing and Verification

Run `gofmt`/`goimports`, `go vet`, the project's linter, and `go test ./... -race`. Prefer table-driven tests; add benchmarks for performance-sensitive changes and use `pprof` for evidence.

## Review Checklist

- Are all errors handled or deliberately returned with context?
- Can any goroutine leak, deadlock, or race?
- Is context propagated and honored for I/O?
- Are interfaces and packages small, and is the exported API intentional?
