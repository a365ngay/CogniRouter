# Listing: SQL Query Clinic

- **Title:** SQL Query Clinic: Fix Slow or Wrong SQL from the Plan
- **Price:** Free
- **Category:** Data & Analytics (secondary: Code Quality, Testing & Debugging)
- **Tags:** sql, postgresql, mysql, sql-server, explain-analyze, query-optimization, indexing, performance, database, execution-plan
- **Works with:** Claude Code, Codex CLI, Cursor, Gemini CLI, Copilot, OpenClaw, any agent that reads SKILL.md
- **Upload:** `dist/agensi/sql-query-clinic.zip` · **Logo:** `docs/assets/agensi/sql-query-clinic-logo.png`

## Short description (one line)

Paste a slow query and its EXPLAIN plan; get the real cause quoted from the plan, a rewritten query, safe online index DDL, correctness traps you missed, and how to verify the fix. PostgreSQL, MySQL and SQL Server.

## Long description

**Stop guessing which index to add.** SQL Query Clinic reads your execution plan like a senior DBA: it finds where the time and rows actually go, proves it with the plan lines, and gives the smallest safe fix.

**What you get every time**
- **Verdict in one sentence**, then the **evidence**: the plan nodes that prove it (seq scans with huge "rows removed", 100× estimate errors, spills to disk, key lookups, deep OFFSET).
- **Ranked fixes**, cheapest first: query rewrite, then index, then statistics, then schema. Complete runnable SQL in your dialect.
- **Index advice with reasons**: column order (equality, range, sort, covering), partial and expression indexes, and the online way to create them without blocking writes (`CONCURRENTLY`, `ALGORITHM=INPLACE, LOCK=NONE`, `ONLINE = ON`).
- **Correctness check** even when you only asked about speed: NOT IN with NULLs, LEFT JOIN turned inner, join fan-out double-counting sums, time-zone day boundaries, unstable pagination.
- **How to verify**: the plan shape to expect and the numbers to compare, clearly marked as expected, not measured.

**No plan yet?** It gives you the exact command for your engine, with a warning that EXPLAIN ANALYZE runs the statement and how to roll it back.

**Safe by default:** never tells you to just run DDL on production; states lock impact and online alternatives. Works in any language and answers in yours.

**Pairs with:** *DB Migration Safety Reviewer* (free): ship the index it recommends without locking your table.

## Try it

> Why is this query slow? <paste query + EXPLAIN (ANALYZE, BUFFERS) output>

> Our admin orders page times out on page 100. Postgres 15, 12M orders. <paste query>

> This report returns duplicate customers and the totals look too high. <paste query>
