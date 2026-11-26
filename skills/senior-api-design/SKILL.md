---
name: senior-api-design
description: Use when designing, reviewing, documenting, or evolving API contracts for REST, GraphQL, gRPC, webhooks, or events, including resource modeling, naming, HTTP methods and status codes, error formats, pagination, filtering, idempotency, versioning and deprecation, authentication, rate limits, or OpenAPI/AsyncAPI specs.
---

# Senior API Design

## Role

Design APIs that are consistent, hard to misuse, evolvable without breaking clients, and documented as a contract.

## Before Designing

1. Read existing API conventions (naming, casing, error format, pagination, auth, versioning) and any OpenAPI, GraphQL schema, or proto files.
2. Identify consumers, their use cases, expected volume, and compatibility requirements.
3. Treat any change to a published contract as potentially breaking until proven otherwise.

## Design Rules

- Model resources and operations from consumer use cases; use consistent nouns, casing, and identifiers across the API.
- Use HTTP methods and status codes by their semantics (201 with Location on create, 204 on empty success, 400/422 validation, 401 vs 403, 404, 409 conflict, 429 rate limit). Use one documented error format (for example RFC 9457 problem details) with machine-readable codes.
- Paginate every list (cursor-based for large or changing sets), with bounded page sizes and documented filtering and sorting.
- Make unsafe operations safe to retry with idempotency keys; make webhooks signed, retried with backoff, and idempotent for receivers.
- Evolve additively: new optional fields and endpoints are compatible; removing or renaming fields, changing types, or tightening validation is breaking and needs versioning and a deprecation period.
- Specify authentication, authorization scopes, rate limits, and timeouts. Never put secrets or personal data in URLs.
- For GraphQL, bound query depth and cost and avoid N+1 resolvers; for gRPC, never reuse or renumber proto field numbers.

## Verification

Keep the spec (OpenAPI, schema, proto) in sync with the implementation and validate it with the project's linter (Spectral, buf, graphql-inspector). Add contract or API tests for status codes, error bodies, and pagination.

## Review Checklist

- Is the contract consistent with the rest of the API?
- Is every change backward compatible, or versioned with a deprecation plan?
- Are errors, pagination, and idempotency defined?
- Is the spec accurate and validated?
