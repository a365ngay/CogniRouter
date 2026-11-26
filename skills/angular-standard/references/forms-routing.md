# Forms And Routing

Use this reference for form strategy, validators, route definitions, guards, resolvers, navigation, and router tests.

## Choosing A Form Strategy

Match the feature's existing form style unless creating a new app or modernizing by request.

- Reactive forms: best default for complex forms, typed controls, validation, dynamic fields, and tests.
- Template-driven forms: acceptable for simple forms in projects already using `FormsModule`.
- Signal forms: use only when the installed Angular version supports them and the app has adopted them.

Do not mix form strategies inside one form without a concrete reason.

## Reactive Forms

For reactive forms, import `ReactiveFormsModule` in standalone component imports or module imports.

```typescript
private readonly fb = inject(NonNullableFormBuilder);

protected readonly form = this.fb.group({
  name: ['', [Validators.required, Validators.maxLength(100)]],
  status: ['ACTIVE' as LocationStatus, Validators.required],
});

protected submit() {
  if (this.form.invalid) {
    this.form.markAllAsTouched();
    return;
  }

  const value = this.form.getRawValue();
}
```

Use `NonNullableFormBuilder` when null values are not part of the domain model. Prefer `getRawValue()` when disabled controls matter.

In templates, bind submit to `ngSubmit` and keep error messages tied to touched/dirty/submitted state.

## Template-Driven Forms

For template-driven forms, import `FormsModule`. Every `[(ngModel)]` inside a form must have a `name` attribute.

```html
<form #form="ngForm" (ngSubmit)="submit()">
  <input name="title" required [(ngModel)]="model.title" #title="ngModel" />
  @if (title.invalid && (title.dirty || title.touched)) {
    <mat-error>Title is required</mat-error>
  }
  <button type="submit" [disabled]="form.invalid">Save</button>
</form>
```

## Route Definitions

Use the project's existing routing style. Standalone apps commonly define `Routes` arrays and `provideRouter`.

```typescript
export const routes: Routes = [
  { path: '', component: DashboardPage, title: 'Dashboard' },
  { path: 'locations/:id', component: LocationDetailPage, title: 'Location detail' },
  { path: '**', component: NotFoundPage },
];
```

Rules:

- Put specific routes before less specific routes.
- Put wildcard routes last.
- Add route titles for accessibility and browser history clarity.
- Use lazy loading for feature areas when it fits the existing architecture.

## Guards And Resolvers

Prefer functional guards/resolvers in modern Angular projects.

```typescript
export const authGuard: CanActivateFn = () => {
  const auth = inject(AuthService);
  const router = inject(Router);
  return auth.isAuthenticated() ? true : router.parseUrl('/login');
};
```

Guards can improve UX but are not security boundaries. Server-side authorization must still protect APIs.

Resolvers are useful for data required before route activation. Avoid resolvers for optional data that can load gracefully inside the component.

## Navigation

Use `RouterLink` for declarative navigation in templates and `Router` for imperative navigation after actions.

In standalone components, import `RouterLink`, `RouterLinkActive`, or `RouterOutlet` explicitly.

Avoid raw `<a href>` for in-app navigation because it triggers full page reloads.

## Router Testing

Use `RouterTestingHarness` or the project's existing router test helper when behavior depends on real router configuration.

```typescript
TestBed.configureTestingModule({
  providers: [provideRouter([{ path: 'locations/:id', component: LocationDetailPage }])],
});

const harness = await RouterTestingHarness.create();
await harness.navigateByUrl('/locations/123', LocationDetailPage);
await harness.fixture.whenStable();
```

Avoid mocking `Router` when you need confidence in route config, guards, params, or navigation behavior.
