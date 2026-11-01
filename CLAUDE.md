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
│   ├── autonomy.md          # Discipline for skills that act on granted authority
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
- YAML frontmatter: `name`, `description`, `model` (opus/sonnet/haiku/fable - lowercase)
- Invoked by user with `/skill-name`
- Define workflows, processes, or specialized behaviors

**Agents** (in `agents/*.md`):
- YAML frontmatter: `name`, `description`, `model` (lowercase)
- Spawned programmatically via `Task` tool with `subagent_type`
- Operate autonomously within defined scope

**Model names must be lowercase** (`opus`, `sonnet`, `haiku`, `fable`) - capitalized names are not recognized.

**New `/think-*` skills must pass the five tests in [`references/think.md`](references/think.md).** When proposing or designing a new `/think-*` skill, read `references/think.md` first and check the proposal against the tests there. Skills outside the `/think-*` namespace are admitted by different criteria — primarily, whether they earn their keep in real software-engineering work — though the practitioner-methodology and structured-discipline values described in `references/think.md` apply across the plugin.

## Workflow

The skills form a layered system. Higher-level workflows orchestrate lower-level ones:

```
/implement (one ticket, a batch, or an open-ended goal)
├── fixed floor: concept inventory → build → practical verification → correctness review
└── judgment-chosen repertoire: SMEs, reviewers, /refactor, /review-*, /bug-hunt, /scope, …

/bug-hunt (commander's intent: scope, severity floor, constraints, ticket/fix authority)
└── loop: assess → hunt → triage → (fix via /implement, if authorized) until no finding above the floor

/review-health (commander's intent: lens, scope, follow-up and ticket authority)
└── map (observe → orient → decide → act) → (with authority) the specialist reviews
    the map calls for, consolidated → tickets created (with authority) or proposed
```

Planning feeds implementation: `/scope` → `/implement`. `/implement` takes one ticket, a batch, or an open-ended goal, and decides by judgment which of the below skills to invoke and when, over a small fixed floor (concept inventory, practical verification, tests green, an independent correctness review, no irreversible actions).

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
- `/bug-hunt` — proactive bug discovery (commander's intent with optional ticket/fix authority; iterates rounds until nothing is confirmed above a severity floor; advisory by default, fixes via `/implement` only when authorized)

**Redesign:**

- `/refactor` — simplification-first redesign (Musk's five steps; behavior pinned by a differential oracle against the incumbent; runs on its own `refactor/<slug>` branch with one checkpoint, the requirements menu; `/implement` runs it unattended with the menu answered from commander's intent)

**Quality pipelines:**

- `/review-code` — adversarial correctness review of a specific diff (advisory; the one diff-scoped `/review-*` skill, so never run by `/review-health`'s follow-up; wraps the same `swe-correctness-reviewer` agent that `/implement` and `/bug-fix` run as blocking gates)
- `/review-value` — value-engineering review (advisory; discovers requirements across provenance tiers — documented, spec-pinned, inferred — attributes implementation cost to them, and presents a behavior-for-simplicity trade menu; run by `/review-health`'s follow-up only when intent asks, because its output is product decisions the operator must rule on)
- `/review-dead` — focused dead-code audit (advisory; per-finding confidence tiers calibrated against the codebase's dynamic-dispatch patterns; `/review-health`'s follow-up runs it before `/review-arch`)
- `/review-namespace` — empirical namespace-legibility review (advisory; cold reader agents probe the file tree by navigation task, misses become evidence-backed findings; optional heavy search mode evolves hypothetical trees to a measured champion; `/review-health`'s follow-up never runs search mode, which needs the operator for calibration)
- `/test-mutation` — mutation testing
- `/review-health` — holistic review (evidence-cited map calibrated to a reference class; with follow-up authority, runs the specialist reviews the map calls for and consolidates them; with ticket authority, creates tickets — otherwise proposes them; never changes code)

**Releases:**

- `/release` — cut a project release (discovers release procedure, always invokes `/review-release` as preflight, plans before executing, halts on first failure rather than attempting rollback)

**Utility:**

- `/pre-compact` — pre-compaction housekeeping (memory, git, trash, SBAR, resume prompt)
- `/tidy-git` — mechanical local repo hygiene (prune stale refs, delete merged branches, report stashes/untracked/unpushed)
