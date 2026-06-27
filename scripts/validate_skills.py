#!/usr/bin/env python3
"""Validate every skill in .claude/skills and that the README lists it.

Checks, for each directory under .claude/skills/:
  1. a SKILL.md file exists
  2. it opens with a YAML frontmatter block (--- ... ---)
  3. the frontmatter has non-empty `name` and `description` fields
  4. `name` matches the directory name
  5. the skill is referenced in README.md

Exits non-zero (and prints every problem) if any check fails, so CI fails loudly.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / ".claude" / "skills"
README = REPO_ROOT / "README.md"


def parse_frontmatter(text: str) -> dict[str, str] | None:
    """Return the top-level key/value pairs of a leading --- frontmatter block."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    fields: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fields
        if ":" in line and not line.startswith((" ", "\t", "#")):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip().strip('"').strip("'")
    return None  # never closed


def main() -> int:
    errors: list[str] = []

    if not SKILLS_DIR.is_dir():
        print(f"ERROR: skills directory not found: {SKILLS_DIR}")
        return 1

    readme_text = README.read_text(encoding="utf-8") if README.exists() else ""
    if not readme_text:
        errors.append("README.md is missing or empty")

    skill_dirs = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())
    if not skill_dirs:
        errors.append("no skill directories found under .claude/skills")

    for skill_dir in skill_dirs:
        name = skill_dir.name
        skill_md = skill_dir / "SKILL.md"

        if not skill_md.is_file():
            errors.append(f"{name}: missing SKILL.md")
            continue

        fm = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        if fm is None:
            errors.append(f"{name}: SKILL.md has no valid --- frontmatter block")
            continue

        if not fm.get("name"):
            errors.append(f"{name}: frontmatter missing a `name` field")
        elif fm["name"] != name:
            errors.append(
                f"{name}: frontmatter name `{fm['name']}` != directory name `{name}`"
            )

        if not fm.get("description"):
            errors.append(f"{name}: frontmatter missing a `description` field")

        ref = f"/.claude/skills/{name}/SKILL.md"
        if ref not in readme_text:
            errors.append(f"{name}: not linked in README.md (expected `{ref}`)")

    if errors:
        print(f"FAILED: {len(errors)} problem(s) found:\n")
        for err in errors:
            print(f"  - {err}")
        return 1

    print(f"OK: validated {len(skill_dirs)} skills; all have valid frontmatter "
          f"and are linked in README.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
