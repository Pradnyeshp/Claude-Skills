---
name: resolve-conflicts
description: Walk through git merge, rebase, or cherry-pick conflicts — understand both sides, resolve each hunk correctly, and verify the result before continuing. Use when the user says "resolve merge conflicts", "fix these conflicts", "help me with this merge", "I have conflicts", "finish this rebase", or "git says conflicts".
argument-hint: "[optional: context, e.g. 'keep our auth changes, take their formatting']"
allowed-tools: Bash, Read, Edit, Grep, Glob
disable-model-invocation: false
---

## Conflict state

!`git status --short 2>/dev/null || echo "Not a git repository"`

!`git diff --name-only --diff-filter=U 2>/dev/null | sed 's/^/CONFLICTED: /' || true`

!`ls -d .git/rebase-merge .git/rebase-apply .git/MERGE_HEAD .git/CHERRY_PICK_HEAD 2>/dev/null | sed 's/^/IN-PROGRESS: /' || echo "No merge/rebase/cherry-pick in progress"`

## Instructions

Resolve the conflicted files listed above. Honor any preference in `$ARGUMENTS` (e.g. "prefer our version"). If there's no conflict in progress, say so and stop.

### Orient first

1. **Identify the operation** from the in-progress markers: a merge (`MERGE_HEAD`), a rebase (`rebase-merge`/`rebase-apply`), or a cherry-pick. This changes what "ours" and "theirs" mean:
   - **Merge:** `ours` = current branch (`HEAD`), `theirs` = the branch being merged in.
   - **Rebase:** roles are *flipped* — `ours` = the upstream you're replaying onto, `theirs` = your commit being applied. Call this out so the user doesn't pick the wrong side.
2. **See what's diverging.** For context, check what each side was doing: `git log --oneline --left-right HEAD...MERGE_HEAD` (merge) or look at the commit being applied during a rebase.

### Resolve each file

1. **Read the full conflicted file**, not just the hunk — surrounding code reveals intent. Find every `<<<<<<<` / `=======` / `>>>>>>>` block.
2. **Understand both sides before editing.** What did each side intend to change, and why? Use `git log`/`git blame` on the region if the reason isn't obvious. The goal is a result that preserves *both* intents, not a mechanical pick of one side.
3. **Resolve by meaning, not by deletion.** Usually you keep parts of both. Take one side wholesale only when they're genuinely mutually exclusive. Remove all conflict markers and leave syntactically valid code.
4. **Watch for semantic conflicts** git can't see: both sides renamed the same thing differently, one side's change relies on code the other side moved or deleted, duplicate imports/definitions after merging. Re-read the merged region for these.
5. After resolving a file, `git add <file>` to mark it resolved.

### Verify, then continue

1. **Confirm no markers remain:** `git diff --check` and a grep for `<<<<<<<` across the resolved files.
2. **Sanity-check the result builds/lints/tests** if a quick command exists — a clean merge that doesn't compile isn't resolved. Hand off to the `lint-fix` or test tooling if useful.
3. **Continue the operation:** `git merge --continue`, `git rebase --continue` (repeat per replayed commit — a rebase can hit fresh conflicts on the next commit), or `git cherry-pick --continue`. For a plain merge, a commit completes it.

### Rules

1. **Never resolve by blindly taking one side** unless the user said so or the sides are truly exclusive — silent data loss is the main hazard here. When unsure which intent wins, show the user both sides and ask.
2. Remember rebase flips ours/theirs. Don't rely on `--ours`/`--theirs` shortcuts unless you've confirmed which is which for the current operation.
3. Don't `git checkout`/`reset`/`abort` to "clean up" without explicit confirmation — that can throw away the user's work. If things look wrong, explain the state and offer `git merge --abort` / `git rebase --abort` as a choice.
4. A rebase resolves one commit at a time; after `--continue`, re-check status for the next conflict rather than assuming you're done.
5. Summarize what you changed per file, which intent you preserved, and the exact command run to continue (or what's left for the user to do).
