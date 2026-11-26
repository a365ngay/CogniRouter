# Discovery And Decisions

Use this reference for architecture context, constraints, option analysis, and ADRs.

## Architecture Context

Gather:

- Business goal and success metrics.
- Users, roles, scale, and critical workflows.
- Existing systems, repositories, modules, and deployment topology.
- Constraints: budget, timeline, team skills, platform, compliance, offline/mobile needs.
- Non-goals and explicit exclusions.

## Decision Inputs

For each meaningful decision, identify:

- Forces: what makes this hard.
- Options considered.
- Tradeoffs.
- Recommendation.
- Consequences.
- Reversibility.

## ADR Template

```text
Title:
Status: Proposed / Accepted / Superseded
Context:
Decision:
Options considered:
Consequences:
Validation plan:
```

Use ADRs for decisions that affect multiple teams, long-lived APIs/data, deployment, security, or operating model.

## Avoiding Over-Architecture

Do not introduce microservices, event buses, CQRS, distributed caches, or complex platform tooling unless requirements justify the operational cost.

Prefer modular monolith boundaries before service extraction when team size and deployment model are modest.
