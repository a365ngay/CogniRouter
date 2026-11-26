# Natural-language routing

Provider-neutral policy for choosing skills, agents, and tools. It works the same on Claude, Codex, Gemini, GLM, Qwen, DeepSeek, Kimi, or any model that can read files. Repository policy (`.cognirouter/` in the repo) wins within its scope; host safety rules always apply.

## Request to execution

1. Infer the outcome, the target repository or external system, constraints, and observable acceptance checks from the conversation. Treat follow-ups as refinements. Ask only for missing business rules, an ambiguous destination, or required authorization; continue independent work meanwhile.
2. Read repository instructions and related source before edits.
3. Choose the smallest useful execution mode. **Direct** is the default, including bounded cross-file work. Use subagents only when the host supports them and independent investigation, distinct owned surfaces, or independent review materially improves the result. Complexity, technology count, or file count alone never requires agents.
4. Select one primary workflow skill and only the relevant stack skill or mandatory tool prerequisites (see the tables below and `SKILLS_INDEX.md`). Read entrypoints once; open references only as needed. Do not run BA → architecture → design → test as a mandatory pipeline.
5. Prefer a purpose-built connected tool or MCP server for external records, the local CLI for repository work, and browser automation only when UI evidence or interaction is needed. Read a tool's schema before calling it. A connection does not grant authorization for writes.
6. State a short plan, implement within scope, run relevant checks against existing services/URLs, review, and report actual evidence and limits. Reuse authorization already given for the same action.

## Skill selection

| Intent | Primary skill | Deep reference (optional) |
|---|---|---|
| Requirements, user stories, acceptance criteria | senior-business-analyst | business-analyst-standard |
| Full SRS document + UI package from any input | ba-srs-builder | senior-business-analyst |
| Architecture, contracts, trade-offs, rollout | senior-tech-lead | solution-architect-standard |
| Multi-package delivery that may need agents | senior-delivery-orchestrator | — |
| Backend services / APIs | senior-backend-engineer | — |
| Frontend implementation | senior-frontend-engineer | — |
| Angular | senior-angular | angular-standard |
| NestJS | senior-nestjs | nestjs-standard |
| Next.js | senior-nextjs | — |
| React (non-Next.js) | senior-react | — |
| Vue / Nuxt | senior-vue | — |
| React Native / Expo | senior-react-native | — |
| Flutter / Dart | senior-flutter | — |
| Node.js backend (Express, Fastify, Koa, Hono) | senior-nodejs | — |
| Java / Kotlin, Spring Boot | senior-java-spring | — |
| C# / .NET, ASP.NET Core | senior-dotnet | — |
| Go | senior-go | — |
| Python web backend (FastAPI, Django, Flask) | senior-python-backend | python-standard |
| Python (scripts, libraries, CLIs, data jobs) | python-standard | — |
| PostgreSQL | senior-postgresql | — |
| SQL Server | senior-sql-server | — |
| MySQL / MariaDB | senior-mysql | — |
| MongoDB | senior-mongodb | — |
| Redis / Valkey, caching, queues | senior-redis | — |
| Docker, compose, images | senior-docker | — |
| CI/CD pipelines | senior-cicd | — |
| Terraform / infrastructure as code | senior-terraform | — |
| Kubernetes | senior-kubernetes | — |
| Cloud servers, VMs, Linux ops | senior-cloud-server | — |
| Logging, metrics, tracing, alerts, incidents | senior-observability | — |
| Application security review or fixes | senior-security | — |
| Review a diff or pull request | senior-code-review | — |
| Behavior-preserving refactor | senior-refactoring | — |
| API contract design (REST, GraphQL, gRPC, events) | senior-api-design | — |
| Performance investigation and tuning | senior-performance | — |
| READMEs, ADRs, runbooks, release notes | senior-technical-writing | — |
| Git branching, conflicts, history, releases | senior-git-workflow | — |
| Test a local web app with Playwright | webapp-testing | — |
| Build an MCP server | mcp-builder | — |
| Create or improve a skill | skill-creator | — |
| Word, Excel, PDF, PowerPoint files | docx, xlsx, pdf, pptx | — |
| QA strategy, release readiness | senior-test-engineer | tester-standard |
| Manual / exploratory / UAT | senior-manual-testing | — |
| Automated tests | senior-test-automation | — |
| UX, flows, design system | senior-design | typeui-fundamentals |
| Admin / dashboard / product UI | interface-design | typeui-fundamentals |
| Public marketing page | frontend-design (design-taste-frontend for art direction) | — |
| Existing UI audit / redesign | redesign-existing-projects | — |
| Slide decks | professional-slides | — |
| Jira BA → Dev → Test flow | jira-ba-dev-test-flow | — |
| Executor work from a TaskSpec | execute-implementation, execute-build-test, execute-browser-verify, execute-debug-evidence | — |

Rules: load only the database, framework, and language skills the repository actually uses; never load several database skills, several frontend framework skills, or all testing skills by default. Process skills (code review, refactoring, API design, performance, technical writing, Git) are primary skills for that kind of request and pair with at most one matching stack skill. A cross-stack request may use one lead role plus one frontend and one backend role with only the matching technologies.

Use other installed skills (documents, spreadsheets, PDF, Figma, images) when the deliverable calls for them. Preserve design tokens and branding; optional style references never override them.

## MCP and external destinations

Route by the verified destination, not by provider name. Your own destinations (Jira/Confluence/GitLab hosts and the MCP server name for each) live in `local/MCP_DESTINATIONS.md` under the router home, which is never committed. If that file exists, read it before using an external system.

- Never copy tokens into prompts, packets, reports, or shared policy.
- Never silently switch tenants or fall back to another server for a failed **write**. If the destination is ambiguous, clarify before mutation.
- For **read-only** work, when a paid connector fails (quota, rate limit, auth, timeout), retry at most once, then fall back to the next free option (built-in web search/fetch → browser) and say which fallback was used in the report.

## Subagent work packets

When delegation is permitted and useful, send a short packet: goal, owned paths, acceptance checks, selected skill names, constraints. Keep parallel edits disjoint; dependent work stays sequential. Agents return changed paths, checks, evidence, and open decisions. No recursive delegation, no full chat history.

Host notes:
- Claude Code: subagents `senior-work-researcher|architect|implementer|verifier|reviewer` are installed to `~/.claude/agents/`.
- Codex, Gemini CLI, Qwen Code, opencode and others: use the host's own subagent feature if it has one; otherwise work directly — the routing still applies.

## Evidence and permissions

Config parsing and tool discovery prove readiness only; claim integration success only after a successful call against the intended system. A push is not a deployment. Preserve unrelated changes. Production mutations, deployment, credential/access changes, destructive actions, and sending messages require the applicable user authorization.
