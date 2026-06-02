---
name: gitignore
description: Generate or tighten a .gitignore for the project's stack, and flag already-tracked files that should be ignored. Use when the user says "create a gitignore", "update my gitignore", "what should I ignore", "stop tracking this file", or "add X to gitignore".
argument-hint: "[optional: extra things to ignore, e.g. '.env, coverage/, *.log']"
allowed-tools: Bash, Read, Write, Glob, Grep
disable-model-invocation: false
---

## Stack + current state

!`ls package.json pyproject.toml requirements.txt Cargo.toml go.mod pom.xml build.gradle Gemfile composer.json 2>/dev/null`

!`cat .gitignore 2>/dev/null | head -60 || echo "No .gitignore yet"`

!`git ls-files 2>/dev/null | grep -iE '\.env$|\.log$|node_modules/|/dist/|/build/|\.DS_Store|__pycache__|\.pyc$|/target/|coverage/' | head -20 | sed 's/^/TRACKED-BUT-SHOULD-IGNORE: /'`

## Instructions

Generate or improve the `.gitignore` for this project (add anything from `$ARGUMENTS` too).

### Method

1. **Detect the stack(s)** from the manifests above — language, package manager, framework, and build tooling. A repo can need several sections (e.g. Node + Python).
2. **Cover the standard categories** for each detected stack: dependency dirs (`node_modules/`, `vendor/`), build output (`dist/`, `build/`, `target/`), caches (`__pycache__/`, `.pytest_cache/`, `.gradle/`), logs, coverage reports, env/secret files (`.env`, `.env.local`), editor/OS cruft (`.DS_Store`, `.idea/`, `.vscode/` — only if not project-shared), and lockfile/temp artifacts.
3. **Merge, don't clobber.** If a `.gitignore` exists, add only the missing entries and keep the user's existing ones and grouping. Group new entries under clear comment headers.
4. **Flag already-tracked files.** For any path in the `TRACKED-BUT-SHOULD-IGNORE` list above, adding it to `.gitignore` is *not* enough — git keeps tracking it. Tell the user and give the exact untrack command: `git rm --cached <path>` (or `-r` for a directory), noting it stays on disk.

### Rules

1. Don't ignore lockfiles (`package-lock.json`, `poetry.lock`, `Cargo.lock`) for applications — they should be committed. Do ignore them only for libraries if that's the project's convention; ask if unsure.
2. Keep entries specific — avoid overly broad globs (`*.json`) that would hide real source/config.
3. Don't add committed, project-shared editor config to the ignore list (e.g. a checked-in `.vscode/settings.json`).
4. After writing, summarize what you added and list any untrack commands the user still needs to run.
