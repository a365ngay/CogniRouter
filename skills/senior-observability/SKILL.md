---
name: senior-observability
description: Use when designing, implementing, reviewing, or troubleshooting logging, metrics, tracing, dashboards, alerts, SLOs and error budgets, OpenTelemetry instrumentation, Prometheus, Grafana, ELK/Loki, incident investigation, on-call runbooks, or postmortems.
---

# Senior Observability

## Role

Make systems explainable in production: structured signals tied to user impact, alerts that are actionable, and evidence-driven incident analysis.

## Before Editing

1. Inspect the existing logging library and format, metrics stack (Prometheus, StatsD, cloud metrics), tracing (OpenTelemetry, vendor agents), dashboards, alert rules, SLO definitions, and runbooks.
2. Identify the user-facing behavior to observe and the questions an on-call engineer will need answered.

## Implementation Rules

- Log structured events (JSON or the project's format) with level, message, correlation/trace ID, and stable field names. Never log secrets, tokens, or unnecessary personal data.
- Instrument the RED signals for services (rate, errors, duration) and USE signals for resources (utilization, saturation, errors). Use histograms for latency, not averages.
- Keep metric label cardinality bounded; never use user IDs, URLs with IDs, or free text as labels.
- Propagate trace context across HTTP, messaging, and background jobs; name spans by operation, not by full URL.
- Alert on symptoms tied to SLOs (error rate, latency, burn rate), not on every cause. Every alert needs an owner, severity, and a runbook link.
- During incidents, gather evidence first (timeline, deploys, metrics, logs, traces), mitigate before root-causing, and record findings for a blameless postmortem.

## Testing and Verification

Trigger the changed path and confirm logs, metrics, and traces appear with the expected fields and labels. Validate alert rules (`promtool check rules` or equivalent) and check dashboards load with real data.

## Review Checklist

- Can an engineer answer "is it broken, for whom, and why" from these signals?
- Are labels low-cardinality and logs free of sensitive data?
- Is every alert actionable with a runbook?
- Are traces connected across service boundaries?
