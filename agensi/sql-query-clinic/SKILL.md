---
name: sql-query-clinic
description: "Diagnoses slow or wrong SQL from the query, its execution plan, schema and table sizes, then gives ranked fixes with rewritten SQL, safe online index DDL, the expected plan change and how to verify it. Covers PostgreSQL, MySQL/MariaDB and SQL Server (SQLite and Oracle best effort). Catches correctness traps too: NULL logic, join fan-out, LEFT JOIN turned inner, implicit casts, time zones, unstable pagination. Use whenever someone shares a slow query, an EXPLAIN or EXPLAIN ANALYZE output, an execution plan, a timeout, high database CPU, a query returning duplicate or missing rows, or asks to review, optimize or index SQL, even if they only say why is this query slow. Works in any language and answers in the user's language."
---

# SQL Query Clinic

Find the one or two things that actually make the query slow or wrong, prove it from the plan, and give the smallest safe fix. No generic "add an index" advice without evidence.

## Pick the mode

| The user gives you | Mode |
|---|---|
| A slow query, timeout, high CPU or I/O, a plan | **Speed** |
| Duplicate, missing or wrong rows, totals that don't add up | **Correctness** (check this before Speed: a fast wrong query is worse) |
| A query or ORM output to check before merge | **Review**: both lenses, findings ranked |

## Workflow

1. **Pin the context.** Engine, version and edition (SQL Server Standard vs Enterprise changes which DDL is online), column types and collations of filtered columns, table sizes (rows and GB), existing indexes, the parameters used, how often the query runs, and the target (for example "p95 under 200 ms"). Missing items go into a short **Need from you** list with the exact command to get each one; continue with stated assumptions.
2. **Get the real plan.** If the user has none, give the exact command for their engine from `references/plan-reading.md`. Warn that `EXPLAIN ANALYZE` executes the statement: for INSERT, UPDATE or DELETE wrap it in a transaction and roll back, and never run it on a production primary without permission.
3. **Read the plan.** Find the node where most time or rows go, and the first node where estimated rows and actual rows differ by 10× or more. Name the cause using `references/plan-reading.md` and `references/anti-patterns.md`. If the user only described the plan in words, quote their description as evidence, call the diagnosis a hypothesis, and ask for the real plan.
4. **Check correctness** against the anti-pattern list, even in Speed mode (operator precedence, NULL logic, outer joins, fan-out). A rewrite that changes results must say so.
5. **Rank fixes** from cheapest and safest to most invasive: rewrite the query → add or change an index → refresh statistics → change schema or data model → change configuration or hardware. Stop at the first level that meets the target; with no target, give the fixes that remove the main bottleneck. When fixes only work together (a rewrite that needs a new index), present them as one fix with ordered steps.
6. **Make each fix safe to ship.** Online index creation for the engine (`references/indexing.md`), its write and storage cost, and what to watch after deploy.
7. **Say how to verify**: the plan you expect after the fix (which node changes and why) and the before/after numbers to compare. Never present an expected plan or timing as measured.

## Output

```markdown
**Verdict:** one sentence: the main cause and the fix.

**Evidence** — the plan lines that prove it (quoted, trimmed), and what they mean.

**Fixes** (in order)
1. <name> — what changes, why it helps, cost/risk.
   ```sql
   -- rewritten query or DDL
   ```
2. ...

**Correctness notes** — any behavior the rewrite changes, or bugs found in the original.

**Verify** — commands to run, the plan shape to expect, the numbers to compare.

**Need from you** — only if something blocked a firmer answer.
```

Keep the user's table and column names. Rewritten SQL must be complete and runnable, in the user's dialect, with parameters left as parameters; when the dialect needs declarations (T-SQL `DECLARE`), declare each with the column's exact type and say where the app or ORM sets that type. Translate the headings into the user's language; keep SQL, plan text and identifiers as they are.

## Quality gates

- Every claim about the cause points to a plan line, a table size, or a definition. If there is no plan, say the diagnosis is a hypothesis.
- Index advice gives the full column order and explains it (equality columns, then range, then sort; covering columns last or in INCLUDE).
- Never suggest dropping an index without checking it is unused (engine-specific usage view) and not backing a constraint.
- Never suggest disabling planner features, hints or forcing plans as the first fix; only as a documented last resort.
- Call out when the bottleneck is not SQL (N+1 calls from the application, network round-trips, lock waits, an undersized connection pool).
- Do not recommend production changes (DDL, configuration, statistics jobs) as "just run this": state the lock impact and suggest a maintenance window or online variant.

## References (read only what the task needs)

- `references/plan-reading.md`: getting the plan per engine, key node and operator names, red flags.
- `references/anti-patterns.md`: performance and correctness traps with rewrites.
- `references/indexing.md`: composite order, covering, partial and expression indexes, when an index will not help, online creation per engine.
- `examples/paid-orders-page.md`: complete worked example on PostgreSQL.
