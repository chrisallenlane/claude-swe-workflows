# /review-test - Comprehensive Test Suite Review

## Overview

The `/review-test` skill performs a five-phase test suite review: fill unit coverage gaps, survey integration coverage, survey E2E (browser) coverage when applicable, identify missing fuzz tests, and audit test quality. Each phase runs its own analysis → present → select → implement → verify cycle.

**Key benefits:**
- Systematic: addresses unit, integration, E2E, fuzz, and quality in deliberate order
- Inside-out by test scope: unit → integration → E2E, then fuzz, then quality
- Interactive: you see findings and choose what to address at each phase
- Parallel analysis: large scopes are partitioned across multiple agents
- Language-aware: dispatches to appropriate SME agents for implementation
- Measures improvement: before/after coverage comparison when tooling is available
- Conditional E2E: Phase 3 only runs for webapps; cleanly skips otherwise

## When to Use

**Use `/review-test` for:**
- Coverage metrics below target or onboarding to an under-tested codebase
- After a burst of agent-written tests that may need quality review
- Before a release, to strengthen and clean up the test suite
- Periodic comprehensive test health checks
- Adding integration or E2E coverage to a project that lacks it (Mode A starter strategy)

**Don't use `/review-test` for:**
- Projects with no tests yet (write initial tests first)
- Quick one-off test additions (just write them directly)
- Mutation testing (use `/test-mutation` for that)

**Rule of thumb:** `/review-test` builds breadth (fill gaps, clean up). `/test-mutation` builds depth (verify tests actually catch bugs).

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ /review-test Workflow                                           │
└─────────────────────────────────────────────────────────────────┘

 ┌──────────────────────────────────────────────┐
 │  1. DETERMINE SCOPE                          │
 │  ────────────────────────────────────────    │
 │  • Entire project (default)                  │
 │  • Specific directory or files               │
 │  • Recent changes (git diff)                 │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  PHASE 1: UNIT COVERAGE GAPS                 │
 │  ────────────────────────────────────────    │
 │  1a. Detect/obtain coverage data             │
 │      (existing report → generate → ask →     │
 │       manual analysis fallback)              │
 │  1b. Analyze gaps (qa-test-coverage-reviewer)│
 │  1c. Present findings by priority tier       │
 │      (CRITICAL → HIGH → LOW)                 │
 │  1d. User selects which gaps to fill         │
 │  1e. SME implements selected tests           │
 │  1f. Verify + re-run coverage                │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  PHASE 2: INTEGRATION COVERAGE               │
 │  ────────────────────────────────────────    │
 │  2a. Analyze (qa-test-integration-reviewer)  │
 │      • Detect existing integration infra     │
 │      • Survey integration seams              │
 │  2b. Mode A (none) → starter strategy        │
 │      Mode B (exists) → gaps + expansion      │
 │  2c. Present + user selection                │
 │  2d. Implement (infra first, then tests)     │
 │  2e. Verify (compile-check; user runs suite) │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  PHASE 3: E2E COVERAGE (webapps only)        │
 │  ────────────────────────────────────────    │
 │  3a. Webapp detection gate                   │
 │      Not a webapp? → Skip to Phase 4         │
 │  3b. Analyze (qa-test-e2e-reviewer)          │
 │      • Survey critical user journeys         │
 │      • Classify Critical/Important/N-T-H     │
 │  3c. Confirm journey classification (USER)   │
 │  3d. Mode A → prescribe Playwright           │
 │      Mode B → respect existing framework     │
 │  3e. SME implements (swe-sme-typescript)     │
 │  3f. Verify (compile-check; user runs suite) │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  PHASE 4: FUZZ COVERAGE                      │
 │  ────────────────────────────────────────    │
 │  4a. Analyze (qa-test-fuzz-reviewer)         │
 │  4b. Check infrastructure                    │
 │      No fuzz infra? → Skip to Phase 5        │
 │  4c. Present candidates + user selection     │
 │  4d. SME implements fuzz tests               │
 │  4e. Verify (compilation + seed corpus)      │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  PHASE 5: TEST QUALITY AUDIT                 │
 │  ────────────────────────────────────────    │
 │  5a. Scan for issues (qa-test-reviewer)      │
 │      • Tautological (can't fail)             │
 │      • Brittle (coupled to implementation)   │
 │      • Redundant (informational only)        │
 │      • False confidence                      │
 │      • Inconsistent assertions               │
 │  5b. Present findings + user selection       │
 │  5c. SME implements changes                  │
 │  5d. Verify                                  │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  SUMMARY + OPTIONAL COMMIT                   │
 │  ────────────────────────────────────────    │
 │  • Per-phase results                         │
 │  • Net test count change                     │
 │  • Coverage improvement (if measurable)      │
 │  • Refactoring-for-testability suggestions   │
 └──────────────────────────────────────────────┘
```

## Phase Details

### Phase 1: Unit Coverage Gaps

Detects or generates a coverage report using a four-step waterfall:

1. **Check for existing artifacts** (coverage.out, lcov.info, etc.)
2. **Detect coverage command** from build files (Makefile, package.json, go.mod, etc.)
3. **Ask the user** for the correct command
4. **Manual analysis fallback** — read source and test files to identify gaps by inspection

For large scopes (>15 source files), the analysis is partitioned across multiple `qa-test-coverage-reviewer` agents running in parallel.

Findings are grouped by priority (CRITICAL / HIGH / LOW). Refactoring-for-testability suggestions are collected separately and presented in the final summary.

### Phase 2: Integration Coverage

A single `qa-test-integration-reviewer` agent surveys the project's integration testing posture. It first detects existing integration test infrastructure (directories, build tags / markers, runners, fixtures, CI), then surveys integration seams (databases, queues, external APIs, etc.).

The reviewer reports in one of two modes:

- **Mode A** (no integration tests detected): proposes a starter strategy anchored in the seams, the infrastructure needed to run integration tests in isolation (Makefile target, build tag, fixture compose file, README), and a starter test set capped at 5–8 high-value tests.
- **Mode B** (integration tests exist): identifies gaps within the existing strategy (capped at ~10 with HIGH/MEDIUM/LOW priority) and missing strategy categories (capped at ~3 with priority).

**Verification is intentionally light.** Integration tests are slow and may require fixtures up. The phase compile-checks new tests and confirms unit tests still pass, then prompts the user to run the integration suite ad-hoc — the suite is **not run automatically**.

### Phase 3: E2E Coverage (webapps only)

A single `qa-test-e2e-reviewer` agent surveys the project's end-to-end (browser-driven) testing posture.

**Webapp detection gate:** the agent's first action is to detect whether the project is a webapp. Signals include:
- Frontend framework dependencies (React, Vue, Svelte, Angular, Next, Nuxt, Remix, Solid, Astro, Qwik, SvelteKit)
- Server-rendered HTML templates (Rails views, Django/Jinja, Twig, Blade, Phoenix, Go html/template)
- Static site generator config (Hugo, Jekyll, 11ty, Gatsby, Astro)
- Existing browser test config (Playwright, Cypress, Selenium, etc.)

If none are detected, the phase skips cleanly to Phase 4.

**Critical user journey survey:** for webapps, the reviewer reads README/product docs, maps auth-gated routes, identifies entry points and state-mutating forms, and classifies each journey as **Critical**, **Important**, or **Nice-to-have**. Journey classification is the most subjective input in the analysis; the orchestrator confirms classification with the user before any implementation begins.

The reviewer reports in one of two modes:

- **Mode A** (no E2E detected): **prescribes Playwright unconditionally** for greenfield webapp E2E. Proposes Playwright config, test directory, fixture/seeding strategy (load-bearing — without it, E2E is non-deterministic), and a starter test set capped at ~5 (E2E maintenance is expensive).
- **Mode B** (E2E exists): respects the existing framework (Playwright, Cypress, Selenium, etc.) and recommends gaps within the strategy (~6) and strategy expansion (~2). **Does not push migration** away from Cypress/Selenium/etc.; an informational note about Playwright as the modern recommendation may appear, but no action.

**Out of scope (declared in the agent's output):**
- Visual regression testing — not Phase 3
- Accessibility — handled by `/review-a11y` and `qa-web-a11y-reviewer`
- Web performance — handled by `swe-web-perf-reviewer`
- Cross-browser / viewport / locale matrices — surfaced as gaps only if the project actually targets multiple
- Component-level testing (Storybook, RTL) — between unit and E2E; not Phase 3
- Mobile native UI — browser-only

**Verification is intentionally light.** E2E tests require a running test environment, fixtures, and browser binaries. The phase compile/type-checks new tests and confirms unit tests still pass, then prompts the user to run the E2E suite ad-hoc — the suite is **not run automatically**.

**Phase 3 is the most "human-in-the-loop" of the five phases.** The journey classification confirmation step is intentionally interactive — Mode A starter-strategy recommendations are the highest-risk in the entire skill (wrong E2E strategy = days of wasted work plus chronic maintenance pain), and the explicit user confirmation guards against acting on misclassifications.

### Phase 4: Fuzz Coverage

A single `qa-test-fuzz-reviewer` agent checks whether fuzz testing infrastructure exists and identifies functions that are good fuzz candidates.

If no fuzz infrastructure is detected, the phase is skipped with a recommendation for tooling. No attempt is made to set up fuzz tooling.

### Phase 5: Test Quality Audit

For large scopes (>15 test files), the audit is partitioned across multiple `qa-test-reviewer` agents running in parallel.

Issue categories and recommended actions:

| Category         | Action   | Description                                    |
|------------------|----------|------------------------------------------------|
| Tautological     | DELETE   | Tests that can't fail                          |
| Brittle          | REWRITE  | Tests coupled to implementation details        |
| False confidence | REWRITE  | Tests that don't verify what they claim        |
| Inconsistent     | SIMPLIFY | Mixed assertion strategies                     |
| Missing          | ADD      | Important gaps not caught in Phases 1–4        |
| Redundant        | (info)   | Duplicate coverage — reported but not actioned |

SMEs receiving DELETE recommendations may choose to REWRITE instead if the test covers real behavior that could regress.

## Example Session

```
> /review-test

What should I review?
> Entire project

## Phase 1: Unit Coverage Gap Analysis

Overall coverage: 68.3% lines (baseline)

### CRITICAL (2 found)
1. [ADD] auth.go:ValidateJWT (lines 45-72) — error paths untested
2. [ADD] payment.go:ChargeCard (lines 88-120) — retry logic untested

### HIGH (3 found)
3. [ADD] parser.go:ParseConfig (lines 30-55) — malformed input
4. [ADD] api.go:CreateUser (lines 15-40) — duplicate email conflict
5. [ADD] middleware.go:RateLimit (lines 22-45) — limit exceeded path

Select which gaps to fill:
> 1-5

Writing tests... Verifying...

Coverage: 68.3% → 78.1% (+9.8%)

## Phase 2: Integration Coverage

Integration test posture: NONE DETECTED (Mode A)
Seams identified: 4 (PostgreSQL, Redis cache, Stripe API, Kafka consumer)

### Proposed Strategy
- Service-level tests with testcontainers (Postgres + Kafka)
- HTTP-level tests against spun-up app

### Proposed Infrastructure
- `make integration-test` with `//go:build integration` tag
- `docker-compose.test.yml`
- `tests/integration/README.md`

### Starter Tests (5)
1. [ADD] Signup → DB persistence → email queued (CRITICAL flow)
2. [ADD] Payment webhook → Stripe sig verification → DB write
3. [ADD] Login → session token → Redis store
4. [ADD] Order placement → queue produce → consumer process
5. [ADD] Account deletion → cascade across tables

Select what to implement:
> infrastructure, 1, 2, 3

Setting up infrastructure... Writing tests... Compile-check...

Run integration tests now? Requires `docker-compose up`. [y/N]
> n

Note: integration tests pending manual verification.

## Phase 3: E2E Coverage

Webapp detection: DETECTED via @playwright/test in package.json + React deps
E2E posture: NONE DETECTED (Mode A)

### Critical User Journeys (please confirm)

CRITICAL:
- Signup → email confirmation → first-login flow
- Login → session establishment
- Core checkout flow (cart → payment → confirmation)

IMPORTANT:
- Password reset
- Profile settings update

⚠️  Journey classification is the most subjective part of this analysis.

Are these classifications correct?
> Yes

### Prescribed Framework: Playwright

### Proposed Infrastructure
- `playwright.config.ts` (Chromium + Firefox + WebKit, headless default)
- `tests/e2e/` directory
- `npm run test:e2e` script
- Fixture: dedicated test users seed + per-test API setup
- `tests/e2e/README.md`

### Starter Tests (5)
1. Signup flow → /welcome (CRITICAL)
2. Login flow → /dashboard (CRITICAL)
3. Checkout happy path (CRITICAL)
4. Password reset (IMPORTANT)
5. Profile update (IMPORTANT)

Out of scope: visual regression, a11y, performance, mobile-native, component tests.

Select what to implement:
> infrastructure, all

Setting up Playwright... Writing tests... Type-check...

Run E2E tests now? Requires environment up + browser binaries. [y/N]
> n

Note: E2E tests pending manual verification.

## Phase 4: Fuzz Coverage

Fuzz infrastructure: native testing.F (Go 1.22)

### HIGH (2 found)
1. [ADD] parser.go:ParseConfig — arbitrary []byte input
2. [ADD] protocol.go:DecodeMessage — wire protocol messages

Select which fuzz tests to add:
> all

Writing fuzz tests... Verifying...

## Phase 5: Test Quality Audit

### Tautological (2 found)
1. [DELETE] model_test.go:TestUserStruct — checks struct fields exist
2. [DELETE] config_test.go:TestDefaultConfig — asserts hardcoded values

### Brittle (1 found)
3. [REWRITE] api_test.go:TestCreateUserError — exact error string match

Select which items to address:
> all

Implementing changes... Verifying...

## Test Review Complete

### Phase 1: Unit Coverage Gaps
- Tests added: 5
- Coverage: 68.3% → 78.1% (+9.8%)

### Phase 2: Integration Coverage
- Mode: A (starter strategy adopted)
- Infrastructure added: yes
- Tests added: 3
- Manual run pending: yes

### Phase 3: E2E Coverage
- Webapp: yes
- Mode: A (Playwright starter strategy)
- Infrastructure added: yes
- Tests added: 5
- Manual run pending: yes

### Phase 4: Fuzz Coverage
- Fuzz tests added: 2

### Phase 5: Test Quality Audit
- Tests deleted: 2
- Tests rewritten: 1

### Net Change
- Total tests added: 15
- Total tests removed: 2
- Net: +13

Commit? > yes
```

### Mode B example (Phase 2)

```
## Phase 2: Integration Coverage

Integration test posture: testcontainers (Postgres), `make integration-test`
Existing tests: 12 (DB suite covering CRUD on Users, Orders, Payments)

### Gaps Within Existing Strategy (3 found)
1. [HIGH] DB suite — `DeleteUser` cascade not tested. Risk: orphan rows on account deletion.
2. [MEDIUM] DB suite — `UpdateOrder` concurrent-write path not tested.
3. [LOW] DB suite — pagination edge cases (empty, max page size).

### Strategy Expansion (1 found)
4. [HIGH] Queue consumer — Kafka consumer has no integration tests despite carrying critical order-processing flow.

Select which items to address:
> 1, 4
```

### Mode B example (Phase 3, existing Cypress)

```
## Phase 3: E2E Coverage

Webapp detection: DETECTED via @cypress/test in package.json
E2E posture: Cypress (cypress/e2e/, npm run cypress:run, 8 existing tests)

### Critical User Journeys
[...]

### Mode B: Cypress detected — recommendations stay within Cypress

### Gaps Within Existing Strategy (3 found)
1. [HIGH] Signup flow tested but email-verification step not exercised.
2. [MEDIUM] Profile settings — only happy path tested; validation-error path missing.
3. [LOW] Search results — no test for empty-result state.

### Strategy Expansion (1 found)
4. [HIGH] Authenticated marketing app untested; only public marketing covered.

> Note: Playwright is the modern recommendation for new projects. Migration is
> out of scope here; recommendations above are made within your existing Cypress framework.

Select which items to address:
```

## Agent Coordination

| Phase   | Analysis Agent                  | Parallelized    | Implementation                    |
|---------|---------------------------------|-----------------|-----------------------------------|
| Phase 1 | `qa-test-coverage-reviewer`     | Yes (>15 files) | Language SME                      |
| Phase 2 | `qa-test-integration-reviewer`  | No (single)     | Language SME                      |
| Phase 3 | `qa-test-e2e-reviewer`          | No (single)     | `swe-sme-typescript` (Playwright default), other SME for Mode B non-Playwright |
| Phase 4 | `qa-test-fuzz-reviewer`         | No (single)     | Language SME                      |
| Phase 5 | `qa-test-reviewer`              | Yes (>15 files) | Language SME                      |

Implementation is always parallelized by target test file — findings targeting the same file go to the same SME agent.

**Fresh instances:** Every agent spawn is a fresh instance. No state carried between invocations.

**State maintained by orchestrator:**
- Scope (shared across all phases)
- Coverage command and baseline metrics
- Webapp detection result (used to skip Phase 3 cleanly)
- Confirmed journey classification (Phase 3, after user correction)
- User selections for each phase
- Implementation results per phase
- Refactoring suggestions (held for final summary)
- Running totals for summary

## Verification Policy by Phase

| Phase   | Auto-run on verify?       | Why                                                              |
|---------|---------------------------|------------------------------------------------------------------|
| Phase 1 | Yes (full unit test run)  | Unit tests are fast and self-contained                           |
| Phase 2 | **No**                    | Integration suite slow + may need fixtures up; user runs ad-hoc  |
| Phase 3 | **No**                    | E2E requires environment up + browser binaries; user runs ad-hoc |
| Phase 4 | Compile-check only        | Fuzz tests run indefinitely; only seed corpus is auto-verified   |
| Phase 5 | Yes (full unit test run)  | Quality audit changes touch unit tests primarily                 |

For Phases 2 and 3, the orchestrator prompts the user to run the suite manually after compile-check confirms the new tests are well-formed.

## Integration with Other Skills

| Skill            | Relationship                                                                              |
|------------------|-------------------------------------------------------------------------------------------|
| `/test-mutation` | Complementary. `/review-test` builds breadth, `/test-mutation` builds depth.              |
| `/implement`     | `/implement` includes QA as part of feature development. `/review-test` is a standalone audit. |
| `/refactor`      | Run `/review-test` before refactoring to ensure tests are strong enough to catch regressions. |
| `/review-a11y`   | Phase 3 explicitly defers accessibility to `/review-a11y`. They are complementary.         |
| `/review-perf`   | Phase 3 explicitly defers web performance to `/review-perf` / `swe-web-perf-reviewer`.    |
| `/review-arch`   | `/review-arch` is advisory (architectural analysis); Phase 2 does its own lightweight survey for integration seams. |

Recommended sequence for test improvement: `/review-test` first (fill gaps, clean up), then `/test-mutation` (verify tests catch bugs).
