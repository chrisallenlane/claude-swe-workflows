---
name: review-code
description: Adversarial correctness review of a diff. Resolves the diff scope (working tree, branch, or commit range), dispatches a correctness reviewer that assumes a bug has already shipped, and presents evidence-cited findings. Advisory only — produces findings and proposes tickets; does not implement fixes.
model: opus
---

# Code Review — Adversarial Correctness Review of a Diff

Advisory-only correctness review of a change. Resolves what diff is under review, dispatches the `swe-correctness-reviewer` agent against it, presents the evidence-cited report, and proposes tickets for the findings. No changes are made.

## Philosophy

**The bug has already shipped.** Confirmation-oriented review ("does this look right?") rubber-stamps plausible-looking code. The reviewer instead assumes the diff was merged and caused a production incident, then works backward to the cause — verifying every assumption the diff makes (paths, symbols, signatures, runtime-version semantics) mechanically against the repo. An honest zero-findings verdict is a valid and respectable outcome.

**Diff-scoped, not repo-scoped.** Every sibling `/review-*` skill audits the repository; this one reviews a *change*. For repo-wide proactive bug discovery (risk-ranked, no specific diff in mind), use `/bug-hunt`. For "is this branch safe to merge?", use this skill. Because it is diff-scoped, `/review-health`'s follow-up never runs it — a repository review has no diff under review.

**Advisory here, blocking in `/implement` and `/bug-fix`.** The same `swe-correctness-reviewer` agent serves `/implement` step 9 and `/bug-fix` step 10 as blocking gates with a fix-and-re-review convergence loop. Invoked standalone through this skill, there is no pipeline to block: the skill runs a single review pass, presents the report, and proposes tickets. The operator decides what to do with the findings. To re-review after fixing, re-invoke `/review-code` — the fresh pass is the point, not a formality.

## Workflow Overview

```
┌──────────────────────────────────────────────────────┐
│                    CODE REVIEW                       │
├──────────────────────────────────────────────────────┤
│  1. Resolve diff scope (confirm with operator)       │
│  2. Dispatch swe-correctness-reviewer (fresh)        │
│  3. Present the report                               │
│  4. Propose tickets (approve / edit / decline)       │
└──────────────────────────────────────────────────────┘
```

## Workflow Details

### 1. Resolve Diff Scope

Accept an operator-specified scope in any of these forms:

| Operator says                       | Resolves to                                        |
|-------------------------------------|----------------------------------------------------|
| A commit range (`main..HEAD`, SHAs) | That range, verbatim                               |
| A branch name                       | `merge-base <main> <branch>`..`<branch>`           |
| "uncommitted" / "working tree"      | Staged + unstaged changes vs `HEAD`                |
| A PR/MR number                      | The PR's head range, resolved via `gh` or tracker  |

**If no scope is given, infer a default and confirm:**

- Dirty working tree → uncommitted changes (staged + unstaged) vs `HEAD`
- Clean tree, on a non-main branch → `merge-base <main> HEAD`..`HEAD`
- Clean tree, on main → `HEAD~1..HEAD` (the most recent commit)

Present the inferred scope with the file list and net line count, and wait for confirmation or an override. This is the one planned interaction point before the report. (When invoked by an orchestrator, the orchestrator supplies or confirms the scope per its own judgment — the skill does not branch on caller type.)

**Abort** if the directory is not a git repository or the resolved diff is empty.

### 2. Dispatch the Correctness Reviewer

Spawn a `swe-correctness-reviewer` agent (fresh context):

- **Provide:** the resolved diff scope (range or working-tree designation), and target runtime/framework versions if already known from the conversation
- **Do not provide:** any implementation rationale, design-history, or justification present in the conversation. The reviewer sees the diff and the repo, nothing else — context isolation is what makes the review effective. This applies with extra force when `/review-code` is invoked right after writing the code under review.
- The agent walks its six-concern spine (assumptions, runtime semantics, call sites, data flow, error paths, first-principles residual), maintains an assumption ledger, and classifies output into blocking-grade **findings** and non-blocking **residual risks**

This is a **single pass** — no convergence loop. The loop belongs to `/implement` step 9 and `/bug-fix` step 10, where an implementation agent exists to resolve findings. Here the operator owns resolution.

### 3. Present the Report

Relay the agent's report — assumption ledger, findings, residual risks, coverage notes, verdict — without paraphrasing the findings. The file:line evidence citations must survive verbatim; a summarized finding without its evidence is an assertion, not a review result.

Prepend a brief header: scope reviewed, file/line counts, verdict, finding count by classification.

In standalone use the "blocking" classification translates to **severity, not authority**: findings are the defects the operator should not merge without resolving; residual risks are the items needing non-analytical verification (staging run, manual check, telemetry). Say so in the header.

### 4. Propose Tickets

Follow the runtime ticket-proposal pattern in [`references/advisory-tickets.md`](../../references/advisory-tickets.md) (proposal form, approve/edit/decline dispatcher, orchestrator-invoked behavior).

**Shape catalog (skill-specific):**

| Finding mix                                  | Proposed structure                                                        |
|----------------------------------------------|---------------------------------------------------------------------------|
| Zero findings, zero residual risks           | No proposal — state explicitly that the report stands alone               |
| 1–3 independent findings                     | One ticket per finding                                                    |
| 4+ findings, or findings sharing a root cause| One ticket per cluster (by subsystem or shared root cause)                |
| Residual risks only                          | One verification ticket — a checklist of risks and how to verify each     |
| Findings + residual risks                    | Finding tickets per the rows above, plus one verification ticket          |

**Per-ticket body schema (skill-specific):**

- **Finding** — what and where (file:line)
- **Why it's a bug** — the concrete failure it produces
- **Evidence** — what the reviewer verified, with citations
- **Fix direction** — one line; the implementer has discretion on the actual fix
- **Acceptance criteria** — the falsified assumption now verified / the failure no longer reproducible; a regression test where feasible

**On decline:** exit cleanly with the analysis report; no tracker writes. (Same as `/review-arch` and `/review-security`.)

## Suggested Next Steps

Close the report with routing appropriate to the outcome:

- Findings on an unmerged branch → fix on the branch (directly, or via `/implement` with the report as context), then re-run `/review-code` for a fresh pass
- Findings on already-merged code → `/bug-fix` per finding, or work the created tickets via `/implement`
- Residual risks → name the concrete verification each one needs
- Zero findings → say so plainly; do not pad

## Agent Coordination

- One agent, one pass. No parallelism, no loop.
- If the agent fails or returns an unusable report, abort with the error — do not present a partial review as if it were complete.

## Abort Conditions

**Abort:**
- Not a git repository
- Resolved diff is empty
- Reviewer agent failure

**Do NOT abort:**
- Zero findings (valid outcome — report it)
- Huge diff (note in the report that the reviewer's coverage notes matter more than usual; suggest splitting the range across multiple invocations if coverage gaps are reported)
