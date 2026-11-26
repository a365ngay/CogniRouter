---
name: senior-test-automation
description: Use when designing, implementing, debugging, reviewing, or improving automated tests, test frameworks, unit tests, API tests, integration tests, end-to-end tests, CI quality gates, test data, flaky tests, or test observability.
---

# Senior Test Automation

## Role

Build automation that gives fast, trustworthy feedback on product behavior. Optimize for reliability and diagnostic value, not raw coverage or UI test count.

## Strategy Workflow

1. Inspect the product risk, existing test pyramid, test runner, fixtures, environment, CI history, flaky tests, contracts, and observability before adding tests.
2. Choose the lowest stable layer that proves the behavior: unit for rules, integration for boundaries, contract/API for public behavior, end-to-end for a small set of critical journeys.
3. Make each test independent, deterministic, readable, and focused on observable behavior. Name the behavior and use Arrange-Act-Assert or an established local style.
4. Control time, randomness, network, clock, concurrency, external dependencies, identity, and data lifecycle. Prefer controllable test doubles at external boundaries; do not mock the behavior under test.
5. Integrate tests into existing CI gates with useful artifacts, failure output, retry policy only for known infrastructure instability, and no silent quarantine.
6. Review failures as product signals: classify code defect, test defect, environment failure, data issue, or nondeterminism; eliminate root causes rather than repeatedly increasing timeouts.

## Implementation Rules

- Test the contract and user-visible result, not private implementation details, CSS selectors, call order, or mock internals unless that is the explicit contract.
- Use stable selectors and accessible roles/names for browser tests. Avoid arbitrary sleeps; wait for meaningful state, event, network completion, or deterministic condition.
- Seed minimal, isolated data through supported APIs or fixtures. Ensure parallel execution isolation and cleanup. Never point destructive automation at production without explicit authorization and safeguards.
- Cover validation, authorization, error mapping, boundary values, retry/idempotency, and the failure/recovery paths that create the most user or data risk.
- Keep fixtures and helpers small; do not hide essential business intent in generic abstractions.

## Quality Gate

Before concluding, verify the test fails for the intended reason before the behavior exists or is fixed, passes afterward, can run repeatedly locally and in CI, produces actionable diagnostics, and has a documented scope and residual risk.
