---
name: senior-react
description: Use when designing, implementing, debugging, reviewing, or optimizing React applications (Vite, CRA, Remix or plain React), components, hooks, state management, data fetching, forms, routing, rendering performance, accessibility, or tests. For Next.js-specific routing, caching or server features use senior-nextjs.
---

# Senior React

## Role

Build React UI that stays predictable: explicit data flow, minimal and well-placed state, effects only for synchronization, accessible markup, and components that are easy to test.

## Before Editing

1. Inspect React version, build tool, router, state and data-fetching libraries (Redux Toolkit, Zustand, TanStack Query, SWR, Context), styling system, form library, lint/type config, and test setup.
2. Trace the affected screen from route to components, props, state owners, server calls, loading/error states, and side effects.
3. State a focused plan that reuses existing components, hooks, tokens, and patterns. Do not add a new state or styling library for one feature.

## Implementation Rules

- Keep state minimal and owned by the lowest common parent that needs it; derive values during render instead of syncing copies. Keep server state in the project's data-fetching layer, not duplicated in client stores.
- Use effects only to synchronize with external systems. Declare complete dependency arrays, clean up subscriptions/timers/aborts, and never fetch in effects when the project already has a query layer.
- Give list items stable keys from data, never array indexes for reorderable lists. Avoid creating components inside render.
- Memoize (`useMemo`, `useCallback`, `memo`) only for measured cost or referential stability that a child or dependency actually needs.
- Handle loading, empty, error, and permission states explicitly. Validate forms on the client for UX and rely on the server for authority.
- Use semantic elements, labelled controls, focus management for dialogs/menus, and keyboard support. Never render untrusted HTML without sanitization (`dangerouslySetInnerHTML`).
- Type props and hooks precisely in TypeScript; avoid `any` and non-null assertions that hide real absence.

## Testing and Verification

Run existing type check, lint, unit/component tests (React Testing Library: query by role and label, assert behavior not implementation), and build. Verify the changed screen in the running app, including error and empty states.

## Review Checklist

- Is every piece of state owned once, with derived data computed rather than stored?
- Do effects have correct dependencies and cleanup, with no fetch races or stale closures?
- Are loading, error, and empty states handled and accessible?
- Did the change avoid unnecessary re-renders without premature memoization?
- Does it reuse existing components, hooks, and design tokens?
