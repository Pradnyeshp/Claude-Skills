# Claude-Skills

[![CI](https://img.shields.io/github/actions/workflow/status/Pradnyeshp/Claude-Skills/ci.yml?branch=main&label=CI)](https://github.com/Pradnyeshp/Claude-Skills/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/Pradnyeshp/Claude-Skills)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-59-blue)](#skills)
![Last commit](https://img.shields.io/github/last-commit/Pradnyeshp/Claude-Skills)
[![Stars](https://img.shields.io/github/stars/Pradnyeshp/Claude-Skills?style=social)](https://github.com/Pradnyeshp/Claude-Skills/stargazers)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](CONTRIBUTING.md)

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
| [Migrate](/.claude/skills/migrate/SKILL.md) | `/migrate <change>` | Apply a sweeping mechanical change across the codebase, then verify |
| [API Docs](/.claude/skills/api-docs/SKILL.md) | `/api-docs` | Generate OpenAPI or markdown docs from the project's route handlers |
| [Gitignore](/.claude/skills/gitignore/SKILL.md) | `/gitignore` | Generate/tighten .gitignore and flag already-tracked files to untrack |
| [Type Annotate](/.claude/skills/type-annotate/SKILL.md) | `/type-annotate` | Add type hints/annotations matching the project's typing strictness |
| [Env Example](/.claude/skills/env-example/SKILL.md) | `/env-example` | Scan code for env vars and generate/update a safe .env.example |
| [Resolve Conflicts](/.claude/skills/resolve-conflicts/SKILL.md) | `/resolve-conflicts` | Walk through and safely resolve git merge/rebase/cherry-pick conflicts |
| [Lint Fix](/.claude/skills/lint-fix/SKILL.md) | `/lint-fix` | Detect the project's linter/formatter, run it, and fix the findings |
| [Readme](/.claude/skills/readme/SKILL.md) | `/readme` | Generate or update a project README from the codebase |
| [Secrets Scan](/.claude/skills/secrets-scan/SKILL.md) | `/secrets-scan` | Scan the working tree and git history for hardcoded secrets |
| [Release](/.claude/skills/release/SKILL.md) | `/release 1.4.0` | Bump version, update changelog, and tag a release |
| [Coverage](/.claude/skills/coverage/SKILL.md) | `/coverage` | Run tests with coverage and report the riskiest gaps |
| [Pre-commit](/.claude/skills/pre-commit/SKILL.md) | `/pre-commit` | Set up pre-commit hooks that lint, format, and check before commits |
| [License](/.claude/skills/license/SKILL.md) | `/license MIT` | Add a LICENSE file (and optional headers) with the right SPDX text |
| [Seed](/.claude/skills/seed/SKILL.md) | `/seed` | Generate realistic seed/fixture data matching the project's schema |
| [Dead Code](/.claude/skills/dead-code/SKILL.md) | `/dead-code` | Find unused exports, functions, imports, files, and dependencies |
| [Diagram](/.claude/skills/diagram/SKILL.md) | `/diagram <what>` | Generate a Mermaid architecture/ER/sequence diagram from the code |
| [Benchmark](/.claude/skills/benchmark/SKILL.md) | `/benchmark <target>` | Measure runtime/throughput/memory and establish a baseline |
| [i18n](/.claude/skills/i18n/SKILL.md) | `/i18n` | Extract hardcoded UI strings into the project's locale files |
| [DB Migrate](/.claude/skills/db-migrate/SKILL.md) | `/db-migrate <change>` | Generate a schema migration with a safe up and down |
| [Squash](/.claude/skills/squash/SKILL.md) | `/squash` | Clean up a branch's commit history before merge, safely |
| [a11y](/.claude/skills/a11y/SKILL.md) | `/a11y` | Audit the UI for accessibility issues and fix them against WCAG |
| [Typecheck](/.claude/skills/typecheck/SKILL.md) | `/typecheck` | Run the type checker and fix reported errors without suppressing |
| [Error Handling](/.claude/skills/error-handling/SKILL.md) | `/error-handling` | Audit and harden error handling — swallowed errors, missing boundaries |
| [Logging](/.claude/skills/logging/SKILL.md) | `/logging` | Add structured, leveled, contextual logging without leaking secrets |
| [E2E](/.claude/skills/e2e/SKILL.md) | `/e2e <flow>` | Write end-to-end/integration tests that drive the app like a user |
| [Validate](/.claude/skills/validate/SKILL.md) | `/validate <boundary>` | Add input validation at boundaries, failing safely on bad input |
| [Contributing](/.claude/skills/contributing/SKILL.md) | `/contributing` | Generate a CONTRIBUTING.md from the project's real dev workflow |
| [GraphQL](/.claude/skills/graphql/SKILL.md) | `/graphql <request>` | Write, explain, or optimize a GraphQL operation or schema |
| [Healthcheck](/.claude/skills/healthcheck/SKILL.md) | `/healthcheck` | Add health/readiness/liveness endpoints that probe dependencies |
| [Mock](/.claude/skills/mock/SKILL.md) | `/mock <dep>` | Generate test doubles for a unit's dependencies in the project's style |
| [Rate Limit](/.claude/skills/rate-limit/SKILL.md) | `/rate-limit <policy>` | Add rate limiting/throttling to endpoints against abuse |
| [Cache](/.claude/skills/cache/SKILL.md) | `/cache <target>` | Add a caching layer with correct keys, TTL, and invalidation |
| [Feature Flag](/.claude/skills/feature-flag/SKILL.md) | `/feature-flag <feature>` | Gate a feature behind a flag to ship dark and roll back safely |
| [Codeowners](/.claude/skills/codeowners/SKILL.md) | `/codeowners` | Generate a CODEOWNERS file mapping paths to owning teams |
| [Prune Branches](/.claude/skills/prune-branches/SKILL.md) | `/prune-branches` | Safely clean up merged/stale local and remote branches |
| [Retry](/.claude/skills/retry/SKILL.md) | `/retry <call>` | Add retry-with-backoff to a flaky external call, safely for idempotent ops |
| [Security Headers](/.claude/skills/security-headers/SKILL.md) | `/security-headers` | Add/harden CSP, HSTS, CORS, and friends to defend against XSS and clickjacking |
| [Flaky Test](/.claude/skills/flaky-test/SKILL.md) | `/flaky-test <test>` | Find and fix the source of a test's nondeterminism, not mask it with retries |
| [Stash](/.claude/skills/stash/SKILL.md) | `/stash <action>` | Save, restore, and manage work-in-progress with git stash, safely |
| [Cherry-pick](/.claude/skills/cherry-pick/SKILL.md) | `/cherry-pick <sha>` | Apply specific commits onto another branch (backport a fix) with conflict handling |

## Installation

### Option 1: Copy to your project (project-level)

Copy the `.claude/skills/` folder into your project root:

```bash
cp -r .claude/skills/ /path/to/your/project/.claude/skills/
```

All of the skills above (`/commit-message`, `/pr-description`, `/changelog`, and the rest) will be available inside that project.

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
/migrate "replace moment with date-fns"  # applies a sweeping change, then verifies
/api-docs                # generates API docs from the route handlers
/gitignore               # generates/tightens .gitignore for the stack
/type-annotate           # adds type hints/annotations to untyped code
/env-example             # generates a .env.example from env vars used in code
/resolve-conflicts       # walks through and resolves git merge/rebase conflicts
/lint-fix                # runs the project's linter/formatter and fixes findings
/readme                  # generates or updates the project README from the codebase
/secrets-scan            # scans the tree and git history for hardcoded secrets
/release 1.4.0           # bumps version, updates changelog, and tags the release
/coverage                # runs tests with coverage and reports the riskiest gaps
/pre-commit              # sets up pre-commit hooks (lint, format, check)
/license MIT             # adds a LICENSE file with the right SPDX text
/seed                    # generates seed/fixture data matching the schema
/dead-code               # finds unused exports, imports, files, and deps
/diagram the architecture  # generates a Mermaid diagram from the code
/benchmark parser.js     # measures runtime/throughput and sets a baseline
/i18n                    # extracts hardcoded UI strings into locale files
/db-migrate "add phone column to users"  # generates a schema migration
/squash                  # cleans up the branch's commit history before merge
/a11y                    # audits the UI for accessibility issues and fixes them
/typecheck               # runs the type checker and fixes the reported errors
/error-handling          # audits and hardens error handling
/logging                 # adds structured, leveled logging without leaking secrets
/e2e "login then checkout"  # writes an end-to-end test for the flow
/validate "the POST /users body"  # adds input validation at the boundary
/contributing            # generates a CONTRIBUTING.md from the dev workflow
/graphql "user with last 5 orders"  # writes/explains/optimizes a GraphQL op
/healthcheck             # adds health/readiness/liveness endpoints
/mock "the payment client"  # generates a test double in the project's style
/rate-limit "login to 5/min per IP"  # adds rate limiting to an endpoint
/cache "the getUser query"  # adds a caching layer with TTL and invalidation
/feature-flag "the new checkout as new_checkout"  # gates a feature behind a flag
/codeowners              # generates a CODEOWNERS file mapping paths to teams
/prune-branches          # safely cleans up merged/stale branches
/retry "the payment API client"  # adds retry-with-backoff to a flaky call
/security-headers        # adds/hardens CSP, HSTS, CORS, and other headers
/flaky-test "the checkout test"  # finds and fixes the source of test flakiness
/stash save "wip on parser"  # shelves your uncommitted changes to switch context
/cherry-pick abc123      # applies a specific commit onto the current branch
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

> rename getUser to fetchUser everywhere
> replace every use of moment with date-fns

> document the API endpoints
> generate an OpenAPI spec for these routes

> create a gitignore for this project
> what should I stop tracking in git

> add type hints to this file
> fix the any types in this module

> what env vars does this project need
> generate a .env.example

> help me resolve these merge conflicts
> finish this rebase, I have conflicts

> fix the lint errors
> run the formatter and clean up warnings

> write a README for this project
> my README is out of date, update it

> scan for hardcoded secrets
> did I commit an API key anywhere

> cut a minor release
> bump the version and tag it

> what's my test coverage
> where are the coverage gaps

> set up pre-commit hooks
> run the linter before every commit

> add an MIT license to this project
> what license should I use

> generate seed data for the database
> create fixtures for my models

> find dead code in this project
> what imports are unused

> draw a diagram of the architecture
> generate an ER diagram of the models

> benchmark this function
> what's the baseline performance here

> extract these strings for translation
> internationalize this component

> create a migration to add a phone column
> generate a schema migration for this change

> squash my commits before merging
> clean up the commit history on this branch

> check this page for accessibility issues
> add aria labels and fix contrast

> fix the type errors
> make tsc pass

> improve the error handling here
> fix these swallowed exceptions

> add structured logging to this module
> what should I log in this handler

> write an end-to-end test for the checkout flow
> set up Playwright and test the login journey

> add validation to this request body
> add a zod schema for these params

> write a CONTRIBUTING guide for this repo
> document the dev workflow

> write a GraphQL query for a user with their orders
> why is this resolver slow

> add a health check endpoint
> add readiness and liveness probes for Kubernetes

> mock the database in this test
> create a stub for the payment client

> add rate limiting to the login endpoint
> throttle this API to prevent abuse

> cache the result of this query
> memoize this expensive function

> put this feature behind a flag
> add a feature toggle for the new checkout

> set up a CODEOWNERS file
> auto-assign reviewers by directory

> clean up merged branches
> which branches can I safely delete

> add a retry with backoff to this API call
> this request fails intermittently, make it resilient

> add security headers to the app
> set up a Content-Security-Policy and lock down CORS

> this test is flaky, fix it
> why does this test pass sometimes and fail other times

> stash my changes so I can switch branches
> pop my stashed work back

> cherry-pick that commit onto main
> backport this fix to the release branch
```

Both methods produce identical results. Slash commands are faster for muscle memory; natural language is easier when you don't remember the exact command name.

## How Claude Code Skills Work

Each skill is a `SKILL.md` file with YAML frontmatter and markdown instructions. Key features:

- **Dynamic context**: Lines starting with `` !`command` `` run before Claude sees the skill, injecting live data (e.g., `git diff`)
- **Arguments**: `$ARGUMENTS` captures what the user types after the command
- **Tool permissions**: `allowed-tools` pre-approves tools so Claude doesn't ask for permission
- **Auto-invocation**: `disable-model-invocation: false` allows Claude to trigger the skill automatically when it matches your natural language prompt. Set to `true` if you want slash-command-only invocation.

See [Claude Code Skills docs](https://code.claude.com/docs/en/skills) for the full reference.

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for how the repo
is laid out and how to add a new skill. Before opening a PR, run the validator
(the same check CI runs):

```bash
python3 scripts/validate_skills.py
```

## License

Released under the [MIT License](LICENSE).
