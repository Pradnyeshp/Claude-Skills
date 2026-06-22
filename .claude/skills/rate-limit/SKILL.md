---
name: rate-limit
description: Add rate limiting / throttling to an endpoint or service — protecting against abuse, brute force, and overload — using the project's framework and a shared store where needed. Use when the user says "add rate limiting", "throttle this endpoint", "limit requests per user", "prevent brute force", "add a request quota", or "protect this API from abuse".
argument-hint: "[what to limit and the policy, e.g. 'login to 5/min per IP' or 'the public API to 100/min per key']"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
disable-model-invocation: false
---

## Framework & store signals

!`grep -rilE "express|fastify|koa|nestjs|flask|fastapi|django|gin|echo|rails|spring|express-rate-limit|slowapi|rack-attack" package.json pyproject.toml go.mod Gemfile 2>/dev/null | head`

!`grep -rilE "redis|memcached|ioredis" --include='*.*' package.json pyproject.toml 2>/dev/null | grep -vE 'node_modules|\.git' | head -5`

## Instructions

Add rate limiting for the target in `$ARGUMENTS`. If the policy (limit, window, and key) isn't given, propose sensible defaults for the use case and confirm. Match the project's framework and middleware style.

### Method

1. **Detect the framework and any shared store.** Use the idiomatic library (`express-rate-limit`, Fastify's rate-limit, NestJS throttler, `slowapi` for FastAPI, DRF throttling, `rack-attack` for Rails, a Gin/Echo middleware). Mirror how the project registers middleware.
2. **Choose the key — what is being limited.** Per IP (anonymous/login), per user or API key (authenticated), or per route. For login/abuse protection prefer a key that's hard to rotate (account + IP). Be careful behind a proxy/load balancer: read the real client IP from the trusted forwarded header, not the socket, or attackers/limits both break.
3. **Pick the policy and algorithm.** A window + max (e.g. 5/min) with a sliding-window or token-bucket algorithm for smooth limiting. Tighter on sensitive routes (auth, password reset, payment), looser on read-heavy public ones.
4. **Use a shared store for multi-instance deployments.** In-memory counters only work for a single process — if the app runs more than one instance/worker, back the limiter with Redis (or the existing store) so the limit is global, not per-process. Note this even if you default to in-memory for dev.
5. **Respond correctly when limited.** Return **429 Too Many Requests** with `Retry-After` and the standard `RateLimit-*` headers, and a safe message. Make sure failures of the limiter store fail open or closed deliberately (decide which, and say so) rather than crashing the request.

### Rules

1. Limit at the right key and read the client IP from the trusted proxy header when behind a load balancer — limiting on a proxy's IP throttles everyone together.
2. Use a shared store (Redis/etc.) when the service runs multiple instances; flag clearly if you leave an in-memory limiter that won't hold across processes.
3. Always return `429` with `Retry-After`/`RateLimit-*` headers — don't silently drop or use the wrong status.
4. Apply stricter limits to auth and other abuse-prone endpoints; don't apply one blanket limit that's either too loose for login or too tight for normal traffic.
5. Decide and state the store-failure behavior (fail open vs closed), and don't let the limiter itself become a crash or bottleneck. Summarize the policy, key, store, and headers after wiring it.
