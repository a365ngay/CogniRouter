---
name: senior-vue
description: Use when designing, implementing, debugging, reviewing, or optimizing Vue 3 or Nuxt applications, Composition API, script setup, reactivity, Pinia, Vue Router, components, forms, server rendering, performance, accessibility, or tests.
---

# Senior Vue

## Role

Deliver Vue and Nuxt features with clear reactivity, small focused components and composables, typed contracts, and predictable rendering on client and server.

## Before Editing

1. Inspect Vue/Nuxt version, Options vs Composition API usage, `<script setup>` and TypeScript conventions, Pinia stores, router setup, UI library, auto-imports, lint config, and test tooling (Vitest, Vue Test Utils, Playwright).
2. Trace the affected view from route and layout to components, props/emits, stores, composables, API calls, and SSR data fetching.
3. Follow the project's existing API style; do not mix Options and Composition API in new code unless the codebase does.

## Implementation Rules

- Use `ref` for primitives and replaced values, `reactive` only for stable objects; never destructure reactive objects without `toRefs`. Prefer `computed` for derived state over watchers.
- Use `watch`/`watchEffect` only for side effects, with explicit sources, cleanup (`onWatcherCleanup` or the cleanup callback), and `immediate`/`deep` set deliberately.
- Define `defineProps`/`defineEmits` with types; keep props read-only and communicate up through events or `v-model` contracts.
- Keep shared logic in composables with clear inputs and returned refs; keep global state in Pinia only when several distant components need it.
- In Nuxt, fetch with `useFetch`/`useAsyncData` using stable keys, handle `pending`/`error`, avoid browser-only APIs during SSR, and keep secrets in server runtime config.
- Never bind untrusted HTML with `v-html` without sanitization. Provide labels, focus handling, and keyboard support for interactive components.

## Testing and Verification

Run type check (`vue-tsc`/`nuxi typecheck`), lint, unit/component tests, and build. Verify the changed page in the running app, including hydration warnings in the console for SSR pages.

## Review Checklist

- Is reactivity preserved (no lost refs from destructuring, no mutated props)?
- Are watchers necessary, scoped, and cleaned up?
- Are SSR and client behavior consistent, with no hydration mismatch?
- Are store, composable, and component responsibilities clearly separated?
