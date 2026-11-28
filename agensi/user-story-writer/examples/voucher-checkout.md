# Worked Example: Voucher at Checkout

## Input (a chat message from a product owner)

> hey, marketing wants voucher codes at checkout for the spring campaign. codes like SPRING10 = 10% off but max $8, and some fixed ones like WELCOME5 = $5 off. needs min order $30 i think. each code has a limit (e.g. first 1000 orders) and start/end dates. should be easy to use and show errors properly. launch in 3 weeks pls

## Output

**Goal.** Shoppers can enter a campaign voucher code at checkout and get the discount immediately, so marketing can run the spring campaign within 3 weeks.

**Size check.** Applying a code, and keeping it valid while the cart changes, are two separate pieces of value. Proposed split:

| # | Slice | Pattern | Depends on |
|---|-------|---------|-----------|
| US-1 | Apply a voucher code at checkout | workflow step, happy + core rules | — |
| US-2 | Keep the voucher valid when the cart changes (remove, replace, re-check minimum) | workflow step | US-1 |

US-1 is the thinnest slice marketing can launch with. Card below.

---

### US-1: Apply a voucher code at checkout

**Story**
As a shopper at checkout, I want to enter a voucher code and see the discount on my order, so that I pay the campaign price without contacting support.

**Context** — Spring campaign launches in 3 weeks. Two voucher kinds exist: fixed amount (WELCOME5) and percentage with a cap (SPRING10). Vouchers are created by marketing outside this story.

**Business rules**
- BR1: One voucher per order.
- BR2: A voucher is valid from its start to its end date-time inclusive, in the store time zone.
- BR3: The cart subtotal (before shipping and tax) must be at least the voucher's minimum order value.
- BR4: A percentage discount is capped at the voucher's maximum discount.
- BR5: The discount never exceeds the subtotal; shipping is never discounted.
- BR6: Each voucher has a total usage limit, counted when an order is placed, not when the code is applied.

**Acceptance criteria**

AC1 — Fixed-amount voucher applied
Given voucher "WELCOME5" gives $5.00 off with a $30.00 minimum and is active
And the cart subtotal is $42.00
When the shopper applies "WELCOME5"
Then a discount line "WELCOME5 −$5.00" appears in the order summary
And the order total before shipping is $37.00

AC2 — Percentage voucher respects the cap (BR4)
Given voucher "SPRING10" gives 10% off, capped at $8.00, minimum $30.00, and is active
When the shopper applies "SPRING10" to a cart with subtotal <subtotal>
Then the discount is <discount>

| subtotal | discount |
|----------|----------|
| $30.00   | −$3.00   |
| $80.00   | −$8.00   |
| $120.00  | −$8.00   |

AC3 — Minimum order value not met (BR3)
Given voucher "WELCOME5" requires a $30.00 minimum
When the shopper applies it to a cart with subtotal <subtotal>
Then the result is <result>

| subtotal | result |
|----------|--------|
| $29.99   | not applied; message "Spend $0.01 more to use WELCOME5." |
| $30.00   | applied, −$5.00 |

AC4 — Voucher outside its validity period (BR2)
Given voucher "SPRING10" is valid from 2027-03-01 00:00 to 2027-03-31 23:59 store time
When the shopper applies it at <time>
Then the result is <result>

| time | result |
|------|--------|
| 2027-02-28 23:59 | not applied; message "SPRING10 starts on 01/03/2027." |
| 2027-03-31 23:59 | applied |
| 2027-04-01 00:00 | not applied; message "SPRING10 expired on 31/03/2027." |

AC5 — Unknown code
Given no voucher "SPRNG10" exists
When the shopper applies "SPRNG10"
Then no discount is applied
And the message "We couldn't find this code. Check it and try again." is shown under the field

AC6 — Usage limit reached (BR6)
Given voucher "SPRING10" has a usage limit of 1000 and 1000 orders have been placed with it
When the shopper applies "SPRING10"
Then no discount is applied
And the message "SPRING10 has been fully redeemed." is shown

AC7 — Code input
- Accepts 4 to 20 letters and digits; other characters show "Codes use letters and numbers only."
- Case-insensitive: "spring10" applies SPRING10
- Leading and trailing spaces are trimmed
- The Apply button is disabled while the field is empty

**Edge cases and errors**
- Two shoppers apply the last remaining use at the same time: BR6 counts usage at order placement, so applying never reserves a use. Candidate AC for the checkout story: re-check the limit when the order is placed.
- Discount larger than subtotal: BR5, candidate AC once a voucher type can exceed it (not possible with current limits).
- Voucher service unavailable: candidate AC, see Q3.

**Out of scope** — removing or replacing a voucher and re-checking it when the cart changes (US-2); "My vouchers" wallet; stacking vouchers; per-customer limits; creating vouchers in the admin; shipping discounts.

**Assumptions**
- A1: The $30 minimum is set per voucher, not global ("min order $30 i think").
- A2: Amounts are in the store currency, rounded half-up to 2 decimals.
- A3: Error text above is draft copy for marketing to approve.

**Open questions**
- Q1 (marketing): Is the minimum the same for every voucher, or set per voucher? Confirms A1.
- Q2 (marketing): Do vouchers apply to items already on sale?
- Q3 (tech lead): If the voucher check fails or times out, block checkout or let the shopper continue without the discount?

**Notes for dev/test** — Track `voucher_applied` and `voucher_rejected` (with reason) for campaign reporting. Usage-limit race conditions belong to the order-placement check, not to this story.

---

**Next step:** generate test cases from AC1–AC7 (boundaries in AC2–AC4 are good candidates), then estimate US-1 and US-2.
