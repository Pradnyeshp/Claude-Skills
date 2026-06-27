---
name: stash
description: Save, restore, and manage work-in-progress with git stash — shelve uncommitted changes to switch context, then bring them back without losing work. Use when the user says "stash my changes", "shelve this work", "save my work in progress", "pop the stash", "I need to switch branches but have uncommitted changes", "restore my stashed changes", or "clean up my stashes".
argument-hint: "[optional action or message, e.g. 'save \"wip on parser\"' or 'pop']"
allowed-tools: Bash, Read
disable-model-invocation: false
---

## Working tree & stash state

!`git status --short 2>/dev/null`

!`git stash list 2>/dev/null | head -20`

!`git branch --show-current 2>/dev/null`

## Instructions

Help the user shelve or restore work with `git stash` based on `$ARGUMENTS`. Stashing touches uncommitted work, so default to the non-destructive option and confirm before anything that can discard changes (`drop`, `clear`, or a conflicting `pop`).

### Method

1. **Read the intent.** Common cases: *save* current changes to switch context, *restore* (pop/apply) a previous stash, *inspect* what's in a stash, or *clean up* old stashes. If `$ARGUMENTS` is empty and there are local changes, assume they want to save; if the tree is clean and stashes exist, assume they want to restore.
2. **When saving:**
   - Use a descriptive message: `git stash push -m "<what this is>"` so the entry is identifiable later — never an anonymous stash when several may pile up.
   - Include untracked files only when needed (`-u`/`--include-untracked`); warn that `-a`/`--all` also stashes ignored files and is rarely wanted.
   - To stash only some files, use a pathspec (`git stash push -m "..." -- path/...`) or `--keep-index` to keep staged changes in the tree.
3. **When restoring:**
   - Prefer `git stash apply <ref>` over `pop` when unsure — `apply` keeps the stash so a botched restore is recoverable; `pop` deletes it on success. Reach for `pop` only once the right stash is confirmed.
   - Identify the target explicitly (`stash@{N}`) rather than assuming the top of the stack, especially when `git stash list` shows several.
   - If applying may conflict (the branch moved on), say so first; on conflict, resolve like a merge (see the `resolve-conflicts` skill) — and note that a failed `pop` leaves the stash intact.
4. **When inspecting:** `git stash show -p stash@{N}` shows the diff; list with `git stash list` and map each entry to its branch/message before acting.
5. **When cleaning up:** confirm exactly which entries before `git stash drop stash@{N}`. Treat `git stash clear` as destructive — it removes *all* stashes and is not part of normal undo. Always confirm explicitly, and mention entries linger in the reflog briefly if recovery is needed.

### Rules

1. Default to non-destructive actions: `apply` over `pop`, named saves over anonymous, and never `drop`/`clear` without explicit confirmation of which entries are affected.
2. Always give saved stashes a descriptive `-m` message, and target restores by explicit `stash@{N}` rather than assuming the top of the stack.
3. Warn before restoring onto a tree that has moved on (conflicts likely) and before stashing untracked/ignored files unless the user asked.
4. A stash is not a backup — surface that dropped/cleared stashes are only briefly recoverable via the reflog, and prefer a commit for anything that must not be lost.
5. End by showing the resulting `git status --short` and `git stash list` so the user can see exactly what was saved or restored.
