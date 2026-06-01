---
name: sql
description: Write, explain, or optimize a SQL query from a plain-English description or an existing query, with attention to correctness, indexes, and dialect. Use when the user says "write a SQL query for", "explain this query", "why is this query slow", "optimize this SQL", "convert this to SQL", or pastes a query and asks what it does.
argument-hint: "[the request, e.g. 'top 10 customers by revenue this quarter' or a query to explain/optimize]"
allowed-tools: Bash, Read, Grep, Glob
disable-model-invocation: false
---

## Schema hints (if the project defines one)

!`find . -type d \( -name node_modules -o -name .git -o -name dist -o -name build -o -name vendor \) -prune -o -type f \( -iname '*.sql' -o -iname 'schema.*' -o -iname '*migration*' -o -iname 'models.py' \) -print 2>/dev/null | head -20`

## Instructions

Handle the SQL request in `$ARGUMENTS`. The request is one of: **write** a query from a description, **explain** a given query, or **optimize** a slow query. If none is given, ask which.

### Determine the dialect and schema first

- Infer the database (PostgreSQL, MySQL, SQLite, SQL Server, BigQuery, …) from migrations, ORM config, or connection strings in the repo. If it can't be determined, ask — dialects differ on quoting, limits, date functions, and window-function support.
- Look at any schema/migration files above for real table and column names. Don't invent columns; if the schema is unknown, state your assumptions explicitly.

### Writing a query

1. Produce a correct, readable query: uppercase keywords, meaningful aliases, explicit `JOIN ... ON`, and `LIMIT` where a sample is implied.
2. Prefer set-based logic over correlated subqueries where it's clearer and faster. Use CTEs to make multi-step logic legible.
3. Handle the tricky cases the request implies: NULLs, duplicates (`DISTINCT` vs `GROUP BY`), timezones, and inclusive/exclusive date ranges. Call out the assumption.
4. Briefly explain what the query returns and any assumption made about the schema.

### Explaining a query

Walk through it from the innermost subquery/CTE outward: what each join, filter, grouping, and window does, and what the final result set represents. Flag anything surprising (implicit cross joins, fan-out from one-to-many joins, `NULL` semantics).

### Optimizing a query

1. Identify the likely cost: missing index, full scan, fan-out join, `SELECT *`, function on an indexed column, `OR` defeating an index, or `N+1` from the app side.
2. Suggest concrete fixes (the index to add, the rewrite, the predicate pushdown) and show the improved query.
3. Recommend running `EXPLAIN`/`EXPLAIN ANALYZE` to confirm, and show the exact command for the detected dialect.

### Rules

1. Never guess at table/column names silently — verify against the schema or state the assumption.
2. Don't suggest destructive statements (`DELETE`/`UPDATE`/`DROP`) unless explicitly asked; if you do, wrap with a `SELECT` to preview affected rows and a transaction.
3. Note dialect-specific syntax when it matters so the query isn't silently non-portable.
