# Safe migration patterns

The rule behind all of them: **expand → migrate data → contract**. First add things the old code can ignore, then move data and code, and remove old things only after no running code uses them. Each arrow is usually a separate deploy.

## Add a NOT NULL column to a big table

1. Migration: add the column **nullable** (or with a constant default where that is metadata-only: PostgreSQL 11+, MySQL INSTANT, SQL Server Enterprise).
2. App release: write the column on every insert/update.
3. Script: backfill old rows in batches (below).
4. Migration: enforce NOT NULL without a long lock (PostgreSQL 12+: `CHECK (...) NOT VALID` → `VALIDATE` → `SET NOT NULL` → drop the check; MySQL: `MODIFY ... NOT NULL, ALGORITHM=INPLACE, LOCK=NONE`; SQL Server: off-peak or `ONLINE = ON`).

Avoid sentinel defaults (`0`, `''`, `'unknown'`) to satisfy NOT NULL: they hide missing data and break foreign keys.

## Rename a column (or table)

1. Add the new column; app writes **both** old and new (or a trigger copies old → new for writers you do not control).
2. Backfill new from old.
3. App reads the new column; still writes both.
4. App stops writing the old column. Tell the ORM to ignore it (Rails `self.ignored_columns`, Django: remove the field with `SeparateDatabaseAndState`, EF Core: remove from the model).
5. Later release: drop the old column.

Often the right advice is "don't rename": a cosmetic rename costs three or four releases. Offer an alias in the ORM instead.

## Change a column type (int → bigint, text → jsonb, etc.)

Same as rename: new column of the new type → dual write → batched backfill with conversion → build indexes and constraints on the new column (online) → switch reads → stop writing old → drop old. For primary keys also move sequences/identity, foreign keys pointing at it, and replicas/CDC consumers. If a trigger keeps the columns in sync during the rollout, it must copy in one direction only (old → new) until the app writes the new column directly.

## Add a unique constraint

1. Find duplicates first, on a replica if possible: `SELECT col, count(*) FROM t GROUP BY col HAVING count(*) > 1;`. The check must use the same comparison as the future index: case- and accent-insensitive collations (MySQL `*_ci`, SQL Server `CI_AS`) treat `A@x.com` and `a@x.com` as equal; PostgreSQL compares exactly unless you index `lower(col)`. MySQL and PostgreSQL allow many NULLs in a unique index; SQL Server allows only one unless you use a filtered index `WHERE col IS NOT NULL`. Decide how to resolve duplicates (a business decision, not a migration detail).
2. Make the app prevent new duplicates (or accept that step 3 may fail and retry after cleanup).
3. Build the index online (PostgreSQL `CREATE UNIQUE INDEX CONCURRENTLY`; MySQL `ADD UNIQUE INDEX ..., ALGORITHM=INPLACE, LOCK=NONE`; SQL Server `ONLINE = ON`), then attach it as a constraint if needed (PostgreSQL `ADD CONSTRAINT ... UNIQUE USING INDEX`).

## Add a foreign key

PostgreSQL: `ADD CONSTRAINT fk ... NOT VALID` (new rows checked), backfill/clean orphans, then `VALIDATE CONSTRAINT fk`. SQL Server: `WITH NOCHECK`, then `WITH CHECK CHECK CONSTRAINT` off-peak. MySQL: an online FK add requires `foreign_key_checks=0` and therefore skips validation; check orphans yourself first. Index the referencing column (deletes on the parent scan it otherwise).

## Drop a column or table

1. App release stops reading and writing it (and ORM ignores it).
2. Wait at least one full deploy cycle; check query logs or `pg_stat_statements` for remaining use.
3. Optionally keep data: rename table to `_deprecated_<date>` or export, if rollback might need it.
4. Drop. This is irreversible without a backup: say so.

## Batched backfill

```sql
-- PostgreSQL / MySQL style; run from a script, not inside the schema migration
UPDATE invoices
SET    tenant_id = a.tenant_id
FROM   accounts a                    -- MySQL: UPDATE invoices i JOIN accounts a ON ... SET ...
WHERE  a.id = invoices.account_id
  AND  invoices.id >= :start AND invoices.id < :start + :batch
  AND  invoices.tenant_id IS NULL;   -- idempotent: safe to rerun
```

- Walk the primary key in ranges (1k–10k rows), commit per batch, sleep between batches, log the last key so it can resume.
- Throttle on replica lag and on database CPU; stop if lag exceeds the agreed limit.
- Rows written by the old app version during the backfill: either the new app already writes the column, or run a final catch-up pass.
- PostgreSQL: large backfills create dead tuples; let autovacuum keep up (or `VACUUM (ANALYZE)` the table after).

## Migration tool switches

PostgreSQL (and SQL Server) tools wrap migrations in transactions; MySQL DDL cannot be transactional, so on MySQL the "outside a transaction" switch does nothing and what matters is explicit `ALGORITHM`/`LOCK` and one risky statement per migration.

| Tool | Run outside a transaction (PostgreSQL) | Online index |
|---|---|---|
| Rails | `disable_ddl_transaction!` | PostgreSQL `add_index ..., algorithm: :concurrently`; MySQL `add_index ..., algorithm: :inplace` (or `execute` with `ALGORITHM=INPLACE, LOCK=NONE`). Use `up`/`down` instead of `change` when a step cannot be reversed automatically (`change_column`, `execute`) |
| Django | `atomic = False` on the Migration class | `AddIndexConcurrently` (`django.contrib.postgres.operations`) |
| Alembic | `with op.get_context().autocommit_block():` | `op.create_index(..., postgresql_concurrently=True)` |
| EF Core | `migrationBuilder.Sql("...", suppressTransaction: true)` | raw SQL with `CONCURRENTLY` / `ONLINE = ON` |
| Flyway | script config `executeInTransaction=false` | raw SQL |
| Liquibase | `runInTransaction="false"` on the changeset | raw SQL or `<sql>` |
| Laravel | `public $withinTransaction = false;` on the migration | `DB::statement('CREATE INDEX CONCURRENTLY ...')` |
| Prisma | edit the generated SQL; check how your version handles non-transactional statements | edit the generated SQL |
| Knex | `exports.config = { transaction: false }` | `knex.raw(...)` |

Verify the switch against the user's tool version; if unsure, say so and show the raw SQL to run manually.

## Rollback

Each step needs its own rollback, written before the deploy: expand steps roll back by dropping what was added; backfills are re-runnable; contract steps (drops, type narrowing) are not reversible without a restore, so take a backup or a table copy first and get explicit sign-off. Some steps are better rolled forward than back (reverting a widened column to a narrower type is itself a risky rebuild); say so explicitly.

## Lock timeout with retry

```ruby
# Rails example (adapt the pattern to any tool): retry a short DDL a few times
def with_lock_retry(attempts: 5, wait: 10)
  tries = 0
  begin
    yield
  rescue ActiveRecord::LockWaitTimeout, ActiveRecord::StatementInvalid => e
    raise unless e.message =~ /lock wait timeout|Lock wait timeout|canceling statement due to lock timeout/i
    tries += 1
    raise if tries >= attempts
    sleep wait
    retry
  end
end
```

Set the timeout first (PostgreSQL `SET lock_timeout = '3s'`, MySQL `SET SESSION lock_wait_timeout = 5`, SQL Server `SET LOCK_TIMEOUT 5000`). In a PostgreSQL transaction a lock timeout aborts the whole transaction, so retry the whole migration, not the statement. Many tools have this built in (strong_migrations `lock_timeout_retries`, GitLab's `with_lock_retries`).
