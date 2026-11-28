# MySQL / MariaDB and SQL Server migration safety

## MySQL 8.0 (InnoDB)

### Algorithms

Always state the algorithm and lock you expect, so MySQL refuses instead of silently copying the table:

```sql
ALTER TABLE orders ADD COLUMN note varchar(255) NULL, ALGORITHM=INSTANT;
ALTER TABLE orders ADD INDEX idx_orders_status_created (status, created_at), ALGORITHM=INPLACE, LOCK=NONE;
```

| Algorithm | Meaning |
|---|---|
| `INSTANT` | Metadata only, no rebuild |
| `INPLACE` + `LOCK=NONE` | Rebuild or build inside InnoDB while reads and writes continue (except brief metadata locks at start and end) |
| `COPY` | Copies the whole table; writes are blocked for the duration |

ORMs (Rails `change_column`, Django `AlterField`, etc.) send no `ALGORITHM`, so MySQL silently picks the cheapest it can, which may be COPY (for example when the generated column definition changes the collation). Run risky changes as raw SQL with explicit `ALGORITHM` and `LOCK` (Rails: `execute`).

Version notes: avoid 8.0.29 (withdrawn because of INSTANT DDL bugs); RDS and Aurora versions differ, check the engine version string.

| Change | 8.0 behavior |
|---|---|
| Add column | INSTANT (8.0.12+ only as last column; any position on 8.0.29+). From 8.0.29 a table allows 64 INSTANT row versions; after that a rebuild is needed |
| Drop column | INSTANT on 8.0.29+; otherwise INPLACE with rebuild |
| Rename column (same type) | INSTANT on 8.0.28+, otherwise INPLACE; either way breaks running code: expand/contract |
| Set / drop column default | INSTANT |
| Add / drop secondary index | INPLACE, LOCK=NONE (build reads the whole table) |
| Add `FULLTEXT` / `SPATIAL` index | INPLACE but LOCK=SHARED (blocks writes) |
| Extend `VARCHAR` within the same length-prefix range (≤255 bytes or >255 bytes) | INPLACE, no rebuild; crossing 255 bytes → COPY. Byte length depends on the charset (`utf8mb4` = 4 bytes per char) |
| Change column data type (for example `INT` → `BIGINT`) | COPY: writes blocked for the whole copy. If a foreign key references the column (or the column references another), the change fails with error 3780 (incompatible FK columns) unless parent and children change together |
| Make column `NULL` / `NOT NULL` | INPLACE with rebuild (concurrent DML allowed; `NOT NULL` needs strict SQL mode and fails if NULLs exist) |
| Add primary key | INPLACE with rebuild (expensive) |
| Add foreign key | INPLACE only with `foreign_key_checks=0` (no validation of existing rows); otherwise COPY |
| `ENUM` add value at the end | INSTANT; reordering or inserting in the middle → COPY |
| Change charset / collation of a column | COPY |
| `OPTIMIZE TABLE` | INPLACE rebuild |

### Metadata locks and the queue

Every `ALTER` needs an exclusive metadata lock (MDL) briefly at start and end. If any transaction has touched the table and not committed, the ALTER waits, and every new query on the table queues behind it. `lock_wait_timeout` defaults to 31536000 seconds (one year), so set `SET SESSION lock_wait_timeout = 5;` for migrations and retry (error 1205 means it timed out; find the long transaction, then rerun). The setting stays on that connection, which an ORM may reuse for later migrations.

### Online rebuild failure modes

- `INPLACE` rebuilds log concurrent writes in a buffer capped by `innodb_online_alter_log_max_size` (default 128 MB). Under heavy writes it overflows and the ALTER fails at the end, after hours of work. Raise it for the session/instance or run off-peak.
- An online `ADD UNIQUE INDEX` fails at the end if a duplicate is inserted during the build: stop duplicates in the app first.
- Rebuilds (INPLACE with rebuild, COPY) need free disk of about the table size plus indexes; check before starting (RDS: `FreeStorageSpace`).

### Not transactional

DDL commits implicitly. A migration file with five statements that fails on the third leaves the first two applied (8.0 atomic DDL is per statement only). Keep one risky statement per migration, and make migrations re-runnable (`IF NOT EXISTS` where supported, or check `information_schema`).

### Big tables and replicas

Online DDL replays on replicas after it finishes on the primary, so replicas lag by the duration of the ALTER. For large or hot tables use `gh-ost` (triggerless, binlog-based, pausable) or `pt-online-schema-change` (trigger-based), which copy in chunks and throttle on replica lag. Both need extra disk about the size of the table.

- **gh-ost does not support tables with foreign keys** (as parent or child). Use pt-osc with `--alter-foreign-keys-method` (read its caveats), or a planned window.
- On RDS/Aurora: gh-ost needs row-based binlogs and usually `--allow-on-master --assume-rbr`; keep binlog retention long enough (`mysql.rds_set_configuration('binlog retention hours', ...)`); pt-osc triggers may need `log_bin_trust_function_creators=1` in the parameter group. RDS Blue/Green deployments are another option for very large changes.
- Changing a key type referenced by foreign keys (for example `users.id` to `BIGINT` with child tables) means changing the parent and every child column in one coordinated operation; treat it as its own project.

### Who is blocking

```sql
SELECT * FROM sys.schema_table_lock_waits;           -- metadata lock waits
SELECT * FROM performance_schema.data_lock_waits;    -- row lock waits
SHOW FULL PROCESSLIST;                                -- "Waiting for table metadata lock"
SELECT trx_mysql_thread_id, trx_started, trx_query FROM information_schema.innodb_trx ORDER BY trx_started;
```

`KILL QUERY <id>;` stops the statement, `KILL <id>;` the connection (on RDS, for other users' sessions: `CALL mysql.rds_kill_query(<id>);` / `CALL mysql.rds_kill(<id>);`). Killing a running COPY/INPLACE ALTER rolls it back, which can itself take a while.

**MariaDB:** INSTANT add column since 10.3, INSTANT drop/reorder since 10.4; syntax similar but verify per version.

## SQL Server

### Locks

Schema changes take a **schema modification lock (`Sch-M`)**, which blocks everything, including reads under most isolation levels. Like PostgreSQL, a waiting `Sch-M` request blocks new requests behind it. Use `SET LOCK_TIMEOUT 5000;` and, for online index operations and partition switches, `WAIT_AT_LOW_PRIORITY (MAX_DURATION = 1 MINUTES, ABORT_AFTER_WAIT = SELF)`.

DDL is transactional; all locks are held until commit.

| Change | Behavior |
|---|---|
| Add nullable column | Metadata only |
| Add `NOT NULL` column with a constant default | Metadata only on Enterprise edition and Azure SQL (2012+); size-of-data update on other editions |
| Increase `varchar`/`nvarchar` length | Usually metadata only (check indexes that include the column) |
| Change type (for example `int` → `bigint`), `NULL` → `NOT NULL` | Size-of-data, `Sch-M` for the duration. `ALTER COLUMN ... WITH (ONLINE = ON)` (2016+, Enterprise) keeps the table available |
| Create / rebuild index | Offline by default (blocks writes, or everything for clustered). `WITH (ONLINE = ON)` on Enterprise/Azure; add `RESUMABLE = ON` (create: 2019+; rebuild: 2017+) |
| Add foreign key / check constraint | Validates existing rows with a scan. `WITH NOCHECK` adds it untrusted (not used by the optimizer, `is_not_trusted = 1`); validate later with `ALTER TABLE t WITH CHECK CHECK CONSTRAINT c` off-peak |
| Rename column (`sp_rename`) | Metadata only; breaks running code and does not update references in procedures or views |
| Drop column | Metadata only (space reclaimed on rebuild) |

Check the edition first: `SELECT SERVERPROPERTY('Edition'), SERVERPROPERTY('ProductVersion');`.

### Who is blocking

```sql
SELECT r.session_id, r.blocking_session_id, r.wait_type, r.wait_time, r.command,
       SUBSTRING(t.text, 1, 200) AS sql_text
FROM sys.dm_exec_requests r
CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) t
WHERE r.blocking_session_id <> 0 OR r.session_id IN (SELECT blocking_session_id FROM sys.dm_exec_requests);
```

`KILL <session_id>;` rolls back that session's transaction; a long transaction can take as long to roll back as it ran (`KILL <id> WITH STATUSONLY` shows progress).
