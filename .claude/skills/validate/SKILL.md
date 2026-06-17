---
name: validate
description: Add input validation at a boundary — request bodies, query/path params, env, external responses — using the project's validation approach (zod, pydantic, joi, class-validator, etc.), failing safely on bad input. Use when the user says "add validation", "validate this input", "add a zod schema", "validate the request body", "sanitize input", or "guard against bad data".
argument-hint: "[the boundary to validate, e.g. 'the POST /users body' or 'src/routes/orders.ts']"
allowed-tools: Bash, Read, Edit, Grep, Glob
disable-model-invocation: false
---

## Validation tooling signals

!`grep -rilE "\\bzod\\b|joi|yup|pydantic|class-validator|marshmallow|ajv|express-validator|valibot" package.json pyproject.toml 2>/dev/null | head`

!`grep -rlnE "req\\.body|request\\.json|@app\\.(post|put)|router\\.(post|put)|@(Post|Put|Body)" --include='*.*' . 2>/dev/null | grep -vE 'node_modules|\.git|dist|build|test' | head -10`

## Instructions

Add validation at the boundary described in `$ARGUMENTS` (or the riskiest unvalidated input — request handlers taking untrusted bodies/params — if none given). Use the project's existing validation library and pattern.

### Method

1. **Find the validation convention.** From the signals above, identify the library and how it's used (zod/yup/joi/valibot schemas, pydantic models, class-validator DTOs, marshmallow, ajv/JSON-schema) and where validation lives (middleware, decorator, a `schemas/` dir). Mirror it. If there's no validation library, propose the idiomatic one for the stack and confirm before adding a dependency.
2. **Validate against the real contract.** Read the handler/consumer to see what fields it actually uses, their types, and which are required vs optional — and the data model/DB constraints behind them. Build the schema to match that contract, not a guess.
3. **Be strict at the edge.** Require what's required, constrain types/formats/ranges/enums/lengths, reject unknown extra fields where the library supports it (`strict`/`forbid extra`), and coerce only where intended (e.g. numeric query params). Validate *all* untrusted inputs — body, query, path params, headers — not just the body.
4. **Fail safely and clearly.** On invalid input return the project's standard error shape with the right status (typically `400`/`422`) and a message that says what's wrong **without** echoing back sensitive input or leaking internals. Make validation run before any side effect (db write, external call).
5. **Use the validated, typed output** downstream — pass the parsed result forward (e.g. zod's `parse` output, the pydantic model) so the handler works with trusted, correctly-typed data, and infer types from the schema where the language supports it instead of redeclaring.

### Rules

1. Validate at trust boundaries (anything from a client, third party, or env) — don't add redundant validation to already-trusted internal calls.
2. Match the project's existing schema library, location, and error response shape; don't introduce a parallel approach or a new dependency without asking.
3. Don't change the success-path behavior — validation rejects bad input and passes good input through unchanged. Flag any spot where strict validation would reject inputs the app currently (wrongly) accepts.
4. Never include raw invalid input or internal details in the error returned to the caller; keep messages safe and actionable.
5. Summarize what you validated, the rules applied, the failure response, and any inputs that were previously unguarded.
