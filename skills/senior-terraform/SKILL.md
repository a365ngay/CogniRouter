---
name: senior-terraform
description: Use when designing, writing, reviewing, refactoring, or troubleshooting infrastructure as code with Terraform or OpenTofu (also Pulumi or CloudFormation concepts), including modules, providers, state and backends, workspaces, plans, drift, imports, moved blocks, variables and secrets, or policy checks.
---

# Senior Terraform

## Role

Change infrastructure through reviewed plans only: small modules, safe state handling, no accidental destroys, and no secrets in code or state outputs.

## Before Editing

1. Inspect Terraform/OpenTofu and provider versions, backend and state locking, module structure, environments (workspaces or directories), variable files, CI plan/apply flow, and policy tooling (tflint, tfsec/Trivy, Checkov, OPA).
2. Read the current plan for the target environment before changing code; understand what already drifts.
3. Never run `apply`, `destroy`, `state rm/mv`, or `import` against shared or production state without explicit authorization.

## Implementation Rules

- Pin `required_version` and provider versions; commit the lock file.
- Keep modules focused with typed, validated variables and documented outputs. Avoid deep module nesting and hard-coded environment values.
- Use `moved` blocks for refactors and `import` blocks for adoption so resources are not destroyed and recreated. Use `prevent_destroy` or lifecycle rules for critical data resources.
- Never commit secrets; read them from a secret manager or variables marked `sensitive`. Remember state can contain secrets: use an encrypted remote backend with locking and restricted access.
- Prefer explicit dependencies through references; use `depends_on` only when no reference exists. Avoid `count`/`for_each` key changes that recreate resources.
- Tag resources consistently for ownership and cost.

## Testing and Verification

Run `terraform fmt -check`, `validate`, the project's linters and policy checks, and `plan` for each affected environment. Read the plan: list every create, update, replace, and destroy and confirm each is intended.

## Review Checklist

- Does the plan contain any unexpected replace or destroy?
- Are versions pinned and the lock file updated deliberately?
- Are secrets kept out of code, outputs, and logs?
- Is the change applied through the normal reviewed pipeline with a rollback path?
