---
name: refactor-min
description: "EXPERIMENTAL — unshipped, unregistered, may be promoted or killed. Redesigns a codebase with simplification as the end goal, running Musk's five-step algorithm as its spine: question the requirements, delete the part, simplify what survives, accelerate the cycle, automate last. Behavior is pinned by a differential oracle — the incumbent implementation itself, observed at the user-visible boundary — not by the existing test suite. A blind minimizer designs and builds the minimum machine for the surviving requirements; convergence is measured in concepts and mechanisms, with an add-back ratio guarding against under-aggression. Runs on an isolated branch; one operator checkpoint (the requirements menu), autonomous after."
model: opus
---

# Refactor Min — Redesign the Machine

> **EXPERIMENTAL.** Lives on a branch, appears in no catalog. Every refactor we run on the Gen-1 engine produces the Gen-1 engine with better cable management. This skill's mandate is different: **redesign the machine with simplification as the end goal** — the Gen-3 engine that is more capable *and* has visibly less machine. It refactors *design*, not implementation; implementation falls out of the smaller design.

## The Algorithm

The spine of this skill is the five-step design algorithm Musk describes from the Raptor program (Starbase interview, 2021), in its strict order:

1. **Make the requirements less dumb.** Every requirement must carry a named source — a document section, an operator declaration, an observed user-facing behavior. "The old code did it" is not a source; a requirement whose only witness is the machinery that serves it was invented by that machinery. Requirements from smart authors are the most dangerous, because nobody questions them — and every line of LLM-written code was written by a confident author.
2. **Delete the part.** The bias is deletion, and it is calibrated: **if you are not adding back ~10% of what you delete, you are not deleting enough.** A deletion the oracle catches costs a revert; a part that should not exist survives forever.
3. **Simplify.** Only what survived steps 1–2. The most common error of a smart engineer is to optimize a thing that should not exist.
4. **Accelerate the cycle.** Verification must be cheap enough that aggressive attempts are rational — that is what the differential oracle is for.
5. **Automate.** Last. Durable harness and docs are bequeathed at the end, never built for machinery that steps 1–3 might kill.

Steps 1–3 are the design work. Steps 4–5 are how the run itself operates.

## Identity

**This skill redesigns downward.** Three rules:

1. **Behavior is pinned by the incumbent, not by the tests.** "Tests green" locks the refactor into the shape the tests assumed — the wrong shape, or there would be nothing to refactor. The oracle is the incumbent implementation itself, run side by side with the replacement and diffed **only at the user-visible boundary** (frames, digests, stdout, responses, files written). The existing suite is demoted to a *diagnostic* — useful for localizing a divergence, never a constraint on the new design.
2. **The unit of work is the design.** The minimizer does not edit the incumbent; it designs the minimum machine for the surviving requirements and builds it blind. Parallel machinery — the same problem solved twice in different modules because each was generated without knowledge of the other — is not hunted and unified; it dissolves, because the fresh design never knew there were two.
3. **Isolation is the safety.** Fresh branch `refactor-min/<slug>` (worktree when asked or conventional). One operator checkpoint — the requirements menu — then autonomous to completion. The deliverable is the branch, its metrics, and its report; merging is the operator's call.

Not golf: the budget is counted in **concepts, then mechanisms, then branches, then lines — in that order**. Comments and whitespace are free and written at house density. A version that is smaller because the same design got denser is a failure.

## Workflow

```
0. ISOLATE      branch refactor-min/<slug> from HEAD
1. CENSUS       symbol inventory + machinery clustering — the truth `ls` hides
2. QUESTION     [step 1] attribute machinery to requirements; source or
                invented; keep/kill/relax menu → the ONE operator checkpoint
3. ORACLE       [step 4 built early] differential harness: the ORIGINAL
                incumbent as oracle at the user-visible boundary, for all
                non-relaxed behavior; built once, reused by every generation
4. GENERATIONS  loop until convergence — one FRESH minimizer per pass:
                  a. re-census the current champion → new budget numbers
                  b. spawn a NEW swe-minimizer instance (empty context,
                     blind): pinned behavior + requirements + budget only —
                     never a prior generation's design, notes, or rationale
                  c. converge vs the ORIGINAL oracle (add-backs tracked;
                     ~10% is calibrated; 0% means under-aggressive)
                  d. verify: correctness gate on the generation's diff
                  e. champion = the new build if it shrank the machine;
                     stop when a fresh pass yields no meaningful reduction
                     (or declines), or at the generation cap
5. FINISH       dx-reviewer, one pass on the champion: local, human-facing
                tidying only — no structural or cross-file remedies
6. AUTOMATE     [step 5] bequeath: oracle compiled into a standing
                conformance suite; behavior-level tests ported; docs amended
7. APPRAISE     swe-value-engineer, review-only, on the champion: a priced
                trade menu — which behaviors force the remaining machinery,
                and what each would free if the operator gave it up
8. REPORT       per-generation series of concepts / mechanisms / lines;
                add-back ratios; requirements killed, relaxed, kept;
                finish-pass findings; the trade menu
```

### 1. Census — what the machine actually contains

`ls` describes the intended architecture; the census describes the real one. Using language tooling where present (LSP document-symbols, ctags) and reading where not, inventory every declared type, function, table, and mechanism **regardless of which file it hides in** — `foo.lang` quietly implementing a `Bar` is exactly what this pass exists to catch. Then:

- **Cluster parallel machinery**: mechanisms that solve the same problem (two queues, two clamp helpers, two config readers, two "manager" shapes). Each cluster is one design concept the incumbent pays for N times.
- **Count the incumbent**: concepts (distinct ideas a reader must hold), mechanisms (moving parts), code lines. These numbers are the budget the minimizer must beat and the "before" column of the report.

The census is measurement, not judgment; it feeds steps 2 and 4 and the final report.

**Parallelism:** collection is map-reduce — harvest symbols per region in parallel freely, but clustering and the counts run in **one context over the merged inventory**. A duplicate mechanism split across two shards is invisible to both, and cross-module duplication is the census's most important catch. The merged inventory (names, signatures, one-liners) is small enough for a single context even when the source is not.

### 2. Question — the requirements menu (the one checkpoint)

For each machinery cluster, name the requirement it serves and the requirement's **source**:

- **Sourced** — traces to a design-doc section, an operator declaration, or user-facing behavior a user would notice losing. Survives to the oracle.
- **Invented** — witnessed only by the incumbent implementation (its own comments, assertions, sibling precedent, or tests included). Presumed dumb; dies with its machinery unless the operator rescues it.
- **Sourced but priced** — real, but the operator might trade it: a behavior whose relaxation would dissolve disproportionate machinery.

Present one menu: kills (invented, with the machinery each drags down), trades (priced, with the machinery each would free), keeps. The operator rules — this is the "named person" the algorithm demands; a requirement nobody will put their name to is deleted. After the menu, the run is autonomous.

### 3. Oracle — pin behavior, not shape

Build the differential harness for everything not relaxed in step 2:

- **Boundary only.** Diff what a user could observe: rendered frames or digests, stdout/stderr, exit codes, responses, files written, save formats. Never internal state, module APIs, or call patterns.
- **Inputs**: recorded/replayed command logs, CLI transcripts, seeded generated input streams — enough breadth that the incumbent's observable behavior is covered, per the target's determinism story.
- **The original incumbent runs live** as the reference implementation for the whole run — every generation is diffed against it, never against the previous generation, so behavior cannot drift by degrees. Keep it runnable on the base commit.
- Divergence localization: bisect by input prefix; use the old suite as a diagnostic map, not a gate.

Where the "user" is a program (a library's published API), the boundary is that API's documented surface — the oracle diffs observable results of published calls, and internals remain fair game.

### 4. Generations — fresh eyes per pass

A single minimization pass under-strips, reliably: a designer who has just produced a design defends it, and an orchestrator that has watched the design form inherits its justifications. Field observation confirms it — re-running this skill on its own output kept finding machine to remove. So the loop is structural, and its law is: **every generation is designed by a minimizer that has never seen this project before.**

Each generation, until convergence:

1. **Re-census the champion** (the current smallest build) → fresh budget numbers.
2. **Spawn a new `swe-minimizer` instance** — empty context, blind — with the packet: the pinned behavior (oracle boundary description, surviving requirements with sources, operator relaxations), the champion's census **numbers** (budget), platform constraints (language, engine, dependencies), and house style. **Never any generation's source, tests, or history** — not the original's, not the champion's. The census's shapes stay behind too; the minimizer gets counts, not designs, so no machine ever anchors its successor. It designs first — a concept inventory naming what it *omitted* against the budget — then builds, one shot, whole target. If the packet is insufficient it says what is missing rather than peeking. (For targets too large for one context: regions with frozen external boundaries, but prefer the largest region the context carries — parallel-machinery dissolution only happens inside one designer's view.)
3. **Converge against the original oracle.** For each divergence: restore the *smallest* mechanism that repairs it (add-back), then ask whether the repaired design can shrink again. Track the **add-back ratio** per generation: ~10% says the aggression was calibrated; 0% means margin was left on the table; far above ~25% says a real requirement class was missed — check step 2's menu before grinding.
4. **Verify.** `swe-correctness-reviewer` on the generation's diff, with the design note and oracle results in hand. Findings resolved or the generation is discarded (the champion stands). The oracle passing is necessary, not sufficient — the gate hunts what the input corpus missed.
5. **Rule.** The new build becomes champion if it shrank the machine (concepts first, per the ladder). Stop when a fresh generation produces no meaningful reduction or declines outright — that is convergence, and the champion is the deliverable — or at the generation cap (elicit at startup; default 4).

What crosses generations: the pinned behavior, the requirements verdicts (including the dead list, so nothing is re-invented or re-litigated), the oracle, and the budget numbers. What never crosses: designs, design notes, rationales, divergence forecasts, add-back histories. Fresh eyes are the mechanism; inherited justification is the disease.

New behavior-for-simplicity trades proposed in any generation's design note accumulate into the report for the operator — no generation may take them itself.

### 5. Finish — one pass for the human reader

The champion is a machine no human has yet read. Spawn `dx-reviewer` (the reader advocate from `/refactor-human` — the one deliberate cross-dependency on this branch) for **a single finalizing pass**: it runs its think-aloud and concern spine over the champion and files findings, but the remedies executed here are **local only** — a rename, a module header, a comment brought to house register, a file split at the ceiling, a magic value named. No structural moves, no rewrites, no cross-file redesign: the machine's shape was settled by the generations loop and is not re-litigated by the finisher.

Findings whose remedy would be structural go to the report, not the diff. After the local edits, run the oracle and the correctness gate once — tidying is behavior-safe by intent, not by assumption. One pass, no re-review loop.

### 6. Automate — last, and only for the survivor

- Compile the differential harness into a standing conformance suite that outlives the incumbent (golden outputs, digests, transcripts committed).
- Port or rewrite the behavior-level tests worth keeping against the new design; retire internals suites with the machine they pinned (logged).
- Amend docs that promised the dead machinery — one line each, past tense — so nothing invites a faithful rebuild.

### 7. Appraise — the price menu for going further

The run's floor is the pinned behavior; the only simplification left below the champion is *behavioral*. Spawn `swe-value-engineer` (shipped; the `/review-value` agent), review-only, on the champion. Its job here is unusually clean: minimization has already stripped everything the requirements did not force, so every remaining expense attributes to a requirement that survived step 2 — and the appraisal prices exactly those. The menu it returns, per line: the behavior, its source, the machinery it forces (concepts / mechanisms / lines), and what deleting it would free.

Fold in the trades already accumulated — step 2's declined "sourced but priced" items and the generations' design-note proposals — deduplicated, so the operator sees one menu.

**Nothing on the menu is executed.** Taking a trade is a product decision: the operator relaxes the behavior in a future run's step-2 menu (where the oracle is rebuilt without it), or routes it through `/review-value` proper. This run's diff stays behavior-preserving to the end.

### 8. Report

```
## Refactor Min Complete
### Isolation: branch refactor-min/<slug> @ <sha> (base <sha>)
### The machine, by generation (gen 0 = incumbent):
###   concepts  C0 → C1 → … → Cn | mechanisms M0 → … → Mn | code lines L0 → … → Ln
### Generations: N run, champion = gen K | terminated by: convergence | cap
### Requirements: K killed (invented) / T traded (operator) / S kept — each with source
### Parallel machinery dissolved: [cluster → the one mechanism that remains]
### Add-back ratio per generation: [g1: X% … gn: Z%] — [calibrated | under-aggressive | over-aggressive]
### Oracle: N inputs, boundary [what was diffed], final state green
### Finish pass: F findings — L applied locally, R reported (structural, not taken)
### Bequest: conformance suite [location]; tests ported P, retired Q; docs amended
### Trade menu: [behavior — source — machinery it forces — what its removal frees]
### Merge: the operator's call
```

## Guardrails

- **Behavior at the boundary is inviolable** after step 2. Only the step-2 menu can relax a behavior, and only the operator can approve it; nothing is relaxed mid-run to rescue a design.
- **The oracle is never weakened** — no shrinking the input corpus or coarsening the diff to get to green.
- **The minimizer stays blind, every generation.** No source, tests, or history — the original's or any champion's — ever enters a packet; census shapes stay out; numbers only.
- **Nothing but behavior, requirements verdicts, the oracle, and budget numbers crosses generations.** A design note handed to the next designer is anchoring smuggled past the blindfold.
- **Not golf.** Concepts before mechanisms before branches before lines; house-style density; comments free. Illegibility is not simplicity.
- **Optimize nothing in step-2's kill pile.** Simplification passes run only on machinery that survived questioning.
- **The report is the conscience**: every killed requirement names the machinery it took with it; every kept one names its source.
