---
name: healthcheck
description: Add health, readiness, and liveness check endpoints to a service — verifying dependencies (db, cache, queues) — matching the project's framework, for load balancers and orchestrators. Use when the user says "add a health check", "add a /health endpoint", "add readiness/liveness probes", "health endpoint for Kubernetes", or "how do I check if the service is up".
argument-hint: "[optional: which checks or path, e.g. 'check the db and redis' or '/healthz']"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
disable-model-invocation: false
---

## Service & dependency signals

!`grep -rilE "express|fastify|koa|nestjs|flask|fastapi|django|gin|echo|actix|rails|spring" package.json pyproject.toml go.mod Gemfile 2>/dev/null | head`

!`grep -rilE "createConnection|DataSource|pg|mongoose|redis|prisma|sqlalchemy|database_url" --include='*.*' . 2>/dev/null | grep -vE 'node_modules|\.git|dist|build|test' | head -8`

## Instructions

Add health check endpoint(s) to this service per `$ARGUMENTS`. Match the project's framework and how it registers routes — don't introduce a new server or router.

### Method

1. **Detect the framework and an existing route** to copy registration style, middleware, and conventions (Express/Fastify/Nest, Flask/FastAPI/Django, Gin/Echo, Rails, Spring). Mirror it.
2. **Distinguish liveness from readiness** — they answer different questions, so prefer two endpoints:
   - **Liveness** (`/livez` or `/health`) — is the process up? Cheap, no dependency calls; returns 200 unless the process is broken. Orchestrators restart on failure, so it must not fail just because a dependency is down.
   - **Readiness** (`/readyz` or `/health/ready`) — can it serve traffic *right now*? Checks critical dependencies (db, cache, queue, required downstreams) and returns 503 when any is unavailable so the load balancer stops routing to it.
3. **Check real dependencies, cheaply.** Use a lightweight probe per dependency (`SELECT 1`, a Redis `PING`, a fast head request) with a short timeout so a hung dependency can't hang the check. Run them concurrently where the language makes it easy.
4. **Return a useful, safe body.** A JSON payload with overall status and per-dependency `up`/`down` + latency aids debugging — but don't leak connection strings, credentials, internal hostnames, or versions to an unauthenticated endpoint. Set the right status code (200 healthy / 503 not ready) since probes key on it.
5. **Wire it up** following the project's routing, and note any config (the path, whether it should bypass auth/rate-limiting, the orchestrator probe settings to point at it).

### Rules

1. Liveness must not depend on external services — tying it to the db means a db blip triggers pointless restarts. Keep dependency checks in readiness.
2. Every dependency probe needs a timeout; a health check that can hang is worse than none.
3. Don't leak sensitive detail (secrets, internal topology, exact versions) in the response or expose an internal-only check publicly without auth.
4. Reuse the app's existing db/cache clients and config — don't open new connections per request or hardcode endpoints.
5. After adding, summarize the endpoints, what each checks, the status codes, and the probe configuration to use (e.g. Kubernetes `livenessProbe`/`readinessProbe`).
