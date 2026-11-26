# Stories And Acceptance Criteria

Use this reference for user stories, acceptance criteria, business rules, and examples.

## Story Format

Use story format when it clarifies user value:

```text
As a <role>
I want <capability>
So that <business outcome>
```

For technical enablers, use a task format with clear outcome and acceptance criteria.

## Acceptance Criteria

Prefer Given/When/Then for workflow behavior:

```text
AC1 - Create location successfully
Given an admin is on the Locations page
When they submit valid required fields
Then the location is saved
And it appears in the list with the selected status
```

Criteria should be:

- Observable.
- Testable.
- Specific about roles, data, states, and error messages when relevant.
- Independent enough that pass/fail is clear.

## Business Rules

Capture rules separately from UI steps:

```text
BR1: A beacon can be assigned to only one active location at a time.
BR2: Published locations must have at least one audio file in the default language.
```

## Edge Cases

Include edge cases when they affect implementation or testing:

- Empty states.
- Duplicate data.
- Permission denied.
- Invalid formats and limits.
- Offline/network failure.
- Concurrent edits.
- Localization/time zone differences.
