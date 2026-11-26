# NestJS Testing

Use this reference for unit, integration, and e2e tests in NestJS projects.

## Choose The Test Level

Use the narrowest test that proves the behavior:

- Pure helper/domain logic: plain unit test.
- Service behavior with mocked dependencies: Nest testing module or direct class instantiation.
- Controller validation/guards/interceptors: e2e or integration test when framework behavior matters.
- Database queries, migrations, transactions: integration test against a test database when available.
- Public API contract: e2e test with Supertest or the project's existing request test tool.

Do not add a heavy e2e test for a tiny pure function. Do not mock away the database when the bug is the query.

## Service Unit Tests

Use `@nestjs/testing` when DI, provider tokens, or module setup matters.

```typescript
const moduleRef = await Test.createTestingModule({
  providers: [
    LocationsService,
    {
      provide: PrismaService,
      useValue: prismaMock,
    },
  ],
}).compile();

service = moduleRef.get(LocationsService);
```

For simple services, direct construction is acceptable if it matches local test style.

Mock external services at the boundary. Keep mocks behaviorally faithful: same error shape, same nullability, same important fields.

## Controller And E2E Tests

Use e2e tests for route behavior that depends on Nest plumbing:

- Global validation pipes.
- Guards and decorators.
- Interceptors/serialization.
- Exception filters.
- File upload parsing.

Typical shape:

```typescript
const moduleFixture = await Test.createTestingModule({
  imports: [AppModule],
}).compile();

app = moduleFixture.createNestApplication();
app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
await app.init();

await request(app.getHttpServer())
  .post('/locations')
  .send(payload)
  .expect(201);
```

Mirror the real app bootstrap when behavior depends on global pipes, prefixes, filters, or versioning. If the repo has a test bootstrap helper, use it.

## Database Tests

Prefer the repository's established strategy:

- Testcontainers or Docker database for realistic integration.
- Dedicated test schema/database with migrations.
- Transaction rollback between tests if already implemented.
- Prisma client cleanup with `deleteMany` in safe order when no transaction harness exists.

Do not run destructive cleanup against non-test databases. Check environment variables before database reset scripts.

## Assertions To Include

For NestJS API changes, include at least one assertion for the behavior that could regress:

- Status code and response shape.
- Validation failure for bad input.
- Authorization failure for missing/wrong role.
- Database state after successful write.
- Transaction rollback or no partial write on failure.
- External dependency called with expected payload, or not called on failure.

## Common Test Smells

- Testing implementation details such as private method calls.
- Mocking the method under test's own logic.
- Rebuilding global app setup differently from production when testing validation/auth behavior.
- Leaving timers, app instances, database clients, or queues open after tests.
- Using `any` mocks so loose that contract changes do not fail tests.
