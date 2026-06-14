---
name: squash
description: Clean up a branch's commit history before merge — squash WIP/fixup commits into logical units and rewrite messages — safely, without losing work. Use when the user says "squash my commits", "clean up the history", "combine these commits", "tidy the branch before merging", "squash the fixups", or "rewrite the commit history".
argument-hint: "[optional base branch or commit to squash onto, e.g. 'main']"
allowed-tools: Bash, Read
disable-model-invocation: false
---

## Branch state

!`git status --short 2>/dev/null`

!`git log --oneline --no-merges "$(git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null)"..HEAD 2>/dev/null | head -30`

!`git branch --show-current 2>/dev/null`

## Instructions

Tidy the current branch's commits onto its base (`$ARGUMENTS` if given, else `main`/`master`) so the history that merges is clean and logical. History rewriting is destructive — be careful and confirm before rewriting.

### Before touching history

1. **Require a clean working tree.** If there are uncommitted changes, stop and tell the user to commit or stash first — a rewrite with a dirty tree risks losing work.
2. **Confirm the branch isn't shared,** or that collaborators know. Rewriting commits others have pulled forces a `--force-push` that rewrites their view. If the branch is already pushed, note that a force-push (`--force-with-lease`) will be needed and confirm that's acceptable.
3. **Make a safety net:** record the current tip (`git rev-parse HEAD`) or suggest a backup ref (`git branch backup/<name>`) so the pre-squash state is recoverable via reflog if anything goes wrong.
4. **Identify the base** with `git merge-base` and review the commits above. Propose how to group them into logical units (e.g. squash all `fixup`/`wip`/`address review` commits into the feature commit they belong to) before doing anything.

### Squashing

1. **Prefer the safest mechanism that fits:**
   - Whole branch into one commit: `git reset --soft <base>` then a single `git commit` — simple and avoids interactive rebase.
   - Selective grouping: a non-interactive autosquash (`git rebase --autosquash`) when commits were made with `--fixup`, or scripted reword — interactive `-i` rebase isn't available in this environment, so drive it with explicit commands.
2. **Write clear messages** for the resulting commits (Conventional Commits if the repo uses them — see the `commit-message` skill). One commit per logical change, each message explaining the *why*.
3. **Verify nothing was lost:** after rewriting, confirm `git diff <base>..HEAD` is identical to before (same tree), and the test suite still passes. The content must be unchanged — only the history shape changes.
4. **Don't push automatically.** Show the resulting `git log --oneline` and the exact `git push --force-with-lease` command, and let the user run it.

### Rules

1. Never rewrite history with a dirty tree or without a recoverable backup (reflog/backup branch). State the recovery path.
2. The final tree must be byte-identical to before squashing — verify with a diff. Squashing changes history, never content.
3. Use `--force-with-lease`, never a bare `--force`, when a push is needed — and only after the user confirms. Don't push on their behalf unless asked.
4. Be cautious on shared branches: call out who is affected before any rewrite.
5. End with the new history, confirmation the diff is unchanged and tests pass, and the push command the user can run.
