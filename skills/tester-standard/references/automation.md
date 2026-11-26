# Test Automation

Use this reference for deciding what to automate and how to keep tests reliable.

## Automation Fit

Automate when a check is:

- Stable and repeatable.
- Valuable for regression.
- Has clear assertions.
- Can run in CI or a known local environment.

Do not automate exploratory questions, unstable UI timing, or flows without reliable test data.

## Pyramid Guidance

Prefer many fast unit/integration tests and fewer end-to-end tests. Use E2E for cross-system confidence, not every validation branch.

## UI Automation

Use user-facing selectors and accessibility roles where possible. Avoid brittle CSS based on layout internals.

Wait for real conditions: visible text, network completion, route changes, or stable app state. Avoid fixed sleeps.

## API Automation

Assert status code, response schema, important fields, side effects, auth behavior, and error cases.

Create and clean up test data safely. Never point destructive tests at production.

## Flake Prevention

- Isolate test data.
- Avoid order dependencies.
- Control time when needed.
- Mock only external unstable boundaries.
- Capture logs/screenshots/traces on failure.
