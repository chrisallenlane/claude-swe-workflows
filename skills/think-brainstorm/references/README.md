# /think-brainstorm - Divergent Idea Generation

## Overview

`/think-brainstorm` generates candidate approaches for achieving a goal. It validates the goal's assumptions with you first. When the framing itself is in doubt, it also checks whether you are brainstorming the right problem. Then it runs several brainstorming techniques as isolated parallel agents and pools the results into a catalog of ideas.

It counters anchoring and evaluation apprehension, the two ways group brainstorming narrows its own output. The method is Nominal Group Technique (Delbecq & Van de Ven) applied to AI agents, with Osborn's rules and de Bono's generative techniques supplying the palette. The namespace-wide rationale, including why generation runs in isolation, lives in [`references/think.md`](../../../references/think.md).

The step-by-step procedure lives in [`SKILL.md`](../SKILL.md); this guide covers when to use the skill and what to expect.

The skill only generates. Choosing and critiquing belong to other skills. It produces feedback only: no code, no tickets, no artifacts.

## When to Use

**Use `/think-brainstorm` for:**
- Early-stage exploration where you know the goal but not the approach
- Escaping conventional thinking on a stuck problem
- Generating a diverse candidate set before committing to a direction
- Suspecting you are solving the wrong problem. Assumption validation catches a wrong premise, and the framing check catches a wrong problem.

**Don't use `/think-brainstorm` for:**
- Choosing between known options (use `/think-deliberate`)
- Stress-testing an existing plan (use `/think-scrutinize`)
- Implementing changes (this skill makes nothing; follow up with `/scope` or `/implement`)
- Goals so vague that no meaningful assumptions can be extracted (refine the goal first)

**Rule of thumb:**
- "What could I even do here?" → `/think-brainstorm`
- "Which of these options is best?" → `/think-deliberate`
- "What's wrong with this plan?" → `/think-scrutinize`

**Natural pipeline:** `/think-brainstorm` → `/think-deliberate` → `/think-scrutinize` → `/scope` (generate → choose → stress-test → specify).

## Flow

```
Receive goal → Validate assumptions (with you) → [Framing check, if in doubt]
  → Choose techniques → Brainstormers (parallel, isolated) → Synthesize → Report
```

**The assumption check is interactive.** Expect to confirm, revise, or discard each assumption the skill extracts. Sometimes this alone dissolves or reframes the goal, which is a good result.

**The framing check runs only when it's warranted:** validation left the framing in doubt, the problem feels stuck, a debate has gone around without converging, the stakes justify pressure-testing the framing, or you ask whether this is even the right problem. Otherwise the report says in one line why it was skipped. When it runs, you choose the problem to brainstorm: keep the original framing, adopt a reframing, or pick among several.

## Techniques

The skill picks 3–6 techniques that fit the goal and drops the rest. You do not pick them.

| Technique           | Angle                                                     |
| ------------------- | --------------------------------------------------------- |
| first-principles    | Strip to irreducible requirements, reason up              |
| working-backwards   | Imagine success, trace paths back                         |
| lateral             | Random entry and provocation to break convention          |
| analogical          | Structural analogies from unrelated domains               |
| constraints-shift   | Force the goal through artificial constraints             |
| worst-possible-idea | Generate bad ideas, invert them                           |
| six-hats-green      | de Bono's creative hat; pure generation                   |
| SCAMPER             | Seven verbs; only for refining an existing solution       |

The framing check uses 3–6 reframing lenses chosen the same way: problem-vs-symptom, scope-shift, stakeholder-shift, level-of-abstraction, time-horizon, inversion, category-shift, constraints-shift.

## What You Get Back

- **Validated Assumptions**: each assumption, and whether you confirmed, revised, or discarded it
- **Framing Check**: if it ran, the standout reframings, where the original framing held, and which framing you chose; otherwise one line saying why it was skipped
- **Standouts**: the 3–7 most novel, promising, or counterintuitive ideas, without technique attribution
- **Hybrid Ideas**: cross-technique combinations the orchestrator constructed, flagged as such
- **Other Reasonable Ideas**: clustered by theme, with technique attribution
- **Questions the Exercise Raised**: often the real insight
- **Suggested Next Steps**: handoffs to `/think-deliberate`, `/think-scrutinize`, or a re-invocation

The skill is one-shot. To go deeper on a direction, refine the goal and re-invoke.

## Example Session

```
> /think-brainstorm We want to reduce deploy friction for our web app.
  Deploys currently take 45 minutes and require manual coordination.

Assumptions I see in the goal:
1. The 45-minute duration is the main friction
2. Manual coordination is separable from deploy speed
3. The current deploy pipeline is the right thing to optimize
4. Friction reduction is a speed problem (vs. a process/safety problem)

Can you validate these?

> 1: yes, also coordination overhead. 2: no, they're tangled — coordination is
  needed because rollbacks take 20 min and we're risk-averse. 3: not sure. 4:
  mixed — both speed and safety.

Revised goal: the coordination is downstream of rollback fear. Friction is
slow rollback → risk aversion → manual coordination → deploy latency.

> Yes, keep rollback in scope.

Techniques: first-principles, working-backwards, lateral, analogical,
constraints-shift. Skipping SCAMPER (the pipeline isn't sacred),
worst-possible-idea (poor fit), six-hats-green (covered by the others).

## Brainstorm Report

### Framing Check

Skipped: assumption validation already reframed the goal around rollback
fear, and you confirmed that framing.

### Standouts

1. **Make rollback the default operation, not the exception**
   If rollback is instant and risk-free, coordination overhead evaporates.
   Why a standout: attacks the root cause the validation phase surfaced.

2. **Feature flags as the real deploy unit**
   "Deploys" become config changes; rollback is a flag flip.
   Why a standout: the unit of deploy was wrong.

### Hybrid Ideas

- **Flag-gated blue/green with auto-rollback on telemetry**
  Combines: idle-stack swap + feature flags + telemetry-triggered rollback.
  Together they remove the human decision point.

### Other Reasonable Ideas

**Cluster: pipeline optimization**
- Parallelize test stages *(first-principles)*
- Skip full regression for safe-change deploys *(constraints-shift)*

### Questions the Exercise Raised

- What % of deploys currently roll back? If it's <1%, the
  coordination-for-risk tradeoff is likely miscalibrated.
- Is the coordination driven by rollback risk, or by habit from when
  rollback was hard?
```

The instructive part is the assumption check. Your answer to assumption 2 reframed the goal before any ideas were generated, and the standouts attack the reframed problem.
