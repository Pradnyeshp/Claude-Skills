---
name: deps
description: Audit the project's dependencies for outdated, deprecated, or vulnerable packages and recommend a safe upgrade path. Use when the user says "check dependencies", "audit deps", "are my packages out of date", "any vulnerabilities", "what should I upgrade", or "check for CVEs".
argument-hint: "[optional package name to focus on]"
allowed-tools: Bash, Read, Grep, Glob
disable-model-invocation: false
---

## Detected manifests & lockfiles

!`ls package.json package-lock.json yarn.lock pnpm-lock.yaml requirements.txt pyproject.toml poetry.lock Cargo.toml Cargo.lock go.mod Gemfile Gemfile.lock 2>/dev/null`

## Instructions

Audit the project's dependencies (or just `$ARGUMENTS` if a package was named). Detect the ecosystem from the manifests above and use the matching tooling.

### Method

1. **Pick the right tools** for the detected ecosystem and run the read-only audit/outdated commands:
   - **npm/yarn/pnpm:** `npm outdated`, `npm audit` (or the yarn/pnpm equivalents)
   - **Python:** `pip list --outdated`, and `pip-audit` if available
   - **Rust:** `cargo outdated`, `cargo audit` if available
   - **Go:** `go list -u -m all`, `govulncheck` if available
   - If a tool isn't installed, say so and suggest how to install it rather than guessing results.
2. **Read the manifest** to see which versions are pinned vs. ranged, and which are direct vs. transitive.
3. **Triage findings into:**
   - 🔴 **Security** — known vulnerabilities (include severity and the fixed version)
   - 🟡 **Major outdated** — behind by a major version (potential breaking changes)
   - 🟢 **Minor/patch outdated** — safe, low-risk bumps
4. **Recommend an upgrade path**, safest first: patch/minor bumps and security fixes before major upgrades. Note which majors likely need code changes or a changelog review.

### Rules

1. Only run **read-only** commands. Never modify manifests, lockfiles, or run installs/upgrades unless the user explicitly asks.
2. Report actual command output — don't claim a package is vulnerable or outdated without evidence from a tool.
3. Distinguish direct dependencies (the user controls) from transitive ones (fixed by upgrading a parent).
4. If everything is current and clean, say so plainly.
5. Summarize with a short prioritized action list the user can act on.
