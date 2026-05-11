# /refactor-deep — Tactical Cleanup + Architectural Review

## Overview

The `/refactor-deep` skill pairs `/refactor` (tactical cleanup) with `/review-arch` (advisory architectural analysis with optional ticket creation). Gathers all major user input upfront and runs Phase 1 autonomously. Phase 2 is interactive — the operator reviews the architectural analysis and decides which (if any) of its recommendations to convert into tickets in the issue tracker.

This skill implements the autonomy discipline documented in [`references/autonomy.md`](../../../references/autonomy.md). Its upfront-input gathering is the skill's commander's intent (scope, aggression ceiling, QA instructions, ticket-creation preference, and any constraints/non-goals the operator wants to add).

**Key benefits:**
- Tactical refactoring (Phase 1) and architectural review (Phase 2) in one workflow.
- Architectural recommendations are captured as tickets the operator approves, rather than implemented inside this skill — the implementation happens separately via `/refactor`, `/implement`, or `/implement-batch`.
- A single up-front input gathering step and a single ticket-review touchpoint mid-run; no other interruptions.

## When to Use

**Use `/refactor-deep` for:**
- Periodic code-quality maintenance combined with architectural read-out.
- Preparing a codebase for a major feature where both tactical cleanup and structural rethinking are warranted.
- Generating a coherent batch of refactoring tickets after Phase 1's tactical pass has cleared noise.

**Don't use `/refactor-deep` for:**
- Quick tactical cleanup only — use `/refactor` standalone.
- Architectural analysis only — use `/review-arch` standalone.
- A fully autonomous run with no user interaction — use `/implement-project`'s quality pipeline (which invokes `/review-arch` in autonomous mode and produces an advisory report instead of cutting tickets).

**Rule of thumb:** If you want tactical cleanup *and* an architectural read-out *and* you're willing to spend a few minutes reviewing tickets, this is the skill.

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ /refactor-deep Workflow                                         │
└─────────────────────────────────────────────────────────────────┘

 ┌──────────────────────────────────────────────┐
 │  0. BRANCH SAFETY CHECK                      │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  1. GATHER UPFRONT INPUT                     │
 │  ────────────────────────────────────────    │
 │  1a. Scope                                   │
 │  1b. Refactor aggression ceiling             │
 │  1c. QA instructions                         │
 │  1d. Ticket-creation preference (Phase 2)    │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  2. PHASE 1 — /refactor                      │
 │  ────────────────────────────────────────    │
 │  Tactical cleanup (autonomous).              │
 │  /review-doc pass inside /refactor is        │
 │  suppressed; deferred to step 4.             │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  3. PHASE 2 — /review-arch (interactive)     │
 │  ────────────────────────────────────────    │
 │  • Noun analysis + blueprint                 │
 │  • Operator iterates on plan                 │
 │  • If ticket creation opted in:              │
 │    - Preview ticket set to operator          │
 │    - Operator approves / edits / removes     │
 │    - Tickets created in tracker              │
 │  • /review-arch produces advisory report     │
 │    only (no implementation).                 │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  4. UPDATE DOCUMENTATION (/review-doc)       │
 │  ────────────────────────────────────────    │
 │  Catches any stale docs from Phase 1's       │
 │  tactical changes.                           │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  5. COMPLETION SUMMARY                       │
 │  ────────────────────────────────────────    │
 │  Consolidated across phases. Includes        │
 │  tickets created (if any) and recommended    │
 │  next steps.                                 │
 └──────────────────────────────────────────────┘
```

The former third phase (a second `/refactor` after `/review-arch` implemented changes) is removed. `/review-arch` no longer implements changes, so there is nothing for a post-restructuring tactical cleanup to do.

## Workflow Details

### 0. Branch Safety Check

If on `main`/`master`, the skill asks the operator to confirm or to create a new working branch (`refactor-deep/<date>`). Otherwise, proceeds without asking.

### 1. Gather Upfront Input

| Field                       | Default        | Notes                                                                       |
|-----------------------------|----------------|-----------------------------------------------------------------------------|
| Scope                       | Entire codebase| Pass to both phases.                                                        |
| Refactor aggression ceiling | (operator picks)| Maximum / High / Low / Discuss. Applies to Phase 1 only.                    |
| QA instructions             | None           | Special verification steps beyond standard test suite. Passed to Phase 1 QA.|
| Ticket-creation preference  | Yes            | Yes / No / Preview-then-decide. Passed to `/review-arch` in Phase 2.        |

After this step, the only further user interaction is the ticket-review pause in Phase 2 (and only if ticket creation is opted in).

### 2. Phase 1 — Tactical Refactoring

Runs `/refactor` with the scope, aggression, and QA instructions from step 1. The `/refactor` skill's built-in `/review-doc` pass is suppressed; documentation is updated once at the end of `/refactor-deep`.

### 3. Phase 2 — Architectural Review (Advisory)

Runs `/review-arch` in **interactive mode** so it can offer to cut tickets at the end. `/review-arch` no longer implements changes (advisory as of v8.0.0); its job here is to analyze, surface the plan, and route recommended work into the tracker.

The operator participates in `/review-arch`'s plan-iteration phase (step 4 of `/review-arch`'s workflow) and the ticket-review phase (step 5). Behavior at the ticket-creation step depends on the operator's preference from step 1d:

- **Yes** — `/review-arch` proceeds with preview-and-approve ticket creation.
- **Preview-then-decide** — `/review-arch` builds the ticket set, shows it to the operator, and asks whether to create them.
- **No** — `/review-arch` skips ticket creation; produces advisory analysis only.

### 4. Update Documentation

Runs `/review-doc` once. Phase 1's tactical changes may have renamed functions or moved code; documentation is updated to reflect the current state.

### 5. Completion Summary

A consolidated summary across phases:
- Phase 1 statistics (commits, lines changed, batches completed/aborted).
- Phase 2 results (blueprint items proposed, tickets created or "declined").
- Documentation updates.
- Recommended next steps (named follow-up skill invocations).

## Andon Cord

This skill follows the shared autonomy discipline documented in [`references/autonomy.md`](../../../references/autonomy.md), including the shared handoff template for andon-cord pulls (pre-loaded options, recommendation with pre-rebutted counterargument, current-state snapshot, resume instructions).

The skill is largely autonomous. **Ticket review in Phase 2 is a planned interactive touchpoint**, not an andon-cord pull — it is the one expected mid-run user interaction.

**Triggers (skill-specific):**
- Phase workflow encounters an unrecoverable error.
- Git repository in unclean state that can't be resolved.
- Tracker is unavailable when ticket creation was approved — surface the proposed ticket set in the handoff so the operator can either fix the tracker or create tickets manually.
- Critical system error.

## Tips for Effective Use

1. **Pick the aggression ceiling carefully.** Maximum aggression is appropriate after substantial feature work has landed; lower ceilings are safer for incremental cleanup.

2. **Set ticket-creation preference up front.** It's the only mid-run user touchpoint; deciding ahead of time avoids surprises.

3. **Use `preview-then-decide` if you're unsure.** You'll see the proposed ticket set and can decide based on the actual content.

4. **The architectural analysis surfaces even if you decline ticket creation.** It appears in the completion summary as a planning artifact you can revisit.

5. **Review the completion summary's "Recommended next steps."** It names the natural follow-up — usually `/implement-batch` if a cohesive batch of tickets was cut, or "revisit later" if you declined ticket creation.

## Agent Coordination

`/refactor-deep` is a thin orchestrator. It delegates to:
- `/refactor` for Phase 1
- `/review-arch` for Phase 2 (interactive mode)
- `/review-doc` for the documentation pass

State maintained between phases is light — phase outcomes are captured for the consolidated summary; otherwise each sub-skill is self-contained.

## Abort Conditions

**Phase-level failures do NOT abort the workflow.** If Phase 1 finds nothing to refactor, proceed to Phase 2. If Phase 2 finds no architectural improvements, proceed to documentation update.

**Abort entire workflow only on andon-cord triggers** (see the Andon Cord section above).

**Agent failures within phases** are handled by the sub-workflow's own retry/abort logic.
