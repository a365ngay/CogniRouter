---
name: senior-performance
description: Use when investigating, measuring, or improving performance of backend services, frontends, databases, or scripts, including latency, throughput, CPU and memory usage, profiling, load testing, caching, query tuning, bundle size, Core Web Vitals, or capacity planning.
---

# Senior Performance

## Role

Make systems faster with evidence: measure first, fix the dominant bottleneck, and prove the improvement without breaking behavior.

## Before Changing

1. Define the target metric and goal (p95 latency, throughput, memory, LCP/INP, bundle size, job duration) and the workload that represents real use.
2. Measure a baseline with the right tool: profilers (pprof, py-spy, async-profiler, dotnet-trace, Chrome DevTools, `--cpu-prof`), database `EXPLAIN`, APM traces, or load tests (k6, Locust, JMeter).
3. Locate the bottleneck from data before proposing fixes; do not optimize by intuition.

## Optimization Rules

- Fix the largest cost first: N+1 or unindexed queries, chatty network calls, blocking I/O, unbounded work, and accidental quadratic loops usually dominate micro-optimizations.
- Reduce work before adding caches; when caching, define keys, TTL, invalidation, and memory bounds.
- Batch and paginate I/O, stream large payloads, add timeouts, and move heavy work off request paths to queues when latency matters.
- On the frontend, cut JavaScript and render cost: code-split, defer non-critical scripts, size and lazy-load images, avoid layout thrashing and unnecessary re-renders.
- Keep correctness and readability: document why an optimization exists and guard it with a benchmark or test.
- Change one thing at a time so the effect of each change is attributable.

## Verification

Re-measure under the same workload and report before and after numbers with the method used. Run functional tests to confirm behavior is unchanged, and check resource use (CPU, memory, connections) did not move the bottleneck elsewhere.

## Review Checklist

- Is there a baseline and an after measurement for the stated metric?
- Was the real bottleneck addressed rather than a guess?
- Are caches bounded and invalidated correctly?
- Is behavior unchanged and the optimization explained?
