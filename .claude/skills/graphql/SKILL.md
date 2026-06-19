---
name: graphql
description: Write, explain, or optimize a GraphQL operation or schema — queries, mutations, fragments, resolvers — with attention to the real schema, over-fetching, and the N+1 problem. Use when the user says "write a GraphQL query", "explain this query", "why is this resolver slow", "design a GraphQL schema", "fix N+1 in resolvers", or pastes an operation and asks what it does.
argument-hint: "[the request, e.g. 'query for a user with their last 5 orders' or an operation/schema to explain/optimize]"
allowed-tools: Bash, Read, Grep, Glob
disable-model-invocation: false
---

## Schema & resolver hints

!`find . -type d \( -name node_modules -o -name .git -o -name dist -o -name build \) -prune -o -type f \( -iname '*.graphql' -o -iname '*.gql' -o -iname 'schema.*' -o -iname '*resolver*' -o -iname '*typedefs*' \) -print 2>/dev/null | head -20`

## Instructions

Handle the GraphQL request in `$ARGUMENTS`. It's one of: **write** an operation/schema from a description, **explain** a given operation, or **optimize** a slow query/resolver. If unclear, ask which.

### Determine the schema first

- Find the real schema (SDL `.graphql` files, code-first type defs, or introspection) and use actual type, field, and argument names. Don't invent fields; if the schema is unknown, state your assumptions explicitly.
- Note the server/framework (Apollo, GraphQL Yoga, Nexus, graphql-ruby, Strawberry, Hasura) since resolver patterns and tooling differ.

### Writing an operation or schema

1. Produce a valid operation: a named operation, typed `$variables` (not inline literals), only the fields actually needed, and fragments for reused selections.
2. For schema design: model nullability deliberately, use enums/interfaces/unions where they fit, follow connection/edge pagination conventions for lists, and keep mutations returning the affected object (and a payload type) rather than a bare scalar.
3. Call out the assumption about schema shape and how variables are supplied.

### Explaining an operation

Walk the selection set from the root field outward: what each field, argument, fragment, and directive resolves to, and what the response shape looks like. Flag surprises — deeply nested selections that fan out, fields with side-effectful resolvers, or aliases that mask multiple calls to the same field.

### Optimizing

1. Identify the likely cost: **N+1 resolvers** (the classic — a list field whose item resolver hits the DB per element), over-fetching deep nested selections, missing pagination, or unbounded query depth/complexity.
2. Recommend concrete fixes: a **DataLoader**/batch-load to collapse N+1, pagination on list fields, query depth/complexity limits, projecting only requested fields to the data source, and caching where appropriate. Show the improved operation or resolver sketch.
3. Suggest measuring with the server's tracing/`extensions` timing to confirm the win.

### Rules

1. Never guess at schema field/type names silently — verify against the SDL/type defs or state the assumption.
2. Validate operations against the schema's nullability and argument types; flag a selection that wouldn't type-check.
3. Treat the N+1 resolver problem as the default suspect for slow list queries — don't optimize blindly without naming the batching fix.
4. Watch security/cost: recommend depth/complexity limits and pagination for any client-facing schema, and don't expose unbounded list fields without them.
