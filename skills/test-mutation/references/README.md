# /test-mutation - Mutation Testing Workflow

The step-by-step procedure lives in [`SKILL.md`](../SKILL.md); this guide covers when to use the skill and what to expect.

## Overview

`/test-mutation` checks whether your tests actually catch bugs. It introduces small deliberate changes (mutations) into source code one at a time, runs the suite after each, and reports which mutations survive. A survivor is a real coverage gap. A test that runs code without asserting on it scores 100% line coverage and 0% mutation score.

Each mutation costs a full test run, so the skill is **multi-session**: progress persists in `.test-mutations.json` and a codebase can be worked through over several sittings. After you pick the scope it runs **on autopilot**. For each module it mutates, writes tests for the survivors, confirms the new tests kill them, and commits.

## When to Use

**Use `/test-mutation` for:**
- Critical code (auth, payment, data processing) where test quality matters
- Finding blind spots after writing tests for a new feature
- An objective quality measure that's harder to game than line coverage
- Re-checking tests after a refactor, since a refactor can leave tests passing while they catch fewer bugs

**Don't use it for:**
- Projects with no tests yet. Write tests first.
- Prototypes, throwaway code, or simple one-off scripts

**Rule of thumb:** if a bug in this code would wake you up at night, mutation test it.

**vs. `/review-test`:** `/review-test` is advisory. It surveys coverage and test quality and proposes tickets. `/test-mutation` writes and commits tests. A good sequence: `/review-test` to surface gaps, `/implement` to work the tickets, then `/test-mutation` to find the weaknesses that remain.

## Flow

```
setup (interactive): load or create tracking file → detect test command
  → choose scope → require clean tree
autopilot, per module: mutate → write tests for survivors → verify kills → commit
summary
```

## What It Asks You

- **On first run:** whether to commit `.test-mutations.json` or gitignore it, and the test command if it can't detect one.
- **Every run:** the scope. Pick specific files, re-test completed ones, or press Enter for all pending modules (the default).

After that, no further interaction until the run finishes.

## What It Changes

- **Adds test files** and commits them, one commit per module. The tracking file is included in the commit unless you gitignored it.
- **Mutates source files temporarily** and reverts each mutation with `git restore`. That's why it **requires a clean tree** (no uncommitted changes to tracked files) before autopilot, since an uncommitted edit would be destroyed.
- **Never deletes your pre-existing untracked files.** When a module's new tests can't be made to pass, the skill removes only the files it added and moves on.
- **Stops the whole run** if the suite is already red at baseline, because every result would be meaningless, or if a file changes underneath it mid-run.

## Reading the Results

| Mutation Type      | Example                                 |
| ------------------ | --------------------------------------- |
| Arithmetic         | `amount + fee` → `amount - fee`         |
| Relational         | `count < max` → `count <= max`          |
| Logical            | `valid && active` → `valid \|\| active` |
| Constants          | `maxRetries = 3` → `maxRetries = 4`     |
| Statement deletion | Remove `audit.Log(event)`               |
| Control flow       | `if err != nil` → `if err == nil`       |

- **Killed:** tests failed, so they caught it.
- **Timeout:** the suite ran far past its baseline time. Counted as killed and reported separately.
- **Survived:** tests passed, so there's a gap.
- **Likely-equivalent:** a survivor no input can distinguish from the original, with a stated reason. No tests are written for these. They're listed for you to confirm by hand.

**Mutation score** = (killed + timeout) / (total − likely-equivalent).

| Score   | Meaning                                                 |
| ------- | ------------------------------------------------------- |
| 95-100% | Excellent — tests catch nearly all synthetic bugs       |
| 80-94%  | Good — some gaps, worth addressing for critical code    |
| 60-79%  | Adequate for non-critical code, weak for critical paths |
| < 60%   | Significant gaps — tests provide limited protection     |

A module marked `in_progress` was only partly covered (the mutator capped its site count). There's no mid-file resume, so re-testing it re-mutates the whole file.

## Example Session

```
> /test-mutation

Project: 3/10 modules tested (overall score: 85%)
Scope? Enter file names/numbers, or press Enter to test all pending.
> [Enter]

[1/7] src/api/handler.go — score: 92% → 98%, 3 tests added. Continuing...
[2/7] src/middleware.go — score: 100%, no survivors. Continuing...
...

## Mutation Testing Complete
| Module             | Before | After | Tests Added | Unresolved | Equivalent |
|--------------------|--------|-------|-------------|------------|------------|
| src/api/handler.go | —      | 98%   | 3           | 1          | 0          |
| ...                |        |       |             |            |            |

Unresolved survivors: 3 (listed in the summary)
```

## Tips

1. **Start with critical modules**, or press Enter and let it run through everything.
2. **Don't chase 100%.** Some survivors, such as constant tweaks or removed logging, aren't worth a test. The summary lists unresolved survivors so you can decide later.
3. **Commit the tracking file** to share scores and track improvement over time.
