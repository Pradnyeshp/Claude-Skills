---
name: type-annotate
description: Add or improve type annotations (Python type hints, TypeScript types, etc.) for untyped or loosely-typed code, matching the project's existing typing style. Use when the user says "add type hints", "add types", "annotate this", "type this function", "fix the any types", or "make this strongly typed".
argument-hint: "[optional file/function to annotate; defaults to the changed code]"
allowed-tools: Bash, Read, Edit, Grep, Glob
disable-model-invocation: false
---

## Changed code (default target) + typing setup

!`git diff HEAD --stat 2>/dev/null || echo "No git changes detected"`

!`ls tsconfig.json mypy.ini pyrightconfig.json .flake8 pyproject.toml 2>/dev/null`

!`grep -hiE "strict|noImplicitAny|disallow_untyped|check_untyped" tsconfig.json mypy.ini pyproject.toml 2>/dev/null | head -10`

## Instructions

Add type annotations to the target in `$ARGUMENTS`, or to the changed code above if none is given.

### Method

1. **Detect the language and type system,** and read the config above to learn how strict the project is (TS `strict`, mypy `disallow_untyped_defs`, etc.). Match that bar — don't under- or over-type relative to the codebase.
2. **Infer types from real usage,** not assumptions: follow how a value is constructed, what's passed in, and what's returned/branched on. Read call sites and existing typed neighbors to match conventions (e.g. project's alias names, `TypedDict` vs dataclass, `interface` vs `type`).
3. **Annotate function signatures first** (params + return), then important locals/containers where the type isn't obvious. Add the smallest set of annotations that makes the code check cleanly and reads clearly.
4. **Prefer precise types over escape hatches.** Replace `any`/`Any`/`object` with a real type, a union, a generic, or a narrowed shape. Use `Optional`/`| None`/`| undefined` where values can be absent. Reach for `unknown` over `any` when truly dynamic, and explain why.
5. **Add or import shared types** rather than duplicating shapes. Reuse the project's existing models/interfaces.

### Rules

1. **Don't change runtime behavior** — annotations only. Flag (don't silently fix) any spot where adding a correct type reveals an actual bug.
2. Don't suppress errors with `# type: ignore` / `@ts-ignore` / `as any` to force a pass — only use a suppression as a last resort, with a comment explaining why, and call it out.
3. Match the project's import and syntax style (e.g. `from __future__ import annotations`, `list[str]` vs `List[str]`, inline vs imported types).
4. **Verify** by running the type checker (`tsc --noEmit`, `mypy`, `pyright`) and report the result. End with what you annotated and any real type errors the new annotations surfaced.
