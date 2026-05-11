---
name: review-arch
description: Architectural review workflow. Analyzes codebase organization via noun analysis and produces a target blueprint. Advisory only — does not implement changes. In interactive standalone mode, offers to cut tickets for the planned work. In autonomous mode (when invoked by an orchestrator), produces a report with concrete next-step recommendations.
model: opus
---

# Arch Review — Advisory Architectural Analysis

Analyzes codebase architecture and produces a target blueprint via noun analysis. **Advisory only.** The skill does not implement changes — it surfaces opportunities and, when run interactively, offers to cut tickets so the work can be picked up by implementation skills.

## Philosophy

**Review and implementation are different concerns.** A skill that does both makes both worse — implementation pressure compromises the review, and review pressure compromises the implementation. The plugin is moving `/review-*` skills toward advisory-only over time (see the "Advisory aspiration" section of [`references/autonomy.md`](../../references/autonomy.md)); `/review-arch` is the first concrete step in that direction.

**Clarity through organization is the goal.** Every module should have a clear identity — a domain noun it owns. Functions should live where a reader expects to find them. DRY and Prune serve this organizational goal, not the other way around.

**Recommend boldly.** The analysis agent surfaces every opportunity it finds, even uncertain ones — the user can always reject a recommendation when reviewing the plan. The skill's job is to *see*, not to *act*.

**Two modes, one analysis.** The architectural analysis is the same whether the skill is invoked directly by an operator or by another skill. What changes is the output:

- **Interactive standalone mode** — collaborates with the user on the plan, offers to cut tickets for the planned work.
- **Autonomous mode** (called by an orchestrator) — produces a structured report with concrete next-step recommendations. No user interaction, no ticket creation.

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│           ARCH REVIEW WORKFLOW (advisory)                       │
├─────────────────────────────────────────────────────────────────┤
│  1. Determine scope and mode                                    │
│  2. Spawn swe-arch-reviewer agent (full analysis)               │
│     → returns dead code list + target blueprint                 │
│                                                                 │
│  Interactive standalone mode (3 — 6):                           │
│  3. Present analysis to user                                    │
│  4. Iterate on plan with user                                   │
│  5. Offer to cut tickets                                        │
│     ├─ Preview ticket set to user                               │
│     ├─ User edits / approves                                    │
│     └─ Create tickets in tracker with appropriate labels        │
│                                                                 │
│  Autonomous mode (skips 3 — 5):                                 │
│                                                                 │
│  6. Completion summary                                          │
│     ├─ Interactive: tickets created (or "no tickets — analysis only")│
│     └─ Autonomous: structured report for the caller             │
└─────────────────────────────────────────────────────────────────┘
```

## Workflow Details

### 1. Determine Scope and Mode

**Scope:** Default is the entire codebase. If the caller specifies a path or module, respect that scope.

**Mode detection:**

- If invoked by another skill (e.g., `/implement-project` quality pipeline, `/refactor-deep` Phase 2), the caller passes an explicit `interactive: true|false` parameter. Use that.
- If invoked directly by the operator (no parameter passed), default to **interactive**.
- When in doubt, the principle: a skill at the keyboard with a human operator is interactive; a skill running inside an orchestrator's autonomous loop is not.

Tools the operator can use to override the default: `--autonomous` to force advisory-only output even when invoked directly, `--interactive` to force ticket-cutting offer even when called by another skill (rare; usually a hint the wrong skill is calling).

Pass scope to the analysis agent. Pass mode forward to the post-analysis phases.

### 2. Analyze Codebase

**Spawn fresh `swe-arch-reviewer` agent:**

The agent performs four sequential analysis steps:

1. Catalogs dead code for removal
2. Builds a domain model via noun analysis
3. Catalogs repetition patterns
4. Produces a target architecture blueprint

**Prompt the agent with:**
```
Perform a full architectural analysis of this codebase.
Scope: [entire codebase | user-specified scope]
Produce a comprehensive target architecture blueprint showing where
everything should live. Cover every module — existing and proposed.
```

The agent returns:
- A noun frequency table (the primary analytical artifact)
- A per-noun namespace evaluation
- A dead code list
- A repetition catalog (DRY candidates, resolved in the blueprint)
- A target architecture blueprint (existing modules + proposed new modules)
- Any linter/formatter issues observed
- Any behavior-altering implications worth flagging

**If the agent reports "No refactoring needed":** Workflow complete. Skip to step 6 (completion summary) with an empty findings list.

### 3. Present Analysis to User *(interactive mode only)*

After the analysis agent returns, present its findings to the user. The user needs to see the full picture before deciding what to do.

**Present three things:**

**a) Noun analysis.** Show the noun frequency table and the per-noun namespace evaluations. This is the analytical foundation — the user should understand what nouns the agent identified, how frequently they appear, and why they do or don't deserve their own namespace.

**b) Proposed changes.** Show the blueprint items — modules to change, absorb, dissolve, or rename, plus proposed new modules. For each item, include the agent's rationale. Group by category (dead code removal, renames, moves, absorptions, dissolutions, new modules).

**c) No-change items.** Show the modules the agent evaluated and explicitly decided to leave alone, with their domain justifications. This is important context — the user may disagree and want to add items, or may spot a module the agent missed entirely.

### 4. Iterate on Plan with User *(interactive mode only)*

The user has the full analysis. Give them the opportunity to shape the plan before any tickets are cut.

**The user may want to:**
- Remove items they disagree with
- Add items the agent missed
- Modify proposed changes (e.g., "move that function to module X instead of Y")
- Ask questions about specific recommendations ("why did you flag this as dead code?")
- Adjust the scope based on what they see
- Reprioritize items

**Continue iterating until the user is satisfied with the plan.** Don't rush this — architectural decisions are consequential and benefit from deliberation.

### 5. Offer to Cut Tickets *(interactive mode only)*

Once the plan is finalized, offer to convert the planned work into tickets. **This is the only place the skill writes to anything outside the working tree.**

**Generate a draft ticket per blueprint item.** Group related items into a single ticket if doing so makes the work cohesive (e.g., "dissolve helpers.go: distribute its 6 functions" is one ticket, not six). Each ticket includes:

- **Title** — short, action-oriented (e.g., "Dissolve helpers.go; distribute functions to domain owners").
- **Description** — the rationale from the blueprint plus the specific moves/renames involved.
- **Recommended implementation skill** — name the skill that should pick this up, with scope hint. Examples:
  - "Implementation: `/refactor` with scope `src/utils/`" (for mechanical changes within an existing module)
  - "Implementation: `/scope` first to plan dependencies, then `/implement`" (for new module creation)
  - "Implementation: `/implement-batch` with this ticket plus the related `request.go` absorption ticket" (for cross-cutting changes)
- **Acceptance criteria** — what "done" looks like for this ticket (tests still pass, specific symbols moved, specific files removed).

**Preview the full ticket set to the user.** Show all tickets at once so the user can see the whole plan. The user can:

- Approve as-is
- Edit titles, descriptions, or acceptance criteria
- Remove tickets they don't want cut
- Add labels (default to no labels; offer common candidates: `refactor`, `tech-debt`, `arch`)

**On approval, create tickets in the tracker.** Detect the tracker using the same pattern as `/scope`:
- GitHub → `gh` CLI
- Gitea → `mcp__gitea__*` MCP tools
- GitLab → `glab` CLI

Capture each ticket's URL or number for the completion summary.

**If the user declines to cut tickets:** That's a valid outcome. Note in the completion summary that the analysis was advisory-only.

### 6. Completion Summary

The summary format depends on mode.

#### Interactive mode

```
## Arch Review Complete

### Scope
[Entire codebase | user-specified scope]

### Analysis statistics
- Modules evaluated: N
- Blueprint items proposed: N
- Dead code items identified: N
- Items the user removed during iteration: N
- Items finalized for ticket creation: N

### Tickets created
- #123: Dissolve helpers.go; distribute functions — recommends /refactor scoped to pkg/helpers
- #124: Absorb validate() into request.go — recommends /refactor scoped to pkg/request and pkg/server
- ...

(or: "No tickets created — analysis was advisory-only per user request.")

### Recommended next steps
[Brief paragraph naming the natural follow-up. Examples:
 - "Tickets are labeled `arch`; consider `/implement-batch` to work through them as a cohesive unit."
 - "Single ticket — run `/implement` when ready."
 - "No tickets cut — analysis stands as a planning artifact; revisit when you have time to act on it."]
```

#### Autonomous mode

The report is structured for the calling orchestrator to consume and surface in its final report. No ticket creation.

```
## Arch Review Report (Autonomous)

### Scope
[Entire codebase | scope passed by caller]

### Noun analysis
[Frequency table + per-noun namespace evaluations.]

### Dead code (advisory)
- <file>:<line> — <description> — recommended action

### Blueprint items (advisory)
- <item> — <rationale> — recommended action

### No-change items
[Modules evaluated and left alone, with domain justifications.]

### Recommended next steps

Each recommendation names a specific skill with a scope hint so the caller (or operator reading the caller's final report) can chain the right next step.

- "Dead code in `src/foo/`: `/refactor` scoped to that directory."
- "Module dissolution of `helpers.go`: `/scope` to plan dependencies, then `/implement` or `/implement-batch` to execute."
- "Cross-module DRY in `request`/`response`: `/refactor` with aggression MAX, scoped to the two modules."
- "Linter/formatter issues: any `/refactor` invocation will catch these as part of its standard pass."
```

The caller decides what (if anything) to do with these recommendations. `/implement-project` typically surfaces them under "Deferred Items / Architectural Recommendations" in its final report.

## Agent Coordination

**Sequential execution:**
- The analysis agent runs once per invocation. Fresh instance per invocation.
- No SME agents are spawned by this skill (no implementation).
- No QA agents are spawned by this skill (no changes to verify).

**State to maintain (as orchestrator):**
- Mode (interactive or autonomous)
- Scope
- Analysis output from `swe-arch-reviewer`
- In interactive mode: the iterating plan as the user shapes it
- Ticket URLs/numbers created (interactive mode only)

## Abort Conditions

**Abort the workflow:**
- Analysis agent fails or returns malformed output — retry once; if it fails again, surface the error.
- User interrupts during iteration.
- Tracker is unavailable when the user has approved ticket creation — surface the error; preserve the approved ticket set in the completion summary so the user can create them manually.

**Do NOT abort for:**
- Empty findings — that's a valid outcome. Report "no architectural improvements identified" and exit cleanly.
- User declining to cut tickets in interactive mode — analysis stands as a planning artifact.

## Integration with Other Skills

**Relationship to `/refactor`:**
- `/refactor` is a tactical workflow for code quality improvements within existing architecture (DRY, dead code, naming, complexity).
- `/review-arch` is the strategic analysis that questions and proposes restructuring of architecture itself (noun analysis, module boundaries, blueprints).
- Use `/refactor` for routine cleanup; use `/review-arch` when the module structure itself needs rethinking. After `/review-arch`'s tickets are cut, `/refactor` and `/implement` carry them out.

**Relationship to `/refactor-deep`:**
- `/refactor-deep` Phase 2 invokes `/review-arch` in interactive mode so it can offer ticket creation as part of the deep cycle.
- See `/refactor-deep`'s SKILL.md for the full sequence.

**Relationship to `/implement-project`:**
- `/implement-project` step 7b invokes `/review-arch` in autonomous mode for a read-out as part of the quality pipeline.
- Recommendations surface in `/implement-project`'s final report under "Deferred Items / Architectural Recommendations."

**Relationship to `/scope`:**
- `/scope` creates individual tickets through exploratory dialogue.
- `/review-arch` (interactive mode) cuts a batch of tickets from a blueprint in one go.
- Use `/scope` for one ticket at a time when you know what you want; use `/review-arch` to *discover* what tickets are needed.

**Relationship to `swe-arch-reviewer` agent:**
- The agent is the analytical core. It is unchanged by this skill's advisory shift — it produces the same output; the skill just routes that output differently.

## Example Session (Interactive)

```
> /review-arch

Scope: entire codebase
Mode: interactive (default; invoked directly)

Spawning swe-arch-reviewer agent...

Analysis complete. Here's what I found:

## Noun Frequency
| Noun     | Count | Has Namespace? | Modules Where It Appears |
|----------|-------|----------------|--------------------------|
| request  | 14    | No             | Server, App, Middleware  |
...

## Proposed Changes
1. Dead code removal (4 instances across 3 files)
2. Rename parser.go → request.go (domain noun)
3. request.go absorbs validate() from server.go
4. Dissolve helpers.go; distribute its 6 functions
5. Create response.go (response construction is scattered)

## No-Change Items
- config.go — clear identity, well-scoped
- middleware.go — cohesive, correctly placed

What would you like to change about this plan?

> I agree with 1-4, but let's hold off on creating response.go.

Updated plan: 4 items.

Offer: create tickets for the 4 finalized items?
> Yes, please.

Drafting tickets...

### Ticket preview
1. Remove dead code (4 instances)
   - Implementation: /refactor scoped to {server.go, helpers.go, parser.go}
   - AC: lines listed in description are gone; tests pass

2. Rename parser.go → request.go (domain noun)
   - Implementation: /refactor scoped to parser.go
   - AC: file is renamed; all references updated; tests pass

3. request.go absorbs validate() from server.go
   - Implementation: /refactor scoped to {server.go, request.go}
   - AC: validate() lives in request.go; server.go imports nothing from request beyond what it already uses; tests pass

4. Dissolve helpers.go; distribute 6 functions
   - Implementation: /scope first (cross-module moves benefit from planning); then /implement-batch
   - AC: helpers.go is deleted; each named function has a new home documented in the ticket

Labels to apply (defaults to none)?
> arch, tech-debt

Creating tickets in Gitea...
- #201: Remove dead code (4 instances) — created
- #202: Rename parser.go → request.go — created
- #203: request.go absorbs validate() from server.go — created
- #204: Dissolve helpers.go — created

## Arch Review Complete

### Scope: entire codebase

### Analysis statistics
- Modules evaluated: 8
- Blueprint items proposed: 5
- Items removed during iteration: 1 (create response.go, deferred)
- Items finalized for ticket creation: 4

### Tickets created
- #201, #202, #203 — recommend /refactor scoped per ticket
- #204 — recommends /scope then /implement-batch

### Recommended next steps
Tickets are labeled `arch, tech-debt`. Consider `/implement-batch` to
work through #201-#203 as a cohesive unit (they touch overlapping
files); #204 deserves its own scoping pass first.
```

## Example Session (Autonomous, via `/implement-project`)

```
[Called by /implement-project step 7b with interactive=false]

Scope: entire codebase
Mode: autonomous

Spawning swe-arch-reviewer agent...

Analysis complete. Producing report (no user interaction, no ticket creation).

## Arch Review Report (Autonomous)
...
[Report returned to /implement-project, which surfaces it in its
 final report's "Deferred Items / Architectural Recommendations"
 section.]
```
