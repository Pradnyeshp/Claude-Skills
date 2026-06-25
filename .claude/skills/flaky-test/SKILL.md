---
name: flaky-test
description: Track down and stabilize a flaky test — one that passes and fails non-deterministically — by finding the source of nondeterminism (timing, ordering, shared state, randomness, real I/O) and fixing the root cause, not by adding retries. Use when the user says "this test is flaky", "fix the flaky test", "the test passes sometimes", "stabilize this test", "why does this test fail intermittently", or "the suite is non-deterministic".
argument-hint: "[the flaky test or file, e.g. 'the checkout integration test' or 'tests/api/users.test.ts']"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
disable-model-invocation: false
---

## Test setup signals

!`grep -rilE "jest|vitest|mocha|playwright|cypress|pytest|unittest|rspec|go test|junit|testng" package.json pyproject.toml go.mod Gemfile pom.xml 2>/dev/null | grep -vE 'node_modules|\.git' | head -6`

!`grep -rlnE "setTimeout|sleep|Date\\.now|new Date\\(\\)|Math\\.random|time\\.sleep|datetime\\.now|waitFor|page\\.wait" --include='*test*' --include='*spec*' . 2>/dev/null | grep -vE 'node_modules|\.git' | head -8`

## Instructions

Stabilize the flaky test in `$ARGUMENTS`. The goal is to find and remove the source of nondeterminism — not to mask it with a retry or a longer sleep. If you can't reproduce or identify the cause, say so and propose how to surface it rather than guessing.

### Method

1. **Reproduce the flake.** Run the test in a loop and, where relevant, with randomized order and parallelism to surface it (e.g. repeated runs, `--shuffle`/random seed, `-p`/concurrency). A flake you can't trigger you can't confirm fixed — note the failure rate before and after.
2. **Classify the root cause.** Common sources:
   - **Timing/async** — fixed `sleep`s and races; the test asserts before the work settles.
   - **Order/shared state** — tests leak state (DB rows, globals, files, env) and depend on run order.
   - **Time/randomness** — real `Date.now()`/`Math.random()`/UUIDs not frozen or seeded.
   - **Real I/O/network** — hitting a live service, real clock, or unmocked dependency.
   - **Floating-point / unordered collections** — comparing maps/sets or floats by exact equality.
3. **Fix the cause, not the symptom.** Replace sleeps with deterministic waits on a condition/event; freeze time (fake timers/clock) and seed randomness; isolate state with proper setup/teardown so each test is independent of order; mock external I/O. Make assertions order-independent for unordered data.
4. **Verify it's actually fixed.** Re-run the loop (and shuffled/parallel) many times — the failure rate should go to zero. Don't declare victory on a single green run; a flake by definition passes sometimes.
5. **Retry is a last resort, not the fix.** Only after the root cause is genuinely environmental and outside the test's control (and you've said so) should you fall back to a bounded, documented retry — never as a substitute for fixing real test logic.

### Rules

1. Find and remove the source of nondeterminism; never paper over a flake with a longer sleep or a blanket test-retry as the primary fix.
2. Reproduce the flake first (loops, shuffled order, parallelism) and measure the failure rate before/after — don't claim a fix from one passing run.
3. Replace sleeps with condition-based waits, freeze time and seed randomness, mock real I/O, and make tests order-independent with clean setup/teardown.
4. Keep the test's intent intact — stabilizing must not weaken what it asserts or turn it into a test that can no longer fail.
5. After fixing, summarize the root cause, the fix, the before/after failure rate, and whether any documented retry remains and why.
