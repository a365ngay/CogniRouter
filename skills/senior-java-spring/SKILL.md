---
name: senior-java-spring
description: Use when designing, implementing, debugging, reviewing, or refactoring Java or Kotlin services with Spring Boot, Spring MVC/WebFlux, Spring Data JPA, transactions, validation, Spring Security, configuration, messaging, Maven/Gradle builds, tests, or observability.
---

# Senior Java Spring

## Role

Build Spring services with clear layering, correct transaction and persistence behavior, secure endpoints, validated input, and tests at the right level.

## Before Editing

1. Inspect Java/Kotlin and Spring Boot versions, build tool (Maven/Gradle), module layout, controller/service/repository conventions, DTO mapping (MapStruct or manual), exception handling (`@ControllerAdvice`), security config, profiles, and test setup (JUnit 5, Mockito, Testcontainers).
2. Trace the request or message from entry point through validation, security, service logic, transactions, repositories, external calls, and response mapping.
3. Reuse existing patterns; do not introduce a new framework layer, mapper, or reactive stack for one change.

## Implementation Rules

- Keep controllers thin; put business rules in services; expose DTOs, never JPA entities, across the API boundary.
- Validate input with Bean Validation (`@Valid`, constraints) and map failures to the project's error contract.
- Place `@Transactional` on service methods with deliberate propagation and read-only flags. Remember self-invocation bypasses proxies; avoid long transactions around remote calls.
- Watch JPA pitfalls: N+1 queries (use fetch joins or entity graphs), lazy loading outside transactions, `equals/hashCode` on entities, and unbounded `findAll`. Paginate lists.
- Enforce authorization in Spring Security with method or request rules tied to the resource, not only UI hiding. Never log secrets or personal data.
- Use constructor injection, immutable configuration properties (`@ConfigurationProperties` with validation), and explicit timeouts/retries for outbound HTTP and messaging.
- Add Micrometer metrics, structured logs with correlation IDs, and health indicators consistent with the project for changed operational paths.

## Testing and Verification

Run the build with unit tests and relevant slice tests (`@WebMvcTest`, `@DataJpaTest`) or integration tests with Testcontainers. Check generated SQL for changed queries and run static analysis the project already uses.

## Review Checklist

- Are transaction boundaries and propagation correct, including rollback on the intended exceptions?
- Are queries bounded, indexed, and free of N+1 behavior?
- Is input validated and authorization enforced before side effects?
- Are entities kept inside the persistence layer and errors mapped consistently?
