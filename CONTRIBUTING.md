# Contributing to Claude-Skills

Thanks for your interest in improving this collection of Claude Code skills! This
guide explains how the repo is laid out and how to add or change a skill.

## Repository layout

```
.claude/skills/<skill-name>/SKILL.md   # one folder per skill
scripts/validate_skills.py             # CI validation (see below)
README.md                              # the catalog — every skill is listed here
```

Each skill is a single `SKILL.md` file: YAML frontmatter followed by markdown
instructions. There is no build step — the skills are consumed directly by
Claude Code.

## Adding a new skill

1. **Create the folder and file**: `.claude/skills/<skill-name>/SKILL.md`. The
   folder name must be kebab-case and must exactly match the `name` field in the
   frontmatter.

2. **Write the frontmatter.** Required fields are `name` and `description`;
   the others are recommended:

   ```yaml
   ---
   name: my-skill
   description: One-line summary, then "Use when the user says ..." trigger phrases.
   argument-hint: "[what the user types after the command]"
   allowed-tools: Bash, Read, Write, Edit, Grep, Glob
   disable-model-invocation: false
   ---
   ```

   - `description` is what Claude uses to decide when to auto-invoke the skill —
     pack it with concrete trigger phrases.
   - `allowed-tools` pre-approves tools so Claude doesn't prompt for permission.
   - `disable-model-invocation: false` lets natural-language prompts trigger the
     skill; set `true` for slash-command-only skills.

3. **Write the instructions.** Keep the style consistent with the existing
   skills: a short intro, a `## Method` (numbered steps), and a `## Rules`
   section. Lines beginning with `` !`command` `` run before Claude sees the
   skill and inject live context; `$ARGUMENTS` captures what the user typed.

4. **Add it to `README.md`.** Add a row to the Skills table linking to
   `/.claude/skills/<skill-name>/SKILL.md`, and (optionally) entries to the
   usage examples. **CI fails if a skill is not linked in the README.**

## Before you open a PR

Run the validator locally — this is the same check CI runs:

```bash
python3 scripts/validate_skills.py
```

It confirms every skill has a `SKILL.md` with valid frontmatter, that each
`name` matches its directory, and that each skill is linked in the README.

## Commit and PR conventions

- Use [Conventional Commits](https://www.conventionalcommits.org/) for messages,
  e.g. `feat(skills): add stash skill` or `docs: document the stash skill`.
- Keep each PR focused — one skill or one logical change at a time.
- Make sure `python3 scripts/validate_skills.py` passes before pushing.

Happy contributing! 🎉
