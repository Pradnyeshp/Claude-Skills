---
name: webhook
description: Securely receive and handle an inbound webhook from a third party (Stripe, GitHub, Shopify, etc.) — verify the signature, reject replays, acknowledge fast, and process idempotently — so forged or duplicated events can't harm the system. Use when the user says "handle this webhook", "verify a webhook signature", "add a Stripe/GitHub webhook endpoint", "secure my webhook", "my webhook fires twice", or "process incoming events from X".
argument-hint: "[the webhook to handle, e.g. 'the Stripe payment webhook' or 'POST /webhooks/github']"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
disable-model-invocation: false
---

## Provider, framework & signing signals

!`grep -rilE "webhook|stripe|svix|Webhook-Signature|X-Hub-Signature|X-Signature|hmac|createHmac|constant_time|express|fastify|nestjs|flask|fastapi|django" --include='*.*' package.json pyproject.toml go.mod Gemfile 2>/dev/null | grep -vE 'node_modules|\.git|dist|build' | head -8`

## Instructions

Wire up the inbound webhook in `$ARGUMENTS` so it only acts on authentic, non-replayed, deduplicated events. A webhook endpoint is public and attacker-reachable — treat every request as untrusted until the signature verifies. Reuse the project's framework and the provider's official SDK/verification helper where one exists.

### Method

1. **Verify the signature over the raw body.** Compute the HMAC (or use the provider's verify helper — e.g. Stripe's `constructEvent`, GitHub's `X-Hub-Signature-256`) using the signing secret, and compare with a **constant-time** comparison. Critically, verify against the **raw, unparsed request body** — many frameworks' JSON body parsers mutate bytes and break the signature, so capture the raw buffer before parsing for the webhook route only.
2. **Load the signing secret from config/env**, never hardcoded (see the `secrets-scan` skill). A missing secret should fail closed, not skip verification.
3. **Reject replays.** Check the signed timestamp (when the provider signs one) and reject requests outside a small tolerance (e.g. ±5 min) so a captured request can't be resent later.
4. **Acknowledge fast, process out of band.** Return `2xx` as soon as the event is verified and safely recorded; do the real work (DB writes, emails, downstream calls) asynchronously (queue/background job). Providers time out and retry aggressively — slow handlers cause duplicate deliveries and back-pressure.
5. **Process idempotently.** Providers deliver at-least-once, so the same event id will arrive more than once. Dedupe on the provider's event id before applying effects (see the `idempotency` skill). An unrecognized or unhandled event type should be acknowledged and ignored, not error.
6. **Return honest status codes.** `400` for a malformed/invalid signature, `2xx` for accepted (even if the event type is ignored). Don't return `2xx` on a signature failure, and don't `5xx` on events you simply don't handle — that triggers needless provider retries.
7. **Verify.** Add tests: a valid signed payload is accepted and processed once; a tampered body or wrong secret is rejected with `400`; a stale timestamp is rejected; the same event id delivered twice applies the effect once.

### Rules

1. Always verify the signature against the raw body with a constant-time compare before doing anything else; fail closed if the secret is missing.
2. Never trust or act on an unverified payload — parsing, logging PII, or side effects must come after verification.
3. Reject replays via the signed timestamp tolerance, and dedupe by event id so at-least-once delivery can't double-apply effects.
4. Acknowledge quickly with `2xx` and move heavy processing off the request path; reserve `4xx` for auth/validation failures and don't `5xx` on unhandled event types.
5. Keep the signing secret in config/env, and end by summarizing the verification method, replay/idempotency handling, the async processing path, and the status codes returned.
