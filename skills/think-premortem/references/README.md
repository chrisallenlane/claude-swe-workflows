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
- Natural follow-up to `/think-scrutinize` (stress-test mitigations) or `/scope` (ticket the defendable failure modes)

## When to Use

**Use `/think-premortem` (plan mode) for:**

- Before committing to a plan, design, or significant decision
- Pre-flight check before invoking `/lead-project` or `/implement-project` on multi-week work
- Before merging a major architectural change
- Before announcing a deadline or rollout to stakeholders
- When a plan feels solid but residual unease remains — the unease often points at a real failure mode

**Use `/think-premortem` (scenario mode) for:**

- Hardening an existing system against a hypothetical catastrophe ("if a zero-day were used against us, how could it have happened?")
- Investigating worst-case scenarios for a deployed service before adversarial conditions actually materialize
- Stress-testing a system's hidden coupling, reversibility, or detection assumptions by imagining specific catastrophic outcomes
- Pre-incident-response preparation — surfacing what the on-call team would need if a named scenario hit

**Don't use `/think-premortem` for:**

- Plans too vague to fail concretely (refine first via `/scope` or `/think-reframe`)
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
 │  Plan: what/why/when/who/where                │
 │  Scenario: scenario + system scope            │
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
|---------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| Judge (you)   | Detect mode, capture target, validate concreteness, choose lenses, synthesize the risk register                                           |
| Pre-mortemers | Plan mode: imagine catastrophic failure within an assigned lens. Scenario mode: investigate actual code for given scenario. In isolation. |

## The Two Modes

### Plan mode

The user has not yet committed to a plan. The skill imagines how the plan could fail catastrophically across multiple lenses, broadly. Pre-mortemers reason from the plan brief alone — the brief is their ground truth.

*Use when:* the work has not started, and the user wants to harden the plan before commitment.

*Example trigger:* "Premortem this auth-service migration plan before we kick off."

*Output emphasis:* mitigations to add to the plan; load-bearing assumptions to verify.

### Scenario mode

The user poses a specific catastrophic scenario against an existing system and asks how it could have happened. Pre-mortemers investigate the actual code, architecture, and configuration — looking for features of the system that would have allowed the given scenario. The codebase is their ground truth.

*Use when:* the work is shipped or running, and the user wants to harden the system against a hypothetical catastrophe before it actually materializes.

*Example triggers:*
- "An undiscovered zero-day exploit was used to attack our users via this app. How did this happen?"
- "A critical design defect destroyed the production database. How did this happen?"
- "A design defect caused AWS to hyperscale, causing a runaway bill. How did this happen?"

*Output emphasis:* hardening work to do on the system; specific code/config to fix; signals to monitor for.

### Critical distinction: scenario mode is for *hypothetical* catastrophes

Scenario mode operates on catastrophes that have *not* occurred. The user uses prospective-hindsight framing as a stress-testing technique against a system that is currently fine.

If the catastrophe is *actually happening now* — symptoms observable, cause unclear — that is `/think-diagnose`'s territory (abductive reasoning to infer causes of an observed phenomenon). If the incident has *resolved* and the user wants to learn from it, that is `/think-reflect`. Scenario-mode pre-mortem sits between the two: imagine a catastrophe that *could* hit, and harden against it.

## Failure-Class Lenses

Pre-mortemers cover three categories of lens. The orchestrator selects from each:

### 1. Standard lenses (pick 4-7)

The 11 prescribed failure classes, available in every pre-mortem:

| Lens                          | Failure shape                                                              |
|-------------------------------|----------------------------------------------------------------------------|
| technical                     | Implementation broke; design didn't survive contact with reality           |
| operational                   | Couldn't deploy, observe, maintain, or sustain on-call                     |
| estimation                    | Took 3-5x longer; sandbagged assumptions; hidden complexity surfaced late  |
| scope                         | Built the wrong thing; problem moved while team built                      |
| adoption                      | Users didn't take it up; defected; found a workaround                      |
| dependency-and-environment    | External factor changed (vendor, regulation, market, library)              |
| team-and-coordination         | Attrition, knowledge loss, blocked-on-someone, handoff breakdown           |
| incentive                     | Goodhart; system rewarded the wrong thing                                  |
| detection                     | Failure went unnoticed; instrumentation gap; silent corruption             |
| reversibility                 | Couldn't roll back; sunk-cost trapped continuation                         |
| adversarial                   | Malicious or careless actor; trust assumption was load-bearing and unstated |

4-7 standard lenses is typical. Drop lenses that don't fit — forcing an unfit lens produces noise. **For software projects, technical, operational, and estimation are almost always present.**

### 2. Ad-hoc target-specific lenses (0-3)

The orchestrator may add lenses tailored to the target's domain when the standard taxonomy doesn't cover a known class of failure cleanly. The orchestrator names the lens and provides a one-sentence definition; the pre-mortemer applies that definition.

Examples of ad-hoc lenses:

| Domain                       | Ad-hoc lens                  | Failure shape                                                                       |
|------------------------------|------------------------------|-------------------------------------------------------------------------------------|
| ML system                    | training-distribution-drift  | Model performance degrades as input distribution diverges from training data        |
| Multi-tenant SaaS            | tenant-isolation             | One tenant's actions affect another's correctness, performance, or privacy          |
| Real-time trading            | latency-and-jitter           | Timing variance produces correctness or ordering failures                            |
| Federated identity           | cross-domain-trust           | Trust propagation across boundaries amplifies a single compromise                    |
| Compliance-bound system      | regulatory-shift             | A regulation change retroactively invalidates compliant behavior                     |

Add an ad-hoc lens when:

- The target's domain has a recognized class of failure that doesn't map cleanly to a standard lens
- A standard lens would technically cover it but would dilute focus by mixing it with unrelated concerns

If no ad-hoc lens is warranted, run zero. **The standard lenses + first-principles cover most cases.** Adding ad-hoc lenses for the sake of comprehensiveness dilutes the register.

### 3. The `first-principles` lens (always runs)

The free-form lens. Its job is to catch failure modes specific to *this* target that don't fit cleanly into any other lens being applied. Klein's original pre-mortem worked exactly this way — participants imagined freely without category constraints. The structured lens taxonomy is our addition for systematic coverage; the `first-principles` lens recovers what the taxonomy can miss.

The pre-mortemer assigned to `first-principles` is told which other lenses are being applied. Its job is to find failures *outside* their territory — modes that span multiple lenses, emerge from the target's unique architectural choices, or arise from interactions the structured lenses each touch separately.

Honest "nothing here that the other lenses don't already catch" is a valid, calibrated outcome from the `first-principles` lens. Manufactured findings dilute the register; the lens earns its slot when it surfaces something the prescribed taxonomy missed, not by always producing.

## The Prospective Hindsight Mechanism

Pre-mortem methodology comes from Gary Klein's decision research (*Sources of Power*, 1998; *HBR*, 2007). The cognitive trick is *prospective hindsight*: imagining a failure as if it has already happened produces more concrete and better-calibrated cause identification than imagining failure as a forward-looking risk. Mitchell, Russo, and Pennington (1989) measured the effect: prospective hindsight produced roughly 30% better identification of correct reasons than risk-assessment framing.

The skill operationalizes this. Each pre-mortemer is told the plan failed, given a specific failure mode to inhabit, and asked to reconstruct how it got there. The framing is load-bearing — pre-mortemers are explicitly forbidden from saying "this could happen" and required to say "this happened."

## The Risk Register Output

The synthesis differs from `/think-brainstorm` (catalog of options) and from `/think-scrutinize` (faults that survived adversarial cross-examination). The output here is a *risk register*: failure modes calibrated by likelihood and impact, paired with early-warning signals.

Each failure mode includes:

- **Failure scenario** — concrete narrative, past tense, specific
- **Causal chain** — the path that produced it
- **Causes (root)** — the upstream causes that allowed it
- **Early-warning signals** — what an observer would have noticed *before* the catastrophic moment
- **Likelihood** — qualitative (*high / moderate / low / uncertain*)
- **Impact** — qualitative (*high / moderate / low*)
- **Defendable / monitor-only** — can it be designed against now, or only watched for?

The report headlines the top 3-5 by likelihood × impact, with a tabulated tail for completeness and a cross-cutting observations section that often matters more than any single finding.

## Output

A structured report with:

- **Top Failure Modes** (headline) — 3-5 detailed entries, each with scenario, causes, signals, calibration
- **Other Failure Modes Worth Tracking** — lower-priority entries in tabulated form
- **Cross-Cutting Observations** — patterns that emerged across multiple lenses
- **Load-Bearing Assumptions** — assumptions that, if false, invalidate the plan
- **Lenses That Found Little** — honest reporting where a chosen lens produced limited value
- **Suggested Next Steps** — natural follow-ups (`/think-scrutinize`, `/scope`, etc.)

## Iteration

The skill is **one-shot by design**. Each plan gets one clean consultation. To pre-mortem a revised plan, re-invoke. To stress-test a specific mitigation, hand off to `/think-scrutinize`. To turn defendable failure modes into work, hand off to `/scope`.

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
[Time horizon: 8 weeks from now — 2 weeks past the planned end]
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

## Example Session (Scenario Mode)

```
> /think-premortem A critical design defect caused the destruction of
  our production database. How did this happen?

Detecting mode: scenario mode. The framing is past-tense catastrophic,
posed against an existing system.

Capturing the brief:
- Scenario: production database was destroyed by a critical design defect
- Target system: needs scoping

Two questions before I spawn pre-mortemers:

1. Which database / service is in scope? "The production database" is
   too broad to investigate concretely.
> The orders service. Postgres backend. The orders-svc/ directory plus
  the migration scripts in db/migrations/.

2. By "destroyed" — do you mean structural (schema corruption / data loss)
   or operational (unrecoverable performance state)? The lens selection
   differs.
> Data loss. Imagine all order rows for the past quarter are gone and the
  backups don't restore cleanly.

OK. Lenses I'll apply:
- technical (most likely path to data loss via design defect)
- reversibility (backups didn't restore cleanly is a reversibility claim)
- detection (a defect that destroys data may have been silently brewing)
- operational (the operational path that allowed the defect to ship)
- adversarial (worth checking — a malicious actor exploiting a design
  defect is a related causal path)

Skipping estimation, scope, adoption, dependency-and-environment, team,
incentive — they don't materially advance this scenario.

[Spawning 5 pre-mortemers in parallel, with read access to orders-svc/
 and db/migrations/...]
[Each investigating the actual code for causes of the given scenario...]
[Synthesizing...]

## Pre-Mortem Report

Mode: scenario
Target: orders-svc/ + db/migrations/
Scenario: A critical design defect caused destruction of the production
          database (data loss for the past quarter; backups failed to
          restore cleanly).
Lenses applied: technical, reversibility, detection, operational, adversarial

### Top Failure Modes

1. **Migration script lacks transaction boundary on destructive ops**
   *(lenses: technical, reversibility)*
   - **Failure scenario:** Migration `db/migrations/20260318_normalize_orders.sql`
     executes a multi-step rewrite that deletes from `orders_legacy` and
     inserts into `orders` without wrapping the operation in a transaction.
     A failure mid-script leaves `orders_legacy` partially deleted and
     `orders` partially populated. The rollback path attempts to restore
     from `orders_legacy` but the rows are gone.
   - **Causes:** The script uses `BEGIN`/`COMMIT` at the top and bottom,
     but a `\set ON_ERROR_STOP` is not set, and an intermediate
     `RAISE NOTICE` is incorrectly used for status logging in a way
     that does not abort on error. The migration runner (`scripts/migrate.sh`)
     does not check exit codes between steps.
   - **Evidence:** `db/migrations/20260318_normalize_orders.sql:1-12`
     (no `ON_ERROR_STOP`); `scripts/migrate.sh:34` (does not check
     intermediate exit codes).
   - **Early-warning signals:** Any migration in the repo that uses
     `DELETE` followed by `INSERT` against the same table family without
     `ON_ERROR_STOP` set. Currently 3 other migrations match this pattern.
   - **Likelihood:** moderate — the pattern is present and unguarded
   - **Impact:** high — data loss
   - **Defendable / monitor-only:** Defendable. Add `ON_ERROR_STOP=1` to
     all migrations; refactor migrate.sh to halt on any non-zero exit.

2. **Backup restore path is untested and likely broken**
   *(lenses: reversibility, detection)*
   - **Failure scenario:** When the team attempted to restore from the
     nightly backup, the restore script `scripts/restore-from-backup.sh`
     fails because it expects a backup format that was changed in
     `scripts/backup.sh:18` six weeks ago to a streaming format. The
     restore script was never updated to match. The backups exist but
     cannot be applied to a running cluster.
   - **Causes:** Backup format change without corresponding restore-side
     update. No automated restore test in CI. The last successful test
     restore was 4 months ago, before the format change.
   - **Evidence:** `scripts/backup.sh:18` (format change committed
     2026-03-12); `scripts/restore-from-backup.sh:42-58` (still expects
     pre-change format); `.github/workflows/` contains no restore test.
   - **Early-warning signals:** No restore-from-backup test runs in CI
     currently. A scheduled monthly drill would catch this. The fact
     that backups complete cleanly says nothing about whether they can
     be restored.
   - **Likelihood:** high — the format mismatch is verifiable from the code now
   - **Impact:** high — turns a recoverable failure into an unrecoverable one
   - **Defendable / monitor-only:** Defendable. Add a CI job that
     restores yesterday's backup to a throwaway database and validates
     row counts.

3. **Soft-delete column unused but relied on by orphan-prevention logic**
   *(lenses: technical, detection)*
   - **Failure scenario:** A soft-delete-then-purge job in `orders-svc/jobs/cleanup.go`
     filters by `deleted_at IS NOT NULL AND deleted_at < NOW() - INTERVAL '90 days'`,
     but a recent migration changed the column type from `timestamp` to
     `timestamptz` without updating the cleanup job's timezone-handling.
     Under DST transition, a window of orders gets `deleted_at` values that
     compare incorrectly, and the cleanup job permanently deletes rows that
     should still be live.
   - **Causes:** Column type change; cleanup job logic not updated; no test
     covering the timezone-boundary case.
   - **Evidence:** `orders-svc/jobs/cleanup.go:23` (timezone-naive comparison);
     `db/migrations/20260205_orders_timestamptz.sql` (column type change);
     no corresponding test in `orders-svc/jobs/cleanup_test.go`.
   - **Early-warning signals:** A spike in customer complaints about
     missing orders in the days following a DST transition. Or a
     scheduled query that audits cleanup-job actions before they run.
   - **Likelihood:** moderate — only fires under DST transitions
   - **Impact:** moderate — partial data loss, recoverable from backups
     *if* backup restore works (see #2)
   - **Defendable / monitor-only:** Defendable. Add explicit timezone
     handling and tests for DST-boundary cases.

### Other Failure Modes Worth Tracking

| Failure mode                                                | Lens          | Likelihood | Impact   | Early signal                                        |
|-------------------------------------------------------------|---------------|------------|----------|-----------------------------------------------------|
| Privileged DB role used by app for migrations               | adversarial   | low        | high     | Audit DB role permissions; check app's role grants  |
| No row-count validation post-migration                      | detection     | moderate   | moderate | Add row-count checks to migration runner            |
| Replication lag masks data loss until catastrophic          | operational   | low        | high     | Replication lag dashboards exist but aren't alerted |

### Cross-Cutting Observations

- **Three lenses (technical, reversibility, detection) all converged on
  *unverified rollback paths*.** The migration script lacks transactions;
  the backup restore isn't tested; row-count validation is absent. The
  pattern: the system trusts that rollback works without ever exercising
  it. Highest-leverage hardening: institute regular rollback drills.

- **The migration runner (`scripts/migrate.sh`) is a single point of
  failure.** Multiple lenses pointed to it. Worth a focused review.

### Load-Bearing Assumptions

- Backups can be restored to a running cluster (likely false — see #2)
- Migrations are atomic at the file level (false — see #1)
- The cleanup job is timezone-safe (false — see #3)
- All migrations use the same safety conventions (verifiable; currently false)

### Lenses That Found Little

- adversarial — produced one moderate-likelihood finding (privileged DB
  role) but the scenario as posed is more naturally explained by design
  defect than by adversarial action

### Suggested Next Steps

- Add `ON_ERROR_STOP=1` and exit-code checks to migration tooling (defends against #1)
- Add CI restore-from-backup test (defends against #2 and the cross-cutting observation)
- Audit migration scripts for the DELETE+INSERT-without-transaction pattern
- To stress-test the proposed hardening: `/think-scrutinize`
- To turn the defendable items above into tickets: `/scope`
```

## Relationship to Other Skills

| Skill                | Relationship                                                                                                                                  |
|----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| `/think-scrutinize`  | Natural downstream — stress-test mitigations or load-bearing assumptions surfaced                                                              |
| `/think-deliberate`  | Natural downstream — choose between candidate mitigation / hardening approaches                                                                |
| `/scope`             | Natural downstream — turn defendable failure modes into tickets                                                                                |
| `/think-reflect`     | Matched pair on the time axis — pre-mortem ex-ante (hypothetical), reflect ex-post (resolved)                                                  |
| `/think-brainstorm`  | Pre-mortem can identify the *problem* (failure modes); brainstorm generates *mitigations*                                                       |
| `/think-diagnose`    | Adjacent skill for *currently-occurring* failures with unknown causes; pre-mortem (scenario mode) is for *hypothetical* failures against running systems |

**Pre-mortem and scrutinize compared.** Both stress-test plans / systems, but they are not redundant. Pre-mortem is broader and more generative — it sweeps the failure space using prospective hindsight. Scrutinize is narrower and more dialectical — skeptics versus advocate on a specific concern. Natural ordering: *pre-mortem first, scrutinize second*. Pre-mortem identifies the top failure modes; scrutinize stress-tests the mitigations or load-bearing assumptions.

**Pre-mortem and diagnose compared (important).** These are easy to confuse but distinct.

- `/think-diagnose` is for *currently-observable* failures whose causes are unknown — abductive reasoning to infer what *is* causing a real phenomenon. Symptoms are observable now; the question is "why?"
- `/think-premortem` (scenario mode) is for *hypothetical* catastrophes against running systems — the user posits "imagine X happened" against a system where X has *not* happened, and the skill investigates what features of the system could have allowed X. The scenario is given; the question is "what in the system would have produced this?"

If the failure is real and now, route to `/think-diagnose`. If it is hypothetical, scenario-mode pre-mortem applies.

**Pre-mortem and reflect as matched pair.** Pre-mortem is prospective failure imagination *before* the failure has happened; reflect is retrospective learning *after* an experience has resolved. They share the discipline of separating decision quality from outcome quality (Tetlock) — pre-mortem at the front, reflect at the back.

## Philosophy

Optimism is the default mode of both planning and operating systems. People imagine plans succeeding and systems running cleanly, patch over the failure modes that happen to surface, and proceed. This systematically under-attends to risks and produces post-hoc surprise when those risks materialize.

Klein's contribution is the framing reversal. Asking "what could go wrong?" lets the planning brain shrug off concerns; pre-mortem instead says "the failure has already happened; figure out why." Prospective hindsight bypasses the optimism filter — people are surprisingly good at imagining concrete failure causes when they are told a failure already occurred.

The technique generalizes. It works on plans before commitment (Klein's original framing) and on running systems against hypothetical catastrophes (the same cognitive trick, applied to a different target). What changes is whether the pre-mortemers imagine causes broadly within a plan, or investigate the actual system for causes that could have produced a specific given scenario. In scenario mode, the discipline tightens: claims must be backed by evidence in the actual code.

The plugin operationalizes both with the NGT-isolated parallel-agents pattern that the other `/think-*` skills use. Independent imagination or investigation prevents anchoring on the first plausible failure cause; synthesis produces a register the user can act on rather than a list of generic risks they can dismiss.

The discipline is: imagine or investigate specifically, generate in isolation, calibrate honestly, surface the early-warning signals. The output is meant to make the plan stronger or the system harder, not to prevent the plan from being attempted or the system from being trusted. A pre-mortem that turns up few specific failure modes is a stronger result, not an under-pre-mortemed one — calibration honesty is the bar.
