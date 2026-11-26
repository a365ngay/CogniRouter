# Routing And Budget

## Delivery Tier

| Tier | Use when | Agents |
|---|---|---|
| Direct | Default for questions, reviews, and bounded implementations following existing patterns | None; work in the main session. |
| Focused | One bounded code surface with a clear outcome | Direct by default; optional implementer or verifier when isolation adds value. |
| Integrated | Multiple files or layers that follow an existing pattern, or a security/data/API/regression concern | Optional distinct specialists only for unresolved investigation or independent checks; no mandatory agent pipeline. |
| Broad | An unresolved cross-system/rollout decision, a migration, or independent packages that must coordinate | Controller selects only useful specialists with disjoint scope; dependent work stays sequential. |

Never classify work as Broad merely because it uses multiple technologies. Never parallelize agents that might edit the same path. Do not use architecture or review agents merely to restate a small task.

## Work Packet

    Goal:
    Owned paths:
    Acceptance checks:
    Selected skills:
    Constraints:

Use only entries that affect the request. A role skill establishes responsibility; a technology skill adds stack-specific judgment.

The skill cap applies per Work Packet, not to the whole delivery. Do not load every potential role into the parent or a single agent.

| Signal | Skill | Use only when |
|---|---|---|
| Requirements, scope, acceptance criteria | senior-business-analyst | A missing business decision blocks a correct implementation. |
| UX, visual flow, design system | senior-design | The request has distinct UX, visual behavior, or design-system requirements; not an ordinary screen following local patterns. |
| Cross-system design, trade-offs, rollout | senior-tech-lead | An architectural boundary, contract, rollout, or trade-off decision is unresolved; not merely because a request is cross-stack. |
| UI implementation | senior-frontend-engineer | A frontend surface is owned by the task. |
| API, service, integration, persistence | senior-backend-engineer | A backend surface is owned by the task. |
| Quality strategy or release risk | senior-test-engineer | Test scope or release risk needs design. A generic request to test uses existing targeted checks first. |
| Exploratory/UAT/manual evidence | senior-manual-testing | Manual behavior is explicitly requested or is the only practical evidence. |
| Existing or requested automated tests | senior-test-automation | Automation is explicitly requested or the project already has a relevant suite. |

| Technology | Skill |
|---|---|
| SQL Server | senior-sql-server |
| PostgreSQL | senior-postgresql |
| Angular | senior-angular |
| Next.js | senior-nextjs |
| NestJS | senior-nestjs |
| Flutter | senior-flutter |
| Kubernetes | senior-kubernetes |
| Cloud server, deployment, runtime operations | senior-cloud-server |

Do not select both database skills, both frontend framework skills, or all test skills by default. A cross-stack request can use a tech-lead skill plus one frontend and one backend role, but should still load only the matching technologies.

Example: a notification-settings request spanning Next.js, NestJS, and PostgreSQL is normally Integrated when local patterns exist. Route a frontend packet to senior-frontend-engineer plus senior-nextjs, an API/data packet to senior-backend-engineer plus senior-nestjs and senior-postgresql, and then verify. Add BA, design, tech lead, or a testing specialization only when the stated trigger is present.
