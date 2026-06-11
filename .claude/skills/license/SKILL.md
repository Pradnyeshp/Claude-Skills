---
name: license
description: Add or update an open-source LICENSE file for the project, filling in the right SPDX license, copyright holder, and year, and optionally inserting license headers into source files. Use when the user says "add a license", "what license should I use", "add MIT/Apache license", "add license headers", or "set up licensing".
argument-hint: "[optional: license id (MIT, Apache-2.0, GPL-3.0, BSD-3-Clause) and/or copyright holder]"
allowed-tools: Bash, Read, Write, Glob, Grep
disable-model-invocation: false
---

## Licensing signals

!`ls LICENSE* COPYING* 2>/dev/null && echo "(a license file already exists — update it, don't blindly overwrite)"`

!`cat package.json composer.json 2>/dev/null | grep -iE '"license"|"author"' | head`

!`git config user.name 2>/dev/null`

## Instructions

Add or update the project's license per `$ARGUMENTS` (license id and/or copyright holder). If no license is named and the manifest doesn't already declare one, ask which license the user wants before writing — licensing is a deliberate legal choice, not a default to guess.

### Method

1. **Determine the license.** Use the id in `$ARGUMENTS`, else the one declared in the manifest (`package.json` `license`, `pyproject.toml`, `Cargo.toml`). If they conflict, surface the conflict and confirm. Don't pick a license on the user's behalf.
2. **Determine holder and year.** Copyright holder from `$ARGUMENTS`, the manifest `author`, or git `user.name`; year is the current year (or `first-current` if an existing header shows an earlier start). Confirm the holder if you had to guess.
3. **Write `LICENSE`** with the exact, unmodified canonical SPDX text, substituting only the bracketed `[year]` and `[holder]` placeholders. Never paraphrase or trim license text.
4. **Keep metadata in sync.** Set/update the `license` field in the manifest to the matching SPDX identifier (e.g. `MIT`, `Apache-2.0`).
5. **License headers (only if asked).** When the user wants per-file headers, insert the short SPDX header (`// SPDX-License-Identifier: MIT` + copyright line) at the top of source files in the project's comment style. Skip vendored/generated files and anything already carrying a header.

### Rules

1. Reproduce canonical license text verbatim — the only edits are the year and copyright-holder placeholders. A modified license is not that license.
2. Don't overwrite an existing LICENSE without confirming; if updating, preserve the original year/holder and the existing license unless the user is intentionally changing it (a license change has implications — call them out).
3. Keep the LICENSE file, manifest `license` field, and any headers all naming the same SPDX id — no drift.
4. You're not a lawyer: when the user is unsure which license fits, briefly describe the common options (MIT = permissive/simple, Apache-2.0 = permissive + patent grant, GPL-3.0 = copyleft) and let them choose — don't decide for them.
5. After writing, report the license chosen, the holder/year used, the files written, and whether headers were added.
