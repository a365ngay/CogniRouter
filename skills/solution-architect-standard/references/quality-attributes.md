# Quality Attributes

Use this reference for non-functional requirements and architecture risks.

## Security

Define trust boundaries, authentication, authorization, secret handling, audit logging, input validation, output encoding, and data access controls.

Use least privilege. Client-side checks are UX aids, not security boundaries.

## Reliability

Specify failure modes:

- What happens when dependencies are down?
- What can retry safely?
- What must be idempotent?
- What needs fallback or degraded mode?
- How does rollback work?

## Performance And Scalability

Tie performance design to expected load and user experience.

Consider pagination, indexing, caching, batching, async jobs, compression, CDN, and query optimization before service extraction.

## Observability

Define logs, metrics, traces, alerts, dashboards, and audit events needed to operate the feature.

For background jobs and integrations, include job status and failure visibility.

## Maintainability

Prefer simple module boundaries, clear ownership, typed contracts, migration safety, and tests at architecture boundaries.

Avoid designs that require every future feature to touch many layers or repositories without clear reason.

## Offline And Mobile

For mobile/offline systems, define cache ownership, sync trigger, conflict handling, package/versioning, storage limits, and background execution constraints.
