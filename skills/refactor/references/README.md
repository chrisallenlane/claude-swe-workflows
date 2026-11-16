# Refactor — Human Guide

The step-by-step procedure lives in [`SKILL.md`](../SKILL.md); this guide covers when to use the skill and what to expect.

`/refactor` does not clean code up; it deletes machine. Reduction is the
goal — stripping is the primary act, and regeneration is the most
effective instrument of it. The mental model is the Raptor engine line:
each generation more capable, less machine. The spine is the five-step
design algorithm from that program, in strict order — question the
requirements, delete the part, simplify what survives, accelerate the
cycle, automate last.

## Why it is shaped this way

- **Behavior is pinned by the incumbent, not by the tests.** "Tests green"
  locks a redesign into the shape the tests assumed. Instead, the
  original implementation runs live beside every candidate and is diffed
  only at the user-visible boundary. The old suite is a diagnostic, never
  a constraint.
- **Adoption is mechanical.** Both recorded failures of this skill's
  ancestors were judgment failures — trusting a self-report, then
  defending the machine it was handed. So candidates pass or fail gates
  (behavior, correctness, structure); nobody argues either side.
- **Documents nominate; only you ratify.** In an LLM-written repo, the
  design docs were written by the same confident author as the code.
  They can put a requirement on the menu, but cannot keep it alive.

## When to use

- You want a codebase, or a region of one, to become visibly smaller
  while behaving the same at the boundary users see.
- The design has accreted parallel machinery, invented requirements, or
  layers nobody can justify.

**Not for:** a targeted bug fix (`/bug-fix`), new features (`/implement`),
or advice without changes — `/review-repo value` for requirement
trades, `/review-repo architecture` for a structural blueprint,
`/review-repo dead-code` for a dead-code audit.

## The flow

```
ISOLATE  →  BASELINE  →  ITERATE  →  FINISH  →  AUTOMATE  →  REPORT
            (the menu:   (strip ⇄     (local     (oracle →
             your one     regenerate,  tidying    conformance
             checkpoint)  gated)       for humans) suite)
```

## What you'll be asked

**One menu, once, near the start** — the only interactive step. It opens
with two stakes questions (*what happens if this breaks?* and *who
maintains it, for how long?*), the iteration cap (default 4), and any
custom verification probes you can name ("run `make demo` and check the
output"). Then a verdict per machinery cluster: ratified, documented
(docs nominate; you ratify), invented (presumed dead unless you rescue
it), or priced (offered as a trade). Bulk rulings ("keep all
documented") are fine. Everything you kill takes its machinery with it.
After the menu the run is autonomous.

## What you get back

- **A branch, not a merged result** — `refactor/<slug>` (or a worktree),
  one atomic commit per change. Your working tree is untouched; merging
  is your call.
- **Deletion-biased results by design.** The run is calibrated so that
  roughly 10% of what it deletes gets restored when the oracle objects.
- **Behavior preservation at the user-visible boundary**, not test-suite
  preservation. Internal tests pinned to the old structure retire with
  it; behavior-level tests are ported; the differential harness becomes
  a standing conformance suite.
- **A report** with the per-iteration machine count (concepts,
  mechanisms, lines), requirements killed/traded/kept with sources, a
  **trade menu** (behaviors you could give up in a future run), and a
  **side memo** of bugs found but not touched — the oracle pins today's
  behavior, bugs included, so a silent fix would be a divergence.

## What it never does

- Relax a behavior you didn't relax at the menu, or weaken the oracle to
  get to green.
- Let a document or precedent defend machinery after the menu.
- Count density as simplification: a candidate that "shrank" by merging
  named functions into long bodies fails the structure gate.
- Modify anything untracked by git.
