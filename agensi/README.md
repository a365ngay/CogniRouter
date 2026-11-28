# Agensi listings

Free skills published on [Agensi](https://www.agensi.io). Each folder is one skill in the SKILL.md format; it is not part of the CogniRouter bundle in `skills/`.

| Skill | Folder | Logo | Listing copy |
|---|---|---|---|
| User Story & Acceptance Criteria Writer | `user-story-writer/` | `docs/assets/agensi/user-story-writer-logo.png` | `listings/user-story-writer.md` |
| Test Case Generator | `test-case-generator/` | `docs/assets/agensi/test-case-generator-logo.png` | `listings/test-case-generator.md` |

The two skills share one worked example (voucher at checkout): the story written by the first is the input of the second.

## Package

Agensi wants one zip per skill with a single top-level folder named after the skill and `SKILL.md` at its root.

```bash
python agensi/package.py            # writes dist/agensi/<skill>.zip for every skill folder
```

## Logos

Edit the SVG in `docs/assets/agensi/<skill>-logo.html`, then render a 512×512 transparent PNG, for example:

```bash
chrome --headless=new --hide-scrollbars --default-background-color=00000000 --window-size=512,512 --screenshot=<skill>-logo.png <skill>-logo.html
```
