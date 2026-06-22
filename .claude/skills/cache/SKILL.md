---
name: cache
description: Add a caching layer to an expensive function, query, or endpoint — in-memory, Redis, or HTTP — with correct keys, TTL, and invalidation. Use when the user says "add caching", "cache this result", "memoize this", "cache the API response", "add a Redis cache", or "this is recomputed too often".
argument-hint: "[what to cache, e.g. 'the getUser query' or 'the GET /products response']"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
disable-model-invocation: false
---

## Caching infrastructure signals

!`grep -rilE "redis|ioredis|memcached|node-cache|lru-cache|functools\\.lru_cache|cachetools|@cache" --include='*.*' package.json pyproject.toml 2>/dev/null | grep -vE 'node_modules|\.git' | head -8`

## Instructions

Add caching for the target in `$ARGUMENTS`. If it's unclear what's expensive or how fresh the data must be, ask before adding a cache — a wrong TTL or key serves stale or leaked data. Reuse the project's existing cache client/library.

### Method

1. **Confirm it's worth caching.** Caching fits expensive, frequently-repeated, read-heavy work whose inputs repeat and whose result tolerates some staleness. If the data must be exact and real-time, or writes dominate, say caching is the wrong tool here.
2. **Pick the layer for the need**, preferring infra the project already has:
   - **In-process** (memoization, `lru-cache`, `functools.lru_cache`) — single instance, small/hot data, fine to lose on restart.
   - **Shared** (Redis/Memcached) — multi-instance, larger data, must be consistent across processes.
   - **HTTP** (`Cache-Control`/`ETag`) — cacheable GET responses, push caching to client/CDN.
3. **Build a correct key.** Include every input the result depends on — args, the user/tenant for per-user data, locale, version. A key that omits an input serves one caller's data to another (a real security bug for per-user responses). Namespace keys to avoid collisions.
4. **Set TTL and invalidation deliberately.** Choose a TTL from how stale the data may acceptably be. Where correctness matters, invalidate or update the entry on the write that changes the underlying data (write-through / explicit delete on mutation) rather than relying on TTL alone. State the staleness window you're accepting.
5. **Handle the edges:** cache misses and cache-store failures must fall back to the source (fail open — a down cache shouldn't take down the feature); avoid caching errors/empties unintentionally; and be aware of stampedes on hot keys (consider a lock/single-flight for very hot entries).

### Rules

1. Key on every input the value depends on — especially user/tenant for per-user data. A missing key dimension serves wrong or another user's data; treat that as a correctness/security risk, not a tuning detail.
2. Have an invalidation story, not just a TTL, whenever a write can change the cached value — and state the accepted staleness window.
3. Reuse the project's cache client/config; use a shared store when the app runs multiple instances rather than a per-process cache that fragments.
4. Fail open on cache-store errors and on misses — fall back to recomputation; never let the cache layer become a new single point of failure. Don't change the function's observable result, only its speed/freshness.
5. After adding, summarize what's cached, the key, the TTL/invalidation, the layer, and the staleness trade-off.
