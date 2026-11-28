# Listing: Incident Postmortem

- **Title:** Incident Postmortem: Blameless Reports from Slack and Logs
- **Price:** Free
- **Category:** DevOps & Infrastructure (secondary: Writing & Documentation, Productivity)
- **Tags:** postmortem, incident-management, sre, rca, root-cause-analysis, blameless, on-call, status-page, devops, reliability
- **Works with:** Claude Code, Codex CLI, Cursor, Gemini CLI, Copilot, OpenClaw, any agent that reads SKILL.md
- **Upload:** `dist/agensi/incident-postmortem.zip` · **Logo:** `docs/assets/agensi/incident-postmortem-logo.png`

## Short description (one line)

Paste the incident Slack thread, alerts and notes; get a blameless postmortem with a sourced timeline, quantified impact, time to detect and mitigate, root cause vs contributing factors, and action items that actually change something. Plus status page and customer texts.

## Long description

**Write the postmortem in 10 minutes, then spend the review on what to fix.** Incident Postmortem turns messy incident material into a document your team can learn from.

**From a chat export it builds**
- **Timeline** in one time zone, every row with its source, including what was known at each decision.
- **Impact with numbers**: failed requests, users, orders, tickets, error budget, each with its source or calculation, estimates labeled.
- **Response metrics**: time to detect, acknowledge, mitigate and resolve, and the longest gap and why.
- **Causes in three layers**: the trigger, the root cause, and the contributing factors in review, testing, detection and response. A why chain that asks about the system, not the person.
- **What went well, what went wrong, where we got lucky.**
- **Action items** typed prevent / detect / mitigate / process, each tied to a cause, with priority, owner and due date. No "be more careful".
- **Open questions** instead of invented facts.

**Also does**
- **Review** an existing postmortem: blame and hindsight language, vague actions, missing impact.
- **Status updates** during an incident and **customer-facing summaries** with no internal names or speculation.

Blameless by design, works in any language and answers in yours.

**Pairs with:** *DB Migration Safety Reviewer* (free), the example incident is a migration that locked the orders table.

## Try it

> Write the postmortem for yesterday's outage. <paste Slack thread + notes>

> Review this postmortem and make the action items better: <paste>

> Write the status page update: checkout errors since 14:03, cause unknown yet.
