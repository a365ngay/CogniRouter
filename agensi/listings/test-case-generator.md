# Listing: Test Case Generator

- **Title:** Test Case Generator: Traceable Test Cases from Any Requirement
- **Price:** Free
- **Category:** Testing & Debugging (secondary: Product Management)
- **Tags:** test-cases, qa, testing, boundary-value-analysis, equivalence-partitioning, decision-table, test-plan, uat, testrail, xray, gherkin
- **Works with:** Claude Code, Codex CLI, Cursor, Gemini CLI, Copilot, OpenClaw, any agent that reads SKILL.md
- **Upload:** `dist/agensi/test-case-generator.zip` · **Logo:** `docs/assets/agensi/test-case-generator-logo.png`

## Short description (one line)

Turn user stories, acceptance criteria, specs, API docs or a diff into risk-prioritized test cases with exact test data and expected results, a coverage map, a smoke set, and CSV ready for Excel, TestRail, Xray or Zephyr.

## Long description

**Fewer, sharper test cases that catch the bugs that matter.** Test Case Generator designs tests the way a senior QA engineer does: model the inputs, find the boundaries, rate the risk, then write only the cases worth running.

**Real test design, not a list of happy paths**
- Equivalence partitioning and boundary values ($29.99 / $30.00 / $30.01, 23:59 / 00:00, 20 / 21 characters)
- Decision tables for combined rules, state transitions for statuses, pairwise for configuration explosions
- A cross-cutting checklist for forms, permissions, money, dates and time zones, files, APIs, integrations, notifications, concurrency and accessibility

**Every run gives you**
- **Requirement gaps first.** Ambiguous or missing expected results are flagged as questions, never invented.
- **Coverage map** from each requirement to its tests, with risk and technique.
- **Test cases** with concrete data, numbered steps and exact expected results, all traceable to requirement IDs.
- **Smoke set** of P1 cases, **automation candidates** with reasons, and what was deliberately not covered.

**Output your way:** compact Markdown table, detailed manual or UAT scripts, Gherkin scenarios for BDD, or CSV with the right columns for Excel, TestRail, Xray or Zephyr Scale.

Works from a bug fix (reproduce + same root cause + regression) or a code diff too. Works in any language and answers in yours.

**Pairs with:** *User Story Writer* (free) — write the story first, then hand its acceptance criteria to this skill. Need a full SRS with screens? See *BA SRS Builder*.

## Try it

> Generate test cases for this story and its acceptance criteria: <paste story>

> What should I test in this PR? <paste diff or link>

> Write UAT scripts for the password reset flow and export CSV for TestRail.
