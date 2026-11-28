# Acceptance Criteria

## Two formats, pick per behavior

**Scenario format (Given/When/Then)** for behavior that follows a flow: a user does something and the system responds.

```text
AC3 — Expired voucher is rejected
Given a voucher "SPRING10" that expired on 2026-03-31 23:59 store time
And a cart with subtotal $50.00
When the shopper applies "SPRING10" on 2026-04-01 at 00:01
Then the voucher is not applied
And the message "This voucher expired on 31/03/2026." is shown under the voucher field
And the order total stays $50.00
```

**Rule-list format** for constraints that hold everywhere and have no single trigger (formats, limits, display rules, non-functional targets).

```text
AC7 — Voucher code input
- Accepts 4 to 20 characters, letters and digits only
- Is case-insensitive ("spring10" = "SPRING10")
- Leading and trailing spaces are trimmed before validation
```

Do not force rule lists into fake Given/When/Then.

## Writing rules

- **Given** sets state and data, not actions. Name the role and the relevant records.
- **When** is exactly one action or event (user action, time passing, inbound message).
- **Then** is observable from outside: what is shown, stored, sent, charged, logged, or denied. Not "the system validates".
- Use concrete example values. Examples catch misunderstandings that abstractions hide.
- Name every scenario (`AC3 — Expired voucher is rejected`) so it can be referenced in tests and comments.
- One AC per distinct outcome. Merge only when the outcome is identical for several inputs (then list the inputs, or use a small examples table).
- Cover each business rule with at least one passing and one failing scenario.
- Include the exact user-facing message, or write `message: copy TBD` and add an open question. Never write "an error message is shown".

## Examples table (many inputs, same shape)

```text
AC4 — Minimum order value
Given voucher "WELCOME5" gives $5.00 off and requires a subtotal of at least $30.00
When the shopper applies it to a cart with subtotal <cart>
Then the result is <result>

| cart   | result                                           |
| $29.99 | not applied: "Spend $0.01 more to use WELCOME5." |
| $30.00 | applied, total $25.00                            |
| $30.01 | applied, total $25.01                            |
```

## Vague words and what to write instead

| Vague | Ask or replace with |
|---|---|
| fast, quickly, in real time | a number: "within 2 seconds for 95% of requests", "within 1 minute" |
| user-friendly, intuitive, easy | the concrete behavior that makes it easy (default value, autofocus, one click) |
| properly, correctly, as expected, appropriate | the actual expected value or state |
| should work, should be supported | the scenario that proves it works |
| etc., and so on, such as | the full list, or "the list in BR2" |
| secure | who may and may not do it, and what happens when they try |
| large, many, a lot | the limit and what happens when it is exceeded |
| immediately | synchronous, or a maximum delay |
| handle errors | each error, its trigger and its message |
| notify the user | channel (email, push, in-app), recipient, content, timing |

## Unhappy paths checklist

Ask of each story: what happens when the input is missing, invalid, too long, duplicate, or out of range; the user lacks permission or the session expired; the record was deleted, changed by someone else, or is in the wrong state; an external service is slow or down; the action is repeated (double click, retry, back button); time crosses a boundary (midnight, month end, time zone, daylight saving).

You do not need an AC for every item. You need a conscious decision: covered by ACn, out of scope, or an open question.

## Bad vs good

Bad:
```text
AC1: User can apply a voucher and the discount is calculated correctly.
```

Good:
```text
AC1 — Percentage voucher applied to eligible cart
Given voucher "SPRING10" gives 10% off, capped at $8.00
And the cart subtotal is $50.00
When the shopper applies "SPRING10"
Then a discount line "SPRING10 −$5.00" appears
And the order total before shipping is $45.00
```
