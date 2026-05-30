---
name: tech-debt
description: Scan the codebase for TODO/FIXME/HACK markers and common code smells, then triage them into a prioritized, actionable list. Use when the user says "find tech debt", "list the TODOs", "what needs cleanup", "where are the FIXMEs", "audit code smells", or "what should we pay down".
argument-hint: "[optional path or marker to focus on, e.g. 'src/' or 'FIXME']"
allowed-tools: Bash, Read, Grep, Glob
disable-model-invocation: false
---

## Marker scan

!`grep -rniE "TODO|FIXME|HACK|XXX|DEPRECATED|TEMP|WORKAROUND" --include='*.*' -l . 2>/dev/null | grep -vE 'node_modules|\.git|dist|build|vendor|\.min\.' | head -40`

!`grep -rniE "TODO|FIXME|HACK|XXX" . 2>/dev/null | grep -vE 'node_modules|\.git|dist|build|vendor|\.min\.' | wc -l | xargs echo "Total marker hits:"`

## Instructions

Scan for technical debt (scoped to `$ARGUMENTS` if a path or marker was given) and turn it into a triaged backlog the team can act on.

### What to gather

1. **Inline markers** — collect the `TODO`/`FIXME`/`HACK`/`XXX`/`DEPRECATED` comments from the scan above. For each, read enough surrounding code to understand what it's actually asking for. Discard stale or already-resolved ones.
2. **Code smells** — while reading, note recurring structural debt: large/god functions, duplicated logic, dead code, missing error handling, magic numbers, tight coupling, missing tests around fragile code, commented-out blocks.

### Triage

Group findings by priority and give each an estimated effort (S/M/L):

```
### 🔴 High — risk or actively blocking
- `path/file:line` — <what & why it matters> (effort: S)

### 🟡 Medium — should fix, not urgent
- ...

### 🟢 Low — nice to have / cosmetic
- ...
```

Prioritize by **impact × risk**: things that can cause bugs, security issues, or block features rank above cosmetic cleanup.

### Rules

1. Report real findings with `file:line` locations — don't pad the list. If the codebase is clean, say so.
2. Read the context before judging a marker; a `TODO` may already be done or no longer relevant.
3. Don't fix anything in this pass — this is discovery and triage. Offer to tackle specific items next (the `refactor`, `optimize`, or `test-gen` skills can do the work).
4. End with a short "if you only do three things" recommendation.
