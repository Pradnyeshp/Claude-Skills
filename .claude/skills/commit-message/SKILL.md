---
name: commit-message
description: Generate a conventional commit message from staged git changes. Use when the user asks to commit, write a commit message, says "commit this", "what should the commit message be", or "prepare a commit".
argument-hint: "[optional scope override]"
allowed-tools: Bash, Read
disable-model-invocation: false
---

## Staged changes

!`git diff --cached --stat`

!`git diff --cached`

## Instructions

Generate a commit message for the staged changes above following the **Conventional Commits** specification.

### Format

```
<type>(<scope>): <subject>

<body>
```

### Rules

1. **type** must be one of: `feat`, `fix`, `refactor`, `chore`, `docs`, `test`, `style`, `perf`, `ci`, `build`
2. **scope** is the primary area affected (e.g., `auth`, `api`, `ui`). Auto-detect from the changed file paths. If the user passed an argument, use `$ARGUMENTS` as the scope instead.
3. **subject** is imperative mood, lowercase, no period, under 50 characters
4. **body** is optional — include only when the "what" isn't obvious from the subject. Wrap at 72 characters. Explain *why*, not *what*.
5. If changes span multiple logical units, suggest splitting into separate commits and show each proposed message.
6. If there are no staged changes, tell the user to stage files first with `git add`.

### Output

Print ONLY the commit message — no explanation, no markdown fences. If suggesting a split, use numbered sections.
