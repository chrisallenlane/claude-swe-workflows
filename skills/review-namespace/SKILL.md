---
name: review-namespace
description: Empirical namespace-legibility review. Measures how well a file tree communicates by running navigation probes against cold readers who see only the listing, then reports mispredictions as evidence-backed findings. An optional heavy search mode iterates hypothetical trees against the probe battery until legibility converges. Advisory only — produces findings, candidate trees, and proposed tickets; never moves a file.
model: opus
---

# Namespace Review — Measured Legibility

Measures whether a codebase is organized so a reader can *reason about it* — not by analyzing the tree, but by testing it: cold reader agents receive only the file listing and answer "which file would you open first for task X?" against ground truth the skill has verified in the actual code. **Advisory only.** Audit mode reports where the tree deceives its readers; search mode additionally evolves hypothetical trees against the battery and proposes the champion as a migration ticket. No file is ever moved.

## Philosophy

**Measure, don't argue.** Taxonomy debates ("should knight live in sim or own its namespace?") are traditionally settled by taste and seniority. This skill settles them by experiment: propose both, probe both, count the mispredictions. The probes need only a *listing*, so hypothetical restructures are cheap to test even though they are expensive to perform — taxonomy search becomes offline.

**Fresh eyes are a renewable resource.** A human team cannot summon unlimited naive readers; agents can be summoned per question. "Easy to reason about" stops being a feeling and becomes cold-reader task performance: can a newcomer predict what the app does from `ls`? Do they open the right file first try? Every finding carries that evidence.

**Trees are for humans; specs are for machines.** Technical boundaries (purity, dependency direction) are real, but they belong to tests, not to the directory layout. When the most legible tree crosses a technical boundary, the resolution is a reachability spec over the import graph, not a less legible tree. (See the house-style ontology amendment.)

**The owner is the calibration standard, used sparingly.** Reader pools are a proxy for the maintainer. A pool primed with the project's style guide is a *validated* proxy — in field trials, primed readers came to reproduce the maintainer's exact misses — but the maintainer's own small self-tests and vetoes outrank any score, and human testing fatigues fast (~10 questions), so the owner is consulted briefly and rarely.

## Laws of the Instrument

Field-derived rules; the skill applies all of them:

1. **Pre-register scoring before reading any answers.** Exact file = 1.0; right directory, wrong file = 0.5; for value-change questions, the value-store file and the mechanism file both count as correct first opens; a plausible-but-wrong value store earns 0.5. Rules may be refined per project, but always *before* grading.
2. **Ground truth is pinned by a sighted pass, per question, before anyone is graded.** Questions that lack a defensible single answer are dropped, and the drop is recorded.
3. **Measure the noise floor before comparing trees.** Run the battery twice on the same tree; the between-run delta bounds what any later difference must clear.
4. **Score per-question paired, not aggregate.** Aggregates saturate (ceiling effects); the signal lives in which questions flipped between trees.
5. **Every rename is re-probed for what it newly attracts.** Fixes create traps: a rename that cures one question's miss routinely steals a neighboring question. Keep the neighbors in the bank.
6. **Universal mispredictions are placement problems.** When every reader in every tree misses the same location, stop renaming and move the code to where they all look.
7. **Moves beat renames after repeated failure.** A location that fails probes under multiple names doesn't need a better name; it needs a different home.
8. **Confident-unanimous-wrong is the severity ceiling.** A miss the readers agree on at high confidence means the tree actively misleads; unsure-wrong merely fails to help.
9. **The canary leads.** The haiku-class reader degrades first on vague names and scores highest on genuinely legible trees; weight its movement.

## Mode Selection

Ask the operator (or accept from the invocation):

- **Audit** (default) — one probe battery against the actual tree; findings and proposed tickets. Moderate cost (~10-15 agents).
- **Search** — the full evolutionary loop over hypothetical trees. Heavy by design (several reader fleets per round, typically 3-5 rounds; budget in the millions of tokens). Confirm the operator wants this before starting; elicit a round cap (default 4).

## Audit Mode

```
1. Discover purpose docs      README, DESIGN, specs — the behavior inventory
2. Generate probes BLIND      writer agent reads ONLY purpose docs, never src/
3. Pin ground truth           sighted orchestrator greps; drop unpinnables;
                              pre-register scoring rules
4. Run the reader fleet       ≥3 cold readers (readers + canary), listing inline;
                              PLUS a style-primed pool when a style guide exists
5. Optional extra batteries   ls-test (predict the app from the tree alone);
                              reverse-navigation (place stripped file contents)
6. Score and classify         severity by unanimity × confidence
7. Present findings           evidence = the readers' own answers and rationales
8. Offer tickets              per references/advisory-tickets.md
```

**Step 2 — blind probe generation.** Spawn a general-purpose agent instructed to read ONLY the project's purpose documents (design doc, README, user docs — named explicitly; no directory listings, no source). It writes 15-25 navigation-task questions grounded in described behavior, spread across all major areas, never mentioning file or directory names. Blindness is the point: questions must come from behavior space, not from knowledge of the tree's traps.

**Step 4 — the reader fleet.** Spawn `swe-namespace-reader` (×2) and `swe-namespace-canary` (×1) with the file listing and questions pasted inline — never a repository path. When the project declares a style guide (e.g. conventions in CLAUDE.md), run a second pool of the same shape with the guide's decomposition/naming rules as a conventions preamble: this pool proxies the maintainer.

**Step 6 — finding classes.**

- *Deceptive location* — unanimous confident miss. The worst class; the tree sends readers to the wrong place with conviction.
- *Placement problem* — universal misprediction across readers and pools. Recommend moving the code, not renaming (Law 6).
- *Attractor trap* — a name that steals questions belonging elsewhere.
- *Homonym tax* — one word meaning different things across namespaces, measured by cross-routing.
- *One-hop conventions* — systematic half-misses (e.g., model/draw coin-flips). Report, usually accept: bounded cost.
- *Blind spots* — behaviors readers cannot place at all (from the ls-test's "can't locate" section).

## Search Mode

Runs the audit first (round 0 = the incumbent's baseline + noise floor: battery ×2, Law 3), then loops:

```
1. PROPOSE     candidates = tree + old→new mapping (a tree without a mapping
               is not actionable). Round 1 seeds diverse organizing lenses —
               the house-style/ontology lens always among them; later rounds
               mutate the champion from reader rationales on training misses
2. GATE        a sighted feasibility agent checks each mapping against the real
               dependency structure and technical boundaries. Boundary
               conflicts resolve by PROPOSING A REACHABILITY SPEC (the
               boundary moves to a test), never by silently bending the tree
               back toward runtime contracts; the trade is surfaced either way.
               Infeasible candidates are disqualified with reasons — which are
               themselves findings
3. PIN         examiner re-pins ground truth per candidate via its mapping;
               each round's bank adds fresh questions oversampling the regions
               the candidates changed (static banks ceiling out), while keeping
               the neighbors of every rename (Law 5)
4. PROBE       both pools against every candidate and the incumbent champion
5. SELECT      per-question paired wins clearing the noise floor (Law 4);
               canary movement weighted (Law 9)
6. CALIBRATE   present the champion to the operator: structural vetoes and
               comments are RULINGS that outrank scores; offer (never require)
               a short self-test — 5-6 fresh questions, hard fatigue cap of 10,
               ground truth pinned only after the operator answers
7. CONVERGE    champion unbeaten for 2 rounds, operator satisfied, or round
               cap reached. Expect the endgame residue to be conventions and
               content-level decisions, not structure — that is what converged
               looks like
```

**Output:** the champion tree, its complete old→new mapping, any reachability-spec designs, the code-level moves the probes voted for (consistent misses against a coherent tree are refactoring advice — code that doesn't match the ontology its tree advertises), and the probe dossier as evidence. On operator approval, a migration ticket per `references/advisory-tickets.md` — the ticket must be workable without this conversation: tree, mapping table (including deliberately-kept files, so nothing is "helpfully" renamed), spec changes, sequencing, acceptance criteria.

## Completion Summary

```
## Namespace Review Complete
### Mode: audit | search (N rounds)
### Battery: N questions (M dropped as unpinnable), pools: vanilla / primed
### Scores: [per tree × pool, with noise floor; per-question flips for search]
### Findings: N by class (deceptive / placement / attractor / homonym / one-hop / blind-spot)
### Champion (search mode): [tree summary + margin vs incumbent]
### Tickets: [#s] | none — findings stand as planning artifact
```

## Agent Coordination

`swe-namespace-reader` / `swe-namespace-canary` — fresh instances per battery, listing inline, never given a repository path. General-purpose spawns for the blind probe-writer, feasibility gate, and (optionally) candidate proposers. The orchestrator itself is the *examiner* — it pins ground truth with greps and holds the scoring rules, because grading judgment must stay consistent across rounds.

## Abort Conditions

**Abort:** operator interrupt; probe-writer produces unusably vague questions after one retry; tracker unavailable after ticket approval (surface the approved set for manual creation).

**Do NOT abort for:** a high-scoring tree (honest "already legible" is a valid audit outcome — report the score and the residue); search mode failing to beat the incumbent (that IS the result: the incumbent is validated, with evidence).

## Integration with Other Skills

**vs `/review-arch`:** `/review-arch` analyzes structure (noun frequency, blueprints — the analyst's view); `/review-namespace` *tests* it (reader task performance — the user study). They can disagree; when they do, prefer the measurement. The catalog's longer-term direction is `/review-arch` as a wrapper dispatching this skill plus a stack-tier review; until then they run independently.

**Excluded from `/lead-review`'s pipeline:** audit mode overlaps `/review-arch`'s in-pipeline noun analysis, and search mode's operator-calibration checkpoints (vetoes, self-tests) cannot be answered by an autonomous orchestrator. Run it deliberately.

**Feeds `/refactor` and `/implement-batch`:** the migration ticket routes there; this skill never mutates the tree itself.
