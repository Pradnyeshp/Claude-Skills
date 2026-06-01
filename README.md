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
| [Debug](/.claude/skills/debug/SKILL.md) | `/debug <symptom>` | Diagnose a bug from an error/stack trace/failing test and fix the root cause |
| [Refactor](/.claude/skills/refactor/SKILL.md) | `/refactor <target> <goal>` | Restructure code toward a goal without changing behavior |
| [Scaffold](/.claude/skills/scaffold/SKILL.md) | `/scaffold <what>` | Generate boilerplate for a new file/component/module from project conventions |
| [Deps](/.claude/skills/deps/SKILL.md) | `/deps` | Audit dependencies for outdated, deprecated, or vulnerable packages |
| [Onboard](/.claude/skills/onboard/SKILL.md) | `/onboard` | Orient to an unfamiliar repo — how to run it, architecture, where to start |
| [Regex](/.claude/skills/regex/SKILL.md) | `/regex <description>` | Build, explain, or debug a regex with examples and test cases |
| [Optimize](/.claude/skills/optimize/SKILL.md) | `/optimize <target>` | Find and fix performance bottlenecks while preserving behavior |
| [Tech Debt](/.claude/skills/tech-debt/SKILL.md) | `/tech-debt` | Scan for TODO/FIXME markers and code smells, triaged into an action list |
| [Dockerize](/.claude/skills/dockerize/SKILL.md) | `/dockerize` | Generate a production-ready Dockerfile, .dockerignore, and optional compose |
| [CI Setup](/.claude/skills/ci-setup/SKILL.md) | `/ci-setup` | Generate a CI pipeline (GitHub Actions) that lints, tests, and builds |
| [SQL](/.claude/skills/sql/SKILL.md) | `/sql <request>` | Write, explain, or optimize a SQL query for the project's dialect |
| [Bisect](/.claude/skills/bisect/SKILL.md) | `/bisect <symptom>` | Find the commit that introduced a regression via git bisect |

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
/debug "TypeError at line 42"  # diagnoses and fixes a bug from the symptom
/refactor utils.py "split the parser out"  # behavior-preserving restructure
/scaffold a UserCard React component       # generates boilerplate from conventions
/deps                    # audits dependencies for outdated/vulnerable packages
/onboard                 # orients you to an unfamiliar repo
/regex "match an email address"  # builds a regex with examples and tests
/optimize parser.js      # finds and fixes performance bottlenecks
/tech-debt               # scans and triages TODOs and code smells
/dockerize               # generates a Dockerfile + .dockerignore for the project
/ci-setup                # generates a CI pipeline (GitHub Actions by default)
/sql "top 10 customers by revenue"  # writes, explains, or optimizes a SQL query
/bisect "login broke since v1.2.0"  # finds the commit that caused a regression
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

> why is this test failing
> I'm getting a NullPointerException here

> refactor this function to be more readable
> extract the validation logic into its own module

> scaffold a new API endpoint for health checks
> create a new React component called Sidebar

> are any of my dependencies out of date
> check for vulnerable packages

> help me understand this repo
> how do I run this project

> write a regex for a valid email
> why doesn't this pattern match

> this function is slow, speed it up
> reduce the latency of this endpoint

> find the tech debt in this codebase
> list all the TODOs and FIXMEs

> dockerize this app
> write a Dockerfile for this project

> set up GitHub Actions for this repo
> add a CI pipeline that runs my tests

> write a SQL query for the top 10 customers by revenue
> why is this query slow

> find the commit that broke login
> bisect this regression since the last release
```

Both methods produce identical results. Slash commands are faster for muscle memory; natural language is easier when you don't remember the exact command name.

## How Claude Code Skills Work

Each skill is a `SKILL.md` file with YAML frontmatter and markdown instructions. Key features:

- **Dynamic context**: Lines starting with `` !`command` `` run before Claude sees the skill, injecting live data (e.g., `git diff`)
- **Arguments**: `$ARGUMENTS` captures what the user types after the command
- **Tool permissions**: `allowed-tools` pre-approves tools so Claude doesn't ask for permission
- **Auto-invocation**: `disable-model-invocation: false` allows Claude to trigger the skill automatically when it matches your natural language prompt. Set to `true` if you want slash-command-only invocation.

See [Claude Code Skills docs](https://code.claude.com/docs/en/skills) for the full reference.
