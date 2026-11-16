---
name: refactor
description: "Simplification-first codebase redesign (Musk's five steps), with behavior pinned by a differential oracle against the incumbent implementation. Runs on an isolated branch; one operator checkpoint (the requirements menu), then autonomous."
model: opus
---

# Refactor — Redesign the Machine

> A conventional refactor of the Gen-1 engine produces the Gen-1 engine with better cable management. This skill's mandate is different: **redesign the machine with simplification as the end goal** — the Gen-3 engine that is more capable *and* has visibly less machine. It refactors *design*, not implementation; implementation falls out of the smaller design.

## The Algorithm

The spine of this skill is the five-step design algorithm Musk describes from the Raptor program (Starbase interview, 2021), in its strict order:

1. **Make the requirements less dumb.** Every requirement must trace to a *person* — the operator — or to behavior a user would notice losing. "The old code did it" is not a source; a requirement whose only witness is the machinery that serves it was invented by that machinery. Neither is "the old docs say so": in an LLM-written repository, DESIGN.md and the ADRs were written by the same confident author as the code — usually *after* it — and are the incumbent's testimony in better dress. Documents **nominate** requirements for the menu; only the operator ratifies them. Requirements from smart authors are the most dangerous, because nobody questions them — and every line of LLM-written code and docs was written by a confident author.
2. **Delete the part.** The bias is deletion, and it is calibrated: **if you are not adding back ~10% of what you delete, you are not deleting enough.** A deletion the gates catch costs a revert; a part that should not exist survives forever.
3. **Simplify.** Only what survived steps 1–2. The most common error of a smart engineer is to optimize a thing that should not exist.
4. **Accelerate the cycle.** Verification must be cheap enough that aggressive attempts are rational — that is what the differential oracle is for.
5. **Automate.** Last. Durable harness and docs are bequeathed at the end, never built for machinery that steps 1–3 might kill.

## Identity

**This skill redesigns downward, and its end is deletion.** The goal is the reduction of the machine — fewer parts, held to at most today's behavior. Stripping is the primary act; regeneration is the most effective *instrument* of stripping we have found (it deletes parallel machinery and invented requirements wholesale, by never rebuilding them), but it is means, not end. Three rules:

1. **Behavior is pinned by the incumbent, not by the tests.** "Tests green" locks the refactor into the shape the tests assumed — the wrong shape, or there would be nothing to refactor. The oracle is the *original* implementation, run side by side with every candidate and diffed **only at the user-visible boundary** (frames, digests, stdout, responses, files written). The existing suite is demoted to a *diagnostic* — useful for localizing a divergence, never a constraint on the new design.
2. **Adoption is mechanical, never discursive.** A candidate that passes the gates — behavior, correctness, structure — and shrank the machine is adopted; there is nothing to discuss. One that fails a gate is not; there is still nothing to discuss. The orchestrator is a **clerk, not a judge**: it runs gates, records results, and never argues with a minimizer or defends an incumbent. Both recorded failures of this skill's ancestors were judgment failures — a bench trusting a self-report, then a bench wrongfully defending the machine it was handed. The gates replace the bench.
3. **Isolation is the safety.** Fresh branch `refactor/<slug>` (worktree when asked or conventional). One operator checkpoint — the requirements menu — then autonomous to completion. The deliverable is the branch, its metrics, and its report; merging is the operator's call.

Not golf: the machine is counted in **concepts, then mechanisms, then branches, then lines — in that order**. Comments and whitespace are free and written at house density. A version that is smaller because the same design got denser is a failure, and the structure gate catches it mechanically.

## Workflow

```
0. ISOLATE     branch refactor/<slug> from HEAD
1. BASELINE    census the incumbent; the requirements menu — the ONE
               operator checkpoint (stakes, probes, verdicts); build the
               oracle against the ORIGINAL incumbent, pinned for the run
2. ITERATE     until an iteration changes ~nothing (cap: set at the menu; default 4):
                 a. CENSUS      recount the champion → budget numbers
                 b. QUESTION    re-attribute machinery to the standing
                                verdicts (non-interactive); new nominations
                                and trades accumulate to the report
                 c. STRIP ⇄ REGENERATE — an inner loop, not a sequence:
                                strip until stripping stalls; regenerate
                                (fresh blind swe-refactor-minimizer) while design-
                                level work remains; strip again after any
                                regeneration. A strip that breaks pinned
                                behavior is repaired by restoring the old
                                part OR regenerating a minimal replacement
                                — whichever measures smaller. Every
                                candidate faces the gates; adopt iff they
                                pass and the machine shrank — no court
3. FINISH      swe-refactor-dx, one pass: local, human-facing tidying only
4. AUTOMATE    bequeath: oracle compiled into a standing conformance suite;
               behavior-level tests ported; docs amended
5. REPORT      per-iteration series; strips; requirements verdicts; trade
               menu; side memo
```

### 1. Baseline

**Census the incumbent.** Using language tooling where present (LSP document-symbols, ctags) and reading where not, inventory every declared type, function, table, and mechanism **regardless of which file it hides in** — `foo.lang` quietly implementing a `Bar` is exactly what this pass catches. Cluster **parallel machinery** (the same problem solved twice in different modules), and count the machine: concepts, mechanisms, code lines. Collection may fan out; **clustering and counts run in one context over the merged inventory** — a duplicate split across two shards is invisible to both.

**The requirements menu — the one checkpoint.** It opens with stakes, answered once and recorded verbatim: *what happens if this breaks?* and *who maintains it, for how long?* — plus the iteration cap (default 4). Stakes calibrate the whole run — how hard questioning presumes death, how deep the corpus must go, what an add-back is worth. **Operator probes ride along**: custom verification steps ("run `make demo` and check the output," "hit `/health`") become oracle corpus. Then the verdicts, one machinery cluster at a time:

- **Ratified** — an operator declaration, or user-facing behavior a user would notice losing. Pinned.
- **Documented** — cited by a design doc, ADR, or README, but not independently user-visible. **A citation is a nomination, not a verdict** — the docs are part of the incumbent, not above it. The operator's keep ratifies; bulk rulings ("keep all documented") are fine.
- **Invented** — witnessed only by the incumbent itself (its comments, assertions, sibling precedent, tests included). Presumed dead unless the operator rescues it.
- **Priced** — real, but worth trading: a behavior whose relaxation would dissolve disproportionate machinery. Offered; the operator may take the trade now or leave it on the menu.

After the menu, the run is autonomous.

**The oracle.** Build the differential harness for everything not relaxed: the **original incumbent runs live** as the reference for the entire run — every candidate in every iteration is diffed against it, never against the previous champion, so behavior cannot drift by degrees. Diff **only what a user could observe**: rendered frames or digests, stdout/stderr, exit codes, responses, files written, save formats — never internal state, module APIs, or call patterns. Inputs: recorded/replayed command logs, transcripts, seeded generated streams, and the operator's probes verbatim. Where the "user" is a program (a library's published API), the boundary is that API's documented surface. Keep the incumbent runnable at the base commit; localize divergences by input-prefix bisection, using the old suite as a map, not a gate.

### 2. Iterate

Each iteration is one turn of the crank on the current champion (iteration 1's champion is the raw incumbent). Stop when an iteration changes approximately nothing — a thin strip and a declined or cosmetic regeneration — or at the iteration cap.

**a. Census.** Recount the champion. Budget numbers for this iteration; the "by iteration" row of the report.

**b. Question.** Re-attribute the champion's machinery to the standing verdicts — non-interactive; the menu is never reopened mid-run. Newly visible nominations and trades (stripping uncovers them) accumulate to the report for the operator's next run. The dead list persists so nothing is re-invented or re-litigated.

**c. Strip ⇄ Regenerate — the inner loop.** Stripping and regeneration are two moves in one game, not two stages: stripping often exposes design-level work only regeneration can do, and an aggressive strip sometimes takes a pinned behavior with it — in which case the repair is **either restoring the old part or regenerating a minimal replacement for just that hole, whichever measures smaller**. Restore-versus-rebuild is a gate question like everything else, not a discussion. Alternate the moves freely — strip until stripping stalls, regenerate while design-level work remains, always strip again after a regeneration lands — and end the iteration when neither move produces an adoptable candidate.

**The strip move.** **Never regenerate what you can simply remove.** Spawn `swe-refactor-deleter` — fresh instance, assigned stance, removal-only jurisdiction — and apply its proposals in batches, highest-confidence first. Each batch is adjudicated by the gates like any candidate: pass → dead; fail → repaired (restore or minimal rebuild, as above), no discussion. The hunt is safe from anchoring for a structural reason — **anchoring poisons designers, not deleters**: an examiner that may only remove makes no design decisions for the incumbent to bias. Behavior-touching finds route to the trade menu; add-shaped finds to the side memo.

**Target identification is an optimizer's job, not a connoisseur's.** Reachability finds only what nothing needs; the real prey is live structure that does no work, and compilers have destroyed that mechanically for decades. The deleter runs the classic pass catalog as its detectors — dead-code elimination (references, plus oracle-corpus coverage where the language has instrumentation), copy propagation (forwarding wrappers, aliases, export mirrors), inlining (fan-in-1/fan-out-1 pipe nodes), constant folding (parameters with one value across all call sites; config nothing varies), common-subexpression elimination (the census's parallel-machinery clusters), branch simplification (corpus branch coverage: arms never taken, conditions that never vary) — and **cascades them to a fixpoint**, because each pass unlocks the next: a folded constant decides a branch, the dead arm orphans a function, DCE takes it. We hold a looser license than any compiler — only boundary behavior is pinned — so every classic pass applies *a fortiori*, plus the moves no compiler may make (the guard whose input cannot occur). Judgment is spent only on the residue no detector sees. What no pass can do — dissolve a concept, change a data structure, see that three state machines are one — is the regenerate move's jurisdiction: the deleter estimates each mechanism's **naive-baseline delta** (the dumbest implementation meeting the stakes, versus what stands) and hands the largest gaps to regeneration as its priority list.

**How a part dies — the excision protocol.** A strip is an excision, not an `rm`, and it is performed like this:

1. **Root first, compiler-guided.** Delete the *declaration* — the concept — never the uses; the build errors and lint diagnostics are the worklist. Follow the cascade until clean. Anything the cascade reveals as referenced only by the dead part is a bonus kill: take it in the same batch.
2. **The suture rule.** Every hole the excision leaves closes with *less* machine: the constant the function always returned, the expression the wrapper forwarded to, nothing at all if the result went unused. A hole that needs **new** machinery to close means this was never a deletion — it is a redesign wearing one's clothes; withdraw the strip and leave it for the regenerate move (alongside the naive-baseline-delta priorities).
3. **The part dies whole.** Its internals-pinning tests, its comments and warnings, its config knobs, and its observers — anything whose only purpose was watching it — die in the same commit. One concept and its cascade per batch, one atomic commit, so a gate failure indicts exactly one deletion.

**The regenerate move.** Spawn a **new `swe-refactor-minimizer` instance** — empty context, blind — with: the pinned behavior (oracle boundary, surviving requirements with sources, relaxations), the stripped champion's census **numbers** as budget, platform constraints, house style. **Never any machine's source, tests, or history** — not the original's, not the champion's; census shapes stay behind; no design, note, or rationale from any earlier iteration crosses. It designs first (a concept inventory naming its omissions checkably), then builds whole-target. Converge via add-backs: run the oracle; classify each divergence — **the corpus defines behavior**: a difference no realistic input can produce is a **discovered kill** (log it, accept it; the same law governs differences found by reading); a real divergence gets the smallest repairing add-back. Track the add-back ratio (~10% calibrated; ≫25% means a missed requirement class — recheck the verdicts; ~0% read against the structure numbers, a precise spec legitimately needs few). Then the gates. For targets too large for one context: regions with frozen boundaries, but prefer the largest region a context carries — parallel-machinery dissolution happens only inside one designer's view.

### The Gates — mechanical, all of them

Every candidate — strip batch or regeneration — faces the same three gates. Self-reported numbers are never inputs; the orchestrator measures everything itself.

1. **Behavior.** Oracle green over the full corpus, probes included.
2. **Correctness.** `swe-correctness-reviewer` on the diff. Findings resolved or the candidate is discarded. Exhaustiveness demoted to a default case, and deleted compile-time assertions, are regressions even when today's behavior matches.
3. **Structure.** Orchestrator-computed (grep, LSP, scc): declarations and functions per file, public symbols, branch count, max and median function length, code lines. The candidate must not grow the machine, and **density must not degrade**: max and median function length within the champion's neighborhood and the house register — a build that shrank its line count by merging named functions into long bodies fails here, mechanically, with no reading of intent required. Public-surface sweep rides along: every public symbol shows an external reference or is demoted — no caller, no export.

Gates pass and the machine shrank → adopt. Anything else → the champion stands. Neither outcome is argued, rebutted, or re-litigated; the minimizer's design note and forecasts are context for humans reading the report, not evidence before a court there isn't one.

### 3. Finish — one pass for the human reader

The champion is a machine no human has yet read. Spawn `swe-refactor-dx` (the reader advocate) for **a single finalizing pass**: think-aloud plus concern spine, but remedies executed here are **local only** — a rename, a module header, a comment brought to house register, a file split at the ceiling, a magic value named. No structural moves, no rewrites: the machine's shape was settled by the loop. Structural findings go to the report, untaken. After the edits, run the gates once — tidying is behavior-safe by intent, not by assumption.

### 4. Automate — last, and only for the survivor

- Compile the differential harness into a standing conformance suite that outlives the incumbent (golden outputs, digests, transcripts committed).
- Port or rewrite the behavior-level tests worth keeping; retire internals suites with the machine they pinned (logged).
- Amend docs that promised dead machinery — one line each, past tense — so nothing invites a faithful rebuild.

### 5. Report

```
## Refactor Complete
### Isolation: branch refactor/<slug> @ <sha> (base <sha>)
### The machine, by iteration (0 = raw incumbent):
###   concepts  C0 → C1 → … → Cn | mechanisms M0 → … → Mn | code lines L0 → … → Ln
### Iterations: N run | terminated by: convergence | cap
### Per iteration: strip (proposed/applied/restored, red lines) + regeneration (adopted/declined, add-back ratio)
### Requirements: K killed (invented) / T traded / S kept — each with source
### Parallel machinery dissolved: [cluster → the one mechanism that remains]
### Oracle: N inputs, boundary [what was diffed], final state green
### Finish pass: F findings — L applied locally, R reported (structural, not taken)
### Bequest: conformance suite [location]; tests ported P, retired Q; docs amended
### Trade menu: [behavior — source — machinery it forces — what removal frees; from question + minimizer proposals]
### Side memo: [bugs and missing capabilities found and not touched — for the operator]
### Merge: the operator's call
```

## Guardrails

- **Behavior at the boundary is inviolable** after the menu. Only the menu can relax a behavior, and only the operator can approve it; nothing is relaxed mid-run to rescue a candidate.
- **The oracle is never weakened** — no shrinking the corpus or coarsening the diff to get to green.
- **The minimizer stays blind, every iteration.** No source, tests, or history — the original's or any champion's — ever enters a packet; census shapes stay out; numbers only. Nothing but behavior, requirements verdicts, the oracle, and budget numbers crosses iterations.
- **The clerk does not judge.** Adoption and decline are gate outcomes. An orchestrator caught arguing a candidate down — or defending one — has left its role; both failure modes are on this skill's record.
- **Not golf — and adjudicated, not just declared.** Concepts before mechanisms before branches before lines; house-style density; comments free. The structure gate enforces this mechanically; a guardrail that exists only as prose fires only by luck.
- **After the menu, documents are dead law.** No agent may decline or soften a removal by citing DESIGN.md, an ADR, a README, a comment, or "how it was done before." The pinned behavior and the operator's verdicts are the *entire* law of the run; a document matters only as the nominator of a requirement the operator kept.
- **Optimize nothing in the kill pile.** Simplification runs only on machinery that survived questioning.
- **Commit discipline.** One atomic commit per strip batch, per adopted regeneration, per finish pass, per bequest — stage the specific files, verify the staged diff, `refactor:` prefix. The branch history is the run's audit trail.
- **Version-controlled files only.** The run modifies nothing untracked by git — untracked work could be irreversible to lose. Non-negotiable regardless of scope.
- **The side memo.** Any pass that trips over a genuine bug or missing capability records it and moves on — the oracle pins today's behavior, bugs included, so a silent fix is a divergence and a dropped finding is a loss.
- **The report is the conscience**: every killed requirement names the machinery it took with it; every kept one names its source.
