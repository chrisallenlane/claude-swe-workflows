# /implement - Automated Development Workflow

## Overview

The `/implement` skill orchestrates a complete development workflow through specialist agents, taking you from requirements to tested, documented, production-ready code. It coordinates design, implementation, refactoring, quality assurance, and documentation in a systematic, repeatable process.

**Key benefits:**
- Specialist expertise applied to each phase
- Prevents common failure modes (untested code, breaking changes, outdated docs)
- Design-first discipline: nothing is built that a requirement does not force
- Built-in quality gates and feedback loops
- Language-specific best practices enforced
- Comprehensive but efficient (agents skip unnecessary work)

## When to Use

**Use `/implement` for:**
- Non-trivial features requiring multiple files or subsystems
- Bug fixes where you want comprehensive testing and documentation
- Changes where quality gates matter (refactoring, security, performance)
- Work that benefits from specialist review (GraphQL APIs, Docker, Makefiles)
- Features where practical verification is important (CLI tools, MCP servers)

**Don't use `/implement` for:**
- Simple typo fixes or trivial one-line changes
- Quick exploratory work or prototyping
- Tasks where overhead outweighs benefit
- Work you'll throw away or iterate on rapidly

**Rule of thumb:** If the task is substantial enough that you'd normally write tests, update docs, and get a code review, use `/implement`.

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ /implement Workflow                                               │
└─────────────────────────────────────────────────────────────────┘

 ┌──────────────────────────────────────────────┐
 │  1. REQUIREMENTS CLARIFICATION               │
 │  ────────────────────────────────────────    │
 │  • Gather requirements from user             │
 │  • Ask clarifying questions                  │
 │  • Define acceptance criteria                │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  2. DESIGN AND PLANNING                      │
 │  ────────────────────────────────────────    │
 │  2a. Concept inventory (always)              │
 │      • Every concept cites its requirement   │
 │      • Naive baseline is the default         │
 │      • Shop before you build                 │
 │      • No caller, no export                  │
 │                                              │
 │  2b. Planning (conditional)                  │
 │      Agent: swe-planner                      │
 │      Complex task?                           │
 │      ├─ Yes → Generate implementation plan   │
 │      └─ No  → Skip to implementation         │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  3. IMPLEMENTATION                           │
 │  ────────────────────────────────────────    │
 │  Agent: Language-specific SME or generalist  │
 │                                              │
 │  Detects project type:                       │
 │  • Go         → swe-sme-golang               │
 │  • GraphQL    → swe-sme-graphql              │
 │  • Docker     → swe-sme-docker               │
 │  • Makefile   → swe-sme-makefile             │
 │  • Ansible    → swe-sme-ansible              │
 │  • Zig        → swe-sme-zig                  │
 │  • HTML       → swe-sme-html                 │
 │  • CSS        → swe-sme-css                  │
 │  • JavaScript → swe-sme-javascript           │
 │  • TypeScript → swe-sme-typescript           │
 │  • Other      → Generalist implementation    │
 │                                              │
 │  Builds the inventoried concepts, and only   │
 │  those, + writes unit tests                  │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  4. QA - ACCEPTANCE VERIFICATION             │
 │  ────────────────────────────────────────    │
 │  Agent: qa-engineer (Mode 1)                 │
 │                                              │
 │  CRITICAL GATE:                              │
 │  1. Practical verification (actually run it) │
 │  2. Write unit tests                         │
 │                                              │
 │  Passes? ──┬─ Yes → Continue                 │
 │            └─ No  → Back to step 3 ──┐       │
 │                     (max 3 attempts) │       │
 └──────────────────┬───────────────────┘       │
                    ▼                           │
 ┌──────────────────────────────────────────────┤
 │  5. CODE REVIEW (conditional reviewers)      │
 │  ────────────────────────────────────────    │
 │  Only review working code!                   │
 │                                              │
 │  Conditional reviews based on code changes:  │
 │                                              │
 │  5a. Security (if sensitive code)            │
 │      Agent: sec-blue-teamer                  │
 │      Authority: Can demand changes           │
 │                                              │
 │  5b. Refactoring (if non-trivial, or the     │
 │      inventory lists new concepts/exports)   │
 │      Agent: swe-code-reviewer                │
 │      Authority: Inventory departures must    │
 │      be resolved; the rest is advisory       │
 │                                              │
 │  5c. Performance (if critical code)          │
 │      Agent: swe-perf-reviewer                │
 │      Authority: Advisory suggestions         │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  6. IMPLEMENT REVIEW FEEDBACK                │
 │  ────────────────────────────────────────    │
 │  Agent: Same as step 3 (SME or generalist)   │
 │                                              │
 │  • Aggregate all review feedback             │
 │  • Security: Must address or get approval    │
 │  • Inventory departures: Remove or amend     │
 │  • Other: Advisory - use discretion          │
 │  • Implement accepted changes                │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  7. SME PEER REVIEW (conditional)            │
 │  ────────────────────────────────────────    │
 │  Agent: Fresh instance of same SME as step 3 │
 │                                              │
 │  Non-trivial changes?                        │
 │  ├─ Yes → Fresh SME reviews with clean slate │
 │  │        "Would I accept this PR?" lens     │
 │  │        Makes small fixes directly (nits)  │
 │  └─ No  → Skip to QA                         │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  8. QA - COVERAGE & QUALITY                  │
 │  ────────────────────────────────────────    │
 │  Agent: qa-engineer (Mode 2)                 │
 │                                              │
 │  • Test coverage analysis                    │
 │  • Fill coverage gaps                        │
 │  • Run linters/formatters                    │
 │  • Verify steps 6-7 didn't break tests       │
 │                                              │
 │  Tests broken? → Back to step 6 or revert 7  │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  9. CORRECTNESS REVIEW (run-unless)          │
 │  ────────────────────────────────────────    │
 │  Agent: swe-correctness-reviewer (fresh)     │
 │                                              │
 │  "The bug has already shipped. Find it."     │
 │  • Verify every diff assumption vs repo      │
 │  • Findings are blocking, not advisory       │
 │  • Mandatory if empirical gates degraded     │
 │                                              │
 │  Findings? ──┬─ Yes → fix → fresh review     │
 │              │      (max 3 rounds)           │
 │              └─ No → APPROVE, continue       │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  10. DOCUMENTATION                           │
 │  ────────────────────────────────────────    │
 │  Agent: doc-maintainer                       │
 │                                              │
 │  • Update affected documentation             │
 │  • Verify code examples                      │
 │  • Check for broken links                    │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  11. FINAL VERIFICATION                      │
 │  ────────────────────────────────────────    │
 │  • Run full test suite                       │
 │  • Run all linters                           │
 │  • Check git status                          │
 │  • Present summary to user                   │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  12. WORKFLOW COMPLETION (optional)          │
 │  ────────────────────────────────────────    │
 │  Ask: "Complete the workflow?"               │
 │                                              │
 │  If yes:                                     │
 │  • Commit all changes                        │
 │  • Update/close ticket (if applicable)       │
 │  • Rebase on main (if applicable)            │
 │  • Present final status                      │
 └──────────────────────────────────────────────┘
```

## Workflow Details

### 1. Requirements Clarification
The workflow starts by ensuring requirements are clear and unambiguous. The orchestrator asks clarifying questions about:
- What feature/bug/change is requested
- Acceptance criteria (how do we know it works?)
- Constraints or preferences

This step loops until requirements are crystal clear.

### 2. Design and Planning

**2a. Concept Inventory (Always):**
Before any plan or code, the orchestrator writes down every concept the change will introduce — each type, module, mechanism, layer, configuration knob, or abstraction — and holds it to four rules:
- **Every concept cites its requirement.** A concept that no requirement or acceptance criterion forces is not built. "We might need it later" is a question for you, not a reason to write code.
- **The naive baseline is the default.** A plain array, a direct call, a hard-coded value — unless a named requirement rules the simple form out.
- **Shop before you build.** The codebase, the standard library, and existing dependencies are searched for a mechanism that already solves the problem. This is the fix for parallel machinery: the second queue or config reader that appears because nobody looked for the first.
- **No caller, no export.** A public symbol must name its caller outside the module.

The inventory scales with the task (a small fix may introduce no new concepts at all) but always runs. It then binds the rest of the workflow: the planner and the implementation agent build what it lists and nothing else, and the refactoring review in step 5b audits the diff against it.

**Why this exists:** it is cheaper not to write bloat than to strip it afterwards, and no later gate looks for working code that never needed to exist. The discipline has a ceiling — nothing at write time can prove a concept unnecessary the way `/refactor` can by removing it and re-checking behavior — so it reduces the need for `/refactor` without replacing it.

**2b. Planning (Conditional):**
For complex tasks, the `swe-planner` agent creates a structured implementation plan from the inventory:
- **Complex tasks** needing planning: architectural changes, migrations, cross-cutting concerns, multi-module features
- **Simple tasks** skip planning: bug fixes, single-file changes, straightforward CRUD

The planner produces ordered sub-tasks with What/Why/How/Verify/Risks for each step.

### 3. Implementation
A language-specific specialist (or generalist) implements the feature:
- Follows language idioms and best practices
- Writes unit tests for pure functions (TDD encouraged)
- Handles edge cases and errors
- Builds the concepts in the inventory and only those; a concept discovered mid-build is reported back and added to the inventory with its forcing requirement before it is built
- Follows the plan if one exists

**Specialists available:**
- `swe-sme-golang` - Go projects
- `swe-sme-graphql` - GraphQL schemas/resolvers
- `swe-sme-docker` - Dockerfiles and containers
- `swe-sme-makefile` - Makefiles and build systems
- `swe-sme-ansible` - Ansible playbooks and roles
- `swe-sme-zig` - Zig projects
- `swe-sme-html` - HTML structure and semantics
- `swe-sme-css` - CSS styling and layout
- `swe-sme-javascript` - Vanilla JavaScript
- `swe-sme-typescript` - TypeScript

### 4. Quality Assurance - Acceptance Verification (CRITICAL GATE)
The `qa-engineer` performs practical verification before writing tests:
- **CLI tools**: Run commands in subshell
- **MCP servers**: Spawn Claude subagent to test
- **APIs**: Make actual calls
- **Libraries**: Test with realistic usage

Only after confirming the feature works does it write unit tests. This prevents "passing tests for broken code."

**Failure mode prevented:**
```
❌ Old workflow: Write code → Write passing tests → Ship broken code
✅ New workflow: Write code → Actually run it → Then write tests
```

If verification fails, returns to implementation (max 3 attempts).

**Key insight:** Don't proceed to code review until we know the code actually works.

### 5. Code Review (Conditional Reviewers)

**Only review working code.** If acceptance verification failed, we never get here.

All reviewers run conditionally based on code changes and provide feedback. The implementation agent responds to all feedback in step 6.

**5a. Security Review (Has Authority):**
If security-sensitive code changed (auth, crypto, input validation):
- `sec-blue-teamer` evaluates defensive security posture
- Checks control consistency, defense-in-depth, and configuration
- **Has authority to demand changes** - critical/high severity findings must be addressed or require explicit user approval

**5b. Refactoring Review (Advisory, except the inventory audit):**
If non-trivial implementation (>50 lines, multiple files, complex logic), or the inventory lists any new concept or export:
- `swe-code-reviewer` audits the diff against the concept inventory: uninventoried concepts, forms more elaborate than recorded, duplicated mechanisms, exports with no outside caller. These departures must be resolved in step 6 — removed, or admitted by amending the inventory with a forcing requirement
- `swe-code-reviewer` analyzes code quality
- Identifies DRY violations, dead code, complexity
- Provides recommendations (advisory only)

**5c. Performance Review (Advisory):**
If performance-critical code changed (hot paths, loops, DB queries):
- `swe-perf-reviewer` reviews code for performance bottlenecks
- Identifies bottlenecks
- Provides optimization recommendations (advisory only)

### 6. Implement Review Feedback

The implementation agent (same as step 3) receives all review feedback and responds:
- **Security findings**: Must address or get explicit user approval to skip
- **Other feedback**: Advisory - agent uses discretion
- Specialists can decline recommendations based on language idioms
- Example: Go agent may decline "extract helper" if Go culture prefers "a little copying"

All accepted changes are implemented and committed.

### 7. SME Peer Review (Conditional)

A fresh instance of the same SME type (with a clean context window) reviews the work:
- **Condition**: Non-trivial changes (>50 lines, multiple files, or complex logic)
- **Skip if**: Changes are trivial or no language-specific SME was used

**The "fresh eyes" principle:**
- The original SME accumulates context and justifications that can create blind spots
- A fresh SME sees only the current code state via git diff
- Reviews with "would I accept this PR" lens

**Scope (critical constraints):**
- Small cleanups and nits only
- No architectural changes or re-implementing features
- No changing approaches chosen by original SME
- If something seems wrong at a deeper level, flag it rather than fix it

**Has authority to make small fixes directly** - this is efficient for nits. If peer review changes break tests, they're reverted (nits aren't worth breaking functionality).

### 8. Quality Assurance - Coverage & Quality

General QA assessment of test coverage, linters, and code quality:
- Assesses coverage for all changed code (from steps 3, 6, and 7)
- Fills coverage gaps
- Runs linters/formatters
- **Verifies steps 6 and 7 changes didn't break tests** - catches bad refactors, security fixes, or peer review issues

If tests are broken by changes from step 6, returns to step 6. If broken by step 7, reverts peer review changes. Minor issues don't block workflow.

### 9. Correctness Review (Conditional — Blocking)

The analytical correctness gate, and the last review gate in the pipeline. Every earlier gate is either empirical (run the feature, run the tests) or quality-focused (clarity, security posture, nits) — none of them reads the diff asking "is this correct?" The `swe-correctness-reviewer` agent does exactly that, with a deliberately adversarial framing borrowed from `/think-premortem`: *assume the diff already shipped and caused a production incident, then work backward to the bug.*

The reviewer walks a fixed six-concern spine:
1. **Assumptions** — every path, symbol, signature, and config key the diff references, verified mechanically against the repo
2. **Runtime semantics** — features used exist in the *target* language/framework version, not the version the model remembers
3. **Call sites** — every caller of every changed function still holds
4. **Data flow** — values traced forward to consumers and backward to producers
5. **Error paths** — failure branches, not just the happy path
6. **First-principles residual** — whatever is idiosyncratic about this diff that the spine misses

**Run-unless, not run-if:** the default is to run. The orchestrator may skip it only for trivial diffs (typo fixes, comment-only changes, single-line changes that are obviously correct). And if the empirical gates degraded — the feature couldn't actually be run in step 4, or the project has no meaningful test suite — the review is **mandatory regardless of diff size**. That rule exists because degraded environments are exactly where the rest of the pipeline silently stops checking correctness.

**Findings are blocking.** Unlike the advisory reviews in step 5, correctness findings must each be fixed or refuted with cited evidence. The loop runs: findings → implementation agent resolves → tests/linters re-run → a *fresh* reviewer instance re-reviews the full diff. Convergence is a round with zero findings; the cap is 3 rounds, then escalation.

**The reviewer's independence is structural:** it receives the diff and the repo, never the implementation rationale. Fresh eyes each round — the same anchoring-suppression principle as the SME peer review, applied to correctness.

Non-blocking "residual risks" (things unverifiable from the repo alone, like external service behavior) don't loop — they're carried forward and surfaced in the final summary so a human sees them.

### 10. Documentation
The `doc-maintainer` updates affected documentation:
- README.md for user-facing changes
- CLAUDE.md for architectural changes
- API docs for interface changes
- Verifies code examples still work

Targeted review (not comprehensive audit).

### 11. Final Verification
Comprehensive checks before presenting to user:
- Full test suite passes
- All linters pass
- No new warnings
- Git status clean

Presents summary: files changed, tests added, coverage improvements, residual risks from the correctness review (if any), TODOs.

### 12. Workflow Completion (Optional)
After presenting the summary, asks if you want to complete the workflow. If yes, performs housekeeping:

**Commit changes:**
- Creates commit with descriptive message
- References ticket number if available

**Update/close ticket (if applicable):**
- Detects platform integration
- Extracts ticket number from branch name or asks user
- Posts summary comment
- Optionally closes ticket

**Sync with main (if applicable):**
- Checks if branch is behind main
- Offers to rebase on main
- Reports conflicts if any arise

Presents final status showing what was completed.

## Examples

### Example 1: Adding a Feature to a Go CLI Tool
```
User: "Add a --format flag to support JSON and YAML output"

Workflow:
1. Clarify: Output format for what command? Default behavior?
2. Design: Inventory lists one concept (an output formatter selected by flag, forced by
           the --format requirement); shopping finds encoding/json in the stdlib and a YAML
           library already in go.mod, so no new dependency. Plan: skip (straightforward)
3. Implement: swe-sme-golang adds flag, implements formatters, writes tests
4. QA (acceptance): qa-engineer runs CLI with --format json and --format yaml,
                   verifies output actually works, writes additional test cases
5. Review: swe-code-reviewer suggests extracting common formatting logic
          (security/performance reviews skipped - not applicable)
6. Respond: swe-sme-golang reviews refactoring suggestions, implements extraction
7. Peer review: Fresh swe-sme-golang reviews, fixes minor naming inconsistency
8. QA (coverage): Checks coverage, runs linters, verifies changes didn't break tests
9. Correctness: swe-correctness-reviewer verifies flag wiring, formatter call sites,
                and library versions against go.mod — APPROVE, zero findings
10. Docs: doc-maintainer updates README with --format examples
11. Verify: All tests pass, present summary
12. Complete: User confirms, commits changes, skips ticket update, branch already up to date
```

### Example 2: GraphQL API with Security Concerns
```
User: "Add user mutation with password reset capability"

Workflow:
1. Clarify: Email verification required? Token expiration? Rate limiting?
2. Design: Inventory lists reset token, mutation, and rate limit, each citing a clarified
           requirement; shopping finds an existing mailer and rate limiter, so both are
           reused rather than rebuilt. Plan: swe-planner sequences the inventoried work
3. Implement: swe-sme-graphql implements following plan, writes resolver tests
4. QA (acceptance): qa-engineer spawns test agent, actually tests password reset
                    flow end-to-end, verifies feature works
5. Review: sec-blue-teamer finds timing attack vulnerability, recommends constant-time comparison
          swe-code-reviewer flags an exported token helper with no caller outside its module
          (inventory departure)
          (performance reviews skipped - not applicable)
6. Respond: swe-sme-graphql addresses security issue (must fix), makes the helper private
7. Peer review: Fresh swe-sme-graphql reviews, cleans up error message formatting
8. QA (coverage): Coverage check, linters, verify changes didn't break tests
9. Correctness: Round 1 finds the resolver assumes the email service throws on failure,
                but it returns null (cited evidence from the service source). Fix applied,
                tests re-run, fresh reviewer instance approves in round 2.
10. Docs: Updates API docs with mutation examples
11. Verify: All checks pass
12. Complete: User confirms, commits changes with "Fixes #456", updates and closes ticket,
             rebases on main
```

### Example 3: Simple Bug Fix
```
User: "Fix off-by-one error in pagination"

Workflow:
1. Clarify: Which pagination function? Expected behavior?
2. Design: Inventory is one line — no new concepts. Plan: skip (simple fix)
3. Implement: Fix error, add test case
4. QA (acceptance): Actually runs pagination, verifies correct behavior
5. Review: swe-code-reviewer finds no issues (all other reviews skipped)
6. Respond: Skip (no feedback to implement)
7. Peer review: Skip (trivial change)
8. QA (coverage): Coverage check
9. Correctness: Runs despite small diff — boundary logic is exactly where off-by-ones
                hide. Reviewer checks all call sites of the pagination function, APPROVE
10. Docs: doc-maintainer finds no docs affected
11. Verify: Tests pass
12. Complete: User declines, will commit manually later
```

## Tips for Effective Use

1. **Be specific with requirements**: The clearer your requirements, the better the output. Specify acceptance criteria upfront.

2. **Trust the specialists**: If a specialist declines a refactoring recommendation, they likely have a good reason (language idioms, design decisions).

3. **Let agents skip work**: Agents are designed to skip unnecessary work. Don't worry if doc-maintainer reports "no docs affected" - that's efficient.

4. **Watch for iteration loops**: If QA verification fails 3 times, there's likely a deeper issue. The workflow will escalate to you for guidance.

5. **Use for the right tasks**: This workflow is heavyweight by design. Don't use it for quick experiments or throwaway code.

6. **Leverage planning for complex work**: If you're unsure how to approach a task, let the planner think it through first.

7. **Practical verification is key**: The workflow specifically prevents "works in tests but not in reality" - agents actually run the code.

8. **Hostile repos get extra scrutiny automatically**: When the code can't be run locally and no test suite exists, the correctness review (step 9) becomes mandatory rather than discretionary. That's the lesson of legacy codebases - the environments where verification is hardest are the ones that need it most.

## Agent Coordination

All agents run **sequentially** (never in parallel):
- Each agent completes before the next starts
- State is preserved and passed between agents
- Feedback loops return to earlier steps when needed
- Max 3 iterations for acceptance verification before escalation

## Iteration Limits

**Safety limits:**
- Acceptance verification loop: 3 attempts max
- Correctness review convergence loop: 3 rounds max
- Overall workflow: 15 agent spawns max

If limits reached, workflow escalates to user with current state and specific blockers.

## Philosophy

The `/implement` workflow embodies several key principles:

**Different lenses, different stages:**
- Design focuses on "does this need to exist?" - the one stage that asks before the code is written
- Implementation focuses on "does it work?"
- Acceptance QA focuses on "does it actually work in practice?"
- Review phase focuses on multiple concerns (security, quality, performance) - all reviewers provide feedback on working code
- Response phase focuses on "how should we address feedback?" - implementation agent uses discretion
- Peer review focuses on "would I accept this PR?" - fresh eyes catch what accumulated context misses
- Coverage QA focuses on "did our changes break anything?"
- Correctness review focuses on "the bug has already shipped - where is it?" - the analytical backstop, and the only correctness gate that survives when the code can't be run and no tests exist
- Documentation focuses on "can others understand it?"

**Specialists have final say:**
- Language SMEs make language-specific decisions
- Generalist code review provides perspective
- Specialists can decline recommendations that don't fit

**Practical verification over test-passing:**
- Actually run the feature before trusting tests
- Prevents false confidence from passing tests

**Efficient thoroughness:**
- Comprehensive when needed, but agents skip unnecessary work
- Not every task needs security review or performance testing
- Conditional specialist invocation based on code changes

---

Ready to use? Just type `/implement` and describe what you want to build.
