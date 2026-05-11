# /review-arch - Advisory Architectural Analysis

## Overview

The `/review-arch` skill analyzes codebase architecture and produces a target blueprint via noun analysis. It is **advisory only** — the skill does not make changes to the codebase. When run interactively by an operator, it offers to convert the planned work into tickets in your issue tracker. When invoked by another skill (autonomous mode), it produces a structured report with concrete next-step recommendations.

The plugin is moving `/review-*` skills toward advisory-only over time; `/review-arch` is the first concrete step in that direction. See the "Advisory aspiration" section of [`references/autonomy.md`](../../../references/autonomy.md) for the broader direction.

**Key benefits:**
- Blueprint-driven analysis — surfaces a coherent target architecture, not a grab-bag of independent fixes
- Noun analysis identifies the natural decomposition boundaries in the domain
- Interactive review lets the user shape the plan before any tickets are cut
- Ticket creation (interactive mode) routes the work to the right implementation skill with scope hints
- Autonomous mode produces structured reports that orchestrators can surface in their final reports

## When to Use

**Use `/review-arch` for:**
- Rethinking module boundaries and responsibilities
- When modules have unclear identities or overlap
- After a codebase has grown organically and needs structural cleanup
- When "helpers.go" or "utils.py" has become a dumping ground
- Preparing a codebase for a major new feature that needs clean abstractions
- Generating a coherent batch of refactoring tickets for `/implement-batch` to work through

**Don't use `/review-arch` for:**
- Routine code cleanup (use `/refactor` instead)
- Quick DRY fixes or dead code removal (use `/refactor`)
- Active development where module structure is still in flux

**Rule of thumb:** Use `/review-arch` when the module structure itself needs rethinking — the output is a plan (or a set of tickets), not a set of commits.

## Two Modes

| Mode                  | When                                                                         | Output                                                                  |
|-----------------------|------------------------------------------------------------------------------|-------------------------------------------------------------------------|
| Interactive standalone| Invoked directly by the operator (default)                                   | Iterates plan with user; offers to cut tickets with preview-and-approve |
| Autonomous            | Invoked by another skill (e.g., `/implement-project`, `/refactor-deep`)      | Structured report with skill-named next-step recommendations            |

The mode is set by an explicit `interactive: true|false` parameter from the caller. When invoked directly by the operator without a parameter, the default is interactive. The operator can force autonomous output with `--autonomous` or force interactive with `--interactive` (rare; usually a hint the wrong skill is calling).

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ /review-arch Workflow (advisory)                                │
└─────────────────────────────────────────────────────────────────┘

 ┌──────────────────────────────────────────────┐
 │  1. DETERMINE SCOPE AND MODE                 │
 │  ────────────────────────────────────────    │
 │  • Scope: entire codebase or user-specified  │
 │  • Mode: interactive or autonomous           │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  2. ANALYZE CODEBASE                         │
 │  ────────────────────────────────────────    │
 │  Agent: swe-arch-reviewer (fresh instance)   │
 │                                              │
 │  Four sequential analysis steps:             │
 │  • Catalog dead code                         │
 │  • Noun analysis (domain model)              │
 │  • Identify repetition                       │
 │  • Produce target blueprint                  │
 │                                              │
 │  No opportunities? → COMPLETION SUMMARY      │
 └──────────────────┬───────────────────────────┘
                    ▼
              Mode? ────────┐
                            │
           interactive ◄────┘────► autonomous
              │                          │
              ▼                          │
 ┌──────────────────────────────────────────────┐
 │  3. PRESENT ANALYSIS TO USER                 │
 │     (interactive only)                       │
 ├──────────────────────────────────────────────┤
 │  4. ITERATE ON PLAN WITH USER                │
 │     (interactive only)                       │
 ├──────────────────────────────────────────────┤
 │  5. OFFER TO CUT TICKETS                     │
 │     (interactive only)                       │
 │  • Generate draft ticket per item            │
 │  • Preview to user                           │
 │  • Get approval; user may edit/remove        │
 │  • Create in tracker with labels             │
 └──────────────────┬───────────────────────────┘
                    │                          │
                    ▼                          ▼
 ┌──────────────────────────────────────────────┐
 │  6. COMPLETION SUMMARY                       │
 │  ────────────────────────────────────────    │
 │  Interactive: tickets created (or none)      │
 │  Autonomous:  structured report for caller   │
 │                                              │
 │  Both: "Recommended next steps" name         │
 │  specific skills with scope hints            │
 └──────────────────────────────────────────────┘
```

## Workflow Details

### 1. Determine Scope and Mode

**Scope:** Default is the entire codebase. Caller may pass a narrower scope (directory, files, module). The scope is propagated to the analysis agent.

**Mode:** Detected from the caller's parameter, or defaulted from invocation context (interactive when invoked directly by the operator; autonomous when invoked by another skill).

### 2. Analyze Codebase

A fresh `swe-arch-reviewer` agent performs four sequential analysis steps:

| Step                   | What it does                                                                       |
|------------------------|------------------------------------------------------------------------------------|
| 1. Prune dead code     | Catalogs unused functions, dead imports, legacy assumptions                        |
| 2. Noun analysis       | Builds domain model — identifies what nouns exist, where they live, where they should live |
| 3. Identify repetition | Catalogs duplication patterns as inputs to the blueprint                           |
| 4. Produce blueprint   | Synthesizes steps 1-3 into a target architecture                                   |

The blueprint describes each module's target state: what it owns, what it absorbs from other modules, what gets renamed, and what implementation simplifications are possible.

The agent is unchanged by this skill's advisory shift — it produces the same output; the skill just routes that output differently.

### 3. Present Analysis to User *(interactive mode only)*

After the analysis agent returns, the skill presents its findings in full:

- **Noun analysis table** — the domain model: what nouns were found, where they live, where they should live
- **Proposed changes** — blueprint items grouped by category (dead code removal, renames, moves, absorptions, dissolutions, new modules)
- **No-change items** — modules the agent evaluated and decided to leave alone, with domain justifications

### 4. Iterate on Plan with User *(interactive mode only)*

The user shapes the plan before any tickets are cut. They may add, remove, or modify items, ask questions about specific recommendations, or adjust priorities. Continue until the user is satisfied.

This is the heart of the interactive flow. Architectural decisions are consequential and benefit from deliberation; don't rush this step.

### 5. Offer to Cut Tickets *(interactive mode only)*

Once the plan is finalized, offer to convert the planned work into tickets. The user can decline — analysis stands as a planning artifact.

For each blueprint item (or cohesive group of items), generate a draft ticket including:

- **Title** — short, action-oriented
- **Description** — rationale plus specific moves/renames
- **Recommended implementation skill** — names the skill that should pick this up, with scope hint (e.g., `/refactor scoped to src/utils/`, or `/scope then /implement-batch` for cross-module work)
- **Acceptance criteria** — what "done" looks like

**Preview the full set to the user.** The user can approve as-is, edit any field, remove tickets they don't want cut, and choose labels (default: none).

**On approval, create tickets in the tracker** using the same detection pattern as `/scope` (GitHub via `gh`, Gitea via MCP, GitLab via `glab`).

### 6. Completion Summary

The format depends on mode. Interactive mode lists tickets created (or notes that no tickets were cut); autonomous mode produces a structured report for the caller. Both modes include a "Recommended next steps" section that names specific skills with scope hints.

See SKILL.md for the exact templates.

## Tips for Effective Use

1. **Mode is set by who calls the skill.** Operator at the keyboard → interactive. Orchestrator running autonomously → advisory report. The skill defaults sensibly; you rarely need to override.

2. **In interactive mode, the iteration phase (step 4) is where most of the value lands.** The agent's first proposal is rarely the right plan — the back-and-forth with the user shapes it into something accurate.

3. **Ticket creation is opt-in even in interactive mode.** If you want the analysis as a planning artifact rather than a set of tickets, decline at step 5. The recommendations stand.

4. **Pay attention to the "Recommended implementation skill" hint in each ticket.** It names the right next move (`/refactor` for mechanical changes; `/scope` then `/implement` for new modules; `/implement-batch` for cohesive groups).

5. **Autonomous mode is for orchestrators, not for one-shot reports.** If you want a quick read-out without ticket creation, use interactive mode and decline at step 5. That's cleaner than `--autonomous` from the operator side.

6. **Consider running `/refactor` first.** Cleaning up dead code and DRY violations with `/refactor` reduces noise in the architectural analysis. The analysis agent can then focus on structural opportunities rather than rediscovering tactical ones.

7. **Scope aggressively for large codebases.** `/review-arch src/core/` targets a specific module; better than analyzing everything when you already know where the problems are.

## Agent Coordination

**Single agent invocation.** The skill spawns `swe-arch-reviewer` once per invocation. No SMEs are spawned (no implementation). No QA agents are spawned (no changes to verify).

**State maintained by the skill:**
- Mode (interactive or autonomous)
- Scope
- Analysis output from the agent
- In interactive mode: the iterating plan as the user shapes it; tickets created at the end

## Abort Conditions

**Abort the workflow:**
- Analysis agent fails or returns malformed output — retry once; if it fails again, surface the error.
- User interrupts during iteration.
- Tracker is unavailable when the user has approved ticket creation — surface the error; preserve the approved ticket set in the completion summary so the user can create the tickets manually.

**Do NOT abort for:**
- Empty findings — that's a valid outcome. Report "no architectural improvements identified" and exit cleanly.
- User declining to cut tickets — analysis stands as a planning artifact.

## Philosophy

The `/review-arch` workflow embodies several principles:

**Review and implementation are different concerns.**
- A skill that does both makes both worse.
- `/review-arch` surfaces opportunities and routes them to implementation skills via tickets.
- The plugin's broader direction is for `/review-*` skills to move toward advisory-only (see the "Advisory aspiration" section of [`references/autonomy.md`](../../../references/autonomy.md)).

**Organization first:**
- Every module should own a clear domain noun.
- Functions should live where a reader expects to find them.
- The blueprint describes a target architecture, not a grab-bag of fixes.

**Recommend boldly, decide collaboratively:**
- The analysis agent surfaces every opportunity, even uncertain ones.
- In interactive mode, the user reviews, refines, and decides what becomes a ticket.
- Architectural decisions are consequential and benefit from human judgment.

**Atomic tickets, not atomic commits:**
- Each blueprint item becomes a ticket (or a cohesive group becomes one ticket).
- Tickets are individually implementable — one ticket per coherent unit of work.
- The implementation skills (`/refactor`, `/implement`) handle the commit discipline.
