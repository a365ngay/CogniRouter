# Safety Policy

## LOW Risk

Local tools may execute within the authorized task scope:

- Local code edits
- Formatting
- Build
- Tests
- Lint
- Local browser testing
- Generated files
- Non-destructive local commands

## MEDIUM Risk

Controller must decide the solution before local execution:

- Dependency changes
- Schema migrations
- Docker configuration
- CI modification
- Caching
- Performance-related implementation

## HIGH Risk

Requires applicable explicit human authorization. Reuse authorization already given for the same action; pause only when required authorization is missing.

- Production deployment
- Production database access or mutation
- `DELETE`, `DROP`, `TRUNCATE`
- Secrets or credentials
- Permission changes
- Force push
- History rewrite
- Destructive git operation
- External production service mutation
- Destructive cloud infrastructure change

## Git Safety

Allowed by default: `git status`, `git diff`, `git diff --stat`.

Not allowed by default: `git push`, `git push --force`, `git reset --hard`, `git clean -fd`, destructive rebase, remote branch deletion.

Preserve unrelated dirty work. Report conflicts instead of overwriting.

## Logs and Secrets

Do not store secrets, passwords, tokens, credentials, or sensitive test data in TaskSpec, raw logs, ExecutionResult, screenshots, or review files.

