# claude-swe-workflows

A system of composable software engineering workflows for [Claude Code][cc].
Plan projects, implement tickets, and run quality passes — from a single
ticket to a multi-batch project, using the same layered architecture.

## Installation

```bash
claude plugin marketplace add https://github.com/chrisallenlane/claude-swe-workflows.git
claude plugin install claude-swe-workflows@claude-swe-workflows
```

## How It Works

These workflows form a layered system where higher-level workflows
orchestrate lower-level ones. Each layer adds coordination, quality gates,
and autonomy.

```
/lead-project                                   ← autonomous tech lead (OODA loop)
└── invokes any skill below, driven by commander's intent

/implement-project                              ← full project lifecycle
├── /implement-batch (per batch)                ← multi-ticket orchestration
│   ├── /implement (per ticket)         ← single-ticket implementation
│   │   ├── SME implementation        ← language-specific specialist
│   │   ├── QA verification           ← practical + coverage
│   │   ├── Code review               ← security, refactor, perf
│   │   └── Documentation             ← targeted doc updates
│   ├── /refactor                     ← per-batch cleanup
│   └── /review-doc                   ← per-batch doc audit
├── /refactor (MAXIMUM aggression)    ← project-level cleanup
├── /review-arch (advisory)           ← architectural analysis; surfaces recommendations
├── /review-test                      ← test suite review
├── /review-doc                       ← documentation audit
└── /review-release                   ← pre-release readiness
```

Planning feeds implementation. `/scope-project` plans a multi-batch
project with adversarial review, producing tagged tickets that `/implement-project`
consumes directly:

```
/scope-project  →  /implement-project
    plan             implement + verify + polish
```

For single tickets: `/scope` plans, `/implement` implements.

For open-ended work where the next step depends on the outcome of the last,
`/lead-project` runs an OODA loop — observing project state, deciding what
to work on next, and invoking lower-level skills until commander's intent is
fulfilled.

Supporting workflows are available at any level:

**Reasoning and decisions:**

- `/think-reframe` — problem redefinition
- `/think-brainstorm` — divergent idea generation
- `/think-diagnose` — abductive reasoning about causes
- `/think-ach` — analysis of competing hypotheses
- `/think-deliberate` — adversarial decision-making
- `/think-premortem` — prospective failure imagination
- `/think-scrutinize` — adversarial idea critique
- `/think-reflect` — retrospective learning

**Bug work:**

- `/bug-fix` — diagnosis-first bug fixing
- `/bug-hunt` — proactive bug discovery

**Quality pipelines:**

- `/test-mutation` — mutation testing
- `/refactor-deep` — tactical cleanup followed by advisory architectural review (with optional ticket creation)
- `/review-deep` — comprehensive pre-release review pipeline

**Utility:**

- `/pre-compact` — pre-compaction housekeeping (memory, git, trash, SBAR, resume prompt)

## Choosing a Workflow

Not everything needs the full pipeline. Enter at the level that matches
your task:

| You want to...                                                          | Use                  |
|-------------------------------------------------------------------------|----------------------|
| Drive a project to completion autonomously, deciding what to work on    | `/lead-project`      |
| Implement an entire multi-batch project autonomously                    | `/implement-project` |
| Implement a batch of related tickets                                    | `/implement-batch`   |
| Implement a single ticket or feature                                    | `/implement`         |
| Plan a multi-batch project with adversarial review                      | `/scope-project`     |
| Plan a single feature and create a ticket                               | `/scope`             |
| Fix a bug with diagnosis and root-cause analysis                        | `/bug-fix`           |
| Proactively hunt for bugs before they're reported                       | `/bug-hunt`          |
| Pressure-test a problem's framing before solving it                     | `/think-reframe`     |
| Brainstorm approaches to a goal                                         | `/think-brainstorm`  |
| Reason about why a phenomenon is happening                              | `/think-diagnose`    |
| Narrow among competing hypotheses against evidence                      | `/think-ach`         |
| Make a hard decision with adversarial deliberation                      | `/think-deliberate`  |
| Imagine how a plan could fail, or how a hypothetical catastrophe could hit a running system | `/think-premortem`   |
| Scrutinize an idea or plan before committing to it                      | `/think-scrutinize`  |
| Reflect on a completed experience to update beliefs                     | `/think-reflect`     |
| Clean up code quality (DRY, dead code, naming)                          | `/refactor`          |
| Rethink module boundaries and architecture                              | `/review-arch`       |
| Review and strengthen the test suite                                    | `/review-test`       |
| Verify test quality via mutation testing                                | `/test-mutation`     |
| Audit all project documentation                                         | `/review-doc`        |
| Pre-release readiness check                                             | `/review-release`    |
| Audit web content for accessibility barriers                            | `/review-a11y`       |
| First-pass strategic orientation on a repo                              | `/review-health`     |
| Review performance (compute and/or web)                                 | `/review-perf`       |
| Perform a white-box security audit                                      | `/review-security`   |
| Run every review dimension before a release, in one go                  | `/review-deep`       |
| Tidy up the session before running `/compact`                           | `/pre-compact`       |

**Rules of thumb:**
- Open-ended work where the next step depends on the outcome of the last? `/lead-project`
- Multiple batches of tickets forming a project? `/implement-project`
- One batch of 2+ related tickets? `/implement-batch`
- One ticket? `/implement` (or `/bug-fix` if it's a bug)
- Not sure what to build yet? Start with `/scope` or `/scope-project`

## Skills

### Orchestration

These workflows manage the lifecycle of tickets — from implementation
through quality passes to a merge-ready branch.

The orchestrator family shares an autonomy discipline — high-altitude escalation, pre-loaded options, pre-rebutted recommendations, commander's intent, and risk budgets. See [references/autonomy.md](references/autonomy.md) for the discipline that governs `/lead-project`, `/implement-project`, `/implement-batch`, and `/refactor-deep`.

#### /lead-project — Autonomous Technical Lead

Drives a project from a stated commander's intent to completion with
minimal user involvement. Takes structured intent from the user at startup
(purpose, key tasks, end state, constraints, non-goals), then runs an OODA
loop — observing project state, orienting against intent, deciding what to
work on next, and acting by invoking other skills (`/scope`, `/implement`,
`/refactor`, `/review-*`, `/bug-*`, `/think-*`). The user acts as product
owner; the skill acts as project manager and tech lead.

Stops autonomously when mechanical end-state conditions are met and reviews
are clean, or pulls an andon cord when it hits a genuine blocker. Includes
periodic trajectory audits (every 10 cycles) and a capped run (50 cycles)
to prevent drift or thrash.

[Detailed documentation](skills/lead-project/references/README.md)

#### /implement-project — Full-Lifecycle Project Workflow

Orchestrates an entire project from tickets to release-ready code. Takes
batched tickets, implements each batch via `/implement-batch` in autonomous mode,
runs smoke tests, then executes a comprehensive quality pipeline (refactor,
review-arch, review-test, review-doc, review-release). The result is a
single project branch ready for human review and merge.

Maximizes autonomy — the andon cord (stop-the-line escalation) is the only
planned intervention path.

[Detailed documentation](skills/implement-project/SKILL.md)

#### /implement-batch — Multi-Ticket Orchestration

Takes a batch of tickets, plans their execution order, implements each
sequentially using `/implement` in autonomous mode, runs cross-cutting
quality passes (`/refactor`, `/review-doc`), and presents results for
final review.

[Detailed documentation](skills/implement-batch/SKILL.md)

#### /implement — Single-Ticket Development

Orchestrates a complete development cycle through specialist agents:
requirements → planning → implementation → QA → code review →
documentation. Detects project type and dispatches to language-specific
SMEs (Go, GraphQL, Docker, Makefile, Ansible, Zig, HTML, CSS,
JavaScript, TypeScript).

[Detailed documentation](skills/implement/SKILL.md)

### Planning

These workflows explore problem spaces and produce well-specified tickets
without doing implementation work.

#### /scope-project — Adversarial Project Planning

Plans an entire project through layered adversarial review loops.
Explores the problem space, drafts tickets organized into batches, then
runs a mandatory UX loop ("should we build this?"), zero or more
discretionary specialist loops (security, performance) for projects with
architectural implications in those domains, and a mandatory implementer
loop ("could we build this?") to find gaps, ambiguities, and missing
work. The architectural filter governs specialist loop invocation,
preventing checklist behavior on projects where the domain isn't
load-bearing. Locked elements (UX-locked, security-locked,
performance-locked) become hard constraints on downstream loops. Only
when every applicable loop signs off do tickets go upstream — already
tagged with batch labels ready for `/implement-project` to consume.

[Detailed documentation](skills/scope-project/SKILL.md)

#### /scope — Problem Space Exploration

Explores problem spaces through iterative dialogue and codebase analysis,
then creates a detailed ticket in your issue tracker. For single features,
bug investigations, or refactoring proposals.

[Detailed documentation](skills/scope/SKILL.md)

### Quality

These workflows improve code, tests, architecture, and documentation.
They run as part of `/implement-project`'s quality pipeline, but each works
standalone too.

#### /refactor — Iterative Code Quality Improvement

Autonomously scans for tactical improvements (DRY violations, dead code,
naming issues, unnecessary complexity), implements through specialist
agents with QA verification, and loops until no improvements remain. Works
within existing architecture — for structural changes, use `/review-arch`.

[Detailed documentation](skills/refactor/SKILL.md)

#### /review-arch — Advisory Architectural Analysis

Analyzes codebase architecture via noun analysis and produces a target
blueprint. **Advisory only** — does not implement changes. In interactive
standalone mode, collaborates with the user on the plan and offers to cut
tickets for the recommended work. In autonomous mode (invoked by an
orchestrator), produces a structured report with concrete next-step
recommendations. For module boundaries, responsibility overlap, utility
grab-bag dissolution, and structural rethinking.

[Detailed documentation](skills/review-arch/SKILL.md)

#### /review-test — Comprehensive Test Suite Review

Five-phase review: fills unit coverage gaps, surveys integration coverage,
surveys E2E (browser) coverage for webapps, identifies missing fuzz tests,
and audits test quality. Each phase has its own analysis → present →
select → implement → verify cycle. Phase 3 (E2E) cleanly skips when the
project is not a webapp; integration and E2E phases verify by compile-check
and prompt the user to run the suite ad-hoc rather than auto-running.

[Detailed documentation](skills/review-test/SKILL.md)

#### /test-mutation — Mutation Testing

Systematically introduces mutations into source code and checks if tests
catch them. Surviving mutations reveal genuine coverage gaps that line
coverage misses. Multi-session with progress tracking.

[Detailed documentation](skills/test-mutation/SKILL.md)

#### /review-doc — Documentation Quality Audit

Comprehensively reviews all project documentation for correctness,
completeness, and freshness. Fixes issues autonomously within its
authority.

[Detailed documentation](skills/review-doc/SKILL.md)

#### /review-release — Pre-Release Readiness Check

Pre-flight check before cutting a release. Scans for debug artifacts,
version mismatches, changelog gaps, git hygiene issues, breaking API
changes, and license compliance. Interactive — presents findings and lets
you decide what to fix.

[Detailed documentation](skills/review-release/SKILL.md)

#### /review-a11y — Accessibility Audit

Audits web content against WCAG 2.2 Level AA. Detects web content files
(HTML, JSX/TSX, Vue, Svelte, CSS, templates), dispatches accessibility
auditor agents to evaluate conformance, and produces a consolidated
report prioritized by real-world user impact. Advisory only — no
changes made.

[Detailed documentation](skills/review-a11y/SKILL.md)

#### /review-health — Strategic Orientation Review

First-pass strategic-orientation review of a repository. Use when you want
to step back and assess a repo strategically — inheriting a work project,
evaluating a FOSS library, revisiting your own repo, onboarding a
teammate. Produces an evidence-cited map (not a grade) calibrated to a
reference class, built to inform decisions about where to engage, where
to tread carefully, and where to leave alone. OODA-structured workflow
(Observe → Orient → Decide → Act) with per-class rubrics, ASHI severity
tiers on individual findings, and an explicit coverage manifest for
unavailable tooling. Advisory only — no changes made. Routes to sibling
specialists (`/review-arch`, `/refactor`, `/review-test`, etc.) when
findings warrant deeper follow-up.

[Detailed documentation](skills/review-health/SKILL.md)

#### /review-perf — Performance Review

Reviews a project for performance issues across two domains: compute
performance (algorithms, memory, CPU, benchmarking) and web performance
(caching, asset delivery, loading strategy, Core Web Vitals). Detects the
project type and dispatches the appropriate specialist(s) in parallel.
Advisory only — no changes made.

[Detailed documentation](skills/review-perf/SKILL.md)

#### /review-deep — Comprehensive Pre-Release Review Pipeline

Thin orchestrator that runs every `/review-*` skill in sequence:
`/review-health`, `/review-arch`, `/review-security`, `/review-perf`,
`/review-a11y`, `/review-test`, `/review-doc`, `/review-release`. Each
sub-skill keeps its normal interactive behavior — the operator
participates throughout. Auto-detects phases that don't apply (no web
content → skip `/review-a11y`; no tests → skip `/review-test`; etc.)
and asks for confirmation on the skip list before starting. Ends with
a consolidated report that synthesizes findings across all phases.

[Detailed documentation](skills/review-deep/SKILL.md)

### Security

#### /review-security — White-Box Security Audit

Orchestrates a comprehensive security assessment of the project's source code
using both defensive and offensive analysis. A blue-teamer evaluates the
defensive posture first, then red-teamers attack informed by the defensive
gaps. Dedicated red-teamers investigate each attack vector in depth. Findings
are synthesized, exploit chains are explored, and the process iterates until
no new chains emerge. Heavy and thorough by design.

[Detailed documentation](skills/review-security/SKILL.md)

### Decision and Diagnosis

The `/think-*` skills share a common design discipline — each is a structured countermeasure to a specific cognitive failure mode, sourced from a practitioner tradition (decision research, reflective practice, adversarial proceduralism, NGT, and others). See [THINK.md](THINK.md) for the family's design discipline, the five-test admission gate for new `/think-*` skills, and the intellectual lineage.

#### /think-reframe — Problem Redefinition Before Problem Solving

Pressure-tests how a problem is framed before anyone tries to solve it.
Extracts the premises embedded in the stated problem, then spawns
parallel reframers applying different lenses in isolation
(problem-vs-symptom, scope-shift, stakeholder-shift, level-of-abstraction,
time-horizon, inversion, category-shift, constraints-shift), and
synthesizes the alternatives into a report with a clear recommendation:
keep the original framing, adopt a specific reframing, or explore further.
Produces feedback only — no code, no tickets, no artifacts. Sits upstream
of `/think-brainstorm` in the natural pipeline.

[Detailed documentation](skills/think-reframe/SKILL.md)

#### /think-brainstorm — Divergent Idea Generation

Generates candidate approaches for a goal. Validates the assumptions
embedded in the goal, then spawns parallel brainstormers running
different techniques in isolation (first-principles, working-backwards,
lateral, analogical, constraints-shift, etc.), and synthesizes the pool
into a catalog of standouts, hybrid ideas, and reasonable alternatives.
Produces feedback only — no code, no tickets, no artifacts. Natural
handoff to `/think-deliberate` (choose) or `/think-scrutinize`
(stress-test).

[Detailed documentation](skills/think-brainstorm/SKILL.md)

#### /think-diagnose — Abductive Reasoning About Causes

Figures out *why* something is happening. Takes a phenomenon, separates
observations from interpretations, then spawns parallel diagnosticians
applying different reasoning lenses in isolation (technical,
human-factors, process, incentive-structure, environmental, temporal,
measurement-artifact, statistical). The orchestrator evaluates candidate
causes against evidence, calibrates confidence honestly (qualitative
categories — no fabricated percentages), and reports leading candidates
with distinguishing tests the user can run. Applicable to non-code
phenomena. Produces feedback only — no code, no tickets, no artifacts.

[Detailed documentation](skills/think-diagnose/SKILL.md)

#### /think-ach — Analysis of Competing Hypotheses

Systematically narrows among multiple hypotheses against evidence using
Richards Heuer's Analysis of Competing Hypotheses (ACH) — a CIA-tradition
technique designed to counter confirmation bias, premature closure,
anchoring, and cherry-picking. Spawns parallel hypothesizers in isolation
across angles (leading, alternative, adversarial, null, deceptive,
surprise) and parallel evidence-gatherers across classes
(direct-observational, documentary-historical, structural, behavioral,
absent, anomalous). Builds an explicit hypothesis-vs-evidence matrix.
**Ranks hypotheses by least disconfirming evidence**, not most confirming
— the central insight: hypotheses cannot be proven, only failed-to-be-
disproven. Includes diagnosticity analysis (which evidence actually
discriminates), sensitivity analysis (what if load-bearing evidence is
wrong?), and falsification milestones (what future observations would
distinguish the top candidates). Produces feedback only — no code, no
tickets, no artifacts. Natural composition: `/think-diagnose` generates
candidate causes, `/think-ach` rigorously narrows among them.

[Detailed documentation](skills/think-ach/SKILL.md)

#### /think-deliberate — Adversarial Decision Making

Uses adversarial representation to make decisions. Spawns advocate agents
for each option who argue their cases, rebut each other, and respond to
probing questions before a judge renders a verdict with reasoning and
trade-offs.

[Detailed documentation](skills/think-deliberate/SKILL.md)

#### /think-premortem — Prospective Failure Imagination

Treats a catastrophic failure as already-having-happened and reasons backward
to the causes. Operates in two modes: **plan mode** (a not-yet-committed plan;
imagine its catastrophic failure broadly across lenses) and **scenario mode**
(a specific catastrophic scenario posed against an existing system;
investigate the actual code and architecture for causes that could have
allowed it). Spawns parallel pre-mortemers in isolation across failure-class
lenses (technical, operational, estimation, scope, adoption,
dependency-and-environment, team-and-coordination, incentive, detection,
reversibility, adversarial). Synthesizes into a prioritized risk register
with early-warning signals the user can monitor for, calibrated qualitatively
(*high / moderate / low / uncertain*) rather than with fabricated percentages.
Produces feedback only — no code, no tickets, no artifacts. Sourced from
Klein's pre-mortem methodology and the *prospective hindsight* finding from
decision research.

[Detailed documentation](skills/think-premortem/SKILL.md)

#### /think-scrutinize — Devil's Advocate for Ideas

Stress-tests an idea or plan before you commit to implementing it. Spawns
critical skeptics from multiple angles (technical, economic,
operational, etc.), pairs them with an advocate defending the idea in
good faith, then synthesizes a report of faults that survived
cross-examination. Produces feedback only — no code, no tickets, no
artifacts.

[Detailed documentation](skills/think-scrutinize/SKILL.md)

#### /think-reflect — Retrospective Learning

Extracts learnings from a completed experience — a project that shipped,
an incident that resolved, a decision that played out. Gathers ground
truth (observations) separately from recollections (memory), actively
loads external sources (logs, timelines, notes, git history), then spawns
parallel reflectors applying different lenses in isolation
(what-worked-vs-got-lucky, what-didn't, what-surprised,
system-rewards-vs-intent, decisions-that-aged, what-to-tell-past-self,
patterns-that-recur). The headline output is **updated mental models** —
changed beliefs — not a findings document. Produces feedback only.

[Detailed documentation](skills/think-reflect/SKILL.md)

#### /bug-fix — Diagnosis-First Bug Fixing

Coordinates specialist agents through a diagnosis-first bug-fixing cycle:
reproduce with a failing test, perform root-cause analysis with git
archaeology, implement a targeted fix, and verify. Same review pipeline as
`/implement`.

[Detailed documentation](skills/bug-fix/SKILL.md)

#### /bug-hunt — Proactive Bug Discovery

Systematically hunts for bugs before they reach users. A risk assessor
cross-references code complexity, test coverage gaps, and structural risk
factors to produce a ranked hotspot list. Dedicated hunters then
deep-dive into each hotspot, writing reproducing tests to validate or
invalidate suspected bugs. Every confirmed finding is backed by a
reproducing test — no speculative reports. Optionally routes confirmed
bugs to SME agents for fixing.

[Detailed documentation](skills/bug-hunt/SKILL.md)

### Utility

#### /pre-compact — Pre-Compaction Housekeeping

Run this immediately before `/compact`. Compaction destroys
conversation context, so anything important from the session that
isn't persisted somewhere durable is lost. Walks a fixed checklist
as a floor — update persistent memory, audit `git status` and
optionally commit (with permission), clean up trash files
conservatively — then uses judgment to spot session-specific
cleanup the checklist can't anticipate (open threads, undocumented
decisions, background processes, stashes). Ends with an
SBAR-formatted handoff with one of three explicit recommendations
(**safe to compact**, **safe after [X]**, or **do not compact
yet**), plus a copy-pasteable resume prompt the user can paste into
the next turn if pending work remains. Does not invoke `/compact`
itself.

[Detailed documentation](skills/pre-compact/SKILL.md)

## Agents

Specialist agents spawned by the workflows above:

| Agent                          | Purpose                                                                                                    |
|--------------------------------|------------------------------------------------------------------------------------------------------------|
| `thk-ach-evidence-gatherer`    | Good-faith evidence enumerator for ACH proceedings, parameterized by an evidence class                     |
| `thk-ach-hypothesizer`         | Good-faith hypothesis generator for ACH proceedings, parameterized by a hypothesis-generation angle        |
| `thk-advocate`                 | Argues for an assigned position in adversarial proceedings                                                 |
| `thk-brainstormer`             | Good-faith idea generator parameterized by a specific brainstorming technique                              |
| `thk-diagnostician`            | Good-faith abductive reasoner that generates candidate causes through an assigned reasoning lens           |
| `thk-premortemer`              | Good-faith failure imaginer that uses prospective hindsight to identify causes through an assigned failure-class lens |
| `thk-reflector`                | Good-faith reflector that extracts learnings from an experience through an assigned reflection lens        |
| `thk-reframer`                 | Good-faith reframer that restates a problem through an assigned reframing lens                             |
| `thk-skeptic`                  | Good-faith skeptic that identifies faults in an idea through an assigned critical lens                     |
| `swe-planner`                  | Decomposes complex tasks into implementation plans                                                         |
| `swe-sme-golang`               | Go implementation specialist                                                                               |
| `swe-sme-graphql`              | GraphQL schema and resolver specialist                                                                     |
| `swe-sme-docker`               | Dockerfile and container specialist                                                                        |
| `swe-sme-makefile`             | Makefile and build system specialist                                                                       |
| `swe-sme-ansible`              | Ansible automation specialist                                                                              |
| `swe-sme-zig`                  | Zig implementation specialist                                                                              |
| `swe-sme-html`                 | HTML structure, semantics, and accessibility specialist                                                    |
| `swe-sme-css`                  | CSS styling, layout, and responsive design specialist                                                      |
| `swe-sme-javascript`           | Vanilla JavaScript implementation specialist                                                               |
| `swe-sme-typescript`           | TypeScript implementation and type design specialist                                                       |
| `swe-code-reviewer`            | Tactical code quality reviewer (DRY, dead code, naming, complexity)                                        |
| `swe-arch-reviewer`            | Architecture reviewer (noun analysis, module boundaries, blueprints)                                       |
| `swe-bug-assessor`             | Codebase risk assessor (complexity, coverage, structural risk, git churn — produces ranked hotspot list)   |
| `swe-bug-hunter`               | Focused bug investigator (deep-dives hotspots, writes reproducing tests, validates findings)               |
| `swe-bug-investigator`         | Bug root-cause investigator (execution tracing, git archaeology, diagnosis reports)                        |
| `swe-perf-reviewer`            | Compute performance reviewer (algorithmic complexity, benchmarking, profiling, optimization)               |
| `swe-web-perf-reviewer`        | Web performance reviewer (caching, asset delivery, loading strategy, Core Web Vitals)                      |
| `qa-engineer`                  | Practical verification and test coverage                                                                   |
| `qa-web-a11y-reviewer`         | WCAG accessibility reviewer (keyboard navigation, ARIA, contrast, semantic structure)                      |
| `qa-test-reviewer`             | Test quality reviewer (brittle, tautological, useless tests)                                               |
| `qa-test-coverage-reviewer`    | Coverage gap reviewer (coverage reports, risk prioritization, testability suggestions)                     |
| `qa-test-integration-reviewer` | Integration test gap reviewer (seam survey, Mode A starter strategy, Mode B gaps and strategy expansion)   |
| `qa-test-e2e-reviewer`         | E2E browser test gap reviewer (webapp detection, journey classification, Playwright-prescriptive Mode A)   |
| `qa-test-fuzz-reviewer`        | Fuzz testing gap reviewer (fuzz infrastructure detection, candidate identification)                        |
| `qa-test-mutator`              | Mutation testing worker (applies mutations, records results)                                               |
| `qa-release-engineer`          | Pre-release scanner (debug artifacts, versioning, changelog, git hygiene, breaking changes, licenses)      |
| `sec-blue-teamer`              | Defensive security analyst (control inventory, consistency, defense-in-depth, configuration)               |
| `sec-red-teamer`               | Adversarial security analyst (attack surface mapping, exploitation, trust boundary analysis)               |
| `ux-reviewer`                  | Methodical UX advocate for `/scope-project`'s pre-implementation review loop (seven-concern spine, target-type detection) |
| `doc-maintainer`               | Documentation updates and verification                                                                     |

## Development

See [HACKING.md](HACKING.md) for local development and testing instructions. See [CHANGELOG.md](CHANGELOG.md) for release history and [CONTRIBUTING.md](CONTRIBUTING.md) for contribution policy.

## Versioning

This project follows [Semantic Versioning](https://semver.org/). Skills (slash commands like `/implement`, `/review-perf`, etc.) are the public interface. Subagent names are internal implementation details and may be renamed or restructured without constituting a breaking change.

## Requirements

- `git` repository
- For ticket creation: integration with your issue tracker (CLI, MCP server, or API)

[cc]: https://claude.ai/code
