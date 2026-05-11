# /lead-project — Autonomous Technical Lead

## Overview

The `/lead-project` skill drives a project from a stated intent to completion with minimal user involvement. The user provides **commander's intent** at startup (a structured five-field statement) and reviews the result at the end — or earlier, if the skill pulls an andon cord. Between those points, the skill runs an **OODA loop** (Observe → Orient → Decide → Act), invoking other skills in the plugin (`/scope`, `/implement`, `/refactor`, `/review-*`, `/bug-*`, `/think-*`) as it judges appropriate.

The user fills the **product-owner** role; the skill fills the **project-manager / tech-lead** role.

This skill is the highest-level implementation of the **autonomy discipline** documented in [`references/autonomy.md`](../../../references/autonomy.md). Its five-field commander's-intent schema is the **canonical implementation** referenced from that document; its handoff format adopts the shared template (with skill-specific extensions for the OODA cycle and mechanical end-state conditions); and it cascades sub-skill escalations through the orchestrator's judgment before any operator-facing handoff.

**Key benefits:**
- Unattended orchestration of the plugin's lower-level skills
- Commander's intent as a durable anchor that survives context drift
- Explicit mechanical gates on termination (not just LLM self-assessment)
- Periodic trajectory audits that can pull the cord on drift or thrash
- Broad autonomy with narrow irreversible-action gates
- `LEAD_PROJECT_STATE.md` as persistent state across sessions

## When to Use

**Use `/lead-project` for:**
- Multi-phase work where the next step depends on the outcome of the last (implement → review → refactor → re-review → …)
- Projects where you know the desired end state but don't want to orchestrate the path
- Bringing a feature branch to release-readiness while you focus on product decisions and QA
- Any time you'd otherwise run `/scope` → `/implement-project` → `/refactor-deep` → `/review-deep` by hand

**Don't use `/lead-project` for:**
- A single ticket (use `/implement` or `/bug-fix`)
- A single batch of tickets (use `/implement-batch`)
- A fixed multi-batch project with a known backlog and no expected feedback loops (use `/implement-project`)
- Exploratory work where the end state is discoverable rather than declarable (use `/scope-project`, `/think-brainstorm`, or `/review-health`)
- Pre-release comprehensive audit (use `/review-deep`)

**Rule of thumb:** if you find yourself repeatedly running "implement something, review it, fix it, review it again" and making the same obvious transitions by hand, `/lead-project` is the right abstraction.

## Relationship to `/implement-project`

| Dimension                | `/implement-project`                                       | `/lead-project`                                           |
|--------------------------|------------------------------------------------------------|-----------------------------------------------------------|
| Input                    | Pre-batched tickets                                        | Commander's intent (may be any combination of tickets, review goals, refactoring objectives) |
| Shape                    | Once-through pipeline                                      | Open-ended OODA loop                                      |
| Termination              | Pipeline end                                               | End state met + mechanical gates pass + quiescence        |
| Scope changes mid-run    | Out of scope                                               | Skill may invoke `/scope` to draft new tickets            |
| Review cadence           | Fixed quality-pipeline sequence                            | Agent decides when and which reviews to run               |
| Duration                 | Roughly predictable from batch count                       | Open-ended (capped at 50 cycles)                          |

`/lead-project` may invoke `/implement-project` internally when it has a coherent batch of tickets to execute.

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ /lead-project Workflow                                          │
└─────────────────────────────────────────────────────────────────┘

 ┌──────────────────────────────────────────────┐
 │  0. STARTUP                                  │
 │  ────────────────────────────────────────    │
 │  0a. Branch and working-tree check           │
 │  0b. Resume existing run or start fresh      │
 │      - Verify SHA match; andon on divergence │
 │  0c. Elicit commander's intent (interactive) │
 │      - Purpose / Key tasks / End state       │
 │      - Constraints / Non-goals               │
 │      - Classify end-state: mechanical or     │
 │        subjective                            │
 │  0d. Optional /review-health                 │
 │  0e. Seed LEAD_PROJECT_STATE.md              │
 └──────────────────┬───────────────────────────┘
                    ▼
        ┌───────────────────────┐
        │  OODA LOOP            │◄───────────────┐
        └───────────┬───────────┘                │
                    ▼                            │
 ┌──────────────────────────────────────────────┐│
 │  1a. OBSERVE                                 ││
 │      git status, tests, build, lint,         ││
 │      recent commits, findings, last cycle    ││
 ├──────────────────────────────────────────────┤│
 │  1b. ORIENT                                  ││
 │      - Intent alignment against pinned text  ││
 │      - Drift check                           ││
 │      - Termination check (mechanical):       ││
 │        1. Mechanical end-state conds pass    ││
 │        2. No constraint violations           ││
 │        3. Pre-term review re-run clean       ││
 │        4. Quiescence over git diff           ││
 │        5. Subjective conds acknowledged      ││
 │      - Model update if observations surprise ││
 ├──────────────────────────────────────────────┤│
 │  1c. DECIDE                                  ││
 │      Priority: blockers > key tasks >        ││
 │      high-severity > implementation > polish ││
 │      - Reviewer tie-breaker: contradictory   ││
 │        findings → andon cord                 ││
 │      - Review re-invoke only if flagged      ││
 │        files changed                         ││
 │      - /think-* for ambiguous decisions      ││
 ├──────────────────────────────────────────────┤│
 │  1d. ACT                                     ││
 │      Invoke skill, verify, commit, log       ││
 ├──────────────────────────────────────────────┤│
 │  1e. TRAJECTORY AUDIT (every 10 cycles)      ││
 │      Read git log/diff/intent directly       ││
 │      Verdict: Converging / Diverging /       ││
 │      Thrashing                               ││
 │      2x Diverging or any Thrashing → andon   ││
 └──────────────────┬───────────────────────────┘│
                    ▼                            │
         Terminate or continue? ─────────────────┘
                    │ (terminate)
                    ▼
 ┌──────────────────────────────────────────────┐
 │  2. TERMINATION                              │
 │  ────────────────────────────────────────    │
 │  2a. Final verification (mechanical)         │
 │      - Re-run mechanical end-state commands  │
 │      - Tests, build, lint                    │
 │      - Smoke test feature claims             │
 │      - Constraint adherence check            │
 │  2b. Completion report                       │
 │      - Outcome + Top things to scrutinize    │
 │      - End-state verification                │
 │      - Key tasks + Deferred items            │
 │      - Constraints + Recommendations         │
 │      - Run metadata (bottom)                 │
 └──────────────────────────────────────────────┘
```

## Commander's Intent

Borrowed from military doctrine: the commander states **why** (purpose) and **what success looks like** (end state), not the detailed how. Subordinates have autonomy to adapt to circumstances as long as they preserve intent. In `/lead-project` the user is the commander; the skill is the subordinate.

This five-field schema is the **canonical implementation** of commander's intent referenced from [`references/autonomy.md`](../../../references/autonomy.md). Other orchestrator-family skills (`/implement-project`, `/refactor-deep`) use lighter variants tailored to bounded work; `/lead-project`'s purpose is the most open-ended, so it elicits the full schema.

Intent has five fields:

| Field        | What it is                                                               | Example                                                               |
|--------------|--------------------------------------------------------------------------|-----------------------------------------------------------------------|
| Purpose      | One or two sentences on why this iteration exists                        | "Ship v1.0 of the MCP server to external users."                      |
| Key tasks    | Non-negotiable outcomes (2–10 items, written as state)                   | "All tickets in milestone v1.0 are closed; README has usage section." |
| End state    | Concrete observable conditions defining "done" — prefer shell-runnable   | "`go test ./...` exits 0; CHANGELOG has v1.0 entry."                  |
| Constraints  | Hard limits the skill must respect                                       | "Do not modify the public API of package `auth`."                     |
| Non-goals    | Explicit out-of-scope                                                    | "No performance optimization this iteration."                         |

**End-state classification.** At intake, each end-state condition is classified:
- **Mechanical** — a shell command or deterministic check the skill can execute
- **Subjective** — requires human judgment (e.g., "README reads clearly")

Mechanical conditions gate termination automatically. Subjective conditions are surfaced to the user in the completion report for final sign-off.

**Iterative elicitation.** The skill walks through the five fields one at a time and pushes back on vague answers. It does not abort on vagueness — it keeps asking follow-up questions until the intent is crisp enough to anchor the loop. Several rounds of dialogue is normal; invest the time.

## The OODA Loop

Each cycle runs four explicit phases. The structure creates reasoning residue in the state doc even when the LLM collapses them into one turn.

| Phase   | What it does                                                                                                       |
|---------|--------------------------------------------------------------------------------------------------------------------|
| Observe | Snapshot current state: git status, test/build/lint results, recent commits, last cycle's outcome                  |
| Orient  | Compare to pinned intent; check drift; run termination checks (mechanical); update model if observations surprise  |
| Decide  | Choose next skill to invoke per priority order; use `/think-*` for ambiguity                                       |
| Act     | Execute the chosen skill, verify, commit (if applicable), update state doc                                         |

**Priority order in Decide:**

1. **Blockers first.** Broken tests, broken build, failing CI.
2. **Key tasks next.** Unfinished key-task items from intent take priority over polish.
3. **High-severity review findings** before medium or low.
4. **Implementation before cleanup.** Prefer `/implement` over `/refactor`/`/review-*` until the backlog is empty.
5. **Cleanup and reviews** once feature work is done.

## Termination

Termination is a **mechanical gate**, not an LLM self-assessment. The Orient phase can only trigger termination when all of the following hold:

1. Every mechanical end-state condition has been executed this cycle and exited successfully
2. No constraint violations in recent commits or current tree
3. A pre-termination review re-run (at minimum `/review-test` and `/review-release`, plus any reviewers named by end state) produces no new high-severity findings
4. Quiescence over git diff — last two cycles produced no material code changes
5. Subjective end-state conditions are collected for the user's review (not self-declared met)

A final verification pass (2a) re-runs the mechanical checks once more before the completion report is produced.

## Trajectory Audits

Every 10 cycles, the skill performs an internal trajectory audit. This is not user-facing unless it triggers the andon cord.

The audit reads **primary artifacts** (git log, git diff, pinned intent, deferred-items list) rather than the cycle log narrative — which the agent authored and may rationalize against.

Three verdicts:

- **Converging** — recent work traces to intent, key tasks advancing. Continue.
- **Diverging** — recent work predominantly on non-intent items or scope has expanded. Attempt one course-correction cycle. If the next audit also returns Diverging, pull the andon cord.
- **Thrashing** — oscillation detected (same files being rewritten, contradictory review findings, no net progress). Pull the andon cord immediately.

## The Andon Cord

Borrowed from Toyota's production system: when something goes wrong, **stop the line immediately** and pull in the human.

**Before pulling the cord:**
1. Attempt autonomous resolution
2. Try `/think-deliberate` or `/think-reframe` for judgment calls
3. Re-read the commander's intent — is the blocker actually a signal that intent needs clarification?
4. Only pull if autonomous resolution has failed or is clearly futile

**Triggers:**
- Irreversible action required (push to main, release, force-push, global dep install, delete data)
- Blocking decision requires product judgment that `/think-deliberate` can't resolve
- Stuck — same failure 3 or more times despite different strategies
- Drift is severe
- Trajectory audit returns Thrashing, or two consecutive Diverging verdicts
- Reviewers produce contradictory findings on the same file
- Fundamental assumption broken
- Constraint conflict (a key task appears to require violating a stated constraint)
- Resume-time HEAD divergence (branch SHA ≠ recorded state)
- 50-cycle hard cap hit
- Sub-skill andon cord cascades up

**Handoff format** follows the **shared handoff template** in [`references/autonomy.md`](../../../references/autonomy.md). The template requires a project-level orientation paragraph (for the user returning cold), then the blocker-specific story (what was being attempted, what went wrong, what was tried), pre-loaded options (2–3 named choices), a recommendation with its pre-rebutted counterargument and the one tradeoff that would flip it, and a current-state snapshot. `/lead-project` extends current state with mechanical-condition pass count, pending key tasks, and a cycle-log pointer.

## Authority and Gates

**Broad authority.** The skill may:
- Create and modify branches (except main/master)
- Commit freely on the working branch
- Open tickets via `/scope`
- Invoke any skill in the plugin
- Spawn subagents
- Run tests, linters, formatters
- Install local project dependencies declared by the package manifest

**Narrow gates.** The skill may NOT without explicit permission:
- Push or merge to main/master
- Create public releases or tags
- Force-push
- Install global or system dependencies
- Run irreversible destructive operations

## Severity Thresholds

`/review-*` skills produce findings indefinitely at low severity. The skill applies thresholds:

| Severity       | Handling                                                                                                     |
|----------------|--------------------------------------------------------------------------------------------------------------|
| Critical/High  | Must address before termination. Blocks the termination gate.                                                |
| Medium         | Fix if bounded (small, obvious, localized). Otherwise defer with rationale. Does not block termination.     |
| Low/Info       | Defer by default with note. Does not block termination.                                                     |

Every deferral is recorded in the state doc with its rationale so the completion report can present them transparently.

## State Management

`LEAD_PROJECT_STATE.md` is maintained at the repository root (gitignored) throughout a run. Persists across invocations so the skill can resume.

**Contents:**

- Pinned commander's intent (all five fields, verbatim — re-read every cycle)
- Branch + SHA at startup; base branch + SHA; last-cycle HEAD
- Current phase, cycle number, status
- Current orientation (agent's working mental model)
- Drift status
- Triage plan (updated as orientation evolves)
- Cycle log — one entry per cycle with OODA residue and commit SHAs
- Trajectory audit verdicts (cycles 10, 20, 30, 40)
- Review invocation log (to enforce "only re-invoke if flagged files changed")
- Deferred items with rationale
- Open questions the skill resolved autonomously (to surface in completion report)

**On resume**, the skill verifies the recorded branch SHA matches current HEAD. If it doesn't, it pulls the andon cord rather than auto-continuing on stale orientation. Three resume options are offered: resume as-is, resume with updated intent, or start fresh (which archives the existing state doc with a timestamp).

## Hard Caps

- **50 cycles** — if the loop reaches cycle 50 without terminating, pull the andon cord. Something is likely wrong.
- **3 consecutive failed actions** — if the skill attempts the same goal 3 times with different strategies and all fail, pull the andon cord.

These are safety ceilings, not targets.

## Available Sub-Skills

The skill may invoke any of the following during the Decide phase:

| Skill                           | When to use                                                                          |
|---------------------------------|--------------------------------------------------------------------------------------|
| `/scope`                        | Draft new tickets when gaps emerge that serve intent                                 |
| `/implement`                    | Single-ticket implementation                                                         |
| `/implement-batch`              | Batch of related tickets                                                             |
| `/implement-project`            | Multi-batch ticket project                                                           |
| `/refactor`                     | Tactical code cleanup                                                                |
| `/refactor-deep`                | Tactical + architectural + tactical cleanup cycle                                    |
| `/review-arch`                  | Architectural review                                                                 |
| `/review-test`                  | Test suite survey; advisory; produces ticket-structure proposal                      |
| `/tidy-docs`                   | Documentation audit                                                                  |
| `/review-release`               | Pre-release readiness                                                                |
| `/review-perf`                  | Performance review                                                                   |
| `/review-a11y`                  | Accessibility review                                                                 |
| `/review-security`              | Security audit                                                                       |
| `/review-deep`                  | Comprehensive review across all dimensions                                           |
| `/bug-hunt`                     | Proactive bug discovery                                                              |
| `/bug-fix`                      | Diagnosis-first bug fixing                                                           |
| `/test-mutation`                | Mutation testing                                                                     |
| `/think-deliberate`             | Adversarial option selection when options are materially different                   |
| `/think-scrutinize`             | Stress-test a plan before executing it                                               |
| `/think-reframe`                | Reframe a problem when framing seems wrong                                           |
| `/think-diagnose`               | Abductive reasoning about causes when a failure is mysterious                        |
| `/think-brainstorm`             | Divergent idea generation when no obvious next action presents itself                |

`/think-reflect` is intentionally **not** invoked inside the loop — it is calibrated for human consumption. The user may invoke it themselves on the completion report if they want retrospective learning.

## Examples

### Example 1: Driving a feature to release-readiness

```
User: /lead-project

Starting commander's intent elicitation.

Purpose — in one or two sentences, why are we doing this iteration?
> Take the auth module from "prototype that mostly works" to "shipped
  with confidence" for the v2.0 release.

Key tasks — what non-negotiable outcomes must be true?
> - All tickets in milestone v2.0 closed
  - Test coverage for auth/* above 80%
  - CHANGELOG has v2.0 entry
  - No known security issues

End state — concrete conditions that define "done"?
> - `go test ./auth/...` exits 0
  - `go tool cover -func=coverage.out | grep auth/ | awk ...` shows 80%+
  - grep -q 'v2.0' CHANGELOG.md
  - /review-security produces no high-severity findings

Classifying:
  - `go test` — MECHANICAL
  - coverage check — MECHANICAL
  - CHANGELOG grep — MECHANICAL
  - /review-security clean — MECHANICAL (via pre-termination re-run)
All end-state conditions are mechanical. Good.

Constraints?
> - Don't break the public API of pkg/auth
  - Must remain Go 1.22 compatible

Non-goals?
> - No rewrites of pkg/session
  - No performance optimization

Read back:
[five-field intent]

Confirm?
> Yes

Creating branch: lead-project/auth-v2.0
Seeding LEAD_PROJECT_STATE.md

[Cycle 1]
Observe: 6 open tickets in v2.0, tests pass (87/87), coverage auth/ 64%
Orient: Key task 1 (close tickets) not met; implementation phase
Decide: /implement-project on the 6 tickets (batched into 2 batches by scope)
Act: /implement-project (autonomous)... 6 tickets closed, 23 commits, all tests pass

[Cycle 2]
Observe: 0 open tickets, tests pass (104/104), coverage 72%
Orient: Key task 1 met. Key task 2 (80% coverage) not met.
Decide: /review-test to surface coverage gaps
Act: /review-test... 8 gaps surfaced; orchestrator declined proposed
     tickets and implemented 5 critical gaps inline via /implement.
     Coverage now 83%.

[Cycle 3]
Observe: tests pass (111/111), coverage 83%
Orient: Key task 2 met. No CHANGELOG v2.0 entry yet.
Decide: draft CHANGELOG entry directly
Act: CHANGELOG updated, committed

[Cycle 4]
Observe: CHANGELOG has v2.0
Orient: All key tasks met. Running pre-termination review re-run...
        /review-security: 0 high-severity findings
        /review-test: clean
        /review-release: clean
        Quiescence: cycle 2 and 3 both produced commits; continue.

[Cycle 5]
Observe: (no changes since cycle 4)
Orient: Quiescence 2-cycle window satisfied. All mechanical conditions pass.
        Terminating.

[Final verification]
- go test ./auth/... → exit 0 ✓
- Coverage auth/ = 83% ≥ 80% ✓
- grep v2.0 CHANGELOG.md → match ✓
- /review-security re-run → 0 high-severity ✓
- No constraint violations (pkg/auth public API intact)

## Lead-Project Complete

### Commander's intent
[Verbatim ...]

### Outcome
Auth v2.0 is release-ready. All 6 milestone tickets closed, coverage at 83%
(target 80%), CHANGELOG updated, and no high-severity security or release
findings remain.

### Top things to scrutinize
1. Commit 7a3f2b9 — non-trivial refactor to token refresh logic during #15.
   Worth eyeballing. (auth/token.go:120)
2. Deferred: medium-severity /review-test finding about mock usage in
   auth/session_test.go. Fix is 3 files deep; deferred.
3. Deferred: /review-arch suggested extracting a validator module. Out of
   scope for this iteration.

### End-state verification
Mechanical:
- [✓] go test ./auth/... — `go test ./auth/...` exit 0 at SHA a1b2c3d
- [✓] Coverage ≥ 80% — `go tool cover -func=coverage.out | grep ...` → 83% at SHA a1b2c3d
- [✓] CHANGELOG v2.0 — `grep -q 'v2.0' CHANGELOG.md` exit 0 at SHA a1b2c3d
- [✓] Security clean — /review-security produced 0 high-severity at cycle 4

Subjective: (none)

### Key tasks status
- [✓] All v2.0 tickets closed — 6 tickets, see SHAs 2f1a8... through 8d3c9...
- [✓] Auth coverage ≥ 80% — 83% measured at a1b2c3d
- [✓] CHANGELOG has v2.0 — SHA 9e4f2b1
- [✓] No known security issues — /review-security clean at cycle 4

### Deferred items
- [medium | /review-test | cycle 2] Mock overuse in session_test.go —
  approved as ticket (#107) because fix spans 3 files and touches the
  separate /session refactor that's out of scope
- [medium | /review-arch | cycle 2] Extract validator module —
  deferred as out of scope per non-goal "no pkg/session rewrites"

### Constraint/non-goal adherence
pkg/auth public API intact (verified: git diff on auth/*.go shows no
signature changes on exported symbols). pkg/session not modified.
Go 1.22 compatibility not exercised (no version-specific code introduced).

### Recommendations
Ready to merge to main. The two deferred items are appropriate follow-ups
for a separate iteration.

### Changes summary
- Branch: lead-project/auth-v2.0 (SHA a1b2c3d)
- Base: main (SHA 4f5e6d7)
- Commits on branch: 32
- Net lines: +847 / -209
- Tickets closed: 6 (#101, #102, #103, #104, #105, #106)

### Run metadata
- Cycles: 5 of 50
- Actions: 1x /implement-project, 1x /review-test, 1x direct edit,
  1x pre-termination review re-run
- Trajectory audits: none triggered (run was under 10 cycles)
- Duration: ~1h40m wall-clock
```

### Example 2: Andon cord on trajectory drift

```
[Cycle 20 — Trajectory audit]

Reading git log and diff against branch start...

Findings:
- Commits 1-8 traced to key task 1 (implement feature). Converging.
- Commits 9-14 traced to key task 2 (docs). Converging.
- Commits 15-20: 4 of 6 touched src/logging/* — not named in any key task.
  2 of 6 were refactoring within auth/, still in scope.
- Deferred list grew from 2 items (cycle 10) to 7 items (cycle 20).

Verdict: DIVERGING — recent work has drifted into src/logging, which is not
in the pinned intent's key tasks or end state, and the deferred list is
growing faster than completion.

Attempting one course-correction cycle (next Decide will prioritize
remaining key task over further polish).

[Cycle 21 — Observe / Orient / Decide]
Decide: key task 3 (CHANGELOG v2.0) is unstarted. Direct edit.
Act: CHANGELOG updated, committed.

[Cycle 30 — Trajectory audit]
Recent 10 cycles traced to intent. Converging. Continue.
```

### Example 3: Resume after an external commit

```
User: /lead-project

Found LEAD_PROJECT_STATE.md. Verifying state...

Recorded Last cycle HEAD: 4a8b2c1
Current HEAD:             9f3e4d5

⚠ ANDON CORD — HEAD has moved since last cycle

### Project orientation (30-second reorient)
This run was driving the auth module to v2.0 readiness. Cycles 1-14 closed
four of six milestone tickets. Coverage reached 76%. Cycles 15-20 deferred
to work on the /logging reorganization (trajectory audit flagged and
course-corrected at cycle 21). At cycle 21, CHANGELOG was updated. The
loop was about to begin the pre-termination review sequence.

### What went wrong
The recorded branch HEAD (4a8b2c1) does not match the current HEAD
(9f3e4d5). Between runs, 3 commits landed on this branch from outside
this skill. Continuing on the stale orientation would cause the skill
to act on code state it has not observed.

### What I need from you
One of:
  1. Run Observe + Orient fresh against current HEAD, then continue.
  2. Resume with updated intent (re-elicit the five fields, preserving cycle log).
  3. Start a new run (archives existing state doc).
  4. Hard-reset the branch to 4a8b2c1 and resume exactly as before
     (WARNING: destroys the 3 external commits — confirm carefully).

Awaiting your guidance.
```

## Tips

1. **Invest in intent elicitation.** It's the only time you're deeply involved. The crisper the intent, the less likely drift and false termination. Don't accept "figure out what needs fixing" — push yourself to state what "fixed" would look like.

2. **Prefer shell-runnable end states.** "`go test ./... && make lint` both exit 0" gates termination mechanically. "Works well" doesn't. The skill accepts subjective conditions but cannot self-verify them, so they turn into user sign-off at the end rather than automatic termination.

3. **Use constraints liberally.** They're cheap to add and prevent scope drift. "Don't touch the frontend" is a one-line constraint that can save many cycles.

4. **Trust the andon cord.** If the skill pulls it, something is genuinely ambiguous. Read the handoff's project-orientation paragraph, answer the specific question, and resume. Don't override and force the skill to continue on a decision you haven't made.

5. **Read the "Top things to scrutinize" section of the completion report first.** That's the forced triage. If everything there looks fine, the rest is usually fine too.

6. **The working branch is your safety net.** The skill never touches main. If a run goes poorly, `git reset --hard` the working branch and start over. Cost is wasted tokens.

7. **Resume with updated intent is the right option after a refinement.** If the completion report surfaces a deferred item you want addressed, don't start fresh — resume with an updated intent that adds the item as a key task.

## Integration with Other Skills

| Skill                | Relationship                                                                                              |
|----------------------|-----------------------------------------------------------------------------------------------------------|
| `/scope`             | Run before `/lead-project` to establish tickets, or invoked by `/lead-project` when it identifies gaps     |
| `/scope-project`     | Run by the user before `/lead-project` to establish initial backlog                                       |
| `/implement-project` | Invoked by `/lead-project` when a coherent batch of tickets is ready                                      |
| `/implement-batch`   | Invoked by `/lead-project` for smaller batches                                                            |
| `/implement`         | Invoked by `/lead-project` for individual tickets                                                         |
| `/refactor`, `/refactor-deep`           | Invoked by `/lead-project` during cleanup phases                                    |
| `/review-*`          | Invoked by `/lead-project` for targeted reviews; pre-termination re-run uses `/review-test` and `/review-release` at minimum |
| `/review-deep`       | May be invoked near the end of a run as a comprehensive validation                                        |
| `/bug-hunt`, `/bug-fix` | Invoked when bugs are suspected or known                                                              |
| `/test-mutation`     | Invoked to validate test suite effectiveness                                                              |
| `/think-*` (except `/think-reflect`) | Invoked in Orient or Decide for ambiguous or high-stakes decisions                        |
| `/think-reflect`     | NOT invoked inside the loop. User may invoke after the completion report for retrospective learning       |

**Hierarchy:**

```
/lead-project
├── (startup)
│   └── /review-health (optional)
├── (per cycle, any of:)
│   ├── /scope
│   ├── /implement | /implement-batch | /implement-project
│   ├── /refactor | /refactor-deep
│   ├── /review-arch | /review-test | /tidy-docs | /review-release
│   │   /review-perf | /review-a11y | /review-security | /review-deep
│   ├── /bug-hunt | /bug-fix
│   ├── /test-mutation
│   └── /think-reframe | /think-diagnose | /think-deliberate
│       /think-scrutinize | /think-brainstorm
├── (pre-termination)
│   └── /review-test + /review-release (+ others per end state)
└── (termination)
    └── Completion report
```

## Agent Coordination

**Sequential execution.** One cycle at a time, one skill invocation per cycle. No parallel cycles.

**Context discipline.** The skill is a thin coordinator. It delegates all implementation to sub-skills. It maintains only summary-level state in its context; `LEAD_PROJECT_STATE.md` holds durable memory that the skill re-reads each cycle (pinned intent verbatim, recent cycle log entries, deferred items, trajectory audit history).

**Sub-skill invocation.** The skill invokes sub-skills via the Skill tool, using autonomous overrides where sub-skills support them. When a sub-skill requires interactive input, the skill answers using engineering judgment anchored to the pinned commander's intent.

## Abort Conditions

**Do NOT abort for:**
- Individual cycle failures (try a different approach in the next cycle)
- Sub-skill findings that look overzealous (apply severity threshold, defer)
- Drift that can be course-corrected autonomously

**Pull the andon cord for:**
- All the triggers listed above under "The Andon Cord"

**Abort the entire workflow only for:**
- User interrupts
- Critical system error (repository corrupted, git state unrecoverable)
- User declines to confirm commander's intent at startup
