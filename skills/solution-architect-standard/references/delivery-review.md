# Delivery And Review

Use this reference for implementation slicing, migration, rollout, validation, and architecture reviews.

## Implementation Slices

Break architecture into deliverable slices:

1. Data model and migration.
2. API/service contract.
3. UI/client workflow.
4. Background job/integration.
5. Observability and operations.
6. Test and rollout validation.

Each slice should have acceptance and verification notes.

## Migration And Rollout

For risky changes, plan:

- Backward-compatible schema/API changes.
- Feature flags or staged rollout.
- Backfill scripts and verification queries.
- Rollback path.
- Data reconciliation.
- Communication/operational steps.

## Architecture Review Checklist

Ask:

- Does the design solve the stated business goal?
- Are boundaries and ownership clear?
- Are security and data protection addressed?
- Are failure modes and rollback addressed?
- Are quality attributes explicit and testable?
- Is the design simpler than the problem allows?
- Can dev/test teams implement and validate it incrementally?

## Output Template

```text
Context:
Goals:
Non-goals:
Recommended design:
Components and responsibilities:
Data/API contracts:
Security and permissions:
Operational concerns:
Alternatives considered:
Implementation slices:
Validation plan:
Open questions:
```
