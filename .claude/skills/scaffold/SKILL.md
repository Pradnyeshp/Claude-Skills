---
name: scaffold
description: Generate boilerplate for a new file, component, module, endpoint, or test by following the project's existing conventions. Use when the user says "scaffold a", "create a new component/module/endpoint", "generate boilerplate for", "set up a new", or "stub out".
argument-hint: "[what to create, e.g. 'a UserCard React component' or 'a /health API endpoint']"
allowed-tools: Bash, Read, Write, Glob, Grep
disable-model-invocation: false
---

## Project layout & config

!`ls 2>/dev/null`

!`ls package.json pyproject.toml Cargo.toml go.mod tsconfig.json 2>/dev/null`

## Instructions

Scaffold what the user described in `$ARGUMENTS`. If it's unclear what to create or where, ask for the type and intended location before generating files.

### Method

1. **Find a sibling to copy from.** Locate an existing file of the same kind (another component, route, model, test) with Glob/Grep and read it. The existing code — not generic templates — defines the conventions: directory, file naming, imports, export style, typing, framework idioms.
2. **Mirror those conventions exactly.** Match indentation, quote style, naming case, and structure. Place new files where siblings live.
3. **Generate the minimum useful skeleton** — correct imports, the declaration, a sensible default structure, and clearly marked `TODO` placeholders where the user must fill in logic. Don't invent business logic.
4. **Wire it up** only where the project's pattern makes it obvious and low-risk (e.g. add an export to an index barrel, register a route) — and say what you wired.
5. **Create the companion test file** if the project conventionally pairs tests with this file type.

### Rules

1. Follow existing conventions over any external "best practice." When two patterns exist, match the most recent / most common one and note the choice.
2. Keep generated logic minimal — skeletons with TODOs, not guessed implementations.
3. Don't add new dependencies or config unless the user asked.
4. List every file you created and any wiring you did. Mention the next step the user needs to take.
