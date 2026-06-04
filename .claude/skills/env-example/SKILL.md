---
name: env-example
description: Scan the codebase for environment variable usage and generate or update a .env.example with every required variable, documented and safely placeholdered. Use when the user says "generate a .env.example", "what env vars does this need", "document the environment variables", "update my dotenv template", or "find missing env vars".
argument-hint: "[optional: a path/dir to focus on, or extra vars to include]"
allowed-tools: Bash, Read, Write, Glob, Grep
disable-model-invocation: false
---

## Env var usage in the code

!`grep -rohiE '(process\.env\.[A-Z0-9_]+|process\.env\[["'"'"'][A-Z0-9_]+["'"'"']\]|os\.environ(\.get)?\(?[\[ ]*["'"'"'][A-Z0-9_]+["'"'"']|os\.getenv\(["'"'"'][A-Z0-9_]+["'"'"']|ENV\[["'"'"'][A-Z0-9_]+["'"'"']\]|getenv\(["'"'"'][A-Z0-9_]+["'"'"']|System\.getenv\(["'"'"'][A-Z0-9_]+["'"'"'])' . --include='*.js' --include='*.ts' --include='*.jsx' --include='*.tsx' --include='*.py' --include='*.rb' --include='*.go' --include='*.java' --include='*.php' 2>/dev/null | grep -oiE '[A-Z0-9_]{2,}' | grep -vE '^(process|env|environ|os|get|getenv|System)$' | sort -u | head -120`

## Existing templates & config

!`ls .env.example .env.sample .env.template .env.dist .env 2>/dev/null`

!`cat .env.example 2>/dev/null | head -60 || echo "No .env.example yet"`

## Instructions

Generate or update `.env.example` so it lists every environment variable the project reads (focus on `$ARGUMENTS` if given). The detected names above are a starting point — verify them against the source.

### Method

1. **Confirm the real set of variables.** The grep above catches common access patterns but can miss dynamically built names, config-library schemas (e.g. a `config`/`env` module, `zod`/`envalid`/`pydantic` settings, framework `.env` loaders), and Docker/compose/CI references. Search those too with Grep, and read the config module if there is one — it's usually the authoritative list.
2. **For each variable, determine:** whether it's required or optional, its purpose, and a safe example/default. Infer type and format from how it's used (URL, port, boolean, comma-list, secret token).
3. **Never include real secrets.** Use obvious placeholders (`your-api-key-here`, `changeme`, `postgres://user:pass@localhost:5432/dbname`). If a real value appears in an existing `.env`, do not copy it into the example.
4. **Merge, don't clobber.** Keep existing entries, comments, and ordering in `.env.example`; add only the missing variables under clear section headers (grouped by concern: database, auth, third-party APIs, feature flags).
5. **Document each entry** with a short `#` comment for its purpose, and mark optional ones (e.g. `# optional, default: 3000`).

### Rules

1. Output goes only to `.env.example` (or the project's existing template name) — never write or modify a real `.env`.
2. Don't invent variables the code doesn't use; every entry must trace to a real read in the source. Note any you couldn't classify as required/optional.
3. Use placeholders for all secrets and connection strings — no real credentials, ever.
4. If `.env.example` exists and isn't tracked-but-should-be ignored, that's fine — but if a real `.env` is tracked by git, flag it and suggest `git rm --cached .env` plus a `.gitignore` entry (hand off to the `gitignore` skill if needed).
5. After writing, summarize what you added, list any variables that need real values before the app runs, and note anything you weren't sure about.
