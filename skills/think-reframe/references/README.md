# /think-reframe - Problem Redefinition Before Problem Solving

## Overview

The `/think-reframe` skill stress-tests how a problem is framed before anyone tries to solve it. It extracts the premises embedded in the stated problem, then spawns parallel reframers applying different lenses in isolation (problem-vs-symptom, scope-shift, stakeholder-shift, etc.), and synthesizes the alternatives into a report with a clear recommendation: keep the original framing, adopt a specific reframing, or explore further.

**Key properties:**
- Runs upstream of `/think-brainstorm` — ensures you brainstorm the right problem
- Multiple lenses in parallel — different framings catch different miscasts
- Isolated reframers — no anchoring across agents (Nominal Group Technique)
- Honest "original framing holds up" is a valid outcome — it's calibration signal
- Produces feedback only — no code, no tickets, no artifacts

## When to Use

**Use `/think-reframe` for:**
- Pre-brainstorm pressure test: before generating approaches, is this the right problem?
- Stuck problems: when conventional approaches aren't working, often the framing is off
- High-stakes decisions: worth the cost of reframing before committing
- Problems debated without convergence: often the debate is really about framing, not solutions

**Don't use `/think-reframe` for:**
- Generating approaches (use `/think-brainstorm`)
- Choosing between options (use `/think-deliberate`)
- Stress-testing a chosen approach (use `/think-scrutinize`)
- Trivial problems where reframing is disproportionate effort
- Problems so vague that no framing exists yet (refine the problem first)

**Rule of thumb:**
- "Am I solving the right problem?" → `/think-reframe`
- "What could I do about this problem?" → `/think-brainstorm`
- "Which of these options is best?" → `/think-deliberate`
- "What's wrong with this plan?" → `/think-scrutinize`

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ /think-reframe Workflow                                     │
└─────────────────────────────────────────────────────────────┘

 ┌──────────────────────────────────────────────┐
 │  1. RECEIVE THE PROBLEM                      │
 │  ────────────────────────────────────────    │
 │  • From context, document, or user input     │
 │  • Produce a written brief                   │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  2. EXTRACT PREMISES                         │
 │  ────────────────────────────────────────    │
 │  • Stated + unstated premises                │
 │  • Implied scope, category, stakeholders     │
 │  • Implied time horizon                      │
 │  (Reconnaissance, not confrontation)         │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  3. CHOOSE REFRAMING LENSES                  │
 │  ────────────────────────────────────────    │
 │  Problem-vs-symptom / Scope-shift /          │
 │  Stakeholder-shift / Level-of-abstraction /  │
 │  Time-horizon / Inversion / Category-shift / │
 │  Constraints-shift                           │
 │  (3-6 selected; irrelevant ones dropped)     │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  4. SPAWN REFRAMERS (parallel, isolated)     │
 │  ────────────────────────────────────────    │
 │  One agent per lens                          │
 │  No cross-talk (NGT — avoids anchoring)      │
 │  Each returns: reframed problem + diff +     │
 │  "when this framing applies"                 │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  5. SYNTHESIZE                               │
 │  ────────────────────────────────────────    │
 │  • Assess meaning-shift per reframing        │
 │  • Construct composite framings (optional)   │
 │  • Identify standout reframings              │
 │  • Form orchestrator recommendation          │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  6. REPORT                                   │
 │  ────────────────────────────────────────    │
 │  Original framing / Standout reframings /    │
 │  Composite framings / Refinements /          │
 │  Where original held up / Recommendation     │
 └──────────────────────────────────────────────┘
```

## Roles

| Role          | What they do                                                             |
|---------------|--------------------------------------------------------------------------|
| Judge (you)   | Capture problem, extract premises, choose lenses, synthesize report      |
| Reframers     | Restate the problem through assigned lenses, in isolation                |

## Reframing Lenses

The orchestrator selects lenses based on the problem's shape. Common lenses:

| Lens                  | Asks                                                                      |
|-----------------------|---------------------------------------------------------------------------|
| problem-vs-symptom    | Is the stated problem a symptom of something upstream?                    |
| scope-shift           | Narrower or wider framing?                                                |
| stakeholder-shift     | What does this look like from different stakeholders' perspectives?       |
| level-of-abstraction  | More general or more specific?                                            |
| time-horizon          | 1 week? 6 months? 5 years?                                                |
| inversion             | What new problems emerge if we succeeded wildly?                          |
| category-shift        | Is this really technical / people / process / spec / business / etc.?     |
| constraints-shift     | Which "fixed" constraints are actually negotiable?                        |

3-6 lenses is typical. Irrelevant lenses are dropped — forcing an unfit lens produces noise, not insight.

## Why Isolation

Reframers do not see each other's output during generation. This is deliberate — the same research supporting Nominal Group Technique over classical group brainstorming applies here: *coordinated* reframers anchor on each other and produce less distinct alternatives; *independent* reframers produce genuinely different framings that synthesis can then combine.

Synthesis re-introduces cross-pollination through *composite framings* (combining two lenses into a sharper framing), capturing the benefit of combination without the cost of anchoring.

## Output

A structured report with:
- **Original framing** — stated problem + premise snapshot (implicit assumptions made visible)
- **Standout reframings** — 1-3 reframings that materially shift the problem's meaning, each with explicit "what changed" diff and "when this framing applies"
- **Composite framings** — orchestrator-constructed combinations across lenses (optional)
- **Refinements** — reframings that sharpen without replacing
- **Where the original framing held up** — calibration signal: which lenses produced no meaningful shift
- **Recommendation** — Keep original / Adopt reframing X / Further explore
- **Suggested next steps** — natural handoffs

## Iteration

The skill is **one-shot by design**. If a reframing resonates, restate the problem with the new framing and re-invoke `/think-brainstorm` (or, if you want to pressure-test the reframing further, re-invoke `/think-reframe` on the revised problem).

## Natural Pipeline

```
/think-reframe → /think-brainstorm → /think-deliberate → /think-scrutinize
     redefine        generate            choose           stress-test
```

Each skill is a step in the full reasoning chain from raw problem to stress-tested chosen approach. You can enter anywhere and exit anywhere — `/think-reframe` is the dedicated "am I solving the right problem?" step that precedes idea generation.

## Example Session

```
> /think-reframe Our team is burned out and I need to figure out what to do about it.

Let me capture the problem and extract premises.

Problem brief:
- Stated: team is burned out, user needs a plan of action
- Implied scope: the user's team
- Implied category: people / management problem
- Implied stakeholders: team members, user as manager
- Implied time horizon: near-term (the burnout is present-tense)
- Unstated premises: (a) burnout is the problem (not a symptom),
  (b) a "plan of action" from the user will fix it, (c) the user has
  the authority to make the necessary changes

Lenses I'll apply: problem-vs-symptom, stakeholder-shift, constraints-shift,
category-shift, time-horizon. Skipping scope-shift (scope is clear),
level-of-abstraction (current level fits), inversion (unlikely to illuminate
for burnout-type problems — we know what "solved" looks like).

[Spawning 5 reframers in parallel...]
[Collecting reframings...]
[Synthesizing...]

## Reframing Report

Stated problem: "Our team is burned out and I need to figure out what to do."
Lenses applied: problem-vs-symptom, stakeholder-shift, constraints-shift,
category-shift, time-horizon

### Original Framing

The user's team is experiencing burnout. The user, as manager, treats
this as a people/management problem requiring an action plan. Implicit
premises: burnout is the problem (not a symptom), a managerial
intervention can fix it, the user has the authority to act.

### Standout Reframings

#### problem-vs-symptom

**Reframed:** "Our team's sustained output level has exceeded what the
work structure can support. Burnout is the symptom; the sustainable
capacity mismatch is the root problem."

**What changed:** The stated problem treats burnout as the thing to fix.
The reframed problem treats burnout as a signal about a broken fit
between commitments and capacity. Interventions shift from "manage the
burnout" to "fix what's generating the burnout."

**When this framing applies:** When burnout is recurring (not tied to a
single exceptional quarter), when the team has historically absorbed
similar load without burning out (something changed), or when the user
has control over scope/commitments.

#### category-shift

**Reframed:** "Our team's incentive structure rewards output that exceeds
what's sustainable. The individuals are responding rationally to the
incentives; the incentives need to change."

**What changed:** The stated framing treats this as a people/management
problem (people are burned out, manager must act on the people).
The reframed framing treats it as an incentive design problem — the
people are downstream of a system that rewards unsustainable patterns.
The intervention is at the system level, not the individual level.

**When this framing applies:** When the team keeps re-burning-out after
apparent solutions, when "heroic" work is visibly praised, when individual
self-care approaches haven't worked.

### Composite Framings

- **stakeholder-shift (team-member view) + time-horizon (6 months)**:
  "What does this look like to each team member if the current pace
  continues for another 6 months?" Surfaces whether the burnout is
  evenly distributed or concentrated, whether retention risk is acute,
  and whether individual team members have different thresholds.

### Refinements (Not Materially Shifting)

- **stakeholder-shift**: shifts which stakeholders' perspectives matter but
  the underlying problem remains a people/management one
- **constraints-shift**: surfaces that "we have to deliver X by Y" is
  assumed; user confirmed it's genuinely negotiable, so this refinement
  is real but narrow

### Where the Original Framing Held Up

- **time-horizon (1 week)** produced no meaningful shift — the urgent
  framing is in fact about immediate relief, not long-term restructuring

### Recommendation

**Adopt reframing: problem-vs-symptom.** This reframe most materially
changes what "solving the problem" would mean — shifting from "manage
burnout" to "fix the capacity mismatch that produces burnout." The
category-shift reframing is also strong and may compound with
problem-vs-symptom if the mismatch is incentive-driven.

### Suggested Next Steps

- Restate the problem as the capacity mismatch framing, then `/think-brainstorm`
  for interventions on that reframed problem
- If the capacity mismatch and incentive framings both resonate, consider
  exploring their composite (the mismatch exists because the incentives
  reward it) before generating approaches
```

## Relationship to Other Skills

| Skill                | Relationship                                                                        |
|----------------------|-------------------------------------------------------------------------------------|
| `/think-brainstorm`  | Natural downstream — brainstorm on the (possibly reframed) problem                  |
| `/think-deliberate`  | Further downstream — choose between generated approaches                            |
| `/think-scrutinize`  | Final stress-test of a chosen approach                                              |
| `/scope`             | When a reframed problem is clear enough, translate into a ticket                    |

## Philosophy

Most wasted engineering effort goes into solving well-defined versions of the wrong problem. The discipline of reframing — deliberately asking "is this the right problem?" before solving — is universally skipped because it feels like delay. `/think-reframe` formalizes that discipline so it can't be skipped.

The honest outcome of a reframing exercise is often "the original framing holds up." That's not a failure — it's calibration. The user can proceed with more confidence that they're solving the right problem. The outcome to fear is never reframing at all, not reframing and finding the original was sound.

Einstein (possibly apocryphally): "If I had an hour to solve a problem, I'd spend 55 minutes defining it." This skill is the 55-minute discipline, formalized.
