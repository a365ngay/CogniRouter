# PostgreSQL migration safety

## The lock queue problem

Locks are granted in order. An `ALTER TABLE` waiting for `ACCESS EXCLUSIVE` behind one long transaction (a report, an idle-in-transaction session, a pg_dump) makes every later query on that table wait too, including plain `SELECT`s. A statement that would take 5 ms can take the site down. Always:

```sql
SET lock_timeout = '3s';        -- fail fast instead of queueing
SET statement_timeout = '15min'; -- cap long operations you did not expect to be long
```

and retry the migration a few times with a pause. In a transaction, every lock taken is held until `COMMIT`, so a quick `ALTER` followed by a slow `UPDATE` in the same transaction keeps the table blocked for the whole time.

## Lock levels (what blocks what)

| Lock | Blocks |
|---|---|
| `ACCESS EXCLUSIVE` | Everything, including `SELECT` |
| `EXCLUSIVE` | All writes and `SELECT ... FOR UPDATE`; plain reads continue |
| `SHARE ROW EXCLUSIVE` | Writes (INSERT/UPDATE/DELETE); reads continue |
| `SHARE` | Writes; reads continue |
| `SHARE UPDATE EXCLUSIVE` | Other DDL, VACUUM, ANALYZE; reads and writes continue |

## Statements

| Statement | Lock | Rewrite / scan | Safe form |
|---|---|---|---|
| `ADD COLUMN` nullable, no default | ACCESS EXCLUSIVE (brief) | No | Safe with `lock_timeout` |
| `ADD COLUMN ... DEFAULT <constant or stable expr like now()>` | ACCESS EXCLUSIVE (brief) | No on 11+ (default stored in catalog) | Safe on 11+; on 10 and older it rewrites: add nullable, set default, backfill |
| `ADD COLUMN ... DEFAULT <volatile expr>` (`gen_random_uuid()`, `clock_timestamp()`, `random()`) | ACCESS EXCLUSIVE | **Full rewrite** | Add nullable column, `SET DEFAULT` for new rows, backfill in batches |
| `ADD COLUMN ... NOT NULL` without default | — | Fails if table has rows | Add nullable → backfill → constraint (see patterns) |
| `ALTER COLUMN SET NOT NULL` | ACCESS EXCLUSIVE | Full scan while locked | 12+: `ADD CONSTRAINT c CHECK (col IS NOT NULL) NOT VALID` → `VALIDATE CONSTRAINT c` → `SET NOT NULL` (skips scan) → `DROP CONSTRAINT c` |
| `ALTER COLUMN TYPE` | ACCESS EXCLUSIVE | **Rewrite + rebuild of all indexes**, except binary-compatible changes (`varchar(n)` → larger `n` or `text`, `numeric(p,s)` → larger `p` with same `s`) | New column + backfill + switch (patterns). `int` → `bigint` always rewrites |
| `ALTER COLUMN SET DEFAULT` / `DROP DEFAULT` | ACCESS EXCLUSIVE (brief) | No | Safe with `lock_timeout` |
| `RENAME COLUMN` / `RENAME TABLE` | ACCESS EXCLUSIVE (brief) | No | Fast, but breaks running code: expand/contract |
| `DROP COLUMN` | ACCESS EXCLUSIVE (brief) | No (space reclaimed later) | Fast, but app must stop reading/writing it first (ORM column caches) |
| `CREATE INDEX` | SHARE (blocks writes for the whole build) | Full scan | `CREATE INDEX CONCURRENTLY` outside a transaction; on failure drop the INVALID index and retry |
| `DROP INDEX` | ACCESS EXCLUSIVE | No | `DROP INDEX CONCURRENTLY` |
| `REINDEX` | Blocks writes | Rebuild | `REINDEX INDEX CONCURRENTLY` (12+) |
| `ADD FOREIGN KEY` | SHARE ROW EXCLUSIVE on both tables | Scans the table | `ADD CONSTRAINT ... FOREIGN KEY ... NOT VALID` (enforced for new rows), then `VALIDATE CONSTRAINT` (SHARE UPDATE EXCLUSIVE; referenced table ROW SHARE) |
| `ADD CHECK` | ACCESS EXCLUSIVE | Scan | `NOT VALID` then `VALIDATE CONSTRAINT` |
| `ADD UNIQUE` / `ADD PRIMARY KEY` | ACCESS EXCLUSIVE | Index build while locked | `CREATE UNIQUE INDEX CONCURRENTLY` → `ADD CONSTRAINT ... UNIQUE USING INDEX` / `PRIMARY KEY USING INDEX` (PK columns must already be NOT NULL) |
| `ALTER TYPE ... ADD VALUE` (enum) | Brief | No | Safe; on 12+ may run in a transaction but the new value cannot be used until commit |
| `ATTACH PARTITION` | SHARE UPDATE EXCLUSIVE on parent (12+) | Scans partition unless a matching valid CHECK exists | Add matching CHECK `NOT VALID` → validate → attach |
| `VACUUM FULL`, `CLUSTER` | ACCESS EXCLUSIVE | Full rewrite | `pg_repack` |
| `TRUNCATE` | ACCESS EXCLUSIVE | — | Irreversible once committed; confirm it is intended |
| Large `UPDATE` / `DELETE` | Row locks until commit | Writes a new version of every row (bloat, WAL, replica lag) | Batches by key range, commit per batch (patterns) |

Triggers, views and functions that depend on a column can make renames and type changes fail; check `pg_depend` or try on a copy.

## Transactions and tools

PostgreSQL DDL is transactional (good for rollback) but `CREATE INDEX CONCURRENTLY`, `DROP INDEX CONCURRENTLY`, `REINDEX CONCURRENTLY` and `ALTER TYPE ... ADD VALUE` (before 12) cannot run inside a transaction block. Most tools wrap migrations in one; use their opt-out (see `patterns.md`).

## Who is blocking

```sql
SELECT pid, pg_blocking_pids(pid) AS blocked_by, state, wait_event_type,
       now() - xact_start AS xact_age, left(query, 120) AS query
FROM pg_stat_activity
WHERE datname = current_database() AND (cardinality(pg_blocking_pids(pid)) > 0 OR state = 'idle in transaction')
ORDER BY xact_age DESC NULLS LAST;
```

Cancel a statement (rolls back that statement's transaction): `SELECT pg_cancel_backend(<pid>);`. Terminate a session: `SELECT pg_terminate_backend(<pid>);`. Prefer cancelling the waiting migration over terminating application sessions.

Linters that catch many of these in CI: `squawk` (PostgreSQL), `strong_migrations` (Rails), `django-pg-zero-downtime-migrations` / `django-migration-linter` (Django).
