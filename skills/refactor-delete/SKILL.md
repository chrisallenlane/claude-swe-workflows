---
name: refactor-delete
description: "EXPERIMENTAL — unshipped, unregistered, may be promoted or killed. Reduction-only refactoring: a fixpoint strip loop — the classic optimizer passes as mechanical detectors, an excision protocol, and mechanical adjudication gates. Behavior never changes; every remedy must remove or simplify — code may be written only in service of a measured net reduction (a smaller in-place replacement, a general path dissolving special cases). Cheap by design: one abbreviated checkpoint (stakes, floors, probes), the existing behavior-level suite as the default harness. What reduction-in-place cannot reach is reported as sketched redesign candidates for the operator, never attempted."
model: opus
---

# Refactor Delete — Reduction Only

## Identity

**This skill only reduces.** Three rules:

1. **Behavior never changes.** Every change must be invisible at the user-visible boundary. The one nuance is inherited law: **the corpus defines behavior** — a guard on inputs the platform cannot send defends nothing observable, and removing it changes no behavior a realistic input can witness.
2. **Reduction is the only remedy** — the net-red jurisdiction: every remedy must remove or simplify. Fewer concepts, fewer mechanisms, fewer branches, fewer lines, in that order, measured by the structure gate. Writing code is permitted *as a means*: the two-line replacement of a fourteen-line mechanism, the one general path that dissolves three special cases, the smaller closure of an excision's hole. What is out of scope: anything net-additive (new capability, new abstraction, provisions for the future), and whole-design rebuilds — rebuild-sized gaps are reported on the handoff list as sketched redesign candidates for the operator, never attempted.
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
3. FINISH     swe-refactor-dx, one pass: local, human-facing tidying only
4. REPORT     machine before → after; kills by pass; restorations; the
              handoff list (what deletion could not reach); side memo
```

### 1. Baseline

**Census.** Inventory every declared symbol and mechanism regardless of filename (LSP, ctags, reading); cluster parallel machinery; count concepts, mechanisms, code lines. Collection may fan out; clustering and counts run in one context over the merged inventory.

**The abbreviated checkpoint.** Three questions, one interaction: *what happens if this breaks?* and *who maintains it?* (stakes, recorded verbatim — they calibrate aggression and harness depth); **hard floors** — mechanisms that survive regardless, no argument; **probes** — custom verification steps that join the harness. There is no requirements docket: nothing will be rebuilt, so nothing needs ratifying.

**The harness.** Default: the existing behavior-level tests — partition the suite first: *behavior-level* exercises what a user observes (outputs, flows, digests); *structure-pinning* imports a module path, asserts an internal API, or checks a directory rule; ambiguous is behavior-level — plus a headless smoke run and the operator's probes. Escalate to a full differential oracle (original implementation as reference, diffed at the user-visible boundary) only when the stakes answer demands it or the strip docket turns out residue-heavy — deletions in the pass tier carry evidence that rarely needs an oracle to check. The harness, once chosen, is never weakened.

### 2. Strip — to fixpoint

Spawn `swe-refactor-deleter` — fresh instance per pass, assigned stance, net-red jurisdiction (strips, plus REPLACE proposals where a strictly smaller in-place substitute is sketchable). It sweeps **pass-major** with tool-derived evidence: dead-code elimination (references; coverage where instrumented), copy propagation (forwarding bodies, aliases, mirrors), inlining (trivial pipe nodes only), constant folding (single-valued parameters and config), CSE (census clusters — only where a copy dies and callers repoint without new abstraction), branch simplification (arms never taken; conditions that never vary); judgment spent on the residue (unreachable-input guards, write-only state, speculative generality, self-created hazards). Passes cascade — a folded constant decides a branch, the dead arm orphans a function — so loop with a fresh hunter until a pass proposes nothing that survives.

**Excision protocol**, per strip: root first, compiler-guided — delete the declaration and let diagnostics enumerate the cascade (orphans are bonus kills, same batch). **The suture rule, net-red form**: every hole closes with *less* machine than died — the constant returned, the expression forwarded, nothing, or a strictly smaller written closure; a hole whose smallest closure is not smaller than what it replaces means this strip is out of scope — withdraw it to the handoff list. **The part dies whole**: its structure-pinning tests, comments, config knobs, observers, and one-line doc amendments ride the same atomic commit (`refactor:` prefix, one concept and its cascade per batch).

**Replacements.** The hunter's naive-baseline sketches are executable here when small: a mechanism whose sketched substitute is a few lines is **replaced in place** — install the sketch, run the gates, one atomic commit like any strip. The structure gate is the arbiter of "smaller" (concepts and declarations before lines; density never degrades), and behavior holds as ever. Sketches beyond in-place scale — a design change, a data-structure change, anything touching multiple mechanisms at once — go to the handoff list; the line between a replacement and a rebuild is whether the surrounding design absorbs it unchanged.

**The gates — mechanical, per batch:**

1. **Behavior**: harness green. Divergence law: a difference no realistic input can produce is a discovered kill (log it); a reachable one fails the batch — restore, no discussion.
2. **Correctness**: `swe-correctness-reviewer` on the batch diff. Exhaustiveness demoted to a default case, and deleted compile-time assertions, are regressions even when behavior matches today.
3. **Structure**: orchestrator-measured — the machine must shrink and **density must not degrade** (max/median function length within the champion's neighborhood and the house register); no-caller-no-export sweep rides along. Self-reported numbers are never inputs.

The orchestrator is a clerk, not a judge: batches pass gates or are restored; neither outcome is argued.

### 3. Finish — one pass for the human reader

Excision leaves scar tissue in the survivors: comments referencing dead parts, names sized for a neighborhood that shrank, a parameter gap where a folded constant was, a file reduced below coherence. The gates measure counts and density; nobody upstream has read the result *as a reader*. Spawn `swe-refactor-dx` for **a single finalizing pass** — think-aloud plus its concern spine — with remedies executed **local only**: a rename, a module header, a comment corrected or deleted, a file split or merged at the house ceiling, a magic value named. No structural moves, no rewrites; structural findings go to the report, untaken. After the edits, run the gates once — tidying is behavior-safe by intent, not by assumption.

### 4. Report

```
## Refactor Delete Complete
### Isolation: branch refactor-delete/<slug> @ <sha> (base <sha>)
### The machine: concepts C0 → C1 | mechanisms M0 → M1 | code lines L0 → L1
### Kills by pass: DCE n / copy-prop n / inline n / const-fold n / CSE n / branch n / residue n
### Replacements installed: n (net −L lines, −M mechanisms)
### Restored by the gates: n (each with the gate that fired)
### Passes run: N (terminated by clean pass | cap)
### Harness: [suite+smoke+probes | full oracle] — final state green
### Handoff list — what reduction-in-place could not reach (redesign candidates):
###   [mechanism — naive-baseline delta — the sketch, in one line]
###   [withdrawn sutures — holes that needed new machinery]
### Side memo: [bugs and missing capabilities found and not touched]
### Finish pass: F findings — L applied locally, R reported (structural, not taken)
### Docs amended: [file: one-line change]
### Merge: the operator's call
```

The **handoff list is a first-class deliverable**, not an apology: each entry is a sketched redesign candidate — the mechanism, its distance from the dumbest adequate design, the sketch in a line — for the operator to pursue by whatever means they choose. A run that strips 15% and reports three well-sketched candidates has also done the reconnaissance for whatever comes next.

## Guardrails

- **Hard floors are never stripped.** The harness is never weakened. Behavior at the boundary never changes.
- **No net additions, ever.** Code is written only in service of a measured reduction, and the structure gate verifies the reduction per batch. The moment a remedy grows the machine — or exists for the future — it belongs elsewhere.
- **Not golf**: density is policed by the structure gate; inlining is confined to trivial bodies.
- **Version-controlled files only**; one concept per atomic commit; the side memo catches bugs (the harness pins today's behavior, bugs included — a silent fix is a divergence).
- **The report is the conscience**: every kill names its pass and evidence; every restoration names its gate.
