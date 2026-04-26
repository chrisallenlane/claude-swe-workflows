# /think-ach - Analysis of Competing Hypotheses

## Overview

The `/think-ach` skill operationalizes Richards Heuer's Analysis of Competing Hypotheses (ACH) — a CIA-tradition technique for systematically narrowing among multiple hypotheses against evidence. It generates hypotheses (parallel, isolated, by angle), enumerates evidence (parallel, isolated, by class), builds an explicit matrix mapping every piece of evidence against every hypothesis, focuses on disconfirming evidence to rank hypotheses, and reports the surviving leader along with sensitivity analysis and falsification milestones.

**Key properties:**

- **Disconfirmation-focused.** The central insight: a hypothesis cannot be proven, only disconfirmed. The leading hypothesis is the one with the *least* inconsistent evidence — not the most consistent. This counters confirmation bias structurally.
- **Explicit matrix.** Evidence × hypothesis grid with C / I / N/A markings. Defeats cherry-picking by making the analysis legible.
- **NGT-isolated generation.** Hypothesizers and evidence-gatherers run in parallel, in isolation, across distinct angles/classes — preventing the leading hypothesis from anchoring all the others.
- **Diagnosticity analysis.** Surfaces which evidence actually discriminates among hypotheses; drops evidence consistent with all.
- **Sensitivity analysis.** For each load-bearing piece of evidence, asks "what if this is wrong?" and watches the conclusion shift.
- **Falsification milestones.** Identifies future observations that would distinguish the top hypotheses, making the analysis falsifiable.
- **All hypotheses preserved in the report**, not just the leader. The 2nd-place hypothesis is "currently disconfirmed less than possible new evidence might change," not "wrong."
- Produces feedback only — no code, no tickets, no artifacts.

## When to Use

**Use `/think-ach` for:**

- Multiple competing hypotheses (3-7+) need rigorous narrowing
- A causal investigation has surfaced multiple candidate causes; formal discrimination is needed
- Attribution questions ("who/what is responsible for X?") with multiple actors or mechanisms
- Forecasting questions with multiple competing scenarios and evidence available
- Intelligence-style questions where confirmation bias is a known risk
- After `/think-diagnose` has generated candidate causes and the user wants formal narrowing

**Don't use `/think-ach` for:**

- Only 1-2 hypotheses (use `/think-scrutinize` to stress-test the leading one)
- Hypotheses too vague or non-mutually-exclusive (refine first via `/think-reframe`)
- Insufficient evidence to discriminate (narrow the question or gather more evidence first)
- Generating hypotheses (use `/think-diagnose` for causes, `/think-brainstorm` for options)
- Picking among options (use `/think-deliberate` — option selection has different cognitive structure)

**Rule of thumb:**

- "Which of these competing hypotheses is most likely correct?" → `/think-ach`
- "What could be causing this phenomenon?" → `/think-diagnose`
- "Which option should I pick?" → `/think-deliberate`
- "What's wrong with this idea?" → `/think-scrutinize`

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ /think-ach Workflow                                         │
└─────────────────────────────────────────────────────────────┘

 ┌──────────────────────────────────────────────┐
 │  1. RECEIVE QUESTION + SEED HYPOTHESES       │
 │  ────────────────────────────────────────    │
 │  • Capture the question                      │
 │  • Capture any user-provided hypotheses      │
 │  • Identify available evidence sources       │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  2. VALIDATE ACH-SHAPED                      │
 │  ────────────────────────────────────────    │
 │  • Multiple plausible hypotheses (3-7)       │
 │  • Evidence available                        │
 │  • Hypotheses mutually exclusive enough      │
 │  • Rigorous narrowing wanted (not ideation)  │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  3. ENUMERATE HYPOTHESES (parallel, isolated)│
 │  ────────────────────────────────────────    │
 │  Angles: leading / alternative /             │
 │  adversarial / null / deceptive / surprise   │
 │  (4-6 selected; user seeds added after)      │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  4. ENUMERATE EVIDENCE (parallel, isolated)  │
 │  ────────────────────────────────────────    │
 │  Classes: direct-observational /             │
 │  documentary-historical / structural /       │
 │  behavioral / absent / anomalous             │
 │  (3-5 selected; surface BOTH confirming      │
 │   and disconfirming evidence)                │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  5. BUILD MATRIX                             │
 │  ────────────────────────────────────────    │
 │  Each cell: C / I / N/A                      │
 │  (optional intensity: CC / II)               │
 │  Evaluate each cell independently            │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  6. DIAGNOSTICITY ANALYSIS                   │
 │  ────────────────────────────────────────    │
 │  Identify high-diagnosticity (discriminating)│
 │  vs low-diagnosticity (uniform) evidence     │
 │  Set aside non-discriminating evidence       │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  7. DISCONFIRMATION-FOCUSED LEADERBOARD      │
 │  ────────────────────────────────────────    │
 │  Rank by FEWEST inconsistencies              │
 │  (not by most consistencies)                 │
 │  Preserve all hypotheses; don't collapse     │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  8. SENSITIVITY ANALYSIS                     │
 │  ────────────────────────────────────────    │
 │  For load-bearing evidence:                  │
 │  what if it's wrong / misinterpreted?        │
 │  How does the leaderboard shift?             │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  9. FALSIFICATION MILESTONES                 │
 │  ────────────────────────────────────────    │
 │  For top 2-3 hypotheses, what future         │
 │  observations would distinguish them?        │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  10. REPORT                                  │
 │  ────────────────────────────────────────    │
 │  Hypotheses / Evidence / Matrix /            │
 │  Diagnosticity / Leaderboard /               │
 │  Sensitivity / Falsification milestones /    │
 │  Caveats / Suggested next steps              │
 └──────────────────────────────────────────────┘
```

## Roles

| Role                  | What they do                                                                                       |
|-----------------------|----------------------------------------------------------------------------------------------------|
| Judge (you)           | Capture question, validate, build matrix, run diagnosticity / leaderboard / sensitivity / falsification |
| Hypothesizers         | Generate plausible hypotheses from an assigned angle, in isolation                                  |
| Evidence-gatherers    | Enumerate relevant evidence in an assigned class, in isolation                                      |

## Hypothesis-Generation Angles

The orchestrator selects 4-6 angles based on the question's character:

| Angle         | Hypothesis shape                                                                       |
|---------------|----------------------------------------------------------------------------------------|
| leading       | The obvious, popular, most-favored hypothesis (plus close variants)                    |
| alternative   | Hypotheses that contradict the leading candidate                                       |
| adversarial   | An actor with motivation acted intentionally to produce the outcome                    |
| null          | Nothing unusual is happening; appearances are normal                                   |
| deceptive     | Appearances are intentionally misleading; signals have been manipulated                |
| surprise      | An unexpected hypothesis that fits the evidence but the others would miss              |

**Selection heuristics:**

- Always include `leading` and `alternative` — these establish the basic competition
- Include `null` unless the phenomenon is structurally non-null
- Include `adversarial` when actors with motivations are in play
- Include `deceptive` when trust, intelligence, security, or signal-manipulation are relevant
- Include `surprise` when the question is novel or the user worries about missing the right answer

User-provided seed hypotheses are added to the pool *after* the hypothesizers run — including them upfront would anchor the hypothesizers.

## Evidence Classes

The orchestrator selects 3-5 classes:

| Class                    | Evidence shape                                                                       |
|--------------------------|--------------------------------------------------------------------------------------|
| direct-observational     | Logs, sensor data, metrics, witness accounts                                          |
| documentary-historical   | Records: decision documents, message threads, configuration history, prior reports   |
| structural               | System / environment features that constrain what's possible                          |
| behavioral               | Patterns of action over time (baseline + deviations)                                  |
| absent                   | What's missing; the dog that didn't bark                                             |
| anomalous                | Observations that don't fit any obvious story                                        |

**Selection heuristics:**

- Always include `direct-observational` if any direct observation exists
- Include `documentary-historical` for any non-instantaneous question
- Include `structural` for any system / code / architectural question
- Include `behavioral` when actors operate over time
- **Always include `absent` for security, intelligence, or deception-relevant questions** — what's missing is often the most diagnostic evidence
- Include `anomalous` when the user has flagged unexplained observations

## The Matrix

The matrix is the central artifact. For each (hypothesis, evidence) cell:

- **C** — *Consistent* — evidence is consistent with this hypothesis being true
- **I** — *Inconsistent* — evidence contradicts this hypothesis
- **N/A** — *Not applicable* — evidence has no bearing on this hypothesis (silence is not support)

Optional intensity markers:
- **CC** — *Strongly consistent*
- **II** — *Strongly inconsistent*

## Disconfirmation Focus — The Central Insight

ACH ranks hypotheses by *number of inconsistencies*, not by number of consistencies.

This is operationalized Popper. A hypothesis cannot be proven, only failed-to-be-disproven. The hypothesis with the fewest disconfirmations is the one most likely to survive future scrutiny — *not* the one with the most confirmations.

Why: any hypothesis can accumulate "consistent" evidence (most evidence is consistent with most hypotheses, especially if the hypotheses are not very specific). What kills hypotheses is *inconsistency*. The hypothesis that has been hardest to kill is the leader.

This is the load-bearing principle of ACH. Flipping it back to "rank by most-consistent" loses the technique's anti-confirmation-bias property entirely.

## Diagnosticity

Evidence is *diagnostic* when it discriminates among hypotheses — consistent with some, inconsistent with others. Evidence consistent with all (or inconsistent with all) tells us nothing about the relative likelihood. Drop or set aside non-diagnostic evidence to focus the analysis.

A single piece of high-diagnosticity evidence outweighs ten pieces of low-diagnosticity evidence. *Diagnosticity, not quantity, drives ACH conclusions.*

## Sensitivity Analysis

For each load-bearing piece of evidence (high-diagnosticity, decisive in the leaderboard), ask:

- What if this evidence is wrong?
- What if it's misinterpreted?
- What if it was fabricated, planted, or selectively presented?
- What if it has an alternative interpretation we haven't surfaced?

Watch the leaderboard. If a single piece of evidence flipping changes the leader, that evidence is *load-bearing* and should be verified before acting on the analysis.

This step is critical. Informal reasoning treats evidence as ground truth. ACH is explicit that evidence is itself fallible.

## Falsification Milestones

For the top 2-3 hypotheses, identify future observations that would distinguish them. "If H1 is correct, we should observe X within Y. If H2 is correct, Z." This makes the analysis falsifiable and gives the user observable signals to monitor going forward.

## Iteration

The skill is **one-shot by design**. ACH analyses are fragile to silently-changing inputs. If the question, hypothesis set, or evidence set changes, **re-invoke** with the updated inputs.

To stress-test the leading hypothesis adversarially after ACH narrows: hand off to `/think-scrutinize`.

To turn the leading hypothesis's implications into action: `/scope` for ticket creation, `/think-deliberate` for choosing among response options, etc.

## Example Session

```
> /think-ach We had a sudden 30% drop in successful checkouts last week.
  No deploys, no infra changes that we know of. Some hypotheses on the
  table: payment processor degradation, our checkout code regression,
  user-base shift, A/B test interaction. Which is most likely?

The question is ACH-shaped: 4 user-provided hypotheses, evidence available
(metrics, logs, deploy history), narrowing wanted.

Capturing the brief:
- Question: what caused the 30% checkout-success drop last week?
- User-provided seed hypotheses: payment processor degradation,
  checkout code regression, user-base shift, A/B test interaction
- Available evidence: metrics dashboard, application logs, deploy
  history, A/B test config, payment processor status page
- Scope: last week's drop, checkout flow specifically

A few questions:

1. When you say "no deploys" — does that include config changes, feature
   flag flips, third-party SDK auto-updates?
> Good catch. Feature flag flips happen continuously. Let me check...
  yes, several flag flips in the relevant period.

2. Is the drop uniform across user segments, or concentrated?
> Concentrated. Looking at the dashboard, mostly mobile users on iOS.

OK, I'll spawn hypothesizers with the angles: leading, alternative,
adversarial (lower priority — likely overkill for this), null, deceptive
(skip — no signaling component), surprise. Let me drop adversarial and
deceptive given the context.

Hypothesizer angles selected: leading, alternative, null, surprise.

Evidence-gatherer classes: direct-observational (metrics + logs),
documentary-historical (deploy + flag history), structural (checkout
flow architecture, payment processor integration), behavioral (user
segment patterns over time), absent (what alerts SHOULD have fired and
didn't), anomalous (unexplained patterns).

[Spawning 4 hypothesizers and 6 evidence-gatherers in parallel...]
[Pooling outputs and merging with user-provided seeds...]
[Building matrix...]
[Running diagnosticity, leaderboard, sensitivity, falsification...]

## ACH Report

Question: What caused the 30% checkout-success drop last week?
Hypothesis-generation angles applied: leading, alternative, null, surprise
Evidence classes applied: direct-observational, documentary-historical,
                          structural, behavioral, absent, anomalous

### Hypotheses

H1. **iOS Apple Pay integration regression** — *(seed + alternative)* —
    a recent feature flag flip enabled the new Apple Pay v2 integration
    for iOS users; the integration has a defect on iOS Safari versions
    older than 16.

H2. **Payment processor degradation** — *(seed + leading)* —
    the payment processor's mobile API endpoint had elevated error rates
    last week, affecting all mobile users.

H3. **Checkout code regression** — *(seed)* —
    a code change in checkout-svc introduced a regression that affects
    iOS users specifically.

H4. **User-base shift toward iOS Safari < 16** — *(seed + null)* —
    the user base shifted; more iOS users on older Safari are reaching
    checkout where they always failed at the same rate, just now they're
    a larger share.

H5. **A/B test interaction** — *(seed + alternative)* —
    a running A/B test for checkout UI affected only iOS users in a way
    that produced silent failures.

H6. **Third-party SDK auto-update** — *(surprise)* —
    one of the analytics or payments SDKs auto-updated last week and the
    new version has a defect on iOS Safari.

### Evidence

E1. Mobile checkout success rate dropped from 87% to 57% week-over-week
    *(direct-observational; metrics dashboard)*
E2. Drop is concentrated on iOS Safari < 16; iOS Safari 16+ unaffected
    *(direct-observational; metrics dashboard, segmented)*
E3. No code deploys to checkout-svc in the relevant period
    *(documentary-historical; CI/CD logs)*
E4. Apple Pay v2 feature flag was flipped to 100% rollout 6 days before
    the drop began *(documentary-historical; flag service log)*
E5. Apple Pay v2 was tested in staging only on iOS 17+
    *(documentary-historical; QA tracker)*
E6. Payment processor's status page shows nominal mobile API for the
    period *(documentary-historical; vendor status archive)*
E7. checkout-svc structurally cannot fail silently — it logs all checkout
    failures *(structural; code review)*
E8. Application logs for the period show ~30% increase in
    "apple_pay_v2_init_failed" warnings, all from iOS Safari < 16
    *(direct-observational; application logs)*
E9. iOS Safari < 16 share of users has been declining (now ~12%, was ~14%
    a month ago) *(behavioral; analytics)*
E10. NO alerts fired during the period; alerting was not configured for
     this category of warning *(absent; alerting config)*
E11. The A/B test for checkout UI was not segment-restricted to iOS
     *(documentary-historical; experiment config)*
E12. Anomaly: success rate started dropping ~6 days after the flag flip,
     not immediately. *(anomalous; metrics dashboard)*

### Matrix

|     | H1 | H2 | H3 | H4 | H5 | H6 |
|-----|----|----|----|----|----|----|
| E1  | C  | C  | C  | C  | C  | C  |
| E2  | CC | I  | C  | C  | C  | C  |
| E3  | C  | C  | II | C  | C  | C  |
| E4  | CC | I  | I  | I  | I  | I  |
| E5  | CC | I  | I  | N/A| I  | I  |
| E6  | C  | II | C  | C  | C  | C  |
| E7  | C  | C  | I  | C  | I  | C  |
| E8  | CC | I  | I  | I  | I  | C  |
| E9  | I  | I  | I  | II | I  | I  |
| E10 | C  | C  | I  | C  | C  | C  |
| E11 | I  | I  | I  | I  | C  | I  |
| E12 | C  | I  | I  | I  | I  | I  |

### Diagnosticity

**High-diagnosticity evidence (load-bearing):**
- E2 — discriminates strongly: H1 strongly consistent, H2 inconsistent
- E4 — discriminates strongly: only H1 strongly consistent
- E5 — discriminates strongly: only H1 strongly consistent
- E6 — discriminates: H2 strongly inconsistent
- E7 — discriminates: H3 and H5 inconsistent
- E8 — discriminates strongly: H1 strongly consistent, others inconsistent
- E9 — discriminates: H4 strongly consistent, others inconsistent
- E11 — discriminates: only H5 consistent
- E12 — discriminates: only H1 consistent

**Low-diagnosticity evidence (set aside):**
- E1 — consistent with all (every hypothesis predicts a checkout drop)
- E3 — consistent with all except H3 (already represented elsewhere)
- E10 — mostly consistent, weakly diagnostic

### Leaderboard (ordered by least disconfirming evidence)

1. **H1: iOS Apple Pay integration regression** — 1 inconsistency (E9) —
   strongly supported by E2, E4, E5, E8, E12. The 1 inconsistency (declining
   iOS<16 user share) is mild and explainable.

2. **H6: Third-party SDK auto-update** — 8 inconsistencies — possible but
   poorly supported; would need to identify which SDK and would also need
   to explain why it correlates so well with the Apple Pay flag flip
   timing. Likely not.

3. **H4: User-base shift** — 9 inconsistencies — strongly inconsistent
   with E9 trending the other way. The user-base-shift hypothesis predicts
   iOS<16 share growing; observed: declining.

4. **H3: Checkout code regression** — 10 inconsistencies — inconsistent
   with E3 (no deploys) most strongly.

5. **H2: Payment processor degradation** — 10 inconsistencies — strongly
   inconsistent with E6 (vendor status nominal) and E2 (discrimination by
   iOS version is hard to explain via processor degradation).

6. **H5: A/B test interaction** — 10 inconsistencies — inconsistent with
   E7 (silent failure structurally hard) and E11 (test wasn't iOS-only,
   so wouldn't produce iOS-only effect).

### Sensitivity Analysis

**Load-bearing evidence and what changes if it's wrong:**

- **E5** (Apple Pay v2 was tested only on iOS 17+ in staging) — this
  evidence is critical to H1. If staging *did* cover iOS Safari < 16 and
  the test passed, H1 weakens significantly. **Worth verifying directly
  in QA records.**
- **E8** (~30% spike in apple_pay_v2_init_failed warnings on iOS Safari
  < 16) — load-bearing for H1. If the warnings turn out to be expected
  behavior, H1 weakens. Worth checking the warning's emission code path
  to confirm it indicates real failure.
- **E12** (success rate started dropping ~6 days after flag flip, not
  immediately) — *anomaly* that the leading hypothesis has to explain.
  H1 is consistent if the rollout was gradual (which the flag log
  confirms via partial rollout history). If the flag log shows
  instantaneous 100% flip, H1 is weakened by E12.

### Falsification Milestones

To distinguish H1 from H6:

- **If H1 is correct:** rolling back the Apple Pay v2 flag should restore
  iOS Safari < 16 success rates within hours.
- **If H6 is correct:** the rollback won't help; we'd see the drop persist
  until the SDK is rolled back independently.

Recommended action to discriminate: **flip the Apple Pay v2 flag back for
iOS Safari < 16 users** (assuming the flag service supports OS-targeting)
and observe the success rate over the next 24 hours.

### Notes and Caveats

- Hypotheses dropped during refinement: none — all 6 retained
- Evidence we didn't have access to: the actual content of the
  apple_pay_v2_init_failed warning messages (would let us confirm the
  failure mode mechanically)
- Confidence in this analysis: **high** for H1 leading; the convergence
  of 5 high-diagnosticity pieces of evidence (E2, E4, E5, E8, E12) on
  H1 is strong, and the alternative hypotheses each have major
  disconfirmations.

### Suggested Next Steps

- **Verify E5** in QA records (staging coverage of iOS Safari < 16 for
  Apple Pay v2)
- **Test E8** by reading the apple_pay_v2_init_failed code path
- **Discriminate H1 vs H6** via flag rollback for iOS Safari < 16
- To turn the rollback decision into action: `/scope` to ticket the
  rollback + post-mortem
- To stress-test the H1 leading hypothesis adversarially before acting:
  `/think-scrutinize`
```

## Relationship to Other Skills

| Skill                | Relationship                                                                                              |
|----------------------|-----------------------------------------------------------------------------------------------------------|
| `/think-diagnose`    | Natural upstream — generates candidate causes that ACH then rigorously narrows                            |
| `/think-brainstorm`  | Natural upstream — when ACH operates on candidate options/scenarios rather than causes                    |
| `/think-scrutinize`  | Natural downstream — adversarially stress-test the leading hypothesis                                     |
| `/think-deliberate`  | Adjacent — operates on options-to-pick rather than hypotheses-to-narrow; different cognitive mode         |
| `/think-reframe`     | Upstream when hypotheses are too vague or non-mutually-exclusive                                          |
| `/think-premortem`   | Adjacent — both deal with hypothetical states, but premortem imagines failures while ACH evaluates competing real-world hypotheses |

**ACH and diagnose compared.** Diagnose is open-ended causal exploration via lens-driven brainstorming + narrative evidence assessment. ACH is rigorous narrowing via explicit matrix + disconfirmation focus. Different cognitive modes:

- *Diagnose:* generative + evaluative, lens-driven, narrative output
- *ACH:* primarily evaluative, matrix-driven, disconfirmation-focused, structured leaderboard

Use diagnose when "what could be happening?" Use ACH when "given these candidate hypotheses, which survives the evidence?" The two compose well: diagnose generates, ACH narrows.

**ACH and scrutinize compared.** Scrutinize stress-tests *one* idea adversarially. ACH narrows among *many* hypotheses systematically. ACH is breadth (many hypotheses, structured discrimination); scrutinize is depth (one hypothesis, adversarial dialectic). Natural ordering: ACH narrows to the leader, scrutinize stress-tests the leader.

## Philosophy

The default mode of reasoning under uncertainty is to find a hypothesis that fits the evidence and stop. This produces the well-known failure modes ACH was designed to counter: confirmation bias, premature closure, anchoring, cherry-picking.

Heuer's insight: these failures share a root. *We ask the wrong question.* "Does this evidence fit my hypothesis?" invites confirmation; "Does this evidence disconfirm my hypothesis?" invites honesty. The matrix forces the second question for every cell, against every hypothesis, in every direction — and the disconfirmation-focused ranking ensures the answer cannot be ignored.

ACH operationalizes Karl Popper's falsification principle for everyday reasoning: hypotheses cannot be proven, only failed-to-be-disproven. The surviving hypothesis is the one that has been hardest to kill.

The structural commitments — the matrix, the disconfirmation focus, the diagnosticity analysis, the sensitivity analysis, the falsification milestones — are the unskippable disciplines. ACH is not sophisticated. It is just unusually rigorous about preserving the alternatives that informal reasoning suppresses.
