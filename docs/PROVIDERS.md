# Using Skill Compass with different model providers

Skill Compass is installed into the **tool** (agent harness), not the model. Pick the tool you already use, point it at any model, and the routing behaves the same.

| You want to use | Recommended tool | Install with |
|---|---|---|
| Claude | Claude Code | `--hosts claude` |
| GPT / OpenAI | Codex CLI or app | `--hosts codex` |
| Gemini | Gemini CLI | `--hosts gemini` |
| Qwen | Qwen Code | `--hosts qwen` |
| GLM (Z.ai / Zhipu) | Claude Code with an Anthropic-compatible endpoint, or opencode | `--hosts glm` (= claude) or `--hosts opencode` |
| Kimi (Moonshot) | Claude Code with an Anthropic-compatible endpoint, or opencode | `--hosts kimi` (= claude) or `--hosts opencode` |
| DeepSeek | Claude Code with an Anthropic-compatible endpoint, or opencode | `--hosts deepseek` (= claude) or `--hosts opencode` |
| OpenRouter / Ollama / LM Studio / any OpenAI-compatible API | opencode | `--hosts opencode` |
| Cursor, GitHub Copilot, Windsurf, Zed, Amp, Jules | the editor itself (reads `AGENTS.md`) | `--project path/to/repo` |
| ChatGPT, GLM chat, Gemini app, Claude Projects (web) | custom instructions / project knowledge | `export` and paste the file |

## Claude Code with GLM, Kimi or DeepSeek

Several providers expose an Anthropic-compatible API, so Claude Code can run their models. Set the variables in your shell profile or in `~/.claude/settings.json` under `env`. Use the base URL from your provider's current documentation; typical values:

| Provider | `ANTHROPIC_BASE_URL` |
|---|---|
| Z.ai GLM (international) | `https://api.z.ai/api/anthropic` |
| Zhipu GLM (mainland China) | `https://open.bigmodel.cn/api/anthropic` |
| Moonshot Kimi | `https://api.moonshot.ai/anthropic` |
| DeepSeek | `https://api.deepseek.com/anthropic` |

```powershell
$env:ANTHROPIC_BASE_URL = "https://api.z.ai/api/anthropic"
$env:ANTHROPIC_AUTH_TOKEN = "<your key>"   # keep it in your secret store, never in this repo
claude
```

Then `python installer/compass.py install --hosts glm`. The block, skills and subagents are identical to a Claude install.

## Hosts without a native skill tool

The router block tells the model: if there is no skill tool, open `<skills dir>/<name>/SKILL.md` with the file-read tool. Any agent that can read files therefore gets the full routing. In a web chat (no file access), use `export --with-skills a,b,c` to inline the skills you use most; for anything else the model will ask you to paste the skill.

## Smaller or local models

The block is short and imperative on purpose. For models with a small context window:

- install with `--no-upstream` to keep the index short;
- trim the intent table in `core/NATURAL_LANGUAGE_ROUTING.md` to the stacks you use;
- prefer `--project` installs so only the relevant repository carries the block.
