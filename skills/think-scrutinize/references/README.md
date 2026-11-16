# /think-scrutinize - Devil's Advocate for Ideas

## Overview

`/think-scrutinize` stress-tests a single idea or plan before you commit to it. Skeptics critique it in isolation, each through a different lens. An advocate defends it, conceding real faults and refuting weak ones, and the skeptics answer the defense. The report keeps only what survived that exchange.

It counters confirmation bias: people stop looking for faults in an idea they already like. The method is adversarial steelmanning from the rationalist tradition, in the spirit of Munger's borrowing from Jacobi, "Invert, always invert." It uses the same adversarial pattern as `/think-deliberate`, pointed inward at one idea instead of across competing options. The namespace-wide rationale lives in [`references/think.md`](../../../references/think.md).

The step-by-step procedure lives in [`SKILL.md`](../SKILL.md); this guide covers when to use the skill and what to expect.

"No faults found" is a legitimate result. The skill produces feedback only: no code, no tickets, no artifacts.

## When to Use

**Use `/think-scrutinize` for:**
- Reviewing a plan or design before starting implementation
- Pressure-testing a proposal before presenting it to stakeholders
- Surfacing objections that politeness or groupthink would suppress
- Stress-testing mitigations or assumptions surfaced by `/think-premortem`

**Don't use `/think-scrutinize` for:**
- Choosing between options (use `/think-deliberate`)
- Sweeping a plan's whole failure space (use `/think-premortem`; run it first, then scrutinize what it surfaces)
- Finding bugs in existing code (use `/bug-hunt` or `/review-security`)
- Implementing changes (this skill makes nothing; follow up with `/scope` or `/implement`)
- Vague dissatisfaction with a plan that has no concrete form yet

**Rule of thumb:** "What's wrong with this idea?" → `/think-scrutinize`. "Which option is best?" → `/think-deliberate`.

**Natural pipeline:** `/think-brainstorm` → `/think-deliberate` → `/think-scrutinize` → `/scope` (generate → choose → stress-test → specify).

## Flow

```
Receive idea → Fact-finding (with you) → Choose lenses → Skeptics (parallel, isolated)
  → Consolidate → Advocate defends → Skeptics counter-rebut → Synthesize → Report
```

**Fact-finding is interactive.** Expect three to five questions about the goal, constraints, prior attempts, stakeholders, and scope. You'll also be asked which angles you want scrutinized hardest, and your nominations become lenses.

## Critical Lenses

The skill picks the lenses where the idea plausibly has weaknesses, typically 2–5, and skips those that don't apply.

| Lens             | Asks                                     |
| ---------------- | ---------------------------------------- |
| Technical        | Does this work as engineered?            |
| Economic         | Is the cost/benefit sound?               |
| Operational      | Can this run day-to-day?                 |
| Adversarial-user | How could users misuse this?             |
| Security/trust   | What attack surface is created?          |
| Regulatory/legal | What compliance risks arise?             |
| Social/org       | Will people adopt this? Political risks? |
| Temporal         | Does this hold up over time?             |

## What You Get Back

Each finding gets a verdict: **stands**, **refuted**, **partial** (narrowed but not eliminated), or **uncertain** (needs your judgment). The report has:

- **Findings That Stand**: faults that survived rebuttal
- **Load-Bearing Assumptions to Validate**: what the idea depends on; verify these
- **Partial / Uncertain**
- **Findings That Were Refuted**: brief, to show the exchange was two-sided
- **Strengths**: where the idea held up
- **Recommendation**: Proceed / Proceed with adjustments / Rethink / Reject

The skill is one-shot. Revise the idea and re-invoke rather than extending the exchange.

## Example Session

```
> /think-scrutinize Let's scrutinize our plan to migrate the session
  store from Postgres to Redis.

Idea brief: move sessions, CSRF tokens, and rate-limit counters to Redis;
Postgres keeps durable data; goal is lower session-read latency.

- Current p99 and target? Session lifetime? Regulatory scope? Who owns Redis?
> p99 150ms → target <20ms. 30-day TTL. No regulatory concerns.
  Platform team owns Redis.

Lenses: technical, operational, temporal, adversarial-user. Skipping
regulatory (no compliance scope) and economic (cost out of scope).

## Scrutinization Report

### Findings That Stand

- **[adversarial-user]** With a 30-day TTL, revoked sessions can't be
  invalidated by a DB mutation as they can in Postgres. Needs an explicit
  revocation path: short TTLs + refresh, or a revocation set.

- **[operational]** Redis restore could exceed the current SLA during an
  incident. Define a DR runbook and RTO target before migrating.

### Load-Bearing Assumptions to Validate

- The platform team has capacity to own another critical Redis instance
- Latency gains hold under real workload, not just synthetic

### Findings That Were Refuted

- [temporal] "Redis won't scale to projected 2-year growth." The advocate
  cited Redis Cluster sizing against current size; the skeptic conceded.

### Strengths

- Session data is naturally key-value and TTL-friendly

### Recommendation

**Proceed with adjustments:** design the revocation path and DR runbook
before cutover.
```

The instructive part is the refuted finding. A plausible-sounding objection was dropped once the advocate answered it with evidence, so the findings that stand are the ones worth acting on.
