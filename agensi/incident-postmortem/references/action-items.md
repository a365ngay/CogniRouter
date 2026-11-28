# Action items

## Good vs weak

| Weak | Strong |
|---|---|
| Be more careful with migrations | Migration runner sets `lock_timeout=5s` and `statement_timeout=10min` for every migration session |
| Improve monitoring | Alert when more than 20 sessions wait on locks for over 60 s on the orders DB, paging the orders on-call |
| Add more tests | CI step runs `squawk` on new migration files and fails on non-concurrent index builds and table rewrites |
| Document the process | Runbook "Migration blocking production" with the blocking query, safe cancel command and decision rule, linked from the alert |
| Investigate X | Spike (time-boxed, 2 days): measure index build times on a production-size snapshot; decide whether staging needs a large dataset |

A strong action: one owner, a clear done condition someone else can verify, and small enough to finish in weeks, not quarters. Split large ones; track them in the team's issue tracker.

## Types

- **Prevent**: stop this class of failure (guardrails, safer defaults, design change).
- **Detect**: notice sooner (alerts, SLO burn alerts, synthetic checks).
- **Mitigate**: shorten or shrink impact (runbooks, feature flags, automatic rollback, rate limits, graceful degradation).
- **Process**: communication, ownership, review, training, support macros.

A good set has at least one prevent and one detect or mitigate action. If every action is "process", the system has not changed.

## Priority

- **P1**: the same trigger could cause this again soon, or the impact was severe; due within 1–2 weeks.
- **P2**: meaningfully reduces risk or time to mitigate; due within the next cycle or month.
- **P3**: nice to have; may be accepted as backlog.

Explicitly list **accepted risks**: factors you decided not to address, and why.

## Owners and dates

- Owner = a person or team that agreed in the review. If not known, write `TBD in review`, or propose the team that owns the affected system and label it "proposed"; never present a person as the owner unless the user said so.
- Due dates: use the user's dates; otherwise propose ones counted from today (or the review date, if given), never dates already in the past, and label them proposed.
- Actions owned outside engineering (marketing, support, vendors) are fine; prefer ones backed by a tool or a gate (a required field, a scheduling check) over a request to "remember to tell us".
- Limit to roughly 3–8 actions. Merge duplicates; move ideas without an owner into "Open questions" or "Accepted risks".
