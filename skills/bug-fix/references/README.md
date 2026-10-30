# /bug-fix - Automated Bug-Fixing Workflow

## Overview

The `/bug-fix` skill orchestrates a diagnosis-first bug-fixing workflow through specialist agents. It reproduces the bug with a failing test, performs root-cause analysis with git archaeology, implements a targeted fix, and verifies the fix through practical testing — then runs it through review, correctness, and documentation gates.

**Key benefits:**
- Test-driven reproduction: a failing test defines "done"
- Root-cause analysis prevents surface-level patches
- Git archaeology uncovers when and why the bug was introduced
- Related failure modes are identified and tested, not just the reported bug
- Practical verification confirms the fix actually works
- A full review pipeline: security, refactoring, performance, peer review, and a blocking correctness gate

## When to Use

**Use `/bug-fix` for:**
- Bugs that need investigation before fixing
- Issues where you want a failing test before any code changes
- Bugs that might have related failure modes (same root cause, similar patterns)
- Fixes where you want comprehensive regression testing
- Problems where git history might reveal how the bug was introduced

**Don't use `/bug-fix` for:**
- Obvious typos or trivial one-line fixes (just fix them directly)
- Feature requests disguised as bugs (use `/implement`)
- Exploratory debugging where the symptom is unclear (investigate first, then `/bug-fix`)

**Rule of thumb:** If the bug is worth a failing test and root-cause analysis, use `/bug-fix`. If the fix is obvious, just do it.

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ /bug-fix Workflow                                                │
└─────────────────────────────────────────────────────────────────┘

 ┌──────────────────────────────────────────────┐
 │  1. CLARIFY THE BUG                          │
 │  ────────────────────────────────────────    │
 │  • Symptoms, expected vs actual behavior     │
 │  • Reproduction steps                        │
 │  • When did it start? Recent changes?        │
 │  • Environment specifics                     │
 │  • Loop until bug is clearly understood      │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  2. WRITE FAILING TEST(S)                    │
 │  ────────────────────────────────────────    │
 │  Agent: Language-specific SME                │
 │                                              │
 │  • Write test encoding expected behavior     │
 │  • Verify test actually fails (proves bug)   │
 │  • This is the contract: when it passes,     │
 │    the bug is fixed                          │
 │                                              │
 │  Can't reproduce? ──┬─ Back to step 1        │
 │                     └─ (max 2 attempts)      │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  3. DIAGNOSIS                                │
 │  ────────────────────────────────────────    │
 │  Agent: swe-bug-investigator (read-only)     │
 │                                              │
 │  • Trace execution paths                     │
 │  • Git archaeology (depth at discretion):    │
 │    - Shallow: git log on involved files      │
 │    - Medium: git blame, commit context       │
 │    - Deep: git log -S, pattern search        │
 │  • Identify root cause + evidence            │
 │  • Identify related failure modes            │
 │  • Recommend fix approach                    │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  4. IMPLEMENT THE FIX                        │
 │  ────────────────────────────────────────    │
 │  Agent: Same SME as step 2                   │
 │                                              │
 │  • Follow diagnostician's recommended fix    │
 │  • Write tests for related failure modes     │
 │  • Verify: originally-failing test passes    │
 │  • Run full test suite for regressions       │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  5. QA - VERIFY FIX                          │
 │  ────────────────────────────────────────    │
 │  Agent: qa-engineer (Mode 1)                 │
 │                                              │
 │  CRITICAL GATE:                              │
 │  1. Practical verification (reproduce the    │
 │     original scenario, confirm it's fixed)   │
 │  2. Run full test suite                      │
 │  3. Check related failure modes              │
 │                                              │
 │  Passes? ──┬─ Yes → Continue                 │
 │            └─ No  → Back to step 4 ──┐       │
 │                     (max 3 attempts) │       │
 └──────────────────┬───────────────────┘       │
                    ▼                           │
 ┌──────────────────────────────────────────────┤
 │  6. CODE REVIEW (conditional reviewers)      │
 │  ────────────────────────────────────────    │
 │  Only review working code!                   │
 │                                              │
 │  6a. Security (if sensitive code)            │
 │      Agent: sec-blue-teamer                  │
 │      Authority: Can demand changes           │
 │                                              │
 │  6b. Refactoring (if non-trivial)            │
 │      Agent: swe-code-reviewer                │
 │      Authority: Advisory suggestions         │
 │                                              │
 │  6c. Performance (if critical code)          │
 │      Agent: swe-perf-reviewer                │
 │      Authority: Advisory suggestions         │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  7. IMPLEMENT REVIEW FEEDBACK                │
 │  ────────────────────────────────────────    │
 │  Agent: Same SME as steps 2/4                │
 │                                              │
 │  • Aggregate all review feedback             │
 │  • Security: Must address or get approval    │
 │  • Other: Advisory - use discretion          │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  8. SME PEER REVIEW (conditional)            │
 │  ────────────────────────────────────────    │
 │  Agent: Fresh instance of same SME           │
 │                                              │
 │  Non-trivial changes?                        │
 │  ├─ Yes → Fresh SME reviews, makes nit fixes │
 │  └─ No  → Skip to QA                         │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  9. QA - COVERAGE & QUALITY                  │
 │  ────────────────────────────────────────    │
 │  Agent: qa-engineer (Mode 2)                 │
 │                                              │
 │  • Test coverage analysis                    │
 │  • Fill coverage gaps                        │
 │  • Run linters/formatters                    │
 │  • Verify steps 7-8 didn't break tests       │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  10. CORRECTNESS REVIEW (run-unless)         │
 │  ────────────────────────────────────────    │
 │  Agent: swe-correctness-reviewer (fresh)     │
 │                                              │
 │  "The bug has already shipped. Find it."     │
 │  • Gets diff + bug report; NOT diagnosis     │
 │  • Findings are blocking, not advisory       │
 │  • Mandatory if empirical gates degraded     │
 │                                              │
 │  Findings? ──┬─ Yes → fix → fresh review     │
 │              │      (max 3 rounds)           │
 │              └─ No → APPROVE, continue       │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  11. DOCUMENTATION                           │
 │  ────────────────────────────────────────    │
 │  Agent: doc-maintainer                       │
 │                                              │
 │  • Update affected documentation             │
 │  • Verify code examples                      │
 │  • Check for broken links                    │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  12. FINAL VERIFICATION                      │
 │  ────────────────────────────────────────    │
 │  • Run full test suite                       │
 │  • Run all linters                           │
 │  • Present summary: root cause, fix, tests   │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  13. WORKFLOW COMPLETION (optional)          │
 │  ────────────────────────────────────────    │
 │  • Commit with root-cause in message         │
 │  • Update/close ticket (if applicable)       │
 │  • Rebase on main (if applicable)            │
 └──────────────────────────────────────────────┘
```

## How /bug-fix Differs from /implement

`/implement` builds from requirements; `/bug-fix` starts from a symptom and spends steps 2-4 on reproduction and diagnosis before any fix. Both end with the same kinds of gates: practical verification, a fresh blocking correctness review, and a documentation pass.

Key differences:
- **Test first, then fix.** `/implement` implements then tests. `/bug-fix` writes a failing test before any fix attempt.
- **Diagnosis before implementation.** The diagnostician performs root-cause analysis so the SME implements a targeted fix, not a guess.
- **Git archaeology.** The diagnostician traces when and how the bug was introduced, providing context the SME wouldn't otherwise have.
- **Related failure modes.** The diagnostician identifies patterns, and the SME writes tests for all of them — not just the reported bug.

## Workflow Details

### 1. Clarify the Bug
The workflow starts by ensuring the bug is clearly understood:
- Symptoms (error messages, crashes, unexpected behavior)
- Expected vs actual behavior
- Reproduction steps
- When it started, any recent changes
- Environment specifics

Loops until there's enough information to write a reproducing test.

### 2. Write Failing Test(s)
A language-specific SME writes test(s) that encode the expected behavior:
- Tests fail against the current buggy code (proving the bug is real and reproducible)
- This is the "contract" — when these tests pass, the bug is fixed
- If the bug can't be reproduced after 2 attempts, escalates to user

**Specialists available:**
- `swe-sme-golang` - Go projects
- `swe-sme-graphql` - GraphQL schemas/resolvers
- `swe-sme-docker` - Dockerfiles and containers
- `swe-sme-makefile` - Makefiles and build systems
- `swe-sme-ansible` - Ansible playbooks and roles
- `swe-sme-zig` - Zig projects
- `swe-sme-html` - HTML/markup
- `swe-sme-css` - CSS/styling
- `swe-sme-javascript` - Vanilla JavaScript
- `swe-sme-typescript` - TypeScript

### 3. Diagnosis
The `swe-bug-investigator` agent performs read-only root-cause analysis:
- **Traces execution paths** from the failing test through the code
- **Git archaeology** at its own discretion:
  - Shallow: `git log` on involved files for recent changes
  - Medium: `git blame` on suspicious code, commit context
  - Deep: `git log -S` for pattern search, similar bugs elsewhere
- **Identifies root cause** with supporting evidence
- **Identifies related failure modes** (same root cause affecting other paths)
- **Recommends fix approach** (what to change and why, not specific code)

The diagnostician does not modify any code. It produces a diagnosis report that guides the implementation agent.

### 4. Implement the Fix
The same SME from step 2 implements the fix:
- Follows the diagnostician's recommended approach
- Fixes the bug as narrowly and precisely as possible
- Writes additional tests for each related failure mode
- Verifies the originally-failing test now passes
- Runs the full test suite for regressions

### 5. QA - Verify Fix (CRITICAL GATE)
The `qa-engineer` performs practical verification:
- Actually reproduces the originally-reported scenario and confirms it's fixed
- Runs the full test suite
- Checks related failure modes identified by the diagnostician

If verification fails, returns to step 4 (max 3 attempts before escalating).

### 6-13. Reviews, Correctness Gate, Documentation, Completion

- **6-7. Conditional reviews and feedback.** `sec-blue-teamer` (security-sensitive changes; Critical/High findings must be addressed or explicitly waived), `swe-code-reviewer` (non-trivial changes; advisory), and `swe-perf-reviewer` (performance-critical changes; advisory). The implementing SME addresses the feedback.
- **8. SME peer review.** A fresh instance of the same SME makes small fixes on non-trivial changes; reverted if it breaks tests.
- **9. QA coverage and quality.** `qa-engineer` fills coverage gaps, runs linters, and confirms steps 7-8 broke nothing.
- **10. Correctness review** (below).
- **11-13. Documentation, final verification, completion.** `doc-maintainer` runs a targeted pass; the full suite and linters run; with your confirmation the skill commits, updates or closes the ticket, and offers a rebase.

One step deserves bug-fix-specific mention — **step 10, the correctness review**. A fresh `swe-correctness-reviewer` reads the diff assuming a bug already shipped and mechanically verifies every assumption the fix makes (paths, signatures, runtime-version semantics, call sites). Its findings are blocking and resolve through a fix-and-fresh-re-review loop (max 3 rounds). Two contracts differ from the rest of the pipeline:

- **The reviewer gets the diff and the original bug report, but not the diagnosis.** The bug report is the user's symptom — ground truth. The diagnosis is the implementing SME's adopted theory; passing it would anchor the reviewer to the frame that produced the fix. The reviewer isn't re-answering "is the bug fixed" (the reproducing test answers that); it's answering "does this fix rest on false assumptions or break anything else."
- **The gate is mandatory when empirical verification degrades.** In a repo with no test infrastructure, the step-2 reproduction contract itself collapses — there may be no failing test at all — and this gate becomes the only correctness check between the fix and production.

## Examples

### Example 1: Off-by-One in Pagination
```
User: "The last item on each page is duplicated on the next page"

Workflow:
1. Clarify: Which endpoint? Happens with all page sizes? Started after recent changes?
2. Failing test: swe-sme-golang writes TestPaginationBoundary that asserts
   no duplicates — test fails against current code
3. Diagnosis: swe-bug-investigator traces pagination logic, finds boundary
   comparison uses < instead of <=, git blame shows it was introduced
   in commit abc123 during a refactor. Also identifies: same pattern
   exists in the cursor-based pagination path.
4. Fix: swe-sme-golang fixes both comparison operators, adds tests for
   cursor pagination boundary too
5. QA: qa-engineer actually paginates through test data, confirms no dupes
6-9. Reviews and coverage QA
10. Correctness: reviewer checks all call sites of both pagination paths,
    verifies boundary semantics — APPROVE
11-13. Docs, verification, commit

Summary:
- Root cause: < vs <= in boundary check, introduced in refactor abc123
- Fixed: 2 files, both offset and cursor pagination
- Tests added: 4 (original bug + 3 related failure modes)
```

### Example 2: Race Condition in Cache
```
User: "Intermittent 500 errors under load, started after adding caching"

Workflow:
1. Clarify: Which endpoint? Error logs? Frequency? Load characteristics?
2. Failing test: swe-sme-golang writes TestConcurrentCacheAccess using
   goroutines — test fails with data race detector
3. Diagnosis: swe-bug-investigator finds unsynchronized map access in cache,
   git log shows cache was added without mutex protection. Related: the
   cache eviction path has the same issue.
4. Fix: Adds sync.RWMutex to cache, protects both read/write and eviction paths
5. QA: Runs concurrent test, race detector clean

Summary:
- Root cause: Unsynchronized map access in cache layer
- Fixed: 1 file (cache.go), added RWMutex protection
- Tests added: 3 (concurrent read/write, concurrent eviction, mixed load)
```

### Example 3: Can't Reproduce
```
User: "App crashes on startup"

Workflow:
1. Clarify: Error message? OS? Configuration file? Recent updates?
2. Failing test: swe-sme-golang tries to reproduce — test passes (no crash).
   Reports: tested with default config, various invalid configs, missing
   config file. Cannot reproduce.
   → Back to step 1.
   User provides: "Only happens with YAML config, not TOML"
2. (retry): swe-sme-golang writes TestYAMLConfigParsing — fails! Bug reproduced.
3-13. Continue with diagnosis and fix...
```

## Tips

1. **Provide reproduction details.** The more specific your reproduction steps, the faster step 2 goes. Vague reports lead to reproduction failures.

2. **Trust the diagnostician's depth.** It chooses shallow or deep git archaeology based on the bug's complexity. Don't worry about it spending too much time on simple bugs.

3. **The failing test is the contract.** Once the SME writes a failing test, that test defines "fixed." This is more reliable than manual verification alone.

4. **Related failure modes are valuable.** The diagnostician looks for patterns, not just the single reported bug. This often catches adjacent bugs that would have been reported next.

5. **Use `/implement` for feature-shaped bugs.** If the "bug" is really a missing feature or a design change, `/implement` is a better fit. `/bug-fix` is for when existing behavior is wrong.

## Agent Coordination

**Sequential execution:** One agent at a time, each completes before the next starts.

**SME continuity:** The same SME type is used across steps 2 (failing test), 4 (fix), and 7 (review feedback). Step 8 (peer review) uses a fresh instance for independent perspective.

**Diagnosis pass-through:** The diagnostician's report from step 3 is passed to the SME in step 4. The SME follows the recommended approach and writes tests for each identified related failure mode. The report is deliberately **not** passed to the correctness reviewer in step 10 — see above.

## Iteration Limits

**Safety limits:**
- Reproduction loop (step 2): 2 attempts max
- Fix verification loop (step 5): 3 attempts max
- Correctness review convergence loop (step 10): 3 rounds max
- Overall workflow: 16 agent spawns max

If limits reached, workflow escalates to user with current state and specific blockers.
