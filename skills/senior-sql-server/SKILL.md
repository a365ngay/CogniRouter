---
name: senior-sql-server
description: Use when designing, reviewing, tuning, migrating, securing, or troubleshooting Microsoft SQL Server schemas, T-SQL, indexes, stored procedures, transactions, locking, execution plans, backups, or operations.
---

# Senior SQL Server

## Role

Make SQL Server changes correct, secure, reversible, and evidence-driven. Protect data integrity and production availability before pursuing micro-optimizations.

## Workflow

1. Inspect schema, constraints, data volume, query callers, existing indexes, execution plans, SQL Server version, isolation level, and deployment process before changing a query or table.
2. State the correctness invariant, expected cardinality, access pattern, concurrency behavior, performance target, and rollback method.
3. Prefer declarative constraints, normalized ownership, parameterized T-SQL, and set-based operations. Use stored procedures or functions only where they fit existing conventions and responsibilities.
4. Review actual execution plans and measured I/O, CPU, duration, waits, and row estimates before declaring a performance fix. Compare baseline and result on representative data.
5. Use explicit transactions with the smallest safe scope. Account for deadlocks, blocking, lock escalation, isolation anomalies, retry behavior, and idempotency.
6. Ship schema changes as forward and rollback scripts; make long-running migrations online, batched, or staged when production size requires it.

## Query and Schema Rules

- Avoid `SELECT *`, implicit conversions, non-SARGable predicates, cursor or RBAR patterns, unbounded result sets, dynamic SQL without parameterization, and accidental cross joins.
- Index for the measured predicate, join, sort, and include needs; balance read improvement against write cost and maintenance. Do not add duplicate or speculative indexes.
- Preserve primary keys, foreign keys, unique constraints, checks, defaults, null semantics, data types, collation, and precision intentionally.
- Use least-privilege database principals and never embed credentials or expose raw database errors to users.
- Treat backups, restore testing, retention, encryption, auditing, and monitoring as production requirements; do not alter them without explicit authorization.

## Verification

Test semantics, permissions, transactions, concurrent behavior, migration forward/rollback, and representative performance. For a performance change, report plan comparison and measured before/after evidence, plus remaining uncertainty caused by data or workload differences.
