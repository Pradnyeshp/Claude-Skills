---
name: codeowners
description: Generate or update a CODEOWNERS file mapping paths to owning people or teams, so the right reviewers are auto-requested on PRs. Use when the user says "add a CODEOWNERS file", "set up code owners", "who should review which files", "auto-assign reviewers", or "map directories to teams".
argument-hint: "[optional: owners/teams to assign, or a path to focus on, e.g. 'frontend → @web-team']"
allowed-tools: Bash, Read, Write, Grep, Glob
disable-model-invocation: false
---

## Ownership signals

!`ls CODEOWNERS .github/CODEOWNERS docs/CODEOWNERS 2>/dev/null && echo "(existing CODEOWNERS above — update it, don't replace blindly)"`

!`ls -d */ 2>/dev/null | head -30`

!`git shortlog -sne --all 2>/dev/null | head -15`

## Instructions

Generate or update a `CODEOWNERS` file. Use the owners/teams in `$ARGUMENTS` if given; otherwise propose a structure from the repo layout and ask the user to fill in the actual owners — **don't invent team or user handles**.

### Method

1. **Read the repo structure** (top-level dirs and the major subsystems) to identify the areas that warrant distinct ownership — frontend, backend, infra, docs, CI config, shared libs. The `git shortlog` above hints at who works where, but ownership is a human/policy decision: use it only as a suggestion, never as the assignment.
2. **Decide create vs update.** If a CODEOWNERS exists, preserve its existing rules and only add/adjust what's missing. Otherwise create one at the conventional path (`.github/CODEOWNERS` for GitHub; `CODEOWNERS` at root, or GitLab's `.gitlab/CODEOWNERS`).
3. **Write rules most-general to most-specific.** The **last matching pattern wins** (GitHub semantics), so put a catch-all `*` default at the top and progressively more specific paths below it. Use the platform's path syntax (gitignore-style globs, leading `/` to anchor, trailing `/` for directories).
4. **Assign real owners** — `@org/team` or `@user` handles the user provides. Where the user hasn't named an owner for an area, leave a clearly-marked `# TODO: owner` placeholder rather than guessing a handle that may not exist.
5. **Keep it maintainable** — prefer teams over individuals (resilient to people leaving), group related paths, and don't over-specify every file. Cover the high-traffic and sensitive areas (auth, infra, CI, security) deliberately.

### Rules

1. Never invent owner handles — use only the teams/users the user supplies; mark unknown owners as a `# TODO` for the maintainer to fill.
2. Order rules correctly for the platform (last-match-wins on GitHub): general defaults first, specific overrides last, or the specific rules get shadowed.
3. Validate that every owner is a syntactically valid handle and every path pattern matches something real in the repo; flag patterns that match nothing.
4. Preserve existing rules when updating; don't drop ownership someone is relying on.
5. After writing, summarize the mapping, note that owners must have write access for auto-request to work, and list any `# TODO` placeholders the user still needs to fill.
