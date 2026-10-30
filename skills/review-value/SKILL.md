---
name: review-value
description: Value-engineering review. Discovers a project's requirements across provenance tiers (documented, spec-pinned, inferred from behavior), attributes implementation cost to the requirements that force it, and presents a trade menu — small concrete behavior relaxations that dissolve disproportionate machinery. Advisory only — behavior changes are product decisions; proposes document amendments and tickets on operator approval.
model: opus
---

# Requirements Review — Value Engineering

Audits the *price list*: what each requirement costs to satisfy, and what a small behavior relaxation would save. **Advisory only.** The skill applies the value-engineering discipline (Miles, GE, 1947) — analyze each function the product commits to, ask what it costs, what else would serve, and what the alternative costs — and presents the result as a trade menu the operator rules on. Behavior is the product owner's property; this skill prices it and never changes it.

## Philosophy

**Every requirement has a price, and nobody else audits the price list.** Every other skill treats requirements as fixed input: the correctness gate enforces the spec, `/refactor` preserves behavior by definition, and `/review-arch`'s mechanism audit stops at "keep — serves requirement X" and salutes. After scoping ends, requirements only accrete. This skill is the pipeline's one descoping voice — the counterpart to `/scope`, which turns desired behavior into cost; this turns cost back into behavior options.

**The trade is the unit of output.** Each finding names a current commitment, a proposed relaxation, a *concrete* user-visible delta a product owner can rule on, the machinery that dissolves, and an estimated saving. "If we changed the behavior by 5%, we'd simplify the implementation by 85%" — with the files cited and the numbers presented as estimates.

**Requirements are discovered, not assumed.** Not every project has a design document, and design documents drift. The analysis agent discovers requirements from three provenance tiers — **documented** (design docs, ADRs, README promises, user docs), **pinned** (what the test suite asserts), and **inferred** (behavior the implementation exhibits that nothing records, presumed intentional per Chesterton's fence) — and the tier shapes the trade: renegotiate the document, amend the spec, or simply confirm the behavior was ever wanted at all.

**The document amendment is the real deliverable.** An approved trade that only changes code is a time bomb: the next agent to read the unamended requirement will faithfully rebuild the machinery. Amendment first, implementation second.

**Single workflow for everyone.** Human operator or orchestrator, the flow is the same: analysis → trade menu → operator rules on each trade → amendments and tickets for the approved ones. Because trades are product decisions, orchestrators should treat contested or high-leverage trades as andon-cord material rather than auto-approving — see [`references/autonomy.md`](../../references/autonomy.md).

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│      REQUIREMENTS REVIEW WORKFLOW (advisory value engineering)  │
├─────────────────────────────────────────────────────────────────┤
│  1. Determine scope and gather context                          │
│  2. Spawn swe-value-engineer agent                              │
│     → returns requirements inventory + ranked trade menu        │
│  3. Present the trade menu to the operator                      │
│  4. Operator rules on each trade (approve / decline / discuss)  │
│  5. For approved trades: offer to cut tickets                   │
│     ├─ Each ticket leads with the document/spec amendment       │
│     ├─ Operator approves / edits / declines the set             │
│     └─ Create approved tickets in tracker                       │
│  6. Completion summary                                          │
└─────────────────────────────────────────────────────────────────┘
```

## Workflow Details

### 1. Determine Scope and Gather Context

**Scope:** Default is the entire codebase. If the caller names a subsystem or module, respect that scope.

**Context worth passing to the agent when available:**
- A recent `/review-arch` mechanism audit — its `serves:` citations are pre-computed cost attribution.
- Operator suspicions ("the event system feels heavier than the product needs") — hypotheses to check, not conclusions to confirm.

### 2. Analyze

**Spawn a fresh `swe-value-engineer` agent** with the scope and any context from step 1:

```
Perform a value-engineering review of this codebase.
Scope: [entire codebase | caller-specified scope]
Context: [mechanism audit if available; operator suspicions if any]
Discover the requirements (documented / pinned / inferred), attribute
implementation cost to them, and return a trade menu ranked by leverage.
```

The agent returns a provenance-tagged requirements inventory, a ranked trade menu, drift observations (documented requirements vs. observed behavior), items deferred to other reviews, and an honest-zero statement if the menu is thin.

**If the agent reports honest zero:** workflow complete; skip to step 6.

### 3. Present the Trade Menu

Present the menu in full, ranked by leverage. For each trade the operator must be able to see, without asking follow-ups: the current commitment and its provenance, the proposed relaxation, the concrete user-visible delta, what dissolves, the estimated savings (as estimates), and any category flags (core-requirement, correctness, security).

Also present the drift observations — a documented requirement the implementation no longer honors is a decision waiting to be made in either direction.

### 4. Operator Rules on Each Trade

These are **product decisions** — the operator's judgment, not the skill's. Support the deliberation:

- Answer questions from evidence ("which files exactly?" — cite them).
- Adjust estimates if the operator's spot-check disagrees; say so plainly.
- Record each ruling: approved / declined / deferred.
- Never advocate. The menu is a price list, not a sales pitch. If asked for a recommendation, give one and label it as opinion.

When invoked by an orchestrator: trades flagged core-requirement, correctness, or security are andon-cord material — surface them to the human rather than ruling autonomously. Low-leverage unflagged trades may be declined autonomously per the orchestrator's own judgment.

### 5. Offer to Cut Tickets

For each **approved** trade, draft one ticket. **The amendment leads; the implementation follows:**

- **Title** — action-oriented, naming the relaxation (e.g., "Relax final-tick order rendering; remove per-record phase stamping").
- **Description** — the trade in full: old commitment, new commitment, user-visible delta, machinery to dissolve.
- **First acceptance criterion — amend the record.** The design doc section, ADR, README claim, or spec that carries the old requirement is updated to the new one. For *inferred* requirements: record the newly-confirmed intent wherever the project keeps such decisions (an ADR is the natural home).
- **Remaining acceptance criteria** — the dissolution: files/mechanisms removed, tests amended, suite green.
- **Recommended implementation skill** — typically `/implement` — per ticket, or with the chain's tickets together when approved trades share a chain.

Preview the set; the operator approves / edits / declines per the standard advisory pattern ([`references/advisory-tickets.md`](../../references/advisory-tickets.md)). On approval, create tickets via the canonical tracker integration ([`references/trackers.md`](../../references/trackers.md)).

**If the operator declines tickets:** valid outcome — the menu stands as a planning artifact.

### 6. Completion Summary

```
## Requirements Review Complete

### Scope
[Entire codebase | caller-specified]

### Statistics
- Requirements inventoried (cost-plausible): N
- Trades proposed: N (ranked by leverage)
- Trades approved: N | declined: N | deferred: N
- Drift observations: N

### Tickets created
- #131: Relax final-tick order rendering; remove phase stamping — /implement
- #132: Accept rare mutual kills; remove resolution-order machinery — /implement
(or: "No tickets created — menu stands as a planning artifact.")

### Recommended next steps
[e.g., "Run /review-arch after the approved dissolutions land — removing
requirements changes the blueprint. Then /refactor to shrink what remains."]
```

## Agent Coordination

- One `swe-value-engineer` agent per invocation, fresh instance.
- No SME or QA agents — the skill changes nothing.

**State to maintain (as orchestrator):** scope, the agent's menu, per-trade rulings, ticket URLs created.

## Abort Conditions

**Abort:** agent failure after one retry; operator interrupt; tracker unavailable after approval (surface the approved set so tickets can be created manually).

**Do NOT abort for:** an honest-zero menu (valid outcome — report and exit cleanly), or the operator declining every trade (the price list was the product).

## Integration with Other Skills

**`/review-value` vs `/review-arch`:** the mechanism audit prices machinery *within* fixed requirements ("does this heap serve a requirement?"); this skill prices the requirements themselves ("does that requirement earn its cost?"). Chain them: requirements first — compressing or restructuring the implementation of a requirement you're about to delete is wasted work.

**`/review-value` vs `/scope`:** inverses. `/scope` turns desired behavior into planned cost; this turns observed cost back into behavior options.

**Run by `/review-health`'s follow-up only when intent asks:** its output is product decisions, which an autonomous run cannot rule on. Run it deliberately, with the product owner present.

## Example Session

```
> /review-value

Scope: entire codebase
Spawning swe-value-engineer agent...

## Trade Menu (3 trades, ranked by leverage)

### Trade 1: Accept rare mutual kills
- Current: "a mutual kill is impossible" (Documented — DESIGN.md §4.3)
- Relaxation: simultaneous resolution; ties broken by seeded coin flip
- User-visible delta: ~once per hundreds of matches, two knights kill
  each other in the same tick and the coin decides placement
- Dissolves: sequential resolution order, per-tick shuffle, id-bias
  measurement and its specs (src/sim/combat.lua, ~6 spec files)
- Estimated savings: ~450 source lines, ~700 spec lines (estimates)
- Flags: none
- On approval: amend DESIGN.md §4.3

[Trades 2-3 elided]

> Approve 1 and 3. Decline 2 — that guarantee is the product.

Recorded. Cut tickets for trades 1 and 3?
> Yes.

### Ticket preview
1. Accept rare mutual kills; remove resolution-order machinery
   - AC 1: DESIGN.md §4.3 amended to the new commitment
   - AC 2: sequential-resolution machinery removed; suite green
   ...

Creating tickets... #131, #132 created.
```
