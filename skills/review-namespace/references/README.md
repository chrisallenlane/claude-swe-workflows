# /review-namespace - Measured Namespace Legibility

## Overview

The `/review-namespace` skill measures how well a file tree communicates — not by analyzing it, but by *testing* it: cold reader agents receive only the file listing (pasted inline, no repository access) and answer navigation questions ("which file would you open first for task X?") scored against ground truth the skill verifies in the actual code. It is **advisory only**: audit mode reports where the tree deceives readers; search mode evolves hypothetical trees against the battery and proposes the champion as a migration ticket. No file is ever moved.

**Key benefits:**
- "Easy to reason about" becomes a measurement, not a debate — taxonomy arguments are settled by counting mispredictions
- Hypothetical restructures are testable at full fidelity from the listing alone: taxonomy search is *offline*, so you test dozens of restructures and perform one
- A style-primed reader pool proxies the maintainer (in field trials it converged to reproducing the maintainer's exact misses)
- Findings carry built-in evidence: the readers' own wrong answers and their reasoning
- Consistent misses against a coherent tree double as *refactoring advice* — code that doesn't match the ontology its tree advertises

## The Method in One Paragraph

A blind writer (who reads only the design doc/README, never the source) generates behavior-grounded navigation questions. The orchestrator — the *examiner* — pins each question's ground truth with greps, drops unpinnable questions, and pre-registers scoring rules (exact = 1.0, right-directory = 0.5, value-store leniency) before reading any answers. Reader fleets (sonnet readers + a haiku canary; a second pool primed with the project's style guide) answer from the listing alone. Misses are classified and reported; in search mode, candidate trees (each with an old→new mapping) are gated for feasibility, probed with fresh questions oversampling changed regions, selected by per-question paired wins clearing a measured noise floor, and mutated from reader rationales until convergence.

## The Laws of the Instrument

Field-derived, all enforced by the skill:

| # | Law |
|---|-----|
| 1 | Pre-register scoring rules before reading any answers |
| 2 | Pin ground truth sighted, per question, before grading; drop and record unpinnables |
| 3 | Measure the noise floor (battery ×2, same tree) before comparing trees |
| 4 | Score per-question paired, not aggregate — aggregates saturate |
| 5 | Re-probe every rename for what it *newly* attracts; keep renamed files' semantic neighbors in the bank |
| 6 | Universal mispredictions are placement problems — move the code, don't rename it |
| 7 | Moves beat renames after repeated probe failure |
| 8 | Confident-unanimous-wrong is the severity ceiling |
| 9 | The canary (haiku reader) degrades first on vague names — weight its movement |

## Finding Classes

- **Deceptive location** — unanimous confident miss; the tree sends readers somewhere wrong with conviction
- **Placement problem** — every reader in every pool misses the same location (Law 6)
- **Attractor trap** — a name that steals questions belonging to a neighbor
- **Homonym tax** — one word meaning different things across namespaces
- **One-hop convention** — systematic half-misses (model/draw coin-flips); bounded cost, usually accepted
- **Blind spot** — behavior no reader can place at all

## When to Use

**Audit mode:**
- The codebase "works but doesn't feel easy to reason about" and you want the feeling converted into a ranked, evidenced worklist
- After a restructure, to verify it actually helped
- Before onboarding (human or agent) — the findings are exactly what newcomers will trip on

**Search mode:**
- You want the *optimal* tree, not just a critique — and will pay for it (reader fleets × candidates × rounds; budget in the millions of tokens)
- A restructure is planned anyway, and testing five hypothetical trees is cheaper than performing one wrong one

**Don't use it for:**
- Structural analysis without measurement (`/review-arch`)
- Mechanism/stack appropriateness (`/review-arch`'s mechanism audit, `/review-value`)
- Actually moving files (`/refactor`, `/implement` — fed by this skill's tickets)

## The Owner Calibration Loop (search mode)

Reader pools are proxies for the maintainer; the maintainer is the standard. Each round's champion is presented for **vetoes and comments, which are rulings that outrank scores**. A short self-test is *offered*, never required: 5-6 fresh questions, hard cap of 10 (human probe-fatigue is real), ground truth pinned only after the owner answers so nothing leaks. Owner misses are findings about the tree; owner comments about namespaces that "feel wrong" are next-round design input. Expect convergence to look like: the owner's misses and the primed pool's misses become the same misses, scores plateau, and the residue is conventions (model-vs-draw coin flips) and content-level decisions rather than structure.

## Boundaries and Feasibility

The most legible tree often wants to cross technical boundaries (pure simulation code beside draw code, when both belong to the same entity). The skill's rule — *trees are for humans, specs are for machines* — resolves this by proposing a **reachability spec**: the boundary is enforced as a test over the import graph's transitive closure rather than as a directory wall. The feasibility gate (a sighted agent checking each candidate's mapping against real dependencies) surfaces the trade explicitly; it never silently bends the tree back toward runtime contracts, and it disqualifies genuinely unimplementable mappings with reasons that are themselves findings.

## Abort Conditions

**Abort:** operator interrupt; unusably vague probe generation after one retry; tracker unavailable after ticket approval (surface the approved set for manual creation).

**Do NOT abort for:** a high-scoring tree (honest "already legible" is a valid outcome), or search mode failing to beat the incumbent — that result *validates* the incumbent, with evidence.

## Cost Expectations

Audit: ~10-15 agents (probe writer, two 3-reader pools, optional extra batteries). Search: several fleets per round across candidates and pools, typically 3-5 rounds — millions of tokens. The skill states this at mode selection; search runs only on explicit operator opt-in with a round cap.

## Integration

- **`/review-arch`** — the analyst's view (noun frequency, blueprints) vs this skill's user study. When they disagree, prefer the measurement. Longer-term catalog direction: `/review-arch` becomes a wrapper dispatching this skill plus a stack-tier review.
- **Excluded from `/lead-review`** — audit overlaps `/review-arch`'s in-pipeline analysis, and search mode's owner-calibration checkpoints cannot be answered by an autonomous orchestrator.
- **`/refactor` / `/implement`** — execute the migration ticket this skill proposes.
