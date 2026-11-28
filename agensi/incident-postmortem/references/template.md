# Templates

## Postmortem

```markdown
# Postmortem: <short title describing the failure, not the person>

| | |
|---|---|
| Date | YYYY-MM-DD |
| Severity | SEVn (scale: ...) |
| Duration of impact | HH:MM–HH:MM <TZ> (N min) |
| Status | Draft / In review / Final |
| Authors | <roles or names> |
| Incident commander | <role or name> |

## Summary
Three to five sentences: what users experienced, for how long, the trigger, how it was
mitigated, and the single most important follow-up.

## Impact
- Users / customers: ...
- Requests / orders / jobs failed: ... (source or calculation)
- Revenue or SLA: ... (estimate, method)
- Error budget: ... of the monthly budget for <SLO>
- Support: N tickets / chats
- Data: lost / corrupted / none (how verified)

## Timeline (all times <TZ>)
| Time | Event | Source |
|---|---|---|
| ... | Trigger: ... | deploy log |
| ... | Impact starts | error-rate graph |
| ... | Alert fires / first report | alert name |
| ... | Decision: ... (what was known then) | #channel |
| ... | Mitigation | ... |
| ... | Impact ends | ... |
| ... | Resolved / all clear | ... |

## Response metrics
| Metric | Value | From → to |
|---|---|---|
| Time to detect | | impact start → first alert/report |
| Time to acknowledge | | alert → human ack |
| Time to first mitigating action | | impact start → first action that reduced impact |
| Time to mitigate | | impact start → impact stopped |
| Time to resolve | | impact start → incident closed |
Longest gap and why: ...

## Causes
**Trigger:** ... [Confirmed / Likely / Hypothesis: evidence]
**Root cause(s):** ... [Confirmed / Likely / Hypothesis: evidence]
**Contributing factors:**
1. ... (category: change management / testing / detection / response / capacity / dependency / knowledge)

Why chain (optional):
1. Why did X happen? Because ...
...

## What went well
## What went wrong
## Where we got lucky

## Action items
| # | Action | Type | Addresses | Priority | Owner | Due | Ticket |
|---|---|---|---|---|---|---|---|

## Open questions
## Appendix (graphs, queries, links)
```

Keep the summary readable by someone outside the team. Put long logs in the appendix, not the timeline. Fields you have no data for (Authors, Ticket) may be dropped or left as `TBD`. Translate headings and labels into the user's language.

## Status update (during the incident)

```text
[<Investigating | Identified | Monitoring | Resolved>] <service>: <user-visible symptom>
Impact: <who, what, since HH:MM TZ>
Known: <facts only>
Doing now: <next action>
Next update: <time>
```

## Customer-facing summary

```markdown
**<Date>: <Service> <symptom> (resolved)**

Between HH:MM and HH:MM <TZ>, some customers <could not ...>. <Who was affected and how much,
in customer terms.> <Data/payments statement if relevant and verified.>

**What happened:** one or two sentences, no internal jargon or names.
**What we did:** how it was fixed.
**What we are changing:** one to three concrete changes, no dates unless given.

We are sorry for the disruption. <Contact / credit / retry instructions if applicable.>
```

Tone: plain, specific, accountable ("we"), no blame of vendors or staff, no speculation. Do not mention security details that could help an attacker.
