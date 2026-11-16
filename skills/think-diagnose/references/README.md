# /think-diagnose - Abductive Reasoning About Causes

## Overview

`/think-diagnose` works out *why* something is happening. Given a phenomenon, it separates what was observed from what is already believed about it. It then runs several reasoning lenses as isolated parallel diagnosticians, and judges each candidate cause on how well it fits the evidence. When several candidates survive and the evidence can't separate them, it narrows them by Analysis of Competing Hypotheses. The result is the leading candidates and the specific tests that would tell them apart.

It counters narrative preference: a cause with a clean story feels explanatory even when it fits the evidence poorly. The lineage is Peirce's abduction (inference to the best explanation) plus Richards Heuer's ACH (*Psychology of Intelligence Analysis*, 1999), which ranks hypotheses by what *disconfirms* them rather than what fits. The namespace-wide rationale lives in [`references/think.md`](../../../references/think.md).

The step-by-step procedure lives in [`SKILL.md`](../SKILL.md); this guide covers when to use the skill and what to expect.

It works on non-code phenomena as readily as code ones. It produces feedback only: no code, no tickets, no artifacts.

## When to Use

**Use `/think-diagnose` for:**
- Unexplained metric changes ("why did engagement drop?")
- Recurring problems with unclear cause ("why does this project keep slipping?")
- Behavioral patterns ("why do customer calls go badly when X happens?")
- Organizational issues ("why does our goal-setting keep producing missed goals?")
- Anywhere `/bug-fix` doesn't apply because the phenomenon isn't code-specific
- Rigorously narrowing several explanations you already have. Pass them in as interpretations, and the narrowing step takes over if they don't separate.

**Don't use `/think-diagnose` for:**
- Code-specific diagnosis (use `/bug-fix`, which has artifact output and execution tooling)
- Choosing between known options (use `/think-deliberate`)
- Stress-testing a chosen plan (use `/think-scrutinize`)
- Generating remediations (use `/think-brainstorm` *after* diagnosis)
- Phenomena so vaguely described that no observations exist (refine the phenomenon first)

**Rule of thumb:**
- "Why is this happening?" → `/think-diagnose`
- "Code is broken, find and fix it" → `/bug-fix`
- "What could I do about this?" → `/think-brainstorm`

**Natural pipeline (non-code phenomena):** `/think-diagnose` → `/think-brainstorm` → `/think-deliberate` → `/think-scrutinize` (why? → what to do? → which approach? → what's wrong?).

## Flow

```
Receive phenomenon → Gather evidence (with you) → Choose lenses
  → Diagnosticians (parallel, isolated) → Evaluate fit and calibrate
  → [Narrow by ACH, if candidates won't separate] → Report
```

**Evidence gathering is interactive, and it is the step that matters most.** Expect a few questions that sort what you know into three buckets: *observations* (what was measured or seen), *interpretations already held* (what you or others have inferred), and *unavailable evidence*. If you say "the metric dropped because of the migration," the skill will split that into an observation and an interpretation. Your interpretations are held aside so they don't anchor the diagnosticians. They come back as hypotheses if narrowing runs.

**Narrowing runs only when it's warranted.** Three conditions must hold: three or more candidates reach moderate fit or better, or an "unable to distinguish" tie remains; evidence exists, or can be gathered, to discriminate among them; and the candidates make different predictions. Otherwise the report says in one line why it was skipped. When it runs, it adds a null hypothesis, and a deceptive one when manipulation is plausible. Evidence-gatherers then work across evidence classes (direct-observational, documentary-historical, structural, behavioral, absent, anomalous), and hypotheses are ranked by least disconfirming evidence.

Before v12, ACH was a separate skill, `/think-ach`. For a non-causal question of that shape, such as attribution among actors, frame the competing explanations as the phenomenon's candidates.

## Reasoning Lenses

The skill picks 3–6 lenses that fit the phenomenon and drops the rest. Measurement-artifact is always included for metric-based phenomena.

| Lens                 | Surfaces causes rooted in                                         |
| -------------------- | ----------------------------------------------------------------- |
| technical            | Engineering systems (code, infra, config, capacity)               |
| human-factors        | People, skills, fatigue, turnover, miscommunication               |
| process              | Broken or missing process, handoffs, ownership, rituals           |
| incentive-structure  | The system rewards the observed behavior (Goodhart)               |
| environmental        | External factors (market, regulation, vendors, customer mix)      |
| temporal             | Change-points that correlate with the phenomenon                  |
| measurement-artifact | The phenomenon isn't real; it's an instrumentation issue          |
| statistical          | Base rates, regression to mean, Simpson's, selection, confounders |

## What You Get Back

- **Observations**, **Interpretations Held Aside**, **Unavailable Evidence**: the evidence split
- **Leading Candidate(s)**: 1–2 strong-fit causes, each with mechanism, evidence fit (observations explained, predictions, refuters), plausibility, and lens attribution
- **Other Candidates**: moderate- and weak-fit causes, briefly
- **Narrowing**: if it ran, the hypotheses, the consistent/inconsistent matrix, diagnosticity, a least-disconfirmation leaderboard, and sensitivity; otherwise one line saying why it was skipped
- **Distinguishing Evidence**: concrete checks that would separate the leading candidates. This is the most actionable section.
- **What Remains Unknown**
- **Recommendation**: act on the leading candidate / gather distinguishing evidence first / the phenomenon may not be real / insufficient evidence

Fit is reported as strong, moderate, weak, or unable to distinguish, with no percentages. "Can't distinguish" is a legitimate result. The skill is one-shot: gather the distinguishing evidence and re-invoke for an updated diagnosis.

## Example Session

A non-code example, to show breadth:

```
> /think-diagnose Our quarterly product review meetings have gotten dramatically
  less useful over the past year. Senior folks have started skipping.

1. "Less useful" — what specifically do you observe?
> We used to close ~8 decisions per meeting; now ~3. Senior skipping is ~40%,
  was <10% a year ago. People re-ask for context covered in the meeting.

2. Do you have candidate explanations already?
> The team thinks it's growth from ~15 to ~35 attendees. I think it's that
  we stopped doing prep docs after the previous PM left.

3. What's NOT known?
> No recordings, no per-decision tracking, no individual sentiment data.

Interpretations held aside (not accepted as given):
- "Growth from 15 to 35 attendees" (team)
- "Prep docs stopped after PM turnover" (you)

Lenses: process, human-factors, incentive-structure, measurement-artifact,
temporal. Skipping technical, environmental, statistical.

## Diagnosis Report

### Leading Candidate — Strong Fit

#### Prep-doc discipline collapsed after PM turnover

**Mechanism:** Without prep docs, participants spend meeting time orienting
instead of deciding; senior folks lose their preferred engagement mode and
stop attending.

**Evidence fit:** explains all three observations. Prediction: onset should
align with the PM's departure. **Check this.** Refuter: onset predates it.

### Other Candidates

**Meeting size grew past effective ceiling** *(process, moderate fit)*
Explains lower throughput but not senior attrition. Likely contributing.

**Measurement artifact** *(weak fit)* Senior attendance is an independent
signal, so the drop is unlikely to be pure counting change.

### Narrowing

Skipped: only two candidates reached moderate fit or better, with no tie;
the distinguishing checks below separate them directly.

### Distinguishing Evidence

- Does onset align with the PM turnover date, or with growth past ~25
  attendees? Turnover → prep-doc. Growth threshold → meeting size.
- Reinstate prep docs for one meeting; compare decisions closed and senior
  attendance against trend.

### Recommendation

**Gather distinguishing evidence first.** The two candidates may compound;
confirm which is primary before acting.
```

The instructive part is the evidence split. Both explanations already on the table were held aside, so the diagnosticians generated candidates independently. The report then names the single check that separates the top two.
