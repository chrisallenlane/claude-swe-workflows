# /think-brainstorm - Divergent Idea Generation

## Overview

The `/think-brainstorm` skill generates candidate approaches for achieving a goal. It validates the assumptions embedded in the goal, then spawns parallel brainstormers running different techniques in isolation, and synthesizes the pool into a catalog of ideas.

**Key properties:**
- Divergent by design — generation, not evaluation
- Multiple techniques in parallel — first-principles, working-backwards, lateral, analogical, constraints-shift, etc.
- Isolated brainstormers — no anchoring across agents (Nominal Group Technique)
- Dedicated assumption-validation phase — often the most valuable part
- Produces feedback only — no code, no tickets, no artifacts
- Natural handoff to `/think-deliberate` (choose) or `/think-scrutinize` (stress-test)

## When to Use

**Use `/think-brainstorm` for:**
- Early-stage exploration where you know the goal but not the approach
- Escaping conventional thinking on a stuck problem
- Generating a diverse candidate set before committing to a direction
- Pressure-testing a problem framing (the assumption-validation phase often reframes the goal)

**Don't use `/think-brainstorm` for:**
- Choosing between known options (use `/think-deliberate`)
- Stress-testing an existing plan (use `/think-scrutinize`)
- Implementing changes (this skill makes nothing — it's a consultant)
- Goals so vague no meaningful assumptions can be extracted (refine the goal first)

**Rule of thumb:**
- "What could I even do here?" → `/think-brainstorm`
- "Which of these options is best?" → `/think-deliberate`
- "What's wrong with this plan?" → `/think-scrutinize`

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ /think-brainstorm Workflow                                  │
└─────────────────────────────────────────────────────────────┘

 ┌──────────────────────────────────────────────┐
 │  1. RECEIVE THE GOAL                         │
 │  ────────────────────────────────────────    │
 │  • From context, document, or user input     │
 │  • Produce a written brief                   │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  2. VALIDATE ASSUMPTIONS                     │
 │  ────────────────────────────────────────    │
 │  • Extract stated + unstated assumptions     │
 │  • Validate each with the user               │
 │  • Refine the goal if needed                 │
 │  (May dissolve or reframe the problem)       │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  3. CHOOSE TECHNIQUES                        │
 │  ────────────────────────────────────────    │
 │  First-principles / Working-backwards /      │
 │  Lateral / Analogical / Constraints-shift /  │
 │  Worst-possible-idea / Six-hats-green /      │
 │  SCAMPER                                     │
 │  (3-6 selected; irrelevant ones dropped)     │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  4. SPAWN BRAINSTORMERS (parallel, isolated) │
 │  ────────────────────────────────────────    │
 │  One agent per technique                     │
 │  No cross-talk (NGT — avoids anchoring)      │
 │  5-10 ideas each, with rationale             │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  5. SYNTHESIZE                               │
 │  ────────────────────────────────────────    │
 │  • Deduplicate (preserve attribution)        │
 │  • Cluster by theme                          │
 │  • Construct hybrids                         │
 │  • Surface standouts (novel/promising/       │
 │    counterintuitive)                         │
 │  • Drop weak ideas                           │
 │  • Note questions raised                     │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  6. REPORT                                   │
 │  ────────────────────────────────────────    │
 │  Standouts / Hybrids / Other reasonable /    │
 │  Questions raised / Suggested next steps     │
 └──────────────────────────────────────────────┘
```

## Roles

| Role          | What they do                                                                 |
|---------------|------------------------------------------------------------------------------|
| Judge (you)   | Capture goal, validate assumptions, choose techniques, synthesize report     |
| Brainstormers | Generate ideas through assigned techniques, in isolation                     |

## Brainstorming Techniques

The orchestrator selects techniques based on the goal's shape. Common techniques:

| Technique           | What it does                                                                      |
|---------------------|-----------------------------------------------------------------------------------|
| first-principles    | Strip to irreducible requirements, reason up                                      |
| working-backwards   | Imagine success concretely, trace paths back                                      |
| lateral             | Random entry + provocation; deliberately break conventional thought               |
| analogical          | Structural analogies from unrelated domains (biomimicry, cross-industry, etc.)    |
| constraints-shift   | Force the goal through artificial constraints (10x budget, ship tomorrow, etc.)   |
| worst-possible-idea | Generate bad ideas, invert them                                                   |
| six-hats-green      | de Bono's creative hat; pure generative mode                                      |
| SCAMPER             | Applies 7 verbs to an existing solution (only for refining, not greenfield)       |

3-6 techniques is typical. Irrelevant techniques are dropped — forcing an unfit technique produces noise, not insight.

## Why Isolation

Brainstormers do not see each other's output during generation. This is deliberate.

Research on group brainstorming (Osborn's original 1953 model) has repeatedly shown that *coordinated* groups produce fewer and more homogeneous ideas than the same number of individuals generating in parallel and pooling afterwards. The phenomenon is called **production blocking** (one person's ideas block others' thinking) and **anchoring** (early ideas constrain later ones).

Nominal Group Technique (NGT) addresses both: silent independent generation, then pooling. This skill applies NGT to AI agents. Each brainstormer's technique is their contribution — isolation keeps contributions distinct.

Synthesis re-introduces cross-pollination through *hybrid idea construction*, capturing the benefit of combination without the cost of anchoring.

## Output

A structured catalog with:
- **Validated Assumptions** — what held, what got revised, what got dropped
- **Standouts** — 3-7 most promising/novel/counterintuitive ideas, no technique attribution (let them stand on merit)
- **Hybrid Ideas** — orchestrator-constructed combinations across techniques
- **Other Reasonable Ideas** — clustered by theme, with technique attribution for transparency
- **Questions Raised** — often the real insight
- **Suggested Next Steps** — natural handoffs to `/think-deliberate`, `/think-scrutinize`, `/scope`

## Iteration

The skill is **one-shot by design**. If the report suggests a direction worth exploring deeper, refine the goal and re-invoke. If you want to choose between standouts, hand off to `/think-deliberate`. If you want to stress-test one, `/think-scrutinize`. Each invocation is a clean consultation.

## Example Session

```
> /think-brainstorm We want to reduce deploy friction for our web app.
  Deploys currently take 45 minutes and require manual coordination.

Let me capture the goal and check assumptions.

Goal brief:
- Current: deploys take 45 minutes, require manual coordination
- Desired: reduced friction — faster deploys, less coordination
- Success criteria: TBD

Assumptions I see in the goal:
1. The 45-minute duration is the main friction
2. Manual coordination is separable from deploy speed
3. The current deploy pipeline is the right thing to optimize (vs. rearchitecting
   how the app is deployed)
4. Friction reduction is a speed problem (vs. a process/safety problem)

Can you validate these?

> 1: yes, also coordination overhead. 2: no, they're tangled — coordination is
  needed because rollbacks take 20 min and we're risk-averse. 3: not sure. 4:
  mixed — both speed and safety.

Revised goal: reduce deploy friction, where "friction" is the combination of
slow rollback (20 min) driving risk aversion driving manual coordination
driving deploy latency. The coordination is downstream of rollback fear.

Proceed?

> Yes, and the rollback reframing is useful. Let's keep rollback in scope.

Techniques I'll apply: first-principles, working-backwards, lateral, analogical,
constraints-shift. Skipping SCAMPER (greenfield enough — the pipeline isn't
sacred), worst-possible-idea (doesn't fit this style of problem), six-hats-green
(covered by the others).

[Spawning 5 brainstormers in parallel...]
[Collecting idea sets...]
[Synthesizing...]

## Brainstorm Report

Goal: Reduce deploy friction by attacking the rollback-fear → coordination →
latency chain
Techniques applied: first-principles, working-backwards, lateral, analogical,
constraints-shift

### Validated Assumptions

- Deploy duration is the friction → Revised: coordination overhead is equally
  weighted, driven by rollback risk
- Rollback is in scope → Confirmed
- The current pipeline is sacred → Revised: not sacred, open to rearchitecture

### Standouts

1. **Make rollback the default operation, not the exception**
   Most deploy systems optimize forward deploys; rollback is a fallback. If
   rollback is instant and risk-free, coordination overhead evaporates.
   Why a standout: attacks the root cause the validation phase surfaced.

2. **Deploy to an idle stack, swap at the edge**
   Blue/green at the load balancer level. Deploy takes as long as it takes;
   cutover is a DNS/LB change. Rollback is a second DNS/LB change.
   Why a standout: decouples deploy duration from user-visible friction.

3. **Feature flags as the real deploy unit**
   Ship code continuously, flip flags gradually. "Deploys" become config
   changes. Rollback is a flag flip.
   Why a standout: reframes the problem — the unit of deploy was wrong.

### Hybrid Ideas

- **Flag-gated blue/green with auto-rollback on telemetry**
  Combines: [idle-stack swap + feature flags + telemetry-triggered rollback]
  Why the combination matters: each alone handles one dimension; together
  they eliminate coordination because the system rolls back itself on
  signal, removing the human decision point.

### Other Reasonable Ideas

**Cluster: pipeline optimization**
- Parallelize test stages *(first-principles)*
- Incremental artifact builds *(first-principles)*
- Skip full regression for safe-change deploys *(constraints-shift)*

**Cluster: architectural**
- Canary deploys to 1% first *(analogical — from cloud providers)*
- Service mesh for traffic shifting *(analogical)*
- Progressive rollout by customer segment *(lateral)*

**Cluster: workflow**
- On-call dedicated deploy coordinator (removes meeting overhead) *(constraints-shift: "one person only")*
- Deploy from chat (reduces context switch) *(lateral)*
- Scheduled deploy windows (batches coordination) *(working-backwards)*

### Questions the Exercise Raised

- Is the 20-minute rollback the real bottleneck? If rollback were <30 seconds,
  how much coordination would evaporate?
- What % of deploys currently *do* roll back? (Data-driven: if it's <1%, the
  coordination-for-risk tradeoff is likely miscalibrated.)
- Is the coordination overhead driven by rollback risk, or by *habit* from
  when rollback was hard?

### Suggested Next Steps

- To choose a direction from standouts: `/think-deliberate`
- To stress-test "rollback-as-default-operation": `/think-scrutinize`
- To scope feature-flag-first rollout: `/scope`
```

## Relationship to Other Skills

| Skill                | Relationship                                                                        |
|----------------------|-------------------------------------------------------------------------------------|
| `/think-deliberate`  | Chooses between generated options. Natural downstream of brainstorming.             |
| `/think-scrutinize`  | Stress-tests a selected standout. Natural downstream of deliberation.               |
| `/scope`             | Translates a chosen idea into a ticket                                              |
| `/scope-project`     | Translates a chosen idea into a multi-batch project plan                            |

**Natural pipelines:**
- `/think-brainstorm` → `/think-deliberate` → `/think-scrutinize` → `/scope` (generate → choose → stress-test → specify)
- `/think-brainstorm` → `/think-scrutinize` (generate → stress-test standouts without deliberation)

## Philosophy

Brainstorming is valuable when generation is constrained by convention, anchoring, or exhaustion. The skill formalizes techniques — each derived from established creativity literature — that deliberately break those constraints.

Isolation is what makes it work at scale. Osborn's original group-brainstorming model produces less than parallel-independent generation because coordination creates production blocking and anchoring. Running techniques as isolated agents, then synthesizing, captures the best of both: diversity of generation, richness of combination.

Assumption validation is what makes it *useful*. Brainstorming solutions to the wrong problem is a common failure mode. The validation phase often reframes or even dissolves the original goal — which is almost always better than the most creative solutions to a misframed problem.
