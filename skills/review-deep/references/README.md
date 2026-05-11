# /review-deep - Comprehensive Pre-Release Review

## Overview

The `/review-deep` skill runs every `/review-*` skill in the plugin — eight in total — as a coordinated pipeline. It is a thin orchestrator: each sub-skill keeps its normal interactive behavior, and the operator participates throughout. Before execution starts, the orchestrator auto-detects phases that do not apply to the current project (no web content → no `/review-a11y`; no tests → no `/review-test`) and asks for confirmation on the proposed skip list. When all enabled phases are complete, it presents a single consolidated report synthesizing findings across every phase.

**Key benefits:**
- One entry point for the full pre-release review sweep — no need to remember the order or invoke each skill manually
- Skip detection keeps the pipeline from running irrelevant phases (no web → no a11y, no tests → no test review)
- Branch safety check up front, so the sweep's commits do not land directly on `main`/`master`
- Consolidated final report surfaces cross-cutting themes that no single sub-skill would see

**This is an interactive pipeline.** You stay engaged with every sub-skill's decision points. `/review-deep` does not run autonomously — it is meant to replace the manual "run each review in turn" dance, not replace your participation in the reviews.

## When to Use

**Use `/review-deep` for:**
- Pre-release readiness sweeps
- Periodic comprehensive audits of a codebase
- After a large feature or refactoring effort, when you want to inspect every review dimension at once
- Onboarding to an unfamiliar codebase (paired with an operator who can answer the sub-skills' prompts)

**Don't use `/review-deep` for:**
- Targeted single-dimension review — use the individual `/review-*` skill directly
- Fire-and-forget automation — this skill is interactive; the operator is expected to participate
- Bug hunting — use `/bug-hunt` or `/bug-fix`
- Change-oriented refactoring sweeps — use `/refactor-deep`

**Rule of thumb:** If the goal is "evaluate the state of the codebase across every dimension before shipping", `/review-deep` is the right entry point. If the goal is targeted (fix one thing, review one area), invoke the relevant skill directly.

## Workflow

```
┌──────────────────────────────────────────────────────┐
│                 REVIEW-DEEP WORKFLOW                 │
├──────────────────────────────────────────────────────┤
│  0. Branch safety check                              │
│  1. Skip detection + user confirmation               │
│  2. Execute enabled phases, in order:                │
│     a. /review-health                                │
│     b. /review-arch                                  │
│     c. /review-security                              │
│     d. /review-perf                                  │
│     e. /review-a11y                                  │
│     f. /review-test                                  │
│     g. /review-doc                                   │
│     h. /review-release                               │
│  3. Consolidated final report                        │
└──────────────────────────────────────────────────────┘
```

### 0. Branch Safety Check

If you are on `main` or `master`, the orchestrator offers to create `review-deep/<date>` for you. On any other branch, it proceeds without asking.

### 1. Skip Detection + User Confirmation

The orchestrator scans the project and proposes skipping phases that do not apply:

| Phase              | Skipped when                                                                           |
|--------------------|-----------------------------------------------------------------------------------------|
| `/review-security` | No meaningful executable source code (e.g., a plugin or docs-only repo)                 |
| `/review-perf`     | No meaningful executable source code                                                    |
| `/review-a11y`     | No web content (`.html`, `.jsx`, `.tsx`, `.vue`, `.svelte`, `.css`, templates)          |
| `/review-test`     | No tests detected (no test directories, no `*_test.go` / `test_*.py` / `*.test.ts` / etc.) |

You can override in either direction — force-run a proposed-skip phase, or skip a phase that was not proposed for skipping. `/review-health`, `/review-arch`, `/review-doc`, and `/review-release` always run unless you explicitly opt out.

### 2. Execute Enabled Phases

Each phase runs in order. The orchestrator announces the phase, then hands control to the sub-skill. You interact with the sub-skill directly — answering its scope questions, boldness prompts, selection menus, and so on. When the sub-skill completes, the orchestrator captures its summary and transitions to the next phase.

Individual phase failures or mid-phase aborts do not kill the workflow. If a phase fails or you abort it, the orchestrator asks whether to continue with the next phase or end the workflow.

### 3. Consolidated Final Report

A single report aggregating every enabled phase:
- Phases table with status and key outcome per phase
- Summary of commits made during the sweep (via `git log` from the branch-start point)
- Cross-cutting observations synthesized across phases
- Outstanding recommendations — items a sub-skill surfaced but did not implement
- Release readiness verdict carried forward from `/review-release`

## Phases at a Glance

| Phase              | What it does                                                      | Makes changes? |
|--------------------|-------------------------------------------------------------------|----------------|
| `/review-health`   | Strategic-orientation review: classification + per-class rubric   | No             |
| `/review-arch`     | Noun-analysis architectural review; advisory; offers to cut tickets | No           |
| `/review-security` | White-box security audit (blue team + red team + synthesis)       | No             |
| `/review-perf`     | Compute and/or web performance review                             | No             |
| `/review-a11y`     | WCAG conformance audit on web content                             | No             |
| `/review-test`     | Coverage gaps, fuzz opportunities, and test quality audit         | Yes            |
| `/review-doc`      | Comprehensive documentation audit and fixes                       | Yes            |
| `/review-release`  | Pre-release readiness check with final verdict                    | Yes            |

Advisory-only phases produce reports you can act on manually or via `/refactor` or `/implement`. Change-making phases have their own interactive decision points — you choose what lands.

## Tips

1. **Set aside time.** Eight phases with interactive decision points is a substantial session. `/review-deep` is meant for when you can stay engaged, not when you need to step away.

2. **Take the branch.** Even if the advisory phases make no changes, `/review-test`, `/review-doc`, and `/review-release` all can. Accepting the `review-deep/<date>` branch keeps `main`/`master` clean while you work.

3. **Do not fight the skip detection.** If the orchestrator proposes skipping a phase, it is usually right. Override only when you have a specific reason (e.g., you're about to add tests but want to see what `/review-test` would recommend against the current state).

4. **Address issues phase-by-phase, not all at once.** Each phase gives you a chance to act on findings or defer them. Deferring everything to the final report sounds efficient but buries findings in a larger document — act on what you can when each phase surfaces it.

5. **Use the cross-cutting observations.** The final report's cross-cutting section is the unique value `/review-deep` adds over running each skill manually. If three phases flag the same concern, that is a project-level signal worth acting on.

6. **Running it back-to-back with `/refactor-deep` is usually redundant.** Both share `/review-arch` and `/review-doc`. Pick one based on the goal — `/refactor-deep` for change-oriented cleanup, `/review-deep` for release-readiness evaluation.

## Integration with Other Skills

| Skill              | Relationship                                                                                            |
|--------------------|---------------------------------------------------------------------------------------------------------|
| `/lead-project`    | May invoke `/review-deep` near the end of a run as a comprehensive validation pass, or invoke individual `/review-*` skills earlier when specific concerns arise. |
| `/review-health`   | Phase 1                                                                                                 |
| `/review-arch`     | Phase 2                                                                                                 |
| `/review-security` | Phase 3                                                                                                 |
| `/review-perf`     | Phase 4                                                                                                 |
| `/review-a11y`     | Phase 5                                                                                                 |
| `/review-test`     | Phase 6                                                                                                 |
| `/review-doc`      | Phase 7                                                                                                 |
| `/review-release`  | Phase 8                                                                                                 |
| `/refactor-deep`   | Sibling workflow — change-oriented cycle (refactor → advisory arch review → doc). Usually one or the other, not both. |
| `/implement-project` | Contains its own post-batch quality pipeline. `/review-deep` is the standalone equivalent for use outside a ticket-driven project. |

## Resource Usage

Substantial. Eight sub-skills, each of which may spawn its own agents. Expect a long session with many sub-agent invocations — especially during `/review-security` (heavy by design) and `/review-test` (three internal phases). Plan accordingly.
