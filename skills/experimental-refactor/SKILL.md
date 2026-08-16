---
name: experimental-refactor
description: "EXPERIMENTAL — unshipped, unregistered, may be promoted or killed. Adversarial stakes-calibrated simplification run as a docket: a biased prosecutor indicts every file, an evidence-bound defense contests what it can actually win, and judgment is priced to the contest — summary judgment for the uncontested, deliberation for the genuinely disputed. Net-RED diffs in source only (tests may grow); behavior preserved against an inviolable behavior-level harness. Run only on projects whose owner has declared the stakes."
model: opus
---

# Experimental Refactor — The Adversarial Docket

> **EXPERIMENTAL.** Lives on a branch, appears in no catalog, and carries authority no shipped skill has. Second design. The first — a neutral scanner asked to convict against a taxonomy — under-destroyed in every cycle: its misses were deference failures, a judge hedging toward KEEP because criticizing the codebase it was handed is the socially penalized move. This design removes the hedge by **assigning the stance**: a prosecutor is *told* the code is over-built and ordered to say why, and calibration moves downstream into a defense and a bench that hold every indictment to an evidentiary standard. Bias the generator; judge neutrally; price the judgment to the contest.

## Identity

**This skill destroys.** It simplifies a codebase to the simplest representation that preserves behavior *at the declared stakes*. Three rules define it:

1. **Net-red diffs in source, per commit. Always.** Tests and ADRs may grow; `src/` may only shrink. This rule also bounds the prosecution: an indictment whose remedy would add machinery is outside its jurisdiction by construction — the bias cannot express the armor ratchet.
2. **Cross-module authority.** Pass 1 indicts within files; pass 2 indicts the boundaries themselves. Only region-external behavior and the behavior harness are fixed.
3. **Armor below the stakes line dies, including its defenses.** Enforcement mechanisms, their guard specs, and their warning comments are removed together.

What it is NOT: it never changes observable behavior (requirement trades are `/review-value`'s), never weakens the behavior harness, and never runs without a stakes declaration.

## Workflow

```
0. STAKES       elicit and pin the stakes declaration — the standard every
                verdict cites
1. HARNESS      partition specs: behavior-level (inviolable) vs
                internals-pinning (mutable)
2. INDICT       swe-prosecutor, per file, boundaries frozen: mandatory
                class-tagged indictments (ARMOR/BUG/DEAD) + side memo
3. DOCKET       route by class and resolve:
                  ARMOR → swe-defense-counsel triage →
                          waived: SUMMARY JUDGMENT (strip)
                          contested: BENCH RULING on the brief's evidence
                          genuinely disputed: DELIBERATION (THK - Advocate ×2)
                          coin-flip after deliberation: OPERATOR
                  BUG   → reproduce (failing test) or drop
                  DEAD  → reference evidence or drop
4. PRESENT      one batch approval: verdict sheet by disposition + side memo;
                operator strikes items or approves; then autonomy
5. DESTROY      strikes + regenerations; test bequests; doc amendments
6. VERIFY       harness green → spec-failure classification → correctness
                gate → net-red check (revert on failure)
7. PASS 2       prosecutor at architecture level (regions) → same docket →
                destroy/verify
8. REPORT       metrics, ledger, docket stats; specimen autopsy invitation
```

### 0. Stakes Declaration

Elicit before touching anything, and record verbatim in the run ledger:

- What happens if this breaks? (money / users / a laugh on stream / nothing)
- Who maintains it, and for how long?
- The embarrassment threshold — what would the owner not want a peer to read?
- **Hard floors** — named mechanisms that survive regardless ("determinism stays"). Floors are automatic defense wins; the prosecution may still indict them, and the brief is one line.

No declaration, no run. The declaration is the prosecutor's briefing, the defense's standard, and the bench's law — it is the entire difference between this skill and vandalism.

### 1. The Harness Partition

Classify every spec file before any destruction: **behavior-level** (observable outputs, user-visible behavior, end-to-end flows, determinism digests) vs **internals-pinning** (module APIs, internal structure, mechanism presence, directory rules). The behavior set plus a headless smoke run is the harness — **inviolable, never weakened, and never reclassified after a conviction to make a diff pass.** Internals-pinning specs are mutable and die with the armor they pin, each deletion logged. Ambiguous specs are behavior-level.

### 2. The Indictment Pass

Spawn `swe-prosecutor` with the stakes declaration verbatim. It operates under an assigned fiction — every file was written by a stakes-miscalibrated junior predecessor; state the error and prescribe the fix — with one jurisdictional bound: **every remedy must remove or simplify.** Defects whose fix would add code land in a side memo for the operator, never in the docket. Every file receives at least one indictment; there is no clean-file verdict, because the docket downstream absorbs wrongful indictments cheaply. The prosecutor tags each indictment ARMOR, BUG, or DEAD, and ships the naive-baseline sketch (ARMOR), reproduction sketch (BUG), or search trace (DEAD) that the class's standard will demand.

Parallelize freely — indictment is per-file and embarrassingly parallel.

### 3. The Docket

Three classes, three evidentiary standards, judgment priced to the contest:

**ARMOR** — the judgment class, and the only one that reaches the defense. `swe-defense-counsel` triages the full ARMOR list against the stakes declaration and splits it:

- **Waived** → **summary judgment**: straight to the strip pile. No trial for the export mirror nobody will defend — most indictments end here, and building a tribunal for them would be this skill committing its own crime.
- **Contested** → **bench ruling**: the orchestrator verifies the brief's evidence (the cited doc §, the demonstrated null-implementation failure, the attribution claim) and rules. Decisive evidence one way or the other ends it: KEEP, STRIP, STRIP-WITH-BEQUEST, or ROUTE to `/review-value`.
- **Genuinely disputed** — verified evidence on both sides — → **deliberation**: spawn two `THK - Advocate` instances, one assigned the indictment, one assigned the brief, both given the stakes declaration. The orchestrator judges on the merits against the stakes, never on rhetoric.
- **Still a coin-flip** → **operator escalation**. This is the taste-oracle call, and it should be rare — a handful per run, each a one-sentence ruling.

**BUG** — no deliberation; the standard is **reproduce or drop**. Write the failing test from the prosecutor's repro sketch. Test fails → the fix proceeds (its remedy already passed the net-red jurisdiction). Test passes → the charge is dismissed; if the test is independently valuable, keep it (tests may grow).

**DEAD** — no deliberation; the standard is **reference evidence**: grep/LSP confirmation at the confidence discipline `/review-dead` uses, calibrated against the codebase's dynamic-dispatch patterns. Confirmed → strip. Unconfirmed → dismissed.

### 4. One Batch Approval

Present the resolved verdict sheet to the operator **once**: summary judgments (count and list), bench rulings with the test each brief won or lost, deliberation verdicts, escalations awaiting rulings, BUG/DEAD outcomes, the side memo, and — highlighted — every strip that touches a design-doc- or ADR-cited mechanism, since those documents made promises the strip unmakes. The operator strikes items or approves the batch; after approval the skill runs autonomously to completion.

### 5. Destroy

**Strikes** (mechanical): the summary-judgment and ruled-STRIP pile — ceremony, mirrors, dead code, comment-register violations (rationale worth keeping → `adr/` behind a one-line pointer), constant consolidation. Direct implementation or SME per `/refactor`'s dispatch table.

**Regenerations** (design-level, mostly pass 2): each region goes to `swe-simplifier` with a *region packet* — the external boundary as the frozen public surface, the behavior-level specs that pin it, the prosecutor's naive-baseline sketch as design seed, the stakes declaration, house style, and the region's code-line count as budget. **Packets are provenance-filtered**: only design-doc, stakes, and decision-recording-ADR constraints enter; in-file assertions and sibling-precedent constraints are laundering, and a packet that carries them rebuilds the armor they defend.

**The test bequest.** Every STRIP-WITH-BEQUEST disposition ships its one behavior-level test in the same commit as the strip. Importance licenses a test; only expense licenses machinery — the bequest converts each dead tower of armor into a single line of durable vigilance.

**Doc amendments ride along:** every stripped doc-cited mechanism updates its citing document in the same commit — one line, past tense — so no document keeps promising machinery that no longer exists, and no future agent faithfully rebuilds it.

### 6. Verify — four gates, in order

1. **Harness green.** Behavior specs, digests, smoke.
2. **Spec-failure classification.** Expected failures classified against the step-1 partition — behavior-level ⇒ fix or revert; internals-pinning ⇒ delete with the armor, logged. The partition is binding; no re-litigating to rescue a diff.
3. **Correctness gate.** `swe-correctness-reviewer` on the diff (it carries the proportionality counterweight — it will not demand the armor back). Findings resolved or region reverted; 3-failure discipline as in `/refactor`.
4. **Net-red check.** `scc`-style code lines, comments excluded from both sides. Source not smaller ⇒ revert, log as declined.

### 8. Report

```
## Experimental Refactor Complete
### Stakes declaration: [verbatim]
### Source: N → M code lines (−X%) | comment ratio: A → B (target band 0.2–0.6)
### Docket: I indictments (A armor / B bug / D dead) → W waived, C contested,
###   R bench rulings, L deliberations, E operator escalations
###   defense record: [briefs won / lost — the counsel's calibration, tracked]
### Deletions ledger: [per commit: what died, indictment cited, red lines]
### Test bequests: [each invariant and its one test]
### Doc amendments: [file: one-line change] | design-doc-cited strips highlighted
### Internals specs removed: N (logged) | behavior specs: untouched, all green
### Kept: [each with the defense test that won it]
### Side memo: [add-shaped defects and /review-value routings, for the operator]
```

## The Specimen Autopsy — how this skill converges

Reruns under an unchanged configuration saturate. The loop that converges is **specimen → autopsy → organ diagnosis → rerun**, with the operator as fault oracle. After each run, invite specimens: surviving code that still offends the operator. For each, run the autopsy (strip the comments and judge naked; provenance-check claimed requirements; price survivors with the free-invariant test; sketch the naive baseline; trace defended failure modes to their origin), then diagnose **which organ failed**:

- **The prosecution never indicted it** → recall gap: add the specimen's pattern to the prosecutor's rap sheet.
- **The defense won a brief it shouldn't have** → tighten the defense test that carried it (most laundering hides in provenance and attribution).
- **The bench misruled** → adjust the ruling standard in this file.

Commit the organ fix to this branch and rerun. The prosecutor's rap sheet and the defense's tests are the learned artifacts; convergence is the operator failing to find a specimen.

## Guardrails

- **Behavior changes are the andon cord.** A simplification that cannot preserve behavior at the declared stakes stops and surfaces — that trade belongs to the operator via `/review-value`.
- **Hard floors are never stripped**, however confident the prosecution.
- **The bias stays in the prosecution.** The defense, the bench, the deliberation judge, and every verify gate are neutral; if prosecutor language leaks into a verdict's reasoning ("the junior clearly..."), the verdict is rewritten from the evidence.
- **House style applies to what remains**: the ~500-line ceiling, the narrative comment register, ontology-respecting placement. The telos ladder (fewer concepts > mechanisms > branches > lines) governs regenerations exactly as in `/refactor`'s generative stage.
- **The ledger is the deliverable's conscience.** Every deletion lists its indictment and disposition; the operator audits the run by reading it, not by diffing blind.

## Relationship to Shipped Skills

`/refactor` (even at Maximum) preserves guardrails, module contracts, and internals-pinning specs — it polishes within the walls. This skill tests whether the walls are armor. It reuses `THK - Advocate` for deliberations without touching `/think-deliberate` itself, and hands BUG-class dismissals' useful tests to the suite like `/bug-hunt` would. If the experiment succeeds — sloc/comment-ratio movement, harness integrity, the owner's felt "easy to reason about" — the docket architecture and stakes intake are candidates for promotion into `/refactor` mainline; the assigned-stance prosecution and mutable-spec grant may stay experimental forever, and that would be a valid outcome too.
