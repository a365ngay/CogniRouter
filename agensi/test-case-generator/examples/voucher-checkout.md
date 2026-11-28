# Worked Example: Voucher at Checkout

## Input

User story **US-1: Apply a voucher code at checkout** with these rules and criteria (abridged):

- BR1 one voucher per order · BR2 valid from start to end inclusive, store time · BR3 subtotal (before shipping) ≥ minimum · BR4 percentage capped · BR5 discount ≤ subtotal, shipping never discounted · BR6 usage limit counted at order placement
- AC1 WELCOME5 ($5 off, min $30) on a $42.00 cart → "WELCOME5 −$5.00", total $37.00
- AC2 SPRING10 (10%, cap $8, min $30): $30.00 → −$3.00 · $80.00 → −$8.00 · $120.00 → −$8.00
- AC3 WELCOME5: $29.99 → "Spend $0.01 more to use WELCOME5." · $30.00 → applied
- AC4 SPRING10 valid 2027-03-01 00:00 to 2027-03-31 23:59: before → "SPRING10 starts on 01/03/2027." · after → "SPRING10 expired on 31/03/2027."
- AC5 unknown code → "We couldn't find this code. Check it and try again."
- AC6 1000 of 1000 used → "SPRING10 has been fully redeemed."
- AC7 4–20 letters and digits ("Codes use letters and numbers only."), case-insensitive, trimmed, Apply disabled when empty
- Assumption A2: amounts rounded half-up to 2 decimals

The full story is in the user-story-writer example.

## Output

### Scope
Applying a voucher on the checkout page (UI and the apply-voucher API behind it). Out of scope: removing or replacing a voucher, re-checking it when the cart changes (US-2), order placement.
Assumptions: T1 — store time zone is UTC+7 for test data. T2 — a test clock can be set in the test environment.

### Requirement gaps
- **G1** — When several rules fail at once (for example expired and below the minimum), which message is shown? → product owner. Blocks TC-22.
- **G2** — AC7 gives a message for invalid characters but none for a code shorter than 4 or longer than 20. → product owner / UX writer. TC-19 uses draft wording until answered.
- **G3** — Behavior when the voucher service is down or times out is undecided (story Q3). → tech lead. No case until decided.
- **G4** — Rounding is an assumption (A2), not a confirmed rule. TC-06 expects half-up; re-check if A2 changes.

### Coverage map

| Req | Risk | Cases | Techniques |
|-----|------|-------|-----------|
| AC1 | High | TC-01 | Use-case path |
| AC2, BR4 | High | TC-02 – TC-06 | Boundary values around the cap, rounding |
| AC3, BR3 | High | TC-07, TC-08 | Boundary values |
| AC4, BR2 | High | TC-09 – TC-12 | Boundary values, time zone |
| AC5 | Medium | TC-13 | Equivalence partitioning |
| AC6, BR6 | High | TC-14 – TC-16 | Boundary values, state |
| AC7 | Medium | TC-17 – TC-20 | Equivalence partitioning, boundary values |
| BR5 | Medium | TC-21 | Use-case path |
| BR1 | — | not covered | belongs to US-2 (replace voucher) |
| Combined failures | Medium | TC-22 | Decision table → exposed G1 |

### Test cases

| ID | Title | Req | Type | Pri | Preconditions | Test data | Steps | Expected result |
|----|-------|-----|------|-----|---------------|-----------|-------|-----------------|
| TC-01 | Apply fixed voucher on an eligible cart | AC1 | Positive | P1 | WELCOME5 active, $5 off, min $30 | subtotal $42.00 | 1. Open checkout 2. Enter WELCOME5 3. Click Apply | Line "WELCOME5 −$5.00"; total before shipping $37.00 |
| TC-02 | Percentage voucher at the minimum subtotal | AC2 | Boundary | P1 | SPRING10 active, 10%, cap $8, min $30 | subtotal $30.00 | Apply SPRING10 | Discount −$3.00; total $27.00 |
| TC-03 | Percentage voucher exactly at the cap | AC2, BR4 | Boundary | P1 | as TC-02 | subtotal $80.00 | Apply SPRING10 | Discount −$8.00; total $72.00 |
| TC-04 | Percentage voucher above the cap | AC2, BR4 | Boundary | P1 | as TC-02 | subtotal $120.00 | Apply SPRING10 | Discount −$8.00 (not $12.00); total $112.00 |
| TC-05 | Percentage voucher just below the cap | AC2, BR4 | Boundary | P2 | as TC-02 | subtotal $79.90 | Apply SPRING10 | Discount −$7.99; total $71.91 |
| TC-06 | Percentage discount rounds half-up | AC2, A2 | Boundary | P2 | as TC-02 | subtotal $33.35 | Apply SPRING10 | Discount −$3.34 (3.335 rounded half-up); total $30.01 |
| TC-07 | Reject one cent below the minimum | AC3, BR3 | Boundary | P1 | WELCOME5 active, min $30 | subtotal $29.99 | Apply WELCOME5 | Not applied; message "Spend $0.01 more to use WELCOME5."; total $29.99 |
| TC-08 | Accept exactly at the minimum | AC3, BR3 | Boundary | P1 | as TC-07 | subtotal $30.00 | Apply WELCOME5 | Line "WELCOME5 −$5.00"; total $25.00 |
| TC-09 | Reject one minute before start | AC4, BR2 | Boundary | P1 | SPRING10 dates as AC4; clock 2027-02-28 23:59 UTC+7 | subtotal $50.00 | Apply SPRING10 | Not applied; "SPRING10 starts on 01/03/2027." |
| TC-10 | Accept in the last minute of validity | AC4, BR2 | Boundary | P1 | clock 2027-03-31 23:59 UTC+7 | subtotal $50.00 | Apply SPRING10 | Discount −$5.00 |
| TC-11 | Reject at the first minute after expiry | AC4, BR2 | Boundary | P1 | clock 2027-04-01 00:00 UTC+7 | subtotal $50.00 | Apply SPRING10 | Not applied; "SPRING10 expired on 31/03/2027." |
| TC-12 | Validity uses store time, not shopper time | AC4, BR2 | Boundary | P2 | clock 2027-03-31 17:30 UTC+0 (= 2027-04-01 00:30 store time); browser time zone UTC+0 | subtotal $50.00 | Apply SPRING10 | Not applied; expired message |
| TC-13 | Unknown code | AC5 | Negative | P2 | no voucher SPRNG10 | code SPRNG10 | Apply SPRNG10 | No discount; "We couldn't find this code. Check it and try again." |
| TC-14 | Reject when usage limit reached | AC6, BR6 | Boundary | P1 | SPRING10 limit 1000, 1000 orders placed | subtotal $50.00 | Apply SPRING10 | Not applied; "SPRING10 has been fully redeemed." |
| TC-15 | Accept with one use remaining | AC6, BR6 | Boundary | P1 | limit 1000, 999 orders placed | subtotal $50.00 | Apply SPRING10 | Discount −$5.00 |
| TC-16 | Applying does not consume a use | BR6 | State | P2 | limit 1000, 999 orders placed | subtotal $50.00 | 1. Apply SPRING10 2. Leave checkout without placing the order | Admin voucher report still shows 999 used |
| TC-17 | Code is case-insensitive and trimmed | AC7 | Positive | P2 | SPRING10 active | input "␣spring10␣" | Apply | Discount applied as SPRING10 |
| TC-18 | Reject symbols in the code | AC7 | Negative | P2 | — | input "SPRING-10" | Apply | "Codes use letters and numbers only."; no discount |
| TC-19 | Code length boundaries | AC7 | Boundary | P3 | no vouchers with these codes | "AB1" (3), "AB12" (4), 20 chars, 21 chars | Apply each | 4 and 20 chars: unknown-code message. 3 and 21 chars: rejected, no discount, draft message "Codes are 4 to 20 characters." (wording per G2) |
| TC-20 | Apply disabled for empty input | AC7 | Negative | P3 | — | empty field; field with only spaces | Look at Apply | Disabled for empty. Spaces only: disabled after trim (confirm with G2) |
| TC-21 | Shipping is not discounted | BR5 | Positive | P2 | WELCOME5 active; shipping $4.99 | subtotal $42.00 | Apply WELCOME5, view summary | Subtotal $42.00, discount −$5.00, shipping $4.99, total $41.99 |
| TC-22 | Expired voucher on a cart below minimum | Decision table, BR2+BR3 | Negative | P2 | clock 2027-04-01 00:00 | SPRING10, subtotal $20.00 | Apply SPRING10 | Not applied; which message — TBD, see G1 |

### Smoke set
TC-01, TC-03, TC-07, TC-11, TC-14 (about 10 minutes).

### Automation candidates
- TC-02 – TC-08: one data-driven API test with an examples table; stable and catches calculation regressions.
- TC-09 – TC-12, TC-14 – TC-15: API level with a controllable clock and seeded usage counts.
- TC-01 and TC-21: one UI end-to-end check of the order summary.
- Not automated yet: TC-22 until G1 is answered; TC-19 asserts behavior now and message text once G2 is answered.

### Not covered
Replacing or removing a voucher and re-checking on cart changes (US-2); concurrent use of the last redemption (order placement); voucher service failure (G3); performance during the campaign launch peak (no target stated).
