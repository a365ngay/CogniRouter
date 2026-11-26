---
name: senior-postgresql
description: Use when designing, reviewing, tuning, migrating, securing, or troubleshooting PostgreSQL schemas, SQL, indexes, EXPLAIN plans, transactions, locks, JSONB, replication, backups, or database operations.
---

# Senior PostgreSQL

## Role

Deliver PostgreSQL changes that maintain data integrity, work under real concurrency, and are measured against representative workload rather than intuition.

## Workflow

1. Inspect schema, constraints, migrations, data scale, query callers, PostgreSQL version, extensions, autovacuum health, statistics, locks, and deployment process.
2. Define the invariant, query shape, expected cardinality, isolation behavior, performance target, operational risk, and reversible path.
3. Use parameterized SQL, correct types, declarative constraints, set-based operations, and clear ownership. Keep JSONB flexible only where schema variability is real and query/index behavior remains intentional.
4. Use `EXPLAIN (ANALYZE, BUFFERS)` on safe representative workloads to establish a baseline and validate a change. Account for stale statistics, cache effects, selectivity, and write amplification.
5. Design indexes deliberately: B-tree by default, partial or expression indexes only for proven predicates, GIN/GiST when data operators require them. Consider concurrent index creation and index maintenance cost.
6. Make migration locks, table rewrites, backfills, transaction duration, replicas, and rollback explicit. Stage large operations to protect availability.

## Query and Concurrency Rules

- Avoid `SELECT *`, implicit casts, non-indexable predicates, N+1 access, accidental Cartesian joins, unbounded reads, unsafe dynamic SQL, and `OFFSET` pagination on deep large datasets without a reasoned trade-off.
- Respect MVCC: long transactions can block vacuum and cause bloat; lock only what is necessary; design retries for serialization or deadlock failures where needed.
- Use the least privilege roles, row-level security only with a reviewed policy model, and no credentials or sensitive data in logs or client-visible errors.
- Do not change backup, restore, replication, retention, or production data without explicit authorization.

## Verification

Verify functional semantics, constraints, permissions, concurrent writers/readers, migration forward/rollback, and performance evidence. State PostgreSQL version, workload assumptions, and any production-only uncertainty.
