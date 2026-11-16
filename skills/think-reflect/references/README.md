# /think-reflect - Retrospective Learning from Completed Experience

## Overview

`/think-reflect` extracts learnings from something that already happened: a project that shipped, an incident that resolved, a decision that played out, a period that ended. It separates recorded ground truth from recollection and loads the records you point it to. Reflection lenses then run as isolated parallel agents, and the synthesis leads with **updated mental models**: changed beliefs about how the world works.

It counters the narrative fallacy and luck mistaken for skill. Memory drifts toward coherent stories; the git log doesn't. The lineage is Schön's reflective practice and Kerth's structured retrospectives, with Taleb and Tetlock for process-vs-luck and decision-vs-outcome attribution. The namespace-wide rationale lives in [`references/think.md`](../../../references/think.md).

The step-by-step procedure lives in [`SKILL.md`](../SKILL.md); this guide covers when to use the skill and what to expect.

Most retrospectives produce a tidy document and update nobody's beliefs. This skill treats a reflection that changes no belief as a failure, unless it honestly reports that no belief needed to change. It produces feedback only: no code, no tickets, no artifacts.

## When to Use

**Use `/think-reflect` for:**
- Post-project retrospectives
- Post-incident reflection, once the incident has resolved
- End-of-quarter or end-of-year structured reflection
- Calibration after a significant decision has played out
- Understanding a pattern that keeps recurring

**Don't use `/think-reflect` for:**
- In-flight experiences (reflection works best on bounded, completed ones)
- A decision being made now (use `/think-deliberate`)
- Diagnosing a current phenomenon (use `/think-diagnose`)
- Finding bugs (use `/bug-fix` or `/bug-hunt`)
- Generating forward plans (use `/think-brainstorm`; reflection informs it but is a distinct step)

**Rule of thumb:** "What did I learn?" → `/think-reflect`. "What should I do?" → a different skill.

`/think-reflect` and `/think-premortem` are a matched pair on the time axis: pre-mortem before the fact, reflect after. Typical follow-ups: `/think-brainstorm` to design interventions, `/think-diagnose` for a recurring failure mode, `/think-scrutinize` to stress-test a plan derived from the learnings.

## Flow

```
Scope the experience → Gather ground truth (with you) → Choose lenses
  → Reflectors (parallel, isolated) → Synthesize → Report
```

**Ground-truth gathering is interactive.** Expect questions that sort what you know into three buckets: *observations* (what was recorded: git history, logs, metrics, design docs, postmortems, notes), *recollections* (what people remember, flagged as memory), and *gaps* (unknown and unrecorded). The skill asks for records and loads them, whether file paths, links, pastes, or commit ranges. It also pushes back on judgments presented as facts. "The launch went well" prompts the question: what was actually measured? Where memory and record disagree, the record wins and the disagreement is reported.

## Reflection Lenses

The skill picks 3–6 lenses that fit the experience and drops the rest. When the outcome was positive, what-worked-vs-got-lucky is always included.

| Lens                     | Extracts                                                         |
| ------------------------ | ---------------------------------------------------------------- |
| what-worked-vs-got-lucky | Attribution honesty for positive outcomes (process win vs. luck) |
| what-didn't              | Blameless failure-mode identification                            |
| what-surprised           | Surprises as signal; candidate mental-model updates              |
| system-rewards-vs-intent | Goodhart gaps: what was rewarded vs. what was intended           |
| decisions-that-aged      | Decision quality, separated from outcome quality                 |
| what-to-tell-past-self   | Forward-applicable advice derived from hindsight                 |
| patterns-that-recur      | Connections to prior experiences; one-off vs. recurring          |

## What You Get Back

- **Updated Mental Models** (headline): each written as *previously* → *experience suggests* → *updated belief*, with confidence in the update
- **What Happened**: an observation-based summary, noting where recollection diverged
- **What Worked, and Why**: each outcome labeled process win, lucky, or mixed
- **What Didn't Work**: blameless failure-mode analysis
- **Decisions in Retrospect**: a decision-quality grid (good / fortunate / unfortunate / bad)
- **What Surprised Us**, **System Rewards vs. Intent**, **Advice to Past-Self**, **Recurring Patterns**: as the chosen lenses warrant
- **Gaps in the Record**: what to capture next time
- **Suggested Next Steps**

The skill is one-shot. Re-invoke for a different experience.

## Example Session

```
> /think-reflect We shipped the new payments pipeline 6 months ago. I want to
  reflect on design decisions, rollout, and what happened versus what we expected.

1. What's recorded?
> Design doc in Notion. Full git history. Two incidents have Jira postmortems.
  Latency + error-rate dashboards from before launch. No formal retro notes.

2. What do you remember that might not be captured?
> The migration felt stressful, but I'm not sure that was unusual. We debated
  event-sourcing early on; I don't remember all the tradeoffs.

3. What's genuinely unknown?
> Whether cutting two features mid-project was right.

[Loading design doc, git log, postmortems, dashboards...]

Observations: event-sourcing chosen; 247 commits over 4 months; 2 postmortems
(capacity, data-shape); p99 latency -35% post-launch, error rate unchanged.
Recollections (memory): migration felt stressful; early tradeoff debate.
Gaps: no retro notes; morale not tracked; tradeoff reasoning not written down.

Lenses: what-worked-vs-got-lucky, what-didn't, what-surprised,
decisions-that-aged, what-to-tell-past-self. Skipping system-rewards-vs-intent
(no Goodhart signal) and patterns-that-recur (no prior similar experience).

## Reflection Report

### Updated Mental Models

1. **Event-sourcing readiness for the team**
   - Previously: event-sourcing fits when you need audit trail and replay.
   - Experience suggests: necessary but not sufficient. Commits tagged
     "re-thinking X" cluster in months 2–3, while the team was still learning
     the paradigm; this matches the recalled stress.
   - Updated belief: include a team-readiness assessment; if readiness is low,
     plan 2–3 months of learning overhead or reconsider.
   - Confidence: moderate. One experience, but observation and recollection agree.

2. **Mid-project scope cuts**
   - Previously: a sign of poor scoping.
   - Experience suggests: both cut features were ambiguous in the design doc,
     and production has been stable without them.
   - Updated belief: cutting ambiguous features is healthy; carrying them into
     implementation is the real failure.
   - Confidence: moderate.

### What Worked, and Why

- **Scope cuts — Process win:** driven by identified ambiguity; transferable.
- **Latency -35% vs. 20% target — Mixed, leaning lucky:** the excess came from
  structural inefficiency in the old system nobody had modeled. Don't
  extrapolate.

### Decisions in Retrospect

- **Choose event-sourcing:** good decision; sound match given what was knowable.
- **Not tracking morale:** bad decision, made implicitly. It is why the
  "stressful" recollection can't be validated now.

### Gaps in the Record

- Morale signal; written tradeoff reasoning; a post-launch retro
```

The instructive part is the attribution. The best outcome (latency) was labeled mostly luck. The commit history, not the recalled stress, carried the main mental-model update.
