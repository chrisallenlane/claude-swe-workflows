# Refactor — Human Guide

`/refactor` does not clean code up; it redesigns the machine downward. The
mental model is the Raptor engine line: each generation more capable, less
machine. The skill's spine is the five-step design algorithm from that
program, in strict order — question the requirements, delete the part,
simplify what survives, accelerate the cycle, automate last.

## What happens when you run it

```
0. ISOLATE      a fresh branch (refactor/<slug>) or worktree; your tree is
                never touched — merging the result is always your call
1. CENSUS       symbol inventory of what the code actually contains
                (filenames lie); parallel machinery clustered; the machine
                counted in concepts / mechanisms / lines
2. QUESTION     THE ONE INTERACTIVE STEP. Every requirement the machinery
                serves is put on a menu: ratified (you, or user-visible
                behavior), documented (docs nominate; you ratify), invented
                (only the code itself vouches for it — presumed dead),
                priced (real, but expensive — offered as a trade). You rule
                once; the run is autonomous after.
3. ORACLE       behavior is pinned by running the ORIGINAL implementation
                side by side with each candidate and diffing user-visible
                output only. The old test suite does not constrain the new
                design; it is demoted to a diagnostic.
4. GENERATIONS  the core loop. Each pass, a brand-new blind designer
                (swe-minimizer) — which never sees any existing source, only
                behavior, requirements, and size numbers — builds the
                minimum machine. The orchestrator measures structure
                independently, hears the designer's rebuttal on any
                objection, and adopts unless a grounded objection stands.
                Fresh eyes every pass; loop ends when a generation finds
                nothing more to remove.
5. FINISH       dx-reviewer tidies the result for human readers — local
                edits only.
6. AUTOMATE     the oracle is compiled into a standing conformance suite;
                docs amended so nothing promises dead machinery.
7. APPRAISE     a value-engineering pass prices what remains: a menu of
                behavior-for-simplicity trades you may take in a future run.
8. REPORT       the per-generation series (concepts / mechanisms / lines),
                requirements killed and kept, add-back ratios, trade menu.
```

## What to expect

- **A requirements menu, once, near the start.** This is where you have
  power: everything you kill takes its machinery with it. Bulk rulings
  ("keep all documented") are fine.
- **Deletion-biased behavior by design.** The run is calibrated so that
  roughly 10% of what it deletes gets restored when the oracle objects —
  if nothing ever needs restoring, it wasn't cutting hard enough.
- **Behavior preservation at the user-visible boundary**, not test-suite
  preservation. Internal tests pinned to the old structure are retired
  with it; behavior-level tests are ported; the differential harness
  becomes the durable regression suite.
- **A branch, not a merged result.** Read the report and the ledger, then
  merge or delete.

## Key rules that make it safe

- The original implementation stays runnable and is the reference for
  every generation — behavior cannot drift by degrees.
- After the menu, documents are dead law: no agent may defend machinery by
  citing DESIGN.md or precedent. Only your verdicts and the pinned
  behavior govern.
- The bench defends no incumbent: candidates are adopted unless a
  grounded, evidence-cited objection survives the designer's rebuttal.
- Nothing untracked by git is ever modified.

## Agents used

- `swe-minimizer` — the blind designer; fresh instance per generation
- `dx-reviewer` — the reader advocate for the finishing pass
- `swe-value-engineer` — the appraisal (shared with /review-value)
- `swe-correctness-reviewer` — the adversarial gate on every adoption
