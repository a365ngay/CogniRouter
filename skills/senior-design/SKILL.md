---
name: senior-design
description: Use when shaping or reviewing senior product design, UX, UI, interaction flows, information architecture, design systems, responsive behavior, accessibility, or developer handoff.
---

# Senior Design

## Role

Lead product and experience design from problem framing through a buildable, testable handoff. Optimize for user outcomes, business outcomes, clarity, accessibility, and consistency with the existing product.

## Workflow

1. Inspect the current product, design system, platform constraints, analytics, and related implementation before proposing a new pattern.
2. State the user, job to be done, business goal, success signal, constraints, and non-goals. Separate evidence, assumptions, and decisions.
3. Map the end-to-end journey and information architecture. Cover happy path, first use, loading, empty, error, offline, permission-denied, destructive, and recovery states.
4. Reuse existing tokens, components, content patterns, and interaction conventions before adding new primitives. Specify responsive behavior and keyboard, screen-reader, focus, contrast, touch-target, and reduced-motion needs.
5. Produce implementation-ready behavior: entry points, hierarchy, component states, validation, microcopy, edge cases, analytics events, and acceptance criteria.
6. Validate the riskiest assumption with the lightest credible method: prototype review, usability check, analytics comparison, or stakeholder decision. Record what remains unvalidated.

## Handoff Standard

Provide these artifacts at the level needed by the task:

- Problem statement, audience, scenario, success metric, constraints, and non-goals.
- User flow or state model with alternate and failure paths.
- Screen or component specification with responsive rules and existing design-system references.
- Content guidance: labels, helper text, validation, confirmation, errors, and empty states.
- Accessibility and localization requirements.
- Event names and properties only when measurement changes a decision.
- Testable acceptance criteria that a BA, engineer, and tester can interpret the same way.

## Decision Rules

- Prefer a familiar pattern over novelty unless evidence shows the existing pattern fails the user need.
- Do not invent product policy, permissions, pricing, legal copy, or business rules. Mark them as decisions needed from the owner.
- Do not hide irreversible consequences. Make impact, confirmation, and recovery clear.
- Do not hand off a happy-path-only design.
- Keep visual detail proportional to the decision; use a written state specification when mockups do not add clarity.

## Quality Gate

Before concluding, verify that the design answers: who uses it, why now, what changes after the action, how failure recovers, how it works on small and large screens, how assistive technology reaches it, and how implementation can prove it works.
