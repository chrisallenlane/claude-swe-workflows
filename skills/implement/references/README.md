# /implement — From Tickets to a Review-Ready Branch

The step-by-step procedure lives in [`SKILL.md`](../SKILL.md); this guide covers when to use the skill and what to expect.

## Overview

`/implement` builds whatever you hand it — one ticket, a batch of tickets, or a goal that still needs scoping — and gives you back a branch and a report.

**Judgment over checklists.** The skill does not walk a fixed sequence of review steps. It holds a repertoire of agents and skills — planning, security and performance reviews, peer review, docs, `/refactor`, `/review-*`, `/bug-hunt`, `/bug-fix`, `/think-*` — and uses the ones the work needs, when it needs them. A typo-sized fix gets a one-line concept inventory, a verification run, and a commit. A twelve-ticket feature may get planning, delegated implementation, `/refactor`, `/review-repo architecture`, and a smoke test.

**A small floor is fixed.** Five things hold on every run, at every scale, because they are cheap and they carry the correctness:

| #   | Floor item                                    | What it means                                                                                                    |
|-----|-----------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| 1   | Concept inventory before code, audited        | Nothing is built that a requirement does not force; the diff is checked against the inventory                    |
| 2   | Practical verification of acceptance criteria | The feature is actually run before the tests are trusted                                                         |
| 3   | Tests and linters green                       | At every commit and every merge                                                                                  |
| 4   | Independent correctness review                | Unless the change is trivial — and always when the feature couldn't be run or there's no test suite              |
| 5   | No irreversible actions                       | No pushes, no commits or merges to main/master, no releases, no ticket closing, no unauthorized breaking changes |

**Why a concept inventory?** It is cheaper not to write bloat than to strip it later, and nothing downstream hunts for working code that never needed to exist. Every concept must cite the requirement that forces it, start from the naive form, reuse an existing mechanism where one exists, and have a real outside caller if exported.

**Why practical verification first?** Passing tests for broken code is the classic failure: write code → write passing tests → ship broken code. The feature is actually run — the CLI, the API, the MCP server, the page in a browser — before tests are trusted.

**Judgment is accountable.** The final report lists every pass that ran and gives a one-line reason for every plausible pass that didn't. That's how you audit the run's judgment without supervising it.

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
- A bug that needs diagnosis before fixing — use `/bug-fix` (`/implement` may invoke it when a failure resists a direct fix)

## The Flow

```
Understand and plan ──→ ┌─ per ticket ────────────────────────────┐
(the one interaction)   │ Concept inventory → Build → Verify      │
                        └─────────────────────────────────────────┘
                                         │
                                         ▼
                        Repertoire (judgment) → Finish and report

                        Escalation available throughout
```

## What You'll Be Asked

**One interaction, then autonomy.** The skill asks only what you alone can answer — ambiguous requirements, missing acceptance criteria, real trade-offs between approaches; for multi-ticket work, constraints and non-goals; if `/refactor` is likely, its two stakes questions (*what happens if this breaks?* and *who maintains it, for how long?*); and for user-visible features, a smoke-testing procedure. Then it presents its understanding and plan together and waits. You can pre-approve ("just do it"). The approved intent anchors every later decision.

After that it comes back only to **escalate**: an irreversible action is needed, a decision needs product judgment, attempts or review rounds are exhausted, reviews contradict each other, a merge breaks, or the work drifts from intent. When unattended, it stops all work and hands off with the branch state.

## What You Get Back

- **A branch, never main.** Multi-ticket work gets a project branch (`feat/project-<name>`) with each ticket merged in (`--no-ff`) as one revert unit, plus a gitignored `PROJECT_STATE.md` so a long run survives compaction and can resume.
- **Commits that reference tickets** (`Fixes #123`), so your tracker closes them when *you* merge. The skill never closes or comments on tickets itself.
- **A report ordered by what most needs your scrutiny**, every completion claim backed by an artifact (SHA, command and result, file:line): outcome, "look at these first," tickets, verification, passes run and not run (with reasons), the concept inventory as built, deferred findings (including `/refactor`'s trade menu and side memo), and the branch.
- **No rebase unasked.** If the branch is behind main, the report says so and offers.

**Running `/refactor` unattended:** the skill answers `/refactor`'s requirements menu from your approved intent — your stakes verbatim, the smoke procedure and acceptance criteria as probes, documented requirements kept, no trades taken (they're reported). It stands in for you at the menu and the merge, and nowhere else. If your non-goals name code that must not be touched, or there's no user-visible boundary for an oracle, `/refactor` doesn't run.

**Invoked by another skill:** the caller's intent is the approved intent and the planned interaction is skipped. The floor applies unchanged — a caller cannot waive it or authorize an irreversible action on your behalf — and escalations go to the caller.

## Examples

### Example 1: One-ticket fix

```
You: /implement #212 (pagination returns one item too few on the last page)

Plan: "Off-by-one in paginate() bounds; fix the slice end, add a
  boundary test. On branch fix/212-pagination." You: just do it.
Inventory: no new concepts.
Verify: qa-engineer runs the CLI against a 21-item fixture with page
  size 10 — page 3 now shows 1 item. Tests and lint green. Correctness
  review checks all 4 call sites, approves round 1.
Commit "Fix last-page off-by-one in paginate — Fixes #212".

Report — Passes not run:
- sec-blue-teamer: no trust boundary touched
- Implementer peer review: 3-line diff
- /refactor, /review-*: single-ticket fix, no new surface
- doc-maintainer: no documented behavior changed
```

### Example 2: Three-ticket batch

```
You: /implement #301 #302 #303 (export command: CSV, JSON, --fields flag)

Plan: order #301 → #302 → #303 (#303 depends on both formatters);
  project branch feat/project-export; constraint: no new dependencies.
Per ticket, on its own topic branch:
  #301 inventory: one formatter interface (forced by two formats);
       shopped encoding/csv. Verified, reviewed, merged --no-ff.
  #302 correctness review round 1 finds unescaped field names;
       fixed, fresh reviewer approves round 2; merged.
  #303 audit flags an exported ParseFields with no outside caller —
       made private. Merged.
Repertoire: peer review on #301 (largest diff); doc-maintainer
  updates the README's export section.

Report — Passes not run:
- /refactor: ~180 new lines in a small, fresh module; nothing to shrink yet
- /review-repo architecture: no module boundaries changed
- sec-blue-teamer: output only, no new input handling beyond flags
```

### Example 3: Larger project, `/refactor` unattended

```
You: /implement milestone v2.0 (11 tickets, sync engine rewrite)

Plan: three dependency groups; probable passes /refactor,
  /review-repo architecture, /review-test, smoke test. Stakes asked:
  "Breaks: users lose unsynced edits. Maintained by me, for years."
  Smoke procedure: `sync --dry-run` against the fixtures repo, diffed
  against golden output. Approved.
Eleven tickets, each inventoried, verified, correctness-reviewed, merged.
/refactor, menu answered from intent: 3 iterations; concepts 52 → 41,
  code lines 7,900 → 6,300; oracle green; merged; smoke re-run, passes.
/review-repo architecture: 2 tickets cut, 1 item handled inline.

Report — Deferred: /refactor offered 1 trade (drop legacy v1 lockfile
reading, frees ~400 lines) — not taken; your call.
```

### Example 4: Escalation

```
[During #18 of a project run]
Correctness review, round 3: the reviewer still holds that migration
0042 drops a column existing clients read. The implementer's refutation
rests on an assumption about client versions the repo can't confirm.

Escalation — /implement — #18 (schema migration)
What went wrong: 3 review rounds, contested finding unresolved.
Tried: two migration variants; /think-deliberate (inconclusive).
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
