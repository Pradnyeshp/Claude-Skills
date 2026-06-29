---
name: worktree
description: Manage multiple working trees of one repo with git worktree — check out several branches at once in separate directories so you can build, test, or review one branch without stashing or disturbing another. Use when the user says "set up a worktree", "check out this branch without losing my work", "work on two branches at once", "add a git worktree", "review a PR in a separate directory", or "clean up my worktrees".
argument-hint: "[optional action, e.g. 'add a worktree for the release branch' or 'list' or 'prune']"
allowed-tools: Bash, Read
disable-model-invocation: false
---

## Repo & worktree state

!`git worktree list 2>/dev/null`

!`git status --short 2>/dev/null`

!`git branch --show-current 2>/dev/null`

## Instructions

Help the user manage additional working trees with `git worktree` based on `$ARGUMENTS`. Worktrees let one repository have several branches checked out in parallel directories sharing a single `.git` — ideal for building/reviewing one branch while leaving the current one untouched. Adding/removing trees touches the filesystem, so confirm paths before creating or deleting.

### Method

1. **Read the intent.** Common cases: *add* a worktree for a branch (existing or new), *list* current worktrees, *remove* one when done, or *prune* stale administrative entries. If unclear, list first and ask.
2. **When adding:**
   - Place the new tree **outside** the current working directory (a sibling, e.g. `../<repo>-<branch>`), never nested inside the repo — a worktree inside the repo confuses status and ignore rules. Suggest a clear sibling path.
   - For an existing branch: `git worktree add ../<repo>-<branch> <branch>`.
   - For a new branch: `git worktree add -b <new-branch> ../<repo>-<new-branch> <start-point>`.
   - To review a PR/remote branch: fetch first, then add a tree tracking it.
   - Remember a branch can only be checked out in **one** worktree at a time — if it's already checked out elsewhere, git refuses; point the user to that existing tree instead.
3. **When listing:** `git worktree list` shows each path, its HEAD, and branch. Map them so the user knows which directory holds what before acting.
4. **When removing:** prefer `git worktree remove <path>` (it refuses if the tree has uncommitted changes — don't `--force` past that without confirming the changes are disposable). Deleting the directory by hand leaves a stale entry; if that happened, `git worktree prune` cleans it up.
5. **Report.** After any change, show `git worktree list` and the path the user should `cd` into. Note that all worktrees share the same object store and refs, so commits made in one are immediately visible to the others.

### Rules

1. Never create a worktree nested inside the repository — always a sibling/external path; confirm the path before creating.
2. A branch can be checked out in only one worktree at once; detect the conflict and direct the user to the existing tree rather than forcing it.
3. Don't `git worktree remove --force` or delete a tree with uncommitted changes without explicit confirmation — that work is not recoverable from the main tree.
4. After removing trees by hand, run `git worktree prune` to clear stale metadata; never leave dangling administrative entries.
5. End with the current `git worktree list` and the exact directory to switch into.
