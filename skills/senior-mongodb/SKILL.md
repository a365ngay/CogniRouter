---
name: senior-mongodb
description: Use when designing, reviewing, tuning, migrating, securing, or troubleshooting MongoDB data models, documents and schemas, indexes, queries and aggregation pipelines, explain plans, transactions, Mongoose or driver code, sharding, replication, or backups.
---

# Senior MongoDB

## Role

Model MongoDB data around access patterns, back every frequent query with an index, keep documents bounded, and change schemas without breaking existing documents.

## Before Editing

1. Inspect server version, deployment (replica set, sharded, Atlas), driver or ODM (Mongoose, Motor, official drivers), schema validation rules, existing indexes, and migration approach.
2. List the read and write patterns affected and get `explain("executionStats")` for changed queries.
3. Never run destructive operations or index builds on production without authorization and a plan.

## Implementation Rules

- Embed data that is read together and bounded; reference data that grows without limit or is shared. Never let arrays grow unbounded inside a document (16 MB limit, update cost).
- Create compound indexes following equality, sort, range order; verify queries are covered or use `IXSCAN`, not `COLLSCAN`. Remove unused indexes.
- Validate input before building queries; never pass user-controlled objects directly as filters (operator injection such as `$where`, `$ne`). Use projections to return only needed fields.
- Use multi-document transactions only when invariants span documents; keep them short. Prefer atomic single-document updates (`$set`, `$inc`, `$push` with `$slice`).
- Evolve schemas with a version field or tolerant readers; backfill in batches; add `$jsonSchema` validation for new invariants.
- Choose read/write concerns deliberately; for sharded clusters pick shard keys with high cardinality and even distribution.

## Testing and Verification

Check `explain` output for changed queries and aggregations, run tests against a real MongoDB (container) rather than mocks for query logic, and verify migrations on a copy of production-shaped data.

## Review Checklist

- Does the model match access patterns, with bounded documents?
- Is every hot query index-backed?
- Is user input sanitized against operator injection?
- Can old and new document shapes coexist during rollout?
