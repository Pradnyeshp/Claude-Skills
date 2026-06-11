---
name: benchmark
description: Measure the runtime, throughput, or memory of a function, endpoint, or command — establish a baseline and report the numbers, using the project's benchmark tooling. Use when the user says "benchmark this", "how fast is this", "measure performance", "time this function", "set up a benchmark", or "what's the baseline".
argument-hint: "[target to measure, e.g. a function/file/endpoint, and optional input size]"
allowed-tools: Bash, Read, Write, Grep, Glob
disable-model-invocation: false
---

## Bench tooling signals

!`ls package.json pyproject.toml Cargo.toml go.mod 2>/dev/null`

!`ls benches bench benchmarks 2>/dev/null && echo "(existing benchmarks above — extend them)"`

## Instructions

Benchmark the target in `$ARGUMENTS`. If no target is given, ask what to measure and what "fast enough" means (the workload, input size, and the metric that matters — latency, throughput, or memory).

### Method

1. **Pick the right tool** for the stack, preferring one already in use:
   - **JS/TS:** `vitest bench`, `tinybench`, `benchmark.js`, or `hyperfine` for CLI commands.
   - **Python:** `pytest-benchmark`, `timeit`, or `hyperfine` for scripts.
   - **Rust:** `cargo bench` (criterion).
   - **Go:** `go test -bench=. -benchmem`.
   - For any whole-command timing, `hyperfine` is a good language-agnostic default.
2. **Write a focused benchmark** that exercises the real target with representative input. Isolate the work being measured (set up data outside the timed loop), and use a realistic input size — note it explicitly. Warm up where the runtime/JIT makes cold runs misleading.
3. **Measure stably.** Run enough iterations for a stable result, report central tendency *and* spread (mean/median + stddev or p95, not a single run), and note the environment (machine, runtime version) since absolute numbers aren't portable.
4. **Report the baseline** as a small table: target, input size, metric, and the numbers. If comparing two implementations or before/after, run both under the same harness and report the delta with the relative change.

### Rules

1. Measure, don't estimate — report numbers from an actual run, with the iteration count and spread, not a single noisy sample.
2. Keep setup/teardown out of the timed region; benchmark the work, not the fixture.
3. State the conditions (input size, hardware, runtime version) — a number without them is meaningless and non-reproducible.
4. Don't change the code being measured in this pass; this is measurement. Hand off to the `optimize` skill to act on a bottleneck the baseline reveals.
5. Beware microbenchmark traps: dead-code elimination removing the work, unrealistic all-cache-hot inputs, and measuring the harness instead of the target. Call out anything that makes the result suspect.
