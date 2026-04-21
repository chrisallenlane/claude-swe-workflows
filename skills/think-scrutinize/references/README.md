# /think-scrutinize - Devil's Advocate for Ideas

## Overview

The `/think-scrutinize` skill stress-tests an idea or plan before you commit to implementing it. It spawns critical skeptics from multiple angles (technical, economic, operational, etc.), pairs them with an advocate defending the idea, and produces a synthesized report of faults that survived cross-examination.

**Key properties:**
- Adversarial by design — critique meets defense meets counter-critique
- Good-faith on both sides — no strawmen, no desperate defense
- Lens-based scrutiny — different angles catch different faults
- Produces feedback only — no code, no tickets, no artifacts
- "No faults found" is an honest, valuable outcome

## When to Use

**Use `/think-scrutinize` for:**
- Reviewing a plan before starting implementation
- Pressure-testing a proposal before presenting it
- Pre-mortem analysis on significant decisions
- Surfacing objections that politeness or groupthink would suppress

**Don't use `/think-scrutinize` for:**
- Choosing between options (use `/think-deliberate`)
- Finding bugs in existing code (use `/bug-hunt` or `/review-security`)
- Implementing changes (this skill makes nothing — it's a consultant)
- Venting about a plan without a concrete idea to critique

**Rule of thumb:** If you want to know "what's wrong with this idea?" — use `/think-scrutinize`. If you want to know "which option is best?" — use `/think-deliberate`.

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ /think-scrutinize Workflow                                  │
└─────────────────────────────────────────────────────────────┘

 ┌──────────────────────────────────────────────┐
 │  1. RECEIVE THE IDEA                         │
 │  ────────────────────────────────────────    │
 │  • From context, document, or user input     │
 │  • Produce a written brief                   │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  2. FACT-FINDING                             │
 │  ────────────────────────────────────────    │
 │  • Goal, constraints, prior attempts         │
 │  • Stakeholders, scope boundaries            │
 │  • Angles of particular concern              │
 │  (Typically 3-5 clarifying questions)        │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  3. CHOOSE CRITICAL LENSES                   │
 │  ────────────────────────────────────────    │
 │  Technical / Economic / Operational /        │
 │  Adversarial-user / Security / Regulatory /  │
 │  Social / Temporal                           │
 │  (2-5 lenses typical)                        │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  4. SPAWN SKEPTICS (parallel)                │
 │  ────────────────────────────────────────    │
 │  One agent per lens                          │
 │  Each returns structured critique            │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  5. CONSOLIDATE CRITIQUES                    │
 │  ────────────────────────────────────────    │
 │  Deduplicate, preserve lens attribution      │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  6. ADVOCATE REBUTS                          │
 │  ────────────────────────────────────────    │
 │  Defends idea in good faith                  │
 │  Concedes real faults, refutes weak ones     │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  7. COUNTER-REBUTTAL (parallel)              │
 │  ────────────────────────────────────────    │
 │  Skeptics respond: concede/hold/refine   │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  8. SYNTHESIZE AND REPORT                    │
 │  ────────────────────────────────────────    │
 │  Findings: Stands / Refuted / Partial /      │
 │            Uncertain                         │
 │  Recommendation: Proceed / Adjust /          │
 │                  Rethink / Reject            │
 └──────────────────────────────────────────────┘
```

## Roles

| Role          | What they do                                                             |
|---------------|--------------------------------------------------------------------------|
| Judge (you)   | Capture idea, choose lenses, spawn agents, synthesize report             |
| Skeptics  | Critique the idea through assigned lenses (parallel)                     |
| Advocate      | Defends the idea in good faith — concedes real faults, refutes weak ones |

## Critical Lenses

The orchestrator selects lenses based on the idea's shape. Common lenses include:

| Lens               | Asks                                                  |
|--------------------|-------------------------------------------------------|
| Technical          | Does this work as engineered?                         |
| Economic           | Is the cost/benefit sound?                            |
| Operational        | Can this run day-to-day?                              |
| Adversarial-user   | How could users misuse this?                          |
| Security/trust     | What attack surface is created?                       |
| Regulatory/legal   | What compliance risks arise?                          |
| Social/org         | Will people adopt this? Political risks?              |
| Temporal           | Does this hold up over time?                          |

2-5 lenses is typical. You may nominate specific angles when invoking the skill.

## Output

A structured report with:
- **Findings That Stand** — faults that survived rebuttal
- **Load-Bearing Assumptions** — things the idea depends on; verify them
- **Partial / Uncertain** — narrowed concerns, user judgment items
- **Refuted** — for completeness; shows the exchange was honest
- **Strengths** — where the idea held up
- **Recommendation** — Proceed / Proceed with adjustments / Rethink / Reject

## Iteration

The skill is **one-shot by design**. If the report suggests revision, refine your idea and re-invoke. Each invocation is a clean consultation — not an open-ended conversation. This keeps the skill composable and avoids the anti-pattern of endless "one more round" dialogs that dilute signal.

## Example Session

```
> /think-scrutinize Let's scrutinize our plan to migrate the session
  store from Postgres to Redis.

Before I spawn skeptics, let me confirm my understanding:

Idea brief:
- Move session data (user sessions, CSRF tokens, rate-limit counters)
  from Postgres to Redis
- Postgres remains for durable data
- Goal: reduce session-read latency and offload session writes

Is that accurate?
> Yes.

A few clarifying questions:
- What's the current session-read p99 latency, and what's the target?
- How long should sessions persist? (Redis defaults to volatile; do you
  need RDB/AOF persistence?)
- Do any regulatory requirements touch session data (PCI, HIPAA)?
- Who owns Redis operationally? Same team, or a platform team?
> p99 150ms → target <20ms. 30-day TTL. No regulatory concerns.
  Platform team owns Redis.

Lenses I'll apply: technical, operational, temporal, adversarial-user.
Skipping regulatory (no relevant compliance scope) and economic
(infrastructure cost is not in scope per the plan).

[Spawning 4 skeptics in parallel...]
[Consolidating critiques...]
[Spawning advocate to rebut...]
[Skeptics counter-rebutting in parallel...]

## Scrutinization Report

Idea: Migrate session store from Postgres to Redis
Lenses applied: technical, operational, temporal, adversarial-user

### Findings That Stand

- **[operational]** Redis AOF/RDB recovery is slower than Postgres point-in-time
  recovery. In a disaster, session loss is recoverable from Redis backup, but
  the time-to-restore during an incident could exceed current SLA.
  Addresses: define explicit DR runbook and RTO target before migration.

- **[adversarial-user]** Session TTL of 30 days in Redis means revoked sessions
  cannot be invalidated by DB mutation (as in Postgres). Need an explicit
  revocation mechanism — either short TTLs + refresh, or a revocation set.
  Addresses: design the session revocation path as part of the migration.

### Load-Bearing Assumptions to Validate

- Platform team has capacity to own another critical Redis instance
- Redis latency improvements hold under real workload (not just synthetic)

### Refuted

- [temporal] "Redis won't scale to projected 2-year growth" — advocate cited
  Redis Cluster sizing and your current size. Concern conceded.

### Strengths

- Technical fit is solid — session data is naturally key-value and TTL-friendly
- Migration strategy (dual-write with cutover) is well-understood
- Current Postgres session-write load is a documented bottleneck

### Recommendation
**Proceed with adjustments** — design the revocation path and DR runbook
before cutover.
```

## Relationship to Other Skills

| Skill                | Relationship                                                                                   |
|----------------------|------------------------------------------------------------------------------------------------|
| `/think-deliberate`  | Chooses between N options; `/think-scrutinize` stress-tests 1 idea. Same adversarial pattern.  |
| `/scope`             | If the idea should proceed, translates it into a ticket                                        |
| `/bug-hunt`          | Points at existing code; `/think-scrutinize` points at ideas                                   |
| `/review-security`   | Points at existing code; `/think-scrutinize` points at ideas                                   |

## Philosophy

Inspired by Charlie Munger's adaptation of Jacobi: **"Invert, always invert."** Before committing to an idea, understand how it could fail. The skill formalizes this instinct — not as unstructured doubt, but as adversarial stress-testing with honest synthesis.

A good skeptic finds the faults that matter, not the most faults. A good advocate defends honestly, not desperately. What emerges is the truth the idea needs to hear before it becomes code, tickets, or commitments.
