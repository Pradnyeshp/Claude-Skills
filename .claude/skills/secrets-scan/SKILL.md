---
name: secrets-scan
description: Scan the working tree and git history for hardcoded secrets — API keys, tokens, passwords, private keys, connection strings — and report what to rotate and remove. Use when the user says "scan for secrets", "check for leaked credentials", "any hardcoded keys", "did I commit a secret", "find exposed tokens", or "audit for credentials".
argument-hint: "[optional path or glob to focus on, e.g. 'src/' or '*.env']"
allowed-tools: Bash, Read, Grep, Glob
disable-model-invocation: false
---

## Scan surface

!`git ls-files 2>/dev/null | grep -viE '\.(png|jpg|jpeg|gif|svg|ico|woff2?|ttf|lock)$' | head -50 || ls 2>/dev/null`

!`ls .env .env.* .gitignore 2>/dev/null`

!`git log --oneline -5 2>/dev/null`

## Instructions

Scan this project for hardcoded secrets and credentials (focused on `$ARGUMENTS` if a path was given). Cover the working tree, and check git history when the user asks or when a tracked `.env`-style file is found.

### Method

1. **Grep for high-signal patterns** across tracked files. Look for:
   - Cloud/provider keys — `AKIA[0-9A-Z]{16}` (AWS), `AIza[0-9A-Za-z_-]{35}` (Google), `ghp_`/`gho_`/`github_pat_` (GitHub), `sk-`/`sk-ant-` (OpenAI/Anthropic), `xox[baprs]-` (Slack), `glpat-` (GitLab), Stripe `sk_live_`/`rk_live_`.
   - Generic assignments — `(api[_-]?key|secret|token|password|passwd|pwd|access[_-]?key|client[_-]?secret)\s*[:=]\s*['"][^'"]{8,}`.
   - Private keys — `-----BEGIN (RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----`.
   - Connection strings with embedded credentials — `(postgres|mysql|mongodb|redis|amqp)(\+srv)?://[^:@\s]+:[^@\s]+@`.
   - JWTs — `eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.`.
2. **Check whether secret-bearing files are tracked.** If `.env` (or similar) is committed, that's a finding on its own — confirm it's in `.gitignore` and flag it for `git rm --cached`.
3. **Scan history when warranted.** Use `git log -p -S<token>` or `git log --all --full-history -- <file>` to see if a secret was ever committed, even if since removed — it still needs rotating.
4. **Rule out false positives.** Read each hit in context: placeholders (`your-api-key-here`, `xxx`, `changeme`), example/test fixtures, public keys, and `.env.example` templates are not leaks. Don't cry wolf.

### Output

For each real finding: the `file:line`, what kind of secret it is, and whether it's in the working tree, history, or both. Then a prioritized remediation list:

1. **Rotate first** — any secret that was ever committed must be treated as compromised and rotated at the provider, regardless of removal.
2. **Remove from code** — move it to an env var / secret manager; add the file to `.gitignore`.
3. **Purge from history** if needed (`git filter-repo` / BFG) — note this rewrites history and requires coordination.

### Rules

1. **Never print full secret values** in your output — show a masked preview (first/last few chars) so the user can locate it without re-leaking it.
2. Read each match in context before reporting — distinguish real credentials from placeholders, examples, and public keys.
3. Read-only: do not edit files, rewrite history, or run installs. Recommend the commands; let the user run them.
4. Removing a secret from the current code does **not** un-leak it — always tell the user to rotate anything that was committed.
5. If the scan comes back clean, say so plainly and note what you checked.
