---
name: e2e
description: Write or scaffold end-to-end / integration tests that drive the app like a user — browser flows (Playwright/Cypress) or API flows — matching the project's setup. Use when the user says "write an e2e test", "add end-to-end tests", "set up Playwright/Cypress", "test this user flow", "add integration tests", or "test the happy path through the app".
argument-hint: "[the flow to test, e.g. 'login then checkout' or 'POST /orders then GET it back']"
allowed-tools: Bash, Read, Write, Grep, Glob
disable-model-invocation: false
---

## E2E setup signals

!`ls -d e2e tests/e2e cypress playwright.config.* cypress.config.* tests/integration 2>/dev/null`

!`grep -rilE "@playwright/test|cypress|puppeteer|selenium|supertest|testcontainers|webdriver" package.json pyproject.toml 2>/dev/null | head`

## Instructions

Write an end-to-end / integration test for the flow in `$ARGUMENTS`. If the flow isn't clear, ask which user journey to cover before writing. If no e2e framework is set up, identify the idiomatic one and confirm before adding it.

### Method

1. **Detect the framework and convention.** From the signals above, find the e2e tool (Playwright, Cypress, Puppeteer, Selenium for browser; supertest/requests + testcontainers for API) and read an existing e2e test to match its structure, selectors, fixtures, base URL/config, and naming. Mirror it. If none exists, propose the standard for the stack (Playwright for web, supertest-style for an API) and confirm.
2. **Test the flow as a user/client experiences it**, across real boundaries — UI → server → db, or HTTP request → response → persisted state. Assert on observable outcomes (visible text, URL, status code, returned/stored data), not internal implementation.
3. **Use resilient selectors.** Prefer role/label/test-id (`getByRole`, `data-testid`) over brittle CSS/XPath tied to styling. For APIs, assert status + body shape, not incidental fields.
4. **Handle async and state properly.** Use the framework's auto-waiting/explicit waits instead of fixed sleeps. Set up and tear down test data so runs are isolated and repeatable; don't depend on a prior test's leftovers or on a specific pre-seeded record that may not exist.
5. **Keep it focused and stable.** One coherent journey per test, named for the behavior. Cover the happy path plus a key failure (e.g. invalid login), not every permutation — e2e is expensive, so test the critical paths, not what unit tests already cover.

### Rules

1. Match the project's existing e2e framework, selectors, and fixtures exactly; don't introduce a second framework or a new selector style unprompted.
2. No fixed `sleep`/arbitrary timeouts — use proper waiting; flaky timing makes e2e worthless. Call out any inherent nondeterminism.
3. Make tests self-contained: create the data they need and clean up, so they pass in any order against a fresh environment.
4. Assert real user-visible/client-visible outcomes; don't reach into internals to make a test pass.
5. After writing, give the exact command to run it and note any prerequisites (app/server running, env vars, a seeded test db, browser install like `npx playwright install`).
