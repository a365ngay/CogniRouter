---
name: senior-docker
description: Use when writing, reviewing, debugging, or optimizing Dockerfiles, multi-stage builds, image size and layer caching, docker compose stacks, container networking and volumes, health checks, image security and scanning, or local development containers.
---

# Senior Docker

## Role

Produce small, reproducible, secure images and compose setups that build fast from cache and behave the same locally and in CI.

## Before Editing

1. Inspect the existing Dockerfiles, `.dockerignore`, compose files, base images and tags, build args, entrypoints, registry, and how CI builds and tags images.
2. Identify the runtime needs: ports, env vars, volumes, health endpoint, user, and signals.

## Implementation Rules

- Pin base images to a specific version (and digest where the project does); prefer slim or distroless runtime images.
- Use multi-stage builds: compile and install dev dependencies in a builder stage, copy only artifacts into the runtime stage.
- Order layers for caching: copy dependency manifests and install before copying source. Keep a strict `.dockerignore` (`.git`, `node_modules`, secrets, build output).
- Run as a non-root user, drop unneeded packages, and never bake secrets into layers or build args; use build secrets (`--mount=type=secret`) or runtime injection.
- Use exec-form `ENTRYPOINT`/`CMD` so the process receives signals; handle `SIGTERM` for graceful shutdown. Add a `HEALTHCHECK` or orchestrator probe.
- In compose, use named volumes, explicit networks, `depends_on` with health conditions, and env files that are git-ignored.

## Testing and Verification

Build with the project's command, run the container and hit its health endpoint, check image size (`docker images`, `docker history`), and scan with the project's scanner (Trivy, Grype, Docker Scout) when available.

## Review Checklist

- Is the image pinned, minimal, and running as non-root?
- Are secrets absent from layers, args, and logs?
- Does the cache order make rebuilds fast?
- Does the container shut down gracefully and report health?
