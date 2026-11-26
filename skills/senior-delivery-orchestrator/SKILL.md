---
name: senior-delivery-orchestrator
description: Coordinate substantial software delivery when distinct work packages or independent review benefit from native agents. Bounded edits and ordinary questions are handled directly.
---

# Senior Delivery Orchestrator

Turn an actionable chat into delivery with the smallest useful context and agent count.

1. Read repository instructions plus only the architecture, paths, and tests relevant to the request. Form an internal Execution Brief: outcome, constraints/risk, likely paths, acceptance checks.
2. Work directly by default, including bounded cross-file changes. Read [routing.md](references/routing.md) only when deciding whether distinct work packages justify delegation. Follow the shared NATURAL_LANGUAGE_ROUTING.md policy and host constraints.
3. Load at most one primary role, two technology skills, and one test skill per work package. Add a second role only when it owns a distinct surface. Never preload the full catalog.
4. Use the Agent tool only at the tier selected in the reference and set the subagent type to the named `senior-work-*` agent. Give each agent a Work Packet under 120 words: goal, owned paths, acceptance checks, skill names, and constraints. Do not forward the full chat; agents must not delegate.
5. Implement and validate routine local source changes without a plan-approval pause. Ask only for a material business decision, conflicting requirements, or production/live infrastructure, credentials, RBAC, deployment, or production-data actions.

Report tier, selected expertise, changed paths, checks, and residual risk briefly.
