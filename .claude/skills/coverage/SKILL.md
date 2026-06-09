---
name: coverage
description: Run the test suite with coverage and report the least-covered files and functions, with concrete suggestions for the next tests to write. Use when the user says "check test coverage", "what's not tested", "run coverage", "where are the coverage gaps", "how covered is this", or "what should I test next".
argument-hint: "[optional path or module to focus the report on]"
allowed-tools: Bash, Read, Grep, Glob
disable-model-invocation: false
---

## Test tooling signals

!`ls package.json pyproject.toml pytest.ini setup.cfg Cargo.toml go.mod jest.config.* vitest.config.* .nycrc* 2>/dev/null`

!`sed -n 's/.*"scripts".*//p;/"test"\|"coverage"/p' package.json 2>/dev/null | head -20`

## Instructions

Measure test coverage for this project and report where it's weakest (scoped to `$ARGUMENTS` if a path was named). Detect the test runner from the signals above and use its native coverage tooling.

### Method

1. **Pick the right coverage command** for the stack, preferring an existing `coverage`/`test:coverage` script when one exists:
   - **JS/TS:** `jest --coverage`, `vitest run --coverage`, or `nyc <test cmd>`
   - **Python:** `pytest --cov=<pkg> --cov-report=term-missing` (or `coverage run -m pytest && coverage report -m`)
   - **Rust:** `cargo llvm-cov` / `cargo tarpaulin`
   - **Go:** `go test ./... -coverprofile=cover.out && go tool cover -func=cover.out`
   - If the coverage tool isn't installed, say so and give the one-line install/setup instead of guessing numbers.
2. **Run it** (read-only — running tests is fine; don't modify source). Capture the per-file/per-function percentages and the uncovered line ranges.
3. **Rank the gaps by risk, not just by percentage.** A 60%-covered auth/payment/parsing module matters more than a 0%-covered constants file. Weight by how much logic and how much blast radius each uncovered area has. Ignore generated code, vendored deps, and trivial getters.
4. **For the top gaps, name the specific untested behavior** — the branch, error path, or edge case that has no test — by reading the uncovered lines, not just citing a number.

### Output

1. **Overall coverage** (line/branch %) and how it compares to any configured threshold.
2. **Top under-covered areas**, ranked by risk: `file:line-range`, current %, and the specific untested behavior.
3. **A short "test these next" list** — concrete cases worth writing, most valuable first. Hand off to the `test-gen` skill to actually write them if the user wants.

### Rules

1. Report real numbers from a coverage run — never estimate coverage by eyeballing the source.
2. If tests fail or error out, surface that first: coverage from a broken suite is meaningless.
3. Prioritize by risk and logic density, not raw percentage — call out when a high-percentage file still misses its critical path.
4. Don't write or modify tests here; this skill measures and prioritizes. Point to `test-gen` for the writing.
5. If coverage is already strong, say so and note the few remaining gaps rather than manufacturing busywork.
