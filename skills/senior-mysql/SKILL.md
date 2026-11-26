---
name: senior-mysql
description: Use when designing, reviewing, tuning, migrating, securing, or troubleshooting MySQL or MariaDB schemas, SQL, indexes, EXPLAIN plans, InnoDB transactions and locking, character sets, online schema changes, replication, backups, or database operations.
---

# Senior MySQL

## Role

Design and change MySQL databases with correct types and collations, index-backed queries, safe online migrations, and controlled locking.

## Before Editing

1. Inspect server version (MySQL vs MariaDB), storage engine, `sql_mode`, default charset/collation, isolation level, replication topology, migration tool, ORM, and existing index conventions.
2. For a slow or changed query, get its `EXPLAIN` / `EXPLAIN ANALYZE`, table sizes, and existing indexes before proposing changes.
3. Never run DDL or data changes against production without explicit authorization and a rollback plan.

## Implementation Rules

- Use `utf8mb4` with a deliberate collation; pick exact types (`DECIMAL` for money, `DATETIME`/`TIMESTAMP` with clear time-zone handling, smallest fitting integer). Define primary keys on every InnoDB table.
- Design composite indexes by leftmost-prefix usage, equality before range columns, and covering needs; remove redundant indexes. Avoid functions on indexed columns in predicates.
- Paginate with keyset (seek) pagination for large tables rather than deep `OFFSET`.
- Keep transactions short; understand gap and next-key locks under REPEATABLE READ; access rows in a consistent order to reduce deadlocks, and retry deadlock errors in application code.
- Plan schema changes for large tables with `ALGORITHM=INSTANT/INPLACE`, gh-ost, or pt-online-schema-change; add columns nullable or with defaults; backfill in batches.
- Use parameterized queries, least-privilege accounts, and TLS; never store plaintext passwords.

## Testing and Verification

Compare `EXPLAIN` before and after, test migrations on a production-like copy, check row counts and constraints after backfills, and confirm replication lag stays acceptable during heavy changes.

## Review Checklist

- Are types, charset, and collation correct for the data?
- Do the target queries use the intended index?
- Will the migration lock or rewrite a large table, and is there a rollback?
- Are transactions short and deadlock-tolerant?
