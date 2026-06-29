---
name: rebase
description: Replay a branch's commits onto a new base with git rebase — update a feature branch onto the latest main, move commits onto a different base, or linearize history — safely, with conflict handling and a recovery path. Use when the user says "rebase onto main", "update my branch with the latest main", "replay my commits", "move my branch onto", "rebase this branch", or "get the latest changes into my branch without a merge commit".
argument-hint: "[base to rebase onto, e.g. 'main' or 'origin/main']"
allowed-tools: Bash, Read
disable-model-invocation: false
---

## Branch state

!`git status --short 2>/dev/null`

!`git branch --show-current 2>/dev/null`

!`git log --oneline --no-merges "$(git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null)"..HEAD 2>/dev/null | head -30`

## Instructions

Rebase the current branch onto the base in `$ARGUMENTS` (default `main`/`master`) so its commits replay on top of the latest base, giving a linear history without a merge commit. Rebasing rewrites commits — be careful and confirm before rewriting anything already pushed or shared.

### Before rebasing

1. **Require a clean working tree.** Uncommitted changes must be committed or stashed first (see the `stash` skill) — rebase refuses to start dirty and a half-rebase can lose uncommitted work.
2. **Make a safety net.** Record the current tip (`git rev-parse HEAD`) or suggest `git branch backup/<name>` so the pre-rebase state is recoverable via the reflog if anything goes wrong.
3. **Check whether the branch is shared.** Rebasing commits others have pulled forces a `--force-push` that rewrites their view. If the branch is already pushed, note that `--force-with-lease` will be needed afterward and confirm that's acceptable. For a shared branch, a merge is often the safer choice — say so.
4. **Fetch first** when rebasing onto a remote base so you replay onto the true latest (`git fetch` then rebase onto `origin/main`).

### Rebasing

1. **Run the rebase:** `git rebase <base>` (or `git rebase --onto <newbase> <upstream>` to transplant only a range of commits onto a different base).
2. **Handle conflicts as a checkpoint.** On conflict, do **not** guess — show the conflicted files, explain both sides, resolve like a merge (see `resolve-conflicts`), `git add` the resolved files, then `git rebase --continue`. Offer `git rebase --skip` for an already-applied commit and `git rebase --abort` to return cleanly to the pre-rebase state. Never leave the repo mid-rebase silently.
3. **Don't auto-squash here.** Reordering/combining commits is the `squash` skill's job — this skill replays the existing commits onto a new base. Keep them intact unless the user asks otherwise.
4. **Verify nothing was lost.** After rebasing, confirm the diff against the base reflects only the intended changes and the test suite still passes — the content should match what the branch contributed before, now on top of the new base.

### Rules

1. Never rebase with a dirty tree or without a recoverable backup (reflog/backup branch); state the recovery path.
2. On conflict, stop and let the user resolve; never guess. Always surface `--continue` / `--skip` / `--abort` and never abandon the repo mid-rebase.
3. Use `--force-with-lease`, never a bare `--force`, when the rebased branch must be pushed — and only after the user confirms. Don't push on their behalf unless asked.
4. Be cautious on shared branches: call out who is affected and offer merge as the safer alternative before rewriting.
5. End with the resulting `git log --oneline`, confirmation the content is intact and tests pass, and the exact `git push --force-with-lease` command to run.
