---
name: cherry-pick
description: Apply specific commits from one branch onto another with git cherry-pick — backport a fix, pull a single feature commit across branches, or recover a commit — safely and with conflict handling. Use when the user says "cherry-pick this commit", "backport this fix to the release branch", "apply commit X to main", "bring that commit over here", "port this change to another branch", or "I need just one commit from that branch".
argument-hint: "[commit SHA(s) or range to apply, e.g. 'abc123' or 'abc123..def456']"
allowed-tools: Bash, Read
disable-model-invocation: false
---

## Branch & commit context

!`git status --short 2>/dev/null`

!`git branch --show-current 2>/dev/null`

!`git log --oneline -10 2>/dev/null`

## Instructions

Apply the commit(s) in `$ARGUMENTS` onto the current branch with `git cherry-pick`. Cherry-picking copies commits and can conflict or duplicate work — confirm the target commits and the destination branch before starting, and stop to let the user resolve conflicts rather than guessing.

### Method

1. **Require a clean working tree.** If there are uncommitted changes, stop and tell the user to commit or stash first (see the `stash` skill) — cherry-pick refuses to run mid-mess and a dirty tree risks losing work.
2. **Confirm what and where.** Verify you're on the intended destination branch and identify the exact commit(s): a single SHA, a list, or a range (`A..B` excludes `A`; `A^..B` includes it). Show `git show --stat <sha>` for each so the user confirms these are the right changes before applying.
3. **Check it isn't already there.** Look for the change on the target (`git log --oneline --grep` or compare patches) — cherry-picking something already merged creates a duplicate/empty commit. If the same content is present, say so instead of re-applying.
4. **Apply deliberately:**
   - Single or several commits: `git cherry-pick <sha> [<sha>...]` (applies oldest-first).
   - Preserve provenance for backports with `-x`, which appends a "cherry picked from commit <sha>" line so the origin is traceable.
   - Use `-n`/`--no-commit` to stage without committing when the user wants to review or combine before committing.
5. **Handle conflicts as a checkpoint.** On conflict, do **not** force a resolution — show the conflicted files, explain both sides, and resolve like a merge (see `resolve-conflicts`). Continue with `git cherry-pick --continue`, or back out cleanly with `git cherry-pick --abort` (or `--skip` for an already-applied commit). Never leave the repo mid-cherry-pick silently.
6. **Verify and report.** After applying, confirm the result builds/tests pass where relevant, show the new `git log --oneline`, and note that cherry-picked commits have new SHAs — so the branches will show the change twice if they're later merged.

### Rules

1. Never start with a dirty tree or without confirming both the source commit(s) and the destination branch.
2. Check whether the change is already present before applying — avoid duplicate or empty commits; surface it if it's already there.
3. On conflict, stop and let the user resolve; never guess a resolution. Always offer `--continue` / `--abort` and never abandon the repo in a half-applied state.
4. Use `-x` for backports so the origin commit is recorded, and prefer cherry-picking the minimal set — for many commits across branches, consider whether a merge or rebase is the right tool instead.
5. End with the resulting history, confirmation tests pass, and a note that the commits are copies with new SHAs.
