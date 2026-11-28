# Coverage Checklist by Feature Type

Pick the sections that match the feature. Each item is a prompt, not a mandatory case: either add a case, mark it out of scope, or raise it as a requirement gap.

## Forms and input
- Required fields empty; only spaces; leading/trailing spaces trimmed
- Min/max length, numeric ranges, decimals and rounding, negative and zero
- Format rules (email, phone, postcode, tax ID); Unicode, emoji, accents; pasted text with hidden characters
- Default values, placeholder vs real value, field-level vs submit-time validation
- Double submit, submit with Enter, browser back after submit, refresh mid-form
- Saved data matches what was entered after reload

## Lists, search, filters, pagination
- Empty state, one item, exactly one page, one more than a page
- Sort order and stable ties; filter combinations; clearing filters
- Search: exact, partial, case, accents, special characters, no results
- Deleted or changed items while paging; deep links to page N

## Authentication, roles, permissions
- Each role can do what it should, and is denied what it should not (UI hidden and API rejected)
- Direct URL or API access to another user's record (IDOR)
- Session expiry mid-action; logout in another tab; password change invalidates sessions
- Lockout after failed attempts; error messages do not reveal whether an account exists

## Tokens, links and one-time codes (password reset, invites, email verification, OTP)
- Expiry measured from issue: just before, at, and just after the limit, using a controllable clock
- Single use: reuse after success; two submissions of the same token at once; is it consumed on open or on submit
- Retry on the same token after a validation failure
- A newer request invalidates older tokens, or not (decide)
- Tampered, truncated, random and other-user tokens all give the same outcome and reveal nothing
- Form opened before expiry, submitted after (check at time of use, not only time of opening)
- Unknown and known identifiers get the same message, status code, redirect and similar response time (no account enumeration)
- Disabled, locked or unverified accounts; rate limits on requesting and on guessing
- Side effects only on success: sessions ended, notifications sent, audit entry written

## Money, prices, quantities
- Rounding per line vs total; currency format and symbol; multiple currencies
- Discounts, caps, minimums at their boundaries; totals never negative
- Tax and shipping included or excluded as specified
- Refunds and cancellations reverse every side effect (stock, voucher usage, points)

## Dates, times, time zones
- Start and end boundaries inclusive or exclusive; midnight; end of month; leap day
- Store, server and user time zones; daylight-saving change
- Date formats per locale; past and future dates allowed or not

## Files and uploads
- Allowed and blocked types (check content, not only extension); size at and above the limit
- Zero-byte file, duplicate names, long or Unicode names
- Upload interrupted; virus or malformed file; preview and download back

## APIs
- Status codes for success, validation error, unauthorized, forbidden, not found, conflict, rate limit
- Required and unknown fields; wrong types; null vs missing; very large payloads
- Idempotency of retries; pagination parameters; contract matches documentation
- Error body format is consistent and leaks no internals

## Integrations and background jobs
- Downstream service slow, down, returning errors or unexpected data
- Retries do not duplicate effects; timeouts surface a clear message
- Jobs: rerun safety, partial failure, run at boundary times, overlapping runs

## Notifications (email, SMS, push, in-app)
- Right recipient, right trigger, right content and links, sent once
- Unsubscribed or missing contact; localization; delay limits

## Concurrency and state
- Two users edit or consume the same record or last unit at once
- Stale data after another user's change; optimistic locking messages
- Invalid state transitions are rejected

## Localization and accessibility
- Translated text fits; plurals; right-to-left if supported
- Keyboard-only use, focus order, visible focus, screen reader labels for errors
- Color is not the only signal; zoom 200% still usable

## Non-functional (only with a stated target)
- Response time under expected load; large data volumes
- Audit log entries for sensitive actions; data retention and deletion
