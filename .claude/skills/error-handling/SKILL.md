---
name: error-handling
description: Audit and harden error handling in a file or module — swallowed exceptions, unhandled rejections, missing boundaries, bare catches, leaked internals — and fix the gaps. Use when the user says "improve error handling", "audit error handling", "handle errors properly", "fix swallowed exceptions", "add error boundaries", or "make this more robust".
argument-hint: "[optional file/module/path to focus on, e.g. 'src/api/']"
allowed-tools: Bash, Read, Edit, Grep, Glob
disable-model-invocation: false
---

## Error-handling hotspots

!`grep -rnE "catch ?\\([^)]*\\) ?\\{ ?\\}|except:|except Exception: ?pass|catch \\{ ?\\}|rescue ?=> ?nil" --include='*.*' . 2>/dev/null | grep -vE 'node_modules|\.git|dist|build|test' | head -20`

!`grep -rlE "async |await |\\.then\\(|Promise" --include='*.ts' --include='*.js' . 2>/dev/null | grep -vE 'node_modules|\.git|dist|build' | head -10`

## Instructions

Audit error handling in `$ARGUMENTS` (or the highest-risk modules — I/O, network, parsing, async boundaries — if none given) and fix the real gaps. Match the project's existing error conventions.

### What to look for

1. **Swallowed errors** — empty `catch`/`except: pass`/`rescue nil` that hide failures; catches that log nothing and continue in a broken state.
2. **Over-broad catches** — catching everything when only a specific error is expected, masking bugs (e.g. catching a `TypeError` you meant to let crash). Catch narrowly.
3. **Unhandled async** — un-awaited promises, missing `.catch`, fire-and-forget tasks, unhandled rejections, `async` functions whose throws nobody handles.
4. **Missing boundaries** — no top-level handler for a request/job/CLI; UI without an error boundary; resources (files, connections, locks) not released on the error path (use `finally`/`with`/`defer`/RAII).
5. **Lost context** — re-throwing that erases the stack or original cause (use error chaining: `raise ... from e`, `{ cause }`); generic messages that don't say what failed.
6. **Leaked internals** — raw exceptions, stack traces, or DB errors surfaced to users/clients instead of a safe message + logged detail.
7. **Control flow via exceptions** — using exceptions for normal, expected outcomes where a return/Result type is clearer.

### Method

1. Read the code and identify concrete issues with `file:line`, explaining what fails and the consequence (silent data loss, crash, leak, hang).
2. **Fix the clear ones** preserving behavior on the success path: narrow the catch, handle or propagate intentionally, await/return promises, add `finally` cleanup, chain the cause, replace a leaked internal with a safe message + log.
3. **Don't invent a logging or error framework.** Use what the project already uses (its logger, error types, Result/Either). If there's no convention for something (e.g. no top-level handler exists), propose one and confirm before adding it broadly.

### Rules

1. Never make an error path quieter — removing or weakening handling is the opposite of the goal. Every error should end up handled, propagated deliberately, or logged with context; never silently dropped.
2. Catch as narrowly as the situation allows; don't blanket-catch to make code "safe" — that hides bugs.
3. Preserve the original error and its stack/cause when re-throwing or wrapping.
4. Match the project's existing error types, logger, and patterns rather than introducing new ones unprompted.
5. Summarize: issues found by severity, what you fixed, and any places that need a human decision (retry policy, user-facing copy, whether a failure should be fatal).
