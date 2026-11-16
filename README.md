# claude-swe-workflows

A system of composable software engineering workflows for [Claude Code][cc].
Plan projects, implement tickets, and run quality passes — from a single
ticket to a multi-batch project, using the same layered architecture.

## Installation

```bash
claude plugin marketplace add https://github.com/chrisallenlane/claude-swe-workflows.git
claude plugin install claude-swe-workflows@claude-swe-workflows
```

## Layered Composition

The skills are arranged as **layered composition** — higher-level skills invoke
lower-level ones. Enter at the layer that matches your task. The deepest stack:

```
/implement                                 ← one ticket, a batch, or an open-ended goal
└── implementer and reviewers, chosen by   ← QA, correctness, security,
    judgment over a fixed floor              /refactor, /review-*, …
```

Two other entry points can run autonomously, given authority up front:

- `/bug-hunt` — hunts until a round confirms nothing above a severity floor; with authority, tickets the bugs and fixes them via `/implement` between rounds.
- `/review-repo` — maps the repository; with authority, runs the deeper reviews the map calls for and tickets their findings.

Planning feeds implementation: `/scope` → `/implement`. Supporting skills (`/think-*`, `/review-*`, `/bug-*`,
`/tidy-*`) compose into any of the orchestrators above or run standalone.

## Namespaces

Skills are grouped by namespace for discoverability. Each namespace gathers
skills with a related purpose.

| Namespace    | Purpose                                     | Skills                                                                                                                                                 |
|--------------|---------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| `/implement` | Implement tickets (mutate the working tree) | `/implement`                                                                                                                                           |
| `/scope`     | Plan and produce tickets                    | `/scope`                                                                                                                                               |
| `/review-*`  | Advisory audits — no code changes           | `/review-repo`, `/review-test`, `/review-perf`, `/review-a11y`, `/review-security`, `/review-release`                                                  |
| `/think-*`   | Reasoning support — no artifacts            | `/think-reframe`, `/think-brainstorm`, `/think-diagnose`, `/think-ach`, `/think-deliberate`, `/think-premortem`, `/think-scrutinize`, `/think-reflect` |
| `/tidy-*`    | Mechanical hygiene                          | `/tidy-docs`, `/tidy-git`                                                                                                                              |
| `/bug-*`     | Find and fix bugs                           | `/bug-fix`, `/bug-hunt`                                                                                                                                |
| `/test-*`    | Test-quality work                           | `/test-mutation`                                                                                                                                       |
| (standalone) | Skills that don't share a namespace         | `/refactor`, `/pre-compact`, `/release`                                                                                                                |

The skills that act on granted authority — `/implement`, `/bug-hunt`, and
`/review-repo` — additionally share an autonomy discipline (commander's
intent, pre-loaded options, pre-rebutted recommendations, risk budgets) — see
[references/autonomy.md](references/autonomy.md). The `/think-*` namespace
shares a design discipline (practitioner-sourced countermeasures to specific
cognitive failure modes) — see [references/think.md](references/think.md).

## Choosing a Workflow

Not everything needs the full pipeline. Enter at the level that matches your
task:

| You want to...                                                                              | Use                         |
|---------------------------------------------------------------------------------------------|-----------------------------|
| Implement a ticket, a batch of tickets, or an open-ended goal                               | `/implement`                |
| Plan work and create tickets — one, or a whole project's worth                              | `/scope`                    |
| Fix a bug with diagnosis and root-cause analysis                                            | `/bug-fix`                  |
| Hunt for bugs — report, ticket, or fix them until a severity floor is met                   | `/bug-hunt`                 |
| Pressure-test a problem's framing before solving it                                         | `/think-reframe`            |
| Brainstorm approaches to a goal                                                             | `/think-brainstorm`         |
| Reason about why a phenomenon is happening                                                  | `/think-diagnose`           |
| Narrow among competing hypotheses against evidence                                          | `/think-ach`                |
| Make a hard decision with adversarial deliberation                                          | `/think-deliberate`         |
| Imagine how a plan could fail, or how a hypothetical catastrophe could hit a running system | `/think-premortem`          |
| Scrutinize an idea or plan before committing to it                                          | `/think-scrutinize`         |
| Reflect on a completed experience to update beliefs                                         | `/think-reflect`            |
| Shrink a codebase: strip and redesign it with behavior pinned                               | `/refactor`                 |
| Rethink module boundaries and architecture                                                  | `/review-repo architecture` |
| Price the requirements and propose behavior-for-simplicity trades                           | `/review-repo value`        |
| Audit for dead code without removing it                                                     | `/review-repo dead-code`    |
| Measure how legibly the file tree communicates (and optionally optimize it)                 | `/review-repo namespace`    |
| Survey the test suite and surface gaps as tickets                                           | `/review-test`              |
| Verify test quality via mutation testing                                                    | `/test-mutation`            |
| Tidy all project documentation                                                              | `/tidy-docs`                |
| Pre-release readiness check                                                                 | `/review-release`           |
| Cut a versioned release (preflight + plan + execute)                                        | `/release`                  |
| Audit web content for accessibility barriers                                                | `/review-a11y`              |
| Orient on a repo — or review every dimension, with authority to run the specialists         | `/review-repo`              |
| Find where technical debt is costing you (and where to aim `/refactor`)                     | `/review-repo`              |
| Review performance (compute and/or web)                                                     | `/review-perf`              |
| Perform a white-box security audit                                                          | `/review-security`          |
| Tidy up the session before running `/compact`                                               | `/pre-compact`              |
| Clean up local git state (stale refs, merged branches)                                      | `/tidy-git`                 |

**Rules of thumb:**
- Tickets to build, one or many, or a goal to reach? `/implement` (or `/bug-fix` for a single bug that needs diagnosis)
- Not sure what to build yet? Start with `/scope`

## Skills

One-line summaries grouped by namespace. Click through to each skill's detailed README.

### `/implement` — Working-tree mutator

- **`/implement`** — Implements one ticket, a batch of tickets, or an open-ended goal, end to end. Chooses by judgment which specialists and skills the work needs (planning, delegated implementation, security and performance reviews, `/refactor`, `/review-repo architecture`, `/bug-hunt`, …) over a fixed floor: concept inventory before code, practical verification of acceptance criteria, tests green at every commit, an independent correctness review, and no irreversible actions. One planned interaction, then autonomous; every pass not run is accounted for in the report. ([details](skills/implement/references/README.md))

### `/scope` — Planning

- **`/scope`** — Explores a problem space with you and turns it into well-specified tickets — one, or a whole project's worth. Chooses which reviewers the drafts need (implementer, UX, security, performance); every draft gets a fresh-context review, and nothing is created without your approval. ([details](skills/scope/references/README.md))

### `/review-*` — Read-only audits

All `/review-*` skills are advisory — they audit and propose, never mutate.

- **`/review-test`** — Five-phase test-suite survey: unit, integration, E2E (browser, webapps only), fuzz, test quality. Proposes a ticket structure for gaps. ([details](skills/review-test/SKILL.md))
- **`/review-perf`** — Performance review across compute (hot paths costed at their actual scale) and web (caching, asset delivery, Core Web Vitals) domains. ([details](skills/review-perf/SKILL.md))
- **`/review-a11y`** — WCAG 2.2 Level AA audit of detected web content. ([details](skills/review-a11y/SKILL.md))
- **`/review-repo`** — The entry point for reviewing a codebase as a whole. With no focus: an evidence-cited map, not a grade, calibrated to the repo's reference class — useful when inheriting a project, evaluating a library, or revisiting your own repo; it locates technical debt by the interest it charges (complexity hotspots that keep changing, files coupled only by change history) and recommends where to aim `/refactor`. With a focus, straight to a deep review: `architecture` (noun-analysis blueprint), `dead-code` (calibrated audit with confidence tiers), `value` (a trade menu of requirement relaxations that dissolve disproportionate machinery), or `namespace` (cold readers who see only the file listing answer navigation questions against verified ground truth, and their misses become findings; an optional heavy search mode evolves a better tree). Given authority, the map runs the deeper reviews it calls for, consolidates them, and creates tickets. Never changes code. ([details](skills/review-repo/SKILL.md))
- **`/review-security`** — White-box security audit. Blue-teamer evaluates defensive posture first; red-teamers then attack informed by the gaps. Iterates until no new exploit chains emerge. ([details](skills/review-security/SKILL.md))
- **`/review-release`** — Pre-release readiness check: debug artifacts, version mismatches, changelog gaps, git hygiene, breaking changes, license compliance. ([details](skills/review-release/SKILL.md))

### `/think-*` — Reasoning

All `/think-*` skills produce feedback only — no code, no tickets, no artifacts. See [references/think.md](references/think.md) for the namespace's design discipline.

- **`/think-reframe`** — Pressure-tests problem framing before solving. Parallel reframers across lenses (problem-vs-symptom, scope-shift, inversion, etc.). ([details](skills/think-reframe/SKILL.md))
- **`/think-brainstorm`** — Divergent idea generation across techniques (first-principles, working-backwards, lateral, analogical, etc.). ([details](skills/think-brainstorm/SKILL.md))
- **`/think-diagnose`** — Abductive reasoning about why a phenomenon is happening. Diagnosticians across lenses (technical, human-factors, process, etc.). ([details](skills/think-diagnose/SKILL.md))
- **`/think-ach`** — Analysis of Competing Hypotheses (Heuer). Builds a hypothesis-vs-evidence matrix; ranks by least disconfirming evidence. ([details](skills/think-ach/SKILL.md))
- **`/think-deliberate`** — Adversarial decision-making. Advocates argue and rebut before a judge renders a verdict. ([details](skills/think-deliberate/SKILL.md))
- **`/think-premortem`** — Treats catastrophic failure as already-happened and reasons backward to causes. Plan mode (not-yet-committed plan) or scenario mode (running system). ([details](skills/think-premortem/SKILL.md))
- **`/think-scrutinize`** — Stress-tests an idea before commitment. Skeptics across angles paired with an advocate; reports faults that survive cross-examination. ([details](skills/think-scrutinize/SKILL.md))
- **`/think-reflect`** — Retrospective learning. Updated mental models from a completed experience; observations and recollections gathered separately. ([details](skills/think-reflect/SKILL.md))

### `/bug-*` — Bug work

- **`/bug-fix`** — Diagnosis-first bug fix: reproduce with a failing test, root-cause via git archaeology, targeted fix, verify. Mutates. ([details](skills/bug-fix/SKILL.md))
- **`/bug-hunt`** — Proactive bug discovery. Risk-ranks hotspots and deep-dives each with reproducing tests, round after round until nothing is confirmed above a severity floor. Advisory by default — proposes tickets for confirmed findings; with authority in its commander's intent, creates tickets and fixes via `/implement`. ([details](skills/bug-hunt/references/README.md))

### `/tidy-*` — Mechanical hygiene

- **`/tidy-docs`** — Documentation audit and repair via the `doc-maintainer` agent. Fixes within agent authority; surfaces judgment calls. ([details](skills/tidy-docs/SKILL.md))
- **`/tidy-git`** — Local repo hygiene: prunes stale refs, deletes merged branches (with preview), reports stashes/untracked/unpushed. Never touches the remote. ([details](skills/tidy-git/SKILL.md))

### `/test-*` — Testing utilities

- **`/test-mutation`** — Mutation testing. Introduces mutations, then writes tests to catch survivors — revealing coverage gaps that line coverage misses. Multi-session via a state file. ([details](skills/test-mutation/SKILL.md))

### Standalone

- **`/refactor`** — Redesigns a codebase with reduction as the goal: question the requirements, delete the part, simplify what survives. One interactive requirements menu, then autonomous. Behavior is pinned by running the original implementation as a differential oracle at the user-visible boundary, not by the existing test suite; each pass strips what can be removed and regenerates the rest from a blind designer, and candidates are adopted by mechanical gates (behavior, correctness, structure). Works on an isolated `refactor/<slug>` branch; merging is your call. For an advisory structural blueprint, use `/review-repo architecture`. Mutates (on its own branch). ([details](skills/refactor/references/README.md))
- **`/pre-compact`** — Pre-compaction housekeeping: persist memory, audit git, clean trash, end with SBAR + resume prompt. Does not invoke `/compact`. ([details](skills/pre-compact/SKILL.md))
- **`/release`** — Cuts a project release. Discovers the release procedure, invokes `/review-release` as preflight, plans every step with reversibility annotations, executes step-by-step, halts on first failure. No skip-preflight or force-release flag. ([details](skills/release/references/README.md))

## Versioning

This project follows [Semantic Versioning](https://semver.org/). Skills (slash commands like `/implement`, `/review-perf`, etc.) are the public interface. Subagent names are internal implementation details and may be renamed or restructured without constituting a breaking change.

## Requirements

- `git` repository
- For ticket creation: integration with your issue tracker (CLI, MCP server, or API)

[cc]: https://claude.ai/code
