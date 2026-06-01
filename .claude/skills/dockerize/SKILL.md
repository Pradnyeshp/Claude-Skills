---
name: dockerize
description: Generate a production-ready Dockerfile, .dockerignore, and optional docker-compose for the project, matching its language and build setup. Use when the user says "dockerize this", "write a Dockerfile", "containerize the app", "add docker-compose", or "how do I run this in a container".
argument-hint: "[optional: target service, base image, or 'compose' to include docker-compose]"
allowed-tools: Bash, Read, Write, Glob, Grep
disable-model-invocation: false
---

## Project type detection

!`ls package.json pyproject.toml requirements.txt Cargo.toml go.mod pom.xml build.gradle Gemfile composer.json 2>/dev/null`

!`ls Dockerfile .dockerignore docker-compose.yml docker-compose.yaml compose.yaml 2>/dev/null && echo "(existing docker files above — update, don't blindly overwrite)"`

!`cat package.json 2>/dev/null | head -40`

## Instructions

Generate Docker assets for this project (scoped to `$ARGUMENTS` if a service or base image was named).

### Rules

1. **Detect the stack first.** Infer language, runtime version, package manager, build step, and start command from the files above and lockfiles. Match the actual versions in use — don't pin to `latest`.
2. **Use a multi-stage build** for compiled languages and for any project with a build step (install deps + build in one stage, copy only artifacts into a slim runtime stage). This keeps the final image small.
3. **Pick a minimal, pinned base image** (e.g. `node:22-slim`, `python:3.12-slim`, `golang:1.23` → `gcr.io/distroless` or `alpine` runtime). State why.
4. **Follow security best practices:** run as a non-root user, don't bake secrets into layers, copy lockfiles and install deps before copying source (to maximize layer caching), and use `--no-install-recommends` / `--frozen-lockfile` style flags.
5. **Write a matching `.dockerignore`** — exclude `node_modules`, `.git`, build output, env files, and local caches so the build context stays small.
6. **Expose the right port** and set a sensible `CMD`/`ENTRYPOINT`. Add a `HEALTHCHECK` when the service has an HTTP endpoint.
7. **Generate `docker-compose.yml` only if** the user asks, or the project clearly needs companion services (a database, cache, queue). Wire env vars and volumes; don't invent services that aren't referenced in the code or config.
8. If an existing Dockerfile is present, read it and propose targeted edits rather than replacing it wholesale.
9. After writing, print the exact `docker build` and `docker run` (or `docker compose up`) commands to build and run it.
