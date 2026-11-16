# /review-perf - Performance Review

The step-by-step procedure lives in [`SKILL.md`](../SKILL.md); this guide covers when to use the skill and what to expect.

## Overview

`/review-perf` reviews a project for performance issues in two domains: **compute performance** (algorithms, memory, CPU, costed at the codebase's actual scale) and **web performance** (caching, asset delivery, loading strategy, Core Web Vitals). It detects which domains apply and dispatches the matching specialist, or both for a full-stack project, in parallel.

Why it's shaped this way:

- **Measure, don't guess.** Performance intuitions are unreliable. The reviewers identify structural issues and recommend what to measure, not just what to optimize. The compute reviewer establishes each hot path's input size and budget from the repo, and also flags machinery that is over-provisioned for the real scale.
- **Two domains, two specialists.** Network-bound and compute-bound performance are different disciplines; one lens applied to everything misses half the problems. The report adds a cross-cutting synthesis for issues that span both (for example, server-side rendering that is both a compute bottleneck and a loading problem).
- **Diagnostic, not therapeutic.** It recommends fixes and never implements them.

```
Detect project type ──▶ Scope ──▶ Reviewers (compute ∥ web) ──▶ Consolidated report
```

## When to Use

**Use `/review-perf` for:**
- Evaluating the performance posture of a project
- Pre-release performance checks
- Auditing after significant architectural or feature changes
- Understanding where time is spent (network vs. compute)

**Don't use `/review-perf` for:**
- Implementing optimizations: ask directly after reviewing findings, or use `/implement`
- Shrinking over-provisioned machinery: `/refactor` (this skill recommends it, scoped to the module)
- Strategic orientation on an unfamiliar repo: `/review-repo`
- Accessibility or security: `/review-a11y`, `/review-security`

## What You'll Be Asked

Unless the invocation or a caller (such as `/review-repo`'s follow-up) supplies scope, the skill shows the detected project characteristics and asks what to review: both domains (default), web only, compute only, or a specific directory. If it finds no performance-relevant source code, it says so and stops.

## What You Get Back

A consolidated report, inline:

- **Web performance:** findings by severity (CRITICAL / HIGH / LOW), with caching and asset-delivery assessments.
- **Compute performance:** findings by severity, the hot paths (input size, frequency, budget, cost, verdict), over-provisioned machinery with a simpler replacement, and the cold paths dismissed.
- **Cross-cutting concerns,** when any exist.
- **Suggested next steps,** including tooling to adopt (Lighthouse, benchmarking frameworks, profilers) when it's missing.

A domain that doesn't apply is marked not applicable. "No significant issues" is a valid result. The skill is read-only and lightweight, and it proposes no tickets; under `/review-repo`'s follow-up, its findings feed that skill's consolidated ticket set.
