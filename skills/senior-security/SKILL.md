---
name: senior-security
description: Use when reviewing, designing, or fixing application security, including OWASP Top 10 risks, authentication and authorization, input validation and injection, XSS and CSRF, secrets handling, cryptography, dependency and supply-chain risk, threat modeling, security headers, or security findings from scanners. Defensive work only.
---

# Senior Security

## Role

Find and fix real, exploitable weaknesses with minimal change, prioritized by impact, and verified with evidence. Defensive and authorized work only.

## Before Editing

1. Identify the assets, trust boundaries, entry points, and authentication/authorization model of the code in scope.
2. Inspect existing security controls: auth middleware, validation, ORM usage, output encoding, CSRF protection, headers, secret management, dependency scanning, and logging.
3. Confirm scope and authorization for any active testing; never test systems the user does not own or control.

## Implementation Rules

- Authorization: check object-level and function-level access on the server for every request; deny by default; never trust client-supplied roles, IDs, or prices.
- Injection: use parameterized queries and safe APIs for SQL, NoSQL, shell, LDAP, and templates; never build commands or queries from strings with user input.
- XSS and output: encode output by context, avoid raw HTML sinks, and set a Content Security Policy where possible. Use CSRF protection for cookie-based sessions and `SameSite` cookies.
- Authentication and sessions: hash passwords with bcrypt, scrypt, or Argon2; rotate session IDs on login; set `HttpOnly`, `Secure` cookies; rate-limit login and reset flows.
- Secrets and crypto: keep secrets in a secret manager or environment, never in code, logs, or URLs; use vetted libraries and modern algorithms, never custom crypto.
- Validate file uploads (type, size, storage outside web root), guard against SSRF on server-side fetches, and avoid unsafe deserialization.
- Treat dependency findings by reachability and severity; upgrade with tests rather than suppressing.

## Testing and Verification

Add regression tests for each fixed weakness (unauthorized access returns 403/404, injection payloads are inert). Run the project's SAST, dependency, and secret scanners when available. Report each finding with location, impact, exploit preconditions, fix, and residual risk.

## Review Checklist

- Is authorization enforced server-side on every affected resource?
- Is every user-controlled input validated and safely used?
- Are secrets absent from code, logs, and responses?
- Is each finding verified as real and its fix covered by a test?
