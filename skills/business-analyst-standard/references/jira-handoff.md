# Jira And Handoff

Use this reference for Jira-ready tickets, splitting work, and handing requirements to developers/testers.

## Ticket Template

```text
Summary:
Business goal:
User story / task outcome:
Scope:
Out of scope:
Acceptance criteria:
Business rules:
Data/permissions:
Design/API references:
Dependencies:
Test notes:
Open questions:
```

## Splitting Work

Split by deliverable value and dependency:

- Backend/API contract.
- CMS/admin workflow.
- Mobile/user workflow.
- Data migration or sync package.
- Reporting/export.
- Cross-cutting auth/audit/integration.

Avoid splitting only by technical layers when one story cannot be validated independently.

## Developer Handoff

Developers need:

- Inputs and outputs.
- API behavior and status/error expectations.
- Data model changes.
- Permissions.
- Edge cases.
- Compatibility/migration constraints.

## Tester Handoff

Testers need:

- Acceptance criteria traceability.
- Roles and test data.
- Positive/negative scenarios.
- Regression areas.
- Known assumptions and open risks.

## Readiness Checklist

Before marking ready:

- No blocking questions remain.
- AC are testable.
- Dependencies are linked or named.
- Scope boundaries are clear.
- Designs/contracts are attached or explicitly unnecessary.
