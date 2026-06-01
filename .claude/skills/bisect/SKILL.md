---
name: bisect
description: Find the commit that introduced a regression using git bisect, guided by a description of what broke and a way to test it. Use when the user says "find the commit that broke this", "bisect this regression", "when did this stop working", "git bisect", or "what change caused this bug".
argument-hint: "[what broke, and a known-good ref if you have one, e.g. 'login fails since last release; good at v1.2.0']"
allowed-tools: Bash, Read, Grep, Glob
disable-model-invocation: false
---

## Repo state

!`git log --oneline -15 2>/dev/null || echo "Not a git repository"`

!`git tag --sort=-creatordate 2>/dev/null | head -10`

!`git status --short 2>/dev/null`

## Instructions

Locate the commit that introduced the regression described in `$ARGUMENTS` using `git bisect`. If the symptom or a way to reproduce it isn't clear, ask before touching the repo.

### Before starting

1. **Confirm the working tree is clean.** If there are uncommitted changes, stop and tell the user to stash or commit first — bisect checks out old commits and would clobber or be blocked by them.
2. **Establish a "bad" and a "good" ref.** "Bad" is usually `HEAD`. For "good", use the ref the user named, or help find a plausible older commit/tag where the behavior worked. Verify the assumption if cheap (e.g. note when the relevant code was last touched).
3. **Define a precise pass/fail test.** A single command that exits 0 when good and non-zero when bad is ideal (a failing test, a build, a script, a grep on output). Pin this down — a fuzzy "it looks broken" makes bisect unreliable.

### Running the bisect

1. Start: `git bisect start`, then `git bisect bad <bad>` and `git bisect good <good>`.
2. **Prefer `git bisect run <command>`** when a deterministic test command exists — it automates the whole search. Make sure the command's exit code reflects pass/fail (use exit code `125` to skip un-testable commits, e.g. ones that don't build for unrelated reasons).
3. If the test must be manual, check out each step, have the user test, and relay `git bisect good` / `git bisect bad` per step.
4. When bisect names the first bad commit, **`git bisect reset`** to restore the original `HEAD` — always clean up, even if interrupted.

### After finding it

1. Show the offending commit: `git show <sha> --stat`, then read the actual diff to explain *why* it caused the regression.
2. Summarize: the first bad commit, what it changed, the likely mechanism of the break, and a suggested fix or revert (`git revert <sha>` for a clean undo).
3. If the cause is subtle, hand off to the `debug` skill to drive the fix.

### Rules

1. Never run bisect with a dirty working tree. Always `git bisect reset` when done or on any error.
2. Keep the pass/fail test deterministic and fast — flaky tests give wrong answers. Use `git bisect skip` for commits that genuinely can't be tested.
3. Don't modify code during the bisect; this is diagnosis. Propose the fix separately once the commit is found.
