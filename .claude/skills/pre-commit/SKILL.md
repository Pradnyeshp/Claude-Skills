---
name: pre-commit
description: Set up or improve pre-commit hooks that lint, format, and check the project before each commit, matching its language and tooling. Use when the user says "set up pre-commit hooks", "add a git hook", "run lint before commit", "configure husky", "add pre-commit", or "block bad commits".
argument-hint: "[optional: checks to include, e.g. 'lint format test' or a framework like 'husky' or 'pre-commit']"
allowed-tools: Bash, Read, Write, Glob, Grep
disable-model-invocation: false
---

## Project + existing hook detection

!`ls package.json pyproject.toml Cargo.toml go.mod Gemfile 2>/dev/null`

!`ls .pre-commit-config.yaml .husky .lefthook.yml lefthook.yml .git/hooks 2>/dev/null`

!`cat package.json 2>/dev/null | grep -A20 '"scripts"'`

## Instructions

Set up (or improve) pre-commit hooks for this project. Use the checks/framework in `$ARGUMENTS` if given; otherwise pick the idiomatic tool for the stack and wire up the checks the project already supports.

### Method

1. **Pick the right framework** for the ecosystem, preferring one already in use:
   - **JS/TS:** `husky` + `lint-staged` (run linters/formatters only on staged files).
   - **Python:** the `pre-commit` framework (`.pre-commit-config.yaml`).
   - **Polyglot / language-agnostic:** `pre-commit` or `lefthook`.
   - If a framework is already configured, extend its config rather than introducing a second one.
2. **Use the project's real commands.** Pull lint/format/typecheck/test commands from the scripts/manifest above (e.g. `eslint`, `prettier --write`, `ruff`, `black`, `gofmt`, `cargo fmt`). Don't invent script names or add tools the project doesn't have.
3. **Scope to staged files** where the tool supports it (lint-staged, pre-commit) so the hook stays fast — a slow hook gets bypassed with `--no-verify`.
4. **Order checks fast-to-slow and fail early:** format → lint → typecheck → quick tests. Keep the full/slow test suite in CI, not the hook, unless the user asks.
5. **Write the config** to the conventional path and add any needed `prepare`/install step (e.g. `"prepare": "husky"` in package.json). Note the one command the user runs to activate hooks locally.

### Rules

1. Only wire checks the project can actually run — verify the command exists in scripts/manifest before adding it. If a desired check has no tooling yet, say so instead of inventing it.
2. Don't add new dependencies beyond the hook framework and its standard companions, and call out exactly what gets installed.
3. Keep hooks fast and staged-file-scoped; heavy work belongs in CI (point to the `ci-setup` skill).
4. Never weaken or auto-`--no-verify` anything. The hook should be bypassable by the user, not by default.
5. After writing, summarize each hook, the install/activate command, and how to skip a hook in an emergency (`git commit --no-verify`).
