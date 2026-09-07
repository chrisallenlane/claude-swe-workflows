# Refactor — Human Guide

`/refactor` does not clean code up; it deletes machine. Reduction is the
goal — stripping is the primary act, and regeneration is the most
effective instrument of it. The mental model is the Raptor engine line:
each generation more capable, less machine. The spine is the five-step
design algorithm from that program, in strict order — question the
requirements, delete the part, simplify what survives, accelerate the
cycle, automate last.

## What happens when you run it

```
0. ISOLATE     a fresh branch (refactor/<slug>) or worktree; your tree is
               never touched — merging the result is always your call
1. BASELINE    the machine is counted (filenames lie; symbols are
               inventoried wherever they hide), then THE ONE INTERACTIVE
               STEP: a requirements menu opening with two stakes questions
               (what happens if this breaks? who maintains it?) and any
               custom verification probes you can name, then verdicts —
               ratified / documented (docs nominate; you ratify) /
               invented (presumed dead) / priced (offered as a trade).
               Then behavior is pinned: the ORIGINAL implementation runs
               live as a differential oracle, diffing user-visible output
               only. The old test suite never constrains the new design.
2. ITERATE     each pass: recount → re-attribute → then an inner loop of
               STRIP (a deletion-stance hunter deletes everything the
               gates permit — never regenerate what you can simply
               remove) interleaved with REGENERATE (a brand-new blind
               designer builds the minimum machine for the surviving
               requirements); a strip that breaks pinned behavior is
               repaired by restoring the old part or regenerating a
               smaller replacement, whichever measures less machine.
               Candidates pass or fail three
               MECHANICAL gates — behavior, correctness, structure — and
               nobody argues: the orchestrator is a clerk, not a judge.
               Fresh eyes every pass; stop when a pass changes ~nothing.
3. FINISH      swe-refactor-dx tidies the result for human readers — local
               edits only.
4. AUTOMATE    the oracle becomes a standing conformance suite; docs are
               amended so nothing promises dead machinery.
5. REPORT      the per-iteration series (concepts / mechanisms / lines),
               strips, requirements verdicts, trade menu, side memo.
```

## What to expect

- **One menu, once, near the start.** This is where you have power:
  everything you kill takes its machinery with it. Bulk rulings ("keep
  all documented") are fine.
- **Deletion-biased behavior by design.** The run is calibrated so that
  roughly 10% of what it deletes gets restored when the oracle objects —
  if nothing ever needs restoring, it wasn't cutting hard enough.
- **Behavior preservation at the user-visible boundary**, not test-suite
  preservation. Internal tests pinned to the old structure retire with
  it; behavior-level tests are ported; the differential harness becomes
  the durable regression suite.
- **A trade menu and a side memo in the report**: behaviors you could
  give up to dissolve machinery (your call, for a future run), and bugs
  the run found but did not touch — fixing a bug changes behavior, and
  the oracle pins behavior, bugs included.
- **A branch, not a merged result.** Read the report and the ledger,
  then merge or delete.

## Key rules that make it safe

- The original implementation stays runnable and is the reference for
  every iteration — behavior cannot drift by degrees.
- After the menu, documents are dead law: no agent may defend machinery
  by citing DESIGN.md or precedent. Only your verdicts and the pinned
  behavior govern.
- Adoption is mechanical: gates pass and the machine shrank → adopted;
  anything else → the previous champion stands. No agent argues either
  side, because both argued directions have failed in the field.
- The structure gate catches golf: a candidate that "shrank" by merging
  named functions into dense bodies fails on measured function lengths.
- Nothing untracked by git is ever modified.

## Agents used

- `swe-refactor-deleter` — the deletion hunter; fresh instance per strip pass
- `swe-refactor-minimizer` — the blind designer; fresh instance per iteration
- `swe-refactor-dx` — the reader advocate for the finishing pass
- `swe-correctness-reviewer` — the correctness gate on every candidate
