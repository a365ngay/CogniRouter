# Reading Execution Plans

## Getting the plan

| Engine | Estimated plan | Actual plan (runs the query) |
|---|---|---|
| PostgreSQL | `EXPLAIN (FORMAT TEXT) <query>;` | `EXPLAIN (ANALYZE, BUFFERS, SETTINGS) <query>;` |
| MySQL 8.0.18+ | `EXPLAIN FORMAT=TREE <query>;` | `EXPLAIN ANALYZE <query>;` |
| MariaDB | `EXPLAIN <query>;` | `ANALYZE FORMAT=JSON <query>;` |
| SQL Server | `SET SHOWPLAN_XML ON;` or "Display Estimated Execution Plan" | `SET STATISTICS IO, TIME ON;` + "Include Actual Execution Plan" (or `SET STATISTICS XML ON;`) |
| SQLite | `EXPLAIN QUERY PLAN <query>;` | — |
| Oracle | `EXPLAIN PLAN FOR <query>; SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);` | `/*+ GATHER_PLAN_STATISTICS */` then `DBMS_XPLAN.DISPLAY_CURSOR(FORMAT=>'ALLSTATS LAST')` |

For data-changing statements, run actual plans inside a transaction and roll back:
```sql
BEGIN; EXPLAIN (ANALYZE, BUFFERS) UPDATE ...; ROLLBACK;        -- PostgreSQL
BEGIN TRAN; SET STATISTICS XML ON; UPDATE ...; ROLLBACK;        -- SQL Server
```

Use the same parameter values as the slow case. A plan for an easy value can look nothing like the slow one (parameter sniffing in SQL Server, generic vs custom plans in PostgreSQL prepared statements).

Table sizes:
```sql
-- PostgreSQL
SELECT relname, n_live_tup, pg_size_pretty(pg_total_relation_size(relid)) FROM pg_stat_user_tables ORDER BY pg_total_relation_size(relid) DESC;
-- MySQL
SELECT table_name, table_rows, ROUND((data_length+index_length)/1024/1024) AS mb FROM information_schema.tables WHERE table_schema = DATABASE();
-- SQL Server
EXEC sp_spaceused N'dbo.orders';
```

## How to read

1. Read from the innermost (most indented) nodes outward; each parent consumes its children's rows.
2. Find the node with the largest **actual time** (PostgreSQL: `actual time=start..end` × `loops`; SQL Server 2016 SP1+: per-operator actual elapsed and CPU time and actual rows in the actual plan; operator "cost %" is an estimate even in an actual plan; MySQL tree: `actual time` and `rows`).
3. Compare **estimated rows vs actual rows** at each node. A 10× gap or more means the planner chose with bad information: stale or missing statistics, correlated columns, functions on columns, parameter sniffing, or table variables (SQL Server).
4. Look at **rows removed by filter** (PostgreSQL `Rows Removed by Filter`, SQL Server residual predicate): many rows read to keep few means the predicate is not being used for access.
5. Check **buffers / logical reads**: high shared read (PostgreSQL) or logical reads (SQL Server) shows I/O volume even when timing is cached.
6. Check **loops**: a cheap inner node executed 100,000 times is the real cost.

## Red flags by engine

**PostgreSQL**
- `Seq Scan` on a large table with a selective `Filter` → missing or unusable index.
- `Sort Method: external merge Disk:` → sort spilled; reduce rows earlier, add an index for the order, or raise `work_mem` for that query only.
- `Hash ... Batches: N` with N > 1 → hash spilled to disk.
- `Nested Loop` with large outer rows and an inner `Seq Scan` → missing index on the join key.
- `Bitmap Heap Scan` with large `Recheck` / `lossy` → bitmap overflowed `work_mem`.
- `Index Scan` followed by many `Heap Fetches` on an Index Only Scan → visibility map stale; vacuum.
- Estimates way off after bulk loads → `ANALYZE <table>`; correlated columns → `CREATE STATISTICS`.

**MySQL / MariaDB**
- `type: ALL` (full scan) or `Table scan on` in tree output on a large table.
- `Using filesort`, `Using temporary` on large row counts.
- `key: NULL` with `possible_keys` listed → index not chosen; check types and functions on columns.
- `rows` × `filtered` much larger than the result.

**SQL Server**
- `Clustered Index Scan` / `Table Scan` with a selective predicate.
- `Key Lookup` (or RID Lookup) executed thousands of times → covering index with `INCLUDE`.
- Warnings: implicit conversion that affects the plan (`CONVERT_IMPLICIT` on the column in a scan or residual predicate, "may affect CardinalityEstimate / SeekPlan"), spill to tempdb, missing index hint (treat as a hint, not a prescription).
- Estimated rows 1 vs actual rows huge → table variable, multi-statement TVF, or parameter sniffing.

## Not a SQL problem

If the query itself is fast in the plan but slow in the application: N+1 calls, network round-trips, fetching more columns or rows than displayed, ORM hydration cost, lock waits (check `pg_stat_activity` / `sys.dm_exec_requests` / `performance_schema.data_lock_waits`), or connection pool exhaustion.
