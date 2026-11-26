# Routing Policy

## Always Controller

- Architecture
- Domain design
- Business rules
- Authentication
- Authorization
- Permissions
- Tenancy
- Payment
- Security
- Data ownership
- Transaction strategy
- Concurrency
- Idempotency
- Database schema strategy
- Destructive migrations
- Event semantics
- Distributed transactions
- Production infrastructure architecture
- Production secrets
- Performance architecture
- Breaking public API contract changes

## Default Local Execution

Run these tasks with local tools.

- Scaffolding
- Boilerplate
- Repetitive edits
- Rename or move files inside approved scope
- Import or namespace fixes
- Formatting
- Lint
- Package restore
- Controller-approved dependency install
- Build
- Unit test execution
- Integration test execution
- E2E execution
- Local Docker build
- Local Docker Compose
- Generated code
- DTOs
- Mappers
- Validators
- Simple CRUD after controller-defined contract
- Test generation from acceptance criteria
- Browser smoke testing
- UI click-through verification
- Console and network inspection
- Screenshot capture
- Log collection
- `git status`
- `git diff`
- `git diff --stat`
- Changelog from diff

## Hybrid

Controller decides, executes with local tools, verifies, and reviews. Native subagents are optional under NATURAL_LANGUAGE_ROUTING.md.

- Migrations
- SQL optimization
- Performance optimization
- Caching
- Kubernetes configuration
- CI/CD changes
- Major dependency upgrades
- Multi-module refactors
- Authentication implementation
- Background jobs
- Message queues

## Stack-aware Commands

Allow only when present in the repo and listed in TaskSpec.

- .NET: `dotnet restore`, `dotnet build`, `dotnet test`, `dotnet format`
- Angular or Node: package install, lint, build, test, format, generate, browser test
- NestJS: scaffold, DTO, validation, Swagger boilerplate, build, test, lint
- Flutter: `flutter pub get`, `flutter analyze`, `flutter test`, `dart format`

See NATURAL_LANGUAGE_ROUTING.md for intent, skill, native-agent, and MCP destination selection.
