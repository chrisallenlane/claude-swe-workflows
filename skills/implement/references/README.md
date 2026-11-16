# /implement — From Tickets to a Review-Ready Branch

## Overview

`/implement` builds whatever you hand it — one ticket, a batch of tickets, or a goal that still needs scoping — and gives you back a branch and a report. It covers what `/implement-batch` and `/implement-project` used to do; there is now one skill at every scale.

**Judgment over checklists.** The skill does not walk a fixed sequence of review steps. It holds a repertoire of agents and skills and uses the ones the work needs, when it needs them. A typo-sized fix gets a one-line concept inventory, a verification run, and a commit. A twelve-ticket feature may get planning, delegated implementation, `/refactor`, `/review-repo architecture`, and a smoke test.

**A small floor is fixed.** Five things hold on every run, at every scale:

| #   | Floor item                                    | What it means                                                                                                    |
|-----|-----------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| 1   | Concept inventory before code, audited        | Nothing is built that a requirement does not force; the diff is checked against the inventory                    |
| 2   | Practical verification of acceptance criteria | The feature is actually run before the tests are trusted                                                         |
| 3   | Tests and linters green                       | At every commit and every merge                                                                                  |
| 4   | Independent correctness review                | Unless the change is trivial — and always when the feature couldn't be run or there's no test suite              |
| 5   | No irreversible actions                       | No pushes, no commits or merges to main/master, no releases, no ticket closing, no unauthorized breaking changes |

**Judgment is accountable.** The final report lists every pass that ran and gives a one-line reason for every plausible pass that didn't. That's how you audit the run's judgment without supervising it.

**One interaction, then autonomy.** The skill confirms its understanding and plan with you once, scaled to the work, then runs to completion. It comes back early only to escalate.

## When to Use

**Use `/implement` for:**
- A single ticket or change you want built, verified, and reviewed
- A batch of related tickets, typically from `/scope`
- An open-ended goal ("make config handling work end to end") — the skill scopes it first
- Any work where you want the result on a branch with a report, not a running conversation

**Don't use `/implement` for:**
- Exploration or design without code — use `/scope`
- Throwaway prototypes where verification and review are overhead
- Redesigning an existing codebase — use `/refactor` directly

## Workflow

```
┌──────────────────────────────────────────────────────────────┐
│                     /implement WORKFLOW                      │
├──────────────────────────────────────────────────────────────┤
│  1. Understand and plan                                      │
│     ├─ Gather tickets (or clarify the request / scope goal)  │
│     ├─ Ask only what you alone can answer                    │
│     ├─ Present understanding + plan; wait for approval       │
│     └─ Branch (never main); PROJECT_STATE.md if multi-ticket │
│  2. Concept inventory — per ticket (floor)                   │
│  3. Build — swe-implementer or direct; plan first if unclear │
│  4. Verify (floor)                                           │
│     ├─ qa-engineer: practical verification, then tests       │
│     ├─ Tests and linters green                               │
│     └─ swe-correctness-reviewer: fresh, blocking, ≤3 rounds  │
│  5. Repertoire — whatever else the work needs (judgment)     │
│  6. Finish — commit "Fixes #N", final checks, report         │
│                                                              │
│  Escalation available throughout (§7)                        │
└──────────────────────────────────────────────────────────────┘
```

For multi-ticket work, steps 2–4 repeat per ticket, each on its own topic branch merged into the project branch once verified. Step 5's project-scale passes usually run after the tickets are done.

## Workflow Details

### 1. Understand and Plan

Tickets are fetched from your tracker: title, description, acceptance criteria, dependencies. A request with no ticket is clarified directly. A goal that needs decomposing is scoped first, with `/scope` or inline if its shape is obvious.

The skill asks only what you alone can answer:
- Ambiguous requirements, missing acceptance criteria, or several valid approaches with real trade-offs
- For multi-ticket work: constraints and non-goals, if the tickets don't state them, and the grouping, if you chose one deliberately
- If `/refactor` is likely to run: its two stakes questions — *what happens if this breaks?* and *who maintains it, for how long?*
- If the work spans user-visible features: a smoke-testing procedure

Then it presents its understanding and plan together and waits. For one ticket that's a few lines. For a project it's the ticket order with dependencies, the probable passes, constraints, non-goals, stakes, and smoke procedure. You can pre-approve ("just do it"). The approved intent anchors every later decision.

**Branching:** never commits to main/master; creates a working branch if needed. Multi-ticket work gets a project branch (`feat/project-<name>`) with one topic branch per ticket, merged back with `--no-ff` once verified — one revert unit per ticket.

**State:** multi-ticket runs keep `PROJECT_STATE.md` at the repo root (gitignored): the approved intent, the plan, and a one-line-per-action log. It survives context compaction; on resume the skill re-reads it and re-observes the branch before deciding anything.

### 2. Concept Inventory (Floor)

Before any ticket is planned or built, the skill writes down every concept it will introduce — each type, module, mechanism, layer, configuration knob, or abstraction — and holds it to four rules:

| Rule                                | In practice                                                                                                                 |
|-------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| Every concept cites its requirement | A concept no requirement or acceptance criterion forces is not built. "Might need it later" is a question for you, not code |
| The naive baseline is the default   | A plain array, a direct call, a hard-coded value — unless a named requirement rules the simple form out                     |
| Shop before you build               | The codebase, stdlib, and existing dependencies are searched first; a second queue or config reader needs a cited reason    |
| No caller, no export                | A public symbol names its caller outside the module, or it stays private or unwritten                                       |

The inventory scales with the change — a small fix may record "no new concepts" — but it always runs. It binds the build: the implementation agent builds what it lists and nothing else, and a concept discovered mid-build is added with its forcing requirement *before* it is built.

**The audit:** whenever the inventory lists a new concept or export, `swe-code-reviewer` checks the diff against it — uninventoried concepts, forms more elaborate than recorded, duplicated mechanisms, exports with no outside caller. Departures must be removed or admitted by amending the inventory. They are not advisory.

**Why:** it is cheaper not to write bloat than to strip it later, and nothing downstream hunts for working code that never needed to exist.

### 3. Build

The build goes to `swe-implementer`, a single language-agnostic agent, or is done directly when the change is too small to be worth a handoff. The implementer's value is not language expertise, which the model already has. Its value is discipline against the ways implementation agents fail: it checks APIs against the installed toolchain version rather than recalling them, follows the project's conventions instead of imposing defaults, builds only the inventoried concepts, and reports nothing as done that it hasn't run.

The agent receives the ticket, the inventory, and any plan. When the work is unclear — cross-cutting concerns, migrations, many modules, several viable approaches — the skill plans it first: an ordered sequence of independently verifiable sub-tasks over the inventoried concepts, risky or uncertain parts first, hard-to-reverse steps last. Uncertain approaches are prototyped in a scratch directory. Failures in practical verification go back to the implementer; `qa-engineer` reports, it never fixes.

### 4. Verify (Floor)

**Practical verification first.** `qa-engineer` gets the acceptance criteria and exercises the feature for real — runs the CLI, calls the API, speaks JSON-RPC to the MCP server, drives the page in a browser, uses the library — and only then writes tests. Failure returns to Build; three failed attempts on the same ticket escalate.

```
❌ Write code → write passing tests → ship broken code
✅ Write code → actually run it → then write tests
```

**Tests and linters green** after every change set and before every commit and merge.

**Correctness review.** A fresh `swe-correctness-reviewer` gets the diff and the target runtime/versions — never the implementation history or rationale. It assumes a bug already shipped and works backward, verifying every assumption the diff makes against the repo.

| Situation                                            | Correctness review                  |
|------------------------------------------------------|-------------------------------------|
| Typo, comment-only, obviously-correct one-liner      | May be skipped                      |
| Anything else                                        | Runs (when in doubt, it runs)       |
| Feature couldn't be run, or no meaningful test suite | Mandatory — it's the only gate left |

Findings are blocking: each is fixed or refuted with evidence, tests re-run, and a *fresh* reviewer re-reviews. Up to three rounds, then escalation. Non-blocking residual risks go to the report. In multi-ticket work it runs per ticket before that ticket merges; a final review of the whole project diff is a repertoire choice.

### 5. The Repertoire

Everything here is chosen by judgment. Anything that plausibly applied but didn't run gets a one-line reason in the report.

**Reviews of the change:**

| Pass                            | When                                           | Notes                                                        |
|---------------------------------|------------------------------------------------|--------------------------------------------------------------|
| `sec-blue-teamer`               | Auth, crypto, input handling, trust boundaries | Critical/High findings fixed or explicitly waived by you     |
| `swe-perf-reviewer`             | Hot paths, queries, loops at scale             |                                                              |
| Fresh `swe-implementer` review  | Non-trivial diffs                              | "Would I accept this PR?" nits only; reverted if tests break |
| `doc-maintainer` / `/tidy-docs` | Documentation affected                         | Targeted for one ticket; full pass for a project             |

**Skills, mostly at project scale:**

| Pass                                                                                                                      | When                                                               |
|---------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------|
| `/refactor`                                                                                                               | After the tickets, before other reviews; menu answered from intent |
| `/review-repo architecture`, `/review-test`, `/review-repo dead-code`, `/review-security`, `/review-perf`, `/review-a11y` | The work touched their territory                                   |
| `/bug-hunt`                                                                                                               | Substantial new surface with thin coverage                         |
| `/bug-fix`                                                                                                                | A failure that resists a direct fix                                |
| Smoke-testing procedure                                                                                                   | Before declaring multi-ticket work done                            |
| `/review-release`                                                                                                         | Last, when the work is headed for a release                        |
| `/think-*` (deliberate, reframe, diagnose, scrutinize)                                                                    | Close calls, wrong framings, unclear failures, risky plans         |

Review skills that propose tickets are handled with orchestrator judgment: approve what should be tracked, decline what the run will handle inline (and then handle it), and prefer a ticket when in doubt.

`/review-repo value` runs only when your intent asks for it, and its trade menu is surfaced to you rather than acted on. `/release` is never run.

**Severity handling:** Critical/High resolved before finishing; Medium resolved if bounded and local, else deferred with a note; Low/Info deferred with a note.

**No thrashing:** a review re-runs only if files it flagged have changed. Two reviews contradicting each other on the same code is an escalation, not a loop.

#### Running `/refactor` unattended

`/refactor` normally stops once, for you, at its requirements menu. Here the skill answers the menu from your approved intent, and everything after it runs as `/refactor` defines:

| Menu part | Answered with                                                                                                                                  |
|-----------|------------------------------------------------------------------------------------------------------------------------------------------------|
| Stakes    | Your answers, verbatim                                                                                                                         |
| Probes    | The smoke-testing procedure, plus every ticket's acceptance criteria                                                                           |
| Verdicts  | Ratified: behavior the tickets specify, plus constraints. Documented: keep all. Invented: presumed dead. Priced: no trades taken; all reported |
| Non-goals | `/refactor` takes no exclusions — if non-goals name code that must not be touched, it doesn't run                                              |
| Merge     | `refactor/<slug>` merged (`--no-ff`) once its oracle is green; tests and smoke procedure re-run                                                |

The skill stands in for you at the menu and the merge, and nowhere else: it never rescues an invented requirement, takes a trade, or overrides a gate. With no user-visible boundary to build an oracle against, `/refactor` doesn't run.

### 6. Finish

Each ticket's work is committed with a message referencing it (`Fixes #123`), so your tracker closes the ticket when *you* merge. The skill never closes or comments on tickets itself.

Final checks: full suite, linters, formatters; `git status` clean or every leftover explained; for multi-ticket work, the smoke procedure.

The report is ordered by what most needs your scrutiny, and every completion claim carries an artifact (SHA, command and result, file:line):

- **Outcome** — done or not; anything awaiting your judgment
- **Look at these first** — 1–5 items where judgment was most likely wrong or stakes highest
- **Tickets** — each with outcome and SHA
- **Verification** — acceptance, tests/linters, correctness review rounds and residual risks, smoke test
- **Passes** — run, and not run with reasons
- **Concept inventory, as built** — per ticket, including amendments
- **Deferred** — findings not addressed; `/refactor`'s trade menu and side memo
- **Branch** — name, SHAs, commit count

If the branch is behind main, the report says so and offers a rebase; it doesn't rebase unasked.

### 7. Escalation

The skill tries to resolve problems itself first — `/think-deliberate` for judgment calls, and a re-read of your intent in case a blocker means the intent needs clarifying. When you're present, it asks plainly. When unattended, it stops and hands off: what went wrong, what was tried, 2–3 named options, a recommendation and the trade-off that would flip it, and the branch state.

It escalates when:
- An irreversible action is required
- A decision needs product judgment the repo can't answer
- The same failure recurs 3 times across strategies, or the correctness review exhausts 3 rounds
- Two reviews contradict each other on the same code
- A merge conflicts, or breaks tests for reasons that aren't local
- A requirement appears to violate a constraint
- On resume, HEAD no longer matches `PROJECT_STATE.md`
- The work drifts from your intent and the right path is unclear
- A multi-ticket run's action log reaches 50 entries without finishing

### Invoked by Another Skill

When another skill supplies the tickets and constraints, the planned interaction is skipped — the caller's intent is the approved intent. The floor applies unchanged — a caller cannot waive it or authorize an irreversible action on your behalf — and escalations go to the caller.

## Examples

### Example 1: One-ticket fix

```
You: /implement #212 (pagination returns one item too few on the last page)

1. Plan: "Off-by-one in paginate() bounds; fix the slice end, add a
   boundary test. On branch fix/212-pagination." You: just do it.
2. Inventory: no new concepts.
3. Build: swe-implementer fixes the slice bound, adds a table test.
4. Verify: qa-engineer runs the CLI against a 21-item fixture with
   page size 10 — page 3 now shows 1 item. go test ./... and
   golangci-lint green. Correctness review runs (boundary logic is
   where off-by-ones hide): checks all 4 call sites, approves round 1.
5. Repertoire: none run.
6. Commit "Fix last-page off-by-one in paginate — Fixes #212".

Report — Passes not run:
- sec-blue-teamer: no trust boundary touched
- Implementer peer review: 3-line diff
- /refactor, /review-*: single-ticket fix, no new surface
- doc-maintainer: no documented behavior changed
```

### Example 2: Three-ticket batch

```
You: /implement #301 #302 #303 (export command: CSV, JSON, --fields flag)

1. Plan: order #301 → #302 → #303 (#303 depends on both formatters);
   project branch feat/project-export; constraint: no new dependencies.
   Approved.
2–4. Per ticket, on its own topic branch:
   #301 inventory: one formatter interface (forced by two formats in
        #301/#302); shopped encoding/csv. Built, verified, correctness
        review approves round 1; merged --no-ff.
   #302 inventory: reuses the formatter interface; encoding/json.
        Correctness review round 1 finds unescaped field names;
        fixed, fresh reviewer approves round 2; merged.
   #303 inventory: field selection; audit flags an exported
        ParseFields with no outside caller — made private. Merged.
5. Repertoire: implementer peer review on #301 (largest diff); doc-maintainer
   updates the README's export section.
6. Three commits with Fixes #301/#302/#303.

Report — Passes not run:
- /refactor: ~180 new lines in a small, fresh module; nothing to shrink yet
- /review-repo architecture: no module boundaries changed
- sec-blue-teamer: output only, no new input handling beyond flags
```

### Example 3: Larger project, `/refactor` unattended

```
You: /implement milestone v2.0 (11 tickets, sync engine rewrite)

1. Plan: three dependency groups; probable passes /refactor,
   /review-repo architecture, /review-test, smoke test. Stakes asked:
   "Breaks: users lose unsynced edits. Maintained by me, for years."
   Smoke procedure: run `sync --dry-run` against the fixtures repo,
   diff against golden output. Approved.
2–4. Eleven tickets, each inventoried, verified, correctness-reviewed,
   merged to feat/project-v2-sync. PROJECT_STATE.md tracks progress.
5. /refactor, menu answered from intent: probes = smoke procedure +
   all acceptance criteria; documented requirements kept; no trades
   taken. 3 iterations; concepts 52 → 41, code lines 7,900 → 6,300;
   oracle green; merged --no-ff; tests and smoke re-run, pass.
   /review-repo architecture on the reduced design: proposes 3 items — 2 tickets
   cut (#340, #341), 1 handled inline (conflict-resolver split, SHA a1b2c3d).
   /review-test: coverage gap in retry paths — filled inline.
   Smoke test passes.

Report — Deferred: /refactor offered 1 trade (drop legacy v1 lockfile
reading, frees ~400 lines) — not taken; your call.
```

### Example 4: Escalation

```
[During #18 of a project run]
Correctness review, round 3: the reviewer still holds that migration
0042 drops a column existing clients read. The implementer refutes — but
the refutation rests on an assumption about client versions the
repo can't confirm.

Escalation — /implement — #18 (schema migration)
What went wrong: 3 review rounds, contested finding unresolved.
Tried: two migration variants; /think-deliberate (inconclusive
without client-version data).
Options:
  A. Keep the column, mark deprecated (non-breaking) — recommended
  B. Drop it now (breaking — needs your authorization)
  C. Pause #18, continue the rest
Flips the recommendation: if you know no client older than 2.3 exists.
Branch: #12–#17 merged to feat/project-accounts; #18 on its topic
branch, unmerged.
```

## Tips

1. **Give it tickets with acceptance criteria.** They drive practical verification and the correctness review, and become `/refactor`'s probes.
2. **Say "just do it" when you mean it.** For small, clear tickets, pre-approval skips the plan review.
3. **Read "Look at these first" and "Not run" before the rest.** They're where the run's judgment is most likely to be wrong.
4. **Answer the stakes questions honestly.** They calibrate how hard an unattended `/refactor` cuts.
5. **Name non-goals for big runs.** They're the cheapest guard against drift — and naming code that must not be touched keeps `/refactor` from running.
6. **Merging is yours.** Tickets close when you merge, via `Fixes #N`; nothing reaches main without you.
