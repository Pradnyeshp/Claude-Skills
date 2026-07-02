---
name: soft-delete
description: Convert hard deletes into recoverable soft deletes — mark rows deleted instead of removing them, filter them out of normal reads, and keep uniqueness and foreign keys correct — so data can be restored and history preserved. Use when the user says "add soft delete", "make deletes recoverable", "don't actually delete rows", "add a deleted_at column", "archive instead of delete", "add a trash/restore feature", or "we need to undo deletes".
argument-hint: "[the model or table to soft-delete, e.g. 'the User model' or 'orders']"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
disable-model-invocation: false
---

## ORM, schema & delete-site signals

!`grep -rilE "deleted_at|deletedAt|soft.?delete|paranoid|SoftDelete|prisma|sequelize|typeorm|sqlalchemy|django|knex|mongoose|DELETE FROM|\\.destroy\\(|\\.delete\\(" --include='*.*' package.json pyproject.toml go.mod Gemfile 2>/dev/null | grep -vE 'node_modules|\.git|dist|build' | head -8`

## Instructions

Make deletes on the model/table in `$ARGUMENTS` recoverable instead of destructive. The core is a nullable `deleted_at` timestamp, but the subtle parts are making *every* read exclude deleted rows and keeping constraints valid — get those wrong and you silently leak deleted data or block legitimate re-creates.

### Method

1. **Add the marker column.** A nullable `deleted_at TIMESTAMP` (null = live) is preferred over a boolean — it records *when*, and often *who* alongside (`deleted_by`). Generate a migration with a safe up/down (see the `db-migrate` skill) and index `deleted_at` if you'll query by it.
2. **Change delete to an update.** Replace hard `DELETE`/`.destroy()` calls with setting `deleted_at = now()`. Offer a `restore` (set it back to null) and keep a genuine hard-delete path available for GDPR/erasure and admin purge — soft delete is not a substitute for the right to be forgotten.
3. **Filter deleted rows from all normal reads — this is the trap.** Apply a default scope so every query excludes `deleted_at IS NOT NULL`. Prefer the ORM's built-in mechanism (TypeORM/Sequelize `paranoid`, Django manager, a Prisma extension/middleware, Rails `default_scope`) so no query site is forgotten. Audit existing queries, joins, aggregates, and raw SQL — a single unscoped `SELECT` or `COUNT` leaks or miscounts deleted data.
4. **Fix uniqueness.** A plain `UNIQUE(email)` will reject re-creating a record whose old row was soft-deleted. Switch to a partial/filtered unique index (`UNIQUE(email) WHERE deleted_at IS NULL`) or include `deleted_at` in the key, so a live value is unique but deleted rows don't block reuse.
5. **Handle relations and cascades.** Decide what happens to children of a soft-deleted parent (cascade the soft delete, or block/orphan) — a real `ON DELETE CASCADE` won't fire since no row is removed. Make sure foreign-key lookups from live rows don't resolve to deleted parents.
6. **Mind the trade-offs.** Tables grow unbounded — plan periodic pur/archival of long-deleted rows. Consider pairing with an `audit-log` entry on delete/restore. Note that unique-index and count changes can surprise other features.
7. **Verify.** Test that a delete hides the row from normal reads but keeps it in the table, that restore brings it back, that a soft-deleted unique value can be re-created, and that no relationship/aggregate query returns deleted rows.

### Rules

1. Deletes set `deleted_at`; every normal read must exclude soft-deleted rows via a default scope — audit joins, aggregates, and raw SQL, since one unscoped query leaks deleted data.
2. Convert unique constraints to partial/conditional uniqueness on live rows, or soft-deleted rows will block re-creating the same value.
3. Keep a real hard-delete/purge path for compliance erasure and table growth — soft delete augments deletion, it doesn't replace the ability to truly remove data.
4. Address relations explicitly (cascade or block the soft delete of parents with children); don't rely on database `ON DELETE CASCADE`, which won't fire.
5. Provide a restore path and end by summarizing the column added, how reads are scoped, the uniqueness fix, relation handling, and the purge/retention plan.
