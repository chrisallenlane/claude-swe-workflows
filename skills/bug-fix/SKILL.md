---
name: bug-fix
description: Diagnosis-first bug fixing with test-driven reproduction, root-cause analysis, and a targeted fix plus regression test. Use when the user wants to fix a bug with thorough investigation.
model: opus
---

# Bugfix - Automated Bug-Fixing Workflow

Coordinates specialist agents through a bug-fixing cycle: clarify bug -> reproduce with failing test -> diagnose root cause -> implement fix -> verify -> review -> document.

## Workflow

### 1. Clarify the bug

**Gather bug details from user:**
- What are the symptoms? (error messages, unexpected behavior, crashes)
- What is the expected behavior vs actual behavior?
- How do you reproduce it? (steps, inputs, configuration)
- When did it start? Any recent changes that might be related?
- Environment specifics? (OS, versions, configuration)

**Ask clarifying questions if needed:**
- Ambiguous symptoms
- Missing reproduction steps
- Unclear expected behavior

Loop back to user until the bug is clearly understood. You need enough information to write a test that demonstrates the failure.

### 2. Write Failing Test(s)

**Spawn `swe-implementer` in reproduce-a-bug mode** (or write the tests directly when the bug is small and local).

**Implementer task:**
- Write test(s) that reproduce the reported bug
- Tests should encode the *expected* behavior (so they fail against the *current* buggy behavior)
- Run the tests and **verify they actually fail**
- If the tests pass (bug cannot be reproduced): report back with findings — the bug may be environmental, already fixed, or misunderstood

**This is the contract.** When these tests pass, the bug is fixed.

**If reproduction fails:**
- Return to step 1 for more information from the user
- Report what was tried and why reproduction failed
- Max 2 reproduction attempts before escalating to user with findings

### 3. Diagnosis

**Spawn `swe-bug-investigator` agent:**
- Pass: bug description, failing test(s) from step 2, reproduction results
- Agent performs root-cause analysis:
  - Traces execution paths through the code
  - Git archaeology at agent's discretion (shallow for obvious bugs, deep for systemic ones)
  - Identifies the root cause with supporting evidence
  - Identifies related failure modes that may share the same root cause
- Agent produces a structured diagnosis report

**Diagnosis report includes:**
- Root cause (immediate and underlying)
- Evidence (code paths, git history, test results)
- Recommended fix approach
- Related failure modes (specific, actionable — not vague possibilities)
- Confidence level

### 4. Implement the Fix

**Re-invoke the implementer from step 2, now in implement mode, with the diagnosis report:**
- Pass the diagnosis report as guidance
- It implements the fix following the diagnostician's recommended approach
- It writes additional tests for related failure modes identified in step 3
- It verifies: the originally-failing test(s) from step 2 now pass
- It runs the full test suite to check for regressions

**Implementation agent responsibilities:**
- Fix the bug as narrowly and precisely as possible
- Don't refactor unrelated code (that's a separate workflow)
- Write tests for each related failure mode the diagnostician identified
- Ensure all new and existing tests pass

### 5. Quality Assurance - Verify Fix (CRITICAL GATE)

**Spawn `qa-engineer` agent:**
- Pass: original bug description, reproduction steps, and acceptance criteria: the bug no longer occurs, plus one criterion per related failure mode the diagnostician identified in step 3
- The agent infers its mode from context: presence of acceptance criteria triggers acceptance verification
- Agent performs **practical verification first** — actually reproducing the originally-reported scenario and confirming it's fixed
- This means: executing CLI commands, speaking JSON-RPC to MCP servers, making API calls, driving the page in a browser, etc.
- Only AFTER practical verification confirms the fix works does the agent run the full test suite

**This is a CRITICAL GATE:**
- The originally-reported bug must be demonstrably fixed (practical test) AND tests must pass to proceed
- If practical verification fails: return to step 4 (implementation) immediately
- If verification passes but tests fail: return to step 4 with the failing output — QA reports failures, it never fixes product code
- Track iteration count (max 3 attempts before escalating to user)

**Expected output:** Practical verification results, pass/fail determination with specific findings.

### 6. Code Review (Conditional)

**Only proceed to code review if fix verification passed.** Don't review broken code.

Conditionally invoke specialized reviewers based on code changes and complexity. All reviewers provide feedback; implementation agent responds to all feedback in step 7.

#### 6a. Security Review (Conditional - Has Authority)

**If security-sensitive code changed (auth, crypto, input validation, data access):**

**Spawn `sec-blue-teamer` with the diff (Mode: scoped review):**
- Evaluates defensive security posture of changed code
- Checks control consistency, defense-in-depth, and configuration
- Identifies systemic gaps that enable vulnerability classes
- **Has authority to demand changes** - security issues should block or require explicit user approval

**Output**: Defense evaluation with severity levels (critical/high/medium/low)

#### 6b. Scope Audit (Conditional - Departures Resolved)

**If non-trivial implementation (>50 lines changed, multiple files, or complex logic):**

**Spawn `swe-code-reviewer` agent** with the diff and the step-3 diagnosis report:
- Audits the fix against the narrow fix the diagnosis calls for: anything built beyond what the fix and its related failure modes require — new helpers, options, abstractions, or a mechanism duplicating one already in the codebase
- Every departure is evidence-cited (file:line, and the search that proves a duplicate)
- Agent reports "No departures" when the diff stays within the fix

**Output**: Departures. They are not advisory: step 7 resolves each one by removing it, or by naming the failure mode or requirement that forces it.

#### 6c. Performance Review (Conditional - Advisory)

**If performance-critical code changed (hot paths, loops, database queries, API endpoints):**

**Spawn `swe-perf-reviewer` with the diff (Mode: change review):**
- Costs the changed path at its actual n against its budget
- Exits "no performance impact" when the change isn't on a path that scales

**Output**: Findings with their scale evidence (advisory only)

### 7. Implement Review Feedback

**Aggregate all review feedback from step 6 and provide to implementation agent.**

**Re-invoke the implementation agent from step 4** (`swe-implementer`, or yourself if you implemented directly):
- Provide all review feedback (security, scope-audit departures, performance)
- The implementer reviews all feedback and **uses its own discretion** to implement
- **Security findings**: Critical/High must be addressed or get explicit user approval to skip; Medium/Low are advisory
- **Scope-audit departures**: Each is removed, or justified by the failure mode or requirement that forces it
- **Performance feedback**: Advisory only - the implementer has final authority, and may decline recommendations that conflict with the project's conventions
- The implementer implements accepted changes (uncommitted; step 13a commits).

### 8. Peer Review (Conditional)

**Condition:** Non-trivial changes (>50 lines changed, multiple files, or complex logic).

**Skip if:**
- Changes are trivial (single file, <50 lines, simple logic)

**If applicable, spawn a fresh `swe-implementer` in peer-review mode:**
- Fresh context window - reviewer sees only current code state via git diff
- Reviews with "would I accept this PR" lens
- Focuses on: minor oversights, idiom, naming, small cleanups
- **Has authority to make small fixes directly**

**Scope constraints (critical):**
- Small cleanups and nits only
- No architectural changes
- No re-implementing features
- No changing approaches or patterns chosen by the original implementer
- If something seems wrong at a deeper level, flag it rather than fix it — deeper issues escalate to the user
- If its changes break tests, revert them and proceed (nits aren't worth breaking functionality)

**Expected output:** Small fixes (uncommitted), or "no changes needed" if code is clean.

### 9. Quality Assurance - Coverage of the Changed Diff

**Spawn `qa-engineer` agent:**
- The agent infers its mode from context: absence of acceptance criteria triggers Mode 2, coverage of a changed diff
- Pass the diff of all changed code (from steps 4, 7, and 8)
- Assess test coverage for new/modified code
- Identify gaps and write missing tests
- Run the suite and linters; failures are reported, not fixed — they route back to step 7 or step 4
- **Verify implementations from steps 7 and 8 didn't break tests** - catches issues from refactoring, security fixes, or peer review cleanups

**This is SUPPLEMENTARY:**
- Issues found here don't block the workflow by default
- Agent documents issues and writes tests; it does not modify product code
- Minor issues: proceed to documentation
- Significant issues (tests broken, major bugs): return to step 7 (review feedback) or step 4 (implementation)

**Expected output:** Suite and linter results, tests added, failures for the implementer.

### 10. Correctness Review (Conditional — Blocking)

**This is the analytical correctness gate.** Every gate before this point is either empirical (step 2's reproducing test, step 5's practical verification, step 9's test suite) or quality-focused (security posture, clarity, idiom nits). The reproducing test verifies *the bug is gone*; nothing before this step verifies that the fix's assumptions hold or that other call sites survive the behavior change. This step does. It runs last among the review gates deliberately: mechanical verification is cheap and analytical review is expensive — don't spend review rounds on a fix that fails its own reproducing test.

**When to run (run-unless):**

The default is to run. Skip only when the diff is trivial — typo fixes, comment- or documentation-only changes, single-line changes whose correctness is obvious by inspection. When in doubt, run it.

**Degraded-verification override (mandatory):** if practical verification in step 5 was impossible (the original scenario could not actually be exercised) **or** the project has no meaningful test suite, this step is **mandatory regardless of diff size**. Note that in a repo with no test infrastructure, step 2's reproduction contract itself degrades — there may be no failing test at all — making this gate the only correctness check between the fix and production.

**Spawn `swe-correctness-reviewer` agent (fresh context):**
- Provide: the full diff (or branch/commit range), target runtime and framework versions if known, the **original bug report** (the user's symptom description from step 1), and the round number if looping
- Do **not** provide: the step-3 diagnosis report, implementation history, or prior agents' outputs. The bug report is user-supplied ground truth — symptom, not rationale. The diagnosis is the implementer's adopted theory of the bug; passing it would anchor the reviewer to the same frame that produced the fix. The reviewer's question is not "did we fix the bug" (the reproducing test answers that empirically) but "does this diff rest on false assumptions or break anything else."
- The agent assumes a bug already shipped and works backward to find it, walking a six-concern spine (assumptions, runtime semantics, call sites, data flow, error paths, first-principles residual) with mechanical verification of every assumption the diff makes

**Convergence loop (blocking):**
1. Reviewer reports findings (blocking) and residual risks (non-blocking)
2. **Zero findings:** proceed to step 11. Carry any residual risks forward to the final summary (step 12) so a human sees them.
3. **Findings:** re-invoke the implementation agent (same one as steps 2/4) to resolve each one — fix it, or refute it with cited evidence
4. Re-run mechanical verification — **the step-2 reproducing test explicitly** (it is the contract artifact and must still pass after correctness fixes), plus the full test suite and linters
5. Spawn a **fresh** `swe-correctness-reviewer` instance to re-review the updated diff in full
6. Repeat until a round reports zero findings

**Iteration cap: 3 rounds.** If findings persist after 3 rounds, escalate to the user with the surviving findings and the implementation agent's responses.

**Expected output:** APPROVE verdict (possibly with residual risks for the final summary), or escalation after cap exhaustion.

### 11. Documentation

Spawn `doc-maintainer` in targeted mode with the diff.

### 12. Final verification

**Run comprehensive checks:**
- Execute full test suite (must pass)
- Run all linters and formatters
- Verify no new warnings introduced
- Check git status (document any uncommitted changes)

**Present summary to user:**
- Bug that was fixed (original report)
- Root cause identified (from diagnosis)
- Files changed
- Tests added/modified (regression tests for the bug + related failure modes)
- Residual risks surfaced by the correctness review (step 10), if any
- Any remaining TODOs or follow-ups

**If verification fails:**
- Determine root cause (implementation bug vs. refactoring issue vs. test issue)
- Return to appropriate step (step 4 for implementation bugs, step 7 for refactoring issues)
- Report specific failures to user

### 13. Workflow Completion (Optional)

**After presenting summary from step 12, ask user if they want to complete the workflow.**

User may also explicitly request workflow completion at any point after step 12 succeeds.

**If user confirms, perform housekeeping tasks:**

#### 13a. Commit Changes

**If uncommitted changes exist:**
- Review git status to see what changed
- Create commit with descriptive message
- If ticket number is known (from branch name, prior context, or user input):
  - Reference ticket in commit message (e.g., "Fixes #123" or "Closes: #123")
- Use heredoc format for multi-line commit messages

**Example commit message format:**
```
Fix off-by-one error in pagination boundary check

Root cause: boundary comparison used < instead of <= when calculating
the last page, causing the final item to be excluded from results.
Also added regression tests for adjacent edge cases identified during
diagnosis.

Fixes #456
```

#### 13b. Update/Close Issue Tracker Ticket (Conditional)

Detect tracker, recover the ticket number, and post the close-out per [`references/trackers.md`](../../references/trackers.md) (Detection Procedure + "Comment / update (close-out)" + "Close" operations).

**Close-out comment content (skill-specific):**
- Root cause identified
- Fix applied
- Tests added (regression + related failure modes)
- Files changed

#### 13c. Sync with Main Branch (Conditional)

**Check branch state:**
- Identify main branch name (master or main)
- Check if current branch is not main
- Check if there are new commits on main that current branch doesn't have

**If current branch is behind main:**
- Ask user: "Your branch is behind main. Would you like to rebase on main?"
- If user confirms:
  - Perform: `git fetch origin <main-branch> && git rebase origin/<main-branch>`
  - If conflicts arise, report to user and halt (don't auto-resolve)
  - If rebase succeeds, report success

**Skip if:**
- Current branch is main/master
- Current branch is up to date with main
- No main/master branch exists

**Present final status:**
- Changes committed
- Ticket updated/closed
- Branch rebased on main
- Ready to push or move to next task

## Agent Coordination

The step-3 diagnosis goes to the implementer, and never to the correctness reviewer (step 10).

## Iteration Limits

- Reproduction (step 2): 2 attempts; fix verification (step 5): 3 attempts; correctness review (step 10): 3 rounds
- When a limit is reached, escalate: present the current state, explain what's blocking progress, and request guidance

## Invoked by Another Skill

When a calling skill (such as `/implement`) runs this one, the caller supplies the bug report and answers step 1's clarifying questions and step 13's confirmation; nothing is asked of the user. Steps 2-13a run unchanged. Skip 13b — never update or close tickets — and never rebase (13c). Escalations go to the caller, which decides whether to escalate further.
