---
name: migrate
description: Apply a sweeping, mechanical change consistently across the whole codebase — rename an API, swap a library or pattern, update a deprecated call — then verify nothing broke. Use when the user says "migrate all", "rename X everywhere", "replace every use of", "codemod", "update all callers", or "switch the project from X to Y".
argument-hint: "[the change, e.g. 'replace moment with date-fns' or 'rename getUser to fetchUser everywhere']"
allowed-tools: Bash, Read, Edit, Grep, Glob
disable-model-invocation: false
---

## Scope of the change

!`git status --short 2>/dev/null && echo "(commit or stash first — a migration touches many files)"`

## Instructions

Apply the migration described in `$ARGUMENTS` across the codebase. If the change isn't specific (the old → new mapping, or which symbol/pattern), ask before editing anything — a vague migration corrupts files at scale.

### Method

1. **Map the blast radius first.** Use `grep`/`glob` to find every occurrence — source, tests, config, docs, and string references. Report the count and the distinct usage shapes before changing anything. Watch for partial-word false positives (`getUser` inside `getUserId`).
2. **Confirm the transformation rule.** State the exact old → new mapping and any cases that should be left alone (comments, generated files, vendored code, unrelated same-named symbols in another module).
3. **Apply consistently.** Edit every real call site, plus imports/exports, type signatures, tests, and docs that reference it. Don't leave a half-migrated codebase. For large mechanical renames, prefer a scripted codemod (`sed`/`ast-grep`/language codemod tool) and show the command, but review its diff.
4. **Handle the long tail:** re-exports, dynamic references (string keys, reflection, config files), and anything the search couldn't see. Call out spots you couldn't safely automate so the user can check them.
5. **Verify.** Build/typecheck and run the test suite. Report what passed. If the project has a linter, run it to catch leftover unused imports.

### Rules

1. Insist on a clean working tree (or recent commit) before starting — migrations are large and hard to undo by hand. Stop and say so if it's dirty.
2. Never do a blind global find-and-replace; verify each match class is a real target. Show the diff stat (`git diff --stat`) when done.
3. Preserve behavior unless the migration explicitly changes it — flag any spot where the new API has different semantics (e.g. different default, throws instead of returns null).
4. End with: files changed, occurrences migrated, verification result, and any sites left for manual review.
