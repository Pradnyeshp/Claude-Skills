---
name: pagination
description: Add pagination to a list endpoint or query that returns unbounded rows — offset/limit or cursor-based — so responses stay fast and bounded as the dataset grows. Use when the user says "add pagination", "paginate this endpoint", "this returns too many rows", "add limit and offset", "add cursor pagination", "page through results", or "the list query is slow with lots of data".
argument-hint: "[the endpoint or query to paginate, e.g. 'GET /users' or 'the listOrders query']"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
disable-model-invocation: false
---

## Framework & data-access signals

!`grep -rilE "express|fastify|nestjs|flask|fastapi|django|prisma|sequelize|typeorm|sqlalchemy|knex|mongoose|LIMIT|OFFSET|findMany" --include='*.*' package.json pyproject.toml go.mod Gemfile 2>/dev/null | grep -vE 'node_modules|\.git|dist|build' | head -8`

## Instructions

Bound the result set of the list operation in `$ARGUMENTS` so it can't return the whole table at once. Match the project's existing framework, query builder/ORM, and response conventions rather than inventing a new shape.

### Method

1. **Pick the right strategy for the data:**
   - **Cursor (keyset) pagination** — preferred for large, append-heavy, or real-time data and infinite scroll. Page by `WHERE (sort_key, id) > (:last_sort, :last_id)` on an indexed, stable ordering. It stays fast at deep pages and doesn't skip/duplicate rows when data shifts between requests.
   - **Offset/limit** — fine for small, bounded, or admin datasets and when the client needs jump-to-page/total counts. Simple, but slow at high offsets and prone to drift as rows are inserted/deleted.
   Recommend one explicitly and say why for this dataset.
2. **Enforce a bounded, sane limit.** Apply a default page size (e.g. 20) and a hard maximum (e.g. 100). Clamp — never trust a client-supplied `limit` that could request the whole table. Reject or clamp non-numeric / negative values.
3. **Guarantee a stable, total ordering.** Order by a unique tiebreaker (typically the primary key) alongside the sort column, so pages don't overlap or drop rows when sort values tie. Ensure an index backs the ordering (and the cursor comparison) — see the `optimize` skill if the query is slow.
4. **Return a clear envelope.** Include the page of `data` plus pagination metadata: for cursor, a `nextCursor` (null when exhausted) and `hasMore`; for offset, `page`/`pageSize` and `total` **only if** counting is affordable (a `COUNT(*)` on a huge filtered set can dominate the request — make it optional or approximate). Keep the envelope consistent with the project's other list endpoints.
5. **Encode cursors opaquely.** Base64-encode the cursor payload so clients treat it as a token, not something to construct; validate/decode defensively and fail cleanly on a malformed cursor.
6. **Verify.** Add a test that pages through a seeded dataset end to end, asserting no gaps or duplicates across page boundaries, that the last page reports exhaustion, and that an over-large `limit` is clamped.

### Rules

1. Always enforce a default and a hard-max page size; never let a request return an unbounded result set, even if the client omits or inflates `limit`.
2. Order by a unique tiebreaker so pagination is deterministic; an unstable sort silently drops or repeats rows across pages.
3. Prefer keyset/cursor pagination for large or shifting datasets; reserve offset for small sets or when jump-to-page/totals are genuinely required.
4. Make expensive total counts optional — don't force a full `COUNT(*)` on every page of a large table.
5. Ensure the ordering and cursor comparison are index-backed, and end by summarizing the strategy, the default/max page size, the response envelope, and the ordering guarantee.
