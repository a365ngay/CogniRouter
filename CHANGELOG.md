# Changelog

## Unreleased

- `ba-srs-builder` is no longer bundled (51 bundled skills).

## 1.1.0 - 2026-11-26

- 22 new bundled skills (52 total):
  - Stacks: `senior-react`, `senior-vue`, `senior-react-native`, `senior-nodejs`, `senior-java-spring`, `senior-dotnet`, `senior-go`, `senior-python-backend`, `senior-mysql`, `senior-mongodb`, `senior-redis`.
  - DevOps & security: `senior-docker`, `senior-cicd`, `senior-terraform`, `senior-observability`, `senior-security`.
  - Engineering practice: `senior-code-review`, `senior-refactoring`, `senior-api-design`, `senior-performance`, `senior-technical-writing`, `senior-git-workflow`.
- New upstream skills from anthropics/skills (Apache-2.0, same pinned commit): `webapp-testing`, `mcp-builder`, `skill-creator`, `docx`, `xlsx`, `pdf`, `pptx`.
- Routing table covers every new skill; Python web backends route to `senior-python-backend`.
- Python 3.8 support fixed in the installer; CI runs Python 3.8 on `ubuntu-24.04`.

## 1.0.0 - 2026-11-26

- Project name: CogniRouter.

- Provider-neutral routing core (`core/ROUTER.md`, `NATURAL_LANGUAGE_ROUTING.md`, orchestration, routing and safety policies).
- 30 bundled skills: senior engineering roles, stack standards, executor skills, `ba-srs-builder`, `professional-slides`, `jira-ba-dev-test-flow`.
- Five Claude Code subagents (`senior-work-*`).
- Installer for Claude Code, Codex, Gemini CLI, Qwen Code, opencode, plus per-project `AGENTS.md` mode and a single-file export for web chats.
- Third-party skills fetched at pinned commits (`upstream.lock.json`), symlinks resolved for Windows.
