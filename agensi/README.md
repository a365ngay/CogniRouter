# Agensi listings

Free skills published on [Agensi](https://www.agensi.io). Each folder is one skill in the SKILL.md format; it is not part of the CogniRouter bundle in `skills/`.

| Skill | Folder | Logo | Listing copy |
|---|---|---|---|
| User Story & Acceptance Criteria Writer | `user-story-writer/` | `docs/assets/agensi/user-story-writer-logo.png` | `listings/user-story-writer.md` |
| Test Case Generator | `test-case-generator/` | `docs/assets/agensi/test-case-generator-logo.png` | `listings/test-case-generator.md` |
| SQL Query Clinic | `sql-query-clinic/` | `docs/assets/agensi/sql-query-clinic-logo.png` | `listings/sql-query-clinic.md` |
| DB Migration Safety Reviewer | `db-migration-reviewer/` | `docs/assets/agensi/db-migration-reviewer-logo.png` | `listings/db-migration-reviewer.md` |
| Incident Postmortem | `incident-postmortem/` | `docs/assets/agensi/incident-postmortem-logo.png` | `listings/incident-postmortem.md` |

The user story and test case skills share one worked example (voucher at checkout): the story written by the first is the input of the second. The migration reviewer and postmortem examples tell the same story from both sides: an unsafe index build that locked a hot table.

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
