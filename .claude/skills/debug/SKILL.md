---
name: debug
description: Diagnose a bug from a symptom — an error message, stack trace, failing test, or wrong output — find the root cause, and propose a fix. Use when the user says "debug this", "why is this failing", "I'm getting this error", "this isn't working", "track down this bug", or pastes a stack trace.
argument-hint: "[the error message, failing test, or description of the symptom]"
allowed-tools: Bash, Read, Edit, Grep, Glob
disable-model-invocation: false
---

## Recent changes (a common source of new bugs)

!`git diff HEAD --stat 2>/dev/null || echo "Not a git repo or no changes"`

## Instructions

Debug the symptom described in `$ARGUMENTS` (an error, stack trace, failing test, or wrong behavior). If no symptom was given, ask the user for the exact error, the command that triggers it, and the expected vs. actual behavior.

### Method — follow this order, don't jump to a fix

1. **Reproduce.** Identify the exact command or input that triggers the symptom and run it if possible. A bug you can't reproduce, you can't confirm fixed.
2. **Read the evidence.** Parse the stack trace or error to the precise file and line. Open it and read the surrounding code and any functions it calls.
3. **Form hypotheses.** List the most likely root causes, ranked. Consider recent changes (shown above), bad input/null handling, incorrect assumptions, state/ordering, and environment/config.
4. **Isolate.** Narrow down with the cheapest possible check — read the suspect code, add a targeted log, or inspect a value — before changing anything. Confirm *which* hypothesis is correct.
5. **Fix the root cause, not the symptom.** Apply the minimal change that addresses the actual cause. Don't paper over it with a try/catch unless that's genuinely correct.
6. **Verify.** Re-run the reproduction and the relevant tests to confirm the symptom is gone and nothing else broke.

### Rules

1. State your reasoning at each step — show the hypothesis and how you confirmed or ruled it out.
2. Change as little as possible. Remove any temporary debug logging you added before finishing.
3. If the root cause is environmental or external (missing env var, dependency version, network), say so rather than editing code.
4. Distinguish "confirmed fixed (reproduction now passes)" from "likely fixed (couldn't reproduce)" — never overstate.
5. End with a one-line root-cause summary and what the fix changed.
