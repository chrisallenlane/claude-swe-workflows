# /bug-hunt - Find Bugs Before Users Do

## Overview

`/bug-hunt` hunts for bugs nobody knows about yet. An assessor works out where bugs are likely to hide by cross-referencing complexity, coverage gaps, structural risk, and git history. Focused hunters then probe each hotspot and write a reproducing test for every suspected bug. You state your intent once; the skill hunts round after round until a round confirms nothing above your severity floor. If you give it the authority, it also tickets what it finds and fixes it via `/implement` between rounds — the work `/lead-bug-hunt` used to do.

Four ideas shape it:

- **Evidence, not opinion.** Every confirmed bug has a reproducing test that encodes the correct behavior and fails against the current code. That test is the finding's proof, the ticket's acceptance criterion, and the fix's verification. A finding without a failing test is reported as a suspicion, labeled as one.
- **Finding and fixing stay separate.** Hunters never fix. With fix authority, confirmed findings go to `/implement`, which fixes them in a fresh context under its own floor: concept inventory, practical verification, independent correctness review.
- **Converge on a floor, not on zero.** A hunt always finds *something* at Low. Findings at or above your floor block convergence; findings below it are reported and left alone.
- **No rationalizing bugs away.** A finding with a failing reproducing test is real. The skill may contest one only on substance — the test asserts the wrong behavior, or the "bug" is documented intended behavior — and a contested finding comes to you.

### Commander's intent

Asked once, up front, then read back for confirmation:

| Field          | Question                                                                 | Default if unanswered                                                     |
|----------------|--------------------------------------------------------------------------|---------------------------------------------------------------------------|
| Scope          | What should the hunt cover? Areas you're worried about? Anything to skip? | Production code; tests, dev tooling, generated and vendored code excluded |
| Severity floor | Below what severity should findings be reported but not acted on?        | High (Critical and High block convergence)                                |
| Constraints    | Anything that must not change — public APIs, compatibility, files?       | No breaking changes; nothing else                                         |
| Tickets        | May I create tickets for confirmed bugs without asking again?            | No — a ticket set is proposed at the end for approval                     |
| Fix            | May I fix confirmed bugs (on a branch, via `/implement`) and re-hunt?    | No                                                                        |

The defaults make `/bug-hunt` an advisory audit: it changes nothing outside its report unless you say it may. Granting ticket authority up front *is* your approval to create them.

## When to Use

**Use `/bug-hunt` for:**
- Hunting bugs proactively before a release, after a burst of development, or in a module you don't trust
- Auditing unfamiliar or inherited code for latent bugs
- Driving a codebase to "no bugs above High" without supervising each round (give it fix authority)
- Getting reproducing tests for whatever it finds, so fixes are verifiable

**Don't use `/bug-hunt` for:**
- A bug you already know about — use `/bug-fix`, which diagnoses first
- Security exploitability — use `/review-security`, which asks whether an attacker can exploit the code; `/bug-hunt` asks whether it fails under ordinary use
- Test-suite quality or coverage strategy — use `/review-test`

## Workflow Diagram

```
┌────────────────────────────────────────────────────────────────┐
│  1. COMMANDER'S INTENT                                         │
│     scope · severity floor · constraints · tickets? · fix?     │
│     read back and confirmed; branch + state doc if fixing      │
└────────────────────────────────┬───────────────────────────────┘
                                 ▼
┌────────────────────────────────────────────────────────────────┐
│  2. HUNT (one round)                                           │
│     assess  → swe-bug-assessor ranks hotspots                  │
│     hunt    → swe-bug-hunter per hotspot, sequentially,        │
│               each given prior findings                        │
│     triage  → verify fails at HEAD · classify vs floor ·       │
│               screen contests + breaking changes · patterns    │
└────────────────────────────────┬───────────────────────────────┘
                                 ▼
┌────────────────────────────────────────────────────────────────┐
│  3. ACT (by authority)                                         │
│     fix?     → /implement fixes at-or-above-floor findings;    │
│                reproducing tests go green                      │
│     tickets? → one per Critical/High bug, per pattern,         │
│                batched below                                   │
│     unfixed reproducing tests → committed as expected failures │
└────────────────────────────────┬───────────────────────────────┘
                                 ▼
                ┌─────────────────────────────────┐
                │ Round confirmed anything above  │── yes ──┐
                │ the floor? (cap: 10 rounds)     │         │
                └────────────────┬────────────────┘         │
                                 │ no                       ▼
                                 │          next round: code the fixes
                                 │          changed, siblings of confirmed
                                 │          patterns, next hotspot tier
                                 │          (back to 2)
                                 ▼
┌────────────────────────────────────────────────────────────────┐
│  4. REPORT                                                     │
│     findings by severity · status (fixed / ticketed / deferred)│
│     no ticket authority → propose ticket set for approval      │
│     no fix authority    → offer to hand bugs to /implement     │
└────────────────────────────────────────────────────────────────┘
```

## What Each Authority Combination Produces

| Tickets | Fix | Result                                                                                                                                      |
|---------|-----|---------------------------------------------------------------------------------------------------------------------------------------------|
| no      | no  | Advisory audit: report plus reproducing tests; a ticket structure proposed at the end, created only on approval; offer to commit the tests |
| yes     | no  | Bugs ticketed autonomously; reproducing tests committed as expected failures referencing their tickets                                     |
| no      | yes | Bugs fixed via `/implement` on a branch; commits and the report are the record; tickets only for deferred items, if you approve them       |
| yes     | yes | Both: fixes for findings at or above the floor, tickets for the rest                                                                        |

## Workflow Details

### 1. Commander's intent

The skill asks the five questions above and reads the intent back. Your concerns steer where it looks first; they don't replace the systematic assessment.

With fix authority, it works on a branch — never main/master. If you're on main, it creates `bug-hunt/<date>`. It keeps `BUG_HUNT_STATE.md` (gitignored) with the pinned intent and a per-round log, so a long run survives context compaction and can resume.

### 2. Hunt

Each round has three steps.

**Assess.** A fresh `swe-bug-assessor` maps the code, measures coverage (instrumented where available), finds complexity and structural risk — error-handling gaps, input validation, shared mutable state, resource handling, concurrency, edge cases, consistency — and enriches it with git churn. It ranks hotspots by *converging* signals: complex and untested and structurally risky outranks any single signal. After round 1, it is told what earlier rounds found and changed.

**Hunt.** A fresh `swe-bug-hunter` probes each hotspot, one at a time, each receiving the confirmed bugs and patterns found so far. A broken error-handling utility found in one module becomes a lead for every module that uses it. Hunters write tests that assert at the boundary a caller sees — return values, errors, output, persisted state — not internals, because the test becomes the fix's acceptance criterion:

| Test result | Meaning                 | What happens to the test                                         |
|-------------|-------------------------|------------------------------------------------------------------|
| Fails       | Bug confirmed           | Kept; the finding is documented                                  |
| Passes      | Hypothesis invalidated  | Kept only if it covers a previously untested path; else deleted |

**Triage.** Each confirmed finding is:

1. **Verified** to fail against current HEAD — otherwise it isn't confirmed.
2. **Classified** against the floor — at or above is acted on this round; below is deferred and reported.
3. **Screened for contests** — a finding that looks wrong on substance goes to you, with the reasoning. It is never dropped silently.
4. **Screened for breaking changes** — a fix needing a breaking change, or violating a constraint, goes to you rather than to `/implement`.
5. **Checked for patterns** — bugs sharing a root cause, or a buggy utility used beyond the hotspot that exposed it, become systemic patterns and leads for the next round.

### 3. Act and iterate

**Fix authority.** The round's at-or-above-floor findings go to `/implement` under its "Invoked by Another Skill" contract: the findings (or their tickets) are the work, each reproducing test is the acceptance criterion, your constraints are its constraints. `/implement`'s floor applies unchanged, and its escalations come back to `/bug-hunt`. When it finishes, the reproducing tests pass.

**Ticket authority.** Tickets are created per the plugin's tracker conventions: one per bug at or above the floor that the run does not fix, and one per systemic pattern. Findings below the floor stay in the report; ticket authority does not extend to them. Each carries the bug, impact, root cause, fix guidance, and the reproducing test as acceptance criterion.

**Unfixed bugs keep the suite green.** Their reproducing tests are committed marked as expected failures with the project's mechanism (`t.Skip`, `pytest.mark.xfail`, `it.skip`, …), referencing the ticket or finding. The fix is done when the marker comes off and the test passes. Coverage-improving tests are committed as ordinary tests.

**Next round.** The hunt goes where new bugs are likely: code the fixes changed, siblings of confirmed patterns, and the next tier of hotspots. Without fix authority, rounds still continue through siblings and the next tier — they just don't re-hunt fixes.

**Convergence.** The run stops when a round confirms nothing above the floor, or after 10 rounds, reporting what remains. When the run has written many tests, the skill may run a `/review-test` pass over them.

### 4. Report

```
## Bug Hunt Complete

Intent: [scope; floor; constraints; tickets yes/no; fix yes/no]
Rounds: N — converged | cap reached
Confirmed: N (X critical, Y high, Z medium, W low) — F fixed, T ticketed, D deferred

## Look at these first
[Contested findings, breaking-change findings, anything the run is least sure of]

## Confirmed bugs (by severity)
- **file:line — description** — impact; root cause; reproducing test
  (file:name); status: fixed at <sha> | ticket #N | deferred (below floor)

## Systemic patterns
## Coverage improvements
## Suspected but unconfirmed
## Not investigated
## Branch (if fixing)
```

The skill walks you through Critical findings first: the bug, its impact, and the reproducing test. Without ticket authority, it ends by proposing a ticket structure shaped by the hunt and creates it only on your approval. Without fix authority, it offers to hand the confirmed bugs to `/implement`.

### 5. Escalation

When you're present, the skill just asks. When running on authority, it stops and hands off — what was found, what was tried, two or three named options, and a recommendation — when:

- A finding is **contested** on substance
- A fix would need a **breaking change** or violate a constraint
- `/implement` escalates and the cause can't be resolved here
- A bug fixed in one round is confirmed again in a later round
- A merge conflicts, or the suite breaks for reasons that aren't local
- On resume, HEAD no longer matches `BUG_HUNT_STATE.md`

It never pushes, merges to main/master, releases, or closes tickets.

## Examples

### Example 1: Advisory audit (default authority)

```
User: /bug-hunt — the billing module worries me.

Intent read back: scope src/billing/ (tests, generated code excluded);
floor High; no breaking changes; tickets no; fix no. Confirmed.

Round 1: assessor ranks 6 hotspots. Hunters confirm 3 bugs:
  [HIGH]   ConvertAmount truncates zero-decimal currencies (JPY)
  [HIGH]   ProcessCheckout leaves inventory holds on payment failure
  [MEDIUM] Negative amounts accepted by the refund path
Pattern: payment-failure paths skip cleanup — lead for round 2.
Round 2: siblings of the cleanup pattern; 1 more HIGH (subscription renewal).
Round 3: next hotspot tier; nothing above High. Converged.

Report: 3 HIGH, 1 MEDIUM, 2 coverage tests.
Proposed tickets: 3 per-bug (HIGH), 1 systemic pattern, 1 batched (MEDIUM).
You approve; tickets #41–#45 created. Reproducing tests committed with
xfail markers referencing #41–#45. Offer: "Hand these to /implement now?"
```

### Example 2: Tickets yes, fix no

```
Intent: scope whole repo; floor High; tickets yes; fix no.

Round 1: 2 CRITICAL (race in the cache invalidator; unchecked nil in the
  config loader). Tickets #88, #89 created immediately.
  Tests committed as expected failures:
    t.Skip("bug #88: invalidator races with readers")
Round 2: the nil pattern appears in two other loaders → ticket #90.
Round 3: nothing above High. Converged.

Report: 3 tickets, each naming its skipped test; the suite stays green.
Fixing #88 later with /implement: remove the t.Skip, make it pass.
```

### Example 3: Fix yes, tickets no — three rounds

```
Intent: scope src/; floor High; fix yes; tickets no.
Branch bug-hunt/2026-11-02 created; BUG_HUNT_STATE.md seeded.

Round 1: 4 HIGH confirmed. Handed to /implement with each reproducing test
  as acceptance criterion. Fixed; correctness review clean; tests green.
Round 2: re-hunt code the fixes touched + siblings. 1 HIGH — the retry fix
  exposed a double-submit in the queue consumer. /implement fixes it.
Round 3: nothing above High; 2 MEDIUM deferred.

Report: 5 fixed (SHAs listed), 2 MEDIUM deferred. Offer: ticket the 2 deferred
findings? The branch is yours to review and merge.
```

### Example 4: A contested finding

```
Round 1: hunter confirms "ParseDate rejects 2-digit years" — test fails.
Triage: ADR 0007 documents 4-digit-only years as intended behavior.

Escalation:
  Finding: ParseDate rejects "24-03-01" (test: TestParseDate_TwoDigitYear)
  Why contested: adr/0007 specifies 4-digit years only
  Options:
    A. Accept the ADR — delete the test, record as intended behavior
    B. Treat as a bug — the ADR is outdated; fix and amend the ADR
    C. Defer — keep the test as an expected failure, ticket it for discussion
  Recommendation: A, unless callers now send 2-digit years (B if logs show they do)
```

## Tips

1. **Pick the floor deliberately.** Too low and the hunt never converges; too high and real bugs ship. High is a sensible default; Medium for code that handles money or user data.
2. **Name your worries.** Areas you mention get looked at first, without displacing systematic assessment.
3. **Start advisory on unfamiliar code.** A no/no run shows you what's there before you let anything change.
4. **Give fix authority when you want "clean," not "a list."** The run then iterates fix → re-hunt without you, and every fix still passes `/implement`'s correctness gates.
5. **Treat the reproducing tests as the deliverable.** Even unfixed, they document the bugs and keep them from going unnoticed again.
6. **Read the contested findings first.** They're where the run's judgment and your knowledge of intended behavior meet.
