---
name: implement-project
description: Autonomous project lead. Takes commander's intent — usually a batch of scoped tickets, sometimes an open-ended goal — and drives the project to a review-ready branch, choosing by judgment which implementation, refactoring, review, and bug-hunting skills to run and when. A small fixed floor (tests green at every merge, smoke test, release review last, mechanical end-state checks) holds regardless; every quality pass not run is accounted for in the final report. Escalates via andon cord only for irreversible actions or genuinely blocking decisions.
model: opus
---

# Implement-Project — Autonomous Project Lead

Takes the project from commander's intent to a single branch the user can review and merge. The user states intent at startup and reads the report at the end; between those points the skill decides what to do next and does it.

Most runs start from a batch of tickets, typically drafted by `/scope-project`. The skill also accepts an open-ended goal ("make the CLI's config handling work end-to-end") and scopes its own tickets. The workflow is the same either way: the tickets are simply the key tasks of the intent.

## Philosophy

This skill implements the autonomy discipline in [`references/autonomy.md`](../../references/autonomy.md): the five levers, the cascade rule, the shared handoff template, and "log instead of escalate." Its commander's-intent schema is the canonical one defined there.

**Judgment over checklists.** The skill has no fixed quality pipeline. It holds a repertoire of skills and chooses among them the way a capable tech lead would: what does *this* project, at *this* point, need next? A two-ticket bug-fix project may need nothing past its tickets; a twelve-ticket feature may need `/refactor`, `/review-arch`, and `/review-test`. Running a pass because a list says so wastes the run; skipping one the project needed is a judgment error the report must make visible.

**A small floor is fixed.** These hold on every run, regardless of judgment, because they are cheap and they carry the safety:

1. **Tests and linters green at every merge** into the project branch.
2. **The smoke-testing procedure** passes before the run declares done.
3. **Mechanical end-state conditions** are executed and observed to pass — never inferred.
4. **`/review-release` runs last**, after all code changes.
5. **The irreversible-action gates** (see Andon Cord) are never crossed autonomously.

**Judgment is accountable.** Every repertoire pass the skill chose not to run gets a one-line reason in the final report. That record is what lets the user audit the run's judgment without having supervised it.

**The project branch is the single integration point.** All work lands there; the user makes one decision at the end: merge or don't.

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────┐
│                  IMPLEMENT-PROJECT WORKFLOW                  │
├──────────────────────────────────────────────────────────────┤
│  1. Startup                                                  │
│     ├─ 1a. Branch, working tree, resume check                │
│     ├─ 1b. Elicit commander's intent (six fields)            │
│     ├─ 1c. Agree the smoke-testing procedure                 │
│     └─ 1d. Plan, present, seed PROJECT_STATE.md              │
│  2. Work loop (judgment; repeat until done or andon cord)    │
│     ├─ Decide — the next action that best serves intent      │
│     ├─ Act — invoke the skill, verify, commit                │
│     └─ Record — state doc: action, rationale, outcome        │
│  3. Termination (fixed floor)                                │
│     ├─ 3a. Smoke test + mechanical end-state checks          │
│     ├─ 3b. /review-release                                   │
│     └─ 3c. Final report                                      │
└──────────────────────────────────────────────────────────────┘
```

## 1. Startup

### 1a. Branch, working tree, resume check

Follow the shared startup protocol in [`references/lead-startup.md`](../../references/lead-startup.md) with these values:

- **Branch pattern:** `feat/project-<descriptive-name>`, from the operator or derived from the purpose.
- **State doc:** `PROJECT_STATE.md`.
- **"Resume as-is":** re-observe the project state (tests, branch, open tickets) before the next decision.

### 1b. Elicit commander's intent

Six fields, per [`references/autonomy.md`](../../references/autonomy.md) § "Commander's-intent schemas per skill":

| Field        | Ticket-driven run (the common case)                                                | Open-ended run                                                                  |
|--------------|------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| Purpose      | One line, derived from the tickets; operator confirms                              | Elicited — why this iteration exists                                            |
| Key tasks    | The tickets, fetched per [`references/trackers.md`](../../references/trackers.md)  | Elicited as observable state (2–10 items); the skill scopes tickets for them    |
| End state    | Default: every ticket's acceptance criteria met; tests, linters, smoke test pass   | Elicited — what command proves it is done?                                      |
| Constraints  | Default: none                                                                      | Elicited                                                                        |
| Non-goals    | Default: none                                                                      | Elicited                                                                        |
| Stakes       | Always asked: *what happens if this breaks?* and *who maintains it, for how long?* | Same                                                                            |

In a ticket-driven run, pre-fill everything the tickets imply and ask only for what they can't supply: confirmation, stakes, and any constraints or non-goals. Don't make the operator walk six fields to restate their tickets. In an open-ended run, walk the fields one at a time and push back on vague answers ("works well" → "what command would I run to verify?").

Classify each end-state condition as **mechanical** (a check the skill can run) or **subjective** (needs human judgment). Mechanical conditions gate termination; subjective ones go to the report for sign-off.

If batching is unclear for a ticket set, ask — do not guess at grouping the operator chose deliberately.

### 1c. Agree the smoke-testing procedure

Ask what smoke testing should prove the project works, with examples by project type if needed: a CLI run with representative commands, JSON-RPC calls to an MCP server, Playwright against a web app, an end-to-end exercise of a library's public API. Record it verbatim. It is fixed-floor item 2, and the probe set for any `/refactor` run.

### 1d. Plan, present, seed the state doc

Sketch an initial plan: batch order and dependencies for ticketed work, the scoping needed for open-ended key tasks, and which repertoire passes the project looks likely to need. The plan is a starting hypothesis, not a contract — the loop revises it.

**Present intent, smoke procedure, and plan together, and wait for approval.** This is the run's one planned interaction. Then seed `PROJECT_STATE.md` (gitignored) per the startup protocol: the pinned intent verbatim, the plan, and an empty action log.

## 2. Work Loop

Repeat: decide the next action, take it, verify, record. Stop when the termination conditions hold (section 3) or the andon cord is pulled.

### Deciding

Priorities, in order:

1. **Blockers.** Broken tests, build, or lint on the project branch.
2. **Key tasks.** Unfinished tickets and key-task outcomes before anything else.
3. **High-severity findings** from any review already run.
4. **Quality passes** the project needs, once the key tasks are done.

Re-read the pinned intent before each decision. Work that does not trace to it — scope creep, non-goals, polish on code the project didn't touch — is drift; course-correct, or pull the cord if the right path is unclear. When a choice is genuinely close, `/think-deliberate` it; when the framing seems wrong, `/think-reframe`.

### The repertoire

**Orientation:**
- `/review-health` — at the start of an open-ended run on an unfamiliar codebase.

**Implementation:**
- `/implement-batch` — a batch of tickets (overrides below). The usual workhorse.
- `/implement` — a single ticket, or a fix too small to batch.
- `/scope` — draft a ticket for a gap that serves intent; `/scope-project` for a whole open-ended key task.
- `/bug-fix` — a bug that resists a direct fix.

**Quality (each chosen by judgment, each accounted for in the report):**
- `/refactor` — shrinks the machine with behavior pinned. Best once the key tasks are done and before the reviews, so they examine the reduced design. Menu answered from intent (below).
- `/review-arch` — structural recommendations as a ticket proposal.
- `/review-test` — test-suite gaps as a ticket proposal.
- `/review-dead`, `/review-security`, `/review-perf`, `/review-a11y` — when the project's changes touch their territory.
- `/review-code` — adversarial correctness review of the project diff before declaring done.
- `/bug-hunt` — when the project added substantial untested surface.
- `/tidy-docs` — documentation for what actually shipped.

**Only when intent asks:** `/review-value` — its trade menu is product decisions, so the run surfaces the menu rather than acting on it.

**Never autonomously:** `/release` (publishing is andon territory); `/review-namespace` search mode (needs operator calibration).

### Acting

Invoke the chosen skill with autonomous overrides where it supports them; where it asks for interactive input, answer from the pinned intent. After it completes: tests, linters, and build still pass (fixed-floor item 1 — fix before continuing); its work is committed; the action, a one-sentence rationale, and the outcome are in the state doc.

**Severity handling for findings.** Critical/High: address before termination. Medium: address if bounded and local, else defer with a note. Low/Info: defer with a note. For review skills that propose tickets (`/review-arch`, `/review-test`, `/review-dead`, `/bug-hunt`), apply [`references/autonomy.md`](../../references/autonomy.md)'s orchestrator judgment: approve items worth tracking, decline items you will handle inline — and then actually handle them — and prefer cutting a ticket when in doubt, since a decline commits the run to doing the work.

**Don't thrash.** Re-run a review only if files it flagged have changed since. If two reviews contradict each other on the same file, pull the cord rather than oscillate.

### `/implement-batch` overrides

| `/implement-batch` step            | Override                                                                         |
|------------------------------------|----------------------------------------------------------------------------------|
| **Step 1** (receive tickets)       | Pre-loaded with the batch's tickets.                                             |
| **Step 3** (batch planning)        | Approve the plan autonomously; pull the cord only if the tickets are incoherent. |
| **Step 4** (create project branch) | Skip — run on the project branch; its topic branches merge there.                |
| **Step 7** (final review)          | Review autonomously and log the summary to the state doc.                        |

Andon cords inside the batch cascade up to this skill.

### `/refactor` overrides — the menu answered from intent

`/refactor` has one operator checkpoint, its requirements menu. Answer it from intent; everything after the menu runs as `/refactor` defines it.

| `/refactor` step                | Override                                                                                                                                                                    |
|---------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Step 0** (isolate)            | Branch `refactor/<slug>` from the project branch's HEAD.                                                                                                                    |
| **Menu — stakes**               | The Stakes field, verbatim.                                                                                                                                                 |
| **Menu — probes**               | The smoke-testing procedure, verbatim, plus every ticket's acceptance criteria — the operator's contribution to the oracle corpus.                                           |
| **Menu — verdicts**             | **Ratified:** behavior the tickets or key tasks specify, plus Constraints. **Documented:** keep all. **Invented:** presumed dead. **Priced:** take no trades; report them. |
| **Non-goals**                   | `/refactor` works on the whole target and takes no exclusions. If Non-goals name code the run must not touch, don't run `/refactor`; say why in the report.               |
| **Merge** (the operator's call) | Merge `refactor/<slug>` into the project branch (`--no-ff`) once the oracle is green; re-run tests and the smoke procedure. Andon cord on conflict or failure.               |

The skill stands in for the operator at the menu and the merge, and nowhere else: it never rescues an invented requirement, takes a trade, or overrides a gate. Record the answered menu in the state doc. If the project has no user-visible boundary to build an oracle against, don't run `/refactor` — its safety rests entirely on that oracle — and say so in the report.

## 3. Termination

Termination is a judgment — the key tasks are done and the project needs nothing more from the repertoire — confirmed by the fixed floor.

### 3a. Smoke test and end-state checks

Run the smoke-testing procedure and every mechanical end-state condition, recording each command and its result. Confirm no constraint was violated (check protected paths against the branch diff). Any failure is a blocker: back to the loop.

### 3b. `/review-release`

Run last, after every code change. Auto-fix mechanical findings (debug artifacts, version mismatches, changelog gaps); `/think-deliberate` ambiguous ones; defer user-judgment items to the report; pull the cord for blocking failures. If its fixes touch code, re-run 3a.

### 3c. Final report

Ordered by what most needs the user's scrutiny. Every claim of completion carries both a one-sentence narrative and an artifact — commit SHA, command and result, file:line, or ticket ID. A narrative without an artifact is not evidence.

```
## Project Complete

### Outcome
[One paragraph: was intent met? Name any failed mechanical condition
 or subjective condition awaiting sign-off.]

### Top things to scrutinize
[3–5 items where the run's judgment is most likely wrong or the stakes
 highest: risky commits, downgraded or deferred findings, deliberated
 decisions, inline work done instead of a ticket. One line + artifact each.]

### Key tasks / tickets
- [✓] #12: <title> — <outcome> — SHA <short>
- [~] #18: <title> — partial; see Deferred

### End state
- Mechanical: [✓] <condition> — `<command>` → <result> at SHA <short>
- Subjective (your sign-off): [?] <condition> — <what was done>
- Smoke test: <result>

### Quality passes
- Run: /refactor — concepts C0 → Cn, lines L0 → Ln, merged at <sha>
- Run: /review-arch — 2 tickets cut (#48, #49), 1 handled inline (<sha>)
- Not run: /review-test — <one-line reason>
- Not run: /review-security — <one-line reason>
- /review-release — N resolved, N deferred

### Deferred items
[Severity, source, description, reason, where tracked. Includes
 /refactor's trade menu and side memo, verbatim.]

### Branch
- feat/project-<name> @ <sha>, base <main> @ <sha>; N commits, +X/-Y
- Tickets created / closed: <IDs>
```

The user decides: merge, iterate, or discard.

## Andon Cord

Use the shared handoff template in [`references/autonomy.md`](../../references/autonomy.md): pre-loaded options, a recommendation, the tradeoff that would flip it, a pre-rebutted counterargument. Add the current state: what is merged, what is in flight, which key tasks remain. Title: `## Andon Cord — /implement-project — <current action>`.

Before pulling it, try to resolve autonomously; for judgment calls, `/think-deliberate` first; re-read intent — an apparent blocker may mean intent needs clarifying.

**Pull it when:**
- **An irreversible action is required:** pushing or merging to main/master, a public release or tag, force-push, global dependency installs, deleting data or untracked work, a breaking change the operator has not authorized.
- **A blocking decision needs product judgment** that deliberation cannot resolve from the repo.
- **Stuck:** the same failure three times across different strategies.
- **Reviews contradict each other** on the same file.
- **A merge conflicts**, or a merge breaks tests and the cause isn't local.
- **A key task appears to require violating a constraint.**
- **Resume finds HEAD diverged** from the state doc's record.
- **The run is drifting** and the right path is unclear.
- **A sub-skill's andon cord cascades up** for a reason this skill can't resolve.

## State Management

`PROJECT_STATE.md` at the repo root, gitignored, per the startup protocol's top-matter, plus:

```markdown
## Plan
[Current hypothesis: batches, scoping, likely passes — revised as the run learns]

## Action log
### <n> — <timestamp> — HEAD <short SHA>
- Action: /implement-batch (batch 2: #18, #20)
- Why: next key tasks; batch 1 merged clean
- Outcome: merged; tests green; 1 medium finding deferred

## Quality passes
- /refactor: run at action 6 — merged <sha>; menu: <answers>
- /review-security: not run — <reason>

## Deferred items
## Open questions
```

Update it after every action. It is the run's memory across context compaction and resumption; keep entries short.

## Hard Caps

- **50 actions** without terminating → pull the cord.
- **3 consecutive failed attempts** at the same goal → pull the cord.

## Coordination

One action at a time; each sub-skill completes before the next begins. The skill is a thin coordinator: it delegates implementation to sub-skills, keeps summary-level state in context, and keeps durable state in `PROJECT_STATE.md`.

## Relationship to Other Skills

**`/scope-project` → `/implement-project`** is the planning-to-execution pair: `/scope-project` drafts and adversarially reviews the batched tickets; this skill executes them.

**`/implement-batch`** is this skill's workhorse for ticketed work. It runs one batch with no judgment about what else the project needs; this skill supplies that judgment.

**`/refactor`** is normally operator-run; this is the one caller that runs it unattended, by answering its menu from intent.

```
/implement-project
├── (startup)  /review-health (open-ended run, unfamiliar codebase)
├── (loop, any of)
│   ├── /implement-batch → /implement (per ticket)
│   ├── /implement | /scope | /scope-project | /bug-fix
│   ├── /refactor (menu answered from intent)
│   ├── /review-arch | /review-test | /review-dead | /review-code
│   ├── /review-security | /review-perf | /review-a11y
│   ├── /bug-hunt | /tidy-docs
│   └── /think-deliberate | /think-reframe | /think-diagnose | /think-scrutinize
└── (termination)  smoke test → /review-release → report
```
