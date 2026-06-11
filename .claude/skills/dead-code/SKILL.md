---
name: dead-code
description: Find unused code — unreferenced exports, functions, variables, imports, files, and dependencies — and propose safe removals. Use when the user says "find dead code", "what's unused", "remove unused imports", "find unreferenced functions", "what can I delete", or "clean up dead code".
argument-hint: "[optional path to focus on, e.g. 'src/']"
allowed-tools: Bash, Read, Grep, Glob
disable-model-invocation: false
---

## Stack & tooling signals

!`ls package.json pyproject.toml Cargo.toml go.mod tsconfig.json 2>/dev/null`

!`ls node_modules/.bin/knip node_modules/.bin/ts-prune node_modules/.bin/depcheck 2>/dev/null`

## Instructions

Find dead (unused) code in this project, scoped to `$ARGUMENTS` if a path was given, and propose safe removals. Default to **report-and-confirm**, not silent deletion.

### Method

1. **Prefer a real analyzer when one exists.** Use the language's dead-code tooling and report its output:
   - **JS/TS:** `knip`, `ts-prune`, `depcheck` (unused deps), or `eslint` with `no-unused-vars`.
   - **Python:** `vulture`, or `ruff`/`flake8` unused-import rules.
   - **Rust:** the compiler's `dead_code` / `unused` warnings (`cargo build`).
   - **Go:** `go vet`, `staticcheck` (`U1000`), `deadcode`.
   - If no tool is installed, fall back to careful grep: for each exported symbol, search the codebase for references and flag those with none.
2. **Verify before condemning.** A symbol with zero internal references may still be a public API entry point, a framework hook (route handler, lifecycle method, CLI command), used via reflection/dynamic dispatch, or referenced in a string/config. Read the context and rule these out — don't flag what's reachable through a non-obvious path.
3. **Categorize findings:** unused imports, unused local variables, unreferenced functions/classes, unreachable branches, orphaned files (imported by nothing), and unused dependencies.
4. **Rank by safety.** Unused imports and locals are near-zero-risk; unreferenced exported functions and whole files need more scrutiny (could be public surface). Note the risk per item.

### Output

Group findings by safety, each with a `file:line` and why it appears unused:

```
### Safe to remove — local scope
- `path:line` — unused import `foo`

### Likely dead — verify it's not public API
- `path:line` — exported `bar()` has no references in the repo
```

Then offer to delete the safe tier and let the user confirm the riskier ones.

### Rules

1. Report real, evidenced findings (`file:line` + tool output or the search that found nothing). Don't guess.
2. Be conservative with anything exported or entry-point-like: public APIs, dynamically-referenced code, and framework-invoked functions are easy false positives — flag them as "verify", not "delete".
3. Don't delete in the discovery pass. After the user confirms, removals should be done in small, behavior-preserving steps with tests run after.
4. Treat unused dependencies separately — a package may be used only at runtime/build time or via a config the analyzer can't see.
5. If nothing is unused, say so plainly rather than padding the list.
