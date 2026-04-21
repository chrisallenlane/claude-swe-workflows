# /think-diagnose - Abductive Reasoning About Causes

## Overview

The `/think-diagnose` skill figures out *why* something is happening. Given a phenomenon and the observations supporting it, it spawns parallel diagnosticians applying different reasoning lenses in isolation, then evaluates each candidate cause against the evidence and reports leading candidates with distinguishing tests the user can run.

**Key properties:**
- Hybrid generative + evaluative — unlike the purely divergent think-* skills
- Enforced separation of observation from interpretation in evidence-gathering
- Multiple reasoning lenses in parallel — different angles surface different causes
- Honest confidence calibration — qualitative categories, no fabricated percentages
- Resists compelling-narrative bias — weights evidence fit over story quality
- Applicable to non-code phenomena as readily as code ones
- Produces feedback only — no code, no tickets, no artifacts

## When to Use

**Use `/think-diagnose` for:**
- Unexplained metric changes ("why did engagement drop?")
- Recurring problems with unclear cause ("why does this project keep slipping?")
- Behavioral patterns ("why do customer calls go badly when X happens?")
- Organizational issues ("why does our goal-setting keep producing missed goals?")
- Anywhere `/bug-fix` doesn't apply because the phenomenon isn't code-specific

**Don't use `/think-diagnose` for:**
- Code-specific diagnosis (use `/bug-fix` — has artifact output and execution tooling)
- Choosing between known options (use `/think-deliberate`)
- Stress-testing a chosen plan (use `/think-scrutinize`)
- Generating remediations (use `/think-brainstorm` *after* diagnosis)
- Phenomena so vaguely described that no observations exist (refine the phenomenon first)

**Rule of thumb:**
- "Why is this happening?" → `/think-diagnose`
- "Code is broken, find and fix it" → `/bug-fix`
- "What could I do about this?" → `/think-brainstorm`

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ /think-diagnose Workflow                                    │
└─────────────────────────────────────────────────────────────┘

 ┌──────────────────────────────────────────────┐
 │  1. RECEIVE THE PHENOMENON                   │
 │  ────────────────────────────────────────    │
 │  • From context, document, or user input     │
 │  • Produce a written brief                   │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  2. GATHER EVIDENCE                          │
 │  ────────────────────────────────────────    │
 │  Separate into three buckets:                │
 │  • Observations (ground truth)               │
 │  • Interpretations held aside                │
 │  • Unavailable evidence                      │
 │  (Enforced split — most failure-prone step)  │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  3. CHOOSE REASONING LENSES                  │
 │  ────────────────────────────────────────    │
 │  Technical / Human-factors / Process /       │
 │  Incentive-structure / Environmental /       │
 │  Temporal / Measurement-artifact / Statistical│
 │  (3-6 selected; irrelevant ones dropped)     │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  4. SPAWN DIAGNOSTICIANS (parallel, isolated)│
 │  ────────────────────────────────────────    │
 │  One agent per lens                          │
 │  No cross-talk (NGT — avoids anchoring)      │
 │  Each returns: candidate causes with         │
 │  mechanism, predictions, refuters, plausibility│
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  5. EVALUATE FIT                             │
 │  ────────────────────────────────────────    │
 │  For each candidate cause:                   │
 │  • Explanatory fit against observations      │
 │  • Prediction check                          │
 │  • Refuter check                             │
 │  • Parsimony (simpler fits better)           │
 │  • Domain plausibility                       │
 │  Cluster across lenses                       │
 │  Resist compelling-narrative bias            │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  6. CALIBRATE CONFIDENCE                     │
 │  ────────────────────────────────────────    │
 │  Qualitative categories only:                │
 │  Strong fit / Moderate / Weak /              │
 │  Unable to distinguish                       │
 │  (No fabricated percentages)                 │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  7. REPORT                                   │
 │  ────────────────────────────────────────    │
 │  Leading candidate(s) / Other candidates /   │
 │  Distinguishing evidence / What remains      │
 │  unknown / Recommendation                    │
 └──────────────────────────────────────────────┘
```

## Roles

| Role              | What they do                                                             |
|-------------------|--------------------------------------------------------------------------|
| Judge (you)       | Gather evidence, choose lenses, spawn diagnosticians, evaluate candidates |
| Diagnosticians    | Generate candidate causes through assigned lenses, in isolation           |

## Reasoning Lenses

The orchestrator selects lenses based on the phenomenon's shape. Common lenses:

| Lens                  | Surfaces causes rooted in                                      |
|-----------------------|----------------------------------------------------------------|
| technical             | Engineering systems (code, infra, config, capacity)            |
| human-factors         | People, skills, fatigue, turnover, miscommunication            |
| process               | Broken or missing process, handoffs, ownership, rituals        |
| incentive-structure   | The system rewards the observed behavior (Goodhart)            |
| environmental         | External factors (market, regulation, vendors, customer mix)   |
| temporal              | Change-points that correlate with the phenomenon               |
| measurement-artifact  | The phenomenon isn't real — it's an instrumentation issue      |
| statistical           | Base rates, regression to mean, Simpson's, selection, confounders|

3-6 lenses is typical. **Always include measurement-artifact for metric-based phenomena** — it catches a large share of "phenomena" that turn out to be measurement errors.

## The Observation / Interpretation Split

This is the skill's most important contribution. Most bad diagnoses start by accepting interpretations as observations. The skill forces three buckets:

- **Observations** — concrete things measured, seen, or experienced. "The metric dropped 30% on March 14th."
- **Interpretations already held** — inferences the user or others have made. "The team thinks it's the migration."
- **Unavailable evidence** — what's unknown or wasn't measured.

Diagnosticians receive all three, flagged distinctly. They're told not to accept interpretations as given — their job is to propose causes that could explain the observations, potentially challenging the user's prior interpretations.

If the user says "the metric dropped because of X," that's two claims:
- (a) the metric dropped — observation
- (b) X caused it — interpretation

The skill separates them before proceeding.

## Why Isolation

Diagnosticians do not see each other's output during generation. The same NGT research cited in the other `/think-*` skills applies: *coordinated* diagnosticians anchor on the first compelling cause and produce less distinct alternatives; *independent* diagnosticians across different lenses produce genuinely different candidates that the orchestrator can evaluate on their merits.

## Output

A structured report with:
- **Observations** — ground-truth evidence
- **Interpretations held aside** — what was set aside during diagnosis
- **Unavailable evidence** — what constrains conclusions
- **Leading candidate(s)** — 1-2 causes with strong fit; mechanism, evidence fit, plausibility, lens attribution
- **Other candidates** — moderate and weak-fit causes with brief reasoning
- **Distinguishing evidence** — concrete tests the user can run to distinguish among candidates (the most actionable part of the report)
- **What remains unknown** — honest uncertainty
- **Recommendation** — Act on leading / Gather evidence first / Phenomenon may not be real / Insufficient evidence

## Confidence Calibration

Qualitative categories only. No fabricated percentages.

| Category                 | Meaning                                                                            |
|--------------------------|------------------------------------------------------------------------------------|
| **Strong fit**           | Cause explains all observations; predictions confirmed; no refuters; plausible     |
| **Moderate fit**         | Cause explains most observations; some predictions unconfirmed but not contradicted |
| **Weak fit**             | Cause explains some observations; significant predictions unconfirmed              |
| **Unable to distinguish** | Two or more causes fit the evidence equally well; more evidence needed            |

Honest "can't distinguish" is a valuable outcome. Users can act on acknowledged uncertainty (by gathering more evidence); they can't protect themselves from false confidence.

## Iteration

The skill is **one-shot by design**. If the user gathers distinguishing evidence and wants an updated diagnosis, they re-invoke with the new evidence. Each invocation is a clean diagnostic consultation.

## Example Session

A non-code example, to demonstrate breadth:

```
> /think-diagnose Our quarterly product review meetings have gotten dramatically
  less useful over the past year. We cover fewer decisions per meeting, the
  energy is lower, and senior folks have started skipping. I want to understand
  why.

Before spawning diagnosticians, I need to separate what you've observed
from what you're already inferring about it. Let me ask:

1. "Less useful" — what specifically do you observe? Fewer decisions made?
   Decisions that get revisited later? People zoning out?
> Fewer decisions per meeting (measured: we used to close ~8 per meeting;
  now it's ~3). Senior skipping is about 40% now, was <10% a year ago.
  Retention of what was discussed is also worse anecdotally — people ask
  for context that was covered in the meeting.

2. Do you have any candidate explanations already?
> The team thinks it's because we grew from ~15 to ~35 attendees and the
  meeting got unwieldy. I think it might be that we stopped doing prep docs
  after the previous PM left.

3. What's NOT known / measurable?
> We don't have recordings. We don't track what specific decisions got
  deferred. We don't measure sentiment at the individual level.

Observations:
- Decisions closed per meeting: 8 → 3 over ~1 year
- Senior attendance: >90% → ~60%
- Anecdotal: participants re-asking for context that was covered

Interpretations held aside (not accepted as given):
- "It's because we grew from 15 to 35 attendees" (team's interpretation)
- "It's because prep docs stopped after PM turnover" (your interpretation)

Unavailable: recordings, per-decision tracking, individual sentiment

Lenses I'll apply: process, human-factors, incentive-structure,
measurement-artifact, temporal. Skipping technical (no engineering system),
environmental (no external factors identified), statistical (no aggregate
distribution at play).

[Spawning 5 diagnosticians in parallel...]
[Collecting candidate causes...]
[Evaluating fit against evidence...]

## Diagnosis Report

Phenomenon: Quarterly product review meetings have become substantially
less useful over the past year.
Lenses applied: process, human-factors, incentive-structure,
measurement-artifact, temporal

### Observations
- Decisions closed per meeting: 8 → 3 over ~1 year
- Senior attendance: >90% → ~60%
- Anecdotal: participants re-asking for context already covered

### Interpretations Held Aside
- "Growth from 15 to 35 attendees is the cause" (team)
- "Prep docs stopping after PM turnover is the cause" (you)

### Unavailable Evidence
- No meeting recordings
- No per-decision deferral tracking
- No individual sentiment data

### Leading Candidate — Strong Fit

#### Prep-doc discipline collapsed after PM turnover

**Mechanism:** Before turnover, meetings ran from written prep docs
distributed in advance. After turnover, prep shifted to verbal framing
at the start of each meeting. Senior folks (who read docs in advance)
lost their preferred engagement mode; participants (who arrived unprepared)
spend meeting time orienting instead of deciding; decisions-per-hour falls;
senior attendance erodes because the meeting is no longer efficient for
their time.

**Evidence fit:**
- Observations explained: decision throughput drop (prep-doc meetings close
  more per hour because everyone arrives oriented); senior attendance drop
  (prep-doc meetings favor dense-readers); re-asking for context (no
  pre-reading means people arrive at baseline)
- Predictions confirmed (inferred): the onset of the phenomenon should
  correlate with the PM turnover date. **Check this.** You said the PM
  left "previously" — if the phenomenon onset ≈ PM departure date, this
  is strong confirmation.
- Refuters: if the phenomenon predates PM turnover, this cause is wrong.
- No refuters observed in current evidence.

**Plausibility:** High. Prep-doc discipline is a well-known meeting-quality
factor; senior folks in particular are often dense-reading preppers;
turnover-driven process regressions are very common.

**Lens(es):** process (primary), temporal (supporting — turnover is a
change-point)

### Other Candidates

**Meeting size grew past effective ceiling** *(process, moderate fit)*
Growth from 15 to 35 attendees may independently reduce decision
throughput (more voices, harder to converge). But this wouldn't fully
explain senior attrition (they could attend fewer selectively). Likely
a contributing factor rather than root; may compound with prep-doc
collapse.

**Senior incentive shift** *(incentive-structure, weak fit)*
If senior folks started being rewarded more for other work, they'd
skip the meeting. Plausible but no supporting evidence in observations.
Would predict a correlated increase in other senior activity — check
if this exists.

**Measurement artifact** *(measurement-artifact, weak fit)*
"Decisions per meeting" could have changed how it's counted. But the
drop is large and senior-attendance drop is an independent signal —
unlikely to be pure measurement.

### Distinguishing Evidence

To distinguish **prep-doc collapse** from **meeting size**:
- Check: does the phenomenon onset align with PM turnover date, or with
  growth past ~25 attendees? If turnover date, prep-doc. If growth
  threshold, meeting size. If both happened at once, consider composite.

To test **prep-doc collapse** directly:
- Reinstate prep docs for one quarterly meeting. Compare decisions
  closed and senior attendance against recent trend. A one-meeting
  experiment would be informative.

To rule out **senior incentive shift**:
- Ask the senior folks who've been skipping: what are they prioritizing
  instead, and why?

### What Remains Unknown
- Whether meeting-size growth and prep-doc loss are coincident (the
  critical question for distinguishing top candidates)
- Whether senior incentives have shifted
- The user's interpretation (prep-doc collapse) has strong support; the
  team's interpretation (meeting size) has moderate support. Both may
  be contributing.

### Recommendation
**Gather distinguishing evidence first.** The leading candidate
(prep-doc collapse) has strong fit, but the team's interpretation
(meeting size) has moderate fit and the two may be compounded. Before
acting, confirm which is primary by checking (a) the phenomenon's
onset date against the PM turnover date and (b) running one meeting
with reinstated prep docs to test.

### Suggested Next Steps

- To gather distinguishing evidence: confirm turnover date vs. phenomenon
  onset date; try one meeting with reinstated prep docs
- To design a remediation once cause is confirmed: `/think-brainstorm`
- To pressure-test the planned intervention: `/think-scrutinize`
```

## Relationship to Other Skills

| Skill                | Relationship                                                                          |
|----------------------|---------------------------------------------------------------------------------------|
| `/bug-fix`           | Code-specific diagnosis with artifact output; `/think-diagnose` is non-code, abstract |
| `/think-brainstorm`  | Natural downstream — brainstorm remediations for the diagnosed cause                  |
| `/think-scrutinize`  | Pressure-test either the diagnosis or the planned intervention                         |
| `/think-reframe`     | If the phenomenon itself seems off, consider reframing before diagnosing              |

**Natural pipeline (non-code phenomena):**

```
/think-diagnose → /think-brainstorm → /think-deliberate → /think-scrutinize
     why?            what to do?        which approach?     what's wrong?
```

## Philosophy

Diagnosis is hard because compelling narratives beat correct ones. Humans prefer causes that tell a good story — they feel explanatory. Good abductive reasoning resists this: the most likely cause is the one that *best fits the evidence*, not the one that makes the cleanest story.

The enforced observation-vs-interpretation split is the skill's most important contribution. Most bad diagnoses begin by accepting an interpretation as if it were an observation — "the metric dropped because of X" sneaks the causal claim into the description of what happened. Once that interpretation is treated as fact, no diagnostician will challenge it, and the diagnosis inherits the error. By forcing the split upfront, the skill keeps the evidence space open for genuinely distinct causes.

Honest uncertainty is the other key discipline. "I don't know for sure" is often the correct output when evidence is thin — and it's far more useful than a confident-sounding but brittle conclusion. Users can act on acknowledged uncertainty (by gathering more evidence); they can't protect themselves from false confidence.
