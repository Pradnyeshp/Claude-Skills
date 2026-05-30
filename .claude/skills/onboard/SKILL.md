---
name: onboard
description: Orient a developer to an unfamiliar codebase — how to build and run it, the high-level architecture, key directories, and where to start. Use when the user says "help me understand this repo", "onboard me", "what is this project", "how do I run this", "give me the lay of the land", or "where do I start".
argument-hint: "[optional subsystem or area to focus on]"
allowed-tools: Bash, Read, Glob, Grep
disable-model-invocation: false
---

## Project signals

!`ls 2>/dev/null`

!`cat README* 2>/dev/null | head -60`

!`ls package.json pyproject.toml Cargo.toml go.mod pom.xml Makefile docker-compose.yml .env.example 2>/dev/null`

## Instructions

Produce a concise orientation guide to this codebase (focused on `$ARGUMENTS` if an area was named). This is for a competent engineer who has never seen this repo — help them become productive fast.

### What to cover

1. **What it is** — one paragraph: the project's purpose and what it does, inferred from the README, manifests, and entry points.
2. **Tech stack** — languages, frameworks, runtime, datastore, and notable libraries, read from the manifests and config.
3. **How to run it** — the actual setup, build, run, and test commands. Pull these from `scripts` in package.json, a Makefile, CONTRIBUTING docs, or CI config. Note required env vars (check `.env.example`) and services (e.g. docker-compose).
4. **Architecture map** — the top-level directories and what each is responsible for. Identify the entry point(s) and trace the main flow at a high level (request → handler → service → data, or equivalent).
5. **Where to start** — point to the 3–5 most important files to read first, and call out conventions a newcomer must know (testing approach, module boundaries, naming).

### Rules

1. Read before asserting — open the entry point and a few key files; don't guess the architecture from names alone.
2. Cite real paths (`src/server.ts:1`) so the reader can jump straight there.
3. Prefer commands you can verify exist (in scripts/Makefile/CI) over invented ones. If you can't confirm how to run it, say so and show your best guess clearly labeled.
4. Keep it skimmable — headings, short bullets, a couple of `file:line` anchors. This is a map, not an essay.
5. Do not modify any files — this skill is read-only.
