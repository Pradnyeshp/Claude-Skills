---
name: release
description: Cut a release — pick the next version, bump it in the manifest, update the changelog, and create the tag and release notes. Use when the user says "cut a release", "prepare a release", "bump the version", "tag a release", "ship a new version", or "release X.Y.Z".
argument-hint: "[version or bump level, e.g. '1.4.0' or 'minor']"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
disable-model-invocation: false
---

## Release context

!`git tag --sort=-creatordate 2>/dev/null | head -5`

!`ls package.json pyproject.toml Cargo.toml composer.json VERSION CHANGELOG.md 2>/dev/null`

!`git log --oneline --no-merges "$(git describe --tags --abbrev=0 2>/dev/null)"..HEAD 2>/dev/null | head -40 || git log --oneline --no-merges -40`

## Instructions

Cut a release for this project. Use the version or bump level in `$ARGUMENTS`; if none is given, infer the right semver bump from the commits since the last tag (breaking → major, `feat` → minor, `fix`/`chore` → patch).

### Before changing anything

1. **Confirm the working tree is clean** and you're on the intended branch. If there are uncommitted changes, stop and ask — a release should be cut from a known state.
2. **Find the current version** in the manifest and the latest tag. Decide the next version (respect any pre-1.0 or pre-release conventions already in use).
3. **Review the commits since the last tag** (above) to confirm the bump level matches what actually changed.

### Steps

1. **Bump the version** in the project's manifest (`package.json`, `pyproject.toml`, `Cargo.toml`, `VERSION`, etc.). Use the native tool when it exists and the user is fine with it (`npm version <level> --no-git-tag-version`); otherwise edit the field directly. Keep lockfiles in sync.
2. **Update the changelog.** If a `CHANGELOG.md` exists, add a new section for this version dated today, grouping commits into Added / Changed / Fixed / Removed and rewriting them into user-facing language. If there's no changelog, hand off to the `changelog` skill or generate the notes inline. Move any "Unreleased" entries under the new version.
3. **Commit** the bump and changelog together: `chore(release): vX.Y.Z`.
4. **Tag** it: an annotated tag `vX.Y.Z` whose message is the release summary. Don't tag until the bump commit exists.
5. **Draft release notes** — a short highlights paragraph plus the changelog section — ready to paste into a GitHub/GitLab release.

### Rules

1. Don't push or publish (`git push`, `git push --tags`, `npm publish`, `gh release create`) unless the user explicitly asks — stop after the local commit and tag and report what's ready.
2. Never invent a changelog entry that isn't backed by a commit. Match the existing changelog's format if one exists.
3. Keep version, tag, changelog heading, and commit message all referring to the same version string — no drift.
4. If the bump level is ambiguous or the commits suggest a breaking change the user didn't flag, surface it and confirm before bumping.
5. End by summarizing: the version chosen, the files changed, the tag created, and the exact command(s) the user can run to push/publish when ready.
