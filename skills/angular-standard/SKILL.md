---
name: angular-standard
description: Standards and workflows for implementing, reviewing, debugging, modernizing, and scaffolding Angular applications. Use when working on Angular components, standalone imports, templates, signals, RxJS, forms, Angular Material, routing, guards, resolvers, HttpClient services, interceptors, styling, accessibility, tests, CLI generators, migrations, or new Angular app setup. Prefer this skill for existing Angular repositories where the agent must detect the Angular version and follow local conventions before applying modern Angular patterns.
---

# Angular Standard

Use this skill to make Angular changes that fit the project in front of you. First detect the Angular version and local conventions, then choose the smallest modern pattern that is supported by that version.

## Operating Rules

1. Inspect `package.json`, `angular.json`, `tsconfig*.json`, and nearby feature files before editing.
2. Prefer Angular CLI generators and migrations for Angular-specific structure changes when available.
3. Match the installed Angular version. Do not use APIs such as signal forms, `resource`, or newer standalone defaults unless the project version supports them.
4. Preserve local architecture: standalone components vs NgModules, Material vs custom UI, RxJS services vs signal stores, external templates vs inline templates, and existing naming conventions.
5. For standalone components, every directive, pipe, component, and Angular Material module used by the template must be present in `imports`.
6. Keep components focused on presentation and interaction. Put shared data access, API calls, and state coordination in services or existing stores.
7. Verify with the narrowest useful commands: `ng build`, targeted tests, lint/typecheck, and browser checks for visible UI work.

## Discovery Checklist

Before changing Angular code, identify:

- Angular version, CLI version, package manager, scripts, and builder.
- Project style: standalone components, NgModules, or a mixed migration state.
- Template syntax: built-in control flow (`@if`, `@for`, `@switch`) vs structural directives (`*ngIf`, `*ngFor`).
- State/reactivity style: signals, RxJS subjects/observables, NgRx, ComponentStore, custom services.
- Forms style: reactive forms, template-driven forms, signal forms, or library-specific forms.
- UI library: Angular Material, CDK, Tailwind, Bootstrap, custom design system.
- Test stack: Karma/Jasmine, Jest, Vitest, Cypress, Playwright, Angular testing harnesses.

## Reference Routing

Read only the reference files needed for the task:

- `references/cli-projects.md`: new apps, CLI generation, migrations, builds, dependency changes.
- `references/components-reactivity.md`: components, standalone imports, templates, inputs/outputs, signals, RxJS interop.
- `references/forms-routing.md`: reactive/template/signal form decisions, routes, guards, resolvers, router testing.
- `references/services-http-state.md`: services, DI, HttpClient, interceptors, API state, error/loading handling.
- `references/material-styling-accessibility.md`: Angular Material imports, styling, Tailwind, accessibility, ARIA, animations.
- `references/testing-review.md`: unit/component/e2e tests, harnesses, review checklist, modernization safety.

Do not load every reference by default. Load the smallest relevant set, then inspect source files around the requested change.

## Implementation Workflow

1. Find the closest existing component/service/route/form/test and mirror its style.
2. Use `ng generate` for new Angular artifacts when it will preserve project configuration.
3. Update TypeScript, template, stylesheet, and tests as one behavioral change.
4. For templates, ensure all imports are present and every `@for` has a stable `track` expression when using built-in control flow.
5. For forms, choose the form style already used in the feature unless creating a new app or the user requests modernization.
6. For API calls, use existing API services/interceptors/base URLs rather than creating one-off `HttpClient` calls in components.
7. Run `ng build` when feasible after code generation or template changes. Run targeted tests for logic, routing, forms, and component behavior.

## New App Workflow

When creating a new Angular app:

1. Use the requested Angular version if the user specifies one.
2. If no version is specified, use the available Angular CLI or `npx @angular/cli@latest`.
3. Prefer `ng new <name> --interactive=false` with flags chosen from requirements, such as `--routing`, `--style=scss`, `--ssr`, `--prefix`, and `--ai-config=agents` when supported.
4. Build at least the requested usable feature before starting a dev server.
5. Run `ng build` and fix errors before handing off.

## Review Workflow

For Angular reviews, prioritize findings in this order:

1. Template/runtime errors from missing imports, wrong control flow, nullish access, or version-incompatible APIs.
2. Security issues: unsafe HTML, URL injection, auth guards mistaken for server security, leaking tokens.
3. Broken data flow: subscriptions that leak, effects used to propagate state, duplicated sources of truth.
4. Forms and routing regressions: validators not wired, guards/resolvers returning wrong types, route order mistakes.
5. Accessibility and usability gaps in custom controls, dialogs, menus, tables, and forms.
6. Missing tests for changed behavior and brittle tests that mock Angular primitives instead of using TestBed/harnesses.

Mention when guidance is version-gated or inferred from the installed packages.
