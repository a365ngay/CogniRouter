# NestJS Architecture

Use this reference for modules, providers, dependency injection, boundaries, lifecycle hooks, and circular dependency risks.

## Feature Modules

Prefer feature modules that own their controller, service, DTOs, and local providers. In an existing codebase, follow the local module shape even if it differs from this ideal.

Good default shape:

```text
src/modules/orders/
  orders.module.ts
  orders.controller.ts
  orders.service.ts
  dto/
  entities/ or models/
  orders.service.spec.ts
```

Module rules:

- Import modules for capabilities, not individual providers from private files.
- Export only providers that other modules legitimately consume.
- Avoid duplicate provider registration across modules; it can create multiple instances and confusing state.
- Put cross-cutting providers in a shared/core module only when they are truly shared.

## Dependency Injection

Prefer constructor injection. It is explicit, testable, and consistent with NestJS testing utilities.

Use simple class injection for concrete local services:

```typescript
@Injectable()
export class OrdersService {
  constructor(private readonly paymentsService: PaymentsService) {}
}
```

Use tokens or abstract classes only when there are multiple implementations, external adapters, test swaps, or plugin-like boundaries:

```typescript
export const PAYMENT_GATEWAY = Symbol('PAYMENT_GATEWAY');

@Injectable()
export class OrdersService {
  constructor(@Inject(PAYMENT_GATEWAY) private readonly gateway: PaymentGateway) {}
}
```

Avoid service locator patterns such as injecting `ModuleRef` just to fetch ordinary dependencies. `ModuleRef` is appropriate for dynamic resolution, plugin systems, optional providers, and advanced lifecycle scenarios.

## Provider Scopes

Default singleton scope is correct for most providers. Request scope is expensive because it can bubble through the dependency graph.

Use request-scoped providers only for request-specific state that cannot be passed explicitly, such as per-request DataLoader instances in GraphQL.

Do not store request or user state on singleton services. Pass it as method arguments or use request-scoped context deliberately.

## Circular Dependencies

Treat `forwardRef()` as a temporary escape hatch, not a design goal. First try to break cycles by:

- Moving shared types or pure helpers to a lower-level module.
- Creating an orchestration service in a higher-level module.
- Publishing domain events instead of direct reverse calls.
- Splitting a service that has two responsibilities.

Use `forwardRef()` only when a small, stable cycle is unavoidable and the codebase already accepts that pattern.

## Lifecycle Hooks

Use lifecycle hooks for infrastructure startup and teardown, not business behavior.

- `OnModuleInit`: initialize connections, warm caches, register consumers.
- `OnApplicationBootstrap`: run app-level startup after modules are ready.
- `OnModuleDestroy` / `BeforeApplicationShutdown`: close clients, flush logs, stop workers.

Avoid blocking app startup with heavy work. Use queues or background jobs for expensive boot tasks.

## Events And Queues

Use events to decouple side effects from core writes when the side effect does not need to be part of the transaction.

Use queues for slow or retryable work: email, media processing, sync packages, external webhooks, report generation.

Keep event payloads stable and explicit. Do not pass ORM entity instances when IDs or small DTOs are enough.
