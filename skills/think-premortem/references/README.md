# /think-premortem - Prospective Failure Imagination

## Overview

The `/think-premortem` skill treats a catastrophic failure as already-having-happened and reasons backward to the causes. It operates in **two modes**:

- **Plan mode** — the user has a plan they have not yet committed to. Pre-mortemers imagine a catastrophic failure within their lens against the plan, broadly.
- **Scenario mode** — the user poses a specific catastrophic scenario against an existing system. Pre-mortemers investigate the actual code and architecture for causes that could have allowed the given scenario to occur.

In both modes, the skill spawns parallel pre-mortemers in isolation across failure-class lenses and synthesizes into a prioritized risk register paired with early-warning signals.

**Key properties:**

- Prospective-hindsight framing — pre-mortemers treat the failure as having *already happened*, not "could happen"
- Two modes — plan (broad imagination against a plan) and scenario (evidence-cited investigation against a system)
- Multiple failure-class lenses in parallel — technical, operational, estimation, scope, adoption, dependency-and-environment, team-and-coordination, incentive, detection, reversibility, adversarial
- Isolated generation — no anchoring across pre-mortemers (Nominal Group Technique)
- Qualitative calibration — *high / moderate / low / uncertain*, no fabricated percentages
- Output is a risk register prioritized by likelihood × impact, with early-warning signals
- Produces feedback only — no code, no tickets, no artifacts
- Natural handoff to `/think-scrutinize` (stress-test mitigations) or `/scope` (ticket the defendable failure modes)

## When to Use

**Use `/think-premortem` (plan mode) for:**

- Before committing to a plan, design, or significant decision
- Pre-flight check before invoking `/implement` on multi-week work
- Before merging a major architectural change
- Before announcing a deadline or rollout to stakeholders
- When a plan feels solid but residual unease remains — the unease often points at a real failure mode

**Use `/think-premortem` (scenario mode) for:**

- Hardening an existing system against a hypothetical catastrophe ("if a zero-day were used against us, how could it have happened?")
- Investigating worst-case scenarios for a deployed service before adversarial conditions actually materialize
- Stress-testing a system's hidden coupling, reversibility, or detection assumptions by imagining specific catastrophic outcomes
- Pre-incident-response preparation — surfacing what the on-call team would need if a named scenario hit

**Don't use `/think-premortem` for:**

- Plans too vague to fail concretely (refine first via `/scope` or `/think-brainstorm`)
- Currently-failing situations whose cause is unclear (use `/think-diagnose` — that skill handles real, observable failures with unknown causes; scenario-mode pre-mortem is for *hypothetical* catastrophes)
- Already-resolved incidents the user wants to learn from (use `/think-reflect`)
- Choosing between options (use `/think-deliberate`)
- Generating new approaches (use `/think-brainstorm`)

**Rule of thumb:**

- "What could go wrong with this plan?" → `/think-premortem` (plan mode)
- "If [catastrophe] hit our system, how could it have happened?" → `/think-premortem` (scenario mode)
- "What's wrong with this idea right now?" → `/think-scrutinize`
- "Why is this currently broken?" → `/think-diagnose`
- "What did this teach us?" → `/think-reflect`

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ /think-premortem Workflow                                   │
└─────────────────────────────────────────────────────────────┘

 ┌───────────────────────────────────────────────┐
 │  1. DETECT MODE + RECEIVE TARGET              │
 │  ───────────────────────────────────────────  │
 │  Plan mode: future-tense, plan/design         │
 │  Scenario mode: past-tense catastrophe        │
 │    against an existing system                 │
 │  Produce a written brief                      │
 │  Plan: what/why/when/who/where + horizon      │
 │  Scenario: scenario + scope + system context  │
 └──────────────────┬────────────────────────────┘
                    ▼
 ┌───────────────────────────────────────────────┐
 │  2. VALIDATE CONCRETENESS                     │
 │  ───────────────────────────────────────────  │
 │  Plan / scenario must be concrete enough to   │
 │  fail concretely. Push back on vague input.   │
 │  Plan: deliverable, timeframe, deps, criteria │
 │  Scenario: specific event, scoped target,     │
 │    mechanistically posable                    │
 └──────────────────┬────────────────────────────┘
                    ▼
 ┌───────────────────────────────────────────────┐
 │  3. CHOOSE LENSES (three categories)          │
 │  ───────────────────────────────────────────  │
 │  Standard (4-7): technical / operational /    │
 │    estimation / scope / adoption /            │
 │    dependency-and-environment / team-and-     │
 │    coordination / incentive / detection /     │
 │    reversibility / adversarial                │
 │  Ad-hoc target-specific (0-3): orchestrator   │
 │    names lenses unique to the target's        │
 │    domain (e.g., tenant-isolation)            │
 │  first-principles: always runs; catches       │
 │    failure modes the other lenses miss        │
 └──────────────────┬────────────────────────────┘
                    ▼
 ┌───────────────────────────────────────────────┐
 │  4. SPAWN PRE-MORTEMERS (parallel, isolated)  │
 │  ───────────────────────────────────────────  │
 │  One agent per lens                           │
 │  No cross-talk (NGT — avoids anchoring)       │
 │  Plan mode: imagine a failure within lens     │
 │  Scenario mode: investigate the actual        │
 │    system for causes of the given scenario    │
 │    (read code, cite file:line)                │
 └──────────────────┬────────────────────────────┘
                    ▼
 ┌───────────────────────────────────────────────┐
 │  5. SYNTHESIZE RISK REGISTER                  │
 │  ───────────────────────────────────────────  │
 │  • Cluster causes across lenses               │
 │  • Calibrate likelihood × impact qualitatively│
 │  • Identify early-warning signals             │
 │  • Distinguish defendable from monitor-only   │
 │  • Surface top 3-5 failure modes              │
 │  • Drop generic / weak findings               │
 └──────────────────┬────────────────────────────┘
                    ▼
 ┌───────────────────────────────────────────────┐
 │  6. REPORT                                    │
 │  ───────────────────────────────────────────  │
 │  Top Failure Modes (3-5, detailed) /          │
 │  Tabulated tail / Cross-cutting               │
 │  observations / Load-bearing assumptions /    │
 │  Lenses that found little / Suggested next    │
 │  steps                                        │
 └───────────────────────────────────────────────┘
```

## Roles

| Role          | What they do                                                                                                                              |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Judge (you)   | Detect mode, capture target, validate concreteness, choose lenses, synthesize the risk register                                           |
| Pre-mortemers | Plan mode: imagine catastrophic failure within an assigned lens. Scenario mode: investigate actual code for given scenario. In isolation. |

## Scenario Mode Is for *Hypothetical* Catastrophes

Scenario mode operates on catastrophes that have *not* occurred. The user uses prospective-hindsight framing as a stress-testing technique against a system that is currently fine.

If the catastrophe is *actually happening now* — symptoms observable, cause unclear — that is `/think-diagnose`'s territory (abductive reasoning to infer causes of an observed phenomenon). If the incident has *resolved* and the user wants to learn from it, that is `/think-reflect`. Scenario-mode pre-mortem sits between the two: imagine a catastrophe that *could* hit, and harden against it.

## Failure-Class Lenses

Pre-mortemers cover three categories of lens. The orchestrator selects from each:

### 1. Standard lenses (pick 4-7)

The 11 prescribed failure classes, available in every pre-mortem:

| Lens                       | Failure shape                                                               |
| -------------------------- | --------------------------------------------------------------------------- |
| technical                  | Implementation broke; design didn't survive contact with reality            |
| operational                | Couldn't deploy, observe, maintain, or sustain on-call                      |
| estimation                 | Took 3-5x longer; sandbagged assumptions; hidden complexity surfaced late   |
| scope                      | Built the wrong thing; problem moved while team built                       |
| adoption                   | Users didn't take it up; defected; found a workaround                       |
| dependency-and-environment | External factor changed (vendor, regulation, market, library)               |
| team-and-coordination      | Attrition, knowledge loss, blocked-on-someone, handoff breakdown            |
| incentive                  | Goodhart; system rewarded the wrong thing                                   |
| detection                  | Failure went unnoticed; instrumentation gap; silent corruption              |
| reversibility              | Couldn't roll back; sunk-cost trapped continuation                          |
| adversarial                | An actor exploited a weakness; trust assumption was load-bearing, unstated  |

4-7 standard lenses is typical. Drop lenses that don't fit — forcing an unfit lens produces noise. **For software projects, technical, operational, and estimation are almost always present.**

### 2. Ad-hoc target-specific lenses (0-3)

The orchestrator may add lenses tailored to the target's domain when the standard taxonomy doesn't cover a known class of failure cleanly. The orchestrator names the lens and provides a one-sentence definition; the pre-mortemer applies that definition.

Examples of ad-hoc lenses:

| Domain                  | Ad-hoc lens                 | Failure shape                                                                |
| ----------------------- | --------------------------- | ---------------------------------------------------------------------------- |
| ML system               | training-distribution-drift | Model performance degrades as input distribution diverges from training data |
| Multi-tenant SaaS       | tenant-isolation            | One tenant's actions affect another's correctness, performance, or privacy   |
| Real-time trading       | latency-and-jitter          | Timing variance produces correctness or ordering failures                    |
| Federated identity      | cross-domain-trust          | Trust propagation across boundaries amplifies a single compromise            |
| Compliance-bound system | regulatory-shift            | A regulation change retroactively invalidates compliant behavior             |

Add an ad-hoc lens when:

- The target's domain has a recognized class of failure that doesn't map cleanly to a standard lens
- A standard lens would technically cover it but would dilute focus by mixing it with unrelated concerns

If no ad-hoc lens is warranted, run zero. **The standard lenses + first-principles cover most cases.** Adding ad-hoc lenses for the sake of comprehensiveness dilutes the register.

### 3. The `first-principles` lens (always runs)

The free-form lens. Its job is to catch failure modes specific to *this* target that don't fit cleanly into any other lens being applied. Klein's original pre-mortem worked exactly this way — participants imagined freely without category constraints. The structured lens taxonomy is our addition for systematic coverage; the `first-principles` lens recovers what the taxonomy can miss.

The pre-mortemer assigned to `first-principles` is told which other lenses are being applied. Its job is to find failures *outside* their territory — modes that span multiple lenses, emerge from the target's unique architectural choices, or arise from interactions the structured lenses each touch separately.

Honest "nothing here that the other lenses don't already catch" is a valid, calibrated outcome from the `first-principles` lens. Manufactured findings dilute the register; the lens earns its slot when it surfaces something the prescribed taxonomy missed, not by always producing.

## Output

A prioritized risk register. Each headline failure mode carries a concrete past-tense failure scenario, its causes (with file:line evidence in scenario mode), qualitative likelihood and impact, early-warning signals, and a defendable / monitor-only label. The report sections are:

- **Top Failure Modes** (headline) — 3-5 detailed entries, each with scenario, causes, signals, calibration
- **Other Failure Modes Worth Tracking** — lower-priority entries in tabulated form
- **Cross-Cutting Observations** — patterns that emerged across multiple lenses
- **Load-Bearing Assumptions** — assumptions that, if false, invalidate the plan
- **Lenses That Found Little** — honest reporting where a chosen lens produced limited value
- **Suggested Next Steps** — natural follow-ups (`/think-scrutinize`, `/scope`, etc.)

The skill is **one-shot by design**: to pre-mortem a revised plan or a hardened system, re-invoke.

## Example Session (Plan Mode)

```
> /think-premortem We're planning to migrate our auth service from the legacy
  monolith to a new dedicated service over the next six weeks. Three engineers,
  with rolling deployment. Want to pre-mortem before kicking off.

Capturing the plan brief:
- Deliverable: dedicated auth service replacing the legacy monolith's auth path
- Timeframe: 6 weeks
- Team: 3 engineers
- Approach: rolling deployment
- Time horizon: 8 weeks from now — 2 weeks past the planned end
- Currently in: planning (pre-implementation)

A few questions before I spawn pre-mortemers:

1. What's the existing auth call volume / pattern? Any SSO, MFA, or
   federation involved?
> Mostly internal users; ~2k peak QPS. Standard email/password + TOTP MFA.
  We have one SAML SSO integration with a customer org.

2. Does anyone else read from the auth tables besides the auth path?
> Yes — billing reads user metadata; audit log writes to a shared
  events table.

3. What's the rollback story?
> We were planning to keep the legacy code path callable via feature flag
  for at least one cycle.

OK, the plan is concrete enough. Lenses I'll apply: technical, operational,
estimation, dependency-and-environment, detection, reversibility. Skipping
adoption (internal users, no choice), adversarial (deferred to a separate
security pass per the plan), incentive (no relevant measurement system),
team-and-coordination (small co-located team), scope (well-defined replacement).

[Spawning 6 pre-mortemers in parallel...]
[Collecting outputs...]
[Synthesizing...]

## Pre-Mortem Report

Plan: Migrate auth service from legacy monolith to dedicated service over 6 weeks
Lenses applied: technical, operational, estimation, dependency-and-environment,
                detection, reversibility
Time horizon: 8 weeks from now

### Top Failure Modes

1. **Silent SAML SSO breakage for the one customer org**
   *(lenses: technical, detection, dependency-and-environment)*
   - **Failure scenario:** Six weeks in, after the legacy code path was
     decommissioned, the customer's quarterly contract renewal triggered an
     unusual SAML re-handshake their IdP performs only on renewals. The new
     service handled the standard flow but not the renewal-time variant. The
     customer's users lost access for 14 hours before the team identified the
     issue and rolled back partially.
   - **Causes:** Test coverage for SAML focused on the common login flow. The
     renewal-handshake variant wasn't documented. The legacy implementation
     handled it implicitly; the new one didn't.
   - **Early-warning signals:** SAML-related code paths in the legacy service
     have unusual logging that the team didn't fully understand during planning.
     Discrepancies in handshake byte counts between legacy and new service
     during shadow traffic should be logged and inspected.
   - **Likelihood:** moderate — single customer, rare event, but high impact when it fires
   - **Impact:** high — customer-facing outage, contract risk
   - **Defendable / monitor-only:** Defendable. Run the new service in
     shadow mode against the customer for at least one full quarter cycle
     before decommissioning legacy.

2. **Billing-table coupling produces silent correctness drift**
   *(lenses: technical, detection)*
   - **Failure scenario:** Three weeks post-cutover, billing began producing
     subtly wrong invoices for a small fraction of users — those whose metadata
     was modified during the migration window. The new auth service's eventual
     consistency model differed from the monolith's transactional one; the
     billing read-path assumed transactional semantics.
   - **Causes:** The team treated billing's read path as out-of-scope. The
     consistency-model change wasn't surfaced.
   - **Early-warning signals:** Invoice exception rate begins drifting upward
     in a way that wouldn't be noticed without cross-checking against the
     prior baseline.
   - **Likelihood:** moderate
   - **Impact:** high — financial correctness, invisible until aggregated
   - **Defendable / monitor-only:** Defendable. Audit billing's read path
     before cutover; explicitly contract the consistency guarantees.

3. **Estimation: TOTP secret migration was harder than scoped**
   *(lenses: estimation, technical)*
   - **Failure scenario:** Week 4, the TOTP secret migration discovered that
     ~3% of users had legacy-format secrets that needed re-derivation. The
     re-derivation required a per-user notification flow that wasn't planned.
     Project added 3 weeks.
   - **Causes:** TOTP scope was estimated based on the documented schema, not
     the actual data distribution. Legacy artifacts in a long-running system.
   - **Early-warning signals:** A spike in support tickets during the first
     pilot cohort; or, more reliably, a careful audit of the actual TOTP
     secret schema before estimating.
   - **Likelihood:** high — long-running auth systems almost always have
     legacy data shapes
   - **Impact:** moderate — schedule slip, but recoverable
   - **Defendable / monitor-only:** Defendable. Run a data-shape audit on
     existing TOTP secrets in week 1, before locking the migration plan.

4. **Reversibility is shorter-lived than assumed**
   *(lenses: reversibility, operational)*
   - **Failure scenario:** Week 7, an issue was discovered. The legacy code
     path was technically still callable, but the team had stopped writing
     to one of its dependent caches. Falling back required a 2-hour manual
     warm-up and lost some session state.
   - **Causes:** The "feature flag for one cycle" plan didn't fully include
     the support systems the legacy path depended on. Reversibility has an
     attack surface, and the plan only protected the obvious entry point.
   - **Early-warning signals:** During implementation, decisions to "stop
     writing to X because the new system handles it" should be flagged
     as reversibility-narrowing decisions.
   - **Likelihood:** moderate
   - **Impact:** high — converts a recoverable bug into an outage
   - **Defendable / monitor-only:** Defendable. Maintain a rollback
     checklist; periodically test the rollback path during the migration.

### Other Failure Modes Worth Tracking

| Failure mode                                            | Lens          | Likelihood | Impact   | Early signal                                   |
|---------------------------------------------------------|---------------|------------|----------|------------------------------------------------|
| Audit-log shared events table schema drift              | technical     | low        | moderate | Audit log query failures during shadow phase   |
| 2k peak QPS turns out to be higher in practice          | operational   | low        | moderate | Latency degradation under load tests           |
| One engineer needs to take time off mid-project         | (out of lens) | low        | low      | n/a — plan has redundancy across 3 engineers   |

### Cross-Cutting Observations

- Three lenses (technical, detection, dependency-and-environment) all surfaced
  failure modes around the *non-obvious consumers* of the auth path — billing's
  read coupling, the customer SAML variant, the audit-log integration. Pattern:
  the team's mental model of "the auth path" is narrower than the actual surface.
  The defensible move is a consumer audit before cutover.

- Two lenses (technical, estimation) both flagged that legacy-data shape
  assumptions are likely wrong. Pattern: long-running systems accumulate data
  shapes that don't match the documented schema. A week-1 data-shape audit is
  the highest-leverage planning addition.

### Load-Bearing Assumptions

- TOTP secrets all conform to the documented format (likely false, see top failure mode #3)
- The legacy code path can be re-enabled safely after one cycle (likely false in detail, see #4)
- Billing's read coupling has the same consistency requirements as the legacy auth path provided (unverified)

### Lenses That Found Little

- (none — all 6 selected lenses produced material findings)

### Suggested Next Steps

- Run a data-shape audit on TOTP secrets in week 1 (defends against #3)
- Audit non-obvious auth-path consumers (billing, audit log, SAML variants) before cutover (defends against #1, #2, and the cross-cutting observation)
- Define rollback acceptance criteria and test the rollback path mid-migration (defends against #4)
- To stress-test the proposed mitigations: `/think-scrutinize`
- To turn the defendable items above into tickets: `/scope`
```

Scenario mode follows the same shape, with two differences: the brief pairs the posed scenario with a scoped target system and its context, and every cause in the report cites the code, configuration, or architecture that would have allowed it (file:line).

## Relationship to Other Skills

| Skill               | Relationship                                                                                                                                             |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/think-scrutinize` | Natural downstream — stress-test mitigations or load-bearing assumptions surfaced                                                                        |
| `/think-deliberate` | Natural downstream — choose between candidate mitigation / hardening approaches                                                                          |
| `/scope`            | Natural downstream — turn defendable failure modes into tickets                                                                                          |
| `/think-reflect`    | Matched pair on the time axis — pre-mortem ex-ante (hypothetical), reflect ex-post (resolved)                                                            |
| `/think-brainstorm` | Pre-mortem can identify the *problem* (failure modes); brainstorm generates *mitigations*                                                                |
| `/think-diagnose`   | Adjacent skill for *currently-occurring* failures with unknown causes; pre-mortem (scenario mode) is for *hypothetical* failures against running systems |

## Philosophy

The discipline is: imagine or investigate specifically, generate in isolation, calibrate honestly, surface the early-warning signals. The output is meant to make the plan stronger or the system harder, not to prevent the plan from being attempted or the system from being trusted. A pre-mortem that turns up few specific failure modes is a stronger result, not an under-pre-mortemed one — calibration honesty is the bar.
