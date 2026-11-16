# /review-test — Comprehensive Test Suite Survey

The step-by-step procedure lives in [`SKILL.md`](../SKILL.md); this guide covers when to use the skill and what to expect.

## Overview

`/review-test` surveys a test suite in five phases: unit coverage gaps, integration coverage, E2E (browser) coverage for webapps, fuzz coverage, and test quality. It presents consolidated findings, then proposes a ticket structure for the recommended work. You approve, edit, or decline it.

**Tests are a system, not a checklist.** Unit gaps, integration gaps, E2E gaps, fuzz gaps, and bad tests are facets of one problem: the suite isn't doing its job. The phases run inside-out by test scope (unit → integration → E2E), then fuzz, then a quality audit over everything that exists today.

**Advisory only.** The skill never writes, deletes, or rewrites tests. Finding a gap and designing a test for it take different reasoning, and the discovery agents shouldn't be biased toward gaps that are easy to fill. Removing or rewriting an existing test is a decision you should approve explicitly, via a ticket, not a side effect of a review. `/implement` works the tickets.

```
Scope ──▶ Unit ──▶ Integration ──▶ E2E (webapps only) ──▶ Fuzz ──▶ Quality ──▶ Report ──▶ Ticket proposal
```

## When to Use

**Use `/review-test` for:**
- Coverage below target, or onboarding to an under-tested codebase
- After a burst of agent-written tests that may need quality review
- Before a release, to surface gaps and brittle tests
- Periodic comprehensive test-health checks
- Adding integration or E2E coverage to a project that lacks it (a starter strategy)

**Don't use `/review-test` for:**
- Projects with no tests yet: write initial tests first, or scope the work via `/scope`
- Quick one-off test additions: write them directly, or use `/implement` against a small ticket
- Checking whether existing tests actually catch bugs: that's `/test-mutation`

**`/review-test` vs `/test-mutation`:** `/review-test` builds breadth (it surfaces ticket-shaped work); `/test-mutation` builds depth (it verifies tests catch bugs). A good sequence is `/review-test` → `/implement` the tickets → `/test-mutation`.

**After `/refactor`:** `/refactor` pins behavior with a differential oracle rather than the test suite, and retires tests that pin internals it removed. Run `/review-test` afterward to see what the reduced codebase's suite covers.

## What You'll Be Asked

- **Scope,** unless the invocation or caller supplies it: the entire project (default), a directory, specific files, or the current branch's changes. On a large project the skill suggests narrowing.
- **A coverage command,** only if no coverage report exists and none can be detected from the build files. Without one, unit-gap analysis falls back to reading the code, and coverage isn't measured.
- **The E2E journey classification,** for webapps only. The skill shows which user journeys it classified Critical, Important, and Nice-to-have, and asks you to confirm or correct them. This is the most subjective input in the review, and a wrong E2E starter strategy costs days of work plus chronic maintenance, so it's deliberately a human checkpoint.

## What You Get Back

A consolidated report with one section per phase:

| Phase       | What it reports                                                                                                                                   |
|-------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| Unit        | Coverage baseline (if measured) and untested paths tiered CRITICAL / HIGH / LOW; refactor-for-testability suggestions, informational              |
| Integration | Either a starter strategy (no integration tests yet) or gaps within the existing strategy plus missing strategies                                 |
| E2E         | Skipped if not a webapp. Otherwise a Playwright starter strategy (no E2E yet), or gaps within your existing framework; it never pushes migration  |
| Fuzz        | Fuzz candidates by priority; if there's no fuzz tooling, a starter-tooling recommendation the candidates depend on                                |
| Quality     | Existing tests flagged DELETE (tautological), REWRITE (brittle, false confidence, inconsistent), or SIMPLIFY (smells); redundant is informational |

E2E is scoped to browser-driven journeys; visual regression, accessibility (`/review-a11y`), web performance, component-level testing, and mobile-native UI are declared out of scope.

Then a **ticket proposal** shaped to the findings: for example, one ticket per CRITICAL unit gap, batches for lower tiers, one ticket per starter strategy, and batches per quality category. A clean review proposes nothing. Tickets carry acceptance criteria and a recommended implementation skill, and any DELETE item keeps the reviewer's caveat to rewrite rather than delete if the test covers real behavior. When an orchestrator invokes the skill, it receives the same proposal and applies its own autonomy judgment, typically declining items it will implement inline.

## Tips

1. **The findings walkthrough is where most of the value lands.** Engage with CRITICAL items and starter-strategy proposals before the ticket proposal; they shape the plan more than anything else.
2. **Declining tickets is fine.** The report stands on its own as a planning artifact.
3. **Promote refactor-for-testability suggestions explicitly.** They default to informational; edit the ticket proposal to track them.
4. **Scope aggressively on large codebases.** `/review-test pkg/core/` beats analyzing everything when you already know where the gaps are.

## Example — Ticket Proposal

```
Phase 1: 8 gaps (2 CRITICAL, 3 HIGH, 3 LOW)
Phase 2: existing strategy — 4 gaps
Phase 3: no E2E present — Playwright infrastructure + 5 starter tests
Phase 4: 2 fuzz candidates (1 HIGH, 1 MEDIUM)
Phase 5: 5 findings (2 DELETE, 3 REWRITE; 2 redundant — informational)

Proposed: 7 tickets
  - 1 ticket per CRITICAL unit gap (2 tickets)
  - 1 batch ticket: "Phase 1 — HIGH/LOW unit coverage gaps" (6 gaps)
  - 1 batch ticket: "Phase 2 — Integration gaps within existing strategy" (4 gaps)
  - 1 ticket: "Set up Playwright E2E infrastructure + 5 starter tests"
  - 1 batch ticket: "Phase 4 — Fuzz test additions" (2 candidates)
  - 1 batch ticket: "Phase 5 — Test quality cleanup" (DELETE + REWRITE)
  - (Refactor-for-testability suggestions held as informational — no ticket)

Approve / edit / decline?
```
