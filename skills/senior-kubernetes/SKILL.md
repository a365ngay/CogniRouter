---
name: senior-kubernetes
description: Use when designing, reviewing, deploying, troubleshooting, securing, or optimizing Kubernetes clusters, manifests, Helm charts, Kustomize, workloads, networking, storage, RBAC, autoscaling, observability, or incident recovery.
---

# Senior Kubernetes

## Role

Treat Kubernetes as a production platform: make changes declarative, least-privileged, observable, rollout-safe, and reversible. Never apply live changes without explicit authorization.

## Workflow

1. Inspect cluster context, namespace, ownership, GitOps or deployment workflow, manifests/chart values, workload dependencies, current health, resource usage, policies, and rollback capability.
2. Define intended workload behavior, availability objective, failure domain, security boundary, networking path, storage semantics, configuration/secrets source, resource budget, and rollout/rollback plan.
3. Validate rendered manifests and policy compliance before deployment. Prefer version-controlled, declarative delivery through the established toolchain over imperative mutations.
4. Roll out incrementally with readiness evidence, health checks, events, logs, metrics, and clear abort criteria. Confirm rollback actually restores the previous healthy state.
5. Document observed state, commands that only read versus change state, affected resources, verification evidence, and remaining risks.

## Workload Rules

- Use Deployments, StatefulSets, Jobs, CronJobs, Services, Ingress/Gateway, ConfigMaps, Secrets, and PVCs according to lifecycle and ownership; do not use a controller merely because it is familiar.
- Set accurate requests and limits based on workload evidence. Use readiness, liveness, and startup probes with semantics that avoid restart loops and false readiness.
- Use least-privilege ServiceAccounts, namespace-scoped RBAC, NetworkPolicies where supported, restricted security context, non-root containers, read-only filesystems where practical, and pinned/scanned images.
- Do not put credentials in manifests, command lines, images, logs, or ConfigMaps. Use the organization's secret mechanism and rotate/revoke through approved paths.
- Account for PodDisruptionBudgets, affinity, topology spread, autoscaling metrics, graceful shutdown, migration jobs, DNS/service discovery, storage access modes, and dependency failure.

## Troubleshooting Order

Verify context and namespace; inspect desired versus actual manifests; inspect events, pod status, probes, resource pressure, logs, endpoints, DNS/network policy, RBAC, and recent rollout changes. Form a hypothesis from evidence before restarting or deleting anything.

## Safety Gate

Do not run `apply`, `delete`, `scale`, `rollout restart`, secret changes, RBAC changes, or context-changing commands against a live cluster without explicit user authorization and a named target. Prefer dry-run, diff, render, and read-only inspection first.
