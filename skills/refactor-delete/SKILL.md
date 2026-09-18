---
name: refactor-delete
description: "EXPERIMENTAL — unshipped, unregistered, may be promoted or killed. Reduction-only refactoring: runs /refactor's strip machinery — the optimizer pass catalog, the excision protocol, the mechanical gates — with no whole-target regeneration. Behavior never changes; every remedy must remove or simplify — code may be written only in service of a measured net reduction (a smaller in-place replacement, a general path dissolving special cases). Cheap by design: an abbreviated checkpoint (stakes, floors, probes — no requirements docket), the existing behavior-level suite as the default harness, and a fixpoint strip loop. What deletion cannot reach is reported as /refactor's regeneration priority list, not attempted. Exists to test whether deletion alone captures most of the redesign skill's value at a fraction of its cost."
model: opus
---

# Refactor Delete — Reduction Only

> **EXPERIMENTAL.** Lives on a branch, appears in no catalog. A controlled amputation of `/refactor`: the same strip machinery, the whole-target regeneration organ removed — every remedy must remove or simplify, and code is written only as a means to a measured reduction. Field observation motivated it — a bare deletion pass on a live project was hugely productive with no generative step at all. The open question this skill exists to answer: **how much of the redesign skill's value does deletion alone capture, at what fraction of its cost?** Run it, compare, and let the results decide what `/refactor` should schedule.

## Identity

**This skill only reduces.** Three rules:

1. **Behavior never changes.** There is no requirements docket because no behavior is ever relaxed — every change must be invisible at the user-visible boundary. The one nuance is inherited law: **the corpus defines behavior** — a guard on inputs the platform cannot send defends nothing observable, and removing it changes no behavior a realistic input can witness.
2. **Reduction is the only remedy** — the old net-red jurisdiction: every remedy must remove or simplify. Fewer concepts, fewer mechanisms, fewer branches, fewer lines, in that order, measured by the structure gate. Writing code is permitted *as a means*: the two-line replacement of a fourteen-line mechanism, the one general path that dissolves three special cases, the smaller closure of an excision's hole. What is out of scope: anything net-additive (new capability, new abstraction, provisions for the future), and the whole-design blind rebuild — that is `/refactor`'s organ, and rebuild-sized gaps go on the handoff list, sketched.
3. **Isolation is the safety.** Fresh branch `refactor-delete/<slug>` (worktree when asked or conventional). One abbreviated checkpoint, then autonomous. The deliverable is the branch and its report; merging is the operator's call.

## Workflow

```
0. ISOLATE    branch refactor-delete/<slug> from HEAD
1. BASELINE   census (symbols, clusters, counts); abbreviated checkpoint:
              stakes, hard floors, operator probes — NO requirements menu;
              harness = behavior-level tests + smoke + probes (a full
              differential oracle only when stakes demand it)
2. STRIP      loop to fixpoint: passes → excision → gates; fresh
              swe-refactor-deleter per pass until a pass yields nothing
3. REPORT     machine before → after; kills by pass; restorations; the
              handoff list (what deletion could not reach); side memo
```

### 1. Baseline

**Census.** Inventory every declared symbol and mechanism regardless of filename (LSP, ctags, reading); cluster parallel machinery; count concepts, mechanisms, code lines. Collection may fan out; clustering and counts run in one context over the merged inventory.

**The abbreviated checkpoint.** Three questions, one interaction: *what happens if this breaks?* and *who maintains it?* (stakes, recorded verbatim — they calibrate aggression and harness depth); **hard floors** — mechanisms that survive regardless, no argument; **probes** — custom verification steps that join the harness. There is no requirements docket: nothing will be rebuilt, so nothing needs ratifying.

**The harness.** Default: the existing behavior-level tests (partition them from structure-pinning tests as `/refactor` does; ambiguous is behavior-level), a headless smoke run, and the operator's probes. Escalate to a full differential oracle (original implementation as reference, diffed at the user-visible boundary) only when the stakes answer demands it or the strip docket turns out residue-heavy — deletions in the pass tier carry evidence that rarely needs an oracle to check. The harness, once chosen, is never weakened.

### 2. Strip — to fixpoint

Spawn `swe-refactor-deleter` — fresh instance per pass, assigned stance, net-red jurisdiction (strips, plus REPLACE proposals where a strictly smaller in-place substitute is sketchable). It sweeps **pass-major** with tool-derived evidence: dead-code elimination (references; coverage where instrumented), copy propagation (forwarding bodies, aliases, mirrors), inlining (trivial pipe nodes only), constant folding (single-valued parameters and config), CSE (census clusters — only where a copy dies and callers repoint without new abstraction), branch simplification (arms never taken; conditions that never vary); judgment spent on the residue (unreachable-input guards, write-only state, speculative generality, self-created hazards). Passes cascade — a folded constant decides a branch, the dead arm orphans a function — so loop with a fresh hunter until a pass proposes nothing that survives.

**Excision protocol**, per strip: root first, compiler-guided — delete the declaration and let diagnostics enumerate the cascade (orphans are bonus kills, same batch). **The suture rule, net-red form**: every hole closes with *less* machine than died — the constant returned, the expression forwarded, nothing, or a strictly smaller written closure; a hole whose smallest closure is not smaller than what it replaces means this strip is out of scope — withdraw it to the handoff list. **The part dies whole**: its structure-pinning tests, comments, config knobs, observers, and one-line doc amendments ride the same atomic commit (`refactor:` prefix, one concept and its cascade per batch).

**Replacements.** The hunter's naive-baseline sketches are executable here when small: a mechanism whose sketched substitute is a few lines is **replaced in place** — install the sketch, run the gates, one atomic commit like any strip. The structure gate is the arbiter of "smaller" (concepts and declarations before lines; density never degrades), and behavior holds as ever. Sketches beyond in-place scale — a design change, a data-structure change, anything touching multiple mechanisms at once — go to the handoff list; the line between a replacement and a rebuild is whether the surrounding design absorbs it unchanged.

**The gates — mechanical, per batch:**

1. **Behavior**: harness green. Divergence law: a difference no realistic input can produce is a discovered kill (log it); a reachable one fails the batch — restore, no discussion.
2. **Correctness**: `swe-correctness-reviewer` on the batch diff. Exhaustiveness demoted to a default case, and deleted compile-time assertions, are regressions even when behavior matches today.
3. **Structure**: orchestrator-measured — the machine must shrink and **density must not degrade** (max/median function length within the champion's neighborhood and the house register); no-caller-no-export sweep rides along. Self-reported numbers are never inputs.

The orchestrator is a clerk, not a judge: batches pass gates or are restored; neither outcome is argued.

### 3. Report

```
## Refactor Delete Complete
### Isolation: branch refactor-delete/<slug> @ <sha> (base <sha>)
### The machine: concepts C0 → C1 | mechanisms M0 → M1 | code lines L0 → L1
### Kills by pass: DCE n / copy-prop n / inline n / const-fold n / CSE n / branch n / residue n
### Replacements installed: n (net −L lines, −M mechanisms)
### Restored by the gates: n (each with the gate that fired)
### Passes run: N (terminated by clean pass | cap)
### Harness: [suite+smoke+probes | full oracle] — final state green
### Handoff list — what deletion could not reach, for /refactor:
###   [mechanism — naive-baseline delta — the sketch, in one line]
###   [withdrawn sutures — holes that needed new machinery]
### Side memo: [bugs and missing capabilities found and not touched]
### Docs amended: [file: one-line change]
### Merge: the operator's call
```

The **handoff list is a first-class deliverable**, not an apology: it is `/refactor`'s regeneration priority list, pre-computed. A run that strips 15% and hands over three well-sketched rebuild targets has done both skills' reconnaissance.

## Guardrails

- **Hard floors are never stripped.** The harness is never weakened. Behavior at the boundary never changes.
- **No net additions, ever.** Code is written only in service of a measured reduction, and the structure gate verifies the reduction per batch. The moment a remedy grows the machine — or exists for the future — it belongs elsewhere.
- **Not golf**: density is policed by the structure gate; inlining is confined to trivial bodies.
- **Version-controlled files only**; one concept per atomic commit; the side memo catches bugs (the harness pins today's behavior, bugs included — a silent fix is a divergence).
- **The report is the conscience**: every kill names its pass and evidence; every restoration names its gate.

## Relationship to /refactor

Same deleter, same excision protocol, same gates — minus the requirements menu, the differential-oracle default, the minimizer, the finish pass, and the bequest. The dividing line is anchor, not authorship: this skill edits the design it can see, always downward; `/refactor` adds the blind whole-target rebuild that can reach a *different* design. If field runs show deletion capturing most of the value, `/refactor`'s scheduled regeneration should become a triggered one (fired by this skill's handoff list); if deletion alone plateaus well above `/refactor`'s results, the regeneration organ has earned its cost and this skill retires into being `/refactor`'s cheap first phase.
