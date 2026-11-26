# Orchestration

## Core Rule

```text
Need WHY, WHAT, WHICH APPROACH: Controller.
Need DO, RUN, GENERATE, VERIFY: Controller/local tools.
```

The main model session (any provider) is the controller and reviewer.

## Flow

```text
User Task
  -> Controller analyzes, decides, plans
  -> Controller executes with local tools
  -> Controller verifies
  -> Controller reviews
  -> PASS done, FAIL targeted follow-up
```

## Controller Duties

- Decide architecture, business rules, API contracts, data strategy, security, and scope.
- Execute and verify locally.
- Read git diff and changed files as needed.
- Keep changes scoped.

## Executor Duties

- Optional subagents act as executors only inside a Work Packet (see NATURAL_LANGUAGE_ROUTING.md); they never decide architecture, business rules, or security.

## Follow-up Tasks

Use ordinary local follow-up work.
