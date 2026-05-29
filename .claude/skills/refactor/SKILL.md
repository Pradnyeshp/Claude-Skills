---
name: refactor
description: Restructure a file, function, or module toward a stated goal (readability, decoupling, extracting logic, reducing duplication) without changing its behavior. Use when the user says "refactor this", "clean up this function", "extract this into", "decouple", "restructure", or "make this more readable".
argument-hint: "[target file/symbol] [goal, e.g. 'extract the validation logic']"
allowed-tools: Bash, Read, Edit, Grep, Glob
disable-model-invocation: false
---

## Test setup (used to verify behavior is preserved)

!`ls package.json pyproject.toml Cargo.toml go.mod pom.xml build.gradle Makefile 2>/dev/null`

## Instructions

Refactor the target named in `$ARGUMENTS` toward the stated goal. If the target or goal is unclear, ask which code to refactor and what outcome they want before touching anything.

### Core principle

**Behavior must not change.** A refactor changes how code is expressed, never what it does. Public APIs, return values, and side effects stay identical unless the user explicitly asks otherwise.

### Method

1. **Read first.** Open the target and its call sites (use Grep). Understand the current behavior and who depends on it before changing it.
2. **Establish a safety net.** Identify the tests covering this code. If none exist and the change is non-trivial, say so and offer to add characterization tests first (the `test-gen` skill can help).
3. **Make small, reviewable moves** toward the goal: extract functions/variables, rename for clarity, remove duplication, simplify conditionals, separate concerns. Keep each change focused.
4. **Update all call sites and imports** affected by the change. Don't leave the codebase in a broken intermediate state.
5. **Verify.** Run the relevant tests / type-checker / linter and confirm they still pass.

### Rules

1. Preserve behavior, signatures, and side effects. Flag explicitly if a change is unavoidably behavior-altering.
2. Don't gold-plate — make the change the goal requires, not a sweeping rewrite of unrelated code.
3. Match the project's existing style and idioms; don't introduce new patterns or dependencies just to refactor.
4. Work in coherent steps and explain each. If the refactor is large, outline the plan and confirm before applying.
5. End with a summary of what moved/changed and the verification result.
