---
name: review-test
description: Test suite review covering unit, integration, E2E (browser), and fuzz coverage plus test quality. Advisory only; produces findings and proposes tickets, does not change tests.
model: opus
---

# Test Review — Comprehensive Test Suite Survey

Five-phase survey: unit coverage gaps, integration coverage gaps, E2E (browser) coverage gaps when applicable, fuzz coverage gaps, then test quality issues. Each phase runs its analysis and contributes findings to a consolidated report; at the end, the skill proposes a ticket structure for the recommended work and creates tickets after operator approval.

**Advisory only.** The skill produces findings and proposes tickets; it does not implement test changes. The cognitive seam between "find a coverage gap" and "design a test for it" is wide enough that mixing them under one workflow degrades both — test design requires fresh reasoning about edge cases, mocking strategy, and assertion shape, and the discovery agents shouldn't be biased toward gaps whose fixes are easy. Tickets capture findings durably across that seam and compose with `/implement` for remediation.

The same logic applies in reverse to test-quality findings (DELETE / REWRITE / SIMPLIFY): the operator should approve removing or rewriting an existing test explicitly, via a ticket, rather than have a workflow do it as a side effect of running a review.

## Philosophy

**Tests are a system, not a checklist.** Unit gaps, integration gaps, E2E gaps, fuzz gaps, and bad tests are different facets of the same problem: the test suite isn't doing its job. This workflow surveys all of them in deliberate order — inside-out by test scope (unit → integration → E2E), then fuzz as an addendum, then quality covers everything that exists today.

## Workflow Overview

```
┌──────────────────────────────────────────────────┐
│                  TEST REVIEW                     │
├──────────────────────────────────────────────────┤
│  1. Determine scope                              │
│  2. Phase 1: Unit coverage gaps                  │
│  3. Phase 2: Integration coverage                │
│  4. Phase 3: E2E coverage (webapps only)         │
│  5. Phase 4: Fuzz coverage                       │
│  6. Phase 5: Test quality audit                  │
│  7. Present consolidated findings                │
│  8. Cut tickets (proposed structure, operator-   │
│     approved)                                    │
└──────────────────────────────────────────────────┘
```

## Workflow Details

### 1. Determine Scope

If the invocation or caller supplies scope, use it and skip this question. Otherwise, **ask the user:** "What should I review?"

Present these options:
- **Entire project**: Review all source and test files (default)
- **Specific directory**: A path like `src/`, `pkg/`, `lib/`
- **Specific files**: Individual source files
- **Recent changes**: Files modified on the current branch (via `git diff`)

**Default:** Entire project.

**If the project is large** (many source files), suggest narrowing scope. The user can always re-run on a different scope.

This scope applies to all five phases.

## Phase 1: Unit Coverage Gaps

Survey missing unit-level test coverage, prioritized by risk.

### 1a. Detect/Obtain Coverage Data

Follow this waterfall — stop at the first step that produces a usable report.

**Step A: Check for existing coverage artifacts**

Search for coverage files in common locations:

| Format       | Files to search for                                                              |
| ------------ | -------------------------------------------------------------------------------- |
| Go           | `coverage.out`, `cover.out`, `c.out`                                             |
| lcov         | `lcov.info`, `coverage/lcov.info`                                                |
| Istanbul/nyc | `coverage/coverage-summary.json`, `coverage/coverage-final.json`, `.nyc_output/` |
| coverage.py  | `coverage.xml`, `coverage.json`, `htmlcov/`                                      |
| JaCoCo       | `target/site/jacoco/jacoco.xml`, `build/reports/jacoco/*/jacoco.xml`             |
| Cobertura    | `coverage.xml`, `cobertura.xml`                                                  |

If a report is found, verify it's reasonably recent (warn if older than the most recent source change). Use the report and proceed.

**Step B: Detect coverage command**

If no report exists, detect how to generate one:

1. `Makefile` with a `cover` or `coverage` target → `make cover` (or `make coverage`)
2. `package.json` with a `coverage` script → `npm run coverage`
3. `go.mod` present → `go test -coverprofile=coverage.out ./...`
4. `pyproject.toml` / `setup.cfg` / `pytest.ini` with coverage config → `pytest --cov --cov-report=json`
5. `Cargo.toml` → `cargo tarpaulin --out json` (or `cargo llvm-cov --json`)
6. `build.gradle` / `build.gradle.kts` → `gradle jacocoTestReport`

Run the command and verify it produces a report. If it fails, ask the user for the correct command.

**Step C: Ask the user**

If no coverage tooling is detected: "What command generates a coverage report for this project?"

**Step D: Manual analysis fallback**

If no coverage tooling is available, proceed with manual analysis. The agent will read source and test files to identify gaps by inspection.

**Note:** In manual analysis mode, quantitative coverage measurement is unavailable.

**Store:** the coverage command (if any) and baseline coverage percentage.

### 1b. Analyze Coverage Gaps

**Assess scope size** with Glob.

**Small scope (roughly ≤15 source files):** Spawn a single `qa-test-coverage-reviewer` agent with the full scope and coverage data.

**Large scope (roughly >15 source files):** Partition by directory or module. Spawn multiple `qa-test-coverage-reviewer` agents **in parallel**, each with a focused partition and relevant coverage data.

Merge findings into a single list ordered by priority tier (CRITICAL → HIGH → LOW). Collect REFACTOR-FOR-TESTABILITY suggestions separately — these are presented in the consolidated findings, not as ticket candidates by default.

**Prompt for each agent:**

```
Analyze test coverage gaps.
Scope: [partition or full scope]
Mode: [coverage report / coverage command / manual analysis]
Coverage data: [file path or "manual analysis — no data"]

Identify:
- Untested code paths prioritized by risk (CRITICAL / HIGH / LOW)
- Code that is structurally hard to test (REFACTOR-FOR-TESTABILITY suggestions)

Return structured findings with ADD recommendations and refactoring suggestions.
```

**If no significant gaps found:** Record "No significant coverage gaps found".

### 1c. Record Phase 1 Findings

Record findings grouped by priority tier (CRITICAL / HIGH / LOW) for the consolidated report in step 7. Hold the REFACTOR-FOR-TESTABILITY suggestions separately — they appear as an informational section in the final report; they may or may not be cut as tickets per the runtime ticket-structure proposal in step 8.

## Phase 2: Integration Coverage

Survey integration test coverage and identify gaps or, if none exist, a starter strategy.

### 2a. Analyze Integration Coverage

Spawn a single `qa-test-integration-reviewer` agent.

**Prompt:**

```
Review integration test coverage for this project.
Scope: [full scope from step 1]

Detect:
- Existing integration test infrastructure (frameworks, directories, markers, runners, fixtures, CI)
- Integration seams (databases, queues, external APIs, etc.)

If no integration tests exist (Mode A), recommend a starter strategy with infrastructure
and ~5-8 starter tests. If integration tests exist (Mode B), identify gaps within the
strategy (cap ~10) and missing strategies (cap ~3).

Return findings per the agent's output format, with calibrated confidence.
```

### 2b. Record Phase 2 Findings

The agent reports in one of two modes.

**Mode A (no integration tests detected):** the agent proposes a starter strategy with infrastructure and starter tests. Record the strategy, infrastructure proposal, and starter tests.

**Mode B (integration tests detected):** the agent reports gaps within the strategy and strategy-expansion opportunities. Record them with their priorities.

**If the agent reports "no findings"** (Mode B with empty gaps and expansion), record the existing posture briefly and proceed.

## Phase 3: E2E Coverage

Survey end-to-end (browser-driven) test coverage and identify gaps or, if none exist, a starter strategy using Playwright. **This phase only applies to webapps.**

### 3a. Analyze E2E Coverage

Spawn a single `qa-test-e2e-reviewer` agent. Its Step 0 is the webapp gate: if it reports "NOT A WEBAPP", record "Phase 3 skipped — not a webapp" and move to Phase 4. Otherwise the same invocation produces the full analysis.

**Prompt:**

```
Review E2E (browser-driven) test coverage for this project.
Scope: [full scope from step 1]

Step 0: Detect whether this is a webapp. If not, exit immediately.

If a webapp:
- Detect existing E2E infrastructure (Playwright, Cypress, Selenium, etc.)
- Survey critical user journeys (Critical / Important / Nice-to-have)
- If no E2E exists (Mode A): prescribe Playwright unconditionally, propose
  infrastructure and ~5 starter tests
- If E2E exists (Mode B): respect the existing framework, identify gaps
  within strategy (cap ~6) and strategy expansion (cap ~2). Do NOT push
  Playwright migration.

Out of scope (declare in output): visual regression, accessibility, performance,
mobile-native UI, component-level testing.

Return findings per the agent's output format, with calibrated confidence and
explicit flag that journey classification is the most subjective input.
```

### 3b. Confirm Journey Classification

Before recording the Phase 3 findings, **confirm the agent's journey classification with the user** — this is the most subjective input in the analysis and shapes the priority assigned to each gap.

**Example confirmation prompt:**

```
## Phase 3: E2E Coverage — confirm journey classification

Webapp detection: DETECTED via React + Vite dependencies

CRITICAL:     Signup → first login; Login; Checkout (cart → payment → confirmation)
IMPORTANT:    Password reset; Profile settings; Order history
NICE-TO-HAVE: Marketing pages; Help center search

Journey classification is the most subjective part of this analysis.
Are these classifications correct? [Yes / Correct: ...]
```

Use `AskUserQuestion`. Allow free-form correction.

If the user corrects any classification, update the agent's findings before recording.

### 3c. Record Phase 3 Findings

Record the gaps (Mode A starter strategy, infrastructure, and starter tests; or Mode B gaps and expansion opportunities) with the confirmed journey priorities. The agent's "out of scope" declarations stay in the recorded report.

## Phase 4: Fuzz Coverage

Identify functions that should have fuzz tests.

### 4a. Analyze Fuzz Gaps

Spawn a single `qa-test-fuzz-reviewer` agent with the full scope.

```
Analyze fuzz testing coverage.
Scope: [full scope from step 1]

Identify:
- Whether fuzz testing infrastructure exists
- Functions that are good fuzz candidates but lack fuzz tests
```

### 4b. Record Phase 4 Findings

**If the agent reports no fuzz infrastructure:** Record "No fuzz testing infrastructure detected for [language]" plus the agent's starter-tooling recommendation, then record its candidates as below: the candidates are the case for adopting the tooling. The tooling recommendation may be cut as a ticket per the runtime ticket-structure proposal (step 8), and candidate tickets depend on it. Do not attempt to set up fuzz tooling.

**If the agent reports no candidates or all candidates are covered:** Record "No fuzz coverage gaps" with the brief explanation.

**Otherwise:** Record candidates grouped by priority (HIGH / MEDIUM / LOW). Record covered candidates separately as informational context.

## Phase 5: Test Quality Audit

Identify quality issues across the existing test suite.

### 5a. Scan for Quality Issues

**Assess scope size** with Glob (count test files in scope).

**Small scope (roughly ≤15 test files):** Spawn a single `qa-test-reviewer` agent.

**Large scope (roughly >15 test files):** Partition by directory or module. Spawn multiple `qa-test-reviewer` agents **in parallel**, each with a focused partition.

Merge findings into a single list. Deduplicate overlaps at partition boundaries.

**Prompt for each agent:**

```
Review the test suite for quality issues.
Scope: [partition or full scope]

Run your full category review and return your standard output format.
Missing coverage is out of scope here (Phases 1-4 own it).
```

**If no issues found:** Record "No test quality issues found" and proceed to the consolidated report.

### 5b. Record Phase 5 Findings

Record findings grouped by category (Tautological / Brittle / False-confidence / Test smells / Inconsistent / Redundant / Other) with the per-finding recommended action (DELETE / REWRITE / SIMPLIFY / informational). The redundant category stays informational.

## 7. Present Consolidated Findings

Compile all phases into a single report:

```
## Test Review Summary

Scope: [what was reviewed]
Baseline coverage: XX% (if measured) — or "manual analysis — not measured"

## Phase 1: Unit Coverage Gaps
- N gaps found: X CRITICAL, Y HIGH, Z LOW
- [Numbered list of gaps with file:line and risk description]

## Phase 2: Integration Coverage
- Mode: [A — none detected / B — exists]
- [Mode A: proposed strategy + infrastructure + starter tests, or
   Mode B: N gaps within strategy, M strategy-expansion opportunities,
   with priorities]

## Phase 3: E2E Coverage
- Webapp: [yes / no — skipped]
- Mode: [A — none detected / B — exists / N/A — skipped]
- Framework: [Playwright / Cypress / other]
- [Mode A: prescribed Playwright + infrastructure + starter tests, or
   Mode B: N gaps within strategy, M strategy-expansion opportunities,
   with confirmed journey priorities]

## Phase 4: Fuzz Coverage
- Infrastructure: [present / absent + tooling recommendation]
- [N candidates with priority and properties to verify]

## Phase 5: Test Quality Audit
- N findings: X to DELETE, Y to REWRITE, W to SIMPLIFY, V redundant (info)
- [Findings by category]

## Refactoring for Testability (informational)
[Refactoring suggestions from Phase 1 coverage analyst, if any. These
suggestions are not implemented by this workflow; work them with
/implement if cut as tickets.]
```

Present to the user. Walk through CRITICAL items and high-impact starter-strategy proposals (Mode A items in Phases 2 and 3) explicitly — these are the highest-leverage findings and the operator should engage with them before the ticket-structure proposal.

## 8. Cut Tickets

After presenting findings, propose a ticket structure based on the review's shape. Each review produces a different finding distribution — high-risk unit gaps with sparse integration coverage, Mode A starter strategies for two phases, a quality audit that is mostly tautological-test removal — and the right ticket granularity depends on that shape. Rather than prescribe a fixed mapping, examine the findings and propose a structure that fits.

### 8a. Analyze Findings and Propose Structure

Examine the consolidated findings produced in step 7:
- Count by phase and priority.
- Note Mode A starter strategies (Phases 2 and 3) — these are typically ticket-shaped as one "set up infrastructure + write starter tests" ticket or split (infrastructure separate from each starter test).
- Note clustering — multiple findings in the same file or component.
- Note REFACTOR-FOR-TESTABILITY suggestions and the fuzz tooling recommendation if present.
- Note redundant tests — informational only, no ticket needed by default.

From that shape, propose a ticket structure. Common shapes:

- **Concentrated unit gaps + small integration/E2E asks:** 1 ticket per CRITICAL unit gap; 1 batch ticket per HIGH/LOW tier; 1 ticket per integration or E2E gap; 1 batch ticket for Phase-5 quality issues.
- **Mode A starter strategies dominate:** 1 ticket per phase's starter strategy (e.g., "Set up integration test infrastructure + write 5 starter tests"); individual tickets for unit/quality findings only if there are few.
- **Lots of Phase-5 churn (many DELETE/REWRITE):** 1 batch ticket per quality category (e.g., "Delete tautological tests," "Rewrite brittle tests in `pkg/api/`").
- **Light review, scattered findings:** 1 batch ticket per phase covering all findings.
- **No actionable findings:** No tickets. The review report stands alone.

Present the proposed structure to the operator with the reasoning:

```
Proposed ticket structure for this review:

Phase 1: 8 gaps (2 CRITICAL, 3 HIGH, 3 LOW)
Phase 2: Mode B — 4 gaps within strategy
Phase 3: Mode A — Playwright not present; 5 starter tests + infrastructure
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

Wait for the response and dispatch per [`references/advisory-tickets.md`](../../references/advisory-tickets.md) § "Three outcomes". Approve → proceed to 8b. Edit → loop until approved (edits may include promoting the refactoring suggestions into a ticket). Decline → the review report stands alone, no tracker writes.

### 8b. Create Tickets

Use the canonical tracker integration documented in [`references/trackers.md`](../../references/trackers.md). For each ticket in the approved structure:

**Title:** `[<PHASE/TYPE>] <concise summary>` (e.g., `[Phase 1 CRITICAL] Add unit tests for auth.ValidateJWT error paths`, `[Phase 3 Mode A] Set up Playwright E2E infrastructure + starter tests`, `[Phase 5] Delete tautological tests in model_test.go and config_test.go`).

**Body sections (per-finding tickets):**
- **Gap** — what is untested or what test is problematic.
- **Files** — `file.go:LINE` for the source code and target test file.
- **Risk / Reason** — why this matters (for ADD) or what makes the test bad (for DELETE/REWRITE).
- **Should verify** — the property a new test should establish, copied from the reviewer's recommendation.
- **Acceptance criteria** — measurable definition of done (e.g., "tests added for invalid-token, expired-token, and signature-mismatch paths in `auth_test.go`; `go test ./auth/...` passes").
- **Recommended implementation skill** — names the next move with scope hint. Examples: `/implement` for a single ticket; for Mode A starter strategies, `/scope` first if the operator wants to refine the strategy before implementing.

**Body sections (batch tickets):**
- A brief intro paragraph stating the batch theme (e.g., "Phase 1 HIGH/LOW unit coverage gaps — group remediation as a single implementation pass").
- One section per included finding using the per-finding structure above.
- A single set of acceptance criteria covering the batch.

**For Mode A starter-strategy tickets (Phases 2 and 3):**
- **Strategy** — the proposed strategy (e.g., "testcontainers-based integration tests; HTTP-level against spun-up app").
- **Infrastructure** — itemized: Makefile target, build tag, fixture compose file, README.
- **Starter tests** — N starter tests with the journey/seam each exercises.
- **Out of scope** — the agent's declared out-of-scope items (especially Phase 3).
- **Acceptance criteria** — infrastructure runs, starter tests pass on first invocation.

**For Phase 5 quality tickets:**
- Preserve the per-test recommendation (DELETE / REWRITE / SIMPLIFY). For DELETE: include the "if the test covers real behavior, rewrite instead of delete" caveat from the reviewer so the implementer doesn't blindly remove tests with hidden value.

**For the fuzz tooling recommendation (if Phase 4 reported absence):**
- Optional ticket: "Adopt fuzz testing infrastructure for [language]" with the agent's tooling recommendation as the body. Cut only if the operator approves it during step 8a. Fuzz-candidate tickets list it as a dependency; if the operator declines it, decline the candidate tickets too.

**Labels:** Apply phase-type labels (`test-coverage`, `integration-test`, `e2e`, `fuzz`, `test-quality`) when the tracker supports them. The implementation may apply a `test` umbrella label if one exists.

After all tickets are created, report the URLs to the operator and exit.

### Orchestrator-Invoked Behavior

See [`references/advisory-tickets.md`](../../references/advisory-tickets.md) § "Orchestrator-invoked behavior" — the proposal is presented identically to operator and orchestrator; the orchestrator's auto-approval contract is documented in [`references/autonomy.md`](../../references/autonomy.md) § "Auto-approval of sub-skill ticket proposals".

## Agent Coordination

One fresh agent (or one per partition, in parallel) per phase, as named above. **No remediation agents:** step 8 cuts tickets; test design and implementation happen in `/implement` against them. Hold scope, coverage baseline, the webapp gate result, the confirmed journey classification, and per-phase findings across phases.

## Abort Conditions

**Abort workflow:**
- User interrupts
- No source files found in scope

**Do NOT abort for:**
- Coverage command failure (fall back to manual analysis)
- A phase finding nothing, or the webapp gate skipping Phase 3 (record and continue)
- Operator declining tickets at step 8 (the report stands alone)
- Tracker unavailable after approval (surface the error; give the approved ticket set so the operator can create the tickets by hand)

## Integration with Other Skills

**`/review-test` vs `/test-mutation`:** Complementary. `/review-test` builds breadth (surfaces gap and quality tickets); `/test-mutation` builds depth (verifies that existing tests actually catch bugs). Recommended sequence: `/review-test` → work the cut tickets via `/implement` → `/test-mutation` to strengthen.

**`/review-test` and `/refactor`:** `/refactor` pins behavior with a differential oracle rather than the test suite, and retires tests that pin the internals it removes; it ports behavior-level tests. Run `/review-test` after a `/refactor` run to see what the reduced codebase's suite covers.
