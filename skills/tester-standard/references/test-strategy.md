# Test Strategy

Use this reference for scope, risk analysis, coverage planning, and release recommendations.

## Risk Model

Prioritize tests by impact and likelihood:

- Critical user journeys and revenue/operational workflows.
- Authentication, authorization, privacy, and audit trails.
- Data creation/update/delete, migrations, sync, offline behavior.
- External integrations, background jobs, notifications, file uploads/downloads.
- Browser/device/platform differences.
- Recently changed or historically flaky areas.

## Scope Definition

For each test cycle, define:

- In scope: features, platforms, roles, APIs, data states.
- Out of scope: explicitly excluded areas.
- Entry criteria: build/deployment, test data, access, environment.
- Exit criteria: pass threshold, severity limits, resolved blockers.

## Test Levels

Choose levels intentionally:

- Unit: pure logic and validation.
- Integration/API: service contracts, database, auth, integrations.
- UI/component: rendering, forms, workflow behavior.
- E2E: end-user flows across pages/services.
- Exploratory: unknown risks and usability.

## Release Risk Summary

Summaries should include:

- What was tested.
- What passed and failed.
- Open defects by severity.
- Untested areas and why.
- Go/no-go recommendation or risk acceptance needed.
