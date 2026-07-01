---
name: audit-log
description: Add an audit trail that records who did what, when, and to what — for security-sensitive and compliance-relevant actions (logins, permission changes, data mutations, admin operations) — in an append-only, tamper-evident, PII-conscious way. Use when the user says "add an audit log", "track who changed what", "add an audit trail", "record admin actions", "who did this and when", "add compliance logging", or "log security-sensitive events".
argument-hint: "[the action or area to audit, e.g. 'permission changes' or 'the admin user endpoints']"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
disable-model-invocation: false
---

## Logger, ORM & auth signals

!`grep -rilE "audit|logger|winston|pino|bunyan|structlog|logging|prisma|sequelize|typeorm|sqlalchemy|django|auth|currentUser|req\\.user" --include='*.*' package.json pyproject.toml go.mod Gemfile 2>/dev/null | grep -vE 'node_modules|\.git|dist|build' | head -8`

## Instructions

Add an audit trail for the actions in `$ARGUMENTS`. An audit log is a security/compliance record, distinct from debug logging: it must reliably capture *who did what to what, when* for sensitive operations, and be trustworthy after the fact. Reuse the project's datastore and request/auth context.

### Method

1. **Identify the auditable events.** Focus on security- and compliance-relevant actions, not everything: authentication (login success/failure, logout, MFA), authorization changes (role/permission grants, ownership transfers), sensitive data mutations (create/update/delete of protected records), and privileged/admin operations. Reads usually aren't audited unless the data is regulated.
2. **Capture a complete, structured record per event:** the **actor** (user id + a stable identifier, not just a display name), the **action** (a stable verb like `user.role.granted`), the **target** (entity type + id), a **timestamp** (UTC), the **outcome** (success/failure), and useful **context** (source IP, request id, before/after for changes). Use a consistent schema so the log is queryable.
3. **Write to an append-only, separate store.** Persist audit entries to a dedicated table/stream that the application only ever inserts into — no updates or deletes from app code. Keep it separate from ordinary application logs so retention, access, and integrity can be controlled independently. For stronger tamper-evidence, consider hash-chaining entries or shipping to write-once/external storage.
4. **Record reliably and in context.** Write the audit entry as close to the action as possible — ideally in the same transaction as the state change so a committed change is never missing its audit record (and a rolled-back one leaves no false entry). Emit on **failed** attempts too (e.g. denied permission changes), since those matter most for security.
5. **Protect sensitive data.** Never write secrets, passwords, tokens, or full card/PII into the audit record — store identifiers and redacted diffs. Balance "enough to reconstruct what happened" against not turning the audit log into a new data-leak surface (see the `secrets-scan` and `logging` skills).
6. **Set retention and access.** Define how long entries are kept (compliance often dictates this) and restrict who can read them. Note the chosen retention window.
7. **Verify.** Add tests asserting that a sensitive action writes exactly one audit entry with the right actor/action/target/outcome, that a failed/denied attempt is also recorded, and that a rolled-back transaction leaves no entry.

### Rules

1. Audit records are append-only — application code inserts, never updates or deletes; enforce this at the store level where possible.
2. Every entry must identify actor, action, target, timestamp (UTC), and outcome using a stable, queryable schema — not free-text prose.
3. Write the audit entry atomically with the state change (same transaction) so records can't silently go missing or lie about rolled-back work; record failed/denied attempts too.
4. Never store secrets or unnecessary PII in the trail; redact sensitive values and keep the audit log separate from debug logging with its own retention and access controls.
5. End by summarizing which events are audited, the record schema, the store and its append-only guarantee, the retention window, and that failure cases are captured.
