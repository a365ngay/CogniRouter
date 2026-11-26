---
name: senior-redis
description: Use when designing, reviewing, debugging, or tuning Redis or Valkey usage, including caching strategies and invalidation, TTLs, data structures, distributed locks, rate limiting, pub/sub and streams, queues (BullMQ, Sidekiq, Celery), memory and eviction, persistence, clustering, or security.
---

# Senior Redis

## Role

Use Redis deliberately: right data structure, explicit TTLs and invalidation, bounded memory, and behavior that degrades safely when Redis is slow or unavailable.

## Before Editing

1. Inspect Redis/Valkey version, deployment (standalone, Sentinel, Cluster, managed), client library, key naming conventions, eviction policy, persistence settings, and existing use (cache, sessions, queues, locks, rate limits).
2. Identify the source of truth for cached data and every write path that must invalidate it.

## Implementation Rules

- Namespace keys consistently (`app:entity:id`) and set a TTL on every cache key; add jitter to avoid synchronized expiry.
- Choose a cache pattern explicitly (cache-aside, write-through) and define invalidation on every write path. Protect hot keys from stampedes (locking, early refresh, request coalescing).
- Pick structures by access pattern: hashes for objects, sorted sets for rankings and time windows, streams for durable event processing. Avoid huge keys and unbounded lists or sets.
- Never use `KEYS` or blocking full scans in production code; use `SCAN` with limits. Use pipelining or Lua/functions for multi-step atomic operations.
- Implement locks with `SET key value NX PX ttl` and token-checked release; know their limits and do not use Redis locks as the only guard for money or critical invariants.
- Treat Redis as a cache unless persistence is configured and accepted; the application must tolerate misses, timeouts, and failover. Set client timeouts.
- Require auth/ACLs and TLS, never expose Redis publicly, and do not store secrets or personal data without need and expiry.

## Testing and Verification

Test cache hit, miss, invalidation, and Redis-down behavior. Check memory with `INFO memory` and `MEMORY USAGE` for new key types, and confirm queue jobs are idempotent and retried as intended.

## Review Checklist

- Does every key have a TTL and a clear invalidation path?
- Is memory bounded and are large or hot keys avoided?
- Does the application stay correct when Redis is unavailable?
- Are atomicity and locking semantics correct for the use case?
