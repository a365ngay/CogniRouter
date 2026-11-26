---
name: senior-refactoring
description: Use when restructuring, cleaning up, simplifying, or modernizing existing code without changing behavior, including extracting functions or modules, removing duplication or dead code, reducing coupling, renaming, upgrading legacy patterns, or paying down technical debt in small safe steps.
---

# Senior Refactoring

## Role

Improve structure while preserving behavior exactly, in small verified steps that are easy to review and revert.

## Before Editing

1. Define the goal of the refactor (readability, testability, removing duplication, enabling a feature) and the boundary of code in scope.
2. Find all callers and usages, including reflection, dynamic imports, configuration, templates, and public API consumers.
3. Ensure tests cover current behavior. If they do not, add characterization tests first that pin today's outputs, including odd ones.

## Refactoring Rules

- Never mix refactoring with behavior changes or bug fixes in the same step; note discovered bugs separately.
- Move in small steps (rename, extract, inline, move, replace conditional) and run tests after each. Prefer IDE or tool-assisted refactors for renames and moves.
- Keep public APIs, serialized formats, database schemas, and event contracts stable unless the change explicitly includes a migration path.
- Remove dead code only after proving it is unused (search, logs, feature flags). Delete rather than comment out.
- Do not introduce abstractions for hypothetical future needs; the result should be simpler than the start.
- Preserve formatting and conventions of the codebase; avoid large formatting-only diffs mixed with logic moves.

## Testing and Verification

Run the full relevant test suite, linters, and type checks before and after. Compare behavior on representative inputs when tests are thin. Keep commits small so each can be reviewed and reverted on its own.

## Review Checklist

- Is behavior provably unchanged (tests green before and after, no contract changes)?
- Is the result simpler and easier to change?
- Were all usages updated, including dynamic and external ones?
- Is the diff reviewable, with no unrelated changes?
