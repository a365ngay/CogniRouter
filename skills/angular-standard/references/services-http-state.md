# Services, Http, And State

Use this reference for dependency injection, services, API clients, interceptors, state ownership, and async error/loading handling.

## Services And DI

Use `@Injectable({ providedIn: 'root' })` for application-wide singleton services unless the project has adopted a newer service decorator or scoped provider pattern.

```typescript
@Injectable({ providedIn: 'root' })
export class ApiService {
  private readonly http = inject(HttpClient);
}
```

Use `inject()` in field initializers for modern Angular projects when nearby code does. Constructor injection remains fine in older or established code.

Use `InjectionToken` for configuration values and non-class dependencies:

```typescript
export const API_BASE_URL = new InjectionToken<string>('API_BASE_URL');
```

Provide feature-scoped services at route/component level only when isolated instances are intended.

## HttpClient

Keep HTTP calls in services, not components. Components should call typed service methods and render loading/error states.

```typescript
export interface LocationDto {
  id: string;
  name: string;
  status: 'ACTIVE' | 'INACTIVE';
}

@Injectable({ providedIn: 'root' })
export class LocationsApiService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = '/api/locations';

  list() {
    return this.http.get<LocationDto[]>(this.baseUrl);
  }
}
```

Prefer relative API paths plus dev proxy when the workspace uses a local backend. Do not hardcode `localhost` in reusable services unless existing config already does.

## Interceptors

Use interceptors for cross-cutting HTTP concerns:

- Auth headers.
- Request IDs.
- Global error normalization.
- Loading indicators when the app already centralizes them.

Prefer functional interceptors in modern projects if that is the local style.

```typescript
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const token = inject(AuthService).token();
  return next(token ? req.clone({ setHeaders: { Authorization: `Bearer ${token}` } }) : req);
};
```

Do not swallow errors globally unless the app has a clear user-facing error strategy.

## State Ownership

Pick one owner for each piece of state:

- Local component state for view-only toggles, selected tabs, filters, and transient UI.
- Services/stores for shared feature state, caching, auth session, and API coordination.
- Router state for URL-relevant filters, IDs, and active views.

Avoid duplicating state across service fields, component fields, signals, observables, and route params without a derivation path.

## RxJS Services

For RxJS-based state services, keep subjects private and expose readonly observables.

```typescript
private readonly refreshSubject = new Subject<void>();
readonly locations$ = this.refreshSubject.pipe(
  startWith(void 0),
  switchMap(() => this.api.list()),
  shareReplay({ bufferSize: 1, refCount: true }),
);
```

Use `switchMap` for replacing stale requests, `concatMap` for ordered writes, `exhaustMap` for ignoring duplicate submits, and `mergeMap` for safe parallel work.

## Signal Services

For signal-based services, expose readonly signals and keep mutation methods explicit.

```typescript
private readonly _locations = signal<LocationDto[]>([]);
readonly locations = this._locations.asReadonly();

async reload() {
  const locations = await firstValueFrom(this.api.list());
  this._locations.set(locations);
}
```

Use `resource`/`httpResource` only when supported by the installed Angular version and local project style. Always wire abort signals for cancellable fetches.

## Loading And Errors

Represent loading, success, empty, and error states explicitly in the UI. Avoid a single nullable value that cannot distinguish loading from empty.

For write operations, disable duplicate submits and surface validation/API errors near the affected form or control when possible.
