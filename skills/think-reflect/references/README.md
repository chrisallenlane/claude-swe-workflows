# /think-reflect - Retrospective Learning from Completed Experience

## Overview

The `/think-reflect` skill extracts learnings from something that already happened — a project that shipped, an incident that resolved, a decision that played out, a time period that ended. It gathers ground truth (observations) separately from recollections (memory), spawns parallel reflectors applying different lenses in isolation, and synthesizes the pool into a report whose headline output is **updated mental models** — changed beliefs about how the world works.

**Key properties:**
- Structurally different from the other `/think-*` skills: input is a past experience, not a decision-to-make
- Enforced observation/recollection split (memory drifts toward coherent stories)
- Active loading of external sources (logs, timelines, meeting notes, git history) as first-class input
- Multiple reflection lenses in parallel — isolated to avoid anchoring
- Headline output is mental-model updates, not a findings document
- Luck vs. process attribution is made explicit (conflating them reinforces bad processes)
- Produces feedback only — no code, no tickets, no artifacts

## When to Use

**Use `/think-reflect` for:**
- Post-project retrospectives (project has shipped, learnings needed)
- Post-incident reflection (incident resolved, want to update mental models)
- End-of-quarter / end-of-year structured reflection
- Calibration after a significant decision has played out
- Investigating a pattern that keeps recurring
- Personal reflection on a time period or role

**Don't use `/think-reflect` for:**
- In-flight experiences (reflection works on bounded, completed experiences)
- Decision support for a decision being made now (use `/think-deliberate`)
- Diagnosing a current phenomenon (use `/think-diagnose`)
- Finding bugs (use `/bug-fix` or `/bug-hunt`)
- Generating forward plans (use `/think-brainstorm` — reflection *informs* brainstorming but is distinct)

**Rule of thumb:**
- "What did I learn?" → `/think-reflect`
- "What should I do?" → a different skill

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ /think-reflect Workflow                                     │
└─────────────────────────────────────────────────────────────┘

 ┌──────────────────────────────────────────────┐
 │  1. SCOPE THE EXPERIENCE                     │
 │  ────────────────────────────────────────    │
 │  • What's being reflected on?                │
 │  • Start point, end point                    │
 │  • What's in scope, what's out                │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  2. GATHER GROUND TRUTH                      │
 │  ────────────────────────────────────────    │
 │  Three-bucket split:                         │
 │  • Observations (recorded ground truth)      │
 │  • Recollections (memory, flagged)           │
 │  • Gaps (unknown / unrecorded)               │
 │                                              │
 │  Actively load external sources              │
 │  (logs, timelines, meeting notes, git)       │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  3. CHOOSE REFLECTION LENSES                 │
 │  ────────────────────────────────────────    │
 │  What-worked-vs-got-lucky / What-didn't /    │
 │  What-surprised / System-rewards-vs-intent / │
 │  Decisions-that-aged / What-to-tell-past-self│
 │  / Patterns-that-recur                        │
 │  (3-6 selected; irrelevant ones dropped)     │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  4. SPAWN REFLECTORS (parallel, isolated)    │
 │  ────────────────────────────────────────    │
 │  One agent per lens                          │
 │  No cross-talk (NGT — avoids anchoring)      │
 │  Prefer observation over recollection when   │
 │  they conflict                               │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  5. SYNTHESIZE                               │
 │  ────────────────────────────────────────    │
 │  • Cluster learnings across lenses           │
 │  • Extract updated mental models             │
 │    (first-class output)                       │
 │  • Distinguish process wins from luck         │
 │  • Note observation/recollection gaps        │
 │  • Identify recurring patterns               │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  6. REPORT                                   │
 │  ────────────────────────────────────────    │
 │  Updated Mental Models (HEADLINE) /          │
 │  What Happened / What Worked (attributed) /  │
 │  What Didn't / Decisions in Retrospect /     │
 │  Surprises / Goodhart gaps / Advice to       │
 │  Past-Self / Recurring patterns / Gaps       │
 └──────────────────────────────────────────────┘
```

## Roles

| Role          | What they do                                                                  |
|---------------|-------------------------------------------------------------------------------|
| Judge (you)   | Scope experience, gather ground truth, choose lenses, synthesize models       |
| Reflectors    | Extract learnings through assigned lenses, in isolation                        |

## Reflection Lenses

The orchestrator selects lenses based on what the experience affords:

| Lens                          | Extracts                                                                |
|-------------------------------|-------------------------------------------------------------------------|
| what-worked-vs-got-lucky      | Attribution honesty for positive outcomes (process win vs. luck)         |
| what-didn't                   | Blameless failure-mode identification                                    |
| what-surprised                | Surprises as signal; candidate mental-model updates                      |
| system-rewards-vs-intent      | Goodhart gaps; what was actually rewarded vs. what was intended           |
| decisions-that-aged           | Decision-quality calibration, separated from outcome quality              |
| what-to-tell-past-self        | Forward-applicable advice derived from hindsight                         |
| patterns-that-recur           | Connections to prior experiences; one-off vs. recurring                   |

3-6 lenses is typical. Drop lenses that don't fit — forcing an unfit lens produces noise. **Always include what-worked-vs-got-lucky when the experience had positive outcomes** — mistaking luck for process is among the most damaging reflection failures.

## The Observation / Recollection Split

This is the skill's second-most-important contribution (after surfacing mental-model updates). Memory is reconstructive: it drifts toward coherent stories, smooths over contradictions, and attributes outcomes to the narratives that fit best.

The skill forces three buckets during ground-truth gathering:

- **Observations** — recorded during the experience: git history, deployment logs, metrics, meeting notes, decision documents, ticket updates, Slack threads. Concrete.
- **Recollections** — what the user or others *remember*. Flagged as memory, not observation. Valid input, but less authoritative when they conflict with observations.
- **Gaps** — unknown because nothing was recorded and nobody remembers clearly.

Reflectors receive all three, with flags preserved. When observations and recollections conflict, reflectors prefer observations and note the divergence. The gap between memory and record is itself a learning about how we perceive our own experience.

## External Sources

Unlike other `/think-*` skills, `/think-reflect` benefits from actively loading external records. The orchestrator should solicit and accept:
- File paths to meeting notes, decision docs, incident write-ups
- Links to ticket histories, PRs, deployment logs
- Pasted excerpts the user wants included
- Git commit ranges (`git log <range>`) as context

These become observational ground truth and anchor the reflection against memory.

## Updated Mental Models — The Headline

Most retrospectives produce tidy documents and update no beliefs. That's the failure mode this skill exists to avoid.

Updated mental models are surfaced as the **first** section of the report. Each update is structured as:

- **Previously:** the old mental model
- **Experience suggests:** what this experience indicates
- **Updated belief:** the new or refined mental model
- **Confidence in update:** honest about how well-supported by evidence

A model update is valuable even when it's small: "I used to think our test suite was reliable; this experience suggests it's reliable for CRUD changes but not integration changes" is a real calibration that changes future behavior. A findings list that produces no such updates has taught nothing.

## Output

A structured report with:
- **Updated Mental Models** (headline) — beliefs to carry forward
- **What Happened** — observation-based ground truth summary
- **What Worked — and Why** — attributed as process win, lucky, or mixed
- **What Didn't Work** — blameless failure-mode analysis
- **Decisions in Retrospect** — quality grid (good/fortunate/unfortunate/bad)
- **What Surprised Us** — unexpected observations with replaced beliefs
- **System Rewards vs. Intent** — Goodhart gaps identified
- **Advice to Past-Self** — forward-applicable
- **Recurring Patterns** — connections to prior experiences
- **Gaps in the Record** — what future retrospectives would benefit from capturing

## Iteration

The skill is **one-shot by design**. Each experience gets one clean consultation. To reflect on a different experience, re-invoke. To go deeper on a specific finding, use the appropriate downstream skill (`/think-diagnose` for a causal question, `/think-brainstorm` for intervention design, `/think-scrutinize` for stress-testing a plan).

## Example Session

```
> /think-reflect We shipped the new payments pipeline 6 months ago. It's
  been running in production since then. I want to reflect on what we
  learned — design decisions, rollout approach, what actually happened
  versus what we expected.

Let me scope the experience first.

Scope brief:
- Experience: payments pipeline rewrite
- Start: planning phase (when?)
- End: today, 6 months post-launch
- In scope: design decisions, rollout approach, production behavior, team
  dynamics during the project
- Out of scope: ongoing operations beyond the initial 6 months

Is that accurate?
> Yes. Planning started ~10 months ago.

Before I spawn reflectors, I need to separate what was recorded during the
experience from what you remember about it. A few questions:

1. What's recorded? Design docs? PR history? Incident reports? Retrospective
   notes? Deployment logs? Metrics before/after?
> Design doc in Notion. Full git history. Two incidents have Jira postmortems.
  We have latency + error-rate dashboards going back before launch. No formal
  retro notes.

2. What do you remember about it that might not be captured?
> The team's energy during the migration — it felt stressful but I'm not sure
  how much of that was actually unusual. I also remember us debating the
  event-sourcing approach early on, but I don't remember all the tradeoffs.

3. What's genuinely unknown?
> Whether the original scope was right. We cut two features mid-project; I
  don't know if that was correct.

[Loading Notion design doc, git log, Jira postmortems, dashboards...]

Observations (loaded):
- Design doc: chose event-sourcing architecture, noted trade-offs
- Git: 247 commits over 4 months active development, 3 contributors
- Jira: 2 postmortems — one capacity-related, one data-shape related
- Metrics: p99 latency dropped 35% post-launch; error rate unchanged

Recollections (flagged as memory):
- Team felt the migration was stressful
- Early debate about event-sourcing tradeoffs (details forgotten)
- Uncertainty about whether cutting 2 features was correct

Gaps:
- No formal retrospective notes
- Team energy / morale wasn't tracked
- Tradeoff discussion on event-sourcing wasn't captured in writing

Lenses I'll apply: what-worked-vs-got-lucky (positive outcome needs attribution
check), what-didn't (2 postmortems indicate failures to examine), what-surprised
(likely rich here — 6 months of production will have produced surprises),
decisions-that-aged (design doc preserved specific decisions to review),
what-to-tell-past-self (user is explicitly asking for this).

Skipping system-rewards-vs-intent (no clear Goodhart signal in the observations)
and patterns-that-recur (no prior similar experiences mentioned).

[Spawning 5 reflectors in parallel...]
[Collecting reflections...]
[Synthesizing...]

## Reflection Report

Experience: Payments pipeline rewrite — 10-month project, 6 months
post-launch in production.
Lenses applied: what-worked-vs-got-lucky, what-didn't, what-surprised,
decisions-that-aged, what-to-tell-past-self

### Updated Mental Models

1. **Event-sourcing readiness for the team**
   - Previously: Event-sourcing is appropriate when you need audit trail
     and replay capability
   - Experience suggests: Those properties are necessary but not sufficient;
     the team needs to have internalized event-driven mental models *before*
     the project starts. The team's stress during the migration correlates
     with the git-log pattern of rework (commits tagged "re-thinking X" are
     concentrated in months 2-3, when the team was still learning the
     paradigm).
   - Updated belief: Event-sourcing decisions should include an explicit
     team-readiness assessment; if readiness is low, plan for 2-3 months
     of learning overhead or reconsider the approach.
   - Confidence: Moderate — one experience, but the signal is clear from
     both observation (rework concentration) and recollection (stress).

2. **Scope cuts during active development**
   - Previously: Cutting features mid-project is a project-management
     failure or a sign of poor scoping.
   - Experience suggests: The two features cut both had ongoing ambiguity
     in the design doc. Cutting them mid-project let the team focus on the
     remaining well-defined work. Production has been stable without them.
   - Updated belief: Mid-project scope cuts on ambiguous features are
     healthy, not failure; the real failure is carrying ambiguous features
     into implementation in the first place.
   - Confidence: Moderate — one instance, but the outcome has been robust
     for 6 months.

3. **Pre-launch metric targets vs. post-launch reality**
   - Previously: We set latency-reduction targets based on our best model
     of the system; if we hit the target, the model was right.
   - Experience suggests: We overshot our latency target (35% vs. 20%)
     because we underestimated how much the old system's design was
     constraining the metric. The model of "the old system was fine,
     just needed rewriting cleanly" was wrong; the old system had
     structural latency baked in.
   - Updated belief: When replacing a system, underestimate the
     outperformance of the replacement unless you've specifically modeled
     the old system's structural limits.
   - Confidence: High — the metric outcome is concrete and the
     retrospective analysis is clear.

### What Happened (Ground Truth)

10-month project: 6 months planning/design, 4 months active development,
now 6 months in production. Event-sourcing architecture chosen during
design. Two originally-planned features cut mid-development. 247 commits,
3 contributors. Two post-launch incidents (capacity, data-shape). Latency
reduction 35% post-launch; error rate unchanged.

### What Worked — and Why

- **Architecture decision (event-sourcing) — Mixed:** The architecture was
  right for the problem, but the team's learning overhead was substantial.
  Partial process win (correct architectural match), partial luck (team
  absorbed the learning overhead without blowing the timeline by more than
  expected).
- **Scope cuts of 2 features — Process win:** The cuts were driven by
  ambiguous design. Identifying and cutting ambiguous work is a transferable
  process.
- **Latency outcome (35% improvement) — Mixed leaning lucky:** The target was
  20%; we hit 35%. The excess is attributable to structural inefficiency in
  the old system that we hadn't specifically modeled. A clean-rewrite
  approach doesn't guarantee 35%; the old system happened to be structurally
  suboptimal. Don't extrapolate.

### What Didn't Work

- **Capacity incident (postmortem reviewed):** Load testing didn't cover the
  write-amplification pattern that event-sourcing produces at scale. This is
  a blameless failure mode — the team knew event-sourcing amplified writes
  but didn't translate that into a specific load-test scenario.
- **Data-shape incident (postmortem reviewed):** A downstream consumer
  assumed an event shape that wasn't guaranteed by the contract. The schema
  enforcement was too loose; the team trusted the convention rather than
  the schema.

### Decisions in Retrospect

- **Choose event-sourcing** — **Good decision.** Correct given what was
  knowable; architectural match to the problem was sound. Outcome was
  better-than-even despite team learning overhead.
- **Set latency target at 20%** — **Fortunate decision.** Target was
  conservative but defensible; actual outcome exceeded it. Would look
  overly conservative in hindsight but was appropriate given information
  at the time.
- **Cut 2 features mid-project** — **Good decision.** Correct given the
  design ambiguity at the point of cutting.
- **Not tracking team energy / morale** — **Bad decision** (implicit rather
  than explicit, but this is the gap that makes it hard now to validate the
  "stressful" recollection). Future projects should have a lightweight
  morale signal.

### What Surprised Us

- Latency improvement exceeded target by 75% — contradicts the belief that
  the old system was "basically fine." (See Mental Model #3.)
- The two cut features have not been missed in production — contradicts the
  belief that features in the design doc were all load-bearing.
- Team learning overhead was the biggest source of rework — contradicts the
  belief that "senior engineers can adopt new paradigms quickly."

### Advice to Past-Self

- **At month 0:** Assess team familiarity with event-sourcing explicitly;
  plan learning time in the schedule rather than absorbing it through
  overtime.
- **At month 2:** The rework you're doing is paradigm adjustment, not poor
  planning. Don't interpret it as failure; it's expected.
- **At month 4:** When tempted to carry ambiguous features into
  implementation, cut instead. The two features you cut will not be missed.
- **Always:** Track morale signal lightly, even informally. You'll want it
  when you reflect.

### Gaps in the Record

- No morale / team-energy tracking during the project
- Early event-sourcing tradeoff discussion wasn't captured in writing (the
  decision was captured; the reasoning was lost)
- No formal retrospective done post-launch — this reflection is the first

### Suggested Next Steps

- Internalize the three mental-model updates above — they should shape
  future architecture decisions, scope management, and metric-setting
- To design a learning-overhead tracking approach for future projects:
  `/think-brainstorm`
- To diagnose why event-sourcing adoption was more costly than expected:
  `/think-diagnose` (if the question becomes "what specifically made the
  learning curve steep?")
```

## Relationship to Other Skills

| Skill                | Relationship                                                                        |
|----------------------|-------------------------------------------------------------------------------------|
| `/think-brainstorm`  | Natural downstream — if reflection surfaces actionable themes, brainstorm interventions |
| `/think-diagnose`    | Natural downstream — if reflection surfaces a recurring failure mode, diagnose its cause |
| `/think-scrutinize`  | Natural downstream — stress-test an intervention derived from reflection             |
| `/bug-fix`           | If a reflected-on failure is in code, `/bug-fix` investigates it                    |

**Reflection does not replace these skills; it informs them.** A mental-model update is a changed belief, not an action plan. The action comes from downstream skills operating on the updated beliefs.

## Philosophy

Retrospectives are universally skipped or done as ritual theater. A tidy document gets produced; nobody's beliefs update; the next project runs the same way. This is the failure mode `/think-reflect` exists to avoid.

**The value of reflection is updated mental models, not a findings document.** A model-update is valuable even when it's small: "I used to think our test suite was reliable; this experience suggests it's reliable for CRUD but not integration" is a real calibration that changes future behavior. A findings report that updates no beliefs has taught nothing.

**The enforced observation-vs-recollection split is the other key discipline.** Memory reconstructs coherent narratives; the git log doesn't. When they disagree, prefer the observation — and note the disagreement. The gap is itself a learning.

**Luck and process must stay separate.** A good outcome from a bad process reinforces the bad process. A bad outcome from a good process looks like process failure. Attributing honestly — even when uncomfortable — is the foundation of every other learning.
