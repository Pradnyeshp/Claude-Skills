---
name: logging
description: Add or improve logging in a file or module — structured, leveled, contextual — using the project's existing logger, without leaking secrets or spamming. Use when the user says "add logging", "improve the logging", "add structured logs", "what should I log here", "set up a logger", or "add observability".
argument-hint: "[optional file/module/path to focus on, e.g. 'src/api/payments.ts']"
allowed-tools: Bash, Read, Edit, Grep, Glob
disable-model-invocation: false
---

## Logging setup signals

!`grep -rilE "winston|pino|bunyan|loguru|structlog|logging\\.getLogger|slf4j|zap|logrus|console\\.(log|error)" --include='*.*' . 2>/dev/null | grep -vE 'node_modules|\.git|dist|build|test' | head -15`

!`ls .env.example 2>/dev/null && grep -iE "LOG_LEVEL|LOG_FORMAT" .env.example 2>/dev/null`

## Instructions

Add or improve logging in `$ARGUMENTS` (or the highest-value paths — request entry points, jobs, error handlers, external calls — if none given). Use the project's existing logger and conventions; don't introduce a new logging library unprompted.

### Method

1. **Find the existing logger and pattern.** From the signals above, identify what the project uses (winston/pino, Python `logging`/structlog/loguru, zap/logrus, slf4j) and how it's configured — format (JSON vs text), levels, and any request/correlation context. Mirror it. If the code only uses `console.log`/bare `print`, propose adopting the real logger and confirm before a broad change.
2. **Log at the right boundaries, not everywhere.** Useful points: service/request entry and exit (with outcome + duration), external calls (API/DB/queue) and their failures, state transitions, retries, and caught errors. Don't log inside tight loops or on every trivial call — noisy logs hide signal.
3. **Use levels correctly:** `error` for failures needing attention, `warn` for recoverable/unexpected-but-handled, `info` for significant business events, `debug` for developer diagnostics. Don't log-and-rethrow the same error at every layer (double logging) — log it once where it's handled.
4. **Make logs structured and contextual.** Prefer key-value/structured fields (`logger.info('order placed', { orderId, userId })`) over string interpolation, so logs are queryable. Include identifiers that allow tracing a request end to end; reuse the project's correlation/request id if one exists.
5. **Keep messages clear and actionable** — state what happened and the relevant context, not just "error" or "here". Pair with the `error-handling` skill where logging and error flow intersect.

### Rules

1. **Never log secrets or sensitive data** — passwords, tokens, API keys, full card/PII, auth headers, request bodies that may contain them. Redact or omit; flag any existing log that leaks.
2. Use the project's logger and format; don't add a new dependency or a parallel logging style without asking.
3. Don't change program behavior — logging is additive. The only logic change allowed is removing a double-log or a secret leak, and say when you do.
4. Match levels to severity and avoid noise: no per-iteration logs, no `info` for routine debug detail, no duplicate logging of the same error up the stack.
5. Summarize what you added/changed, the levels used, any secrets you redacted, and anything that needs a config change (e.g. setting `LOG_LEVEL`).
