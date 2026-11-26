# Components And Reactivity

Use this reference for standalone components, templates, inputs, outputs, signals, RxJS interop, and component-level state.

## Standalone And Imports

Detect whether the project uses standalone components or NgModules.

For standalone components, every template dependency must be listed in `imports`:

```typescript
@Component({
  selector: 'app-location-list',
  standalone: true,
  imports: [CommonModule, RouterLink, MatCardModule, MatButtonModule],
  templateUrl: './location-list.component.html',
})
export class LocationListComponent {}
```

For Angular versions where standalone is not the default, keep `standalone: true` explicit when the project does so. In NgModule projects, declare/import through modules instead of converting a feature casually.

Common missing imports:

- `CommonModule` for `ngClass`, `ngStyle`, and older structural directives.
- `AsyncPipe`, `DatePipe`, `CurrencyPipe`, or other standalone pipes.
- `RouterLink`, `RouterOutlet`, `RouterLinkActive`.
- Angular Material modules matching template tags and directives.

## Templates

Match the template syntax already used nearby.

For modern built-in control flow:

```html
@if (loading()) {
  <mat-spinner />
} @else {
  @for (location of locations(); track location.id) {
    <app-location-card [location]="location" />
  } @empty {
    <p>No locations found.</p>
  }
}
```

Use a stable `track` expression for `@for`. Avoid `track $index` for mutable/reordered data.

For Angular versions/features that still use structural directives, keep `*ngIf` and `*ngFor` unless modernizing is requested.

## Inputs And Outputs

Use signal inputs/outputs only when supported by the installed Angular version and project style.

Modern style:

```typescript
readonly location = input.required<Location>();
readonly selected = output<Location>();
```

Legacy-compatible style:

```typescript
@Input({ required: true }) location!: Location;
@Output() selected = new EventEmitter<Location>();
```

Avoid input/output names that collide with native DOM properties or events. Use camelCase output names and do not prefix with `on`.

## Signals

Use signals for local synchronous state when the project already uses them or the Angular version supports them.

```typescript
private readonly _items = signal<Location[]>([]);
readonly items = this._items.asReadonly();
readonly publishedItems = computed(() => this.items().filter((item) => item.status === 'PUBLISHED'));
```

Rules:

- Derive state with `computed`, not effects.
- Use `effect` for imperative side effects such as analytics, localStorage sync, or third-party DOM APIs.
- Do not call `.set()` or `.update()` inside an effect to propagate state unless there is a very specific, guarded reason.
- Read signals before `await` when dependency tracking matters.

## RxJS Interop

Many Angular apps still use RxJS services. Preserve that style when it is established.

Use `async` pipe in templates instead of manual subscriptions where possible:

```html
@if (locations$ | async; as locations) {
  @for (location of locations; track location.id) {
    <app-location-card [location]="location" />
  }
}
```

When subscribing in TypeScript, use Angular-supported cleanup patterns such as `takeUntilDestroyed()`.

```typescript
private readonly destroyRef = inject(DestroyRef);

ngOnInit() {
  this.api.listLocations()
    .pipe(takeUntilDestroyed(this.destroyRef))
    .subscribe((locations) => this.locations.set(locations));
}
```

Do not create duplicate sources of truth between observables and signals. Choose one owner and derive adapters at boundaries.

## Component Responsibilities

Components should own view state, event handling, and composition. Move cross-component data access, caching, authentication, and business rules into services/stores.

Avoid direct DOM manipulation except through Angular bindings, CDK utilities, or narrow integrations with third-party libraries.
