---
name: lead-review
description: Autonomous comprehensive review. Once-through pipeline over /review-health, /review-arch, /review-security, /review-perf, /review-a11y, /review-test, /review-release. Operator-configurable ticket creation at startup — when ON, auto-approves sub-skill ticket proposals per the orchestrator-family contract; when OFF, uniformly declines and surfaces findings in the consolidated report. Auto-detects sub-skills that do not apply (no web content → skip /review-a11y; no tests → skip /review-test).
model: opus
---

# Lead-Review — Autonomous Comprehensive Review

Drives a codebase through every review dimension — orientation, architecture, security, performance, accessibility, tests, release-readiness — without operator involvement between startup and termination. The operator states scope, whether tickets should be cut, and (if so) the severity floor for ticket creation. The skill then runs each enabled sub-skill in sequence, auto-approving or auto-declining ticket proposals uniformly per the startup choice. Termination is structural — once all enabled sub-skills have run, the consolidated report is produced.

This skill is the successor to `/review-deep`. The v10 move into the `/lead-*` namespace makes the autonomy-axis identity explicit; the redesign trades interactive participation for autonomous execution and adds the ticket-creation toggle so the run can serve both "produce a comprehensive backlog" and "produce a comprehensive audit report" use cases.

## Philosophy

This skill implements the autonomy discipline documented in [`references/autonomy.md`](../../references/autonomy.md). The shared discipline governs the five levers (altitude rule, pre-loaded options, pre-rebutted recommendation, commander's intent, risk budgets), the cascade rule, the no-unilateral-breaking-changes guardrail, and the shared handoff template.

### Two modes from one workflow

The same pipeline serves two operator intents:

- **Backlog generation** (tickets ON) — autonomous review-driven ticket creation. The skill runs every enabled review sub-skill, auto-approves each one's ticket proposals at or above the severity floor, and produces a consolidated, batch-tagged backlog the operator can feed to `/implement-project` or `/lead-refactor`.
- **Audit report** (tickets OFF) — autonomous comprehensive audit. The skill runs every enabled review sub-skill, auto-declines all ticket proposals uniformly, and surfaces all findings in the consolidated completion report. No tracker writes.

The operator chooses at startup. There is no mid-run switching.

### Operator intent is sovereign

The orchestrator does not paternalize. If the operator runs with **tickets OFF**, a CRITICAL finding does not trigger automatic ticket creation, override, or andon-cord interruption — it is flagged prominently in the completion report and the operator decides what to do. The autonomy contract is "do what was authorized at startup, nothing more, nothing less." Overriding commander's intent silently would violate that contract.

### Auto-approval (or auto-decline) of ticket proposals is a contract shift

`/review-arch`, `/review-test`, `/review-security`, and `/review-health` are advisory in their native contracts — they produce ticket *proposals* that require operator approval. When invoked under `/lead-review`, those approvals are granted (or declined) automatically per the startup choice. This is consistent with the autonomy discipline: commander's intent authorizes the contract shift; sub-skill prompts are answered by the orchestrator. The completion report lists every ticket action (created or declined) so the operator can audit.

### Once-through, not loop

Reviews produce findings; they don't drive toward a converged state. Looping over them is structural ceremony — the second pass would find roughly the same things as the first unless the codebase changed in between. `/lead-review` runs each enabled sub-skill exactly once.

### Broad authority, narrow gates

The skill may: invoke `/review-health`, `/review-arch`, `/review-security`, `/review-perf`, `/review-a11y`, `/review-test`, `/review-release`; create or decline tickets via auto-approved or auto-declined proposals; create and modify the working branch (no commits expected, but tracker writes are commits-in-spirit).

The skill may NOT without explicit authorization: push or merge to main/master, force-push, propose breaking changes (see `references/autonomy.md` § "No unilateral breaking changes"), invoke skills outside the bounded review repertoire, install dependencies, run irreversible destructive operations.

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                    LEAD-REVIEW WORKFLOW                          │
├──────────────────────────────────────────────────────────────────┤
│  0. Startup                                                      │
│     ├─ 0a. Branch and working-tree check                         │
│     ├─ 0b. Resume existing run or start fresh                    │
│     ├─ 0c. Elicit commander's intent (4 fields)                  │
│     ├─ 0d. Auto-detect skip-list, confirm with operator          │
│     └─ 0e. Seed LEAD_REVIEW_STATE.md                             │
│                                                                  │
│  1. Phase 1: /review-health (orientation)                        │
│  2. Phase 2: /review-arch (architecture)                         │
│  3. Phase 3: /review-security (security)                         │
│  4. Phase 4: /review-perf (performance)                          │
│  5. Phase 5: /review-a11y (accessibility) — if applicable        │
│  6. Phase 6: /review-test (test suite)                           │
│  7. Phase 7: /review-release (release readiness)                 │
│                                                                  │
│  8. Termination                                                  │
│     └─ Consolidated report                                       │
└──────────────────────────────────────────────────────────────────┘
```

Each enabled sub-skill runs once. Skipped sub-skills are recorded in the cycle log and surfaced in the report.

## Workflow Details

### 0. Startup

#### 0a. Branch and working-tree check

- Identify the main branch (`main` or `master`).
- If on `main`/`master`: create `lead-review/<date>` (e.g., `lead-review/2026-05-12`) from current HEAD and check it out. Confirm the branch name with the user before creating.
- Check working tree status:
  - Clean → proceed.
  - Dirty → **ask the user** how to handle uncommitted work: commit as-is, stash, discard, or abort. Do not guess.

Note: `/lead-review` does not itself commit code. The branch is the integration point for any commits sub-skills make (rare — most review sub-skills are advisory) and the boundary for any tickets cut.

#### 0b. Resume existing run or start fresh

Check for `LEAD_REVIEW_STATE.md` at the repo root:

- **If absent:** proceed to intent elicitation.
- **If present:** read it. Verify the recorded branch still exists, is currently checked out, and the current HEAD matches `Last cycle HEAD` from the state doc.
  - **HEAD matches and branch is current** — summarize current phase, pinned intent, and completed phases to the user. Offer three options:
    1. **Resume** as-is (re-check skip-list, continue from the next enabled phase).
    2. **Resume with updated intent** — re-elicit, preserving the cycle log.
    3. **Start fresh** — archive the existing state doc to `LEAD_REVIEW_STATE.<timestamp>.md` and re-elicit intent.
  - **HEAD has moved or branch has changed** — do NOT auto-resume. Pull the andon cord with a handoff explaining the divergence and let the operator decide.

#### 0c. Elicit commander's intent (interactive)

Walk the user through four fields, one at a time. Do not accept a single free-form paragraph — the structure is load-bearing.

1. **Scope** — "What is the scope of the review? Entire codebase, specific modules, or specific areas of concern? Are there directories or files to explicitly exclude (e.g., generated code, vendored code)?"

2. **Ticket creation** — "Should this run cut tickets for findings, or produce a report only? **Yes** — advisory sub-skills' ticket proposals are auto-approved at or above the severity floor; you get a consolidated backlog in the tracker. **No** — all ticket proposals are auto-declined; findings surface in the completion report only, no tracker writes."

3. **Severity floor** — only asked if field 2 = Yes. "What is the lowest severity that gates ticket creation? **Critical+High** is the default. Setting this lower produces a larger backlog including polish-level work; setting this higher means only the most serious findings get tickets and the rest surface as findings in the report."

4. **Constraints** — "Hard limits the skill should pass through to sub-skills. Examples: don't audit `pkg/legacy` (slated for removal), don't propose breaking changes to the public API of package X, must remain compatible with library version Y."

**Push back on vague answers.** "Just check everything" is not a scope — ask about exclusions. "Whatever severity" is not a floor — push for Critical+High as the productive default. Several rounds of dialogue is normal.

Read back the complete intent and ask for confirmation before proceeding.

#### 0d. Auto-detect skip-list and confirm

Inspect the codebase to determine which review sub-skills do not apply:

- **No web content** (no HTML, JSX/TSX, Vue, Svelte, CSS, templates) → skip `/review-a11y`
- **No test suite detected** → skip `/review-test` (or warn; operator may want to run it anyway to flag the absence)
- **No deployable target** (no Dockerfile, no release tags, no build pipeline config) → consider whether `/review-release` adds value; default is to run it anyway since it scans for debug artifacts and version mismatches even without a deployment

Present the proposed skip-list and the enabled-list to the operator. Confirm before proceeding.

#### 0e. Seed `LEAD_REVIEW_STATE.md`

Create the state document at the repo root with:

- Pinned intent (all four fields, verbatim)
- Enabled-list and skip-list (with reasons for skips)
- Branch name and base branch
- Creation timestamp
- Current phase: `phase-1`
- Empty cycle log
- Empty findings ledger

**Add `LEAD_REVIEW_STATE.md` to `.gitignore`** if not already present. Commit the `.gitignore` change separately.

### 1–7. Phases — Sub-Skill Invocations

Each enabled sub-skill runs exactly once. The phases are sequenced so earlier phases inform later ones (orientation → architecture → security → performance → accessibility → tests → release-readiness).

For each phase:

1. **Invoke** the sub-skill with the scope and constraints from commander's intent.
2. **Answer the sub-skill's interactive prompts autonomously** using engineering judgment anchored to commander's intent. Specifically:
   - For advisory sub-skills (`/review-arch`, `/review-security`, `/review-test`, `/review-health`) that reach a ticket-proposal step:
     - **Tickets ON** — auto-approve all proposed tickets at or above the severity floor. Below-floor proposed tickets are declined and the findings are recorded for the consolidated report.
     - **Tickets OFF** — auto-decline all proposed tickets uniformly. Findings are recorded for the consolidated report.
   - For non-ticket sub-skills (`/review-perf`, `/review-a11y`, `/review-release`) — accept the produced report and record findings.
3. **Record** the sub-skill's outcome in the cycle log: findings count by severity, tickets created (with IDs), tickets declined, sub-skill duration (approximate).
4. **Update** state doc: current phase advances; previous phase marked complete.

If a sub-skill cord cascades up (`/review-arch` pulls its own cord, etc.), the orchestrator catches it per `references/autonomy.md` § "Cascade rule" — either resolves it (rare for review work) or pulls its own cord at a higher altitude.

If a sub-skill produces a finding the orchestrator believes is wrong on substance (e.g., a CRITICAL severity classification that contradicts a constraint in commander's intent), record it in `## Contested findings` and pull the andon cord. **Do not silently dismiss.**

If a sub-skill recommends a fix that requires a breaking change (per `references/autonomy.md` § "No unilateral breaking changes"), record it in `## Breaking-change findings` and pull the andon cord. Do not auto-approve such tickets.

### 8. Termination

Termination is structural — every enabled phase completes, no andon cord pulled.

#### 8a. Consolidated report

Produce a single report aggregating every enabled phase. The report is ordered by review priority — sections most likely to need operator scrutiny come first.

```
## Lead-Review Complete

### Commander's intent
[All four fields, verbatim]

### Run mode
- Tickets: <ON | OFF>
- Severity floor: <Critical+High | etc.> (or "N/A — tickets OFF")
- Scope: <verbatim>

### Top things to scrutinize
[Three to five items where the skill's judgment is most likely to need
 review. Each item: one sentence + artifact (SHA, ticket ID, file:line,
 finding ID). Examples: CRITICAL findings in tickets-OFF mode, contested
 findings, breaking-change-requiring fixes, sub-skill cords cascaded.]

### Cross-cutting observations
[Findings that appeared across multiple sub-skills — the unique value
 /lead-review adds over running each skill manually. E.g., the same
 module flagged by /review-arch (boundary issue) and /review-security
 (privilege concentration) and /review-test (coverage gap).]

### Phase summary
- [✓] /review-health — N findings (K Critical, L High, M Medium, N Low) — duration: ~X min
- [✓] /review-arch — N findings, K tickets created (ON) | K tickets declined (OFF)
- [✓] /review-security — N findings, K tickets created (ON) | K tickets declined (OFF)
- [✓] /review-perf — N findings
- [SKIP] /review-a11y — no web content detected
- [✓] /review-test — N findings, K tickets created (ON) | K tickets declined (OFF)
- [✓] /review-release — N findings (debug artifacts: K, version mismatches: K, changelog gaps: K)

### Tickets (if tickets ON)
- [#N] <title> — /review-arch finding — severity HIGH
- [#N+1] <title> — /review-security finding — severity CRITICAL
- ...
(grouped by sub-skill or severity, operator's preference inherited from sub-skills' default behavior)

### Findings declined or below floor (if tickets ON)
- [Medium | /review-arch | sub-skill cycle 1] <description>
- [Low | /review-test | sub-skill cycle 1] <description>
- ...

### Findings surfaced for operator review (if tickets OFF)
- [CRITICAL | /review-security] <description> — <one-line attack summary> — see SKILL output
- [HIGH | /review-arch] <description>
- ...
(grouped by severity, then by sub-skill)

### Contested or breaking-change findings (if any escalated)
- [contested | phase 3 /review-security] <description> — andon-cord SHA <short> in state doc
- ...

### Sub-skills skipped
- /review-a11y — no web content detected
- ...

### Changes summary
- Branch: <branch name> (SHA <short>)
- Base: <base branch> (SHA <short>)
- Commits on branch: N (typically 0 for /lead-review; sub-skills are advisory)
- Tickets created: N (if tickets ON)

### Run metadata
- Phases run: K of 7
- Phases skipped: M (with reasons)
- Andon-cord pulls during run: N (each with handoff in state doc)
- Duration (wall-clock, approximate)
```

The operator decides next steps — most commonly, feed the backlog to `/implement-project` (tickets ON) or address the findings directly (tickets OFF).

## Commander's Intent — Field Reference

### Scope

What the review pipeline covers. Same shape as the individual `/review-*` skills' scope.

Examples:
- "Entire codebase, excluding `vendor/` and `gen/`."
- "Just `pkg/auth` and `pkg/session`."
- "All production code, with extra attention to `pkg/payments`."

### Ticket creation

Single binary choice. The mode-defining field.

| Setting | Effect                                                                                                                  |
|---------|-------------------------------------------------------------------------------------------------------------------------|
| Yes     | Backlog-generation mode. Auto-approve sub-skill ticket proposals at or above severity floor. Tracker writes occur.       |
| No      | Audit-report mode. Auto-decline all sub-skill ticket proposals. No tracker writes. Findings surface in completion report. |

### Severity floor

Only consulted when ticket creation is Yes. The lowest severity that gates ticket creation.

| Floor              | Effect                                                                                                          |
|--------------------|-----------------------------------------------------------------------------------------------------------------|
| CRITICAL only      | Smallest backlog. Ships with HIGH+MEDIUM+LOW deferred. Use for "fix only the worst" sweeps.                      |
| HIGH+              | **Default.** Reasonable backlog covering real-impact findings.                                                   |
| MEDIUM+            | Larger backlog including moderate-severity work.                                                                 |
| All severities     | Largest backlog. May produce hundreds of tickets in mature codebases.                                            |

### Constraints

Hard limits beyond the always-on guardrails (no breaking changes, no main/master writes).

Examples:
- "Do not propose changes to the public API of package `auth`."
- "Do not audit `pkg/legacy`."
- "Must remain Go 1.22 compatible (any version-bump recommendation pulls the cord)."

## Severity & Triage

When tickets ON, triage is mechanical against the severity floor.

- **Floor and above** → ticket auto-approved, created in tracker.
- **Below floor** → ticket auto-declined. Finding recorded in `## Findings declined or below floor` in the completion report.
- **Contested on substance** → andon cord. The skill does not silently dismiss.
- **Breaking change required** → andon cord. The skill does not auto-approve.

When tickets OFF, all findings are recorded in the completion report grouped by severity. The skill does not auto-suppress low-severity findings — every finding the sub-skills produced is in the report.

The skill does NOT:
- Re-rank sub-skills' severity classifications. The reviewer's judgment stands.
- Override commander's intent's ticket setting because a CRITICAL finding "feels important." The operator chose the mode; their intent is sovereign.
- Drop findings to reduce report length.

## Andon Cord Protocol

The andon cord is the only planned escalation path. Pull sparingly but decisively. Use the **shared handoff template** from `references/autonomy.md` § "Shared handoff template," with the skill-specific extensions below.

### Andon cord triggers

Pull the cord when:

- **Contested finding.** The skill believes a sub-skill's finding is wrong on substance — the severity classification contradicts a constraint in commander's intent, the analysis misreads the code, etc.
- **Breaking-change required.** A sub-skill's recommended fix would require a breaking change (per `references/autonomy.md` § "No unilateral breaking changes"). Even though `/lead-review` does not implement fixes, the ticket would carry a breaking-change implication; surface it.
- **Sub-skill cord cascaded up.** A review sub-skill pulled its own cord for a reason this skill cannot resolve.
- **Resume-time HEAD divergence.** On resume, recorded branch SHA does not match current HEAD.

### Handoff format

Use the shared template from `references/autonomy.md`. Skill-specific extensions:

- **Title** — `## Andon Cord — /lead-review — Phase N (<sub-skill>)`
- **Current state** must additionally include:
  - `Current phase: <N of 7> (<sub-skill>)`
  - `Phases complete: <list>`
  - `Phases remaining: <list>`
  - `Findings ledger so far: <N created, M declined, K contested>`
  - `State doc pointer: see LEAD_REVIEW_STATE.md`

After pulling the cord: stop. Do not advance to the next phase. Wait for operator input.

## State Management

### `LEAD_REVIEW_STATE.md`

Maintained at the repo root. Gitignored. Survives across invocations.

**Structure:**

```markdown
# Lead-Review State

Started: <timestamp>
Branch: <branch-name>
Branch SHA at startup: <short SHA>
Base branch: <main-branch>
Base SHA at startup: <short SHA>
Last cycle HEAD: <short SHA>
Current phase: <phase-1 .. phase-7 | termination>
Status: <active | paused-on-andon | complete>

## Commander's Intent

### Scope
<verbatim>

### Ticket creation
<Yes | No>

### Severity floor
<CRITICAL only | HIGH+ | MEDIUM+ | All> (or "N/A — tickets OFF")

### Constraints
- <constraint 1>

## Enabled phases

- [✓] /review-health
- [✓] /review-arch
- [✓] /review-security
- [✓] /review-perf
- [SKIP] /review-a11y — <reason>
- [✓] /review-test
- [✓] /review-release

## Cycle log

### Phase 1 — /review-health — <timestamp> — HEAD <short SHA>
- Findings: K Critical, L High, M Medium, N Low
- Tickets created: N (or "N/A — tickets OFF")
- Tickets declined: N (or "N/A — tickets OFF")
- Duration: ~X min
- Notes: <anything noteworthy>

### Phase 2 — /review-arch — <timestamp> — HEAD <short SHA>
- ...

## Findings ledger

### Created (if tickets ON)
- [Phase 2 | ticket #14 | HIGH] <description>
- ...

### Declined / below floor (if tickets ON)
- [Phase 2 | MEDIUM] <description>
- ...

### Surfaced for operator (if tickets OFF)
- [Phase 3 | CRITICAL] <description>
- ...

### Contested
- [Phase 3] <description> — andon cord pulled, see § Andon Cord history

### Breaking-change-required
- [Phase 2] <description> — andon cord pulled, see § Andon Cord history

## Andon cord history

### Phase N pull
<full handoff text, pasted>

## Open questions

- <question>
```

**Update at every phase transition.** The state doc is the durable orientation — losing it means losing the agent's memory.

### `.gitignore`

Ensure `LEAD_REVIEW_STATE.md` is ignored. Commit the `.gitignore` change on the working branch at startup if needed.

## Hard Caps

- **No iteration cap** — once-through pipeline has structural termination. Each enabled sub-skill runs exactly once.
- **3 consecutive andon-cord triggers from the same sub-skill** — if the same sub-skill produces contested findings repeatedly (3+ in one invocation), pull the cord rather than trying to triage individually.
- **No file-touch or dependency-change budgets** — explicitly excluded per `references/autonomy.md` § "Risk budgets."

## Integration with Other Skills

**Relationship to individual `/review-*` skills:**

`/lead-review` invokes the review sub-skills as its workhorses. Each sub-skill keeps its native contract — `/review-arch` performs noun analysis, `/review-security` runs the blue/red parallel-isolated audit, etc. The orchestration layer adds: scope passthrough from commander's intent, auto-approval or auto-decline of ticket proposals per startup choice, consolidated reporting, autonomous execution across the full pipeline.

Run individual `/review-*` skills directly when you want a single dimension audited; run `/lead-review` when you want comprehensive coverage unattended.

**Relationship to `/implement-project`:**

Natural composition: `/lead-review` (tickets ON) produces a comprehensive backlog → `/implement-project` works through the backlog. `/lead-review` is the planning half; `/implement-project` is the execution half.

**Relationship to `/lead-refactor`:**

`/lead-refactor` runs `/review-arch` internally (within Phase 2). Operators who want both can run `/lead-review` (broad audit with backlog) and then `/lead-refactor` (deep refactor sweep), but the architectural review will run twice. For efficiency: pick one based on goal — `/lead-review` for evaluation across all dimensions, `/lead-refactor` for change-oriented cleanup.

**Relationship to `/lead-bug-hunt`:**

Sibling orchestrator. `/lead-bug-hunt` is bug-elimination-specific; `/lead-review` is multi-dimensional review. Both follow the orchestrator-family contract (auto-approval of sub-skill tickets, severity floor, andon protocol).

**Relationship to `/lead-project`:**

`/lead-project` is the broadest orchestrator — it takes open-ended commander's intent and decides which skills to invoke. `/lead-project` may invoke `/lead-review` near the end of a run as a comprehensive validation pass, or invoke individual `/review-*` skills earlier when specific concerns arise.

**Out-of-axis skills:**

`/tidy-docs` is not in this skill's repertoire. It is a `/tidy-*` (mechanical mutations), not a `/review-*` (advisory). Including it would muddy `/lead-review`'s contract — operators in tickets-OFF mode expect "evaluation only, no tree mutations," and `/tidy-docs` would commit doc changes. Run `/tidy-docs` separately after `/lead-review` if you want doc tidying.

Other out-of-axis skills: `/scope-*`, `/test-mutation`, `/tidy-git`, `/bug-*`, `/refactor`, `/implement-*`. If your goal mixes review with implementation or refactoring, use `/lead-project` instead, or chain `/lead-review` with `/implement-project` / `/lead-refactor`.
