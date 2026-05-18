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
/lead-project                              ← autonomous tech lead (decides what to do next)
└── invokes any skill below
    /implement-project                     ← full-lifecycle project execution
    └── /implement-batch                   ← one batch of related tickets
        └── /implement                     ← one ticket, end-to-end
            └── SME agents                 ← language-specific specialists
```

Three other entry points orchestrate bounded autonomous loops:

- `/lead-bug-hunt` — loops `/bug-hunt` → `/implement-batch` until bugs converge below a severity floor.
- `/lead-refactor` — `/refactor` → loops `/review-arch` + `/implement-batch` → `/refactor`.
- `/lead-review` — runs every `/review-*` sub-skill once.

Planning feeds implementation: `/scope-project` → `/implement-project`, or
`/scope` → `/implement`. Supporting skills (`/think-*`, `/review-*`, `/bug-*`,
`/tidy-*`) compose into any of the orchestrators above or run standalone.

## Namespaces

Skills are grouped by namespace for discoverability. Each namespace gathers
skills with a related purpose.

| Namespace      | Purpose                                     | Skills                                                                                                                                                 |
|----------------|---------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| `/lead-*`      | Autonomous orchestrators                    | `/lead-project`, `/lead-bug-hunt`, `/lead-refactor`, `/lead-review`                                                                                    |
| `/implement-*` | Implement tickets (mutate the working tree) | `/implement`, `/implement-batch`, `/implement-project`                                                                                                 |
| `/scope-*`     | Plan and produce tickets                    | `/scope`, `/scope-project`                                                                                                                             |
| `/review-*`    | Advisory audits — no code changes           | `/review-arch`, `/review-test`, `/review-perf`, `/review-a11y`, `/review-health`, `/review-security`, `/review-release`                                |
| `/think-*`     | Reasoning support — no artifacts            | `/think-reframe`, `/think-brainstorm`, `/think-diagnose`, `/think-ach`, `/think-deliberate`, `/think-premortem`, `/think-scrutinize`, `/think-reflect` |
| `/tidy-*`      | Mechanical hygiene                          | `/tidy-docs`, `/tidy-git`                                                                                                                              |
| `/bug-*`       | Find and fix bugs                           | `/bug-fix`, `/bug-hunt`                                                                                                                                |
| `/test-*`      | Test-quality work                           | `/test-mutation`                                                                                                                                       |
| (standalone)   | Skills that don't share a namespace         | `/refactor`, `/pre-compact`, `/release`                                                                                                                |

The `/lead-*` and `/implement-*` namespaces additionally share an autonomy
discipline (commander's intent, pre-loaded options, pre-rebutted
recommendations, risk budgets) — see
[references/autonomy.md](references/autonomy.md). The `/think-*` namespace
shares a design discipline (practitioner-sourced countermeasures to specific
cognitive failure modes) — see [references/think.md](references/think.md).

## Choosing a Workflow

Not everything needs the full pipeline. Enter at the level that matches your
task:

| You want to...                                                                              | Use                  |
|---------------------------------------------------------------------------------------------|----------------------|
| Drive a project to completion autonomously, deciding what to work on                        | `/lead-project`      |
| Implement an entire multi-batch project autonomously                                        | `/implement-project` |
| Implement a batch of related tickets                                                        | `/implement-batch`   |
| Implement a single ticket or feature                                                        | `/implement`         |
| Plan a multi-batch project with adversarial review                                          | `/scope-project`     |
| Plan a single feature and create a ticket                                                   | `/scope`             |
| Fix a bug with diagnosis and root-cause analysis                                            | `/bug-fix`           |
| Proactively hunt for bugs before they're reported                                           | `/bug-hunt`          |
| Iterate hunt → fix until bugs converge below a severity floor (autonomous)                  | `/lead-bug-hunt`     |
| Comprehensively refactor (tactical + architectural + tactical, autonomous)                  | `/lead-refactor`     |
| Pressure-test a problem's framing before solving it                                         | `/think-reframe`     |
| Brainstorm approaches to a goal                                                             | `/think-brainstorm`  |
| Reason about why a phenomenon is happening                                                  | `/think-diagnose`    |
| Narrow among competing hypotheses against evidence                                          | `/think-ach`         |
| Make a hard decision with adversarial deliberation                                          | `/think-deliberate`  |
| Imagine how a plan could fail, or how a hypothetical catastrophe could hit a running system | `/think-premortem`   |
| Scrutinize an idea or plan before committing to it                                          | `/think-scrutinize`  |
| Reflect on a completed experience to update beliefs                                         | `/think-reflect`     |
| Clean up code quality (DRY, dead code, naming)                                              | `/refactor`          |
| Rethink module boundaries and architecture                                                  | `/review-arch`       |
| Survey the test suite and surface gaps as tickets                                           | `/review-test`       |
| Verify test quality via mutation testing                                                    | `/test-mutation`     |
| Tidy all project documentation                                                              | `/tidy-docs`         |
| Pre-release readiness check                                                                 | `/review-release`    |
| Cut a versioned release (preflight + plan + execute)                                        | `/release`           |
| Audit web content for accessibility barriers                                                | `/review-a11y`       |
| First-pass strategic orientation on a repo                                                  | `/review-health`     |
| Review performance (compute and/or web)                                                     | `/review-perf`       |
| Perform a white-box security audit                                                          | `/review-security`   |
| Run every review dimension autonomously (with optional backlog creation)                    | `/lead-review`       |
| Tidy up the session before running `/compact`                                               | `/pre-compact`       |
| Clean up local git state (stale refs, merged branches)                                      | `/tidy-git`          |

**Rules of thumb:**
- Open-ended work where the next step depends on the outcome of the last? `/lead-project`
- Multiple batches of tickets forming a project? `/implement-project`
- One batch of 2+ related tickets? `/implement-batch`
- One ticket? `/implement` (or `/bug-fix` if it's a bug)
- Not sure what to build yet? Start with `/scope` or `/scope-project`

## Skills

One-line summaries grouped by namespace. Click through to each skill's detailed README.

### `/lead-*` — Autonomous orchestrators

- **`/lead-project`** — Autonomous tech lead. Runs an OODA loop over project state given a commander's intent, invoking lower-level skills until end-state is met or it pulls an andon cord. ([details](skills/lead-project/references/README.md))
- **`/lead-bug-hunt`** — Loops `/bug-hunt` → `/implement-batch` until bugs converge below a stated severity floor; runs `/review-test` on the new reproducing tests at termination. ([details](skills/lead-bug-hunt/references/README.md))
- **`/lead-refactor`** — Three-phase comprehensive refactoring: tactical `/refactor` → loop of `/review-arch` + `/implement-batch` until convergence → final tactical `/refactor`. ([details](skills/lead-refactor/references/README.md))
- **`/lead-review`** — Runs every `/review-*` sub-skill autonomously with an operator-set toggle for whether sub-skill ticket proposals are written to the tracker. ([details](skills/lead-review/references/README.md))

### `/implement-*` — Working-tree mutators

- **`/implement-project`** — Full-lifecycle project execution. Implements batched tickets, runs the quality pipeline (refactor, review-arch, review-test, tidy-docs, review-release), produces a review-ready branch. ([details](skills/implement-project/SKILL.md))
- **`/implement-batch`** — Plans execution order of a batch of tickets, implements each via `/implement` autonomously, runs cross-cutting `/refactor` and `/tidy-docs` passes. ([details](skills/implement-batch/SKILL.md))
- **`/implement`** — Single-ticket development cycle: requirements → planning → implementation → QA → code review → documentation. Dispatches to language SMEs. ([details](skills/implement/SKILL.md))

### `/scope-*` — Planning

- **`/scope-project`** — Plans a multi-batch project through layered adversarial review loops (UX, optional security/performance, implementer). Produces batch-tagged tickets ready for `/implement-project`. ([details](skills/scope-project/SKILL.md))
- **`/scope`** — Iterative problem-space exploration that produces a single detailed ticket. For one feature, bug, or refactor proposal. ([details](skills/scope/SKILL.md))

### `/review-*` — Read-only audits

All `/review-*` skills are advisory — they audit and propose, never mutate.

- **`/review-arch`** — Architectural analysis via noun analysis; produces a target blueprint and proposes tickets for the recommended work. ([details](skills/review-arch/SKILL.md))
- **`/review-test`** — Five-phase test-suite survey: unit, integration, E2E (browser, webapps only), fuzz, test quality. Proposes a ticket structure for gaps. ([details](skills/review-test/SKILL.md))
- **`/review-perf`** — Performance review across compute (algorithms, profiling) and web (caching, asset delivery, Core Web Vitals) domains. ([details](skills/review-perf/SKILL.md))
- **`/review-a11y`** — WCAG 2.2 Level AA audit of detected web content. ([details](skills/review-a11y/SKILL.md))
- **`/review-health`** — First-pass strategic orientation review. Useful when inheriting a project, evaluating a library, or revisiting your own repo. Evidence-cited map, not a grade. ([details](skills/review-health/SKILL.md))
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
- **`/bug-hunt`** — Proactive bug discovery. Risk-ranks hotspots, deep-dives each with reproducing tests. Advisory — proposes tickets for confirmed findings. ([details](skills/bug-hunt/SKILL.md))

### `/tidy-*` — Mechanical hygiene

- **`/tidy-docs`** — Documentation audit and repair via the `doc-maintainer` agent. Fixes within agent authority; surfaces judgment calls. ([details](skills/tidy-docs/SKILL.md))
- **`/tidy-git`** — Local repo hygiene: prunes stale refs, deletes merged branches (with preview), reports stashes/untracked/unpushed. Never touches the remote. ([details](skills/tidy-git/SKILL.md))

### `/test-*` — Testing utilities

- **`/test-mutation`** — Mutation testing. Introduces mutations, then writes tests to catch survivors — revealing coverage gaps that line coverage misses. Multi-session via a state file. ([details](skills/test-mutation/SKILL.md))

### Standalone

- **`/refactor`** — Tactical code-quality improvement (DRY, dead code, naming, complexity). Loops until no improvements remain. For structural changes, use `/review-arch`. Mutates. ([details](skills/refactor/SKILL.md))
- **`/pre-compact`** — Pre-compaction housekeeping: persist memory, audit git, clean trash, end with SBAR + resume prompt. Does not invoke `/compact`. ([details](skills/pre-compact/SKILL.md))
- **`/release`** — Cuts a project release. Discovers the release procedure, invokes `/review-release` as preflight, plans every step with reversibility annotations, executes step-by-step, halts on first failure. No skip-preflight or force-release flag. ([details](skills/release/references/README.md))

## Versioning

This project follows [Semantic Versioning](https://semver.org/). Skills (slash commands like `/implement`, `/review-perf`, etc.) are the public interface. Subagent names are internal implementation details and may be renamed or restructured without constituting a breaking change.

## Requirements

- `git` repository
- For ticket creation: integration with your issue tracker (CLI, MCP server, or API)

[cc]: https://claude.ai/code
