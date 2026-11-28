---
name: test-case-generator
description: "Generates risk-prioritized, traceable test cases from user stories, acceptance criteria, SRS or spec sections, screen descriptions, API specs, bug fixes or code diffs, using equivalence partitioning, boundary values, decision tables, state transitions and pairwise combinations. Produces a coverage map from each requirement to its tests, concrete test data, steps and expected results, a smoke and regression set, automation candidates, and the requirement gaps found along the way. Exports Markdown, Gherkin, or CSV ready to import into Excel, TestRail, Xray or Zephyr. Use whenever someone asks for test cases, test scenarios, a test plan or checklist, QA coverage, UAT scripts, edge cases or boundary tests for a feature, ticket, story, PR or API, even if they only say what should I test. Works in any language and answers in the user's language."
---

# Test Case Generator

Design the smallest set of test cases that would catch the bugs that matter, trace every one back to a requirement, and make each case runnable by someone who has never seen the feature.

## Workflow

1. **Read the source** (story, AC, spec, screen, API contract, diff). List the requirement IDs you will trace to. If the source has none, number them yourself (`R1`, `R2` ...) and show the list.
2. **Find the gaps first.** Anything ambiguous, contradictory, or missing an expected result goes into **Requirement gaps** (`G1` ...). Do not invent behavior: when the behavior itself is unknown, write `Expected: TBD — see G2`, or skip the case and say so. When only the wording is unknown, the case is still fully specified: state the behavior and a draft message, for example `Rejected; password unchanged; message "This link has expired." (wording per G1)`.
3. **Model the inputs and states.** For each requirement, identify the variables (fields, roles, statuses, dates, amounts, flags) and their partitions and boundaries. Pick the technique per requirement with the table below.
4. **Assess risk.** Rate each requirement High / Medium / Low by impact (money, data loss, security, legal, many users) times likelihood (new code, complex rules, integrations, concurrency, past bugs). Risk sets priority and depth.
5. **Generate cases.** Apply the techniques, then add the cross-cutting checks from `references/coverage-checklist.md` that apply to this feature type. Merge cases that would execute the same path with the same outcome.
6. **Build the coverage map.** Every requirement has at least one positive and one negative case, or a stated reason why not.
7. **Select sets.** Mark the smoke set (P1 cases that prove the feature works at all), regression candidates, and automation candidates.
8. **Self-check** with the quality gates, fix failures, then output.

## Pick the technique

| Requirement shape | Technique | Typical number of cases |
|---|---|---|
| A field or value with valid ranges or categories | Equivalence partitioning + boundary values | 2 to 3 per boundary, 1 per class |
| Several conditions combine into different outcomes | Decision table | 1 per meaningful rule column |
| An object moves through statuses | State transition (valid and invalid transitions) | 1 per valid transition + key invalid ones |
| Many independent options or configurations | Pairwise | far fewer than all combinations |
| A flow with alternatives | Use-case paths: main, alternatives, exceptions | 1 per path |
| Experience-based risk (past bugs, tricky areas) | Error guessing from the checklist | as needed |

Details and worked mini-examples: `references/design-techniques.md`.

## Priority

- **P1** — the feature is unusable, money or data is wrong, or security or compliance is broken if this fails. The smoke set is drawn from P1 cases: at most about 10, covering each high-risk requirement once (main success path first); remaining P1 cases go to the regression run.
- **P2** — an important rule or common alternative path fails; a workaround exists.
- **P3** — rare combination, cosmetic, or low-impact message wording.

## Test case format

Default to the compact table; switch to detailed cards when the user wants manual scripts or UAT, and to Gherkin when they automate with Cucumber, SpecFlow, Behave or Playwright-BDD. Formats and import columns: `references/output-formats.md`.

```markdown
| ID | Title | Req | Type | Pri | Preconditions | Test data | Steps | Expected result |
|----|-------|-----|------|-----|---------------|-----------|-------|-----------------|
| TC-01 | Apply fixed voucher at the minimum subtotal | AC3, BR3 | Boundary | P1 | WELCOME5 active, $5 off, min $30 | subtotal $30.00 | 1. Open checkout 2. Enter WELCOME5 3. Click Apply | Discount line "WELCOME5 −$5.00"; total $25.00 |
```

Types: Positive, Negative, Boundary, Permission, State, Integration, Non-functional, Regression.

## Quality gates (check before answering)

- **Concrete data.** Every case names its exact values: "subtotal $29.99", not "a value below the minimum".
- **Exact expected results.** Observable values, states and message text. Never "works correctly", "error is shown", "as expected".
- **One verification focus per case.** Several assertions are fine if they check the same outcome; two different behaviors means two cases.
- **Independent and repeatable.** Preconditions create what the case needs; no case depends on another case having run.
- **No duplicates.** Two cases with the same path and outcome are merged; an examples table is better than ten near-identical rows.
- **Traceable.** Every case lists its requirement IDs; every requirement appears in the coverage map.
- **Proportional.** The number of cases follows risk. A low-risk text change does not get 40 cases; a payment rule does not get 3.
- **Steps are actions, Expected is outcomes.** No "verify that" inside Steps.

## Output structure

```markdown
## Scope
Source, what is in and out of scope for testing, assumptions (A1 ...).

## Requirement gaps
G1 — <what is unclear> → <question, and who should answer> (blocks TC-xx)

## Coverage map
| Req | Risk | Cases | Techniques |
|-----|------|-------|-----------|

## Test cases
<table, cards or Gherkin>

## Smoke set
TC-01, TC-04, ...  (run first, about 15 minutes)

## Automation candidates
TC-xx — why (stable, data-driven, high regression value). Not: one-off exploratory checks.

## Not covered
What you deliberately left out and why (needs production data, performance environment, a decision in G2 ...).
```

Answer in the user's language; keep IDs and Given/When/Then keywords in English unless the team uses translated ones. For more than about 40 cases, give the coverage map and P1 cases first, then offer the full list or write it to a file.

When the user asks for CSV, the CSV replaces the test-case table; do not print the same cases twice. Write it to a `.csv` file when you can write files (UTF-8 with BOM), otherwise give it inline in a `csv` code block and tell the user to save it as "UTF-8 with BOM" for Excel. Use the column set for their tool from `references/output-formats.md`, or `templates/test-cases.csv` when the tool is unknown.

## When the input is code or a bug fix

- From a **diff**: derive behavior from the changed code paths, name the requirement you infer (`R1 (inferred)`), and add regression cases for callers and adjacent features.
- From a **bug fix**: one case that reproduces the original bug and must now pass, cases for the same root cause in neighboring inputs, and a regression check of the main path.

## References (read only what the task needs)

- `references/design-techniques.md`: partitioning, boundaries, decision tables, state transitions, pairwise, with examples.
- `references/coverage-checklist.md`: cross-cutting checks by feature type (forms, lists, auth, files, money, dates, APIs, integrations, notifications, i18n, concurrency, accessibility).
- `references/output-formats.md`: compact table, detailed cards, Gherkin, and CSV columns for Excel, TestRail, Xray and Zephyr.
- `examples/voucher-checkout.md`: complete worked example from acceptance criteria to traced test cases.
