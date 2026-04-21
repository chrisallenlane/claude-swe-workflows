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
├── /review-arch                      ← architectural restructuring
├── /refactor (conditional)           ← post-restructuring cleanup
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

Supporting workflows are available at any level for reasoning and
diagnosis: `/think-reframe` (problem redefinition), `/think-brainstorm`
(divergent idea generation), `/think-diagnose` (abductive reasoning
about causes), `/think-deliberate` (adversarial decision-making),
`/think-scrutinize` (adversarial idea critique), `/think-reflect`
(retrospective learning), `/bug-fix` (diagnosis-first bug fixing),
`/bug-hunt` (proactive bug discovery), `/test-mutation` (mutation
testing), and `/refactor-deep` (full tactical + architectural + tactical
refactoring cycle).

## Choosing a Workflow

Not everything needs the full pipeline. Enter at the level that matches
your task:

| You want to...                                          | Use                  |
|---------------------------------------------------------|----------------------|
| Implement an entire multi-batch project autonomously    | `/implement-project` |
| Implement a batch of related tickets                    | `/implement-batch`   |
| Implement a single ticket or feature                    | `/implement`         |
| Plan a multi-batch project with adversarial review      | `/scope-project`     |
| Plan a single feature and create a ticket               | `/scope`             |
| Fix a bug with diagnosis and root-cause analysis        | `/bug-fix`           |
| Proactively hunt for bugs before they're reported       | `/bug-hunt`          |
| Pressure-test a problem's framing before solving it     | `/think-reframe`     |
| Brainstorm approaches to a goal                         | `/think-brainstorm`  |
| Reason about why a phenomenon is happening              | `/think-diagnose`    |
| Make a hard decision with adversarial deliberation      | `/think-deliberate`  |
| Scrutinize an idea or plan before committing to it      | `/think-scrutinize`  |
| Reflect on a completed experience to update beliefs     | `/think-reflect`     |
| Clean up code quality (DRY, dead code, naming)          | `/refactor`          |
| Rethink module boundaries and architecture              | `/review-arch`       |
| Review and strengthen the test suite                    | `/review-test`       |
| Verify test quality via mutation testing                | `/test-mutation`     |
| Audit all project documentation                         | `/review-doc`        |
| Pre-release readiness check                             | `/review-release`    |
| Audit web content for accessibility barriers            | `/review-a11y`       |
| Assess code health across all project languages         | `/review-health`     |
| Review performance (compute and/or web)                 | `/review-perf`       |
| Perform a white-box security audit                      | `/review-security`   |

**Rules of thumb:**
- Multiple batches of tickets forming a project? `/implement-project`
- One batch of 2+ related tickets? `/implement-batch`
- One ticket? `/implement` (or `/bug-fix` if it's a bug)
- Not sure what to build yet? Start with `/scope` or `/scope-project`

## Skills

### Orchestration

These workflows manage the lifecycle of tickets — from implementation
through quality passes to a merge-ready branch.

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

Plans an entire project through adversarial review. Explores the problem
space, drafts tickets organized into batches, then pits a planner against
an implementer agent to find gaps, ambiguities, and missing work. Only
when the implementer is satisfied do tickets go upstream — already tagged
with batch labels ready for `/implement-project` to consume.

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

#### /review-arch — Blueprint-Driven Architectural Improvement

Analyzes codebase architecture via noun analysis, produces a target
blueprint, then collaborates with the user to decide what to implement.
For module boundaries, responsibility overlap, utility grab-bag
dissolution, and structural rethinking.

[Detailed documentation](skills/review-arch/SKILL.md)

#### /review-test — Comprehensive Test Suite Review

Three-phase review: fills coverage gaps, identifies missing fuzz tests,
and audits test quality. Each phase has its own analysis → present →
select → implement → verify cycle.

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

#### /review-health — Code Health Assessment

Assesses source code health across all languages in the project. Detects
languages, dispatches SME agents for specialist review (or generalists for
unsupported languages), and produces a consolidated health report with
per-language ratings. Advisory only — no changes made. Use to decide
whether `/refactor` is needed.

[Detailed documentation](skills/review-health/SKILL.md)

#### /review-perf — Performance Review

Reviews a project for performance issues across two domains: compute
performance (algorithms, memory, CPU, benchmarking) and web performance
(caching, asset delivery, loading strategy, Core Web Vitals). Detects the
project type and dispatches the appropriate specialist(s) in parallel.
Advisory only — no changes made.

[Detailed documentation](skills/review-perf/SKILL.md)

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

#### /think-deliberate — Adversarial Decision Making

Uses adversarial representation to make decisions. Spawns advocate agents
for each option who argue their cases, rebut each other, and respond to
probing questions before a judge renders a verdict with reasoning and
trade-offs.

[Detailed documentation](skills/think-deliberate/SKILL.md)

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

## Agents

Specialist agents spawned by the workflows above:

| Agent                       | Purpose                                                                                                    |
|-----------------------------|------------------------------------------------------------------------------------------------------------|
| `thk-advocate`              | Argues for an assigned position in adversarial proceedings                                                 |
| `thk-brainstormer`          | Good-faith idea generator parameterized by a specific brainstorming technique                              |
| `thk-diagnostician`         | Good-faith abductive reasoner that generates candidate causes through an assigned reasoning lens           |
| `thk-reflector`             | Good-faith reflector that extracts learnings from an experience through an assigned reflection lens        |
| `thk-reframer`              | Good-faith reframer that restates a problem through an assigned reframing lens                             |
| `thk-skeptic`               | Good-faith skeptic that identifies faults in an idea through an assigned critical lens                     |
| `swe-planner`               | Decomposes complex tasks into implementation plans                                                         |
| `swe-sme-golang`            | Go implementation specialist                                                                               |
| `swe-sme-graphql`           | GraphQL schema and resolver specialist                                                                     |
| `swe-sme-docker`            | Dockerfile and container specialist                                                                        |
| `swe-sme-makefile`          | Makefile and build system specialist                                                                       |
| `swe-sme-ansible`           | Ansible automation specialist                                                                              |
| `swe-sme-zig`               | Zig implementation specialist                                                                              |
| `swe-sme-html`              | HTML structure, semantics, and accessibility specialist                                                    |
| `swe-sme-css`               | CSS styling, layout, and responsive design specialist                                                      |
| `swe-sme-javascript`        | Vanilla JavaScript implementation specialist                                                               |
| `swe-sme-typescript`        | TypeScript implementation and type design specialist                                                       |
| `swe-code-reviewer`         | Tactical code quality reviewer (DRY, dead code, naming, complexity)                                        |
| `swe-arch-reviewer`         | Architecture reviewer (noun analysis, module boundaries, blueprints)                                       |
| `swe-bug-assessor`          | Codebase risk assessor (complexity, coverage, structural risk, git churn — produces ranked hotspot list)   |
| `swe-bug-hunter`            | Focused bug investigator (deep-dives hotspots, writes reproducing tests, validates findings)                |
| `swe-bug-investigator`      | Bug root-cause investigator (execution tracing, git archaeology, diagnosis reports)                        |
| `swe-perf-reviewer`         | Compute performance reviewer (algorithmic complexity, benchmarking, profiling, optimization)                |
| `swe-web-perf-reviewer`     | Web performance reviewer (caching, asset delivery, loading strategy, Core Web Vitals)                      |
| `qa-engineer`               | Practical verification and test coverage                                                                   |
| `qa-web-a11y-reviewer`      | WCAG accessibility reviewer (keyboard navigation, ARIA, contrast, semantic structure)                      |
| `qa-test-reviewer`          | Test quality reviewer (brittle, tautological, useless tests)                                               |
| `qa-test-coverage-reviewer` | Coverage gap reviewer (coverage reports, risk prioritization, testability suggestions)                     |
| `qa-test-fuzz-reviewer`     | Fuzz testing gap reviewer (fuzz infrastructure detection, candidate identification)                        |
| `qa-test-mutator`           | Mutation testing worker (applies mutations, records results)                                               |
| `qa-release-engineer`       | Pre-release scanner (debug artifacts, versioning, changelog, git hygiene, breaking changes, licenses)      |
| `sec-blue-teamer`           | Defensive security analyst (control inventory, consistency, defense-in-depth, configuration)               |
| `sec-red-teamer`            | Adversarial security analyst (attack surface mapping, exploitation, trust boundary analysis)               |
| `doc-maintainer`            | Documentation updates and verification                                                                     |

## Development

See [HACKING.md](HACKING.md) for local development and testing instructions. See [CHANGELOG.md](CHANGELOG.md) for release history and [CONTRIBUTING.md](CONTRIBUTING.md) for contribution policy.

## Versioning

This project follows [Semantic Versioning](https://semver.org/). Skills (slash commands like `/implement`, `/review-perf`, etc.) are the public interface. Subagent names are internal implementation details and may be renamed or restructured without constituting a breaking change.

## Requirements

- `git` repository
- For ticket creation: integration with your issue tracker (CLI, MCP server, or API)

[cc]: https://claude.ai/code
