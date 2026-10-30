# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is `claude-swe-workflows`, a Claude Code plugin for software engineering workflows. It provides skills and agents that extend Claude Code's capabilities for systematic development.

## Plugin Structure

```
├── .claude-plugin/
│   ├── marketplace.json # Marketplace manifest (lists plugins for installation)
│   └── plugin.json      # Plugin metadata (name, version, description, license)
├── agents/              # Agent definitions
│   └── agent-name.md    # Agent prompt with YAML frontmatter
├── skills/              # Skill definitions
│   └── skill-name/
│       ├── SKILL.md          # Skill prompt with YAML frontmatter
│       └── references/
│           └── README.md     # Human-readable guide for the skill
├── references/          # Cross-cutting reference and discipline docs
│   ├── autonomy.md          # Discipline for the orchestrator namespaces
│   ├── think.md             # Design discipline for the /think-* namespace
│   └── ...
├── CHANGELOG.md
├── CONTRIBUTING.md
└── README.md
```

## Development

Test the plugin locally:

```bash
claude --plugin-dir .
```

## Writing Skills and Agents

**Skills** (in `skills/*/SKILL.md`):
- YAML frontmatter: `name`, `description`, `model` (opus/sonnet/haiku - lowercase)
- Invoked by user with `/skill-name`
- Define workflows, processes, or specialized behaviors

**Agents** (in `agents/*.md`):
- YAML frontmatter: `name`, `description`, `model` (lowercase)
- Spawned programmatically via `Task` tool with `subagent_type`
- Operate autonomously within defined scope

**Model names must be lowercase** (`opus`, `sonnet`, `haiku`) - capitalized names are not recognized.

**New `/think-*` skills must pass the five tests in [`references/think.md`](references/think.md).** When proposing or designing a new `/think-*` skill, read `references/think.md` first and check the proposal against the tests there. Skills outside the `/think-*` namespace are admitted by different criteria — primarily, whether they earn their keep in real software-engineering work — though the practitioner-methodology and structured-discipline values described in `references/think.md` apply across the plugin.

## Workflow

The skills form a layered system. Higher-level workflows orchestrate lower-level ones:

```
/implement-project
├── /implement-batch (per batch)
│   └── /implement (per ticket)
└── judgment-chosen repertoire: /refactor, /review-*, /bug-hunt, /scope, … → /review-release last

/lead-bug-hunt
└── loop: /bug-hunt → /implement-batch (until convergence)
    └── termination: /review-test (new tests)

/lead-review
└── /review-health → /review-dead → /review-arch → /review-security → /review-perf
  → /review-a11y → /review-test → /review-release
  (sub-skill ticket proposals auto-approved or auto-declined per startup choice)
```

Planning feeds implementation: `/scope-project` → `/implement-project`, or `/scope` → `/implement`. `/implement-project` is the top-level autonomous lead — given commander's intent (usually a batch of tickets, sometimes an open-ended goal), it decides which of the below skills to invoke and when, over a small fixed floor (tests green at every merge, smoke test, `/review-release` last).

Supporting workflows available at any level:

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
- `/lead-bug-hunt` — autonomous bug-elimination loop (orchestrator-family; iterates `/bug-hunt` → `/implement-batch` until convergence below a severity floor; always runs `/review-test` on new reproducing tests at termination)

**Quality pipelines:**

- `/review-code` — adversarial correctness review of a specific diff (advisory; the one diff-scoped `/review-*` skill, excluded from `/lead-review`'s repo-scoped pipeline; wraps the same `swe-correctness-reviewer` agent that `/implement` (step 9) and `/bug-fix` (step 10) run as blocking gates)
- `/review-value` — value-engineering review (advisory; discovers requirements across provenance tiers — documented, spec-pinned, inferred — attributes implementation cost to them, and presents a behavior-for-simplicity trade menu; excluded from `/lead-review` because its output is product decisions the operator must rule on)
- `/review-dead` — focused dead-code audit (advisory; per-finding confidence tiers calibrated against the codebase's dynamic-dispatch patterns; runs as `/lead-review`'s phase 2)
- `/review-namespace` — empirical namespace-legibility review (advisory; cold reader agents probe the file tree by navigation task, misses become evidence-backed findings; optional heavy search mode evolves hypothetical trees to a measured champion; excluded from `/lead-review` — overlaps `/review-arch` in-pipeline, and search mode needs the operator for calibration)
- `/test-mutation` — mutation testing
- `/lead-review` — autonomous comprehensive review (orchestrator-family; runs its eight-phase review pipeline — health, dead code, arch, security, perf, a11y, test, release — in sequence; `/review-code`, `/review-value`, and `/review-namespace` are structurally excluded; operator-configurable ticket creation at startup)

**Releases:**

- `/release` — cut a project release (discovers release procedure, always invokes `/review-release` as preflight, plans before executing, halts on first failure rather than attempting rollback)

**Utility:**

- `/pre-compact` — pre-compaction housekeeping (memory, git, trash, SBAR, resume prompt)
- `/tidy-git` — mechanical local repo hygiene (prune stale refs, delete merged branches, report stashes/untracked/unpushed)
