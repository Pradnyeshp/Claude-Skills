---
name: api-docs
description: Generate API documentation for the project's HTTP endpoints — an OpenAPI spec or a readable markdown reference — by reading the route handlers. Use when the user says "document the API", "generate OpenAPI", "write API docs", "list the endpoints", "create a Swagger spec", or "document these routes".
argument-hint: "[optional: format ('openapi' or 'markdown'), or a route prefix to focus on]"
allowed-tools: Bash, Read, Write, Grep, Glob
disable-model-invocation: false
---

## Route discovery

!`grep -rniE "@(Get|Post|Put|Patch|Delete|RequestMapping)|app\.(get|post|put|patch|delete)|router\.(get|post|put|patch|delete)|@app\.route|@router\.(get|post|put|patch|delete)|fastapi|express|flask" --include='*.*' -l . 2>/dev/null | grep -vE 'node_modules|\.git|dist|build|vendor|test|spec' | head -30`

## Instructions

Generate API documentation for the endpoints in this project (use the format and scope in `$ARGUMENTS`; default to **markdown** unless an OpenAPI/Swagger spec already exists or is requested).

### Method

1. **Find the routes.** From the files above, locate every endpoint definition. Identify the framework (Express, Fastify, FastAPI, Flask, Django REST, Spring, etc.) so you read handlers correctly.
2. **For each endpoint, extract:** HTTP method and path (including path params), purpose, request shape (path/query params, headers, body schema), response shape and status codes, auth requirement, and notable errors. Read the handler body and any validation schema/DTO/serializer — don't guess the contract.
3. **Document the real contract,** not an idealized one. If validation or types define the schema (zod, pydantic, DTOs, JSON schema), reflect those exactly. Note required vs optional fields and defaults.
4. **Choose the format:**
   - **OpenAPI** (`openapi.yaml`/`.json`) when the project already has one, uses a spec-driven tool, or the user asks. Produce valid OpenAPI 3.x with shared component schemas for reused models.
   - **Markdown** otherwise — group endpoints by resource, with a request/response example per endpoint.
5. **Write to a sensible path** (`docs/api.md` or `openapi.yaml`) unless the user names one. If a spec already exists, update it rather than replacing it.

### Rules

1. Document only endpoints that exist in the code. Don't invent routes, fields, or status codes.
2. Mark anything you couldn't determine from the code (e.g. a response shape built dynamically) as "TBD — verify" rather than fabricating it.
3. Include at least one concrete example request and response per endpoint or resource group.
4. After writing, list how many endpoints were documented and any handlers you skipped (and why).
