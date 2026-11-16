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
└── judgment-chosen repertoire: implementer, reviewers, /refactor, /review-*, /bug-hunt, /scope, …

/bug-hunt (commander's intent: scope, severity floor, constraints, ticket/fix authority)
└── loop: assess → hunt → triage → (fix via /implement, if authorized) until no finding above the floor

/review-repo [focus] (commander's intent: context, scope, follow-up and ticket authority)
├── no focus: map (observe → orient → decide → act) → (with authority) the deeper
│   reviews the map calls for, consolidated → tickets created (with authority) or proposed
└── focus: architecture | dead-code | value → one deep review → ticket proposal
```

Planning feeds implementation: `/scope` → `/implement`. `/implement` takes one ticket, a batch, or an open-ended goal, and decides by judgment which of the below skills to invoke and when, over a small fixed floor (concept inventory, practical verification, tests green, an independent correctness review, no irreversible actions).

Supporting workflows available at any level:

**Reasoning and decisions:**

- `/think-brainstorm` — divergent idea generation (with a framing check when the problem itself is in doubt)
- `/think-diagnose` — abductive reasoning about causes (narrows ties by analysis of competing hypotheses)
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

- `/test-mutation` — mutation testing
- `/review-repo` — the entry point for whole-codebase review (advisory; never changes code). With no focus, it produces an evidence-cited map calibrated to a reference class. With follow-up authority, it runs the deeper reviews the map calls for and consolidates them; with ticket authority, it creates tickets, otherwise it proposes them. Focuses go straight to one deep review:
  - `architecture`: noun-analysis blueprint.
  - `dead-code`: confidence-tiered audit calibrated against dynamic dispatch.
  - `namespace`: cold-reader legibility probes. Search mode needs the operator and never runs unattended.
  - `value`: a requirement trade menu. The map runs this one only when intent asks, because its output is product decisions.

  Diff-scoped correctness review is not a skill. `/implement` and `/bug-fix` run `swe-correctness-reviewer` as a blocking gate, and Claude Code's built-in `/code-review` covers other diffs.

**Releases:**

- `/release` — cut a project release (discovers release procedure, always invokes `/review-release` as preflight, plans before executing, halts on first failure rather than attempting rollback)

**Utility:**

- `/pre-compact` — pre-compaction housekeeping (memory, git, trash, SBAR, resume prompt)
- `/tidy-git` — mechanical local repo hygiene (prune stale refs, delete merged branches, report stashes/untracked/unpushed)
