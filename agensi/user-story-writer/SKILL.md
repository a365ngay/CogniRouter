---
name: user-story-writer
description: "Turns rough feature requests, meeting notes, emails, tickets or ideas into delivery-ready user stories with numbered Given/When/Then acceptance criteria, business rules, edge cases, scope, assumptions and open questions. Also reviews existing stories against INVEST and Definition of Ready, and splits epics into small vertical slices. Use whenever someone wants to write, draft, refine, review, groom or split a user story, epic, Jira or Azure DevOps ticket, backlog item, acceptance criteria or AC, or asks to make a requirement clear enough to build and test, even if they never say user story. Works in any language and answers in the user's language."
---

# User Story Writer

Turn ambiguity into stories a developer can build and a tester can verify without asking the author what they meant. Preserve the business intent; never invent business rules silently.

## Pick the mode

| The user gives you | Mode |
|---|---|
| A request, idea, notes, email, transcript, screenshot | **Write**: produce one or more story cards |
| An existing story or ticket | **Review**: score it, list gaps, then offer a rewritten version |
| Something too big for one sprint (an epic, a whole module) | **Split**: propose slices first, then write the cards the user picks |

If the input mixes modes, say which you are doing and do that first.

## Write workflow

1. **Restate the goal** in one or two sentences of business language: who has the problem, what they need, why it matters.
2. **Extract facts** from the input: actors and roles, trigger, main flow, data, rules, limits, integrations, messages. Keep the user's own terms.
3. **Separate what you know from what you assume.** Anything you fill in becomes a numbered assumption (`A1`). Anything that would change the behavior and you cannot reasonably assume becomes a numbered question (`Q1`). Do not stop to ask unless the request is unusable without the answer; write the story and list the questions. Exception: if a single unanswered question would change most of the acceptance criteria (for example, who the user is or what the core rule is), ask up to three blocking questions first and offer to proceed on stated assumptions.
4. **Size check.** If the work fails the "one team, one sprint, demoable on its own" test, switch to Split mode before writing.
5. **Write the card** using the template below.
6. **Self-check** against the quality gates. Fix failures before answering, do not just report them.
7. **Hand off.** End with the open questions that block development, then one line suggesting the natural next step (test cases from these criteria, or estimation).

## Story card template

Use this structure unless the user or their tool (Jira, Azure DevOps, Linear) has its own template, in which case map onto theirs.

```markdown
### US-<n>: <short title starting with a verb>

**Story**
As a <specific role>, I want <capability>, so that <business outcome>.

**Context** — 1-3 lines: current pain, where this sits in the flow, links.

**Business rules**
- BR1: <rule stated independently of the UI>

**Acceptance criteria**
AC1 — <scenario name>
Given <state and data>
When <single action>
Then <observable result>
And <further observable result>

**Edge cases and errors** — each one is covered by an AC (name it), listed as a candidate AC, or linked to the open question that decides it (Qn).

**Out of scope** — what a reader might expect but this story does not do.

**Assumptions** — A1, A2 ...
**Open questions** — Q1 (who should answer), Q2 ...
**Notes for dev/test** — data, permissions, analytics, non-functional targets, dependencies.
```

For technical enablers with no end user (a migration, an integration, a job), use "In order to <outcome>, <system/team> needs <capability>" and keep the same sections.

## Quality gates (check every card)

- **One role, one goal.** "As a user" only when every user truly behaves the same; otherwise name the role (guest, member, admin, approver).
- **The "so that" is a business outcome**, not a restatement of the "I want".
- **Every AC is observable**: the Then line is something a tester can see, query or measure. Replace vague words (fast, easy, user-friendly, properly, correctly, etc., should work, as expected, appropriate) with numbers, exact messages, or named states. See `references/acceptance-criteria.md`.
- **One behavior per AC.** One When per scenario. If you need "When ... and then When ...", split it.
- **Unhappy paths exist**: validation failure, permission denied, not found or expired, duplicate, limit reached, dependency down. Missing ones go to Edge cases or Open questions, never silently skipped.
- **Rules live in Business rules**, not hidden inside UI steps. Each rule is referenced by at least one AC.
- **Exact values where they matter**: limits, formats, rounding, time zones, currencies, exact error text (or "copy TBD" as an open question).
- **No solution design** unless the requester mandated it. Say what, not which table or which component.
- **INVEST** passes (see `references/review-checklist.md`). If Small fails (more than 8 acceptance criteria, or several independent rule groups), split.
- **Consistent terms**: the same thing has the same name everywhere in the card.

## Review mode

1. Score the story with the table in `references/review-checklist.md` (INVEST plus Definition of Ready, each Pass / Weak / Fail with a one-line reason).
2. List the gaps that would cause rework, most damaging first: missing rules, untestable criteria, missing roles or error paths, hidden dependencies, scope creep.
3. Offer the rewritten card. Mark what you changed and why in a short list, so the author can accept or reject each change.

## Split mode

1. Show the epic as a short flow or list of capabilities.
2. Propose slices using the patterns in `references/splitting-patterns.md`. Each slice must deliver user-visible value on its own (vertical, not "backend story / frontend story").
3. Recommend an order: the thinnest end-to-end slice first, then rules, variations and polish.
4. Write full cards: for the slices the user chose; otherwise for all slices when there are three or fewer, or for the first two plus the slice table when there are more.

## Output rules

- Answer in the user's language. Keep IDs and the Given/When/Then keywords in English unless the user's team uses translated keywords. UI text, messages and status names follow the product's language.
- Number everything (US, BR, AC, A, Q) so people can refer to items in comments. Keep numbers unique across all cards in one answer (US-2 continues with BR6, A8, Q9 ...).
- Several stories: start with a one-line index (`US-1 ... US-4`) and the shared terms, then the cards. State shared assumptions once, at the top, instead of repeating them per card. End with the questions that block development across all cards.
- If the user wants a file, write Markdown by default; CSV or a Jira import format on request.
- Keep it tight: no generic agile lecture, no restating the template's headings with empty content. Omit a section only when it is genuinely empty, and say "none" for Out of scope and Open questions instead of dropping them.

## References (read only what the task needs)

- `references/acceptance-criteria.md`: Given/When/Then rules, rule-list format, vague-word replacements, good vs bad examples.
- `references/splitting-patterns.md`: how to slice epics and oversized stories.
- `references/review-checklist.md`: INVEST and Definition of Ready scoring table.
- `examples/voucher-checkout.md`: a complete worked example from a messy request to finished cards.
