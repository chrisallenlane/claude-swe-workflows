# /review-health — Strategic Orientation Review

## Overview

`/review-health` is a first-pass strategic-orientation skill for a repository. It produces an evidence-cited map of the repo's state, calibrated to a reference class, designed to inform strategic decisions about how to engage with the project.

Use it when you want to step back and assess a repo *strategically* — not when you want line-by-line defect analysis (`/refactor`), architectural restructuring (`/review-arch`), or a security audit (`/review-security`).

## Core Design

**OODA-structured workflow.** Observe → Orient → Decide → Act, with strict phase gates. The Observe phase collects signals without interpretation; Orient applies the calibration rubric; Decide generates strategic options for the user's lens; Act produces a concrete next-step queue. Later phases cite earlier phases.

**Reference-class calibration.** "Good" is a relational claim — a 34% test-coverage finding means something different for a research prototype than for an OSS library. The skill classifies the target repo into a reference class first (see `classes/`), then applies class-specific rubrics to each dimension.

**Evidence-cited findings.** Every claim carries a `file:line` citation or a tool-output reference. A finding without evidence is dropped or moved to the Coverage Manifest.

**Coverage Manifest as first-class output.** Tools that couldn't run, signals that couldn't be computed, and dimensions that couldn't be assessed are explicitly named with the reasons they couldn't be resolved. Named unknowns beat silent unknowns.

**Lens-aware output.** The skill elicits the user's context at invocation (inheriting work repo / evaluating FOSS / revisiting own / onboarding teammate / other) and shapes the Decide-phase options accordingly.

## Reference Materials

| File | Purpose |
|------|---------|
| `severity-tiers.md` | ASHI-style severity taxonomy (Safety Hazard / Major / Minor / Cosmetic) applied to individual findings |
| `classes/README.md` | Classification philosophy + how-to-add-a-class guide |
| `classes/solo-utility.md` | Solo or small-team CLI / utility / internal tool |
| `classes/production-service.md` | Team-maintained production service or backend |
| `classes/oss-library.md` | OSS library with external consumers |
| `classes/prototype.md` | Prototype / research / pre-production exploratory codebase |

## When to Use

**Use `/review-health` for:**

- Strategic overview of a repo you've just inherited
- Evaluating a FOSS project for adoption or contribution
- Revisiting your own project to decide where to invest effort
- Generating an onboarding map for a new teammate
- Any "where am I, where should I start, what should I avoid" question

**Don't use `/review-health` for:**

- Finding specific bugs → `/bug-fix` or `/bug-hunt`
- Making changes → `/refactor`, `/implement`
- Deep architectural review → `/review-arch`
- Test-coverage gaps → `/review-test`
- Security audit → `/review-security`
- Performance analysis → `/review-perf`

**Rule of thumb:** `/review-health` answers "what is this repo, and what does that mean for me?" Every sibling specialist answers a deeper, narrower question. `/review-health` often recommends one or more of them as next steps.

## What the Output Looks Like

The skill presents its report inline as structured markdown, in this order:

1. **Context** — lens the user supplied, scope, and the repo's reference class (with evidence and override instructions)
2. **Observation Record** — factual signals grouped by category, ID-referenced (`O1`, `O2`, ...)
3. **Findings (Orient)** — per-dimension rubric placement (Foundational / Adequate / Strong) with cited evidence; severity-tiered individual findings within each dimension; cross-cutting synthesis
4. **Coverage Manifest** — what couldn't be assessed, with reasons
5. **Strategic Options (Decide)** — lens-specific engagement options, each citing Orient findings
6. **Next Steps (Act)** — top 3-5 prioritized recommendations, including sibling-skill invocations with scoped arguments

## Cognitive Failure Modes the Skill Countermands

Each element of the design is a countermeasure to a specific predictable failure of informal repo review:

| Failure mode | Countermeasure |
|---|---|
| Inheritor's paralysis / availability bias — fixate on first file opened | Systematic Observe phase with fixed signal battery |
| Unknown-unknowns dominance | Coverage Manifest elevates missing tooling to first-class output |
| Premature closure | Phase-integrity gates (Orient cites Observe; Decide cites Orient) |
| Expert deference — accept prior-author choices unexamined | Differential-diagnosis classification forces candidate alternatives with evidence |
| Free-floating adjectives ("health: good") | Reference-class calibration with cited per-class rubrics |

## Intellectual Foundations

The skill draws on practitioner traditions that have solved "rapid assessment of unfamiliar systems under uncertainty" at higher stakes than software review:

- **OODA loop** (Boyd) — Observe before Orient; Orient is the step most commonly skipped
- **Medical differential diagnosis** — enumerate candidates with evidence for/against before committing
- **Home inspection (ASHI)** — severity-tiered findings with mandatory evidence
- **Marine surveying** — reference-class calibration ("good for a 30-year cargo ship" ≠ "good for a 2-year yacht")
- **Technical due diligence (M&A)** — decision-oriented report structure; known-risks and known-unknowns both surfaced
- **Intelligence situational-awareness briefings** — BLUF + confidence-calibrated assessments + collection gaps

## Agent Usage

The skill is primarily executed by the main Claude instance. Subagents are used narrowly:

- **Observe-phase scouts (optional):** parallel subagents for discrete signal-collection tasks on large repos
- **SME consultation (optional, narrow):** for single dimensions requiring specialized language/domain knowledge

Per-language SME dispatch is *not* the default. That was the prior skill's failure mode.

## Resource Profile

Read-only. Non-destructive. Runtime varies with repo size: a small repo (<5k LOC) can complete in minutes; a large multi-service monorepo may take longer, primarily in the Observe phase. Scope can be narrowed at Preflight to manage cost.
