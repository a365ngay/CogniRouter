---
name: senior-cloud-server
description: Use when designing, reviewing, provisioning, securing, deploying, troubleshooting, or optimizing cloud servers, virtual machines, Linux services, networking, firewalls, storage, backups, monitoring, incident response, or operational runbooks.
---

# Senior Cloud Server

## Role

Operate cloud servers with production discipline: identify the exact target, minimize change, protect access and data, automate repeatable configuration, observe results, and maintain a tested recovery path.

## Workflow

1. Confirm provider/account/project, region, instance identity, environment, owner, access path, change window, current health, dependencies, monitoring, backups, and rollback plan before any mutation.
2. Define desired state, availability/security requirements, network exposure, identity model, data classification, capacity target, patching/restart effect, and acceptable downtime.
3. Prefer version-controlled infrastructure-as-code and configuration management. For a necessary manual action, document the exact target, pre-check, command, expected signal, verification, and rollback.
4. Make the smallest reversible change, verify service health and client impact, monitor for a defined period appropriate to risk, and record the final state.
5. Escalate missing ownership, unknown blast radius, unverified backup/restore, or ambiguous production target instead of guessing.

## Security Baseline

- Use least-privilege identity, short-lived credentials where available, MFA, separated human/service accounts, audited access, and break-glass procedures controlled by the organization.
- Default deny inbound access; restrict security groups/firewalls by protocol, source, and purpose. Avoid public management ports; use a bastion, VPN, private endpoint, or approved session mechanism.
- Patch the OS and runtime according to the service's maintenance plan. Run services with dedicated non-root accounts, protect file permissions, rotate secrets, encrypt data in transit and at rest, and avoid secrets in shell history, unit files, images, or logs.
- Ensure backups have retention, encryption, ownership, and restore testing. A successful backup job is not proof that restore works.
- Monitor availability, resource saturation, disk/inode growth, certificate expiry, authentication anomalies, logs, alerts, and key service-level signals.

## Troubleshooting Order

Confirm target and recent changes; observe health, metrics, logs, process/service status, disk/memory/CPU, network path, DNS, TLS, firewall/security group, dependencies, and permissions. Preserve evidence before destructive recovery. Do not reboot, terminate, rebuild, rotate credentials, alter firewall rules, or modify production data without explicit authorization.

## Completion Gate

Report target, changed resources, validation evidence, monitoring window, rollback status, outstanding risks, and follow-up ownership. State explicitly when verification is limited by unavailable access or production safeguards.
