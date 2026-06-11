---
name: seed
description: Generate realistic seed, fixture, or mock data that matches the project's data models, schema, or types — for local development, demos, or tests. Use when the user says "generate seed data", "create fixtures", "make mock data", "populate the database", "add test data", or "seed the dev db".
argument-hint: "[optional: what to seed and how much, e.g. '50 users with orders' or a model/table name]"
allowed-tools: Bash, Read, Write, Grep, Glob
disable-model-invocation: false
---

## Schema & model signals

!`ls prisma/schema.prisma schema.sql migrations models 2>/dev/null`

!`grep -rilE "schema|model|entity|@Entity|class .*\\(Base\\)|createTable|Schema\\(" --include='*.ts' --include='*.js' --include='*.py' --include='*.prisma' --include='*.rb' . 2>/dev/null | grep -vE 'node_modules|\.git|dist|build|vendor' | head -20`

## Instructions

Generate seed/fixture data for this project per `$ARGUMENTS` (what to seed and how many). If the target model/table isn't clear, find the schema first and confirm scope before generating.

### Method

1. **Read the real schema.** Locate the models/tables/types (Prisma schema, SQL DDL, ORM models, TypeScript types, pydantic/dataclasses) and extract every field: type, nullability, defaults, enums, unique constraints, and foreign keys. Generate against the actual shape — don't guess columns.
2. **Match the project's seeding mechanism.** Look for how this project already seeds (a `seeds/`/`fixtures/` dir, a `prisma/seed.ts`, a factory library like factory_boy/FactoryBot/Faker, a `db:seed` script). Extend that mechanism and reuse its style rather than introducing a new one.
3. **Make data realistic and coherent.** Use plausible values per field (names, emails, dates, enums from their allowed set), respect formats and length limits, and keep relationships valid — generate parents before children and use real foreign keys so referential integrity holds.
4. **Honor constraints.** Unique fields get unique values; required fields are always set; enums only use defined variants; numeric/date ranges stay sensible. Make output deterministic (seed the RNG / use a fixed seed) so runs are reproducible.
5. **Write to the conventional location** (the existing seed script or fixtures dir) and wire it to the project's seed command if one exists. Default to a modest volume unless the user asked for a specific count.

### Rules

1. Generate strictly against the real schema — every field, type, and constraint comes from the code, not assumption. Flag anything you couldn't determine rather than inventing it.
2. Never use real personal data or real secrets; synthesize fake-but-plausible values, and clearly fake credentials for any auth fields.
3. Preserve referential integrity — no dangling foreign keys, no constraint violations the database would reject.
4. Don't run destructive operations (truncating tables, resetting the DB) unless the user explicitly asks; default to additive, idempotent seeds where possible.
5. After writing, report what was generated (models and counts), the command to load it, and any constraints you had to work around.
