---
name: implement
description: Implements a ticket, a batch, or an open-ended goal end to end, choosing agents and reviews by judgment over a fixed floor (concept inventory, practical verification, green tests, correctness review). Autonomous after one planning interaction.
model: opus
---

# Implement — From Tickets to a Review-Ready Branch

Implements whatever it is given — one ticket, a batch of tickets, or a goal that still needs scoping — and hands back a branch and a report. The skill decides how much process the work needs. A typo-sized fix gets a concept inventory of "no new concepts," a verification run, and a commit; a twelve-ticket feature may get planning, delegated implementation, `/refactor`, `/review-repo architecture`, and a smoke test. The work decides, not a checklist.

## Philosophy

**Correctness is the goal; judgment chooses the tools.** The skill holds a repertoire of agents and skills (below) and uses the ones the work needs, when it needs them, the way a capable senior engineer would. Running a pass because a list says so wastes the run; skipping one the work needed is a judgment error the report must make visible.

**A small floor is fixed.** These hold on every run, at every scale, because they are cheap and they carry the correctness:

1. **Concept inventory before code, audited against the diff.** Nothing is built that a requirement does not force (§2).
2. **Practical verification of the acceptance criteria.** Actually run the feature before trusting the tests (§4).
3. **Tests and linters green** at every commit and every merge.
4. **An independent correctness review** of each ticket's diff, unless the change is trivial — and always when the feature could not be run or the project has no meaningful test suite (§4).
5. **No irreversible actions.** No pushes, no merges or commits to main/master, no releases, no ticket closing, no breaking changes the user has not authorized.

**Judgment is accountable.** The final report names every repertoire pass that ran and gives a one-line reason for each plausible pass that did not. That record is how the user audits the run's judgment without supervising it.

**One interaction, then autonomy.** The skill confirms its understanding and plan once, scaled to the work, and then runs to completion. It comes back early only through escalation (§7).

## 1. Understand and Plan

**Gather the work.** Tickets are fetched per [`references/trackers.md`](../../references/trackers.md): title, description, acceptance criteria, dependencies. A request with no ticket is clarified directly. A goal that needs decomposing ("make config handling work end to end") is scoped first — draft the tickets with `/scope`, or inline when the shape is obvious.

**Ask what only the user can answer**, and nothing else:
- Ambiguous requirements, missing acceptance criteria, or several valid approaches with real trade-offs.
- For multi-ticket work: constraints and non-goals, if the tickets don't state them; the grouping, if the user chose one deliberately.
- If `/refactor` is likely to run: its two stakes questions — *what happens if this breaks?* and *who maintains it, for how long?*
- If the work spans user-visible features: a smoke-testing procedure (a CLI run with representative commands, JSON-RPC calls to an MCP server, Playwright against a web app, an end-to-end use of a library's API).

**Present understanding and plan together, and wait for approval.** For one ticket this is a few lines; for a project it is the ticket order with dependencies, the probable passes, constraints, non-goals, stakes, and smoke procedure. The user may pre-approve ("just do it"), in which case proceed. Record the approved intent; it anchors every later decision.

**Branching.** Never commit to main/master; if on it, create a working branch first. For multi-ticket work, create a project branch (`feat/project-<name>`) and implement each ticket on a topic branch from it, merged back (`--no-ff`) once verified — one revert unit per ticket.

**State.** For multi-ticket work, keep `PROJECT_STATE.md` at the repo root (gitignored): the approved intent, the plan, and a one-line-per-action log (action, why, outcome, HEAD). It is the run's memory across compaction and resumption; on resume, re-read it and re-observe the branch before deciding anything.

## 2. Concept Inventory (Floor)

**Design before code.** It is cheaper not to write a mechanism than to strip it out later, and nothing downstream hunts for machinery that works but was never needed. The inventory is the gate that asks "does this need to exist?", so it runs for every ticket. It scales with the change — a one-line fix has a one-line inventory ("no new concepts") — but it is never skipped.

**Write it before planning or building each ticket.** Four rules bind it:

- **Every concept cites its requirement.** List each concept the change introduces — a type, module, mechanism, layer, configuration knob, or abstraction — in one sentence, and cite the requirement or acceptance criterion that forces it. A concept that cites nothing is not built. Future needs, symmetry, and completeness are not requirements; if one of them matters, it is a question for the user, not code.
- **The naive baseline is the default.** Each concept is implemented in the dumbest form that meets its cited requirement: a plain array, a direct call, a hard-coded value, a linear scan. Anything more elaborate names the requirement the naive form fails.
- **Shop before you build.** For each concept, search the codebase, the standard library, and the dependencies already present for a mechanism that solves the same problem, and record what was searched and what was found. An existing mechanism is reused or extended. Building a second one beside it — a second queue, clamp, config reader, retry loop — requires a cited reason the first cannot serve.
- **No caller, no export.** Every exported or public symbol names the caller outside its module that this change adds or already has. A symbol with no such caller is private, or is not written.

```
## Concept Inventory — <ticket>

### New concepts
- <concept, one sentence>
  - Forced by: <requirement or acceptance criterion>
  - Form: naive — <what> | elaborated — <what>, because <requirement the naive form fails>
  - Shopped: <what was searched> → <nothing found | reusing X | extending X | X cannot serve because ...>

### Exports
- <symbol> — called by <caller outside the module>

### Considered and omitted
- <concept> — <why no requirement forces it>
```

**The inventory binds the build.** The implementation agent builds the inventoried concepts and only those. A concept discovered mid-build is reported with its forcing requirement and added to the inventory before it is built — never built first and listed afterwards.

**The audit.** Whenever the inventory lists a new concept or export, spawn `swe-code-reviewer` with the inventory and the diff to report each departure: a concept built but not inventoried, a form more elaborate than recorded, a mechanism duplicating one already in the codebase, an export with no outside caller. Departures are resolved — removed, or admitted by amending the inventory with a forcing requirement. They are not advisory.

## 3. Build

**Delegate the build to `swe-implementer`** — or implement directly when the change is small enough that a handoff costs more than it saves. Pass it the ticket, the inventory, any plan, and the target runtime and versions when you know them.

**Plan when the work is unclear** — cross-cutting concerns, migrations, many modules, several viable approaches. Write the plan yourself before delegating: an ordered sequence of sub-tasks over the inventoried concepts (it adds none), each verifiable on its own, with risky or uncertain parts first and hard-to-reverse steps last. Prototype uncertain approaches in a scratch directory before building on them.

**Implementation responsibilities:** language idioms and project conventions; edge cases and errors; unit tests for pure logic as it is written.

## 4. Verify (Floor)

**Practical verification first.** Spawn `qa-engineer` with the ticket's acceptance criteria. It exercises the feature for real — runs the CLI, calls the API, speaks JSON-RPC to the MCP server, drives the page in a browser, uses the library — and only then writes tests. This prevents passing tests for broken code. It never fixes product code; a failure comes back to the implementer with its evidence. Verification it cannot perform from inside a subagent (invoking a Claude skill or agent) is returned to you to run. Failure returns to §3; after 3 failed attempts on the same ticket, escalate (§7).

**Tests and linters green.** Run the suite, linters, and formatters after every change set, and before every commit and merge.

**Correctness review.** Spawn a fresh `swe-correctness-reviewer` with the diff and the target runtime and versions — never the implementation history or rationale; its independence is the point. It assumes a bug already shipped and works backward, verifying every assumption the diff makes against the repo.

- **Run unless trivial:** skip only typo, comment-only, or single-line changes whose correctness is obvious by inspection. When in doubt, run it.
- **Mandatory** when practical verification was impossible or the project has no meaningful test suite — then it is the only correctness gate left.
- **Findings are blocking.** Each is fixed or refuted with cited evidence; re-run tests; spawn a *fresh* reviewer on the updated diff. Up to 3 rounds, then escalate with the surviving findings. Residual risks (non-blocking) go to the report.

For multi-ticket work, run it per ticket before its merge; a final review of the whole project diff is a repertoire choice.

## 5. The Repertoire

Use what the work needs. Each pass that plausibly applied and did not run gets a one-line reason in the report.

**Reviews of the change:**
- `sec-blue-teamer` with the diff (Mode: scoped review) — auth, crypto, input handling, trust boundaries. Critical/High findings must be fixed or explicitly waived by the user.
- `swe-perf-reviewer` with the diff (Mode: change review) — hot paths, queries, loops at scale.
- A fresh `swe-implementer` in peer-review mode — "would I accept this PR?" nits on non-trivial diffs; small fixes only, never re-architecture. If its edits break tests, revert them.
- `doc-maintainer` or `/tidy-docs` — documentation for what changed; targeted for one ticket, a full pass for a project.

**Skills, mostly at project scale:**
- `/refactor` — shrinks the machine with behavior pinned. Best after the tickets are done, before other reviews. Runs with its menu answered from intent (below).
- `/review-repo architecture`, `/review-test`, `/review-repo dead-code`, `/review-security`, `/review-perf`, `/review-a11y` — when the work touched their territory. Those that propose tickets (`/review-repo`, `/review-test`, `/review-security`): approve what should be tracked, decline what you will handle inline — then handle it — and prefer a ticket when in doubt.
- `/bug-hunt` — substantial new surface with thin coverage. Run `/bug-hunt` with its intent answered from approved intent: scope = the new surface; floor High; constraints from intent; tickets no; fix no.
- `/bug-fix` — a failure that resists a direct fix. Run it per its "Invoked by Another Skill" contract: you supply the bug report and answer its questions.
- The smoke-testing procedure — before declaring multi-ticket work done.
- `/review-release` — last, when the work is headed for a release.
- `/think-deliberate`, `/think-brainstorm` (framing check), `/think-diagnose`, `/think-scrutinize` — close calls, wrong-seeming framings, unclear failures, risky plans.

**Only when intent asks:** `/review-repo value` — its trade menu is product decisions, so surface it rather than act on it. **Never:** `/release`.

**Severity handling.** Critical/High: resolve before finishing. Medium: resolve if bounded and local, else defer with a note. Low/Info: defer with a note. **Don't thrash:** re-run a review only if files it flagged have changed; if two reviews contradict each other on the same code, escalate rather than oscillate.

### Running `/refactor` unattended

`/refactor` has one operator checkpoint, its requirements menu. Answer it from the approved intent; everything after the menu runs as `/refactor` defines it.

| Menu part | Answer                                                                                                                                                        |
|-----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Stakes    | The user's answers, verbatim.                                                                                                                                 |
| Probes    | The smoke-testing procedure, plus every ticket's acceptance criteria.                                                                                         |
| Verdicts  | **Ratified:** behavior the tickets specify, plus constraints. **Documented:** keep all. **Invented:** presumed dead. **Priced:** take no trades; report them. |
| Non-goals | `/refactor` takes no exclusions; if non-goals name code that must not be touched, don't run it.                                                               |
| Merge     | Merge `refactor/<slug>` into the working branch (`--no-ff`) once its oracle is green; re-run tests and the smoke procedure.                                   |

Stand in for the user at the menu and the merge, and nowhere else: never rescue an invented requirement, take a trade, or override a gate. If the project has no user-visible boundary to build an oracle against, don't run `/refactor`; its safety rests on that oracle.

## 6. Finish

**Commit** each ticket's work with a descriptive message referencing the ticket (`Fixes #123`), so the tracker closes it when the user merges. Do not close or comment on tickets directly.

**Final checks:** the full suite, linters, and formatters pass; `git status` is clean or every leftover is explained; for multi-ticket work, the smoke procedure passes.

**Report**, ordered by what most needs the user's scrutiny. Every completion claim carries an artifact — a commit SHA, a command and its result, a file:line.

```
## Implementation Complete

### Outcome
[One paragraph: done or not; anything awaiting the user's judgment.]

### Look at these first
[1–5 items where judgment was most likely wrong or stakes highest.]

### Tickets
- [✓] #12: <title> — <outcome> — SHA <short>

### Verification
- Acceptance: <what was run, what happened>
- Tests/linters: <command> → <result>
- Correctness review: <rounds; residual risks>
- Smoke test: <result, if run>

### Passes
- Run: <pass> — <result>
- Not run: <pass> — <one-line reason>

### Concept inventory, as built
[Per ticket, including amendments.]

### Deferred
[Findings not addressed, with reasons; /refactor's trade menu and side memo.]

### Branch
- <branch> @ <sha>, base <main> @ <sha>; N commits
```

If the branch is behind main, say so and offer to rebase; don't rebase unasked.

## 7. Escalation

Try to resolve problems first; for judgment calls, `/think-deliberate`; re-read the approved intent — an apparent blocker may mean the intent needs clarifying. When the user is present, ask plainly. When running unattended, stop all work and hand off per [`references/autonomy.md`](../../references/autonomy.md)'s andon-cord template, adding the branch state (what is merged, what is in flight) under Current state.

**Escalate when:**
- An irreversible action is required (floor item 5).
- A decision needs product judgment the repo cannot answer.
- 3 failed attempts on the same ticket, or the correctness review exhausts its 3 rounds.
- Two reviews contradict each other on the same code.
- A merge conflicts, or a merge breaks tests for reasons that aren't local.
- A requirement appears to violate a constraint.
- On resume, HEAD no longer matches `PROJECT_STATE.md`.
- The work is drifting from the approved intent and the right path is unclear.
- A multi-ticket run's action log reaches 50 entries without finishing.

## Invoked by Another Skill

When a calling skill supplies the tickets and constraints, skip the planned interaction: the caller's intent is the approved intent. Apply the floor unchanged — a caller cannot waive it, and cannot authorize an irreversible action on the user's behalf. Escalations go to the caller, which decides whether to escalate further.
