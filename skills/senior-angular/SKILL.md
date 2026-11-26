---
name: senior-angular
description: Use when designing, implementing, debugging, reviewing, or modernizing Angular applications, standalone components, templates, signals, RxJS, forms, routing, Angular Material, change detection, testing, or performance.
---

# Senior Angular

## Role

Implement Angular changes that follow the repository's version and conventions, keep state and templates understandable, and preserve performance, accessibility, and testability.

## Before Editing

1. Inspect `package.json`, Angular version, workspace configuration, routing, component/module pattern, state management, API services, styling, tests, and existing component examples.
2. Identify component boundaries, input/output or signal contracts, state ownership, data loading, form behavior, error states, change detection strategy, and route/guard impact.
3. State a focused plan. Do not migrate architecture, introduce a state library, or change global configuration unless requested or required by the change.

## Implementation Rules

- Follow the repository's established standalone or NgModule approach. Prefer standalone APIs for new work only when compatible with local conventions and Angular version.
- Keep templates declarative and logic in component or service code. Use `OnPush` where the existing architecture supports it; make change detection behavior explicit when mutating external or asynchronous state.
- Prefer signals for local synchronous state in current Angular patterns; use RxJS for streams, cancellation, composition, and HTTP behavior. Avoid nested subscriptions and ensure subscription lifecycle is safe with `async` pipe, `takeUntilDestroyed`, or a local equivalent.
- Use typed reactive forms for complex or validated forms. Surface validation after appropriate interaction, keep server errors distinct, and disable duplicate submissions.
- Use `track` or `trackBy` for repeated collections, avoid template functions with expensive work, lazy-load substantial routes where consistent, and preserve SSR/hydration constraints if enabled.
- Use semantic markup, labels, keyboard interactions, focus control, ARIA only where needed, and Angular Material/CDK primitives when the project uses them.

## Testing and Verification

Run the project's existing lint, type check, unit, and build commands. Test component states, form validation, service behavior, route/guard behavior, accessibility names, and API error recovery appropriate to the change. Report exact commands and outcomes.

## Review Checklist

- Is state owned and updated predictably without manual subscriptions leaking?
- Are loading, empty, error, unauthorized, and responsive states covered?
- Do template control flow and repeat rendering remain efficient and stable?
- Does the change preserve Angular version compatibility and project conventions?
- Are user-visible behavior and business rules verified rather than internal implementation details?
