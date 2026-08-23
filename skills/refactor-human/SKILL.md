---
name: refactor-human
description: "EXPERIMENTAL — unshipped, unregistered, may be promoted or killed. Refactors a codebase for the human who must understand and change it. A reader advocate (dx-reviewer) learns the codebase as a newcomer, walks a fixed comprehension spine, and files findings; the skill turns them into a work order and executes with full authority — moving, renaming, re-namespacing, redesigning, rewriting from scratch — on an isolated branch or worktree. Its only constraint: observable behavior, as pinned at startup, does not change."
model: opus
---

# Refactor Human — The Reader's Refactor

> **EXPERIMENTAL.** Lives on a branch, appears in no catalog. Where `/refactor` asks *is this code clean?*, this skill asks *will the next human understand this?* — and reshapes. It is patterned on the `UX - Reviewer` proceeding, which has proven effective by walking a fixed spine with evidence rather than taste — here the "user" is the maintainer and the "interface" is the codebase.

## Identity

**This skill reshapes.** It optimizes one thing: how quickly and how correctly a competent newcomer can understand and safely change the code. Three rules define it:

1. **Behavior is the only constraint.** The public behavioral contract is pinned at startup and held by an inviolable harness. Everything else — file layout, namespaces, module boundaries, internal APIs, names, the implementation itself — is the skill's to change.
2. **Full authority, no anchoring.** It does not improve the existing design; it asks what design a reader would find clear, and builds that. Rewriting from scratch is a first-class remedy, executed blind to the current implementation so the old shape cannot anchor the new one.
3. **Isolation is the safety.** It always works on a fresh branch (default) or worktree (when asked, or when the repository's convention is worktrees). The deliverable is that branch plus a report; merging is the operator's decision. Because a bad run costs a `git branch -D`, the skill runs autonomously once the contract is pinned.

What it is NOT: it is not net-red (it may add a signpost, a split, a test, a name, when that buys comprehension), it never changes observable behavior, and it never weakens the harness.

## Workflow

```
0. CONTRACT     pin the public behavioral contract by target type; partition
                the specs into behavior-level (inviolable) vs structure-pinning
                (move with the code)
1. ISOLATE      branch `refactor-human/<slug>` from HEAD, or a worktree
2. REVIEW       dx-reviewer: think-aloud + seven-concern spine → findings,
                verdict
3. PLAN         findings → work order, three remedy kinds, ordered:
                  STRUCTURE  tree + old→new mapping (moves, renames,
                             re-namespacing), feasibility-gated
                  REWRITE    units regenerated blind from contract + the
                             confusions to dissolve
                  SIGNPOST   local edits: names, splits, pointers, comment
                             register, ADR extraction
4. EXECUTE      structure first, then rewrites inside the new structure, then
                signposts; structure-pinning specs move/rename with the code
5. VERIFY       harness green → spec-failure classification → correctness gate
                (revert the remedy on failure; no net-red gate — this skill
                is not that skill)
6. RE-REVIEW    dx-reviewer fresh think-aloud; loop 3-6 until APPROVED,
                stalemate, or round cap (default 3)
7. MEASURE      optional: /review-namespace audit battery on the incumbent
                vs. the result — reader task performance before/after
8. REPORT       branch, findings ledger, mapping table, rewrites, what the
                next reader should read first; merge is the operator's call
```

### 0. The Contract

"Full authority" ends exactly where observable behavior begins, and where that line falls depends on what the code is. Pin it before anything else, record it in the run ledger, and escalate (altitude rule) only if it is genuinely ambiguous:

| Target type    | Public behavioral contract (inviolable)                                  | Fair game                                                  |
|----------------|---------------------------------------------------------------------------|------------------------------------------------------------|
| CLI            | Commands, flags, exit codes, stdout/stderr shape, config file format       | Everything behind the arg parser                           |
| Library / API  | Exported symbols, signatures, documented semantics, error types            | Internal modules; undocumented internals                   |
| Service / web  | Routes, request/response shapes, persisted formats, auth behavior          | Handlers' internals, module layout, service boundaries     |
| Game / sim     | Player-visible behavior, save/replay formats, determinism digests          | Module layout, sim internals, the sim/render seam's shape  |
| MCP server     | Tool names, schemas, response shapes                                       | Everything behind the dispatcher                           |

Then partition every spec file: **behavior-level** (exercises the contract above; end-to-end, digests, smoke) vs **structure-pinning** (imports a module path, asserts an internal API, checks a directory rule). The behavior set plus a headless smoke run is the harness — inviolable, never weakened, never reclassified mid-run. Structure-pinning specs are *not deleted*: they move and rename with the code they pin, and are rewritten against the new structure. Ambiguous specs are behavior-level.

### 1. Isolate

`git switch -c refactor-human/<slug>` from the current HEAD (slug = date or the operator's label). Use a worktree instead when the operator asks, or when the repository's convention is worktrees (existing `git worktree list` entries, a `.worktrees/` dir, or a CLAUDE.md rule) — then `git worktree add`. Record which, and where, in the ledger and the report.

### 2. Review

Spawn `dx-reviewer` with the repository path, the purpose documents named explicitly, and the pinned contract. It learns the codebase in newcomer order — docs, `ls` predictions, the main path, navigation tasks, local-readability probes — then walks the spine. Its think-aloud log is the evidence behind every finding; its verdict and severities drive the loop.

### 3. Plan — the work order

Convert findings into remedies. Every finding gets exactly one disposition; the ledger records it:

- **STRUCTURE** — placement and naming findings (mental-model fit, orientation, coherence at the tree level) become a candidate tree with a complete old→new mapping, including deliberately-kept files. Gate it for feasibility against the real dependency graph. When the most legible tree crosses a technical boundary (purity, dependency direction), the boundary becomes a reachability spec — *trees are for humans, specs are for machines* — never a less legible tree.
- **REWRITE** — units whose confusion is in their design, not their placement (a mechanism the reader cannot model; a function unreadable without five others). The unit goes to a **blind rewriter** — a fresh implementer agent (general-purpose, or the language SME per `/refactor`'s dispatch table) that is forbidden from reading the current unit or its history — with a packet: the unit's external contract as used, the behavior-level specs that pin it, binding constraints (ADR, design doc — provenance-filtered, never in-file assertions), house style, and *the confusions to dissolve* stated in design terms, never as code.
- **SIGNPOST** — everything local: a rename, a file split at the ceiling, a module header, a one-line pointer to the ADR that justifies deliberate structure, comment-register fixes, a magic value named, a unified term.
- **`[CONTRACT]`-tagged findings** — the remedy would change observable behavior. Not executed. Listed in the report for `/review-value` or the operator.
- **Declined** — concerns/suggestions the orchestrator judges acceptable here, with the one-line reason (the reviewer sees these on re-review).

Order: structure → rewrite → signpost. Rewrites happen inside the new tree so they are not redone; signposts last because moves and rewrites make many of them moot.

### 4. Execute

**Structure:** `git mv` preserving history; imports updated (LSP rename where the language has it); structure-pinning specs moved and rewritten alongside. One commit per coherent move group.

**Rewrite:** the blind rewriter never sees the current implementation — not the file, not its history; if the packet is insufficient it says what is missing rather than peeking. It returns a design note, the implementation, expected spec results, and any confusion it could not dissolve without touching the contract. The orchestrator installs it and verifies.

**Signpost:** direct edits or SME per `/refactor`'s dispatch table. Rationale worth keeping goes to `adr/` behind a one-line pointer; the rest of an essay header is deleted.

### 5. Verify — three gates, in order

1. **Harness green.** Behavior specs, digests, smoke.
2. **Spec-failure classification.** Against the step-0 partition: behavior-level ⇒ fix or revert the remedy; structure-pinning ⇒ rewrite the spec to the new structure, logged. The partition is binding.
3. **Correctness gate.** `swe-correctness-reviewer` on the diff; findings resolved or the remedy reverted; 3-failure discipline as in `/refactor`.

No net-red gate, no line budget. The measure is the re-review.

### 6. Re-review

Spawn `dx-reviewer` fresh with the changed tree and the ledger's responses. It re-runs the think-aloud (fixes create new traps — a rename that cures one miss steals a neighbor). Loop to step 3 with its new findings until **APPROVED**, **stalemate** (same blockers recurring, responses not converging → escalate with pre-loaded options per `references/autonomy.md`), or the round cap (default 3; elicit at startup).

### 7. Measure (optional)

If the operator wants a number: run `/review-namespace`'s audit battery against the incumbent tree (from the base commit) and the result, same question bank, same reader pools. Paired per-question wins clearing the noise floor are the before/after; the canary leads. This is the only objective instrument the program has for "easy to reason about," and it costs ~10-15 agents per tree.

### 8. Report

```
## Refactor Human Complete
### Isolation: branch refactor-human/<slug> @ <sha> (base <sha>) | worktree <path>
### Contract: [target type; the pinned public contract, verbatim]
### Rounds: N | final verdict: APPROVED | stalemate (escalated) | cap reached
### Findings: B blockers / C concerns / S suggestions →
###   structure M, rewrite R, signpost P, declined D, [CONTRACT] routed X
### Mapping table: [old → new, every moved file; kept files listed]
### Rewrites: [unit: confusions dissolved; design note one-liner]
### Specs: behavior-level untouched, all green | structure-pinning rewritten: N
### Measurement (if run): [per-pool score before → after; flips; noise floor]
### Read this first: [the path the next maintainer should follow — the
###   report's one sentence of orientation for a human]
### Merge: the operator's call — `git merge` / PR / `git branch -D`
```

## Guardrails

- **Behavior is the andon cord.** A remedy that cannot preserve the pinned contract stops and routes to the report; it is never forced through.
- **The harness is never weakened or reclassified** to rescue a remedy.
- **No anchoring.** The reviewer asks what a newcomer would find clear, not whether the current shape has a reason; the rewriter works blind. Deliberate structure is checked against `adr/` before it is reshaped — and if it is justified *and* confusing, the remedy is a signpost, not a dissolution.
- **Autonomous after the contract.** Isolation makes the run cheap to discard; mid-run approval would only add the ceremony this skill removes. Escalations follow `references/autonomy.md`: contract ambiguity at startup, stalemate at the end, nothing in between.
- **The ledger is the conscience.** Every finding has a disposition and every move a mapping row; the operator audits the branch by reading the ledger, then the diff.
