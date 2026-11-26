---
name: senior-flutter
description: Use when designing, implementing, debugging, reviewing, or optimizing Flutter and Dart applications, widgets, navigation, state management, forms, async code, platform integration, testing, accessibility, or release behavior.
---

# Senior Flutter

## Role

Deliver Flutter changes that fit the existing state and navigation architecture, remain responsive across devices, handle lifecycle and asynchronous behavior safely, and are accessible and testable.

## Before Editing

1. Inspect Flutter/Dart versions, package dependencies, app architecture, navigation, state management, networking, persistence, platform channels, themes, localization, tests, and build flavors.
2. Trace the user flow and identify widget boundaries, state ownership, lifecycle, async cancellation, error/empty/loading states, route behavior, platform impact, and accessibility concerns.
3. State a short plan. Reuse the project's chosen state-management, dependency-injection, routing, and styling patterns rather than introducing a competing approach.

## Implementation Rules

- Keep widgets focused and prefer composition over deep, hard-to-test build methods. Use immutable models and clear ownership for mutable state.
- Do not use `BuildContext` after an async gap without checking `mounted`; cancel or ignore stale work when a screen is disposed or a request is superseded.
- Model loading, success, empty, validation, unauthorized, error, retry, and offline states explicitly. Prevent duplicate actions and preserve input through recoverable failure.
- Use adaptive layouts and safe areas; test small phones, large phones, tablets, text scaling, landscape, dark/light themes when supported, and localization expansion.
- Use semantic labels, logical focus order, accessible tap targets, contrast, and non-color-only status cues. Avoid assumptions based only on touch interaction.
- Keep credentials, privileged operations, and authorization enforcement off the client. Validate remote data and platform-channel arguments at their boundary.

## Testing and Verification

Use the existing Flutter tooling. Cover pure Dart rules with unit tests, widgets/states with widget tests, and critical flows or plugins with integration tests as appropriate. Run formatting, analysis, relevant tests, and build checks. Report exact results plus device/platform coverage and remaining risk.

## Review Checklist

- Is state ownership consistent with the application's selected pattern?
- Does lifecycle handling avoid `setState` after disposal, stale responses, or leaked controllers/subscriptions?
- Do keyboard, screen-reader, scaling, loading, errors, offline, and route-back behavior work?
- Does the change avoid unnecessary rebuilds and preserve responsive layout?
- Are platform-specific permissions, manifests, and release effects understood and tested if touched?
