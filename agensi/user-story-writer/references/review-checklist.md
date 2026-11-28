# Review Checklist

Score each line Pass / Weak / Fail with one short reason. Lead the review with Fails, then Weaks.

## INVEST

| Check | Pass when |
|---|---|
| Independent | Can be built and released without waiting for another story in the same sprint, or the dependency is named and planned |
| Negotiable | States the need and the rules, not a fixed technical solution (unless the solution is a real constraint) |
| Valuable | The "so that" names an outcome a user or the business cares about |
| Estimable | The team has enough information to size it; unknowns are listed as questions or a spike |
| Small | Fits comfortably in one sprint; 8 acceptance criteria or fewer (more than 8, or several independent rule groups: split) |
| Testable | Every acceptance criterion has an observable pass/fail result with concrete values |

## Definition of Ready

| Check | Pass when |
|---|---|
| Role is specific | Not "user" unless all users really behave the same |
| Business rules are explicit | Listed separately, each covered by an AC |
| Unhappy paths considered | Validation, permission, not found, duplicate, limit, dependency failure: each covered, out of scope, or a question |
| Exact values | Limits, formats, rounding, time zone, currency, and message text stated or flagged as TBD |
| Scope boundary | Out-of-scope list exists |
| Dependencies known | Other teams, systems, data, designs, or legal sign-off named |
| Data and permissions | Who can see and do what; what is stored, for how long |
| Non-functional needs | Performance, security, audit, accessibility, analytics where relevant |
| Design available | Link or "no UI change" |
| Open questions owned | Each blocking question has someone to answer it |

## Review output

```markdown
**Verdict:** Ready / Ready with fixes / Not ready — one sentence why.

| Check | Result | Reason |
|---|---|---|
| Testable | Fail | AC2 "discount is calculated correctly" has no expected value |
...

**Gaps that will cause rework**
1. ...

**Rewritten story** (changes: ① added BR2 from AC text, ② split AC2 into AC2 and AC3, ...)
```
