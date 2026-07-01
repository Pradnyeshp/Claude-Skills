---
name: idempotency
description: Make a write endpoint or operation safe to retry by adding idempotency keys — so a duplicate request (from a client retry, double-click, or network timeout) produces one effect, not two. Use when the user says "add idempotency", "make this endpoint idempotent", "prevent duplicate charges", "add an idempotency key", "deduplicate requests", "handle double submits", or "this can be called twice and double-writes".
argument-hint: "[the endpoint or operation to make idempotent, e.g. 'POST /payments' or 'the createOrder handler']"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
disable-model-invocation: false
---

## Framework, store & existing idempotency signals

!`grep -rilE "idempoten|Idempotency-Key|dedup|express|fastify|nestjs|flask|fastapi|django|redis|prisma|sequelize|sqlalchemy|typeorm" --include='*.*' package.json pyproject.toml go.mod Gemfile 2>/dev/null | grep -vE 'node_modules|\.git|dist|build' | head -8`

## Instructions

Make the operation in `$ARGUMENTS` safe to execute more than once with the same input, so retries and double-submits don't create duplicate side effects (a second charge, a second order, a second email). Reuse the project's existing web framework and datastore rather than introducing new infrastructure.

### Method

1. **Decide whether a key is even needed.** Naturally idempotent operations (GET, PUT/DELETE by id, upserts keyed on a unique column) may already be safe — a `UNIQUE` constraint on a natural key is often the simplest fix. Reach for an idempotency key when the operation is a non-idempotent POST with real side effects (payments, orders, sends).
2. **Accept a client-supplied key.** Read an `Idempotency-Key` header (or a body field for internal callers). The client generates a stable UUID per logical operation and reuses it across retries. Validate it's present and well-formed for the endpoints that require it.
3. **Persist request → response, atomically.** On first request, insert the key with a status of `in-progress` inside the **same transaction** as the side effect (or use an atomic `INSERT ... ON CONFLICT DO NOTHING` / `SETNX`). Store the eventual response (status + body) against the key so a replay can return it verbatim.
4. **Handle the replay paths:**
   - **Completed key** → return the stored response with the original status code; do **not** re-run the side effect.
   - **In-progress key** (concurrent duplicate still running) → return `409 Conflict` or have the client back off, rather than racing a second execution.
   - **Same key, different request body** → reject with `422`; a key must map to exactly one request payload, or a client bug could mask a real second operation.
5. **Bound retention.** Keep keys long enough to cover realistic client retry windows (commonly 24h–7d) and expire them (TTL in Redis, or a `created_at` + sweep for SQL). Say what window you chose and why.
6. **Verify.** Add/adjust a test that fires the same request twice with one key and asserts a single side effect plus identical responses, and a test that a different body under the same key is rejected.

### Rules

1. The side effect and the key record must commit together — never write the effect first and the key second, or a crash between them defeats the guarantee. Use one transaction or an atomic insert.
2. A replay of a completed key must return the stored response and must not re-execute the side effect; an in-progress duplicate must not run concurrently.
3. Bind a key to its request payload — reject a reused key with a different body rather than silently returning the old response.
4. Reuse the project's datastore for key storage and set a TTL/retention window; don't let the key table grow unbounded.
5. End by summarizing which operations are now idempotent, the header/field used, the store and retention window, and the replay behavior for completed / in-progress / mismatched requests. Cross-reference the `retry` skill, since safe client retries depend on this.
