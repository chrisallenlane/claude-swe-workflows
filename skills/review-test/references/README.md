# /review-test — Comprehensive Test Suite Survey

## Overview

The `/review-test` skill performs a five-phase test suite survey: unit coverage gaps, integration coverage gaps, E2E (browser) coverage gaps when applicable, fuzz coverage gaps, and test quality issues. It is **advisory only** — the skill does not implement test changes. After all phases run, it presents consolidated findings and proposes a ticket structure for the recommended work; the operator (human or orchestrator) approves, edits, or declines. On approval, tickets land in the issue tracker.

The plugin is moving `/review-*` skills toward advisory-only over time; `/review-test` joined `/review-arch`, `/review-security`, and `/bug-hunt` in this direction in v9.0.0. See the "Advisory aspiration" section of [`references/autonomy.md`](../../../references/autonomy.md) for the broader direction.

**Key benefits:**
- Systematic: surveys unit, integration, E2E, fuzz, and quality in deliberate order
- Inside-out by test scope: unit → integration → E2E, then fuzz, then quality
- Parallel analysis: large scopes are partitioned across multiple agents
- Conditional E2E: Phase 3 only runs for webapps; cleanly skips otherwise
- Operator (human or orchestrator) shapes the ticket plan before any tickets are cut
- Tickets carry per-phase context, acceptance criteria, and a recommended implementation skill
- Single workflow regardless of caller — orchestrators receive the offer like humans do

## When to Use

**Use `/review-test` for:**
- Coverage metrics below target or onboarding to an under-tested codebase
- After a burst of agent-written tests that may need quality review
- Before a release, to surface gaps and brittle tests
- Periodic comprehensive test-health checks
- Adding integration or E2E coverage to a project that lacks it (Mode A starter strategy)

**Don't use `/review-test` for:**
- Projects with no tests yet (write initial tests first, or scope a project via `/scope-project`)
- Quick one-off test additions (just write them directly, or use `/implement` against a small ticket)
- Mutation testing (use `/test-mutation` for that)

**Rule of thumb:** `/review-test` builds breadth (surfaces ticket-shaped work). `/test-mutation` builds depth (verifies tests actually catch bugs).

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ /review-test Workflow (advisory)                                │
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
 │  1c. Record findings by priority tier        │
 │      (CRITICAL → HIGH → LOW)                 │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  PHASE 2: INTEGRATION COVERAGE               │
 │  ────────────────────────────────────────    │
 │  2a. Analyze (qa-test-integration-reviewer)  │
 │  2b. Mode A (none) → starter strategy        │
 │      Mode B (exists) → gaps + expansion      │
 │  2c. Record findings                         │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  PHASE 3: E2E COVERAGE (webapps only)        │
 │  ────────────────────────────────────────    │
 │  3a. Webapp detection gate                   │
 │      Not a webapp? → Skip to Phase 4         │
 │  3b. Analyze (qa-test-e2e-reviewer)          │
 │  3c. Confirm journey classification (USER)   │
 │  3d. Record findings                         │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  PHASE 4: FUZZ COVERAGE                      │
 │  ────────────────────────────────────────    │
 │  4a. Analyze (qa-test-fuzz-reviewer)         │
 │  4b. Record candidates or "no infra" with    │
 │      tooling recommendation                  │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  PHASE 5: TEST QUALITY AUDIT                 │
 │  ────────────────────────────────────────    │
 │  5a. Scan for issues (qa-test-reviewer)      │
 │  5b. Record findings by category             │
 │      (DELETE / REWRITE / SIMPLIFY / ADD;     │
 │       redundant = informational)             │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  7. PRESENT CONSOLIDATED FINDINGS            │
 ├──────────────────────────────────────────────┤
 │  8. CUT TICKETS                              │
 │  • Propose ticket structure                  │
 │  • Operator approves / edits / declines      │
 │    (orchestrators apply autonomy judgment)   │
 │  • Create approved tickets in tracker        │
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

Findings are grouped by priority (CRITICAL / HIGH / LOW). REFACTOR-FOR-TESTABILITY suggestions are collected separately and presented in the consolidated report as informational items.

### Phase 2: Integration Coverage

A single `qa-test-integration-reviewer` agent surveys the project's integration testing posture. It first detects existing integration test infrastructure (directories, build tags / markers, runners, fixtures, CI), then surveys integration seams (databases, queues, external APIs, etc.).

The reviewer reports in one of two modes:

- **Mode A** (no integration tests detected): proposes a starter strategy anchored in the seams, the infrastructure needed to run integration tests in isolation (Makefile target, build tag, fixture compose file, README), and a starter test set capped at 5–8 high-value tests.
- **Mode B** (integration tests exist): identifies gaps within the existing strategy (capped at ~10 with HIGH/MEDIUM/LOW priority) and missing strategy categories (capped at ~3 with priority).

### Phase 3: E2E Coverage (webapps only)

A single `qa-test-e2e-reviewer` agent surveys the project's end-to-end (browser-driven) testing posture.

**Webapp detection gate:** the agent's first action is to detect whether the project is a webapp. Signals include:
- Frontend framework dependencies (React, Vue, Svelte, Angular, Next, Nuxt, Remix, Solid, Astro, Qwik, SvelteKit)
- Server-rendered HTML templates (Rails views, Django/Jinja, Twig, Blade, Phoenix, Go html/template)
- Static site generator config (Hugo, Jekyll, 11ty, Gatsby, Astro)
- Existing browser test config (Playwright, Cypress, Selenium, etc.)

If none are detected, the phase skips cleanly to Phase 4.

**Critical user journey survey:** for webapps, the reviewer reads README/product docs, maps auth-gated routes, identifies entry points and state-mutating forms, and classifies each journey as **Critical**, **Important**, or **Nice-to-have**. Journey classification is the most subjective input in the analysis; the orchestrator confirms classification with the user before finalizing the findings.

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

**Phase 3 is the most "human-in-the-loop" of the five phases.** The journey-classification confirmation step is intentionally interactive — Mode A starter-strategy recommendations are the highest-risk findings in the skill (wrong E2E strategy = days of wasted work plus chronic maintenance pain), and the explicit user confirmation guards against acting on misclassifications before they propagate into tickets.

### Phase 4: Fuzz Coverage

A single `qa-test-fuzz-reviewer` agent checks whether fuzz testing infrastructure exists and identifies functions that are good fuzz candidates.

If no fuzz infrastructure is detected, the phase records the agent's tooling recommendation as an informational entry that may be cut as a ticket per the runtime ticket-structure proposal. No attempt is made to set up fuzz tooling within `/review-test`.

### Phase 5: Test Quality Audit

For large scopes (>15 test files), the audit is partitioned across multiple `qa-test-reviewer` agents running in parallel.

Issue categories and recommended actions on the resulting ticket(s):

| Category         | Action   | Description                                    |
|------------------|----------|------------------------------------------------|
| Tautological     | DELETE   | Tests that can't fail                          |
| Brittle          | REWRITE  | Tests coupled to implementation details        |
| False confidence | REWRITE  | Tests that don't verify what they claim        |
| Inconsistent     | SIMPLIFY | Mixed assertion strategies                     |
| Missing          | ADD      | Important gaps not caught in Phases 1–4        |
| Redundant        | (info)   | Duplicate coverage — reported but not actioned |

The implementer working a Phase 5 ticket retains the discretion to REWRITE rather than DELETE if the test covers real behavior that could regress — this caveat is included in every DELETE-containing ticket body.

## Cut Tickets — Ticket-Structure Proposal

After all five phases have run and the consolidated findings have been presented, the skill proposes a ticket structure based on the review's shape. Common shapes include:

- **Concentrated unit gaps + small integration/E2E asks:** one ticket per CRITICAL unit gap; one batch ticket per HIGH/LOW tier; one ticket per integration or E2E gap; one batch for Phase-5 quality issues.
- **Mode A starter strategies dominate:** one ticket per phase's starter strategy; individual tickets for unit/quality findings only if there are few.
- **Lots of Phase-5 churn:** one batch ticket per quality category.
- **Light review, scattered findings:** one batch ticket per phase covering all findings.
- **No actionable findings:** no tickets; the review report stands alone.

The operator approves / edits / declines:

- **Approve:** tickets are cut as proposed.
- **Edit:** the structure is revised (merge tickets, split, drop a finding, promote refactor-for-testability suggestions to tickets, change granularity). Repeat until approved.
- **Decline:** the review report stands alone.

**Tickets include:**
- Per-finding body sections (gap, files, risk, "should verify," acceptance criteria, recommended implementation skill).
- For Mode A starter strategies: strategy + infrastructure + starter tests + out-of-scope + acceptance criteria.
- For Phase 5: per-test recommendation (DELETE / REWRITE / SIMPLIFY) with the "rewrite-if-still-valuable" caveat preserved for DELETE items.
- Phase-type labels (`test-coverage`, `integration-test`, `e2e`, `fuzz`, `test-quality`) when the tracker supports them.

## Orchestrator-Invoked Behavior

When `/review-test` is invoked by an orchestrator (`/lead-project`, `/review-deep`, `/implement-project`), the workflow above is unchanged. The orchestrator receives the ticket-structure proposal and applies its own judgment per [`references/autonomy.md`](../../../references/autonomy.md) — typically declining items it intends to implement inline and approving items it wants tracked for follow-up.

## Agent Coordination

| Phase   | Analysis Agent                  | Parallelized    |
|---------|---------------------------------|-----------------|
| Phase 1 | `qa-test-coverage-reviewer`     | Yes (>15 files) |
| Phase 2 | `qa-test-integration-reviewer`  | No (single)     |
| Phase 3 | `qa-test-e2e-reviewer`          | No (single)     |
| Phase 4 | `qa-test-fuzz-reviewer`         | No (single)     |
| Phase 5 | `qa-test-reviewer`              | Yes (>15 files) |

**No implementation agents.** `/review-test` does not spawn `swe-sme-*` or `qa-engineer` agents. Test design and implementation are handled out-of-skill by `/implement` or `/implement-project` against the cut tickets.

**Fresh instances:** Every agent spawn is a fresh instance. No state carried between invocations.

**State maintained by orchestrator:**
- Scope (shared across all phases)
- Coverage command and baseline metrics
- Webapp detection result (used to skip Phase 3 cleanly)
- Confirmed journey classification (Phase 3, after user correction)
- Per-phase findings (accumulating)
- Refactoring suggestions (held for informational section)
- Tickets created at step 8 (if any)

## Tips for Effective Use

1. **The findings presentation (step 7) is where most of the value lands.** Take time with CRITICAL items and any Mode A starter-strategy proposals; these shape the ticket plan more than any other phase output.

2. **Ticket creation is opt-in.** If you want the analysis as a planning artifact rather than a set of tickets, decline at step 8. The findings stand on their own.

3. **Promote refactor-for-testability suggestions explicitly.** They default to informational; if you want them tracked, edit the structure during step 8a to add one ticket per suggestion (or one batch ticket if they're related).

4. **Orchestrators apply their own judgment to the offer.** When invoked from `/implement-project` or `/lead-project`, the orchestrator typically declines items it intends to implement inline and approves items it wants tracked for follow-up. Both responses are valid per `references/autonomy.md`.

5. **Consider running `/refactor` first.** If the codebase has tactical clutter, `/refactor` can clean it before `/review-test` analyzes coverage — the coverage analyst is more useful when it isn't navigating dead code and DRY violations.

6. **Scope aggressively for large codebases.** `/review-test pkg/core/` targets a specific module; better than analyzing everything when you already know where the gaps are.

## Integration with Other Skills

| Skill            | Relationship                                                                              |
|------------------|-------------------------------------------------------------------------------------------|
| `/test-mutation` | Complementary. `/review-test` builds breadth (surfaces tickets); `/test-mutation` builds depth. |
| `/implement`     | Pick up tickets cut by `/review-test`. `/implement` includes QA as part of feature development. |
| `/implement-project` | Batch tickets cut by `/review-test` and work them together.                            |
| `/refactor`      | Run `/review-test` before refactoring to surface gaps as tickets; work those before refactoring if needed. |
| `/review-a11y`   | Phase 3 explicitly defers accessibility to `/review-a11y`. Complementary.                  |
| `/review-perf`   | Phase 3 explicitly defers web performance to `/review-perf` / `swe-web-perf-reviewer`.    |
| `/review-arch`   | `/review-arch` is advisory (architectural analysis); Phase 2 of `/review-test` does its own lightweight survey for integration seams. |

Recommended sequence for test improvement: `/review-test` first (surface ticket-shaped work) → `/implement` or `/implement-project` (remediate) → `/test-mutation` (strengthen).
