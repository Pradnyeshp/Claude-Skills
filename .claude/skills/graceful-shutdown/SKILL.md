---
name: graceful-shutdown
description: Make a service shut down cleanly on SIGTERM/SIGINT — stop accepting new work, drain in-flight requests, close DB/queue connections, and exit within the platform's grace period — so deploys and restarts don't drop requests or corrupt state. Use when the user says "add graceful shutdown", "handle SIGTERM", "drain connections on shutdown", "stop dropping requests during deploys", "close connections cleanly on exit", or "my app is killed mid-request".
argument-hint: "[optional entrypoint or server to make shutdown-safe, e.g. 'the Express server' or 'main.py']"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
disable-model-invocation: false
---

## Runtime, server & signal signals

!`grep -rilE "SIGTERM|SIGINT|process\\.on|signal\\.|shutdown|http\\.Server|createServer|express|fastify|nestjs|flask|fastapi|gunicorn|uvicorn|listen\\(|graceful" --include='*.*' package.json pyproject.toml go.mod Gemfile 2>/dev/null | grep -vE 'node_modules|\.git|dist|build' | head -8`

## Instructions

Make the service in `$ARGUMENTS` (or the app's entrypoint) terminate cleanly when the platform sends a shutdown signal, so an in-flight request is finished rather than severed and external resources are released. Reuse the project's server and connection objects rather than introducing a new lifecycle framework.

### Method

1. **Handle the right signals.** Trap `SIGTERM` (what Kubernetes/Docker/systemd send) and `SIGINT` (Ctrl-C in dev). Run the shutdown routine once and guard against re-entry if a second signal arrives.
2. **Stop accepting new work first.** Close the listening socket / stop the HTTP server from taking new connections, and if the app pulls from a queue, stop consuming. Existing in-flight requests keep running; new ones are refused (or shed to another instance).
3. **Fail readiness immediately.** Flip the readiness probe to unhealthy at the start of shutdown so the load balancer / orchestrator stops routing new traffic before the socket closes (see the `healthcheck` skill). In Kubernetes, expect traffic for a moment after SIGTERM — a short pre-drain delay avoids races.
4. **Drain in-flight work with a bounded timeout.** Wait for active requests/jobs to complete, but cap the wait (e.g. 10–30s, comfortably under the platform's kill grace period). If work exceeds the deadline, log what's still pending and proceed — never block forever.
5. **Release resources in dependency order.** After draining, close DB pools, cache/queue clients, and file handles, and flush logs/metrics/traces. Close what depends on the network before the things it depends on.
6. **Exit with an honest code.** `exit(0)` on a clean drain; a non-zero code if shutdown timed out or errored. Don't leave the process hanging — the platform will `SIGKILL` it and undo the graceful intent.
7. **Verify.** Test that sending SIGTERM while a slow request is in flight lets that request finish and returns before exit, that new connections are refused during drain, and that the process exits within the deadline.

### Rules

1. Trap SIGTERM (and SIGINT for dev), make the handler idempotent, and never let a second signal trigger a second concurrent shutdown.
2. Stop new work and fail readiness before closing the socket, so the balancer drains traffic first; then drain in-flight requests.
3. Always bound the drain with a timeout under the platform's kill grace period — drain, but never block shutdown indefinitely.
4. Close DB/queue/cache connections and flush telemetry after draining, in dependency order, then exit with a status code that reflects success or timeout.
5. End by summarizing which signals are handled, the drain timeout and how it relates to the platform grace period, the readiness behavior, and what gets closed on the way out.
