---
name: ci-setup
description: Generate or improve a CI pipeline (GitHub Actions by default) that installs, lints, tests, and builds the project, matching its language and tooling. Use when the user says "set up CI", "add GitHub Actions", "write a CI pipeline", "add a test workflow", or "automate my builds".
argument-hint: "[optional: provider (github/gitlab/circle), or jobs to include like 'lint test build']"
allowed-tools: Bash, Read, Write, Glob, Grep
disable-model-invocation: false
---

## Project + existing CI detection

!`ls package.json pyproject.toml requirements.txt Cargo.toml go.mod pom.xml build.gradle Gemfile 2>/dev/null`

!`ls -d .github/workflows .gitlab-ci.yml .circleci 2>/dev/null && echo "(existing CI config above — extend it, don't duplicate)"`

!`cat package.json 2>/dev/null | grep -A20 '"scripts"'`

## Instructions

Generate or improve a CI pipeline for this project (use the provider/jobs in `$ARGUMENTS` if given; otherwise default to **GitHub Actions**).

### Rules

1. **Detect the stack and its real commands.** Read the manifest/scripts above to find the actual install, lint, test, and build commands — use those verbatim (e.g. `npm ci` + `npm test`, `pytest`, `cargo test`, `go test ./...`). Don't invent script names.
2. **Pin versions sensibly.** Pin action versions (e.g. `actions/checkout@v4`) and the language runtime to what the project targets. Use a matrix only when the project genuinely supports multiple versions.
3. **Standard job order:** checkout → set up runtime → restore cache → install → lint → test → build. Cache the dependency directory (npm/pip/cargo/go module cache) keyed on the lockfile hash.
4. **Trigger on** push to the default branch and on pull requests, unless the user specifies otherwise.
5. **Keep it minimal and fast.** Fail early (lint before test), run independent jobs in parallel, and don't add deploy steps, secrets, or external integrations unless asked — flag where they'd plug in instead.
6. **Don't duplicate existing workflows.** If CI already exists, read it and propose targeted additions/fixes.
7. Write the file to the conventional path (`.github/workflows/ci.yml`, `.gitlab-ci.yml`, etc.).
8. After writing, summarize what each job does and note anything the user must configure (secrets, branch protection, required status checks).
