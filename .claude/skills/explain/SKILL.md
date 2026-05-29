---
name: explain
description: Explain a file, function, or recent diff in plain language — what it does, how it flows, and why. Use when the user asks to explain code, says "what does this do", "walk me through this file", "help me understand this", "explain the diff", or is onboarding to unfamiliar code.
argument-hint: "[file path, function name, or 'diff']"
allowed-tools: Bash, Read, Glob, Grep
disable-model-invocation: false
---

## Recent diff (used when the user asks to explain "the diff" or "the changes")

!`git diff HEAD --stat 2>/dev/null || echo "No git changes detected"`

## Instructions

Explain the target the user named in `$ARGUMENTS` (a file path, a function/symbol name, or "diff"/"changes" to explain recent edits). If no target was given, ask what they'd like explained.

### Approach

1. **Read before explaining.** Open the relevant file(s). For a symbol, use Grep to find its definition and key call sites. For "diff", run `git diff HEAD` and explain those changes.
2. Lead with a **one-sentence summary** of what the code does and why it exists.
3. Then give a **structured walkthrough**:
   - Inputs and outputs (parameters, return values, side effects)
   - The main control flow, step by step
   - Key data structures or algorithms involved
   - External dependencies it touches (DB, network, files, other modules)
4. Call out anything **non-obvious or surprising** — implicit assumptions, edge-case handling, performance characteristics, or footguns.
5. If the code looks buggy or fragile, note it briefly at the end, but don't turn this into a full review.

### Rules

1. Match the explanation depth to the audience — assume a competent engineer new to *this* codebase, not new to programming.
2. Reference real symbols and `file:line` locations; don't speak in generalities.
3. Use short paragraphs and bullet points. Include a tiny annotated snippet only when it clarifies a tricky part.
4. Do not modify any files — this skill is read-only.
