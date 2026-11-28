# Cause analysis

## Three layers

| Layer | Question | Example |
|---|---|---|
| Trigger | What changed right before impact? | Migration 0187 ran `CREATE INDEX` on `orders` |
| Root cause(s) | Why could that change cause this impact? | A non-concurrent index build blocks writes for its whole duration; on 45M rows that is tens of minutes |
| Contributing factors | Why did our defenses not prevent, catch or shorten it? | No lock timeout in the migration runner; staging 200× smaller; no review check for locking DDL; no runbook on whether cancelling is safe |

A trigger is rarely worth fixing on its own (the next one will be different). Root causes and contributing factors are where actions go.

## 5 whys, done well

- Ask "why" of the **system**, not the person: "Why was the index built non-concurrently?" → "Because the ORM's default `add_index` does that and nothing flagged it", not "Because the developer forgot".
- Branch when there are several answers; a causal tree is fine.
- Stop when the answer is something the organisation can change (a tool, a default, a check, a process, a capacity limit).
- Include the detection and response branch: "Why did mitigation take 16 minutes?"

## Factor categories (check each)

- **Change management**: review, rollout strategy (canary, feature flag), deploy timing, rollback path.
- **Testing**: missing test, unrealistic data volume, staging differences.
- **Detection**: no alert, alert too slow or noisy, dashboards missing the signal, customers noticed first.
- **Response**: unclear ownership, missing runbook, access or permissions delays, hesitation from uncertainty, communication gaps.
- **Design and capacity**: single points of failure, no rate limits or timeouts, retry storms, resource limits.
- **Dependencies**: third-party or internal platform behavior, unclear contracts.
- **Knowledge**: only one person knew; docs outdated.

## Blameless rewrites

| Instead of | Write |
|---|---|
| "John deployed a broken migration." | "Migration 0187 was deployed at 14:02; it contained a non-concurrent index build." |
| "The engineer failed to test on production-size data." | "Staging has 200k orders vs 45M in production, so the build took 3 s in staging." |
| "Human error." | Name the condition that made the error easy and undetected. |
| "Should have cancelled immediately." | "Cancelling was delayed 9 minutes because nobody on the call knew whether cancelling a running index build was safe." |
| "Careless", "obviously", "simply", "just" | Remove; describe the decision and what was known at the time. |
| "The vendor's outage caused..." (customer-facing) | "A failure in a service we depend on caused..." and what we will change on our side. |

Names in the timeline: use roles by default (IC, on-call engineer, DBA). Use names only if the organisation's postmortem culture does; never in a customer-facing text.
