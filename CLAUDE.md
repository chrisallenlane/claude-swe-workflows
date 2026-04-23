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
├── CHANGELOG.md
├── CONTRIBUTING.md
├── HACKING.md
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

## Workflow

The skills form a layered system. Higher-level workflows orchestrate lower-level ones:

```
/lead-project
└── OODA loop invoking any skill below, until commander's intent is met

/implement-project
├── /implement-batch (per batch)
│   └── /implement (per ticket)
└── quality pipeline: /refactor, /review-arch, /review-test, /review-doc, /review-release

/refactor-deep
└── /refactor → /review-arch → /refactor → /review-doc

/review-deep
└── /review-health → /review-arch → /review-security → /review-perf
  → /review-a11y → /review-test → /review-doc → /review-release
```

Planning feeds implementation: `/scope-project` → `/implement-project`, or `/scope` → `/implement`. `/lead-project` sits one level higher — given a commander's intent, it decides which of the below skills to invoke and when.

Supporting workflows available at any level:

**Reasoning and decisions:**

- `/think-reframe` — problem redefinition
- `/think-brainstorm` — divergent idea generation
- `/think-diagnose` — abductive reasoning about causes
- `/think-deliberate` — adversarial decision-making
- `/think-scrutinize` — adversarial idea critique
- `/think-reflect` — retrospective learning

**Bug work:**

- `/bug-fix` — diagnosis-first bug fixing
- `/bug-hunt` — proactive bug discovery

**Quality pipelines:**

- `/test-mutation` — mutation testing
- `/refactor-deep` — full tactical + architectural + tactical refactoring cycle
- `/review-deep` — comprehensive pre-release review pipeline
