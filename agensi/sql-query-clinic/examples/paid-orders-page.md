# Example: slow "Paid orders" admin page (PostgreSQL 15)

## Input (as the user sent it)

> The paid orders page in our admin times out on page 100+, and even page 1 takes ~8 s. Postgres 15. orders has about 12M rows (9 GB), order_items 40M. Indexes: orders_pkey, orders_customer_id_idx, order_items_order_id_idx, customers_pkey. Server time zone is UTC, our shop is in Vietnam. Plan below is for page 101.
>
> ```sql
> SELECT o.id, o.created_at, o.status, c.email,
>        SUM(oi.quantity * oi.unit_price) AS total
> FROM orders o
> JOIN customers c ON c.id = o.customer_id
> LEFT JOIN order_items oi ON oi.order_id = o.id
> WHERE o.status = 'paid'
>   AND date(o.created_at) >= '2026-10-01'
> GROUP BY o.id, c.email
> ORDER BY o.created_at DESC
> LIMIT 50 OFFSET 5000;
> ```
>
> ```text
> Limit  (actual time=8412.7..8412.9 rows=50 loops=1)
>   ->  Sort  (actual time=8409.1..8412.2 rows=5050 loops=1)
>         Sort Key: o.created_at DESC
>         Sort Method: top-N heapsort  Memory: 2211kB
>         ->  HashAggregate  (actual time=7650.4..8190.8 rows=612455 loops=1)
>               Group Key: o.id, c.email
>               Batches: 5  Memory Usage: 65585kB  Disk Usage: 98304kB
>               ->  Hash Right Join  (actual time=2604.3..6981.0 rows=2049310 loops=1)
>                     Hash Cond: (oi.order_id = o.id)
>                     ->  Seq Scan on order_items oi  (actual time=0.02..2380.5 rows=40112388 loops=1)
>                     ->  Hash  (actual time=2601.7..2601.8 rows=612455 loops=1)
>                           ->  Hash Join  (actual time=31.2..2440.9 rows=612455 loops=1)
>                                 Hash Cond: (o.customer_id = c.id)
>                                 ->  Seq Scan on orders o  (cost=0.00..389214.00 rows=3950 width=24) (actual time=0.03..2101.6 rows=612455 loops=1)
>                                       Filter: ((status = 'paid'::text) AND (date(created_at) >= '2026-10-01'::date))
>                                       Rows Removed by Filter: 11387545
> Execution Time: 8431.6 ms
> ```
> (plan trimmed by the user)

## Output

**Verdict:** the query sums the items of all 612,455 paid orders since 1 October and then throws away all but 50; filter and order through a partial index, page with keyset, and total only the 50 rows shown.

**Evidence**
- `Seq Scan on orders ... Rows Removed by Filter: 11387545`: reads all 12M orders to keep 612k. `date(created_at)` wraps the column, so no index on `created_at` could be used even if one existed.
- `rows=3950` estimated vs `rows=612455` actual (155× off): the planner cannot estimate a function of the column, so it planned for a small result.
- `Seq Scan on order_items ... rows=40112388` + `Hash Right Join rows=2049310`: every item of every matching order is joined and aggregated (`HashAggregate rows=612455`, spilled to disk: `Batches: 5 Disk Usage: 98304kB`).
- `Sort ... rows=5050` then `Limit rows=50`: the OFFSET makes PostgreSQL build and discard 5,000 rows; deeper pages get slower.

**Fixes** (in order)

1. **Rewrite: sargable time range, keyset pagination, total per displayed row.** Changes the page contract (see correctness notes).
   ```sql
   -- first page: drop the line marked (keyset)
   SELECT o.id, o.created_at, o.status, c.email,
          COALESCE(t.total, 0) AS total
   FROM orders o
   JOIN customers c ON c.id = o.customer_id
   LEFT JOIN LATERAL (
       SELECT SUM(oi.quantity * oi.unit_price) AS total
       FROM order_items oi
       WHERE oi.order_id = o.id
   ) t ON true
   WHERE o.status = 'paid'
     AND o.created_at >= (TIMESTAMP '2026-10-01 00:00' AT TIME ZONE 'Asia/Ho_Chi_Minh')
     AND (o.created_at, o.id) < (:last_created_at, :last_id)   -- (keyset)
   ORDER BY o.created_at DESC, o.id DESC
   LIMIT 50;
   ```
   The app passes `created_at` and `id` of the last row on the current page. The `LATERAL` sum runs 50 times through `order_items_order_id_idx` instead of over 40M rows.

2. **Partial index matching the filter and the order.**
   ```sql
   SET lock_timeout = '5s';
   CREATE INDEX CONCURRENTLY orders_paid_created_at_idx
       ON orders (created_at, id)
       WHERE status = 'paid';
   ```
   - Column order: `status` is fixed by the partial predicate, so the key starts with the range and sort column `created_at`, then `id` as the tiebreaker. PostgreSQL scans it backward for `DESC, DESC`.
   - Run it outside a transaction (most migration tools need a per-migration "no transaction" flag). If it fails, it leaves an INVALID index: drop it and rerun.
   - Cost: only paid orders are indexed (estimated 100–150 MB if about a third of orders are paid; check after the build with `pg_relation_size`). `status` becomes an indexed column, so updates that change `status` can no longer be HOT updates; watch write latency on `orders` after deploy.

3. **Only if still slow:** `ANALYZE orders;` after large imports. Not expected to be needed once the predicate is sargable.

**Correctness notes**
- `date(o.created_at)` on a `timestamptz` uses the session time zone (UTC on this server), so 1 October in Vietnam started at 07:00 local time: orders paid between 00:00 and 07:00 Vietnam time on 1 October were missing from the page. The rewrite uses the Vietnam day boundary; confirm this is the intended business rule.
- `ORDER BY o.created_at` with no tiebreaker plus OFFSET can repeat or skip orders across pages when two orders share a timestamp. The rewrite orders by `(created_at, id)`.
- Orders with no items showed `total = NULL`; the rewrite shows `0`. Keep `NULL` if the UI needs to tell them apart.
- Keyset pagination supports next/previous, not "jump to page 101". If the UI must jump, keep keyset for scrolling and offer a date filter for jumping.

**Verify**
```sql
EXPLAIN (ANALYZE, BUFFERS)
<rewritten query with real :last_created_at / :last_id values>;

SELECT indisvalid FROM pg_index
WHERE indexrelid = 'orders_paid_created_at_idx'::regclass;   -- expect true
```
Expected plan shape (not measured): `Limit` → `Nested Loop Left Join` → `Nested Loop` → `Index Scan Backward using orders_paid_created_at_idx` with `Index Cond` on `created_at` and the `(created_at, id)` row comparison, reading about 50 rows; `Index Scan using customers_pkey (loops=50)`; `Aggregate` over `Index Scan using order_items_order_id_idx (loops=50)`. No `Seq Scan`, no `HashAggregate`, no disk usage. Compare `Execution Time` and `Buffers: shared hit/read` with the 8,431.6 ms baseline, for page 1 and for a deep page; the deep page should now take about as long as page 1.

**Need from you**
- Confirm the business day is Vietnam time (`Asia/Ho_Chi_Minh`).
- Whether the UI needs "jump to page N" (affects the pagination choice).
