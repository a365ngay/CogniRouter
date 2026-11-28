# Listing: User Story & Acceptance Criteria Writer

- **Title:** User Story Writer: Turn Rough Requests into Sprint-Ready Stories
- **Price:** Free
- **Category:** Product Management (secondary: Business & Operations)
- **Tags:** user-stories, acceptance-criteria, gherkin, given-when-then, business-analysis, product-owner, backlog-refinement, jira, agile, requirements
- **Works with:** Claude Code, Codex CLI, Cursor, Gemini CLI, Copilot, OpenClaw, any agent that reads SKILL.md
- **Upload:** `dist/agensi/user-story-writer.zip` · **Logo:** `docs/assets/agensi/user-story-writer-logo.png`

## Short description (one line)

Paste a messy request, chat message or meeting note and get a sprint-ready user story with numbered Given/When/Then criteria, business rules, edge cases and the questions to ask before anyone writes code.

## Long description

**Stop shipping stories that say "should work correctly".** User Story Writer turns whatever you have into a story a developer can build and a tester can verify without coming back to ask what you meant.

**Three modes, picked automatically**
- **Write** — from a Slack message, email, transcript, screenshot or a one-line idea to a complete story card.
- **Review** — scores an existing ticket against INVEST and Definition of Ready, lists the gaps that will cause rework, and gives you a rewritten version with every change explained.
- **Split** — breaks an epic into thin vertical slices (never "backend story / frontend story") and tells you which slice to build first.

**Every story card includes**
- A specific role and a real business outcome in the "so that"
- Business rules numbered separately from the UI (BR1, BR2 ...)
- Numbered Given/When/Then acceptance criteria with concrete values and exact error text, plus examples tables for boundaries
- Edge cases and unhappy paths: each one covered, out of scope, or raised as a question
- Out of scope, assumptions and open questions (with who should answer)

**Built-in quality gates** — vague words like *fast*, *user-friendly*, *properly* and *etc.* get replaced with numbers and observable results before you see the output.

Works in any language and answers in yours. Maps onto your Jira, Azure DevOps or Linear template when you have one.

**Pairs with:** *Test Case Generator* (free) — feed it the acceptance criteria and get traceable test cases with boundaries and a smoke set. Need a full SRS document with screens? See *BA SRS Builder*.

## Try it

> Write a user story: marketing wants voucher codes at checkout, 10% off capped at $8 or fixed $5 off, min order $30, usage limit and start/end dates.

> Review this ticket and tell me if it's ready for the sprint: <paste ticket>

> Split this epic into stories: customers can manage their subscriptions (upgrade, downgrade, pause, cancel, invoices).
