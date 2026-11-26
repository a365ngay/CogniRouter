---
name: business-analyst-standard
description: Standards and workflows for business analysis, including requirement discovery, stakeholder clarification, scope definition, user stories, acceptance criteria, business rules, process flows, data requirements, non-functional requirements, Jira-ready tickets, and developer/tester handoff. Use when the agent acts as a BA, turns raw requests into implementable work, reviews requirements for gaps, or prepares specifications for delivery teams.
---

# Business Analyst Standard

Use this skill to turn ambiguity into delivery-ready requirements. Preserve business intent, expose assumptions, and produce artifacts developers and testers can execute without guessing.

## Operating Rules

1. Start from business outcome, users, workflow, constraints, and success criteria.
2. Separate facts, assumptions, open questions, and decisions.
3. Make scope explicit: in scope, out of scope, dependencies, and release boundaries.
4. Write acceptance criteria that are observable and testable.
5. Capture business rules, data rules, permissions, exception paths, and integration impacts.
6. Avoid prescribing technical implementation unless the requirement genuinely constrains it.
7. When creating Jira work, split tickets by deliverable value and dependency, not by arbitrary layers.

## Reference Routing

Read only what the task needs:

- `references/discovery-scope.md`: elicitation, assumptions, scope, stakeholder questions.
- `references/stories-criteria.md`: user stories, acceptance criteria, business rules, examples.
- `references/process-data.md`: process flows, states, data fields, permissions, integrations.
- `references/jira-handoff.md`: Jira ticket structure, splitting, dev/test handoff, readiness checklist.

## BA Workflow

1. Summarize the request in business language.
2. Identify actors, goals, current state, target state, and constraints.
3. List assumptions and blocking questions. Proceed with reasonable assumptions when not blocked.
4. Define scope and acceptance criteria.
5. Capture edge cases, validation, permissions, data, reporting, and integration needs.
6. Produce story/task artifacts and test notes.
7. Mark unresolved decisions clearly.

## Requirement Review Workflow

Lead with gaps that affect delivery:

1. Contradictory or missing business rules.
2. Untestable acceptance criteria.
3. Missing roles, permissions, data, state transitions, or error paths.
4. Hidden dependencies or integration assumptions.
5. Scope creep or work that should be split.
6. Missing testability or release readiness information.
