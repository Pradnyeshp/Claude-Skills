---
name: lint-fix
description: Detect the project's linter and formatter, run them, and fix the reported problems — auto-fixable ones first, then the rest by hand — without changing behavior. Use when the user says "fix the lint errors", "run the linter", "format this code", "clean up lint warnings", "make lint pass", or "fix formatting".
argument-hint: "[optional: a path/file to limit to, or a specific rule/error]"
allowed-tools: Bash, Read, Edit, Glob, Grep
disable-model-invocation: false
---

## Linter & formatter config

!`ls .eslintrc .eslintrc.js .eslintrc.json .eslintrc.cjs eslint.config.js eslint.config.mjs .prettierrc .prettierrc.json prettier.config.js biome.json ruff.toml .ruff.toml .flake8 setup.cfg pyproject.toml .rubocop.yml .golangci.yml .golangci.yaml rustfmt.toml .editorconfig 2>/dev/null`

!`cat package.json 2>/dev/null | grep -A30 '"scripts"' | grep -iE 'lint|format|fmt|prettier|biome|eslint' | head -20`

## Instructions

Find the project's linter/formatter, run it, and fix what it reports (scope to `$ARGUMENTS` if given). Use the project's own tooling and config — never impose your own style.

### Method

1. **Identify the configured tools** from the files and scripts above. Common stacks:
   - **JS/TS:** ESLint and/or Prettier, or Biome. Prefer the project's npm scripts (`npm run lint`, `lint:fix`, `format`) when they exist.
   - **Python:** Ruff, Flake8, Black, isort. Prefer `ruff check --fix` / `black` / `isort` per config.
   - **Go:** `gofmt`/`goimports`, `golangci-lint run`.
   - **Rust:** `cargo fmt`, `cargo clippy`.
   - **Ruby:** `rubocop -a`.
   If no linter is configured, say so and suggest adding one (hand off to `ci-setup`) rather than inventing rules.
2. **Run the check first** (read-only) to see the full set of problems and their counts. If a tool isn't installed, report that and how to install it instead of guessing.
3. **Apply safe auto-fixes** using the tool's own fixer (`--fix`, `-a`, `--write`, `cargo fmt`). Let formatters and rule-fixers do the mechanical work — don't hand-edit what a tool can fix deterministically.
4. **Re-run, then fix the remainder by hand.** For each manual fix, understand the rule before changing code, and make the *minimal* change that satisfies it while preserving behavior. Group by rule so the edits are consistent.
5. **Re-run until clean** (or until only intentional, suppression-worthy cases remain). Show the before/after problem counts.

### Rules

1. **Behavior-preserving only.** Linting is cleanup, not refactoring or bug-fixing — if a lint rule is flagging a real bug, point it out separately rather than silently changing logic.
2. Use the project's config as the source of truth. Don't add, remove, or relax rules, and don't reformat with different settings than the project uses. If a rule seems wrong, raise it with the user instead of editing the config.
3. Prefer fixing over suppressing. Only add an inline disable (`// eslint-disable-next-line`, `# noqa`) when the rule genuinely shouldn't apply, and add a brief reason — never blanket-disable to make output green.
4. Keep auto-fix and manual changes reviewable: don't bundle unrelated edits. If a formatter would reflow huge swaths of untouched code, flag that and confirm scope before committing to it.
5. Summarize what ran, what was auto-fixed vs. hand-fixed, the remaining count, and anything you suppressed or that needs a human decision.
