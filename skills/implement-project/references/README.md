# /implement-project - Autonomous Project Lead

## Overview

`/implement-project` takes a project from commander's intent to a single branch you can review and merge. You state the intent at startup and read the report at the end. In between, the skill decides what to do next and does it: implementing tickets, scoping new ones, refactoring, reviewing, hunting bugs.

Most runs start from a batch of tickets, typically drafted by `/scope-project`. The skill also accepts an open-ended goal ("make the CLI's config handling work end-to-end") and scopes its own tickets for it. That covers the open-ended work `/lead-project` used to handle. The workflow is the same either way: the tickets are simply the key tasks of the intent.

The skill implements the autonomy discipline in [`references/autonomy.md`](../../../references/autonomy.md): commander's intent, the andon cord with its shared handoff template, the cascade rule, and "log instead of escalate."

**What makes it different from a pipeline:**
- **Judgment over checklists.** There is no fixed quality pipeline. The skill holds a repertoire of skills and chooses what *this* project needs, the way a capable tech lead would. A two-ticket bug-fix project may need nothing past its tickets; a twelve-ticket feature may get `/refactor`, `/review-arch` and `/review-test`.
- **A small fixed floor.** Five things hold on every run regardless of judgment, because they are cheap and they carry the safety (see below).
- **Accountable judgment.** Every quality pass the skill chose not to run appears in the final report with a one-line reason, so you can audit the run's choices without having supervised it.

## When to Use

**Use `/implement-project` for:**
- A batch of scoped tickets you want implemented, verified, and brought to a review-ready branch without supervision
- The second half of the `/scope-project` → `/implement-project` pair
- An open-ended goal where you can say what "done" looks like, even if the tickets don't exist yet

**Don't use it for:**
- A single ticket (use `/implement`)
- One batch with no need for project-level judgment (use `/implement-batch`)
- Exploratory work with no definable end state
- Anything that must end in a published release; the skill stops short of publishing and leaves that to `/release`

## The Fixed Floor

| # | Always holds                                                      | Why                                                                   |
|---|-------------------------------------------------------------------|-----------------------------------------------------------------------|
| 1 | Tests and linters green at every merge into the project branch    | A broken branch compounds every later decision                        |
| 2 | The smoke-testing procedure passes before the run declares done   | Tests can pass while the product is broken                            |
| 3 | Mechanical end-state conditions are executed and observed to pass | "Done" is something the skill checks, never something it infers       |
| 4 | `/review-release` runs last, after all code changes               | Release hygiene must see the final tree                               |
| 5 | Irreversible-action gates are never crossed autonomously          | No merges to main, pushes, releases, or unauthorized breaking changes |

Everything else is judgment.

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ /implement-project Workflow                                     │
└─────────────────────────────────────────────────────────────────┘

 ┌──────────────────────────────────────────────┐
 │  1. STARTUP                                  │
 │  ────────────────────────────────────────    │
 │  1a. Branch, working tree, resume check      │
 │  1b. Commander's intent (six fields)         │
 │      Ticket-driven: pre-filled from tickets  │
 │      Open-ended: elicited field by field     │
 │  1c. Agree the smoke-testing procedure       │
 │  1d. Plan → YOUR APPROVAL → PROJECT_STATE.md │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  2. WORK LOOP (judgment)                     │◄──┐
 │  ────────────────────────────────────────    │   │
 │  Decide: blockers → key tasks → high-        │   │
 │          severity findings → quality passes  │   │
 │  Act:    invoke a repertoire skill; verify   │   │
 │          tests/lint green; commit            │   │
 │  Record: action, rationale, outcome in       │   │
 │          PROJECT_STATE.md                    │   │
 │                                              │   │
 │  Done? ──┬─ No  ─────────────────────────────┼───┘
 │          └─ Yes → termination                │
 │  (cap: 50 actions → andon cord)              │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  3. TERMINATION (fixed floor)                │
 │  ────────────────────────────────────────    │
 │  3a. Smoke test + mechanical end-state       │
 │      checks (failure → back to the loop)     │
 │  3b. /review-release (last)                  │
 │  3c. Final report: evidence for every claim, │
 │      a reason for every pass not run         │
 └──────────────────────────────────────────────┘
```

## Workflow Details

### 1. Startup

**1a. Branch, working tree, resume check.** The skill follows the shared startup protocol in [`references/lead-startup.md`](../../../references/lead-startup.md). It creates `feat/project-<name>` (confirmed with you), asks how to handle a dirty working tree, and offers to resume if `PROJECT_STATE.md` exists from an earlier run. Resuming re-observes the project (tests, branch, open tickets) before the next decision; if HEAD has moved since the state doc was written, it pulls the andon cord instead of guessing.

**1b. Commander's intent.** Six fields:

| Field       | Ticket-driven run (the common case)                                                | Open-ended run                                                               |
|-------------|------------------------------------------------------------------------------------|------------------------------------------------------------------------------|
| Purpose     | One line, derived from the tickets; you confirm                                    | Elicited: why this iteration exists                                          |
| Key tasks   | The tickets                                                                        | Elicited as observable state (2–10 items); the skill scopes tickets for them |
| End state   | Default: every ticket's acceptance criteria met; tests, linters, smoke test pass   | Elicited: what command proves it is done?                                    |
| Constraints | Default: none                                                                      | Elicited                                                                     |
| Non-goals   | Default: none                                                                      | Elicited                                                                     |
| Stakes      | Always asked: *what happens if this breaks?* and *who maintains it, for how long?* | Same                                                                         |

In a ticket-driven run you are not walked through six fields to restate your tickets. The skill pre-fills what the tickets imply and asks only for confirmation, the stakes, and any constraints or non-goals. In an open-ended run it walks the fields one at a time and pushes back on vague answers ("works well" → "what command would I run to verify?").

Each end-state condition is classified as **mechanical** (a check the skill can run, which gates termination) or **subjective** (needs your judgment, presented in the report for sign-off). If the batching of a ticket set is unclear, the skill asks rather than guessing.

**1c. Smoke-testing procedure.** You say what smoke testing proves the project works:

| Project type | Example smoke test                                        |
|--------------|-----------------------------------------------------------|
| CLI tool     | Run the binary with representative commands, check output |
| MCP server   | Build, send JSON-RPC calls, verify responses              |
| Web app      | Playwright against the critical user journeys             |
| Library      | Exercise the public API end-to-end                        |
| API server   | Hit key endpoints, verify responses                       |

The procedure is recorded verbatim. It is fixed-floor item 2, and it becomes the probe set whenever the run uses `/refactor`.

**1d. Plan and approval.** The skill presents intent, smoke procedure and an initial plan together: batch order and dependencies, any scoping needed, and which quality passes the project looks likely to need. This is the run's one planned interaction. The plan is a starting hypothesis; the loop revises it as the run learns.

### 2. Work Loop

Each iteration decides one action, takes it, verifies, and records it.

**Priorities:** blockers (broken tests, build, lint) first; then unfinished key tasks; then high-severity findings from reviews already run; then the quality passes the project needs. Before each decision the skill re-reads the pinned intent. Work that doesn't trace to it (scope creep, non-goals, polish on code the project didn't touch) is drift, which it corrects or escalates.

**The repertoire:**

| Group          | Skills                                                                        | Typical use                                                              |
|----------------|-------------------------------------------------------------------------------|--------------------------------------------------------------------------|
| Orientation    | `/review-health`                                                              | Start of an open-ended run on an unfamiliar codebase                     |
| Implementation | `/implement-batch`                                                            | A batch of tickets; the usual workhorse                                  |
|                | `/implement`                                                                  | A single ticket, or a fix too small to batch                             |
|                | `/scope`, `/scope-project`                                                    | A gap that serves intent; a whole open-ended key task                    |
|                | `/bug-fix`                                                                    | A bug that resists a direct fix                                          |
| Quality        | `/refactor`                                                                   | Shrink the machine once key tasks are done, before the reviews           |
|                | `/review-arch`, `/review-test`                                                | Structural and test-suite gaps, as ticket proposals                      |
|                | `/review-dead`, `/review-security`, `/review-perf`, `/review-a11y`            | When the project's changes touch their territory                         |
|                | `/review-code`                                                                | Adversarial correctness review of the project diff before declaring done |
|                | `/bug-hunt`                                                                   | When the project added substantial untested surface                      |
|                | `/tidy-docs`                                                                  | Documentation for what actually shipped                                  |
| Deliberation   | `/think-deliberate`, `/think-reframe`, `/think-diagnose`, `/think-scrutinize` | Close calls, a framing that seems wrong, unclear failures, risky plans   |

**Only when intent asks:** `/review-value` — its trade menu is product decisions, so the run surfaces the menu to you rather than acting on it.

**Never run autonomously:** `/release` (publishing is andon territory) and `/review-namespace` in search mode (it needs your calibration).

**After every action:** tests, linters and build still pass (fixed-floor item 1); the work is committed; the action, a one-sentence rationale and the outcome go into `PROJECT_STATE.md`.

**Findings by severity:** Critical/High are addressed before termination. Medium are addressed if bounded and local, otherwise deferred with a note. Low/Info are deferred with a note. When a review proposes tickets (`/review-arch`, `/review-test`, `/review-dead`, `/bug-hunt`), the skill approves items worth tracking and declines items it will handle inline. It prefers cutting a ticket when in doubt, because a decline commits the run to actually doing the work.

**No thrashing:** a review re-runs only if files it flagged have changed since, and two reviews contradicting each other on the same file pull the andon cord rather than oscillating.

#### How `/implement-batch` runs inside it

| `/implement-batch` step            | Override                                                                         |
|------------------------------------|----------------------------------------------------------------------------------|
| **Step 1** (receive tickets)       | Pre-loaded with the batch's tickets                                              |
| **Step 3** (batch planning)        | Approved autonomously; the cord is pulled only if the tickets are incoherent     |
| **Step 4** (create project branch) | Skipped; the batch runs on the project branch and its topic branches merge there |
| **Step 7** (final review)          | Reviewed autonomously; the summary is logged to the state doc                    |

An andon cord pulled inside a batch cascades up to `/implement-project`.

#### How `/refactor` runs inside it

`/refactor` normally stops once, for you, at its requirements menu. Here the skill answers the menu from intent, and everything after the menu runs as `/refactor` defines it:

| Menu part | Answered with                                                                                                                                               |
|-----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Stakes    | The Stakes field, verbatim                                                                                                                                  |
| Probes    | The smoke-testing procedure, verbatim, plus every ticket's acceptance criteria                                                                              |
| Verdicts  | Ratified: behavior the tickets or key tasks specify, plus Constraints. Documented: keep all. Invented: presumed dead. Priced: no trades taken; all reported |
| Non-goals | `/refactor` takes no exclusions; if Non-goals name code the run must not touch, it is not run, and the report says why                                      |

`/refactor` works on its own `refactor/<slug>` branch. When it finishes with the oracle green, the skill merges that branch into the project branch (`--no-ff`) and re-runs tests and the smoke procedure; a conflict or failure pulls the andon cord. The skill stands in for you at the menu and the merge and nowhere else: it never rescues an invented requirement, takes a trade, or overrides a gate. The trades `/refactor` offers and the bugs it found but didn't fix (its side memo) go into the final report for you.

If the project has no user-visible boundary to build an oracle against, the skill doesn't run `/refactor` at all, since its safety rests entirely on that oracle, and the report says so.

### 3. Termination

The skill judges the work done when the key tasks are complete and the project needs nothing more from the repertoire. The fixed floor then confirms it:

**3a. Smoke test and end-state checks.** It runs the smoke procedure and every mechanical end-state condition, recording each command and result, and checks the branch diff against protected paths in Constraints. Any failure sends it back to the loop.

**3b. `/review-release`.** This runs last. Mechanical findings (debug artifacts, version mismatches, changelog gaps) are fixed; ambiguous ones are deliberated; user-judgment items are deferred to the report; blocking failures pull the cord. If its fixes touch code, 3a runs again.

**3c. Final report.** The report is ordered by what most needs your scrutiny. Every claim of completion carries a one-sentence narrative *and* an artifact: a commit SHA, a command and its result, a file:line, or a ticket ID.

```
## Project Complete

### Outcome
### Top things to scrutinize        (3–5 items, one line + artifact each)
### Key tasks / tickets             ([✓] / [~] per ticket, with SHA)
### End state                       (mechanical results, subjective items for
                                     your sign-off, smoke test result)
### Quality passes                  (each pass run, with its result;
                                     each pass not run, with its reason)
### Deferred items                  (incl. /refactor's trade menu and side memo)
### Branch                          (SHAs, commit count, tickets created/closed)
```

You decide: merge, iterate, or discard.

## Andon Cord

The skill escalates only when autonomous resolution has failed or can't apply. Before pulling the cord it tries to resolve the problem itself, runs `/think-deliberate` for judgment calls, and re-reads intent, since an apparent blocker sometimes means intent needs clarifying.

**Triggers:**
- An irreversible action is required: pushing or merging to main/master, a public release or tag, force-push, global dependency installs, deleting data or untracked work, or a breaking change you haven't authorized
- A blocking decision needs product judgment that deliberation can't resolve from the repo
- The same failure three times across different strategies
- Two reviews contradict each other on the same file
- A merge conflicts, or a merge breaks tests and the cause isn't local
- A key task appears to require violating a constraint
- On resume, HEAD has diverged from the state doc's record
- The run is drifting and the right path is unclear
- A sub-skill's andon cord cascades up for a reason the skill can't resolve
- 50 actions without terminating, or 3 consecutive failed attempts at the same goal

The handoff uses the shared template in [`references/autonomy.md`](../../../references/autonomy.md): pre-loaded options, a recommendation, the tradeoff that would flip it, and a pre-rebutted counterargument, plus what is merged, what is in flight, and which key tasks remain.

## State File

`PROJECT_STATE.md` lives at the repo root, is gitignored, and is updated after every action. It is the run's memory across context compaction and resumption.

```markdown
# Implement-Project State

Started: 2026-11-03T09:12:00Z
Branch: feat/project-v2-release
Branch SHA at startup: 4e1a9c0
Base branch: main
Base SHA at startup: 4e1a9c0
Last cycle HEAD: b72d3f1
Status: active

## Commander's Intent
### Purpose
Ship the v2 API: auth, metrics, cache fix.
### Key tasks
#12, #15, #18
### End state
- [mechanical] `go test ./...` exits 0
- [mechanical] smoke procedure passes
### Constraints
Do not change the public API of package `client`.
### Non-goals
None.
### Stakes
Breakage takes down two internal dashboards; maintained by me for years.

## Plan
Batch 1: #12, #15 → batch 2: #18. Likely passes: /refactor, /review-arch,
/review-security (auth).

## Action log
### 1 — 09:31 — HEAD 8c02e11
- Action: /implement-batch (batch 1: #12, #15)
- Why: first key tasks; #18 depends on #12
- Outcome: merged; tests green

## Quality passes
- /review-security: queued (auth changes)

## Deferred items
## Open questions
```

## Examples

### Example 1: Ticket-driven run with judgment-chosen passes

```
User: /implement-project — tickets #12, #15, #18, #22, #25 (batches tagged)

Startup:
  Intent pre-filled from tickets; you confirm and answer stakes
  ("internal tool, two teams depend on it; I maintain it").
  Smoke: build, run `tool sync --dry-run` and `tool report`.
  Plan approved.

Loop:
  1. /implement-batch (batch 1: #12, #15, #18) — merged, tests green
  2. /implement-batch (batch 2: #22, #25) — merged, tests green
  3. /refactor (menu answered from intent) — 3 iterations; concepts 41 → 33,
     lines 6,210 → 4,980; oracle green; merged refactor/v2 → project branch;
     tests and smoke pass
  4. /review-arch — 1 item handled inline (SHA c91e0a2), 2 tickets cut (#48, #49)
  5. /tidy-docs — 3 updates

Termination: smoke + `go test ./...` pass; /review-release fixes a stale
  version string.

Report, quality passes:
  Run: /refactor, /review-arch, /tidy-docs, /review-release
  Not run: /review-test — every ticket shipped with tests and /refactor ported
           the behavior-level suite; no untested surface added
  Not run: /review-security — no auth, input-handling, or data-access changes
```

### Example 2: A small run that skips most passes

```
User: /implement-project — tickets #31, #32 (two small bug fixes)

Loop:
  1. /implement-batch (#31, #32) — merged, tests green

Termination: smoke passes; /review-release clean.

Report, quality passes:
  Not run: /refactor — 40-line diff in two functions; nothing to shrink
  Not run: /review-arch — no structural change
  Not run: /review-test — both fixes landed with reproducing tests
  Not run: /tidy-docs — no user-visible behavior or docs touched
```

### Example 3: Open-ended run that scopes its own tickets

```
User: /implement-project — "make config loading work end-to-end"

Startup (fields elicited):
  Purpose: users can configure the CLI from file, env, and flags
  Key tasks: config file loaded; env overrides file; flags override env
  End state: [mechanical] `make test` passes; [mechanical] the precedence
             matrix in the smoke procedure passes; [subjective] README
             config section reads clearly
  Non-goals: no new config formats beyond TOML

Loop:
  1. /review-health — config code is spread across three packages
  2. /scope-project — 4 tickets in 2 batches (#60–#63)
  3. /implement-batch (batch 1) — merged
  4. /implement-batch (batch 2) — merged
  5. /refactor — two parallel config readers dissolved into one; merged
  6. /tidy-docs — README config section rewritten

Report: mechanical conditions pass; the README condition awaits your sign-off.
```

### Example 4: Andon cord

```
## Andon Cord — /implement-project — /implement-batch (batch 2)

What went wrong: ticket #22 requires a new column in the `events` table;
  existing payloads would fail to deserialize. That is a breaking change
  the intent doesn't authorize.

Options:
  A. Authorize the schema change; the skill adds a migration and a CHANGELOG
     breaking-change note.
  B. Store the field in the existing JSON blob column; no schema change.
  C. Defer #22; finish the rest of the project.
Recommendation: B — it meets #22's acceptance criteria without a break.
Would flip if: the field must be indexed or queried.
Counterargument: "B is technical debt" — the blob already holds four
  comparable fields, so this matches the established pattern.

State: batch 1 merged; batch 2 has #20 merged and #22 in flight; key tasks
  remaining: #22, #25.
```

## Integration with Other Skills

| Skill              | Relationship                                                                                                      |
|--------------------|-------------------------------------------------------------------------------------------------------------------|
| `/scope-project`   | The planning half of the pair: drafts and adversarially reviews the batched tickets this skill executes           |
| `/implement-batch` | The workhorse for ticketed work: runs one batch with no project-level judgment; this skill supplies that judgment |
| `/implement`       | Runs per ticket inside `/implement-batch`; also used directly for single tickets or small fixes                   |
| `/refactor`        | Normally operator-run; this is the one caller that runs it unattended, by answering its menu from intent          |
| `/review-*`        | Chosen by judgment; ticket proposals approved or declined per `references/autonomy.md`                            |
| `/review-release`  | Always runs last (fixed floor)                                                                                    |
| `/release`         | Never invoked; publishing is yours to do after you merge                                                          |

## Tips

1. **Answer the stakes questions honestly.** They calibrate how aggressively `/refactor` cuts and how much the skill invests in verification.
2. **Make the smoke procedure concrete.** "Make sure it works" gives the skill nothing to run. "Build the binary and run `./tool --help` and `./tool sync --dry-run`" is a gate, and a probe set for `/refactor`'s oracle.
3. **Read "Top things to scrutinize" and "Quality passes" first.** That's where the run's judgment is concentrated, and where it is most likely to be wrong.
4. **Name your non-goals.** Explicit out-of-scope items are the cheapest protection against drift.
5. **Let it cut tickets.** Review findings it defers become tickets you can feed to the next run, rather than being lost.
