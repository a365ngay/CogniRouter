---
name: jira-ba-dev-test-flow
description: Standard workflow for coordinating BA, developer, and tester agents through Jira. Use when the agent needs to receive a consolidated requirements document, have a BA agent analyze and create Jira tasks/specification work, hand tasks to a dev agent for coding, transition Jira statuses after implementation, hand work to a test agent, mark testing complete, or reopen/link bugs back to development when defects are found.
---

# Jira BA Dev Test Flow

## Core Rule

Run the workflow as a controlled Jira state machine. Always inspect available transitions with `jira_get_transitions` before changing a Jira issue, because workflow names and transition IDs differ by project.

Never invent project keys, issue types, assignees, custom fields, Definition of Ready, or Definition of Done. Infer from user input or existing Jira issues when available; otherwise ask one concise question or create a dry-run plan.

## Required Jira Tools

Use the Atlassian MCP tools when available:

- `jira_get_all_projects`, `jira_get_project_issues`, and `jira_search` to discover the project, existing conventions, parent issues, and recent workflow patterns.
- `jira_get_issue` to inspect fields, assignee, status, comments, and linked context before acting.
- `jira_search_fields` and `jira_get_field_options` to identify required custom fields when a Jira create/update fails or the user mentions a project-specific field.
- `jira_get_user_profile` to resolve assignee identifiers before assignment when needed.
- `jira_create_issue` to create a single Epic, Story, Task, Bug, or Subtask.
- `jira_batch_create_issues` to create BA/dev/test tasks in bulk.
- `jira_update_issue` to update assignee, description, components, attachments, parent/epic link, or custom fields.
- `jira_add_comment` to record handoff notes, decisions, test evidence, and defect details.
- `jira_get_transitions` before every status change.
- `jira_transition_issue` to move issues between statuses.
- `jira_create_issue_link` to connect defects to source tasks.
- `jira_get_issue_dates` for workflow audit or SLA review.
- `jira_add_worklog` only when the user asks to log time or provides time spent.

If Atlassian MCP is not available, produce an executable Jira action plan with exact issue payloads, transition targets, and comments for a human or automation to run.

## Workflow

1. Intake consolidated document
   - Read the document or user-provided summary.
   - Extract goals, scope, actors, flows, data rules, acceptance criteria, dependencies, risks, and open questions.
   - Identify missing decisions before creating work that depends on them.

2. BA creates Jira work
   - Create one parent Epic/Story only when the project convention uses parent work items.
   - Create implementation tasks with clear summaries, business context, acceptance criteria, dependencies, and test notes.
   - Create explicit documentation tasks when the request says "viet tai lieu", "dac ta", "BRD", "SRS", "API spec", or similar.
   - Use `validate_only: true` first unless the user explicitly asks to create issues immediately.
   - After creation, comment with the BA handoff summary and unresolved questions.

3. BA hands off to Dev
   - Confirm each task meets Definition of Ready.
   - Get transitions for each issue and move to the project's dev-ready or in-progress status only when allowed.
   - Add a comment containing scope, acceptance criteria, branch/PR expectation, dependencies, and known risks.

4. Dev implements
   - Code in the target repository using the normal coding workflow.
   - Keep Jira comments factual: changed files/modules, validation commands, known limitations, and PR/commit references.
   - When code is complete, inspect transitions and move to the review, ready-for-test, QA, or equivalent status.
   - Add a dev completion comment before or during the transition.

5. Test verifies
   - Build a test checklist from acceptance criteria and changed behavior.
   - Run automated and manual checks appropriate to the change.
   - Add test evidence: environment, build/commit, commands, pass/fail results, screenshots/logs when relevant.
   - If all checks pass, transition to done/accepted/released according to the available Jira transition.

6. Defect loop
   - If a defect is found, add a detailed comment to the original issue and create or identify a Bug issue.
   - Link the Bug to the source task with `jira_create_issue_link` using the project's standard link type, commonly `Blocks`, `Relates to`, or `is caused by` if available.
   - Reopen or transition the source task only after inspecting available transitions.
   - Assign or hand back to Dev with reproduction steps, expected vs actual behavior, severity, environment, evidence, and regression scope.

## Status Mapping

Treat these as intent labels, not exact Jira status names:

- BA drafting: Backlog, Open, To Do, Analysis, In Refinement.
- Ready for dev: Ready for Development, Selected for Development, To Do.
- Dev active: In Progress, In Development.
- Dev complete: Code Review, Ready for QA, Ready for Test.
- Test active: In QA, Testing, In Test.
- Test passed: Done, Accepted, Ready for Release.
- Defect found: Reopened, In Development, Bug To Do, Failed QA.

Always choose the closest available transition for the current issue and document the reason in the transition comment.

## Handoff Comment Format

Load `references/templates.md` when writing Jira issue descriptions or comments.

Each handoff comment must include:

- Role handing off and recipient role.
- Current scope and issue keys.
- Done so far.
- Next expected action.
- Evidence or links.
- Risks, blockers, or open questions.

## Quality Gates

Definition of Ready:

- Business goal and scope are clear.
- Acceptance criteria are testable.
- Dependencies and impacted systems are named.
- Required designs, APIs, data contracts, or documents are linked or summarized.
- Open questions are either resolved or explicitly non-blocking.

Definition of Dev Done:

- Code change is complete and locally verified.
- Relevant tests pass or skipped tests are justified.
- Jira has a dev completion comment.
- Issue is transitioned to review/QA-ready status when available.

Definition of Test Done:

- Acceptance criteria are verified.
- Regression risk is checked.
- Evidence is attached or summarized.
- Issue is transitioned to Done/Accepted or reopened with defect details.

## Safety

Before creating or transitioning live Jira issues, summarize the intended actions and ask for confirmation when project key, assignee, issue type, status mapping, or production impact is ambiguous.
