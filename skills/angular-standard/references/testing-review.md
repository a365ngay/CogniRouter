# Testing And Review

Use this reference for Angular tests, component harnesses, e2e checks, code review, and modernization risk.

## Choose The Test Level

Use the narrowest useful test:

- Pure functions, pipes, validators: unit tests.
- Services: unit tests with mocked dependencies or HttpClient testing utilities.
- Components: TestBed/component tests for templates, bindings, forms, Material interactions.
- Routing: RouterTestingHarness or existing router test helpers.
- User workflows: e2e tests with the project's configured framework.

Do not add a brittle e2e test for logic that a focused component test can prove.

## Component Tests

Use the project's configured runner and patterns. Angular tests commonly use TestBed.

```typescript
TestBed.configureTestingModule({
  imports: [LocationListComponent],
  providers: [{ provide: LocationsApiService, useValue: apiMock }],
});

const fixture = TestBed.createComponent(LocationListComponent);
await fixture.whenStable();
```

Modern Angular rendering can be async. Prefer an act, wait, assert rhythm:

1. Act: set input, emit event, click button, update signal, resolve request.
2. Wait: `await fixture.whenStable()` or the local helper.
3. Assert: inspect DOM, emitted output, service calls, or router state.

Use `fixture.detectChanges()` when the local test stack still requires it, but do not spam it as a substitute for understanding async rendering.

## Material And Harnesses

For Angular Material components, prefer component harnesses over brittle CSS selectors when available.

Harness tests are especially useful for dialogs, selects, menus, tables, tabs, and form fields.

## Http Tests

Use the project's Angular HTTP testing setup. For modern provider-based apps, this often means `provideHttpClient()` plus testing providers. For older apps, it may mean `HttpClientTestingModule`.

Assert request method, URL, params, body, and error handling.

## Router Tests

Use `RouterTestingHarness` or local helpers for routes, guards, resolvers, params, and navigation. Avoid mocking `Router` when the route configuration itself is the behavior under test.

## E2E And Visual Checks

Use e2e for workflows that span pages, auth, network behavior, or browser APIs. After meaningful frontend UI changes, run or manually verify the page in a browser when a dev server is available.

Check mobile and desktop viewports for text overflow, overlapping controls, inaccessible dialogs, and missing loading/error states.

## Review Checklist

Prioritize:

- Version-incompatible Angular APIs.
- Missing standalone imports or NgModule declarations.
- Template null errors, unstable `@for track`, and bad async pipe usage.
- Subscriptions without cleanup.
- Effects used to propagate state rather than `computed` or explicit methods.
- Unsafe `innerHTML`, URL injection, token exposure, or auth assumptions.
- Forms without validators, error states, submit protection, or disabled/loading handling.
- Routes in the wrong order, missing wildcard placement, or guards returning invalid values.
- Material components without required modules or accessible labels.
- Missing tests for changed behavior.

## Modernization Safety

For migrations to standalone, built-in control flow, signal inputs, outputs, or `inject()`:

1. Run official schematics when available.
2. Keep changes scoped by project/path if possible.
3. Build after each migration step.
4. Inspect generated diffs for changed public inputs/outputs and tests.
5. Avoid mixing modernization with unrelated feature work.
