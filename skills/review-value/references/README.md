# /review-value - Value-Engineering Review

## Overview

The `/review-value` skill applies **value engineering** — the discipline of attributing cost to function and asking whether a cheaper function would serve (Lawrence Miles, General Electric, 1947) — to a codebase. It discovers the project's requirements, attributes implementation cost to the requirements that force it, and presents a **trade menu**: small, concrete behavior relaxations that would dissolve disproportionate machinery.

It is **advisory only**, and more strongly so than the other `/review-*` skills: its findings are *product decisions*. The skill prices behavior; only the product owner may trade it.

**Key benefits:**
- The pipeline's one descoping voice — every other skill treats requirements as fixed input that only accretes
- Works without a design document — requirements are discovered across provenance tiers, not assumed
- Trades name concrete user-visible deltas a product owner can rule on, not vague "simplification opportunities"
- Approved trades amend the requirement's record *first*, so the machinery doesn't get faithfully rebuilt later
- Chains ahead of `/review-arch` and `/refactor`: delete requirements before polishing their implementations

## When to Use

**Use `/review-value` when:**
- A codebase feels far heavier than the product it delivers
- You suspect edge-case guarantees, unshipped features, or uniformity commitments are carrying disproportionate cost
- Before a major refactoring campaign — descoping first shrinks the work
- A design document exists but you suspect it over-commits (or has drifted from reality)

**Don't use it for:**
- Behavior-preserving cleanup (`/refactor`)
- Structural reorganization within fixed behavior (`/review-arch`)
- Machinery that serves *no* requirement — that's `/review-arch`'s mechanism audit; this skill prices machinery that serves a *real but expensive* requirement

**Rule of thumb:** if the question is "is this built right?", use another review. If the question is "should this be built at all, or built to a weaker promise?", use this one.

## The Provenance Tiers

Requirements are discovered, not assumed, because not every project has a design document — and documents drift. Each requirement is tagged with where it was found, and the tier determines what an approved trade must change:

| Tier       | Found in                                                    | Approving a trade means…                     |
| ---------- | ----------------------------------------------------------- | -------------------------------------------- |
| Documented | Design docs, ADRs, README promises, user docs, CLI help     | Amending the document                        |
| Pinned     | Test-suite assertions (specs are executable requirements)   | Amending the spec                            |
| Inferred   | Observed behavior nothing records; presumed intentional     | Confirming intent (and recording it, ADR)    |

Inferred requirements get Chesterton's-fence respect but are the cheapest trades — the operator may simply confirm the behavior was never wanted. Where a documented requirement and observed behavior disagree, the drift itself is reported: one of the two is wrong, and either may be the keeper.

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ /review-value Workflow (advisory value engineering)      │
└─────────────────────────────────────────────────────────────────┘

 ┌──────────────────────────────────────────────┐
 │  1. DETERMINE SCOPE & GATHER CONTEXT         │
 │  • Whole codebase or caller-specified        │
 │  • Mechanism audit / operator suspicions     │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  2. ANALYZE                                  │
 │  Agent: swe-value-engineer (fresh instance)  │
 │  • Discover requirements (3 provenance tiers)│
 │  • Attribute cost (requirement-down, mass-up)│
 │  • Trace requirement chains to their roots   │
 │  • Generate trades, ranked by leverage       │
 │                                              │
 │  Honest zero? → COMPLETION SUMMARY           │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  3. PRESENT THE TRADE MENU                   │
 ├──────────────────────────────────────────────┤
 │  4. OPERATOR RULES ON EACH TRADE             │
 │  • Product decisions — approve/decline/defer │
 │  • Skill answers from evidence; no advocacy  │
 ├──────────────────────────────────────────────┤
 │  5. OFFER TO CUT TICKETS (approved trades)   │
 │  • First AC: amend the requirement's record  │
 │  • Then: dissolve the machinery              │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  6. COMPLETION SUMMARY                       │
 └──────────────────────────────────────────────┘
```

## The Trade Format

Every trade names:

- **Current commitment** — the requirement, with provenance and source
- **Proposed relaxation** — the weaker commitment
- **User-visible delta** — a concrete scenario ("the viewer who orders on the exact final tick sees no acknowledgement"), decidable by a product owner; "slightly different behavior" is not a finding
- **Machinery dissolved** — cited files/mechanisms, including the whole chain when the requirement forces one (design choice → compensating mechanism → defenses of the compensation)
- **Estimated savings** — presented as estimates, spot-checkable via the citations
- **Category flags** — core-requirement / correctness / security trades are labeled so nobody mistakes the menu for a recommendation

## Tips for Effective Use

1. **Run it before refactoring campaigns, not after.** Compressing the implementation of a requirement you then delete is wasted work. The natural chain: `/review-value` → approved dissolutions land → `/review-arch` → `/refactor`.

2. **Feed it a mechanism audit.** A recent `/review-arch` run's mechanism audit ("keep — serves requirement X") is pre-computed cost attribution; pass it in step 1.

3. **The amendment-first acceptance criterion is not bureaucracy.** An approved trade that only deletes code leaves the old requirement on the books, and the next agent to read it will faithfully rebuild the machinery.

4. **Declining every trade is a fine outcome.** The priced menu is itself the product — you now know what your commitments cost, which is information you didn't have.

5. **Watch the drift observations.** A documented requirement the implementation no longer honors is a decision waiting to be made in either direction — enforce it or strike it.

6. **Orchestrators: this skill is excluded from `/lead-review`.** Its output is product decisions an autonomous pipeline cannot rule on. Run it with the product owner present.

## Agent Coordination

**Single agent invocation.** The skill spawns `swe-value-engineer` once per invocation. No SME agents (no implementation), no QA agents (no changes to verify).

**State maintained by the skill:** scope, the trade menu, per-trade rulings, tickets created.

## Abort Conditions

**Abort:** analysis agent fails after one retry; operator interrupts; tracker unavailable after ticket approval (surface the approved set for manual creation).

**Do NOT abort for:** an honest-zero menu, or the operator declining every trade — both are valid outcomes.

## Philosophy

**Every requirement has a price, and nobody else audits the price list.** Design docs, specs, and observed behavior only accrete; implementation pipelines treat them as fixed input. Value engineering is the counter-discipline: attribute the cost, name the trade, let the owner decide.

**Price, don't advocate.** The menu is a price list, not a sales pitch. The skill's credibility rests on honest estimates, concrete deltas, and a willingness to report that nothing is worth trading.

**Behavior belongs to the product owner.** The skill never changes code, specs, or documents — not because caution is a virtue in itself, but because a behavior trade decided by an implementation pipeline is a product decision made by nobody.
