# Test Cases

Use this reference for designing scenarios, test data, and acceptance coverage.

## Scenario Template

Use this concise format unless the project has a formal template:

```text
ID: TC-001
Title: Create published location with valid required fields
Preconditions: Admin user is logged in; API is available
Data: name, description, status=PUBLISHED, beacon optional
Steps:
1. Open Locations page
2. Click Create
3. Fill required fields
4. Submit
Expected:
- Location is saved
- Success message appears
- New row appears with correct status
Coverage: AC-1, AC-3
```

## Coverage Types

For each requirement, consider:

- Happy path.
- Required field and validation failures.
- Boundary values and limits.
- Permissions and roles.
- Duplicate/conflict cases.
- Network/server failure.
- Empty/loading/error UI states.
- Persistence after refresh or navigation.
- Regression around adjacent features.

## Test Data

Make data explicit and reusable. Avoid relying on hidden environment state.

Include user roles, entity status, timestamps/time zones, locale/language, device/browser, and existing records when relevant.

## Traceability

Map test cases to acceptance criteria or requirement IDs. If an AC cannot be tested, mark it as ambiguous or blocked and explain why.
