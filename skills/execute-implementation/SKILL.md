---
name: execute-implementation
description: Execute controller-approved implementation tasks inside the allowed file scope and return compact evidence.
---

# Execute Implementation

Use when acting as EXECUTOR for approved code changes.

Stay inside `allowed_files`. Do not modify `forbidden_files`. Preserve unrelated dirty work. Prefer the smallest change that satisfies acceptance criteria.

Run only commands listed in `commands_allowed`. If required work is outside scope or high risk, stop and return an ExecutionResult with `needs_controller_decision: true`.

Return changed files, diff summary, commands, verification status, remaining errors, and concise evidence. Do not include full logs unless requested.

