# /think-premortem - Prospective Failure Imagination

## Overview

`/think-premortem` treats a catastrophic failure as if it has already happened and reasons backward to the causes. It runs failure-class lenses as isolated parallel pre-mortemers and synthesizes a prioritized risk register paired with early-warning signals.

It counters the planning fallacy and optimism bias. The method is Gary Klein's pre-mortem (*Sources of Power*, 1998; HBR, 2007), built on *prospective hindsight*. Imagining a failure as already having happened produces more concrete cause identification than forward-looking risk assessment, by roughly 30% in Mitchell, Russo, and Pennington (1989). The namespace-wide rationale lives in [`references/think.md`](../../../references/think.md).

The step-by-step procedure lives in [`SKILL.md`](../SKILL.md); this guide covers when to use the skill and what to expect.

It produces feedback only: no code, no tickets, no artifacts.

## Two Modes

The skill detects the mode from your framing and asks if it's ambiguous.

- **Plan mode.** You have a plan, design, or decision you haven't committed to. Pre-mortemers imagine it failed, broadly, within their lens. The output guides what to change before commitment. *"Premortem this auth-service migration plan before we kick off."*
- **Scenario mode.** You pose a specific hypothetical catastrophe against an existing system. Pre-mortemers read the scoped code and investigate what could have allowed it, citing file:line. The output guides hardening. *"An undiscovered zero-day was used to attack our users via this app. How did this happen?"*

Scenario mode is for catastrophes that have *not* happened. If the failure is happening now and the cause is unclear, use `/think-diagnose`. If it has resolved and you want to learn from it, use `/think-reflect`.

## When to Use

**Plan mode:**
- Before committing to a plan, design, or significant decision
- Pre-flight check before invoking `/implement` on multi-week work
- Before merging a major architectural change
- Before announcing a deadline or rollout to stakeholders
- When a plan feels solid but some unease remains. The unease often points at a real failure mode.

**Scenario mode:**
- Hardening an existing system against a hypothetical catastrophe
- Investigating worst-case scenarios for a deployed service before adversarial conditions materialize
- Testing a system's hidden-coupling, reversibility, or detection assumptions
- Preparing for incident response: what on-call would need if a named scenario hit

**Don't use `/think-premortem` for:**
- Plans too vague to fail concretely (refine first via `/scope` or `/think-brainstorm`). The skill checks concreteness and will push back.
- Currently-failing situations (use `/think-diagnose`)
- Already-resolved incidents (use `/think-reflect`)
- Choosing between options (use `/think-deliberate`)
- Generating new approaches (use `/think-brainstorm`)

**Rule of thumb:**
- "What could go wrong with this plan?" → `/think-premortem` (plan mode)
- "If [catastrophe] hit our system, how could it have happened?" → `/think-premortem` (scenario mode)
- "What's wrong with this idea right now?" → `/think-scrutinize`
- "Why is this currently broken?" → `/think-diagnose`
- "What did this teach us?" → `/think-reflect`

**Pre-mortem first, scrutinize second.** The pre-mortem sweeps the failure space, and `/think-scrutinize` then stress-tests the mitigations or load-bearing assumptions it surfaced. Pre-mortem and `/think-reflect` are a matched pair on the time axis: one before the fact, one after.

## Flow

```
Detect mode + receive target → Validate concreteness → Choose lenses
  → Pre-mortemers (parallel, isolated) → Synthesize risk register → Report
```

## Lenses

The skill picks the lenses; you don't. There are three categories.

**Standard lenses (4–7 chosen).** For software projects, technical, operational, and estimation are almost always included.

| Lens                       | Failure shape                                                     |
| -------------------------- | ----------------------------------------------------------------- |
| technical                  | Implementation broke; design didn't survive contact with reality  |
| operational                | Couldn't deploy, observe, maintain, or sustain on-call            |
| estimation                 | Took 3–5x longer; hidden complexity surfaced late                 |
| scope                      | Built the wrong thing; the problem moved while the team built     |
| adoption                   | Users didn't take it up or found a workaround                     |
| dependency-and-environment | An external factor changed (vendor, regulation, market, library)  |
| team-and-coordination      | Attrition, knowledge loss, blocked handoffs                       |
| incentive                  | Goodhart; the system rewarded the wrong thing                     |
| detection                  | Failure went unnoticed; instrumentation gap                       |
| reversibility              | Couldn't roll back; sunk cost trapped continuation                |
| adversarial                | An actor exploited a weakness or an unstated trust assumption     |

**Ad-hoc target-specific lenses (0–3).** The skill names these only when the target's domain has a known failure class the standard set doesn't cover cleanly. Examples: `tenant-isolation` for multi-tenant SaaS, `training-distribution-drift` for ML systems, `regulatory-shift` for compliance-bound systems.

**`first-principles` (always runs).** A free-form lens that catches failure modes specific to this target that fall outside the other lenses. This recovers Klein's original uncategorized pre-mortem.

## What You Get Back

A prioritized risk register:

- **Top Failure Modes** (3–5): each has a concrete past-tense failure scenario, its causes (with file:line in scenario mode), likelihood and impact (high / moderate / low / uncertain), early-warning signals, and a *defendable* or *monitor-only* label
- **Other Failure Modes Worth Tracking**: a table of lower-priority entries
- **Cross-Cutting Observations**: patterns across lenses, which often matter more than any single finding
- **Load-Bearing Assumptions**: what must be true for the plan to work; verify these before committing
- **Lenses That Found Little**: honest reporting
- **Suggested Next Steps**: `/think-scrutinize`, `/think-deliberate`, `/scope`, or a re-invocation

In plan mode, early-warning signals are things to watch for during execution. In scenario mode, they are things observable in the running system now. The skill is one-shot: re-invoke after revising the plan or hardening the system.

## Example Session (Plan Mode)

```
> /think-premortem We're planning to migrate our auth service from the legacy
  monolith to a new dedicated service over the next six weeks. Three engineers,
  with rolling deployment.

Time horizon: 8 weeks from now — 2 weeks past the planned end.

1. Any SSO, MFA, or federation involved?
> Email/password + TOTP MFA. One SAML SSO integration with a customer org.

2. Does anyone else read from the auth tables?
> Billing reads user metadata; audit log writes to a shared events table.

3. What's the rollback story?
> Keep the legacy path callable via feature flag for at least one cycle.

Lenses: technical, operational, estimation, dependency-and-environment,
detection, reversibility, first-principles. Skipping adoption (internal users),
adversarial (separate security pass planned), incentive, team-and-coordination,
scope.

## Pre-Mortem Report

### Top Failure Modes

1. **Silent SAML SSO breakage for the one customer org**
   *(lenses: technical, detection, dependency-and-environment)*
   - **Failure scenario:** After legacy was decommissioned, the customer's
     contract renewal triggered a rare SAML re-handshake the new service
     didn't handle. Their users lost access for 14 hours.
   - **Causes:** SAML tests covered only the common flow; legacy handled the
     renewal variant implicitly.
   - **Early-warning signals:** handshake byte-count discrepancies between
     legacy and new service during shadow traffic.
   - **Likelihood:** moderate. **Impact:** high.
   - **Defendable:** shadow the customer for a full quarter before decommissioning.

2. **Reversibility is shorter-lived than assumed**
   *(lenses: reversibility, operational)*
   - **Failure scenario:** Week 7, the flag still worked, but the team had
     stopped writing a cache the legacy path depended on. Fallback needed a
     2-hour manual warm-up and lost session state.
   - **Early-warning signals:** any "stop writing to X, the new system handles
     it" decision during implementation.
   - **Likelihood:** moderate. **Impact:** high.
   - **Defendable:** keep a rollback checklist; test the rollback path mid-migration.

### Cross-Cutting Observations

- Three lenses surfaced failures in *non-obvious consumers* of the auth path
  (billing, SAML variants, audit log). The team's model of "the auth path" is
  narrower than its real surface. A consumer audit before cutover is the
  highest-leverage addition.

### Load-Bearing Assumptions

- TOTP secrets all match the documented format (likely false)
- The legacy path can be re-enabled safely after one cycle (likely false in detail)
```

Scenario mode has the same shape, with two differences. The brief pairs the posed scenario with a scoped target system, and every cause cites the code, configuration, or architecture that would have allowed it.
