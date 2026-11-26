---
name: execute-debug-evidence
description: Collect scoped diagnostic evidence such as logs, status, diff, and failing command excerpts for controller analysis.
---

# Execute Debug Evidence

Use when the controller needs facts, not a solution decision.

Collect only requested evidence: command output, logs, `git status`, `git diff --stat`, focused `git diff`, screenshots, console errors, or network failures.

Summarize findings. Save raw output as artifacts under `.cognirouter/state/<task_id>/`. Do not propose architecture or business logic changes.

