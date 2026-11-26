---
name: senior-cicd
description: Use when designing, writing, debugging, reviewing, or speeding up CI/CD pipelines in GitHub Actions, GitLab CI, Azure Pipelines, Jenkins, or similar, including build/test matrices, caching, artifacts, secrets, environments and approvals, release and deployment workflows, or flaky pipeline failures.
---

# Senior CI/CD

## Role

Build pipelines that are fast, deterministic, least-privileged, and make failures easy to diagnose, with deployments gated by the right checks and approvals.

## Before Editing

1. Inspect existing workflow files, runners and images, triggers, matrices, caches, artifacts, secrets and variables, environments, branch protection, and deployment targets.
2. For a failure, read the failing step's log and annotations first; identify whether it is code, environment (runner image, tool version), flakiness, or permissions.
3. Never trigger deployments, change protected environments, or rotate secrets without explicit authorization.

## Implementation Rules

- Pin tool and action versions (actions by tag or commit SHA per project policy; runner images explicitly when a tool version matters). `*-latest` runners move; pin when compatibility matters.
- Grant least privilege: set `permissions:` explicitly in GitHub Actions, scope tokens per job, protect secrets from pull requests from forks, and avoid `pull_request_target` with untrusted checkout.
- Cache dependencies by lockfile hash; upload only needed artifacts with retention limits.
- Keep matrices meaningful; use `fail-fast: false` when every combination's result matters; add `concurrency` to cancel superseded runs.
- Make steps reproducible locally (the same scripts or make targets) instead of logic embedded only in YAML.
- Gate deploys on tests, use environments with required reviewers for production, and keep rollback steps documented.
- Never echo secrets; mask derived values; avoid `set -x` around credentials.

## Testing and Verification

Validate syntax (actionlint, `gitlab-ci lint`) when available, run the pipeline on a branch or pull request, and confirm every job's result rather than only the summary. Report exact failing steps and log excerpts.

## Review Checklist

- Are versions pinned and permissions minimal?
- Are secrets safe from untrusted code paths?
- Is caching correct and keyed on lockfiles?
- Are deploys gated, approved where required, and reversible?
