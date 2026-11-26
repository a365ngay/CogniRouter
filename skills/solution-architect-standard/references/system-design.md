# System Design

Use this reference for components, boundaries, APIs, integrations, data ownership, and async flows.

## Boundaries

Define ownership clearly:

- UI/client responsibilities.
- API/application service responsibilities.
- Domain/business rules.
- Data access and persistence.
- External integrations.
- Background jobs and sync.

Avoid duplicate sources of truth. If duplication is necessary for offline/cache/search, define freshness and reconciliation rules.

## API And Contracts

Capture:

- Endpoint/event/message name.
- Consumer and producer.
- Request/response or payload schema.
- Auth and authorization requirements.
- Idempotency and retry behavior.
- Error codes and failure semantics.
- Versioning/backward compatibility.

## Data Architecture

For data changes, define:

- Entity ownership.
- Relationships and lifecycle.
- Validation and invariants.
- Migration/backfill plan.
- Retention, audit, and privacy concerns.
- Reporting/export needs.

## Async And Integration Flows

Use async processing for slow, retryable, or external side effects.

Define:

- Trigger.
- Queue/event/topic.
- Payload.
- Retry/dead-letter behavior.
- Idempotency key.
- Monitoring and operator recovery.

Do not make a distributed workflow when a transaction or simple background job is enough.
