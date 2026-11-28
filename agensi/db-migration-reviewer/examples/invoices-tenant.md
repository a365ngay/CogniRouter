# Example: adding tenant_id to a hot invoices table (PostgreSQL 15, Flyway)

## Input (as the user sent it)

> Can you check this before I merge? Postgres 15, Flyway (default settings, so each migration runs in one transaction). invoices has ~80M rows, ~60 GB, around 400 writes/s at peak. We do rolling deploys on Kubernetes.
>
> ```sql
> -- V42__invoices_tenant.sql
> ALTER TABLE invoices ADD COLUMN tenant_id bigint NOT NULL DEFAULT 0;
> UPDATE invoices i SET tenant_id = a.tenant_id FROM accounts a WHERE a.id = i.account_id;
> ALTER TABLE invoices ADD CONSTRAINT invoices_tenant_fk FOREIGN KEY (tenant_id) REFERENCES tenants(id);
> CREATE INDEX invoices_tenant_created_idx ON invoices (tenant_id, created_at);
> ALTER TABLE invoices RENAME COLUMN amount TO amount_cents;
> ALTER TABLE invoices ALTER COLUMN amount_cents TYPE bigint;
> ```

## Output

**Verdict:** UNSAFE: in one transaction, the first statement's `ACCESS EXCLUSIVE` lock is held until the end, so `invoices` is unreadable and unwritable for the whole 80M-row update, the FK scan, the index build and a 60 GB table rewrite (likely over an hour), and the rename breaks the old pods during the rolling deploy.

**Context and assumptions**
- PostgreSQL 15, Flyway wrapping V42 in a single transaction, rolling deploy (old and new pods run together).
- 80M rows / 60 GB / ~400 writes/s (given). `tenants` is small. `amount` is `integer` holding cents (assumed). `id` is a `bigint` primary key (assumed).
- Duration figures below are rough estimates for this size on typical SSD storage, not measurements.

| # | Statement | Lock / blocks | Rewrite or scan | Risk | Fix |
|---|---|---|---|---|---|
| 1 | `ADD COLUMN tenant_id bigint NOT NULL DEFAULT 0` | ACCESS EXCLUSIVE, blocks everything; **held until commit** | None on 15 (constant default) | High (because of the transaction); also no tenant `0` exists, so #3 fails after everything else has run | Add nullable, no sentinel default |
| 2 | `UPDATE invoices ... FROM accounts` (80M rows) | Row locks on every row until commit (plus #1's lock) | Writes a new version of every row: about 60 GB of new tuples, WAL spike, replica lag | High | Batched, idempotent backfill script outside the migration |
| 3 | `ADD CONSTRAINT ... FOREIGN KEY` | SHARE ROW EXCLUSIVE on `invoices` and `tenants` | Full scan of 80M rows | High; fails on the `0` rows from #1 | `NOT VALID` now, `VALIDATE CONSTRAINT` after backfill |
| 4 | `CREATE INDEX` | SHARE, blocks writes for the whole build (minutes to tens of minutes) | Full scan + sort | High | `CREATE INDEX CONCURRENTLY` in its own non-transactional migration |
| 5 | `RENAME COLUMN amount TO amount_cents` | ACCESS EXCLUSIVE (brief) | None | High: old pods still query `amount` and fail until the rollout completes; rollback of the app breaks too | Do not rename in this change (see below) |
| 6 | `ALTER COLUMN amount_cents TYPE bigint` | ACCESS EXCLUSIVE | **Full rewrite of 60 GB + rebuild of every index**; needs about as much free disk | Critical | Separate expand/contract project, only if `integer` is really too small |

**Is the type change needed?** `integer` holds up to 2,147,483,647 cents (about $21.4M per invoice). If no invoice gets close, drop #5 and #6 from this change; a cosmetic rename costs four releases. If it is needed, follow "Change a column type" in `references/patterns.md` as its own project.

**Safe version** (split into migrations and a script)

```sql
-- V42__invoices_tenant_expand.sql   (transactional is fine: only brief locks)
SET lock_timeout = '3s';
ALTER TABLE invoices ADD COLUMN tenant_id bigint;                      -- nullable, metadata only
ALTER TABLE invoices
  ADD CONSTRAINT invoices_tenant_fk FOREIGN KEY (tenant_id)
  REFERENCES tenants(id) NOT VALID;                                    -- enforced for new rows only
```

```sql
-- backfill_invoices_tenant.sql  (run by a job, batch by batch, NOT a Flyway migration)
UPDATE invoices i
SET    tenant_id = a.tenant_id
FROM   accounts a
WHERE  a.id = i.account_id
  AND  i.id >= :start AND i.id < :start + 5000
  AND  i.tenant_id IS NULL;
-- commit, sleep ~100 ms, advance :start; stop if replica lag > 30 s
```

```sql
-- V43__invoices_tenant_index.sql
-- Flyway script config V43__invoices_tenant_index.sql.conf:  executeInTransaction=false
SET lock_timeout = '3s';
CREATE INDEX CONCURRENTLY IF NOT EXISTS invoices_tenant_created_idx
    ON invoices (tenant_id, created_at);
```

```sql
-- V44__invoices_tenant_enforce.sql  (after backfill reports 0 rows left)
SET lock_timeout = '3s';
ALTER TABLE invoices VALIDATE CONSTRAINT invoices_tenant_fk;            -- SHARE UPDATE EXCLUSIVE: reads/writes continue
ALTER TABLE invoices ADD CONSTRAINT invoices_tenant_nn CHECK (tenant_id IS NOT NULL) NOT VALID;
ALTER TABLE invoices VALIDATE CONSTRAINT invoices_tenant_nn;            -- scan without blocking writes
ALTER TABLE invoices ALTER COLUMN tenant_id SET NOT NULL;               -- 12+: uses the valid check, no scan
ALTER TABLE invoices DROP CONSTRAINT invoices_tenant_nn;
```

Note: in V44 the two `VALIDATE` scans run inside Flyway's transaction, so their `SHARE UPDATE EXCLUSIVE` locks and the brief `ACCESS EXCLUSIVE` from `SET NOT NULL` are held until commit; `SET NOT NULL` is last so the strong lock is held only for milliseconds. If you prefer, split each statement into its own migration.

**Runbook**

| Step | Type | Duration (est.) | Monitor | Stop if | Rollback |
|---|---|---|---|---|---|
| 1. V42 expand | Migration | Seconds | Lock waits on `invoices` | `lock_timeout` hit 3 times → find the long transaction first | `ALTER TABLE invoices DROP COLUMN tenant_id;` |
| 2. App release: set `tenant_id` on every insert/update | App release | Normal rollout | Error rate; FK violations | FK errors → app bug, roll back the app | Roll back app; column stays nullable, harmless |
| 3. Backfill job | Script | Hours at 5k rows/batch (about 16,000 batches) | Replica lag, CPU, dead tuples | Lag > 30 s, CPU > 80 % | Stop the job; rerun later (idempotent) |
| 4. Check: `SELECT count(*) FROM invoices WHERE tenant_id IS NULL;` = 0 | Check | Minutes (scan, read-only) | — | > 0 → rerun backfill | — |
| 5. V43 index | Migration (no transaction) | Tens of minutes | Disk, I/O, replica lag | Fails → `DROP INDEX CONCURRENTLY invoices_tenant_created_idx;` and retry | Same drop |
| 6. V44 enforce | Migration | Two full scans (minutes each); writes continue | Lock waits | `lock_timeout` → retry off-peak | `ALTER TABLE invoices ALTER COLUMN tenant_id DROP NOT NULL;` / `DROP CONSTRAINT invoices_tenant_fk;` |
| 7. App release: queries use `tenant_id` | App release | Normal | Query latency | — | Roll back app |

Also add `SET statement_timeout` for the migration role so an unexpected long statement fails instead of blocking for an hour, and add a CI linter (`squawk`) so these patterns are caught before review.

**Need from you**
- Confirm `amount` max values: is the `bigint` change actually needed?
- Whether every `accounts` row has a non-null `tenant_id` (otherwise the backfill leaves NULLs and V44 fails).
