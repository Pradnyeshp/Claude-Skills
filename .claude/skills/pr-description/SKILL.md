---
name: pr-description
description: Generate a pull request title and description from the current branch diff. Use when the user asks to create a PR, write a PR description, says "open a PR", "draft a PR", "what should the PR say", or "prepare a pull request".
argument-hint: ""
allowed-tools: Bash, Read
disable-model-invocation: false
---

## Branch info

!`git branch --show-current`

!`git log --oneline main..HEAD 2>/dev/null || git log --oneline origin/main..HEAD 2>/dev/null || echo "Could not determine base branch"`

## Full diff from base

!`git diff main...HEAD --stat 2>/dev/null || git diff origin/main...HEAD --stat 2>/dev/null`

## Instructions

Generate a PR title and description from the changes on this branch.

### Output format

```markdown
## Title
<imperative mood, under 70 chars>

## Summary
- <bullet 1: what changed and why>
- <bullet 2: what changed and why>
- <bullet 3 if needed>

## Test plan
- [ ] <how to verify this works>
- [ ] <edge cases to check>
```

### Rules

1. Title is imperative mood, under 70 characters, no period
2. Summary bullets focus on *why*, not *what* — the diff shows what
3. Group related commits into a single bullet
4. Include a test plan with concrete verification steps
5. If the diff is empty or the branch has no commits ahead of main, say so
6. Do NOT include the markdown fences shown above — output raw markdown
