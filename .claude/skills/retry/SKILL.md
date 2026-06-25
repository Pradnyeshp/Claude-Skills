---
name: retry
description: Add retry-with-backoff to a flaky external call — a network request, database query, or third-party API — so transient failures recover instead of surfacing as errors, using the project's existing HTTP/client stack. Use when the user says "add a retry", "retry on failure", "add exponential backoff", "make this resilient to flaky network", "handle transient errors", or "this call fails intermittently".
argument-hint: "[the call to make resilient, e.g. 'the payment API client' or 'the fetchUser request']"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
disable-model-invocation: false
---

## Client & retry-library signals

!`grep -rilE "axios|got|node-fetch|undici|ky|retry|p-retry|tenacity|backoff|resilience4j|polly|retryablehttp|httpx|requests" --include='*.*' package.json pyproject.toml go.mod Gemfile pom.xml 2>/dev/null | grep -vE 'node_modules|\.git|dist|build' | head -8`

## Instructions

Make the call in `$ARGUMENTS` resilient to transient failures. If it's unclear which call is flaky or what its idempotency guarantees are, ask before wrapping it — retrying the wrong operation can double-charge or double-write. Reuse the project's existing client and any retry helper already present.

### Method

1. **Confirm the operation is safe to retry.** Only retry idempotent operations (GETs, reads, PUT/DELETE by id, or writes protected by an idempotency key). Retrying a non-idempotent POST (charge, send, create-without-key) can duplicate the effect — flag that and either skip retry or add an idempotency key first.
2. **Retry only transient, retryable failures.** Network timeouts, connection resets, `429`, and `5xx` are retryable. `4xx` (bad request, auth, not found) are not — retrying them just wastes time and hammers the dependency. Match on those specifically rather than retrying every exception.
3. **Use exponential backoff with jitter.** Space attempts out (e.g. 100ms, 200ms, 400ms…) with random jitter so concurrent clients don't retry in lockstep and create a thundering herd. Honor a `Retry-After` header when the response provides one.
4. **Bound the retries.** Cap attempts (typically 3–5) and the total elapsed time so a failing dependency surfaces an error promptly instead of hanging the request. Pair with a sensible per-attempt timeout. Mention a circuit breaker if the project already has one or the call is hot.
5. **Make it observable and reuse infra.** Prefer the project's existing retry helper (`p-retry`, axios-retry, `tenacity`, resilience4j, Polly) over a hand-rolled loop. Log/trace retry attempts so flakiness is visible, and let the final failure propagate cleanly after retries are exhausted.

### Rules

1. Retry only idempotent operations; for non-idempotent writes, add an idempotency key first or don't retry — never risk a duplicate side effect silently.
2. Retry only transient/retryable errors (timeouts, `429`, `5xx`); never retry `4xx` or programming errors.
3. Always use bounded attempts plus exponential backoff with jitter and a total deadline — no unbounded or fixed-interval retry loops.
4. Honor `Retry-After`, reuse the project's retry library and client, and make attempts observable rather than silent.
5. After wiring, summarize what's retried, the retryable conditions, the backoff/jitter and attempt cap, and the idempotency assumption you relied on.
