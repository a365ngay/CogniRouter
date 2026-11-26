# Discovery And Scope

Use this reference for requirement elicitation, assumptions, scope boundaries, and stakeholder clarification.

## Discovery Questions

Ask only questions that change delivery. Common high-value questions:

- Who uses this and what job are they trying to complete?
- What problem exists today and what outcome proves it is solved?
- What roles, permissions, channels, or platforms are involved?
- What data is created, changed, deleted, imported, exported, or reported?
- What exceptions, failure states, and recovery paths matter?
- What must be included in this release and what can wait?

## Scope Template

```text
Goal:
In scope:
Out of scope:
Actors/Roles:
Assumptions:
Dependencies:
Open questions:
Success metrics:
```

## Assumptions

State assumptions explicitly and tie them to impact.

Example: `Assumption: only admins can delete locations. Impact: if editors can delete, permissions and test coverage must expand.`

## Definition Of Ready

A requirement is ready when:

- The user/business outcome is clear.
- Scope and exclusions are explicit.
- Acceptance criteria are testable.
- Dependencies and data needs are known.
- Designs/API contracts are available or explicitly not needed.
- Open questions are not blocking implementation.
