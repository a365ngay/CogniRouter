# CogniRouter

**Automatic, provider-neutral skill routing for AI coding agents.**

Type an ordinary request ("add an export button to the orders page", "review this migration", "write the SRS from these PDFs") and the agent picks the right skill on its own: one primary workflow skill, the matching stack skill, nothing more. No slash commands, no skill names to remember, the same behavior on every model.

Works with **Claude Code, OpenAI Codex, Gemini CLI, Qwen Code, opencode**, models served through them (**GLM, Kimi, DeepSeek, OpenRouter, local models**), any tool that reads `AGENTS.md` (Cursor, Copilot, Windsurf, Zed...), and web chats through a single-file export.

```text
request ──► ROUTER block (always loaded) ──► SKILLS_INDEX.md ──► 1 primary skill + 1 stack skill ──► plan ► do ► verify ► report
                    │
                    └── safety policy: production, credentials, destructive Git ⇒ ask first
```

## Why

- **One policy, every host.** Each host gets the same routing block, rendered with that host's paths. Hosts with a native skill tool use it; hosts without one simply read `SKILL.md` from disk.
- **Small context.** The always-on block is about 1,000 tokens. Skills load only when the intent matches; references load only when the skill points to them.
- **Direct by default.** Subagents only when they add value. No mandatory BA → architect → dev → QA pipeline for a one-line fix.
- **Safe to install.** Your existing instructions and same-named skills are never overwritten (use `--force` to back up and replace). Everything is reversible with `uninstall`.
- **No secrets in the repo.** Your own Jira/Confluence/GitLab hosts live in a git-ignored local file.

## Quick start

Requirements: Python 3.8+, and Git (only for the third-party skills).

```bash
git clone https://github.com/<you>/cognirouter.git
cd cognirouter
python installer/cognirouter.py install          # auto-detects installed hosts
python installer/cognirouter.py status
```

Windows: `.\install.ps1` · macOS/Linux: `./install.sh` (same arguments).

Start a new session in your AI tool afterwards.

### Common options

| Command | What it does |
|---|---|
| `install --hosts claude,codex,gemini,qwen,opencode` | Choose hosts (`all`, or `auto` = detected). Aliases: `glm`, `kimi`, `deepseek` → `claude`. |
| `install --project path/to/repo` | Write the block into one repo's `AGENTS.md` (+ a `CLAUDE.md` that imports it). |
| `install --no-upstream` | Offline: bundled skills only. |
| `install --upstream all` | Also fetch opt-in upstreams (Understand-Anything). |
| `install --no-skills` | Only the instruction block; skills stay in `~/.cognirouter/skills`. |
| `install --dry-run` | Show what would change. |
| `install --force` | Back up, then replace existing skills/agents that have the same name. |
| `export --with-skills senior-tech-lead` | Single Markdown prompt for ChatGPT, GLM chat, Gemini app, Claude Projects. |
| `uninstall [--hosts x] [--project dir] [--purge]` | Remove blocks, managed skills, and agents. Backups are kept. |
| `lock --refresh` | Move upstream pins to the latest commit (review before committing). |
| `hosts` | Show supported hosts, detected ones, and their paths. |

## What gets installed where

| Host | Instruction file | Skills |
|---|---|---|
| Claude Code | `~/.claude/CLAUDE.md` | `~/.claude/skills/` + subagents in `~/.claude/agents/` |
| Codex | `~/.codex/AGENTS.md` (`$CODEX_HOME` honored) | `~/.agents/skills/` |
| Gemini CLI | `~/.gemini/GEMINI.md` | `~/.agents/skills/` |
| Qwen Code | `~/.qwen/QWEN.md` | `~/.qwen/skills/` |
| opencode | `~/.config/opencode/AGENTS.md` | `~/.config/opencode/skills/` |
| Any repo | `<repo>/AGENTS.md`, `<repo>/CLAUDE.md` | points to `~/.cognirouter/skills/` |

The library itself (policies, skills index, every skill, backups, state) lives in `~/.cognirouter/`. The block is wrapped in `<!-- COGNIROUTER:START/END -->` markers; text outside the markers is yours and is never touched.

Provider setup (GLM, Kimi, DeepSeek, local models): see [docs/PROVIDERS.md](docs/PROVIDERS.md).

## Skills

**Bundled (MIT, 30 skills)**

| Group | Skills |
|---|---|
| Roles | `senior-tech-lead`, `senior-business-analyst`, `senior-design`, `senior-backend-engineer`, `senior-frontend-engineer`, `senior-test-engineer`, `senior-manual-testing`, `senior-test-automation`, `senior-delivery-orchestrator` |
| Stacks | `senior-angular`, `senior-nextjs`, `senior-nestjs`, `senior-flutter`, `senior-postgresql`, `senior-sql-server`, `senior-kubernetes`, `senior-cloud-server` |
| Deep standards | `angular-standard`, `nestjs-standard`, `python-standard`, `solution-architect-standard`, `business-analyst-standard`, `tester-standard` |
| Executors (TaskSpec) | `execute-implementation`, `execute-build-test`, `execute-browser-verify`, `execute-debug-evidence` |
| Deliverables | `ba-srs-builder` (SRS in Word + HTML UI package), `professional-slides`, `jira-ba-dev-test-flow` |

**Fetched from upstream at a pinned commit** (not redistributed, see [NOTICE.md](NOTICE.md)): `interface-design`, `frontend-design`, `design-taste-frontend`, `redesign-existing-projects`, `typeui-fundamentals`, `ui-ux-pro-max`, `Uncodixfy`, `enterprise`, `minimalist-ui`, `industrial-brutalist-ui`, `stitch-design-taste`, `brandkit`, `imagegen-frontend-web`, `imagegen-frontend-mobile`; opt-in: Understand-Anything.

Full list with descriptions: [docs/SKILLS.md](docs/SKILLS.md).

## Your own systems (MCP)

Copy `~/.cognirouter/local/MCP_DESTINATIONS.example.md` to `MCP_DESTINATIONS.md` in the same folder and list your Jira/Confluence/GitLab hosts and the MCP server name used for each. The router reads it before touching an external system and never falls back to another server for a write. Put host names only; tokens stay in each MCP server's own config.

## Repository layout

```text
core/          ROUTER.md (the block) + routing, orchestration, routing and safety policies, TaskSpec templates/schemas
skills/        bundled skills (Agent Skills format: <name>/SKILL.md + references/ + scripts/)
agents/claude/ senior-work-* subagents for Claude Code
installer/     cognirouter.py (stdlib only)
local/         *.example.md templates for private config (real files are git-ignored)
scripts/       optional PowerShell event log + live viewer
tests/         offline installer tests
upstream.lock.json  third-party skills and pinned commits
```

## Customize

- **Change routing:** edit `core/NATURAL_LANGUAGE_ROUTING.md` (intent → skill table) or `core/ROUTER.md` (the always-on block), then re-run `install`.
- **Add a skill:** create `skills/<name>/SKILL.md` with `name` and `description` frontmatter; the index is rebuilt on install. Run `python installer/cognirouter.py index` to refresh `docs/SKILLS.md`.
- **Per-repository policy:** add a `.cognirouter/` folder with your own policy files to a repo; it takes precedence there.

## Development

```bash
python -m unittest discover -s tests -v
python installer/cognirouter.py install --home ./.tmp-home --hosts all --no-upstream
```

## License

MIT for this repository. Upstream skills keep their own licenses.
