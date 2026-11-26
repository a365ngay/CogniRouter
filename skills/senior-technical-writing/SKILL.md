---
name: senior-technical-writing
description: Use when writing, restructuring, or reviewing developer and operations documentation, including READMEs, getting-started guides, API docs, architecture decision records (ADRs), design docs and RFCs, runbooks, changelogs, release notes, migration guides, or code comments and docstrings.
---

# Senior Technical Writing

## Role

Write documentation that lets the intended reader succeed at a specific task quickly, stays accurate as code changes, and matches the project's existing voice.

## Before Writing

1. Identify the reader (new contributor, API consumer, operator on call, decision maker) and the task or decision the document must support.
2. Read the existing docs, code, configuration, and commands the document describes. Run the commands you document when possible.
3. Follow the repository's documentation structure, tone, language, and formatting conventions.

## Writing Rules

- Lead with what the reader needs: purpose, prerequisites, then the shortest working path. Put background and edge cases after.
- Use exact, copyable commands, file paths, and versions; show expected output where it helps confirm success.
- Prefer short sections, numbered steps for procedures, tables for options, and one idea per paragraph. Define terms on first use.
- ADRs: context, decision, alternatives considered, and consequences, dated and immutable once accepted (supersede, do not rewrite).
- Runbooks: symptoms, impact, checks in order, mitigation steps, escalation, and rollback, written for someone under pressure.
- Changelogs and release notes: user-facing changes grouped by type, breaking changes and migration steps called out first.
- Comments explain why, not what; keep docstrings accurate to the signature and behavior.
- Never include secrets, internal hostnames that should stay private, or personal data in examples.

## Verification

Follow the document from a clean state (fresh clone, new environment) where practical, check links and code samples, and confirm every claim matches the current code.

## Review Checklist

- Can the target reader complete the task using only this document?
- Are commands, paths, and versions accurate and tested?
- Is it concise, scannable, and consistent with the project's docs?
- Are breaking changes and risks clearly called out?
