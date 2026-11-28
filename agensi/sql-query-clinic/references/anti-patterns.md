# Anti-patterns

## Performance

| Pattern | Why it hurts | Rewrite |
|---|---|---|
| Function on an indexed column: `WHERE date(created_at) = ...`, `lower(email) = ...`, `YEAR(d) = 2026` | Index on the raw column cannot be used | Range on the raw column: `created_at >= '2026-10-01' AND created_at < '2026-10-02'`; or an expression index on exactly that function |
| Implicit cast: varchar column vs numeric literal; nvarchar parameter vs varchar column (SQL Server); string vs integer column (MySQL) | Usually converts the column on every row and blocks a seek (SQL Server with a Windows collation can still do a range seek through the convert; with a `SQL_*` collation it scans) | Match the parameter type to the column type, usually in the app or ORM: ADO.NET `SqlDbType.VarChar` with size instead of `AddWithValue`, Dapper `DbString { IsAnsi = true }`, EF Core `IsUnicode(false)`, JDBC `sendStringParametersAsUnicode=false` |
| Leading wildcard `LIKE '%abc'` | B-tree cannot seek | Full-text or trigram index (PostgreSQL `pg_trgm`), or a reversed-column index for suffix search |
| `OR` across different columns | Often forces a scan | `UNION` of two indexed queries (use `UNION ALL` only with a guard such as `AND NOT (first condition)` written NULL-safe, or rows matching both branches are counted twice), or an index per column so the engine can combine them (PostgreSQL BitmapOr, SQL Server index union, MySQL index_merge) |
| Deep `OFFSET` pagination | Reads and discards every skipped row | Keyset: `WHERE (created_at, id) < (:last_created_at, :last_id) ORDER BY created_at DESC, id DESC LIMIT 50` |
| `SELECT *` | Prevents index-only/covering plans, moves more data | Select the columns used |
| Correlated subquery per row | Executes once per outer row | `JOIN` / `LEFT JOIN LATERAL` / window function |
| `COUNT(*)` for "is there any" | Counts everything | `EXISTS (SELECT 1 ...)` |
| `NOT IN (subquery)` | Slow and wrong with NULLs | `NOT EXISTS` |
| `DISTINCT` to remove join duplicates | Sorts or hashes everything; hides a join bug | Fix the join, or `EXISTS` for semi-joins |
| Huge `IN (...)` list from the app | Parse and plan cost, plan cache pollution | Temp table / array parameter (`= ANY(:ids)`) / table-valued parameter |
| Sorting on an expression or mixed directions without a matching index | Full sort | Index matching the `ORDER BY` columns and directions |
| Aggregating then filtering in the app | Moves all rows over the network | `WHERE` / `HAVING` in SQL |
| N+1 queries from an ORM | Many round-trips | Eager loading / one query with `IN` or a join |

## Correctness

| Trap | Symptom | Fix |
|---|---|---|
| `NOT IN` with a NULL in the subquery | Returns no rows at all | `NOT EXISTS` or filter NULLs |
| `a OR b AND c` without parentheses | `AND` binds first: means `a OR (b AND c)`, so `c` filters only one branch | Add parentheses; confirm the intended logic with the user |
| `LEFT JOIN b ... WHERE b.col = x` (or `<>`, `IN`, any comparison on `b`, even inside one `OR` branch) | Rows without a match get NULL, the comparison is UNKNOWN, the row is dropped: left join silently becomes inner | Move the condition into the `ON` clause (or allow `b.col IS NULL` explicitly) |
| Join fan-out before aggregation | `SUM` double-counts (order total × number of items) | Aggregate in a subquery/CTE first, then join |
| `GROUP BY` with non-aggregated columns (MySQL without `ONLY_FULL_GROUP_BY`) | Arbitrary values per group | Aggregate or add the column to `GROUP BY` |
| `BETWEEN` on timestamps | Misses or double-counts boundary instants | Half-open range `>= start AND < end` |
| Date functions with time zones | Day boundaries shift with the session time zone | Compute boundaries explicitly in the business time zone |
| `ORDER BY` without a unique tiebreaker + `LIMIT/OFFSET` | Rows repeat or vanish between pages | Add the primary key as the last `ORDER BY` column |
| Floating-point money | Rounding drift | `numeric/decimal` with explicit scale |
| `=` comparisons with NULL | Never true | `IS NULL` / `IS DISTINCT FROM` |
| Integer division (`a / b` with integers) | Truncated results | Cast one side to numeric/decimal |
| Case or collation differences | Missing matches, or duplicates in unique checks | Compare with an explicit collation or normalized column |
| Read-modify-write without locking | Lost updates under concurrency | Single `UPDATE ... SET x = x + 1`, `SELECT ... FOR UPDATE`, or optimistic version column |

When a rewrite fixes a performance problem but also changes results (for example a time-zone boundary), say so explicitly and let the user decide which behavior is correct.
