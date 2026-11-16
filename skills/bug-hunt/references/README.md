# /bug-hunt - Find Bugs Before Users Do

The step-by-step procedure lives in [`SKILL.md`](../SKILL.md); this guide covers when to use the skill and what to expect.

## Overview

`/bug-hunt` hunts for bugs nobody knows about yet. An assessor works out where bugs are likely to hide by cross-referencing change history (complexity × churn hotspots, fix density, change coupling), coverage gaps, and structural risk. Focused hunters then probe each hotspot and write a reproducing test for every suspected bug. You state your intent once; the skill hunts round after round until a round confirms nothing at or above your severity floor. If you give it the authority, it also tickets what it finds and fixes it via `/implement` between rounds.

Four ideas shape it:

- **Evidence, not opinion.** Every confirmed bug has a reproducing test that encodes the correct behavior and fails against the current code. That test is the finding's proof, the ticket's acceptance criterion, and the fix's verification. A finding without a failing test is reported as a suspicion, labeled as one.
- **Finding and fixing stay separate.** Hunters never fix — the pressure to find bugs should not bend toward bugs that are easy to fix. With fix authority, confirmed findings go to `/implement`, which fixes them in a fresh context under its own floor: concept inventory, practical verification, independent correctness review.
- **Converge on a floor, not on zero.** A hunt always finds *something* at Low. Findings at or above your floor block convergence; findings below it are reported and left alone.
- **No rationalizing bugs away.** A finding with a failing reproducing test is real. The skill may contest one only on substance — the test asserts the wrong behavior, or the "bug" is documented intended behavior — and a contested finding comes to you.

## When to Use

**Use `/bug-hunt` for:**
- Hunting bugs proactively before a release, after a burst of development, or in a module you don't trust
- Auditing unfamiliar or inherited code for latent bugs
- Driving a codebase to "no bugs at or above High" without supervising each round (give it fix authority)
- Getting reproducing tests for whatever it finds, so fixes are verifiable

**Don't use `/bug-hunt` for:**
- A bug you already know about — use `/bug-fix`, which diagnoses first
- Security exploitability — use `/review-security`, which asks whether an attacker can exploit the code; `/bug-hunt` asks whether it fails under ordinary use
- Test-suite quality or coverage strategy — use `/review-test`

## What You'll Be Asked: Commander's Intent

Asked once, up front, then read back for confirmation:

| Field          | Question                                                                  | Default if unanswered                                                     |
|----------------|---------------------------------------------------------------------------|---------------------------------------------------------------------------|
| Scope          | What should the hunt cover? Areas you're worried about? Anything to skip? | Production code; tests, dev tooling, generated and vendored code excluded |
| Severity floor | Below what severity should findings be reported but not acted on?         | High (Critical and High block convergence)                                |
| Constraints    | Anything that must not change — public APIs, compatibility, files?        | No breaking changes; nothing else                                         |
| Tickets        | May I create tickets for confirmed bugs without asking again?             | No — a ticket set is proposed at the end for approval                     |
| Fix            | May I fix confirmed bugs (on a branch, via `/implement`) and re-hunt?     | No                                                                        |

The defaults make `/bug-hunt` an advisory audit: it changes nothing outside its report unless you say it may. Granting ticket authority up front *is* your approval to create them. Your concerns steer where it looks first; they don't replace the systematic assessment.

## The Flow

```
Commander's intent ─→ ┌─ Hunt round: assess → hunt → triage ─┐
                      │                                      │
                      └── Act (by authority): fix / ticket ←─┘
                            repeat until a round confirms nothing
                            at or above the floor (capped)
                                         │
                                         ▼
                                       Report
```

## What Each Authority Combination Produces

| Tickets | Fix | Result                                                                                                                                     |
|---------|-----|--------------------------------------------------------------------------------------------------------------------------------------------|
| no      | no  | Advisory audit: report plus reproducing tests; a ticket structure proposed at the end, created only on approval; offer to commit the tests |
| yes     | no  | Bugs ticketed autonomously; reproducing tests committed as expected failures referencing their tickets                                     |
| no      | yes | Bugs fixed via `/implement` on a branch; commits and the report are the record; tickets only for deferred items, if you approve them       |
| yes     | yes | Both: fixes for findings at or above the floor, tickets for the rest                                                                       |

## What You Get Back

- **A report** with confirmed bugs by severity (each with impact, root cause, its reproducing test, and status: fixed, ticketed, or deferred), systemic patterns, coverage improvements, suspicions it couldn't confirm, and areas not investigated. A "look at these first" section leads with contested findings, breaking-change findings, and whatever the run is least sure of. Critical findings are walked through first.
- **Reproducing tests that keep the suite green.** Tests for bugs not fixed this run are committed as expected failures (`t.Skip`, `pytest.mark.xfail`, `it.skip`, …) referencing their ticket or finding; the fix is done when the marker comes off and the test passes.
- **With fix authority, a branch** (`bug-hunt/<date>` if you were on main), plus a gitignored `BUG_HUNT_STATE.md` so a long run survives compaction and can resume.
- **Escalations, not quiet decisions.** Contested findings, fixes that would break a constraint, and anything else it can't resolve come to you — directly when you're present, or as an andon-cord handoff when running on authority.

**It never** pushes, merges to main/master, releases, or closes tickets.

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
Round 3: next hotspot tier; nothing at or above High. Converged.

Report: 3 HIGH, 1 MEDIUM, 2 coverage tests.
Proposed tickets: 3 per-bug (HIGH), 1 systemic pattern, 1 batched (MEDIUM).
You approve. Reproducing tests committed first, with xfail markers
referencing their findings; then tickets #41–#45 created, each citing its
test by path. Offer: "Hand these to /implement now?"
```

### Example 2: Tickets yes, fix no

```
Intent: scope whole repo; floor High; tickets yes; fix no.

Round 1: 2 CRITICAL (race in the cache invalidator; unchecked nil in the
  config loader). Tickets #88, #89 created immediately.
  Tests committed as expected failures:
    t.Skip("bug #88: invalidator races with readers")
Round 2: the nil pattern appears in two other loaders → ticket #90.
Round 3: nothing at or above High. Converged.

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
Round 3: nothing at or above High; 2 MEDIUM deferred.

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
