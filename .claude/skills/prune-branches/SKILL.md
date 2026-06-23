---
name: prune-branches
description: Clean up stale git branches — local and remote — that are already merged or long abandoned, safely and with confirmation. Use when the user says "clean up branches", "delete merged branches", "prune stale branches", "remove old branches", "tidy up git branches", or "which branches can I delete".
argument-hint: "[optional base branch to measure merges against, default main/master]"
allowed-tools: Bash, Read
disable-model-invocation: false
---

## Branch landscape

!`git branch --show-current 2>/dev/null`

!`git branch --merged "$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/@@' || echo main)" 2>/dev/null | head -40`

!`git for-each-ref --sort=committerdate refs/heads --format='%(refname:short)  %(committerdate:relative)' 2>/dev/null | head -40`

## Instructions

Identify stale git branches and clean them up, measuring "merged" against the base in `$ARGUMENTS` (default the repo's default branch — `main`/`master`). This rewrites nobody's history but **deletes refs**, so report first and delete only with confirmation.

### Method

1. **Run `git fetch --prune` first** so the remote-tracking refs are current — otherwise you'll judge branches against stale data and may flag already-deleted ones.
2. **Categorize branches**, never just by name:
   - **Merged** — `git branch --merged <base>`: their commits are all in the base, so deleting loses nothing. Safe.
   - **Stale but unmerged** — no commits in months *and* not merged: these may hold unmerged work. List separately and require explicit per-branch confirmation; show `git log <base>..<branch> --oneline` so the user sees what's unique.
   - **Gone remote** — local branches whose upstream was deleted (`git branch -vv` shows `: gone]`): usually safe once their work merged, but verify they're also merged.
3. **Never touch protected branches** — the current branch, the default branch (`main`/`master`), release/`develop` branches, or anything the user names as protected. Exclude them from every list.
4. **Delete safely.** Use `git branch -d` (merged-only, refuses unmerged) for the merged set — never `-D` unless the user explicitly confirms discarding unmerged work on a specific branch. For remote deletion, `git push origin --delete <branch>` only with explicit confirmation, since it affects everyone.
5. **Local vs remote are separate decisions** — confirm each. Deleting a local branch doesn't remove its remote, and vice versa.

### Rules

1. Report the full categorized list and get confirmation before deleting anything — this removes refs and can lose unmerged work.
2. Prefer `git branch -d` (safe, merged-only); use `-D` only on a specific branch the user explicitly okays. The merged check is the safety net — don't bypass it.
3. Always exclude the current branch, the default branch, and any release/protected branches from deletion.
4. Treat remote deletions (`push --delete`) as higher-stakes than local — they affect all collaborators; confirm separately and never batch them silently.
5. Recovery exists but is finite — note that a mistakenly deleted branch's tip is recoverable via `git reflog` for a while, and capture SHAs in the summary. End with what was deleted (local/remote) and what was kept and why.
