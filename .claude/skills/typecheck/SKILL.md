---
name: typecheck
description: Run the project's type checker (tsc, mypy, pyright, etc.) and fix the reported type errors at the source, without weakening types or suppressing. Use when the user says "run the type checker", "fix type errors", "make tsc pass", "fix the mypy errors", "typecheck this", or "why won't this compile".
argument-hint: "[optional path/file to limit to, or a specific error to chase]"
allowed-tools: Bash, Read, Edit, Grep, Glob
disable-model-invocation: false
---

## Type checker config

!`ls tsconfig.json jsconfig.json mypy.ini pyrightconfig.json pyproject.toml setup.cfg 2>/dev/null`

!`grep -hiE "strict|noImplicitAny|noUncheckedIndexedAccess|disallow_untyped|warn_return_any" tsconfig.json mypy.ini pyproject.toml 2>/dev/null | head -10`

!`cat package.json 2>/dev/null | grep -A30 '"scripts"' | grep -iE 'typecheck|tsc|type-check' | head`

## Instructions

Run the project's type checker and fix the errors it reports (scoped to `$ARGUMENTS` if given). Use the project's configured checker and strictness — don't impose your own.

### Method

1. **Identify the checker and command** from the config above, preferring an existing script:
   - **TS/JS:** `tsc --noEmit` (or the `typecheck` script); respect the existing `tsconfig` strictness.
   - **Python:** `mypy <pkg>` or `pyright`, per the project's config.
   - If the checker isn't installed, report that and the install command instead of guessing errors.
2. **Run it first** to get the full, real error list and counts. Read the actual diagnostics — don't anticipate errors that aren't reported.
3. **Fix at the root, not the symptom.** Group errors by underlying cause (one wrong type often cascades). For each: read the code and types to understand what's actually true, then correct the type or the code so it's sound — add a missing annotation, narrow a union, fix an incorrect signature, handle a `null`/`undefined` case, import the right type.
4. **A type error can be a real bug.** When the checker is right that a value can be `null`, an access is unsafe, or a branch is unreachable, fix the logic — don't just satisfy the checker. Flag these explicitly.
5. **Re-run until clean** (or until only genuinely-unfixable third-party cases remain), and show the before/after error counts.

### Rules

1. **No silencing to force a pass.** Don't use `any`/`as any`/`@ts-ignore`/`# type: ignore`/`cast` to make errors disappear. A suppression is a last resort only for a real tooling/library gap — narrowly scoped, with a comment explaining why, and called out in the summary.
2. Don't loosen the project's config (strict flags, etc.) to reduce errors. If a setting seems wrong, raise it with the user rather than editing it.
3. Preserve runtime behavior unless a type error reveals a genuine bug — in which case fix the bug and say so. Don't change logic just to dodge a type.
4. Prefer precise fixes (real types, narrowing, generics) over broadening to a supertype that hides the problem.
5. Summarize: the checker run, errors fixed grouped by cause, any real bugs uncovered, the remaining count, and anything suppressed and why.
