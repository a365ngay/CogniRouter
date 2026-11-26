# CLI And Projects

Use this reference for new apps, Angular CLI generation, dependency setup, builds, migrations, and workspace structure.

## Version And Workspace Detection

Start with:

- `package.json`: Angular packages, CLI version, scripts, UI libraries, test runner.
- `angular.json`: project names, builders, style preprocessor, assets, budgets, serve proxy.
- `tsconfig*.json`: strictness, path aliases, template checking.
- `src/main.ts`, `src/app/app.config.ts`, `src/app/app.routes.ts`, `src/app/app.module.ts`: standalone vs NgModule bootstrap.

Use the repo's package manager lockfile: `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, or `bun.lockb`.

## New Angular Apps

If the user requests a specific Angular version, use that version explicitly:

```bash
npx @angular/cli@<version> new <app-name> --interactive=false
```

If no version is requested, check whether `ng` is available. Use the installed CLI when it exists; otherwise use the latest CLI:

```bash
ng new <app-name> --interactive=false
npx @angular/cli@latest new <app-name> --interactive=false
```

Choose flags from actual requirements:

- `--routing` for multi-page apps.
- `--style=scss|css|less` based on user/project preference.
- `--ssr` only when server rendering/prerendering is needed.
- `--prefix=<prefix>` for organization or design-system selector conventions.
- `--skip-tests` only when explicitly requested.
- `--ai-config=agents` when supported and useful for agent configuration.

Do not start the app before implementing the requested usable feature. Use `ng build` for verification.

## Generating Code

Prefer CLI generation for Angular artifacts because it respects workspace config and updates related files.

```bash
ng generate component features/locations/location-list
ng generate service core/services/api
ng generate directive shared/directives/autofocus
ng generate pipe shared/pipes/status-label
ng generate guard core/guards/auth
ng generate interceptor core/interceptors/auth
ng generate resolver features/locations/location-detail
```

After generation, inspect the actual generated paths and edit those files. Do not assume path casing or suffixes.

For existing codebases, follow local naming. Some projects use `LocationListComponent`; newer guidance may omit `Component` suffix, but do not rename existing patterns casually.

## Adding Angular Libraries

Prefer `ng add` for Angular libraries because it runs schematics:

```bash
ng add @angular/material
ng add tailwindcss
```

Use the repo's package manager for non-Angular libraries, then wire configuration manually if needed.

## Builds And Serve

Run the script the repo already exposes, often:

```bash
npm run build
npm start
ng build
ng serve
```

If a local backend is required, inspect proxy config before changing API URLs. Prefer Angular dev proxy for local `/api` routing instead of hardcoding localhost in services.

## Migrations And Modernization

Prefer official migrations for large syntax updates:

```bash
ng update @angular/core @angular/cli
ng generate @angular/core:control-flow
ng generate @angular/core:signal-input-migration
ng generate @angular/core:output-migration
ng generate @angular/core:inject
ng generate @angular/core:self-closing-tag
```

Run migrations in small steps and build after each major migration. For standalone migration, use the official multi-phase workflow and verify between phases.

Do not run broad migrations in a dirty worktree without understanding unrelated user changes.
