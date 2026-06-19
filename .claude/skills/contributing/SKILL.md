---
name: contributing
description: Generate or update a CONTRIBUTING.md for the project — how to set up, the dev workflow, branch/commit/PR conventions, and how to run tests and checks — read from the codebase. Use when the user says "write a CONTRIBUTING guide", "add contribution guidelines", "document the dev workflow", "how should people contribute", or "create a CONTRIBUTING.md".
argument-hint: "[optional section to focus on, e.g. 'the PR process']"
allowed-tools: Bash, Read, Write, Grep, Glob
disable-model-invocation: false
---

## Contribution signals

!`ls CONTRIBUTING* CODE_OF_CONDUCT* .github 2>/dev/null && echo "(existing files above — update, don't blindly overwrite)"`

!`cat package.json pyproject.toml Cargo.toml Makefile 2>/dev/null | grep -iE '"scripts"|"test"|"lint"|"format"|test =|lint =|^[a-z-]+:' | head -25`

!`ls .pre-commit-config.yaml .husky .github/workflows .github/PULL_REQUEST_TEMPLATE* 2>/dev/null`

## Instructions

Generate or update `CONTRIBUTING.md` for this project (focus on the `$ARGUMENTS` section if one was named). Write for a new contributor who wants to make their first change correctly.

### Method

1. **Read the project's real workflow** from the signals above — the dev/build/test/lint commands (scripts, Makefile, tox), the hooks (pre-commit/husky), CI (what the workflows enforce), and any PR template or existing conventions. Document what the project actually does, not a generic template.
2. **Decide create vs update.** If `CONTRIBUTING.md` exists, preserve its structure and any project-specific rules; refresh only what's stale or missing. Otherwise create one from the structure below.
3. **Write `CONTRIBUTING.md`** at the repo root (or `.github/`), and don't duplicate the README — link to it for setup rather than repeating it.

### Suggested structure

```
# Contributing

## Getting set up        # prerequisites + the actual setup commands (link README if covered)
## Development workflow   # branch naming, how to run the app, where code lives
## Tests & checks        # the exact commands CI runs — tests, lint, typecheck, format
## Commit & PR guidelines # commit convention, PR size/scope, what a good PR looks like
## Reporting issues      # how to file a bug / request a feature
## Code of conduct       # link, if a CODE_OF_CONDUCT file exists
```

### Rules

1. Document the real, verifiable process — every command must come from a script/Makefile/CI target that exists. If you can't confirm something (e.g. the branching model), mark it as a suggested default rather than asserting it.
2. Reflect what CI actually enforces so contributors can pass checks locally before pushing — point them at the `pre-commit`/`lint-fix`/`test-gen` skills where relevant.
3. If the repo uses Conventional Commits (check git history / commitlint config), state that and link the `commit-message` skill; don't impose a convention the project doesn't use.
4. Keep it practical and skimmable — a new contributor should be able to go from clone to passing PR by following it. Don't pad with boilerplate that doesn't apply.
5. After writing, summarize what you created or changed and flag anything you marked as a suggested default needing the maintainer's confirmation.
