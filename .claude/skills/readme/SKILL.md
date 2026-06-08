---
name: readme
description: Generate or update a project README from the codebase — what it is, how to install, run, test, and configure it. Use when the user says "write a README", "generate a readme", "update the README", "document this project", "my README is out of date", or "create project docs".
argument-hint: "[optional section to focus on, e.g. 'installation' or 'usage']"
allowed-tools: Bash, Read, Write, Grep, Glob
disable-model-invocation: false
---

## Project signals

!`ls 2>/dev/null`

!`cat package.json pyproject.toml Cargo.toml go.mod composer.json 2>/dev/null | head -80`

!`ls Makefile docker-compose.yml Dockerfile .env.example LICENSE* CONTRIBUTING* 2>/dev/null`

!`cat README* 2>/dev/null | head -80`

## Instructions

Generate or update the project's `README.md` (focus on the `$ARGUMENTS` section if one was named). Write for a developer who just landed on the repo and wants to understand and run it quickly.

### Method

1. **Identify the project.** Read the manifests, entry points, and config to determine the name, purpose, language, framework, and runtime. Don't infer purpose from the directory name alone — confirm it in code or existing docs.
2. **Pull real commands.** Take install/build/run/test commands from `scripts` in package.json, a Makefile, `pyproject.toml`/`Cargo.toml`, CI config, or CONTRIBUTING — not from convention. Note required env vars (check `.env.example`) and services (e.g. docker-compose).
3. **Decide create vs update.** If a README already exists, preserve its structure, tone, and any hand-written sections (badges, screenshots, acknowledgements); refresh only what's stale or missing. If none exists, create one from the structure below.
4. **Write `README.md`** at the repo root (or the path the user names).

### Suggested structure

```
# <Project name>

<One-sentence description, then a short paragraph on what it does and why.>

## Features            # optional — only if there are clear, listable capabilities

## Installation        # prerequisites + the actual install steps

## Usage               # the common commands / a minimal code example

## Configuration       # env vars and config files, if any (link to .env.example)

## Development         # build, test, lint commands; how to contribute

## License             # match the LICENSE file if present
```

### Rules

1. Document only what exists. Don't invent features, commands, env vars, or badges. If you can't confirm how to run something, label it clearly as a best guess rather than asserting it.
2. Every command you list must come from a real script/Makefile/CI target — verify it exists before writing it.
3. Match the project's tone and any existing README conventions. Omit sections that don't apply (don't write an empty "License" if there's no license).
4. Keep it skimmable: headings, short paragraphs, fenced code blocks for commands. This is a front door, not a manual.
5. Output raw markdown to the file. After writing, summarize what you created or changed and flag anything you marked as a guess.
