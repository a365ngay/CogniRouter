---
name: incident-postmortem
description: "Turns messy incident material (Slack or Teams threads, alert and deploy logs, on-call notes, timelines, ticket exports) into a blameless postmortem: one-time-zone timeline with sources, quantified impact, detection and response metrics (time to detect, mitigate, resolve), trigger vs root cause vs contributing factors, what went well and where you got lucky, and specific action items with owner, due date and type. Also reviews an existing postmortem for blame, vague actions and missing impact, and writes customer-facing incident summaries or status page updates. Use whenever someone shares an incident thread or notes, asks for a postmortem, post-incident review, RCA, incident report, 5 whys, retrospective of an outage, or a status page or customer message about an outage. Works in any language and answers in the user's language."
---

# Incident Postmortem

Produce a postmortem the team can learn from in a 30-minute review: accurate facts, a clear causal story, and a short list of actions that will actually change something. Blameless means the document explains why the system made the failure easy, not who to blame.

## Pick the mode

| The user gives you | Mode |
|---|---|
| Raw material: chat export, alerts, notes, logs | **Draft**: full postmortem |
| An existing postmortem | **Review**: findings ranked, then rewritten weak sections |
| "Write the status page update / customer email" | **Customer summary**: short external text (see `references/template.md`) |
| An ongoing incident, "summarize where we are" | **Status update**: current impact, what is known, next step, next update time; no root cause speculation |

## Workflow (Draft)

1. **Collect facts** from everything given. Keep a source for each fact (message time and channel, alert name, log line, deploy ID). Never invent a time, number, cause or quote; put unknowns in **Open questions**.
2. **Normalize time.** One time zone for the whole document (say which; add UTC if the team spans zones). Convert relative or mixed timestamps. When a speaker corrects themselves ("9:40… no, 16:40") use the corrected value and note it; when a relative date conflicts with the message time ("yesterday" said during the incident), use the most consistent reading and list the doubt in **Open questions**.
3. **Build the timeline**: start of impact, detection, key decisions, mitigation, resolution, and the events before impact that caused it (deploy, config change, traffic spike). For decisions, write what was known then in the event text ("scaled Redis; evictions not yet confirmed"). Rows you inferred rather than read get the source `derived: <from what>` and `~` on the time.
4. **Quantify impact**: who and what was affected, for how long, how much (failed requests, users, orders, revenue, SLO error budget used, support tickets). Give the calculation; label estimates. If a number is missing, say how to get it.
5. **Compute response metrics** from the timeline: time to detect (impact start → first signal), time to acknowledge, time to first mitigating action, time to mitigate (impact start → impact stopped), time to resolve. If impact start is unknown, use the earliest evidence (trigger time or first signal), say which, and mark the metrics `~`. Name the longest gap; give its reason only if the input supports it, otherwise mark it unconfirmed and add an open question.
6. **Explain causes** with `references/analysis.md`: the **trigger** (what changed), the **root cause(s)** (why that change could hurt), the **contributing factors** (why defenses such as review, tests, staging, alerts, runbooks, rate limits did not stop or shorten it). Label each cause **Confirmed** (evidence given), **Likely** (strong correlation) or **Hypothesis** (to verify), and when it is not confirmed add an action to verify it. Use a 5-whys chain or a short causal tree; there is rarely one root cause.
7. **What went well, what went wrong, where we got lucky.** Luck matters: it is a risk that has not been paid for yet.
8. **Action items** with `references/action-items.md`: each one tied to a cause or factor, specific and verifiable, typed (prevent / detect / mitigate / process), prioritized, with owner and due date. Prefer a few strong actions over many weak ones. If the input already proposes a weak action ("tell marketing to warn us"), keep its intent and rewrite it into an enforceable form, saying so.
9. **Write it** with `references/template.md`, in blameless language (`references/analysis.md`, last section). People appear by role (on-call engineer, incident commander, DBA) unless the user asks for names. Write headings, labels and prose in the user's language; keep technical identifiers (metric names, commands, service names) as they are.

## Quality gates

- Every timeline row has a time and a source; every number has a source or a stated calculation.
- No blame words or hindsight phrasing ("careless", "failed to", "should have known", "human error" as a cause). Rewrite as conditions and decisions given what was known.
- Trigger, root cause and contributing factors are separate; "a bad deploy" is a trigger, not a root cause.
- Every action item maps to at least one cause or factor, and every major factor has an action item or an explicit "accepted risk".
- Action items are things a team can finish and verify ("add `lock_timeout=5s` to the migration runner and a CI check for non-concurrent index builds"), not wishes ("be more careful", "improve monitoring").
- Severity uses the user's scale if given; otherwise propose one with this default and say so: SEV1 = core service down or data loss for most users; SEV2 = a major function failing or badly degraded for many users; SEV3 = minor or limited impact.
- Causes that are not confirmed are labeled, never written as fact.
- External texts (status page, customer email) contain no internal names, blame, unverified causes or promises of dates you were not given.

## Review mode checklist

Missing or unquantified impact; timeline without sources or with gaps during the impact window; root cause that stops at a person or at "bug in code"; no contributing factors about detection and response; action items without owners or dates, duplicated, or not linked to causes; blame or hindsight language; customer impact described only from the system's view.

## References (read only what the task needs)

- `references/template.md`: full postmortem template, status update and customer summary templates.
- `references/analysis.md`: trigger vs root cause vs factors, 5 whys done well, factor categories, blameless rewrites.
- `references/action-items.md`: good vs weak actions, types, priority, ownership.
- `examples/checkout-index-lock.md`: Slack thread → complete postmortem.
