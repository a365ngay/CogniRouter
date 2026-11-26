# MCP destinations (local, never commit)

Copy this file to `MCP_DESTINATIONS.md` in the same folder (`~/.skill-compass/local/`) and fill in your own systems. The router reads it before touching an external system. `local/*.md` (except `*.example.md`) is ignored by Git.

Put **names and hosts only** here. Tokens and passwords stay in the MCP server's own config or your OS secret store.

## Destinations

| Destination (host) | Purpose | Server name per host |
|---|---|---|
| jira.example.com | Company Jira | claude: `jira-company` · codex: `jira_company` |
| wiki.example.com | Confluence | claude: `wiki_company` · codex: `wiki_company` |
| gitlab.example.com | GitLab | `gitlab` |

## Capability connectors (optional)

| Intent | Preferred | Fallback for read-only work |
|---|---|---|
| Web search | built-in web search | browser page text |
| Read a URL | built-in fetch | browser page text → Playwright |
| Browser UI test | Playwright MCP | built-in browser |

## Rules

- If a request names a host that is not in the table, ask before writing anything.
- Never fall back to another server for a failed write.
