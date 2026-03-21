# /bug-hunt - Proactive Bug Discovery

## Overview

The `/bug-hunt` skill systematically hunts for bugs before they reach users. An assessor analyzes the codebase to identify high-risk hotspots by cross-referencing code complexity, test coverage gaps, and structural risk factors. Focused hunters then deep-dive into each hotspot, writing reproducing tests to validate or invalidate suspected bugs.

**Key benefits:**
- Multi-signal assessment: cross-references complexity, coverage, structural risk, and git history to find where bugs are most likely to lurk
- Evidence-based findings: every confirmed bug has a reproducing test — no speculative reports
- Coverage as a side effect: tests that invalidate a suspicion are kept if they improve coverage
- Pattern detection: sequential investigation enables cross-hotspot pattern discovery
- Actionable output: confirmed bugs come with reproducing tests that serve as acceptance criteria for fixes

## When to Use

**Use `/bug-hunt` for:**
- Pre-release quality assurance on critical modules
- After major refactors or feature additions where subtle bugs may have been introduced
- When a module has a history of edge-case bugs and you want to proactively find more
- When onboarding a new codebase and you want to understand where the bodies are buried
- Before handing off code to another team

**Don't use `/bug-hunt` for:**
- Fixing a known, reported bug (use `/bugfix` — it's designed for reactive investigation)
- Security-focused analysis (use `/audit-source` — it has dedicated security methodology)
- Improving test coverage for its own sake (use `/review-test`)
- General code quality review (use `/review-source`)

**Rule of thumb:** If you know the bug, use `/bugfix`. If you want to find the bugs you don't know about yet, use `/bug-hunt`.

## Workflow

```
┌──────────────────────────────────────────────────────┐
│                  BUG HUNT WORKFLOW                    │
├──────────────────────────────────────────────────────┤
│  1. Determine scope                                  │
│  2. Spawn assessor (risk analysis)                   │
│     └─ Output: ranked hotspot list + coverage map    │
│  3. For each hotspot:                                │
│     └─ Spawn hunter (investigation + repro tests)    │
│     └─ Prior findings passed to subsequent hunters   │
│  4. Synthesize findings                              │
│  5. Present consolidated findings to user            │
│  6. Optionally route findings to fixers              │
│  7. Optionally commit reproducing tests              │
└──────────────────────────────────────────────────────┘
```

### 1. Determine Scope

The skill asks about scope, areas of concern, and areas to skip. By default, the hunt targets production code only — test code, dev-only dependencies, generated code, and vendored code are excluded. User concerns inform prioritization but don't replace systematic analysis.

### 2. Risk Assessment

A `swe-bug-assessor` agent analyzes the codebase using multiple signals: code complexity, test coverage (instrumented if available, manual inspection otherwise), structural risk factors (error handling gaps, shared mutable state, edge case blindness, etc.), and optionally git churn patterns. The assessment cross-references signals — hotspots where multiple signals converge are ranked highest.

### 3. Focused Investigation (Hunters)

Each hotspot gets a dedicated `swe-bug-hunter` agent. Hunters run sequentially so findings accumulate — patterns discovered in one hotspot inform investigation of the next. For each suspected bug, the hunter writes a reproducing test and runs it:

- **Test fails**: Bug confirmed. Test kept as evidence and future regression test.
- **Test passes**: Suspicion invalidated. Test kept if it improves coverage, deleted if redundant.

### 4. Synthesis

Findings are cross-referenced to identify systemic patterns — common root causes, shared utility bugs, or codebase-wide anti-patterns. Systemic patterns may warrant follow-up with `/refactor`.

### 5. Consolidated Report

A single report with confirmed bugs (each with reproducing test), coverage improvements, suspected-but-unconfirmed issues, and systemic patterns. Presented interactively — CRITICAL findings first.

### 6. Fix Routing (Optional)

Confirmed bugs can be routed to language-appropriate SME agents. The reproducing test serves as the acceptance criterion — the fix is done when the test passes. Each fix is verified by `qa-engineer` and committed atomically.

### 7. Test Commit (Optional)

Reproducing tests (both bug-confirming and coverage-improving) can be committed in a single commit, even if the user declines fix routing. The tests document known bugs and improve coverage regardless.

## Agents Used

| Agent              | Role                                             |
| ------------------ | ------------------------------------------------ |
| `swe-bug-assessor` | Risk assessment and hotspot identification       |
| `swe-bug-hunter`   | Focused investigation with reproducing tests     |
| `swe-sme-*`        | Implement bug fixes (optional)                   |
| `qa-engineer`      | Verify fixes don't break functionality (optional)|

## Resource Usage

This skill is deliberately thorough. A hunt across a medium-sized codebase may spawn 5-15+ agents (1 assessor + 1 hunter per hotspot) and take significant time. Each suspected bug gets a reproducing test, which means the investigation phase involves writing and running code, not just reading it. The payoff is that every finding is backed by evidence.
