---
name: changelog
description: Generate a changelog entry from recent git commits. Use when the user asks to update the changelog, write release notes, says "prepare a release", "what changed recently", or "generate release notes".
argument-hint: "[version number, e.g. 1.2.0]"
allowed-tools: Bash, Read
disable-model-invocation: false
---

## Recent commits

!`git log --oneline --no-merges -30`

## Instructions

Generate a changelog entry from the commits above.

### Output format

```
## [<version>] - <YYYY-MM-DD>

### Added
- <new features>

### Changed
- <modifications to existing features>

### Fixed
- <bug fixes>

### Removed
- <removed features>
```

### Rules

1. Use the version from `$ARGUMENTS` if provided, otherwise use `Unreleased`
2. Use today's date
3. Group commits into **Added**, **Changed**, **Fixed**, **Removed** sections based on their conventional commit type (`feat` → Added, `fix` → Fixed, `refactor`/`chore` → Changed, etc.)
4. Omit empty sections
5. Rewrite commit subjects into user-friendly language — no commit hashes, no technical jargon
6. If a CHANGELOG.md exists, match its existing style
7. Output raw markdown, no wrapping fences
