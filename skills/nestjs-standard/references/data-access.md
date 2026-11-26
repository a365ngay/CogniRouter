# Data Access

Use this reference for Prisma, TypeORM, transactions, migrations, query placement, and N+1 risks.

## Detect The ORM First

Before editing data access, inspect `package.json`, schema/config files, and nearby modules.

- Prisma: `prisma/schema.prisma`, `@prisma/client`, `PrismaService`, `prisma migrate` scripts.
- TypeORM: `@nestjs/typeorm`, `TypeOrmModule`, entities, repositories, migrations.
- MikroORM/Sequelize/raw SQL: follow the local pattern and avoid importing another ORM.

Never introduce a new ORM or repository style unless the user explicitly asks for a migration.

## Prisma Standards

Prefer direct `PrismaService` use in services for simple CRUD. Add a repository/data-access class only when it reduces meaningful duplication, hides complex query composition, or matches existing project architecture.

```typescript
@Injectable()
export class LocationsService {
  constructor(private readonly prisma: PrismaService) {}

  findPublished() {
    return this.prisma.location.findMany({
      where: { status: 'PUBLISHED' },
      orderBy: { createdAt: 'desc' },
    });
  }
}
```

Use Prisma `select` or `include` intentionally:

- `select` for API responses and sensitive fields.
- `include` for required relations.
- Avoid returning raw Prisma models when response shape should be stable.

Prisma transactions:

```typescript
await this.prisma.$transaction(async (tx) => {
  const order = await tx.order.create({ data: orderData });
  await tx.orderItem.createMany({ data: items.map((item) => ({ ...item, orderId: order.id })) });
  return order;
});
```

Use interactive transactions for dependent writes. Use array transactions for independent operations. Keep transaction bodies short and avoid slow external API calls inside them.

Prisma migrations:

- Change `schema.prisma` first.
- Generate migrations with the repo's script, usually `npx prisma migrate dev --name <name>`.
- Run `npx prisma generate` when generated client types are needed.
- Check generated SQL when altering required columns, renaming fields, or changing relations.

## TypeORM Standards

Use TypeORM repositories when the project is already TypeORM-based.

```typescript
@Injectable()
export class UsersService {
  constructor(
    @InjectRepository(User)
    private readonly usersRepository: Repository<User>,
  ) {}
}
```

Create custom repository/provider classes for complex queries or shared query logic, not for every single entity by default.

TypeORM transactions:

```typescript
await this.dataSource.transaction(async (manager) => {
  const order = await manager.save(Order, orderData);
  await manager.save(OrderItem, items.map((item) => ({ ...item, order })));
});
```

Inside a transaction, use the transaction manager/repositories from that transaction. Do not mix global repositories into transactional code.

Never use `synchronize: true` in production. Use migrations.

## Query Placement

Keep simple queries in services if that is the local pattern. Extract query helpers or repositories when:

- A query is reused across services.
- Query construction is complex enough to distract from business logic.
- The codebase already has a data-access layer.
- Tests need a clear adapter seam around an external database/client.

Do not add a repository solely because a generic best-practice guide says so.

## N+1 Prevention

Look for loops that issue queries per item. Prefer batch queries, relation includes, joins, or DataLoader depending on stack.

Prisma example:

```typescript
const locations = await this.prisma.location.findMany({
  include: { audios: true, beacons: true },
});
```

TypeORM example:

```typescript
return this.locationsRepository.find({
  relations: ['audios', 'beacons'],
});
```

GraphQL resolvers should use request-scoped DataLoaders when field resolvers would otherwise issue repeated queries.

## External Calls And Consistency

Do not perform irreversible external calls inside database transactions unless the local architecture handles compensation.

Prefer this order when possible:

1. Validate input and authorization.
2. Persist local intent/state transactionally.
3. Enqueue or emit external side effects.
4. Update status after side effect completion.

For file uploads, coordinate file storage and DB writes carefully. If storage succeeds and DB write fails, clean up the stored file when practical.
