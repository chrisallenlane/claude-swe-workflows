# /bug-fix - Automated Bug-Fixing Workflow

The step-by-step procedure lives in [`SKILL.md`](../SKILL.md); this guide covers when to use the skill and what to expect.

## Overview

The `/bug-fix` skill orchestrates a diagnosis-first bug-fixing workflow through specialist agents. It reproduces the bug with a failing test, performs root-cause analysis with git archaeology, implements a targeted fix, and verifies the fix through practical testing — then runs it through review, correctness, and documentation gates.

**Why it is shaped this way:**
- **A failing test defines "done."** Writing the reproducing test before any fix turns "is it fixed?" into an empirical question.
- **Diagnosis before implementation** prevents surface-level patches: a read-only investigator finds the root cause (with git archaeology when the bug warrants it) so the fix is targeted, not a guess.
- **Related failure modes are tested too.** The same root cause often affects adjacent paths; those get tests, not just the reported bug.
- **Practical verification** confirms the originally-reported scenario actually works — running the CLI, calling the API, driving the page — not only that tests pass.
- **An unanchored correctness gate.** A fresh correctness reviewer sees the diff and your original bug report, but deliberately *not* the diagnosis. The diagnosis is the implementer's adopted theory; passing it would anchor the reviewer to the frame that produced the fix. The reviewer's question is "does this fix rest on false assumptions or break anything else?" The gate becomes mandatory when empirical verification degrades (no test suite, or the scenario can't be exercised).

## When to Use

**Use `/bug-fix` for:**
- Bugs that need investigation before fixing
- Issues where you want a failing test before any code changes
- Bugs that might have related failure modes (same root cause, similar patterns)
- Fixes where you want comprehensive regression testing
- Problems where git history might reveal how the bug was introduced

**Don't use `/bug-fix` for:**
- Obvious typos or trivial one-line fixes (just fix them directly)
- Feature requests disguised as bugs (use `/implement`)
- Exploratory debugging where the symptom is unclear (investigate first, then `/bug-fix`)
- Finding bugs you don't know about yet (use `/bug-hunt`)

**Rule of thumb:** If the bug is worth a failing test and root-cause analysis, use `/bug-fix`. If the fix is obvious, just do it.

## The Flow

```
Clarify → Reproduce (failing test) → Diagnose → Fix → Verify (practical)
        → Review → Correctness gate → Document → Final verification → Complete
```

## How /bug-fix Differs from /implement

`/implement` builds from requirements; `/bug-fix` starts from a symptom and spends its early phases on reproduction and diagnosis before any fix. Both end with the same kinds of gates: practical verification, a fresh blocking correctness review, and a documentation pass.

- **Test first, then fix.** `/implement` implements then tests. `/bug-fix` writes a failing test before any fix attempt.
- **Diagnosis before implementation.** The diagnostician performs root-cause analysis so the implementer makes a targeted fix.
- **Related failure modes.** The diagnostician identifies patterns, and the implementer writes tests for all of them.

## What You'll Be Asked

- **Up front:** symptoms, expected vs. actual behavior, reproduction steps, when it started, and environment. The skill keeps asking until it can write a reproducing test; if reproduction fails, it comes back with what it tried.
- **On escalation:** when reproduction, fix verification, or correctness review hits its attempt limit, you get the current state and the specific blocker.
- **At the end:** whether to complete the workflow — commit, update or close the ticket, and rebase on main if the branch is behind.

## What You Get Back

A summary of the bug, its root cause, files changed, tests added (the regression test plus one per related failure mode), any residual risks from the correctness review, and remaining follow-ups. Nothing is committed until you confirm completion, and a rebase is offered, never forced; conflicts halt rather than auto-resolve.

**Invoked by another skill** (such as `/implement`): the caller supplies the bug report and answers the questions and the completion confirmation in your place. The workflow runs through the commit, but never updates or closes tickets and never rebases. Escalations go to the caller.

## Examples

### Example 1: Off-by-One in Pagination
```
User: "The last item on each page is duplicated on the next page"

Clarify: Which endpoint? All page sizes? Started after recent changes?
Reproduce: TestPaginationBoundary asserts no duplicates — fails.
Diagnose: boundary comparison uses < instead of <=; git blame shows it
  arrived in commit abc123 during a refactor. Same pattern exists in
  the cursor-based pagination path.
Fix: both operators fixed; cursor-path boundary tests added.
Verify: qa-engineer actually paginates through test data — no dupes.
Correctness: reviewer checks all call sites of both paths — APPROVE.

Summary:
- Root cause: < vs <= in boundary check, introduced in refactor abc123
- Fixed: 2 files, both offset and cursor pagination
- Tests added: 4 (original bug + 3 related failure modes)
```

### Example 2: Race Condition in Cache
```
User: "Intermittent 500 errors under load, started after adding caching"

Reproduce: TestConcurrentCacheAccess fails under the race detector.
Diagnose: unsynchronized map access; cache added without a mutex.
  Related: the eviction path has the same issue.
Fix: sync.RWMutex protects read/write and eviction paths.

Summary:
- Root cause: Unsynchronized map access in cache layer
- Tests added: 3 (concurrent read/write, concurrent eviction, mixed load)
```

### Example 3: Can't Reproduce
```
User: "App crashes on startup"

Reproduce: tried default config, invalid configs, missing config —
  no crash. Reports what was tried; back to clarification.
User: "Only happens with YAML config, not TOML"
Reproduce (retry): TestYAMLConfigParsing fails. Bug reproduced;
  diagnosis and fix proceed.
```

## Tips

1. **Provide reproduction details.** The more specific your reproduction steps, the faster reproduction goes. Vague reports lead to reproduction failures.
2. **Trust the diagnostician's depth.** It chooses shallow or deep git archaeology based on the bug's complexity.
3. **The failing test is the contract.** Once it exists, that test defines "fixed."
4. **Related failure modes are valuable.** They often catch adjacent bugs that would have been reported next.
5. **Use `/implement` for feature-shaped bugs.** `/bug-fix` is for when existing behavior is wrong.
