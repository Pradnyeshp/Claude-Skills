# Claude-Skills

Collection of helpful Claude Code skills for software development.

## Skills

| Skill | Command | Description |
| ----- | ------- | ----------- |
| [Commit Message](/.claude/skills/commit-message/SKILL.md) | `/commit-message` | Generate conventional commit messages from staged changes |
| [PR Description](/.claude/skills/pr-description/SKILL.md) | `/pr-description` | Generate PR title and description from branch diff |
| [Changelog](/.claude/skills/changelog/SKILL.md) | `/changelog 1.2.0` | Generate changelog entries from recent commits |
| [Test Gen](/.claude/skills/test-gen/SKILL.md) | `/test-gen` | Generate unit tests for changed code, matching the project's test style |
| [Review Diff](/.claude/skills/review-diff/SKILL.md) | `/review-diff` | Review the branch/working-tree diff for bugs, security, and style issues |
| [Explain](/.claude/skills/explain/SKILL.md) | `/explain <file\|symbol\|diff>` | Explain a file, function, or diff in plain language |
| [Docstring](/.claude/skills/docstring/SKILL.md) | `/docstring` | Add or update doc comments for changed code in the project's style |

## Installation

### Option 1: Copy to your project (project-level)

Copy the `.claude/skills/` folder into your project root:

```bash
cp -r .claude/skills/ /path/to/your/project/.claude/skills/
```

The skills will be available as `/commit-message`, `/pr-description`, and `/changelog` inside that project.

### Option 2: Install globally (all projects)

Copy the skill folders to your global Claude config:

```bash
cp -r .claude/skills/* ~/.claude/skills/
```

The skills will be available in every Claude Code session.

## Usage

These skills support **two invocation methods** — use whichever feels natural:

### Slash commands (explicit)

```text
/commit-message          # generates message from staged changes
/pr-description          # generates PR title + body from branch diff
/changelog 2.1.0         # generates changelog entry for version 2.1.0
/test-gen                # writes tests for your changed code
/review-diff             # reviews the diff for bugs, security, style
/explain src/auth.ts     # explains a file, symbol, or "diff" in plain English
/docstring               # adds/updates doc comments for changed code
```

### Natural language (conversational)

Just ask Claude in plain English — it will automatically detect and invoke the matching skill:

```text
> write a commit message for my staged changes
> what should the commit message be
> prepare a commit

> draft a PR description
> what should the PR say
> open a pull request

> generate release notes
> what changed recently
> prepare a release for version 2.1.0

> write tests for my changes
> what's untested in this file

> review my code before I commit
> spot bugs in the diff

> what does this function do
> walk me through src/auth.ts

> add docstrings to the changed code
> document this function
```

Both methods produce identical results. Slash commands are faster for muscle memory; natural language is easier when you don't remember the exact command name.

## How Claude Code Skills Work

Each skill is a `SKILL.md` file with YAML frontmatter and markdown instructions. Key features:

- **Dynamic context**: Lines starting with `` !`command` `` run before Claude sees the skill, injecting live data (e.g., `git diff`)
- **Arguments**: `$ARGUMENTS` captures what the user types after the command
- **Tool permissions**: `allowed-tools` pre-approves tools so Claude doesn't ask for permission
- **Auto-invocation**: `disable-model-invocation: false` allows Claude to trigger the skill automatically when it matches your natural language prompt. Set to `true` if you want slash-command-only invocation.

See [Claude Code Skills docs](https://code.claude.com/docs/en/skills) for the full reference.
