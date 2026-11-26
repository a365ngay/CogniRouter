---
name: execute-build-test
description: Run scoped build, lint, and test commands from a TaskSpec and summarize failures without full logs.
---

# Execute Build Test

Use when acting as EXECUTOR for verification commands.

Run only TaskSpec-approved commands. Capture exit codes and concise failures. For build or test failures, report file, line, code, and the smallest useful log excerpt.

Save full output under `.cognirouter/state/<task_id>/raw.log` or a referenced artifact. Return compact ExecutionResult fields for build, tests, lint, remaining errors, and recommended next action.

