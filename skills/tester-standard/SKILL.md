---
name: tester-standard
description: Standards and workflows for test analysis, QA planning, test case design, exploratory testing, regression testing, API/UI/mobile test execution, automation recommendations, bug reporting, and release risk assessment. Use when the agent acts as a tester, validates a feature, reviews acceptance criteria, writes or reviews test cases, reproduces bugs, creates defect reports, or prepares testing handoff for Jira or development teams.
---

# Tester Standard

Use this skill to test by risk, not by ritual. Start from the requirement and user workflow, identify what can fail, then choose focused manual or automated checks.

## Operating Rules

1. Understand the change, affected users, entry points, data, integrations, and acceptance criteria before designing tests.
2. Prioritize high-risk behavior: money/data loss, auth, permissions, sync, destructive actions, migrations, offline/background behavior, and cross-platform differences.
3. Separate test analysis from execution evidence. Say what was tested, what data was used, what passed/failed, and what remains untested.
4. Reproduce bugs with minimal steps and collect clear evidence: expected, actual, environment, logs/screenshots when available, and likely scope.
5. Recommend automation only for stable, repeatable checks with clear assertions. Do not automate vague exploratory work.
6. When linked to Jira, keep outputs story-ready: test scenarios, acceptance coverage, defects, retest notes, and residual risk.

## Reference Routing

Read only what the task needs:

- `references/test-strategy.md`: risk analysis, scope, coverage, release decisions.
- `references/test-cases.md`: scenario design, test data, edge cases, acceptance coverage.
- `references/execution-bugs.md`: execution notes, defect reports, retesting, regression.
- `references/automation.md`: automation selection, API/UI/mobile test guidance, flake prevention.

## Test Workflow

1. Parse requirement, ticket, PR, or implementation diff.
2. Identify assumptions and ask only blocking questions. Otherwise state assumptions and proceed.
3. Map acceptance criteria to positive, negative, boundary, permission, and regression scenarios.
4. Execute available checks or provide an executable test plan when direct execution is not possible.
5. File/report defects with reproduction steps and severity rationale.
6. Summarize coverage, results, blockers, and residual risk.

## Review Workflow

When reviewing a feature from a tester stance, lead with findings:

1. Requirement/acceptance gaps.
2. Functional bugs and broken edge cases.
3. Security/permission issues.
4. Data consistency, migration, sync, or offline risks.
5. Missing or weak test coverage.
6. Usability/accessibility issues that affect task completion.

Use concise, reproducible evidence. Avoid vague quality commentary.
