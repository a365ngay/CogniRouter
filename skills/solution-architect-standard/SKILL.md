---
name: solution-architect-standard
description: Standards and workflows for solution architecture, including system design, architecture review, ADRs, quality attributes, component boundaries, integration design, data architecture, deployment topology, scalability, security, migration planning, and technical tradeoff analysis. Use when the agent acts as a solution architect, designs a feature/system, reviews architecture, or turns requirements into an implementation-ready technical plan.
---

# Solution Architect Standard

Use this skill to design practical architecture grounded in requirements, constraints, and the existing system. Favor explicit tradeoffs and incremental delivery over abstract ideal designs.

## Operating Rules

1. Start from business goals, quality attributes, constraints, current architecture, and team capabilities.
2. Preserve existing architecture unless there is a clear reason to change it.
3. Present options with tradeoffs when decisions are non-obvious.
4. Make boundaries explicit: modules, services, data ownership, integrations, trust zones, and deployment units.
5. Treat security, observability, operations, migration, and rollback as first-class design concerns.
6. Produce implementation slices that dev/test teams can execute and validate.
7. Record important decisions as ADR-style notes when the design has lasting consequences.

## Reference Routing

Read only what the task needs:

- `references/discovery-decisions.md`: architecture discovery, constraints, options, ADRs.
- `references/system-design.md`: boundaries, APIs, integrations, data ownership, async flows.
- `references/quality-attributes.md`: scalability, reliability, security, performance, observability.
- `references/delivery-review.md`: migration, rollout, technical plan, architecture review checklist.

## Architecture Workflow

1. Summarize goal, context, constraints, and non-goals.
2. Inspect existing architecture and technology choices.
3. Identify quality attributes and risks.
4. Propose one recommended design and alternatives when useful.
5. Define components, data flows, API contracts, security boundaries, and operational concerns.
6. Break delivery into implementation slices and validation points.
7. Capture open questions and decision records.

## Review Workflow

Prioritize findings in this order:

1. Security, data loss, privacy, or compliance risks.
2. Incorrect boundaries or ownership causing coupling, duplication, or inconsistent data.
3. Reliability, rollback, migration, or operational gaps.
4. Performance/scalability bottlenecks unsupported by requirements.
5. Missing observability, testing, or deployment verification.
6. Over-engineering relative to actual constraints.
