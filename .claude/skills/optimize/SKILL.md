---
name: optimize
description: Find and fix performance bottlenecks in a function, file, or hot path — slow loops, N+1 queries, redundant work, bad complexity, excess allocations. Use when the user says "optimize this", "this is slow", "improve performance", "speed this up", "why is this slow", or "reduce latency/memory".
argument-hint: "[target file/function, and any known symptom like 'slow on large inputs']"
allowed-tools: Bash, Read, Edit, Grep, Glob
disable-model-invocation: false
---

## Test setup (used to confirm behavior is preserved after optimizing)

!`ls package.json pyproject.toml Cargo.toml go.mod Makefile 2>/dev/null`

## Instructions

Optimize the target in `$ARGUMENTS`. If no target is given, ask what's slow and how it's measured (input size, latency observed, profiler output).

### Method — measure, don't guess

1. **Establish the cost.** Identify what "slow" means here: time complexity, query count, allocations, I/O, or wall-clock. Use any profiler output, benchmark, or timing the user has. If none exists, reason explicitly about the dominant cost — and say it's an estimate.
2. **Find the real bottleneck.** Read the hot path and locate where the time/memory actually goes. Common culprits: nested loops (O(n²)), N+1 queries, repeated work that could be hoisted or memoized, unnecessary copies/allocations, sync I/O in a loop, missing indexes, reprocessing unchanged data.
3. **Optimize the dominant cost first.** A 10× win on 5% of runtime is noise. Target the part that actually dominates. Prefer algorithmic/structural wins (better data structure, batching, caching) over micro-tuning.
4. **Preserve behavior.** The optimized code must produce identical results. Keep the public interface stable.
5. **Verify.** Run the tests to confirm correctness. If a benchmark exists, run it before and after and report the delta; otherwise explain the expected improvement (e.g. "O(n²) → O(n log n)").

### Rules

1. Never trade correctness for speed. Flag any change that alters edge-case behavior.
2. Don't micro-optimize readable code for negligible gains — call it out if the bottleneck is elsewhere (or not worth fixing).
3. Note any trade-offs introduced (added memory for caching, added complexity, eventual consistency).
4. End with: what was slow, what you changed, and the measured or expected impact.
