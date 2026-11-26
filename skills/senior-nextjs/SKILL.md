---
name: senior-nextjs
description: Use when designing, implementing, debugging, reviewing, or optimizing Next.js applications, App Router or Pages Router, React Server Components, Server Actions, route handlers, caching, rendering, SEO, authentication, or deployment.
---

# Senior Next.js

## Role

Build Next.js changes that choose server and client boundaries deliberately, protect data and secrets, preserve predictable caching and rendering behavior, and deliver accessible, performant experiences.

## Before Editing

1. Inspect the Next.js and React versions, router type, project configuration, deployment target, authentication model, API layer, data fetching, caching, middleware, styles, tests, and existing route conventions.
2. Identify the route's rendering mode, data ownership, cache/revalidation behavior, server-client boundary, authorization boundary, metadata/SEO impact, and error/loading states.
3. State a short plan. Do not mix App Router and Pages Router patterns or promote components to client components without a demonstrated browser-only need.

## Implementation Rules

- Default to Server Components and server-side data access. Add `'use client'` only at the smallest interactive leaf; pass serializable data across the boundary.
- Authenticate and authorize on the server for data access and mutations. Treat middleware as a routing optimization, not the sole enforcement point. Keep secrets, privileged queries, and internal errors server-side.
- Choose caching intentionally. Specify `fetch` cache behavior, route segment revalidation, tag invalidation, or dynamic rendering based on freshness and personalization requirements. Do not rely on defaults for sensitive or mutable data.
- Validate all mutation input on the server. Make Server Actions and route handlers handle authorization, idempotency where relevant, expected errors, and safe redirects.
- Use `loading`, `error`, `not-found`, suspense boundaries, and meaningful empty states to maintain a stable user experience. Avoid hydration mismatches and client-side waterfalls.
- Keep metadata, canonical URLs, structured data, robots rules, image optimization, and accessibility aligned with the route's product purpose.

## Performance and Verification

Avoid serial data fetching when parallelism is possible, oversized client bundles, unnecessary client state, and uncached duplicate queries. Run existing lint, type, test, and production build commands; inspect route behavior, permissions, cache invalidation, metadata, and loading/error paths affected by the change.

## Review Checklist

- Is server/client placement minimal and justified?
- Are cache, revalidation, personalization, and mutation semantics explicit?
- Are authorization and validation enforced where data or side effects occur?
- Does the route handle loading, error, not found, empty, and responsive accessibly?
- Did the change preserve the repository's router, deployment, and observability conventions?
