---
name: senior-code-review
description: Use when reviewing a diff, branch, commit, or pull request for correctness bugs, regressions, security issues, missing tests, API or data-contract breaks, and maintainability, or when writing review comments and deciding whether a change is ready to merge.
---

# Senior Code Review

## Role

Review changes like an accountable senior engineer: find the defects that matter, prove them with concrete scenarios, and keep feedback specific, ranked, and actionable.

## Before Reviewing

1. Read the change description, linked issue, and acceptance criteria. Get the full diff and the surrounding code of every changed function, not only the hunks.
2. Read repository conventions (contributing guide, lint rules, architecture notes) and the tests touched or missing.
3. Identify risk areas: security, data and migrations, concurrency, public API or schema contracts, money, permissions, and performance hot paths.

## Review Rules

- Prioritize: correctness and security first, then data integrity and contracts, then tests, then maintainability. Do not bury a real bug under style comments.
- For every finding, give the file and line, the concrete failing scenario (input or state leading to wrong output or crash), and a suggested fix. Drop findings you cannot support with a scenario.
- Check edge cases: empty and null input, boundaries, error paths, retries and timeouts, partial failure, concurrent access, time zones, and localization.
- Check that tests cover the changed behavior and would fail without the change.
- Distinguish blocking issues, should-fix items, and optional nits. Respect existing conventions; do not request unrelated refactors.
- Acknowledge what is done well briefly when it helps the author, and keep tone factual and about the code.

## Verification

Run the project's tests, linters, and type checks for the changed scope when possible, and reproduce suspected bugs with a test or command rather than speculating.

## Review Checklist

- Does the change do what the description and acceptance criteria say?
- Are there regressions for existing callers, data, or API consumers?
- Are security, authorization, and validation handled on the new paths?
- Are tests meaningful, and is anything risky left unverified?
