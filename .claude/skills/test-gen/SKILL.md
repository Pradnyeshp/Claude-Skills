---
name: test-gen
description: Generate unit tests for changed or untested code, matching the project's existing test style. Use when the user asks to write tests, add test coverage, says "test this", "generate unit tests", "cover the changes with tests", or "what's untested".
argument-hint: "[optional file or path to focus on]"
allowed-tools: Bash, Read, Glob, Grep
disable-model-invocation: false
---

## Changed code (working tree + staged)

!`git diff HEAD --stat 2>/dev/null || echo "No git changes detected"`

!`git diff HEAD 2>/dev/null | head -400`

## Detected test setup

!`ls package.json pyproject.toml Cargo.toml go.mod pom.xml build.gradle 2>/dev/null`

!`find . -type d \( -name node_modules -o -name .git -o -name dist -o -name build \) -prune -o -type f \( -name '*.test.*' -o -name '*.spec.*' -o -name 'test_*.py' -o -name '*_test.go' -o -name '*_test.rs' \) -print 2>/dev/null | head -15`

## Instructions

Generate unit tests for the changed code shown above (or for `$ARGUMENTS` if a file/path was provided).

### Rules

1. **Detect the framework first.** Infer the test runner and style from the detected setup and an existing test file (Jest/Vitest for JS/TS, pytest for Python, `go test` for Go, `cargo test` for Rust, JUnit for Java). Match the existing imports, assertion style, file naming, and directory layout exactly — do not introduce a new framework.
2. **Focus on what changed.** Test new and modified functions/branches. Do not regenerate tests for unrelated existing code.
3. **Cover meaningfully:** the happy path, at least one edge case (empty/null/boundary), and error handling where the code can throw. Skip trivial getters.
4. **Name tests descriptively** — state the behavior under test, not the function name (e.g. `returns 0 for an empty cart`, not `test_total`).
5. Use existing fixtures, factories, or mocks where the project already provides them. Read a neighboring test file before inventing helpers.
6. **Place tests in the conventional location** for this project. State the file path before each test block.
7. If you cannot determine the framework with confidence, ask which one to use rather than guessing.
8. After writing, print the exact command to run the new tests.
