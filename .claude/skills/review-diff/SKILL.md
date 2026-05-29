---
name: review-diff
description: Review the current branch or working-tree diff for bugs, security issues, and style problems before committing. Use when the user asks to review changes, says "review my code", "review the diff", "spot bugs in my changes", "is this ready to commit", or "what's wrong with this code".
argument-hint: "[optional: base branch, defaults to main]"
allowed-tools: Bash, Read, Grep
disable-model-invocation: false
---

## Branch & base

!`git branch --show-current`

## Changes under review

!`git diff ${ARGUMENTS:-main}...HEAD --stat 2>/dev/null || git diff HEAD --stat 2>/dev/null || echo "No diff found"`

!`git diff ${ARGUMENTS:-main}...HEAD 2>/dev/null || git diff HEAD 2>/dev/null`

## Instructions

Review the diff above and report concrete, actionable findings. Review only the changed lines and the code they directly affect — do not audit the whole codebase.

### What to look for

1. **Correctness** — logic errors, off-by-one, null/undefined handling, incorrect conditionals, unhandled error paths, race conditions, resource leaks.
2. **Security** — injection (SQL/command/XSS), hardcoded secrets or credentials, missing authz/authn checks, unsafe deserialization, path traversal, unvalidated input.
3. **Maintainability** — duplicated logic, dead code, misleading names, missing edge-case handling, functions doing too much.
4. **Consistency** — deviations from patterns already used elsewhere in the file or project.

### Output format

Group findings by severity. For each, cite the file and line, explain the problem in one sentence, and give the fix:

```
### 🔴 Blocking
- `path/to/file.ts:42` — <problem>. Fix: <suggestion>

### 🟡 Should fix
- ...

### 🟢 Nits
- ...
```

### Rules

1. Be specific — every finding must reference a location and a concrete fix. No vague advice.
2. Do **not** invent problems. If a section has no findings, omit it. If the diff is clean, say so plainly.
3. Prioritize correctness and security over style.
4. Distinguish certainty from suspicion — flag "verify that…" items separately from confirmed bugs.
5. If the diff is empty, tell the user there's nothing to review.
