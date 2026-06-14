---
name: db-migrate
description: Generate a database schema migration from a described change — add a table/column, alter a type, add an index or constraint — using the project's migration tool, with a safe up and down. Use when the user says "create a migration", "add a column to the database", "generate a schema migration", "alter this table", "add an index", or "migrate the database schema".
argument-hint: "[the schema change, e.g. 'add nullable phone column to users' or 'add unique index on orders.number']"
allowed-tools: Bash, Read, Write, Grep, Glob
disable-model-invocation: false
---

## Migration tooling signals

!`ls -d migrations db/migrate prisma alembic.ini knexfile.* 2>/dev/null`

!`grep -rilE "knex|prisma|sequelize|typeorm|alembic|flyway|liquibase|django|ActiveRecord|migrate" package.json pyproject.toml Gemfile 2>/dev/null | head`

## Instructions

Generate a database migration for the change described in `$ARGUMENTS`. If the change is ambiguous (which table, nullability, default, type), ask before generating — a wrong migration against a real database is costly to undo.

### Method

1. **Detect the migration tool and convention.** From the signals above, identify the framework (Prisma, Knex, TypeORM, Sequelize, Alembic, Django, Rails/ActiveRecord, Flyway, Liquibase) and read an existing migration to match its file naming, timestamp/sequence format, and style. **Prefer the tool's own generator** (`prisma migrate dev`, `alembic revision`, `rails g migration`, `knex migrate:make`) so the file lands correctly — show the command.
2. **Read the current schema** for the affected table(s) so the change is consistent with existing columns, types, and constraints. Don't guess the current shape.
3. **Write both directions.** Provide a correct `up` and a real `down` that exactly reverses it (drop the column/table/index you added). If a change is genuinely irreversible (dropping a column with data), say so explicitly rather than writing a lossy down silently.
4. **Make it safe to run on a populated table.** Adding a `NOT NULL` column needs a default or a backfill-then-constrain sequence; renaming/dropping needs a thought-out path. Call out locking/downtime risks on large tables (e.g. index creation) and prefer concurrent/online variants where the database supports them.
5. **Keep code models in sync.** Note (or update, if the project co-locates them) the ORM model/entity/type that must change to match — a migration that drifts from the model breaks the app.

### Rules

1. Generate against the real current schema and the project's actual tool — never hand-write a migration in a format the project doesn't use.
2. Always include a working `down`/rollback, or explicitly flag and explain any irreversible step instead of faking one.
3. Treat the target as having production data: no implicit data loss, and surface NOT-NULL/default/backfill and locking concerns.
4. Don't run the migration against any database unless the user explicitly asks — generate the file and give the command to apply it.
5. After writing, summarize the change, the up/down behavior, any data/locking risk, and the model code that must be updated to match.
