---
name: security-headers
description: Add or harden HTTP security headers on a web app or API — Content-Security-Policy, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, and CORS — using the project's framework, to defend against XSS, clickjacking, and MIME sniffing. Use when the user says "add security headers", "set up CSP", "add HSTS", "configure CORS", "fix clickjacking", "harden the HTTP headers", or "pass a security headers scan".
argument-hint: "[optional: which headers or app to harden, e.g. 'add a CSP' or 'lock down CORS']"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
disable-model-invocation: false
---

## Framework & header signals

!`grep -rilE "express|fastify|koa|nestjs|next\\.config|helmet|flask|fastapi|django|secure\\.py|rails|spring|nginx|cors|csp|content-security-policy|strict-transport" --include='*.*' package.json pyproject.toml go.mod Gemfile next.config.* nginx.conf 2>/dev/null | grep -vE 'node_modules|\.git|dist|build' | head -10`

## Instructions

Add or harden security headers for the app in `$ARGUMENTS` (or the whole app if unspecified). Match the project's framework and where it currently sets headers. CSP and CORS can break a working app if set wrong, so apply them carefully and explain what each does.

### Method

1. **Find where headers are set today.** Look for an existing middleware (`helmet`, `django-csp`, Rails `default_headers`, a reverse-proxy config) and extend it rather than adding a second, conflicting source. Prefer the idiomatic library (`helmet` for Express/Fastify, `secure` for FastAPI/Flask, Spring Security headers) over hand-setting strings.
2. **Set the low-risk headers first.** `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY` (or a frame-ancestors CSP), `Referrer-Policy: strict-origin-when-cross-origin`, and `Strict-Transport-Security` with a sane `max-age` (only once HTTPS is fully in place — HSTS is sticky and hard to undo). These rarely break anything.
3. **Build a Content-Security-Policy deliberately.** This is the highest-value and highest-risk header. Start from `default-src 'self'`, then add only the origins the app genuinely loads from (scripts, styles, images, fonts, connect/XHR). Avoid `unsafe-inline`/`unsafe-eval` — prefer nonces/hashes. Offer to deploy it as `Content-Security-Policy-Report-Only` first so violations are reported without breaking the page.
4. **Lock down CORS to an allowlist.** Never reflect arbitrary origins or pair `Access-Control-Allow-Origin: *` with credentials. Allow only the specific trusted origins, the methods/headers actually used, and set `Allow-Credentials` only when cookies/auth truly cross origins.
5. **Verify before declaring done.** Note how to check (curl `-I`, a securityheaders.com-style scan, browser console for CSP violations) and confirm the app still loads — no blocked scripts/styles, no CORS errors in the console.

### Rules

1. Don't break the running app: CSP and CORS misconfigured will block legitimate assets or requests — prefer CSP report-only first and an explicit CORS allowlist, and verify the app still works.
2. Never set `Access-Control-Allow-Origin: *` together with credentials, and never reflect the request origin without validating it against an allowlist.
3. Avoid `unsafe-inline`/`unsafe-eval` in CSP; use `'self'`, nonces, or hashes, and scope each directive to the origins actually used.
4. Only enable HSTS once HTTPS is fully working (it's hard to roll back), and extend the project's existing header mechanism instead of adding a conflicting second one.
5. After applying, summarize each header set, the CSP/CORS policy, whether CSP is report-only, and how to verify the headers and that nothing broke.
