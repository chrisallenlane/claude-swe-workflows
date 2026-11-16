---
name: bug-hunt
description: Proactive bug hunting. Assesses where bugs likely hide, confirms each finding with a reproducing test, and iterates until nothing is found above a severity floor. Advisory by default; creates tickets or fixes via /implement only when authorized.
model: opus
---

# Bug Hunt — Find Bugs Before Users Do

Hunts for bugs nobody knows about yet. An assessor works out where bugs are likely to hide by cross-referencing change history (complexity × churn hotspots, fix density, change coupling), coverage gaps, and structural risk; focused hunters then probe each hotspot and write a reproducing test for every suspected bug. No speculative reports: a finding without a failing test is a suspicion, and is labeled as one.

The user states intent once. The skill then hunts round after round until a round confirms nothing at or above the severity floor — and, if given the authority, tickets what it finds and fixes it via `/implement` between rounds.

## Philosophy

**Evidence, not opinion.** Every confirmed bug has a reproducing test that encodes the correct behavior and fails against the current code. That test is the finding's proof, the ticket's acceptance criterion, and the fix's verification.

**Finding and fixing stay separate.** Hunters never fix. The pressure to find bugs should not bend toward bugs that are easy to fix, and a fix needs fresh reasoning the hunter isn't in. When the skill has fix authority, it hands confirmed findings to `/implement`, which fixes them under its own floor — concept inventory, practical verification, independent correctness review — in a fresh context.

**Converge on a floor, not on zero.** A hunt always finds *something* at Low. The severity floor is the run's dominant judgment call: findings at or above it block convergence; findings below it are reported and left alone.

**No rationalizing bugs away.** A finding with a failing reproducing test is real. The skill may contest a finding only on substance — the test asserts the wrong behavior, or the "bug" is documented intended behavior — and a contested finding goes to the user, not into a quiet drop.

## 1. Commander's Intent

Ask once, up front:

| Field          | Question                                                                      | Default if unanswered                                                     |
|----------------|-------------------------------------------------------------------------------|---------------------------------------------------------------------------|
| Scope          | What should the hunt cover? Any areas you're worried about? Anything to skip? | Production code; tests, dev tooling, generated and vendored code excluded |
| Severity floor | Below what severity should findings be reported but not acted on?             | High (Critical and High block convergence)                                |
| Constraints    | Anything that must not change — public APIs, compatibility, files?            | No breaking changes; nothing else                                         |
| Tickets        | May I create tickets for confirmed bugs without asking again?                 | **No** — propose a ticket set at the end for approval                     |
| Fix            | May I fix confirmed bugs (on a branch, via `/implement`) and re-hunt?         | **No**                                                                    |

User concerns steer prioritization; they don't replace systematic assessment. Read the intent back and confirm it. Granting ticket authority here *is* the approval to create them; without it, nothing is created unasked.

**With fix authority**, work on a branch: never commit to main/master; if on it, create `bug-hunt/<date>`. Keep `BUG_HUNT_STATE.md` (gitignored) with the pinned intent and a per-round log, so the run survives compaction and can resume.

## 2. Hunt

Each round runs assess → hunt → triage. Round 1 covers the whole scope; later rounds narrow (see §3).

### Assess

Spawn `swe-bug-assessor` with the scope, exclusions, user concerns, and — after round 1 — what earlier rounds found and changed. It reads change history first (complexity × churn hotspots, fix density, change coupling), measures coverage (instrumented where available), finds complexity and structural risk (error-handling gaps, input validation, shared mutable state, resource handling, concurrency, edge cases, consistency), and returns hotspots ranked by **converging** signals: a frequently-fixed, complex, untested hotspot outranks any single signal.

### Hunt each hotspot

Spawn a fresh `swe-bug-hunter` per hotspot, **sequentially**, passing each one the confirmed bugs and patterns found so far — a broken error-handling utility found in one module is a lead for every module that uses it.

```
You are a focused bug hunter.

## Hotspot
Target / files / risk signals / hypothesis / approach: [from the assessor]

## Prior findings
[Confirmed bugs and patterns from earlier hunters and rounds]

## Mission
Probe this hotspot for bugs. For each suspected issue, write a test that
encodes the correct expected behavior, asserted at the boundary a caller
sees — not against internals, which would push the eventual fix toward
the wrong shape.
- Test FAILS: bug confirmed. Keep the test; document the finding.
- Test PASSES: hypothesis invalidated. Keep the test only if it covers a
  previously untested path; otherwise delete it.
No speculative reports. Note patterns that may apply elsewhere.
```

### Triage

For each confirmed finding:

1. **Verify** the reproducing test fails against current HEAD. If it doesn't, the finding is not confirmed.
2. **Classify** against the floor: at or above → act on it this round; below → deferred, reported only.
3. **Screen for contests.** If the finding looks wrong on substance, record why and route it to the user (§5). Never drop it silently.
4. **Screen for breaking changes.** A fix that would require a breaking change, or would violate a constraint, goes to the user, not to `/implement`.
5. **Look for patterns.** Bugs sharing a root cause — or a buggy utility used beyond the hotspot that exposed it — become systemic patterns, and leads for the next round.

## 3. Act and Iterate

**With fix authority:** hand the round's at-or-above-floor findings to `/implement` per its "Invoked by Another Skill" contract — the findings (or their tickets) as the work, each reproducing test as the acceptance criterion, the intent's constraints as constraints. `/implement`'s floor applies unchanged; its escalations come back here. When it finishes, the reproducing tests pass.

**With ticket authority:** create tickets per [`references/trackers.md`](../../references/trackers.md) for confirmed bugs this run does not fix — with fix authority too, that means only the deferred and escalated ones, since a fix's record is its commit. One ticket per bug at or above the floor, and one per systemic pattern; findings below the floor stay in the report — granting ticket authority does not extend to them. Each ticket carries the bug, its impact, root cause, fix guidance, and its reproducing test as acceptance criterion.

**Reproducing tests for bugs not fixed this run**, whenever they are committed — during a run with authority, or at the end when you accept the offer — are marked as expected failures, using the project's mechanism (`t.Skip`, `pytest.mark.xfail`, `it.skip`, …) with a reference to the ticket or finding. The suite stays green; the fix is done when the marker is removed and the test passes. Coverage-improving tests are committed as ordinary tests.

**Next round.** Hunt again where new bugs are likely: code the fixes changed, siblings of confirmed patterns, and the next tier of assessor hotspots. Without fix authority, rounds still continue through siblings and the next tier — they just don't re-hunt fixes.

**Converge** when a round confirms nothing at or above the floor. **Hard cap: 10 rounds**, then stop and report what remains. Use judgment on a final `/review-test` pass over the tests this run wrote when there are many of them.

## 4. Report

```
## Bug Hunt Complete

Intent: [scope; floor; constraints; tickets yes/no; fix yes/no]
Rounds: N — converged | cap reached
Confirmed: N (X critical, Y high, Z medium, W low) — F fixed, T ticketed, D deferred

## Look at these first
[Contested findings, breaking-change findings, and anything the run is
 least sure of — each with its evidence.]

## Confirmed bugs (by severity)
- **file:line — description** — impact; root cause; reproducing test
  (file:name); status: fixed at <sha> | ticket #N | deferred (below floor)

## Systemic patterns
- [pattern] — seen in [locations] — [recommendation]

## Coverage improvements
- [test] in [file] — covers [what]

## Suspected but unconfirmed
- [description] — not testable because [reason]

## Not investigated
[Hotspots deprioritized, or areas outside scope worth a future look]

## Branch (if fixing)
- bug-hunt/<date> @ <sha>, base <main> @ <sha>; N commits
```

Walk the user through Critical findings first: the bug, its impact, and the reproducing test.

**Without ticket authority**, end by proposing tickets for whatever the run did not fix, in a structure shaped by the hunt — per-bug tickets for Critical/High, per-pattern tickets for systemic issues, batched tickets below — and create it only on approval, per [`references/advisory-tickets.md`](../../references/advisory-tickets.md). On approval, commit the reproducing tests first (expected-failure markers referencing the finding), then create the tickets, which cite the tests by path. If tickets are declined, offer to commit the tests anyway. **Without fix authority**, offer to hand the confirmed bugs to `/implement`.

## 5. Escalation

With the user present, ask. When running on authority, stop and hand off per [`references/autonomy.md`](../../references/autonomy.md)'s andon-cord template (phase identifier: the round number), when:

- A finding is **contested** on substance.
- A fix would require a **breaking change** or violate a constraint.
- `/implement` escalates and the cause can't be resolved here.
- A bug fixed in one round is confirmed again in a later round.
- A merge conflicts, or the suite breaks for reasons that aren't local.
- On resume, HEAD no longer matches `BUG_HUNT_STATE.md`.

Never push, merge to main/master, release, or close tickets.

## Coordination

Fresh agent instances for every assessor and hunter. Hunters run sequentially so findings accumulate. The orchestrator keeps the hotspot list, running findings, created test files, and round count; `BUG_HUNT_STATE.md` holds them durably when the run has fix authority.

## Relationship to Other Skills

**`/bug-fix`** fixes a bug you already know about, diagnosis first. **`/bug-hunt`** finds bugs nobody knows about.

**`/review-security`** asks whether an attacker can exploit the code; `/bug-hunt` asks whether it will fail under ordinary use. Their territory overlaps; their lenses don't.
