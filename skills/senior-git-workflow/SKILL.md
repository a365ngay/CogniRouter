---
name: senior-git-workflow
description: Use when planning or performing Git work such as branching strategy, commits and messages, rebasing or merging, resolving conflicts, cherry-picking, bisecting, recovering lost work, rewriting history, tagging and releases, monorepo or submodule issues, or repository hygiene (.gitignore, large files, leaked secrets).
---

# Senior Git Workflow

## Role

Keep history clear and recoverable, resolve conflicts without losing work, and never surprise collaborators with destructive changes.

## Before Acting

1. Check the state: `git status`, current branch, upstream tracking, unpushed commits, stashes, and whether the branch is shared or protected.
2. Read the repository's branching, commit message, and release conventions (contributing guide, PR templates, tag format).
3. Before any destructive operation (force push, history rewrite, `reset --hard`, branch or tag deletion), create a backup ref and get explicit authorization.

## Workflow Rules

- Make focused commits with messages that state what and why, following the project's convention (for example Conventional Commits).
- Prefer `git push --force-with-lease` over `--force`, and never force-push shared or protected branches without agreement.
- Resolve conflicts by understanding both sides: read each change's intent, keep both behaviors where required, then run tests. Never resolve by blindly choosing ours or theirs for whole files.
- Use `git bisect` with a test command to find regressions; use `git reflog` to recover lost commits before assuming work is gone.
- Rewriting published history changes every downstream hash and tag: update tags and releases and tell collaborators to re-clone or reset.
- Leaked secrets: rotate the secret first, then remove it from history (git filter-repo or BFG) and force-push with coordination; history rewriting alone is not enough.
- Keep build output, dependencies, and local config out of the repository with `.gitignore`; use Git LFS for large binaries if the project allows it.

## Verification

After the operation, confirm with `git log --oneline --graph`, `git status`, and a diff against the expected tree, and run tests after merges, rebases, or conflict resolutions.

## Review Checklist

- Was a backup ref created before any destructive step?
- Is the resulting history and tree exactly what was intended?
- Were collaborators, tags, and releases accounted for after rewrites?
- Are secrets rotated, not just removed from history?
