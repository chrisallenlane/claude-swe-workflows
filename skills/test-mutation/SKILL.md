---
name: test-mutation
description: Mutation testing workflow. Systematically mutates source code to verify tests actually catch bugs. Multi-session with progress tracking.
model: opus
---

# Test Mutate - Mutation Testing Workflow

Systematically introduces small changes (mutations) to source code, runs the test suite after each, and reports which mutations survive (tests don't catch them). Surviving mutations reveal genuine test coverage gaps that line coverage misses.

## Philosophy

**Mutation score > line coverage.** A test that runs code without asserting on it scores 100% line coverage and 0% mutation score.

**Multi-session by design.** Each mutation costs a full test run, so progress is tracked in `.test-mutations.json` and a codebase can be worked through across sessions.

**Autopilot after setup.** Once scope is confirmed, the run is unattended: it addresses every survivor, commits per module, and stops only on an unrecoverable error.

## Workflow Overview

```
┌─────────────────────────────────────────────────────┐
│                  TEST MUTATE                        │
├─────────────────────────────────────────────────────┤
│  SETUP (interactive)                                │
│  1. Initialize (load or create tracking file)       │
│  2. Detect test command (first run only)            │
│  3. Determine scope (user selects, default: all)    │
│                                                     │
│  EXECUTION (autopilot — no user interaction)        │
│  For each module in scope:                          │
│    4. Spawn qa-test-mutator agent                   │
│    5. Update tracking file with results             │
│    6. Spawn implementer: tests for ALL survivors    │
│    7. Verify (new tests pass + re-mutate confirms)  │
│    8. Commit changes                                │
│  9. Final summary                                   │
└─────────────────────────────────────────────────────┘
```

## Workflow Details

### 1. Initialize

Check for `.test-mutations.json` in the project root.

**If the file exists:**
- Load tracking data
- Show progress summary: X/Y modules tested, overall mutation score Z%
- List modules by status (completed, in-progress, pending)
- Proceed to step 3 (scope selection)

**If the file doesn't exist:**
- This is a first run — proceed to step 2 (test command detection)
- After detecting the test command, discover source files (see Module Discovery below)
- Create the tracking file with initial structure
- Ask user: "Should I commit `.test-mutations.json` to version control, or add it to `.gitignore`?"

### 2. Detect Test Command

**Try in order:**

1. `Makefile` with a `test` target → `make test`
2. `package.json` with a `test` script → `npm test`
3. `go.mod` present → `go test ./...`
4. `pyproject.toml` or `pytest.ini` or `setup.cfg` with pytest config → `pytest`
5. `Cargo.toml` → `cargo test`
6. `build.gradle` or `build.gradle.kts` → `gradle test`

**If none detected:** Ask the user: "What command runs your test suite?"

**Verify the command works** by running it once. If it fails, report the error and ask the user for the correct command.

Store the test command in the tracking file.

### Module Discovery

Use Glob to find source files in the project. Exclude:
- Test files (`*_test.go`, `test_*.py`, `*.test.js`, `*.spec.ts`, etc.)
- Vendor/dependency directories (`vendor/`, `node_modules/`, `.venv/`, `target/`)
- Generated files (files with generation markers like `// Code generated`)
- Configuration files, documentation, assets

For each source file, attempt to identify covering test files using naming conventions:
- `auth.go` → `auth_test.go`
- `auth.py` → `test_auth.py` or `auth_test.py`
- `Auth.ts` → `Auth.test.ts` or `Auth.spec.ts`

Store discovered modules in the tracking file with status `pending`. If no source files are found, stop and tell the user.

### 3. Determine Scope

Present the current state to the user:

```
## Mutation Testing Progress

Overall: 3/10 modules tested (mutation score: 87%)

### Completed
- src/auth.go — score: 100% (45 mutations)
- src/config.go — score: 92% (24 mutations, 2 survivors)

### Partial (mutator capped the site count; a re-run re-mutates the whole file)
- src/payment.go — score: 80% (50 mutations)

### Pending
- src/api/handler.go
- src/models/user.go
- src/utils/parser.go
- ...

Scope? Enter file names/numbers, or press Enter to test all pending modules.
```

**User can:**
- Pick specific files by name or number (e.g., "1, 3, 5" or "src/auth.go")
- Re-run a partially covered file (there is no mid-file resume)
- Re-test a completed file (useful after adding tests)
- Press Enter / say "all" to test all pending modules (this is the default)

**Default:** All pending modules, processed in alphabetical order.

**Require a clean tree before autopilot.** Run `git status --porcelain --untracked-files=no`. If it prints anything, stop and ask the user to commit or stash first: the mutator reverts with `git restore`, and step 7 discards failed tests the same way, so any uncommitted edit to a tracked file would be silently destroyed. (The mutator re-checks its own file before each module.)

**After scope is confirmed and the tree is clean, the workflow enters autopilot mode. No further user interaction occurs until the run completes or an unrecoverable error is encountered.**

---

### Steps 4-8 repeat for each module in scope (autopilot)

### 4. Spawn Mutator Agent

Spawn a `qa-test-mutator` agent with the selected source file and test command:

```
Apply mutation testing to the following source file:
- Source file: [path]
- Test command: [command]

Systematically mutate the source code, run tests after each mutation,
and report which mutations are killed vs survived.
```

Wait for the agent to complete and collect its results.

**If the agent returns `ABORTED`:**
- `dirty file` — stop the run; something changed the tree mid-run. Report it to the user.
- `baseline red` — the shared suite is failing, so every module's results would be meaningless. Stop the run and report the failing output.

### 5. Update Tracking File

Parse the mutator agent's results and update `.test-mutations.json`:

- Set module status to `completed` (or `in_progress` if the agent reported partial coverage)
- Populate `mutations_by_type` with results grouped by mutation type
- Store surviving and likely-equivalent mutation examples in the `examples` arrays
- Calculate `mutation_score` for the module
- Update `global_statistics` (recalculate totals and overall score)
- Set `last_updated` timestamp

Write the updated tracking file.

### 6. Spawn Implementer to Write Tests

**If no survivors (100% mutation score):** Log the result and proceed to step 8.

**Likely-equivalent mutants are not test tasks.** The mutator marks survivors that no input can distinguish from the original, with a reason. Do not send them to the implementer; record them in the tracking file and list them in the final summary so a human can confirm. Review each reason as you pass it through — if the reason doesn't hold, treat the mutant as an ordinary survivor.

**If survivors exist:** Write tests for ALL surviving mutations.

**Spawn `swe-implementer`.** For a small number of simple survivors, writing the tests directly as orchestrator is fine.

**Before spawning**, record the untracked files: `git ls-files --others --exclude-standard`. Step 7's rollback deletes only files that are new since this snapshot, never the user's pre-existing untracked files.

**Prompt the implementer with:**

```
Mode: kill mutants. Do not re-apply mutations or commit; the orchestrator
re-mutates in step 7.

Write tests to catch the following surviving mutations in [source file]:

1. Line 42: `amount + fee` → `amount - fee`
   The test must verify that the fee is ADDED, not subtracted.

2. Line 78: `price > 0` → `price >= 0`
   The test must verify behavior when price is exactly 0.

3. Line 103: `valid && active` → `valid || active`
   The test must verify that BOTH conditions are required.

Each test should:
- Target the specific behavior that the mutation would break
- Follow the project's existing test conventions
- Be focused and minimal (one assertion per concern)
- Have a clear name indicating what it verifies
```

### 7. Verify

**Run the test suite** to confirm new tests pass with the correct (unmutated) code.

**If new tests fail:** Give the implementer (or yourself) one chance to fix. If still failing, log the failure, remove the tests added for this module (delete untracked files absent from step 6's snapshot; `git restore` modified ones), and continue with the next module.

**Re-mutate to confirm kills:** For each addressed surviving mutation:

1. Re-apply the specific mutation (Edit)
2. Run the test command
3. Verify tests now FAIL (mutation is killed)
4. Revert (`git restore`)

**If a re-applied mutation still survives:** Log it as an unresolved survivor and continue. Do not retry or prompt the user.

Update the tracking file: mark confirmed kills, update mutation score.

### 8. Commit

Automatically commit the changes for this module. Stage the new or modified test files, plus `.test-mutations.json` unless step 1 gitignored it (`git check-ignore -q .test-mutations.json` succeeds; `git add` errors on an ignored path). If nothing is staged (`git diff --cached --quiet` succeeds), skip the commit.

```bash
git add [test files]   # plus .test-mutations.json, unless ignored
git commit -m "$(cat <<'EOF'
test: improve mutation coverage for [module]

Mutation score: X% → Y%
- Added tests targeting N surviving mutations
- [brief description of what the new tests verify]
EOF
)"
```

Print a short progress line before moving to the next module:

```
[3/8] src/payment.go — score: 85% → 95%, 4 tests added. Continuing...
```

Then loop back to step 4 with the next module in scope.

### 9. Final Summary

After all modules in scope have been processed:

```
## Mutation Testing Complete

### Modules Tested This Session
| Module             | Before | After | Tests Added | Unresolved | Equivalent |
|--------------------|--------|-------|-------------|------------|------------|
| src/auth.go        | —      | 100%  | 0           | 0          | 0          |
| src/payment.go     | —      | 95%   | 4           | 2          | 1          |
| src/config.go      | —      | 88%   | 3           | 3          | 0          |

### Project Progress
- Modules complete: 8/10
- Overall mutation score: 91%

### Unresolved Survivors
- src/payment.go:92 — `maxRetries = 3` → `maxRetries = 4` (constant)
- src/payment.go:103 — removed `audit.Log(transaction)` (statement deletion)
- src/config.go:45 — `timeout > 0` → `timeout >= 0` (relational)
- ...

### Likely-Equivalent (confirm by hand)
- src/payment.go:61 — `i < n` → `i != n` (loop index only increments from below `n`)

### Commits Made
- abc1234 test: improve mutation coverage for auth module
- def5678 test: improve mutation coverage for payment module
- ghi9012 test: improve mutation coverage for config module
```

Report any modules that were skipped due to errors (implementer failures, test failures, etc.) and why.

## Tracking File Format

**File:** `.test-mutations.json` in project root.

```json
{
  "version": "1.0",
  "test_command": "go test ./...",
  "last_updated": "2026-02-12T15:30:00Z",
  "modules": {
    "src/auth.go": {
      "status": "completed",
      "covering_tests": ["src/auth_test.go"],
      "last_tested": "2026-02-12T15:30:00Z",
      "mutations_by_type": {
        "arithmetic": {
          "total": 12,
          "killed": 11,
          "survived": 1,
          "timeout": 0,
          "likely_equivalent": 0,
          "examples": [
            {
              "line": 42,
              "original": "count + 1",
              "mutated": "count - 1",
              "result": "survived",
              "test_that_caught_it": null
            }
          ]
        }
      },
      "mutation_score": 91.7,
      "insights": []
    }
  },
  "global_statistics": {
    "total_modules": 10,
    "completed_modules": 3,
    "total_mutations": 150,
    "total_killed": 135,
    "total_survived": 15,
    "overall_score": 90.0
  }
}
```

**Field notes:**
- `examples` should include all surviving mutations (for reporting) and a few representative killed mutations (for insight). Don't store every killed mutation — just survivors and notable kills.
- `insights` are human-readable observations the mutator agent provides (e.g., "Strong error handling coverage" or "No tests for boundary conditions").
- `global_statistics` are recalculated from module data on each update.
- `mutation_score` is (killed + timeout) / (total − likely_equivalent). Skipped mutations are not counted in `total`.
- `status` is one of `pending`, `in_progress`, `completed`. `in_progress` means the mutator capped its site count (partial coverage); re-testing re-mutates the whole file.

## Agent Coordination

**All subagents MUST be executed sequentially — NEVER in parallel.** Mutation testing works by modifying source files and running tests against those modifications. Parallel agents will simultaneously edit the same files, corrupt each other's mutations, and produce meaningless results. This applies to every agent spawn in this workflow: mutator agents, implementer agents, and verification steps. One agent at a time, wait for it to finish, then spawn the next.
