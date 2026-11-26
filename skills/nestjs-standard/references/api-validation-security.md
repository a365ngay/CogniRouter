# API, Validation, And Security

Use this reference for controllers, DTOs, pipes, serialization, guards, authentication, authorization, rate limiting, and upload endpoints.

## Controllers

Controllers should be thin adapters:

- Accept route, query, body, file, and user inputs.
- Rely on DTOs and pipes for validation/transformation.
- Call a service method with typed arguments.
- Return a typed DTO or framework response.

Avoid putting database queries or business rules directly in controllers.

```typescript
@Controller('locations')
export class LocationsController {
  constructor(private readonly locationsService: LocationsService) {}

  @Post()
  create(@Body() dto: CreateLocationDto): Promise<LocationResponseDto> {
    return this.locationsService.create(dto);
  }
}
```

## DTOs And Validation

Prefer DTO classes with `class-validator` and `class-transformer` when the project uses Nest's `ValidationPipe`.

Check `src/main.ts` for global pipe settings. Good defaults for public APIs:

```typescript
app.useGlobalPipes(
  new ValidationPipe({
    whitelist: true,
    forbidNonWhitelisted: true,
    transform: true,
  }),
);
```

Use explicit query DTO transforms for numbers, booleans, and arrays. Do not rely on implicit conversion unless the project already does.

```typescript
export class ListLocationsQueryDto {
  @IsOptional()
  @IsEnum(LocationStatus)
  status?: LocationStatus;

  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  @Max(100)
  limit = 20;
}
```

## Serialization

Do not return sensitive fields such as password hashes, refresh tokens, internal secrets, or private file paths.

Use the project's existing style:

- Explicit response DTO mapping in services or mappers.
- `class-transformer` with interceptors if already configured.
- Prisma `select` clauses to avoid fetching sensitive fields.

Avoid adding global serialization changes casually; they can alter many endpoints.

## Authentication And Authorization

Authentication answers who the caller is. Authorization answers whether they can perform this action.

Use guards for route-level auth and policy checks. Keep complex policy logic in dedicated services/helpers when it needs data access or reuse.

```typescript
@UseGuards(JwtAuthGuard, RolesGuard)
@Roles('admin')
@Delete(':id')
remove(@Param('id', ParseUUIDPipe) id: string) {
  return this.locationsService.remove(id);
}
```

For object-level authorization, do not trust route ownership from the client. Load the resource or verify ownership in the service/policy layer.

## Error Handling

Use Nest HTTP exceptions for expected request failures:

- `BadRequestException` for invalid semantic input.
- `UnauthorizedException` for missing/invalid auth.
- `ForbiddenException` for authenticated but not allowed.
- `NotFoundException` for missing resources.
- `ConflictException` for uniqueness or state conflicts.

Do not leak raw database errors, secrets, stack traces, or user-controlled strings in public error messages.

## File Uploads

For upload endpoints:

- Enforce size limits and MIME/extension allowlists.
- Generate server-side filenames or object keys.
- Store metadata in the database after storage succeeds.
- Do not trust original filenames for paths.
- Scan or restrict risky file types when files are later served to browsers.

When serving uploaded files, set safe content type and disposition headers.

## Rate Limiting And Abuse Controls

Use rate limiting for login, password reset, upload, export, and expensive endpoints. In clustered deployments, prefer Redis-backed throttling over in-memory limits.

Avoid applying strict global limits without checking health checks, internal sync jobs, and mobile app retry behavior.
