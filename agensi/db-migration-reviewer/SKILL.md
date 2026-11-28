---
name: db-migration-reviewer
description: "Reviews database schema migrations for production safety before they ship: lock levels, full-table rewrites, blocked writes, lock queues behind long transactions, unbatched backfills, renames and drops that break the running app version, missing rollback. Rewrites risky migrations into safe expand/contract steps with online DDL, batched backfills and a deploy order. Covers PostgreSQL, MySQL/MariaDB and SQL Server, raw SQL or ORM migrations (Rails, Django, Alembic, Prisma, EF Core, Laravel, Flyway, Liquibase, Knex). Also helps when a migration is stuck or blocking production right now. Use whenever someone shares a migration file or PR, asks whether an ALTER TABLE, index, constraint, column rename, type change or backfill is safe on a big table, plans a zero-downtime schema change, or says a migration is hanging. Works in any language and answers in the user's language."
---

# DB Migration Safety Reviewer

Decide whether a migration can run on a live, busy database without blocking traffic, breaking the app, or losing data, and if not, rewrite it into steps that can.

## Pick the mode

| The user gives you | Mode |
|---|---|
| A migration file, ORM migration or PR diff | **Review**: verdict per statement, then a safe rewrite |
| A goal ("make email unique", "rename this column", "split this table") | **Plan**: safe step sequence with deploy order |
| "Our migration is stuck / the site is down during a migration" | **Rescue**: stop the damage first (see below), review afterwards |

## Workflow (Review and Plan)

1. **Pin the context.** Engine and exact version (lock behavior changes between versions), edition for SQL Server, table row counts and size, write rate, longest-running transactions or reports, the migration tool and whether it wraps each migration in a transaction, and the deploy style (rolling deploy means old and new app versions run against the same schema). Missing facts become stated assumptions plus a **Need from you** list.
2. **Translate ORM code to SQL** when needed, or ask for the generated SQL: Django `python manage.py sqlmigrate <app> <migration>`, Alembic `alembic upgrade <rev> --sql`, Prisma `prisma migrate diff ... --script`, EF Core `dotnet ef migrations script`, Rails (no dry-run): run it on a local or staging copy and copy the SQL from the migration log. Review the SQL, not the ORM call; note where the ORM sends no `ALGORITHM`/`LOCK` (MySQL) or wraps statements in a transaction (PostgreSQL).
3. **Classify every statement** with the engine reference: lock taken, what it blocks (reads, writes, or both), whether it rewrites or scans the table, expected duration at this size, and whether it fails or waits when a long transaction holds the table.
4. **Check app compatibility.** For each change, will the currently running app version still work after it, and will the new app version work before it? Renames, drops, NOT NULL without default, type changes and new constraints usually fail this check.
5. **Check data safety**: can it lose or corrupt data (narrowing a type, truncating strings, dropping a column still written), can it fail halfway (MySQL DDL is not transactional), is there a backup or restore point for irreversible steps.
6. **Rewrite** risky parts with `references/patterns.md`: expand → migrate data → contract, online DDL, batched idempotent backfills, constraints added unvalidated then validated, lock timeouts with retry.
7. **Give a deploy runbook**: ordered steps, which are migrations and which are app releases, how long each may take, what to monitor, the stop condition, and the rollback for each step.

## Output

```markdown
**Verdict:** SAFE | SAFE WITH CHANGES | UNSAFE — one sentence why.

**Context and assumptions** — engine/version, sizes, tool, deploy style (assumed values marked).

| # | Statement | Lock / blocks | Rewrite or scan | Risk | Fix |
|---|---|---|---|---|---|

**Safe version** — the rewritten migration(s), split by step, with comments and the tool's
no-transaction flag where needed.

**Runbook** — numbered: step, type (migration / app release / script), duration estimate,
monitor, stop if, rollback.

**Need from you** — only what would change the verdict.
```

Keep the user's tool and style: if they wrote a Rails migration, answer with Rails migrations (plus SQL comments showing what runs). Duration figures are estimates and must say what they assume.

## Rescue mode (migration blocking production now)

1. Give the read-only query that shows who blocks whom (`references/postgresql.md` / `references/mysql-sqlserver.md`, section "Who is blocking").
2. The usual fix is to **cancel the migration**, not the blocker: a waiting DDL in the lock queue blocks every query behind it. Show the cancel command and explain what it rolls back (PostgreSQL and SQL Server roll back the statement; MySQL may leave earlier statements of the migration applied).
3. Never tell the user to kill sessions, restart the database or edit system catalogs without saying what it will interrupt; the user runs the commands, and production actions need their explicit decision.
4. After traffic recovers: mark the migration state correctly in the tool's history table, then do a normal Review.

## Quality gates

- Every lock claim names the lock (for example PostgreSQL `ACCESS EXCLUSIVE`, MySQL metadata lock, SQL Server `Sch-M`) and is correct for the stated version; say when behavior differs by version or edition.
- Any DDL on a large or hot table sets a lock timeout and has a retry plan.
- Backfills run in batches outside the schema migration, commit per batch, are idempotent and resumable, and watch replica lag.
- Renames and drops never ship in the same release as the code that stops using the old name.
- `NOT VALID` / `WITH NOCHECK` / `ALGORITHM=INSTANT` and similar options are only suggested where that engine and version support them.
- Nothing is called "zero downtime" unless every step avoids blocking locks longer than the lock timeout.
- Never run or advise running migrations against production yourself; give commands for the user to run.

## References (read only what the task needs)

- `references/postgresql.md`: lock levels per statement, version notes, safe forms, who-is-blocking queries.
- `references/mysql-sqlserver.md`: InnoDB online DDL (INSTANT / INPLACE / COPY), metadata locks, gh-ost / pt-osc; SQL Server online operations and Sch-M locks.
- `references/patterns.md`: expand/contract recipes (add NOT NULL column, rename, change type, unique, foreign key, drop), batched backfills, migration-tool flags.
- `examples/invoices-tenant.md`: a full review of an unsafe PostgreSQL migration and its safe runbook.
