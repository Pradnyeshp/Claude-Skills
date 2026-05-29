---
name: docstring
description: Add or update documentation comments (docstrings, JSDoc, etc.) for changed or selected code, matching the project's existing style. Use when the user asks to document code, add docstrings, says "add JSDoc", "document this function", "write doc comments", or "add comments to the changes".
argument-hint: "[optional file or symbol to document]"
allowed-tools: Bash, Read, Edit, Glob, Grep
disable-model-invocation: false
---

## Changed code (working tree + staged)

!`git diff HEAD --stat 2>/dev/null || echo "No git changes detected"`

!`git diff HEAD 2>/dev/null | head -300`

## Instructions

Add or improve documentation comments for the changed code above (or for `$ARGUMENTS` if a file/symbol was given).

### Rules

1. **Match the project's existing convention.** Read a neighboring already-documented function first and mirror its format exactly — JSDoc/TSDoc for JS/TS, Google or NumPy style for Python, `///` doc comments for Rust, GoDoc comments for Go, Javadoc for Java. Do not introduce a new style.
2. **Document the public surface** of changed code: every exported/public function, class, and module that lacks a current, accurate doc comment.
3. For each, cover: a one-line summary of purpose, parameters (with types if the language convention includes them), return value, raised/thrown errors, and any important side effects.
4. **Describe behavior and intent, not the obvious.** Explain *why* and the contract — never restate the code line by line. Skip comments that add no information.
5. **Update stale docs.** If an existing docstring no longer matches the changed signature or behavior, correct it.
6. Apply edits directly to the files. Do not reformat or touch unrelated code.
7. After editing, give a one-line summary of which symbols were documented or updated.
