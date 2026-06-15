---
name: a11y
description: Audit the UI for accessibility problems — missing labels, alt text, contrast, keyboard traps, ARIA misuse, semantic structure — and fix them against WCAG. Use when the user says "check accessibility", "audit a11y", "is this accessible", "fix accessibility issues", "add aria labels", "screen reader support", or "WCAG compliance".
argument-hint: "[optional component/page/path to focus on, e.g. 'src/components/Modal.tsx']"
allowed-tools: Bash, Read, Edit, Grep, Glob
disable-model-invocation: false
---

## UI surface & tooling

!`grep -rilE "react|vue|svelte|angular|<template|\.tsx|jsx" package.json 2>/dev/null | head`

!`ls node_modules/.bin/axe node_modules/.bin/eslint 2>/dev/null && grep -rl "jsx-a11y\|eslint-plugin-vuejs-accessibility" package.json .eslintrc* eslint.config.* 2>/dev/null | head`

## Instructions

Audit the UI in `$ARGUMENTS` (or the main components if none given) for accessibility issues and fix the clear ones. Anchor findings to **WCAG 2.1 AA**.

### What to check

1. **Text alternatives** — `<img>` without `alt` (and decorative images that should have `alt=""`), icon-only buttons/links with no accessible name, `<svg>` without a title/`aria-label`.
2. **Semantic structure** — real headings in order (no skipped levels), landmarks (`main`/`nav`/`header`), lists for lists, `<button>` vs `<a>` used for the right job (action vs navigation) instead of clickable `<div>`s.
3. **Forms** — every input has an associated `<label>` (or `aria-label`/`aria-labelledby`), required/invalid states exposed (`aria-invalid`, `aria-describedby` for errors), grouped controls in `<fieldset>`/`<legend>`.
4. **Keyboard & focus** — everything interactive is reachable and operable by keyboard, no `tabindex > 0`, visible focus styles, focus is managed for modals/menus (trap while open, restore on close), no keyboard traps.
5. **ARIA correctness** — prefer native elements over ARIA; where ARIA is used, roles/states are valid and not contradicting native semantics (the first rule of ARIA: don't use ARIA if a native element works).
6. **Color & contrast** — text/background contrast meets AA (4.5:1 normal, 3:1 large); meaning not conveyed by color alone.
7. **Media & motion** — captions/transcripts for media, and respect `prefers-reduced-motion` for animations.

### Method

1. Read the components and identify real violations with `file:line`. Use an automated checker (`axe`, `eslint-plugin-jsx-a11y`) if configured — but automation catches ~a third of issues, so reason through the rest by reading the markup and interaction.
2. **Fix the unambiguous issues** (missing `alt`, unlabeled inputs, `div` that should be a `button`, missing focus management) preserving behavior and styling.
3. **Flag judgment calls** rather than guessing — contrast that needs a design decision, alt text whose correct wording depends on intent, an interaction pattern that needs rework.

### Rules

1. Prefer native semantic HTML over ARIA; only add ARIA when no native element expresses the semantics, and keep it valid.
2. Don't change visual design or behavior beyond what the fix requires; surface contrast/wording decisions to the user instead of inventing them.
3. Tie each finding to what it breaks for a real user (screen reader, keyboard-only, low vision) and the WCAG criterion — not just "best practice".
4. Automated tools are a floor, not a ceiling — state that keyboard/screen-reader testing is still needed for anything you couldn't verify statically.
5. Summarize: issues found by severity, what you fixed, and what needs a human decision or manual assistive-tech testing.
