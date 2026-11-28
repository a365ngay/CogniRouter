# Indexing

## Composite index column order

1. Columns compared with **equality** (`status = 'paid'`, `tenant_id = :t`), most selective or most commonly filtered first.
2. Then **one range** column (`created_at >= ...`). Columns after the first range column cannot be used for seeking.
3. Then columns that satisfy **ORDER BY** in the same order and direction, so no sort is needed (only works if the preceding columns are equality-filtered).
4. Then **covering** columns the query only reads: PostgreSQL 11+ and SQL Server `INCLUDE (...)`; MySQL InnoDB has no INCLUDE, append them to the key or rely on the primary key being in every secondary index.

Example: `WHERE status = :s AND created_at >= :from ORDER BY created_at DESC LIMIT 50` → `(status, created_at DESC)` plus covering columns.

## Specialised indexes

- **Partial / filtered**: `CREATE INDEX ... WHERE status = 'paid'` (PostgreSQL), `WHERE status = 'paid'` filtered index (SQL Server). Small and fast when queries always use the same predicate. MySQL has none; use a generated column.
- **Expression / functional**: `(lower(email))` in PostgreSQL; MySQL 8.0.13+ functional key parts `((lower(email)))`; SQL Server: computed column + index. The query must use the identical expression.
- **Text search**: PostgreSQL GIN with `pg_trgm` for `LIKE '%x%'`, `tsvector` for words; MySQL `FULLTEXT`; SQL Server full-text index.
- **JSON**: PostgreSQL GIN on `jsonb` (`jsonb_path_ops` for containment), or an expression index on one extracted key.

## When an index will not help

- The query returns a large fraction of the table (roughly more than 5–20%, depends on row width and storage): a scan is cheaper.
- The predicate wraps the column in a function or cast the index does not match.
- Low-selectivity column alone (boolean, status with two values) — combine with a selective column or use a partial index.
- Statistics are stale: the planner may ignore a good index; refresh statistics first.

## Cost of an index

Every insert, update of indexed columns, and delete maintains it; it uses disk and memory; it can block HOT updates in PostgreSQL. Before adding, check for an existing index with the same leading columns that can be extended instead.

Extending an index = create the new one (online form), verify plans use it, then drop the old one (online form) after checking usage and hints. SQL Server can also use `CREATE INDEX ... WITH (DROP_EXISTING = ON)` to keep the name, but offline it holds a lock that blocks reads too.

Check usage before dropping (counters reset on restart; look at a period that includes month-end jobs and reports), and search the code for index hints that name it:

```sql
-- PostgreSQL: unused since last stats reset
SELECT indexrelname, idx_scan FROM pg_stat_user_indexes WHERE idx_scan = 0;
-- SQL Server: indexes with no reads (unused ones have no row in the DMV, hence the LEFT JOIN)
SELECT OBJECT_NAME(i.object_id) AS table_name, i.name, s.user_seeks, s.user_scans, s.user_lookups, s.user_updates
FROM sys.indexes i
LEFT JOIN sys.dm_db_index_usage_stats s
  ON s.object_id = i.object_id AND s.index_id = i.index_id AND s.database_id = DB_ID()
WHERE OBJECTPROPERTY(i.object_id, 'IsUserTable') = 1 AND i.index_id > 1
  AND COALESCE(s.user_seeks + s.user_scans + s.user_lookups, 0) = 0;
-- MySQL 8 (sys schema)
SELECT * FROM sys.schema_unused_indexes;
```

## Creating indexes without blocking writes

| Engine | Online form | Notes |
|---|---|---|
| PostgreSQL | `CREATE INDEX CONCURRENTLY idx ON t (...);` | Cannot run inside a transaction block (many migration tools wrap migrations in one: disable it for this step). If it fails it leaves an `INVALID` index: drop it and retry. Takes longer than a normal build. |
| MySQL 8 / InnoDB | `ALTER TABLE t ADD INDEX idx (...), ALGORITHM=INPLACE, LOCK=NONE;` | Still needs brief metadata locks at start and end; a long-running transaction on the table makes it wait and queue other queries. For very large tables consider gh-ost or pt-online-schema-change. |
| SQL Server | `CREATE INDEX idx ON t (...) WITH (ONLINE = ON);` | ONLINE (and `RESUMABLE = ON`, which needs ONLINE; 2019+ for create) is available on Enterprise, Developer and Azure SQL only. On Standard/Express a new nonclustered index is built offline: it holds a shared lock, so reads continue but inserts, updates and deletes wait for the whole build. Schedule a window, measure the build on a copy, and consider `SORT_IN_TEMPDB = ON`. |

Always set a lock timeout for DDL so it fails fast instead of queueing behind a long query and blocking everyone else: PostgreSQL `SET lock_timeout = '5s';`, MySQL `SET SESSION lock_wait_timeout = 5;`, SQL Server `SET LOCK_TIMEOUT 5000;`.
