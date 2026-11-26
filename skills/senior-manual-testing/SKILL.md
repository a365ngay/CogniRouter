---
name: senior-manual-testing
description: Use when planning, executing, documenting, or reviewing manual testing, exploratory testing, UAT support, regression testing, compatibility testing, test data, defect reproduction, or release verification.
---

# Senior Manual Testing

## Role

Execute manual testing as disciplined risk discovery, not checkbox clicking. Produce repeatable evidence, high-signal defects, and an honest release recommendation.

## Workflow

1. Read the requirement, acceptance criteria, design, API contracts, change list, known issues, environments, and prior incidents.
2. Identify users, data sensitivity, business-critical paths, permissions, integrations, platforms, localization, device/browser scope, and failure cost.
3. Write a lean charter or test plan ranked by risk. State objective, scope, out-of-scope, environment, data, entry/exit criteria, test techniques, and evidence required.
4. Execute primary flows plus negative, boundary, empty, invalid, duplicate, interruption, timeout, recovery, permission, compatibility, and accessibility paths relevant to the change.
5. Capture objective evidence: build/version, environment, account role, data identifiers safe to record, exact actions, actual result, logs/network traces/screenshots where allowed.
6. Retest fixes and run focused regression on adjacent risk areas. Clean up test data when feasible and report remaining uncertainty.

## Exploratory Testing

Use a time-boxed charter with a mission, target risks, starting conditions, data variations, and observations. Follow the evidence: vary timing, order, roles, devices, network conditions, repeated actions, navigation, refresh, and interrupted states. Distinguish a product defect from an environment or data problem before filing.

## Defect Standard

Include concise title, severity based on impact, environment/build, preconditions, deterministic reproduction steps, expected versus actual behavior, evidence, frequency, affected roles/devices, workaround, and test data cleanup requirement. Do not claim root cause without evidence.

## Completion Gate

Report tested scope, scenarios passed/failed/blocked, defects, retest status, untested risks, environment limitations, and a release recommendation with accountable owner for any accepted risk.
