---
name: mock
description: Generate test doubles — mocks, stubs, fakes, spies — for a unit's external dependencies, matching the project's testing and mocking approach, so a unit test can run in isolation. Use when the user says "mock this dependency", "create a stub for", "mock the API call", "fake the database", "add a test double", or "how do I mock X in tests".
argument-hint: "[the dependency or unit to mock, e.g. 'the payment client in OrderService' or 'fetch']"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
disable-model-invocation: false
---

## Test & mocking setup

!`find . -type d \( -name node_modules -o -name .git -o -name dist -o -name build \) -prune -o -type f \( -name '*.test.*' -o -name '*.spec.*' -o -name 'test_*.py' -o -name 'conftest.py' -o -name '*_test.go' \) -print 2>/dev/null | head -15`

!`grep -rilE "jest\\.mock|vi\\.mock|sinon|unittest\\.mock|@patch|monkeypatch|nock|msw|gomock|mockito|testify/mock" --include='*.*' . 2>/dev/null | grep -vE 'node_modules|\.git|dist|build' | head -10`

## Instructions

Create a test double for the dependency in `$ARGUMENTS` so the unit under test can be tested in isolation. Match the project's existing test framework and mocking style — don't introduce a new mocking library.

### Method

1. **Learn the mocking convention.** From the signals above, identify the framework and how the project already mocks (`jest.mock`/`vi.mock`, sinon, `unittest.mock`/`@patch`/pytest `monkeypatch`, nock/MSW for HTTP, gomock/testify, Mockito). Read a neighboring test to match the setup/teardown and assertion style. If nothing exists, propose the idiomatic approach and confirm.
2. **Pick the right kind of double for the need:**
   - **Stub** — returns canned values so the unit can proceed (a repo that returns a fixed record).
   - **Mock/spy** — asserts the dependency was called correctly (args, count) when the interaction *is* the behavior under test.
   - **Fake** — a lightweight working implementation (in-memory repo, MSW handler) when many tests need realistic behavior.
   Prefer the simplest that fits; don't assert on calls that aren't the point of the test.
3. **Mock at the seam, against the real interface.** Replace the dependency at its boundary (the injected collaborator, the module import, the HTTP endpoint), and make the double honor the real signature/return type so the test fails if the contract drifts. Cover the cases the test needs: success, empty, and error/throw.
4. **Reset between tests.** Ensure mocks are cleared/restored in teardown so state doesn't leak across tests. Use the framework's reset (`afterEach(jest.clearAllMocks)`, `restore()`, autouse fixtures).

### Rules

1. Match the project's framework and mocking library exactly; don't add a new one unprompted.
2. Mock only external/slow/nondeterministic collaborators (network, db, clock, randomness, filesystem) — don't mock the unit under test or pure logic, and don't over-mock to the point the test asserts nothing real.
3. Keep doubles faithful to the real interface and reset them between tests so suites stay isolated and order-independent.
4. Prefer a fake or stub over a strict call-asserting mock unless the interaction itself is the behavior being verified — brittle "was-called-with" assertions on incidental calls make refactors painful.
5. After writing, show where the double is wired, what it returns/asserts, and the command to run the affected tests.
