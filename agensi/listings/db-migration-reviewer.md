# Listing: DB Migration Safety Reviewer

- **Title:** DB Migration Safety Reviewer: Zero-Downtime Schema Changes
- **Price:** Free
- **Category:** Code Quality (secondary: DevOps & Infrastructure, Data & Analytics)
- **Tags:** database-migrations, zero-downtime, postgresql, mysql, sql-server, schema-changes, online-ddl, rails, django, flyway
- **Works with:** Claude Code, Codex CLI, Cursor, Gemini CLI, Copilot, OpenClaw, any agent that reads SKILL.md
- **Upload:** `dist/agensi/db-migration-reviewer.zip` · **Logo:** `docs/assets/agensi/db-migration-reviewer-logo.png`

## Short description (one line)

Paste a migration before you merge it: get a SAFE / UNSAFE verdict per statement with the exact lock it takes, then a rewritten expand/contract version with online DDL, batched backfills, deploy order and rollback. PostgreSQL, MySQL, SQL Server, any ORM.

## Long description

**The migration that took 3 seconds in staging can lock your biggest table for an hour in production.** This skill reviews schema changes the way a careful DBA does, before they ship.

**For every statement it tells you**
- The **lock it takes** and what that blocks (reads, writes or both), for your engine and version.
- Whether it **rewrites or scans** the table, and roughly how long that takes at your size.
- Whether it breaks the **app version still running** during a rolling deploy (renames, drops, NOT NULL, type changes).
- The **lock queue trap**: a 5 ms ALTER waiting behind a long transaction that freezes every query.

**Then it rewrites it safely**
- Expand → backfill → contract steps, split into migrations and app releases.
- Online forms: `CREATE INDEX CONCURRENTLY`, `NOT VALID` + `VALIDATE`, `ALGORITHM=INSTANT/INPLACE`, `ONLINE = ON`, gh-ost / pt-osc.
- Batched, idempotent, resumable backfills that watch replica lag.
- Lock timeouts with retry, and the right no-transaction flag for Rails, Django, Alembic, EF Core, Flyway, Liquibase, Laravel, Knex.
- A **runbook**: order, duration estimate, what to monitor, when to stop, rollback per step.

**Migration stuck right now?** Rescue mode gives the read-only query that shows who is blocking whom and the safest thing to cancel, and leaves the decision to you.

Works in any language and answers in yours.

**Pairs with:** *SQL Query Clinic* (free) for the index, *Incident Postmortem* (free) if it already went wrong.

## Try it

> Is this migration safe to run on a 80M-row table? Postgres 15, Flyway. <paste migration>

> Review this Rails migration before I merge: <paste>

> How do I rename a column on a busy MySQL table with zero downtime?

> Our migration is hanging and the site is timing out. What do I do?
