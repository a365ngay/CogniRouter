# Execution And Bugs

Use this reference for test execution notes, defect reports, retesting, and regression.

## Execution Notes

Record enough detail for another tester to trust the result:

- Build/version/commit.
- Environment and platform.
- Account/role and key test data.
- Steps executed or automated command.
- Actual result and evidence.
- Pass/fail/blocked status.

## Bug Report Template

```text
Title: [Area] concise symptom
Severity: Critical/High/Medium/Low
Environment: build, browser/device, API/app version
Preconditions: data, user role, feature flags
Steps to reproduce:
1. ...
Expected result:
Actual result:
Frequency: Always / intermittent / once
Evidence: logs, screenshots, network response, error text
Impact: user/business/data impact
Notes: suspected scope or related regression
```

Severity is based on impact and workaround, not emotion.

## Retesting

When a defect is fixed:

- Re-run the exact reproduction steps.
- Verify the expected fix.
- Run nearby regression checks.
- Note build/commit and result.

## Regression

Select regression by change impact:

- Same feature and adjacent workflows.
- Same shared component/service/API.
- Same role/permission path.
- Same data model or migration.
- Same platform-specific behavior.

Avoid massive unfocused regression when a targeted set is enough.
