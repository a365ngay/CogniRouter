# Splitting Patterns

A good slice is vertical: it goes through every layer needed for a user to see the result, it can be demoed on its own, and it can be released (possibly behind a flag) without the other slices.

Never split by layer ("API story", "UI story", "database story") or by activity ("design story", "test story"). Those are tasks inside a story.

## Patterns, in the order to try them

1. **Workflow steps.** Cut a long flow into steps, starting with the thinnest end-to-end path. Example: checkout with voucher → (a) apply one valid voucher, (b) remove or replace it, (c) show it on the receipt and order history.
2. **Business rule variations.** Ship the simplest rule first, add rules as separate stories. Example: fixed-amount voucher first, then percentage with cap, then minimum order value, then per-customer usage limit.
3. **Data variations.** One data type or source first. Example: vouchers typed by the shopper first, then vouchers picked from "My vouchers".
4. **Happy path, then unhappy paths.** The success path is one story; grouped error handling can be the next one, if the first is safe to release (for example behind a flag).
5. **Operations (CRUD).** Create and view first; edit, delete, bulk actions later.
6. **Roles.** One role first, other roles and permission differences later.
7. **Interface or channel.** Web first, then mobile; manual entry first, then import.
8. **Defer performance or scale.** Make it work for the normal volume, then a separate story with an explicit target ("search 1M vouchers within 1 second").
9. **Spike.** When the team cannot estimate because of an unknown, a timeboxed research story whose output is a decision, followed by the real story.

## Signs a story is too big

- More than 8 acceptance criteria, or several independent rule groups.
- Words like "manage", "handle", "support", "full", "all", "and also".
- The team estimate is larger than half a sprint, or estimates disagree widely.
- Several roles with different behavior in one story.
- It needs a different team or system to finish before it can be demoed.

## Output for Split mode

```markdown
**Epic:** <name> — <one-line goal>

| # | Slice | Pattern | Value on its own | Depends on |
|---|-------|---------|------------------|-----------|
| 1 | Apply one fixed-amount voucher at checkout | workflow / rule | shopper saves money; marketing can run the first campaign | — |
| 2 | Percentage voucher with a cap | rule variation | campaigns with % discounts | 1 |

Recommended order: 1 → 2 → ... and why the first slice is the thinnest useful one.
```

Then write full cards for the chosen slices.
