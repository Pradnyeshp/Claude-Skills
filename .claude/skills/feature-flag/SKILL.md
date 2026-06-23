---
name: feature-flag
description: Gate a feature or code path behind a feature flag — using the project's flag system (LaunchDarkly, Unleash, a config/env toggle) — so it can be shipped dark and rolled out or rolled back without a deploy. Use when the user says "put this behind a feature flag", "add a feature toggle", "gate this feature", "make this configurable on/off", or "ship this dark".
argument-hint: "[the feature/code to gate and the flag name, e.g. 'the new checkout flow as new_checkout']"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
disable-model-invocation: false
---

## Flag system signals

!`grep -rilE "launchdarkly|ld-client|unleash|flagsmith|split\\.io|posthog|growthbook|featureFlags?|isEnabled\\(|@FeatureFlag" --include='*.*' . 2>/dev/null | grep -vE 'node_modules|\.git|dist|build' | head -10`

!`ls .env.example config 2>/dev/null && grep -iE "FLAG|FEATURE|ENABLE_" .env.example 2>/dev/null | head`

## Instructions

Gate the feature in `$ARGUMENTS` behind a flag. If the flag name or the boundary to gate isn't clear, confirm before editing. Use the project's existing flag mechanism — don't introduce a new flag platform unprompted.

### Method

1. **Find the existing flag convention.** From the signals above, identify whether the project uses a flag service (LaunchDarkly/Unleash/Flagsmith/Split/GrowthBook), a config/env toggle, or nothing yet. Mirror how flags are named, defined, and read. If there's no system and the user wants something simple, propose a minimal config/env-based toggle and confirm before adding a dependency.
2. **Gate at the right seam.** Wrap the smallest boundary that cleanly switches the behavior — a route, a component, a branch in a service — so both paths are clear. Keep the old path intact and reachable when the flag is off; the flag should choose between two working states, not leave a half-built one.
3. **Default off and fail safe.** A new flag defaults to its safe/old behavior, and if the flag service is unreachable the evaluation falls back to that default (never crashes or silently enables an unfinished feature). Evaluate the flag with the right context (user/tenant/environment) where the system supports targeting.
4. **Register the flag** wherever the project tracks them (the flag dashboard config, a constants/enum file, `.env.example`) so it's discoverable and not a magic string. Use one canonical name.
5. **Plan for removal.** A flag is temporary scaffolding — note that once the feature is fully rolled out, both the flag check and the dead old path should be removed (the `dead-code`/`refactor` skills can do that later). Avoid deep nesting of multiple flags.

### Rules

1. Use the project's existing flag system and naming; only add a new mechanism (and dependency) with the user's go-ahead.
2. Default to the safe/old behavior and fail to that default if the flag can't be evaluated — never let an unreachable flag service enable an unfinished feature or break the request.
3. Keep both branches working and behavior-preserving when off; the flag selects between states, it doesn't ship broken code behind a false.
4. Make the flag discoverable (registered/named in one place), not a bare hardcoded string scattered around.
5. After wiring, summarize the flag name, where it's gated, its default, the targeting context, and the cleanup step to remove it post-rollout.
