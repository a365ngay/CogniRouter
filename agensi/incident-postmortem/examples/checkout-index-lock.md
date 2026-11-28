# Example: checkout errors during a migration (Slack thread → postmortem)

## Input (as the user sent it)

> Write the postmortem for yesterday's checkout incident (2026-11-12). Slack export from #inc-checkout, times are ICT:
>
> ```text
> 14:02 deploy-bot: orders-service v2.41.0 deploying to prod (migration 0187_orders_add_index)
> 14:04 alertmanager: [FIRING] CheckoutErrorRate > 5% (current 31%)
> 14:06 Minh: looking. lots of 500 on POST /checkout, db timeouts
> 14:09 Lan: pg shows many queries waiting on lock on orders, migration running CREATE INDEX
> 14:11 Minh: can we kill it? not sure if it's safe to cancel mid index build
> 14:14 Lan: declaring SEV2, I'm IC
> 14:15 Lan: status page updated "investigating checkout errors"
> 14:18 Huy (DBA): cancelling is safe, non-concurrent create index will roll back. doing pg_cancel_backend(48213)
> 14:19 Huy: cancelled, locks released
> 14:20 alertmanager: [RESOLVED] CheckoutErrorRate
> 14:23 Minh: error rate back to baseline 0.3%
> 14:35 Lan: not rolling back, v2.41.0 doesn't need the index. migration marked failed
> 14:40 Lan: status page resolved
> ```
> Notes: orders ~45M rows. Index build was estimated at 25+ min. Migrations run in the deploy pipeline with no lock_timeout. Staging orders has 200k rows, the migration took 3 s there. ~4,100 checkout attempts failed (logs, 14:03–14:19). Some customers retried. Huy checked payments at 15:10: 0 double charges. Support got 63 tickets.

## Output

# Postmortem: Checkout failed for 16 minutes while a migration blocked writes to `orders`

| | |
|---|---|
| Date | 2026-11-12 |
| Severity | SEV2 (as declared by the IC) |
| Duration of impact | 14:03–14:19 ICT (16 min) |
| Status | Draft |
| Incident commander | Declared at 14:14 (see timeline) |

## Summary
From 14:03 to 14:19 ICT, about 4,100 checkout attempts failed with HTTP 500. Deploy v2.41.0 of orders-service ran migration `0187_orders_add_index`, which built an index on the 45M-row `orders` table without `CONCURRENTLY`; that blocks all writes to the table for the whole build, estimated at 25+ minutes. Impact ended when the DBA cancelled the migration at 14:19. The most urgent follow-up: migration 0187 is still pending and will run again on the next deploy unless it is changed first.

## Impact
- Customers: about 4,100 failed checkout attempts between 14:03 and 14:19 (application logs). Some customers retried; how many later completed an order is unknown (see open questions).
- Error rate: peak 31 % on checkout (alert at 14:04), baseline 0.3 % (14:23).
- Payments: 0 double charges (checked by the DBA at 15:10).
- Support: 63 tickets.
- Revenue and SLO error budget: not yet calculated.

## Timeline (all times ICT, 2026-11-12)
| Time | Event | Source |
|---|---|---|
| 14:02 | Trigger: deploy of orders-service v2.41.0 starts, including migration `0187_orders_add_index` | deploy-bot |
| 14:03 | Impact starts: checkout requests begin failing | application logs (per notes) |
| 14:04 | Alert `CheckoutErrorRate > 5%` fires at 31 % | alertmanager |
| 14:06 | On-call engineer acknowledges; sees 500s on `POST /checkout` and database timeouts | #inc-checkout |
| 14:09 | Cause identified: many queries waiting on a lock on `orders`; migration running `CREATE INDEX` | #inc-checkout |
| 14:11 | Cancelling considered; on-call engineer unsure whether cancelling a running index build is safe | #inc-checkout |
| 14:14 | SEV2 declared; IC assigned | #inc-checkout |
| 14:15 | Status page: "investigating checkout errors" | #inc-checkout |
| 14:18 | DBA confirms a non-concurrent `CREATE INDEX` rolls back cleanly; runs `pg_cancel_backend(48213)` | #inc-checkout |
| 14:19 | Impact ends: migration cancelled, locks released | #inc-checkout, logs |
| 14:20 | Alert resolves | alertmanager |
| 14:23 | Error rate back to baseline 0.3 % | #inc-checkout |
| 14:35 | Decision: keep v2.41.0 (does not need the index); migration recorded as failed | #inc-checkout |
| 14:40 | Status page resolved | #inc-checkout |
| 15:10 | Payments checked: no double charges | notes |

## Response metrics
| Metric | Value | From → to |
|---|---|---|
| Time to detect | 1 min | 14:03 impact → 14:04 alert |
| Time to acknowledge | 2 min | 14:04 alert → 14:06 on-call |
| Time to first mitigating action | 15 min | 14:03 → 14:18 cancel |
| Time to mitigate | 16 min | 14:03 → 14:19 |
| Time to resolve | 37 min | 14:03 → 14:40 status page resolved |

Longest gap: **9 minutes** between identifying the blocking migration (14:09) and cancelling it (14:18), because nobody on the call knew whether cancelling was safe until the DBA joined. Status page went out 12 minutes after impact started.

## Causes
**Trigger:** migration `0187_orders_add_index` ran during the v2.41.0 deploy. [Confirmed: deploy log, lock waits seen at 14:09]

**Root cause:** the migration built an index with plain `CREATE INDEX`, which holds a `SHARE` lock on `orders` and blocks every insert and update for the entire build. On 45M rows the build was estimated at 25+ minutes, so checkout could not write orders. [Confirmed: impact stopped when it was cancelled]

**Contributing factors**
1. *Change management:* the migration runner sets no `lock_timeout` or `statement_timeout`, so the blocking statement could run indefinitely.
2. *Change management:* nothing in review or CI flags locking DDL such as non-concurrent index builds.
3. *Testing:* staging `orders` has 200k rows (about 225× smaller), so the migration took 3 s there and looked harmless.
4. *Response:* no runbook for "migration blocking production"; the safe-to-cancel decision waited 9 minutes for a DBA.
5. *Response:* SEV declared and status page posted 11–12 minutes into impact.

Why chain
1. Why did checkout fail? Inserts into `orders` waited on a lock and timed out.
2. Why was there a lock? The migration's `CREATE INDEX` blocks writes while it builds.
3. Why was a blocking form used? The default index migration is non-concurrent, and no check or reviewer flagged it.
4. Why didn't testing catch it? Staging data is too small for the duration to show.
5. Why did it last 16 minutes? No timeout stopped it, and the cancel decision depended on one person's knowledge.

## What went well
- The alert fired within a minute of impact.
- The cause was identified 5 minutes after the alert.
- Cancelling rolled back cleanly; no data was lost and no customer was double-charged.

## What went wrong
- Writes to the busiest table were blocked by a routine deploy.
- 9 minutes of hesitation over whether cancelling was safe.
- Customers learned about the problem from failures before the status page said anything.

## Where we got lucky
- A DBA who knew the cancel behavior was reachable within minutes.
- Migration 0187 has not run again yet; the next deploy would repeat the incident unless it is fixed (A1).

## Action items
| # | Action | Type | Addresses | Priority | Owner (proposed) | Due (proposed) |
|---|---|---|---|---|---|---|
| A1 | Change migration 0187 to build the index with `CONCURRENTLY` outside a transaction; block deploys of orders-service until merged | Prevent | Root cause | P1 | Orders team | Before next deploy |
| A2 | Migration runner sets `lock_timeout = 5s` and `statement_timeout` for every migration session | Prevent | Factor 1 | P1 | Platform team | 2026-11-19 |
| A3 | CI runs a migration linter (for example `squawk`) and fails on non-concurrent index builds and table rewrites | Prevent | Factor 2 | P1 | Platform team | 2026-11-26 |
| A4 | Runbook "Migration blocking production": blocking query, `pg_cancel_backend` vs `pg_terminate_backend`, when cancelling is safe; linked from DB lock alerts | Mitigate | Factor 4 | P2 | DBA team | 2026-11-26 |
| A5 | Alert on lock waits on the orders database (more than 20 sessions waiting over 60 s) | Detect | Factor 4 | P2 | SRE | 2026-12-03 |
| A6 | Time-boxed spike: estimate migration duration against a production-size snapshot before deploy | Prevent | Factor 3 | P2 | Platform team | 2026-12-10 |
| A7 | IC checklist: declare severity and post the status page within 5 minutes of a customer-facing alert | Process | Factor 5 | P3 | Incident process owner | 2026-12-03 |

Owners are proposed by team; confirm in the review.

## Open questions
- How many of the ~4,100 failed attempts were later completed by the same customers? Needed for the revenue estimate.
- Which SLO covers checkout, and how much of its monthly error budget was used?
- What prevented double charges (payment idempotency keys or luck)? Worth confirming, since a retry storm is a likely repeat scenario.
- Was the index needed by anything already deployed, or can A1 wait for a planned window?
