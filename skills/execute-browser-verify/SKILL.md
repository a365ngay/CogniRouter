---
name: execute-browser-verify
description: Run deterministic browser smoke verification from a TaskSpec and return screenshots, console, and network evidence.
---

# Execute Browser Verify

Use when TaskSpec provides preconditions, URL, account or test data, steps, expected result, and required evidence.

Verify expected UI state, blocking console errors, unexpected failed network requests, and observed versus expected behavior.

Return PASS or FAIL, failed step, screenshots or paths, console errors, failed network calls, and concise evidence. Do not attach full traces unless requested.

