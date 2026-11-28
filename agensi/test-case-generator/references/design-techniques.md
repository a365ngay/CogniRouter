# Test Design Techniques

## Equivalence partitioning

Split each input into classes the system should treat the same way; one test per class is enough. Always include invalid classes.

Example — voucher code field, 4 to 20 letters and digits:

| Class | Example | Valid |
|---|---|---|
| 4–20 letters/digits | `SPRING10` | yes |
| lowercase of a valid code | `spring10` | yes (case-insensitive rule) |
| shorter than 4 | `AB1` | no |
| longer than 20 | 21 characters | no |
| contains symbols | `SPRING-10` | no |
| empty / spaces only | `"   "` | no |

## Boundary value analysis

Bugs cluster at edges. For each boundary test the value on it and the nearest values on each side, using the smallest step the system stores (1 cent, 1 second, 1 character).

Example — minimum subtotal $30.00: test $29.99, $30.00, $30.01.
Example — valid until 2027-03-31 23:59: test 23:58, 23:59, 2027-04-01 00:00 (and check the time zone used).
Example — max 20 characters: test 19, 20, 21.

Example — link valid for 30 minutes after issue at time T: test T+29:59, T+30:00 (inclusive or not is often unspecified: raise a gap), T+30:01. Set the clock in the test environment or back-date the token instead of waiting.

Two-value BVA (on the boundary and just outside) is enough for low-risk fields; use three values for money, dates and limits.

## Decision table

Use when outcomes depend on a combination of conditions. List conditions as rows, rules as columns, and collapse columns whose outcome does not depend on a condition (`–` = any).

Example — applying a voucher:

| Condition | R1 | R2 | R3 | R4 | R5 |
|---|---|---|---|---|---|
| Code exists | N | Y | Y | Y | Y |
| Within validity period | – | N | Y | Y | Y |
| Usage limit not reached | – | – | N | Y | Y |
| Subtotal ≥ minimum | – | – | – | N | Y |
| **Outcome** | unknown code | not started / expired | fully redeemed | spend more | applied |

Each column becomes at least one test case. The table also exposes questions: when two rules fail at once (expired and below minimum), which message wins? If the spec does not say, that is a requirement gap.

## State transition

Draw the states and allowed events, then test every valid transition and the invalid ones that matter (especially those that would bypass payment, approval or audit).

Example — order: `Draft → Placed → Paid → Shipped → Delivered`, plus `Placed → Cancelled`, `Paid → Refunded`.
Test valid transitions, then invalid ones such as `Shipped → Cancelled` or paying a `Cancelled` order. Check what happens to side effects (voucher usage released on cancellation?).

## Pairwise (all-pairs)

When many independent parameters each have a few values, test every pair of values at least once instead of every combination. 4 parameters × 3 values = 81 combinations, but about 9 to 12 pairwise cases. Generate the set by hand for small inputs or name a tool (PICT, allpairspy) for large ones. Add explicit cases for known risky combinations on top.

## Use-case paths

For a flow: one case for the main success path, one per alternative path, one per exception path. Good for UAT scripts and end-to-end checks.

## Error guessing

Add cases from experience where the spec is silent: double submit, browser back after submit, session expiry mid-flow, very long or Unicode input, copy-paste with hidden spaces, zero, negative, rounding, leap day, daylight-saving change, two users editing the same record. Use `coverage-checklist.md` to pick the ones relevant to this feature.

## Choosing depth by risk

| Risk | Depth |
|---|---|
| High | all partitions, 3-value boundaries, full decision table, invalid transitions, concurrency, regression of neighbors |
| Medium | all partitions, 2-value boundaries, main decision rules, main invalid transitions |
| Low | happy path, one negative per rule, obvious boundary |
