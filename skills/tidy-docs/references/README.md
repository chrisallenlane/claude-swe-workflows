# /tidy-docs - Documentation Hygiene

The step-by-step procedure lives in [`SKILL.md`](../SKILL.md); this guide covers when to use the skill and what to expect.

## Overview

`/tidy-docs` audits every documentation file in the project against the code. It checks accuracy, examples, links, freshness, completeness, and consistency, and fixes what it finds. The work is done by a `doc-maintainer` agent in full-audit mode.

It lives in the `/tidy-*` namespace because the find → fix seam is small for most doc issues. Typos, stale code examples, broken links, and freshness drift are mechanical to correct, so the agent fixes them without per-fix approval. Anything judgment-laden is reported under "Needs a decision" rather than auto-fixed. Examples: a deprecation that needs a stakeholder call, or an architectural claim that may no longer hold.

## When to Use

**Use `/tidy-docs` for:**
- After a major feature, `/refactor`, or architectural change
- Before a release
- Periodic hygiene, or whenever you suspect docs have drifted

**Don't use it for:**
- Docs for one specific change. `/bug-fix` handles those, and so does `/implement` when the work calls for it. Both run the agent in targeted mode, scoped to the diff. `/tidy-docs` checks everything regardless of recent changes.
- Writing new documentation from scratch. Just ask directly.

**vs. `/review-repo`:** `/review-repo` never changes files. For a full pre-release sweep, run it and `/tidy-docs` separately.

## Flow

```
audit + fix all docs (doc-maintainer, full audit) → report → commit (optional)
```

## What to Expect

- **Edits land in your working tree** without per-fix prompts.
- **The report** lists what was reviewed, what was changed, and what needs your decision.
- **Committing is your call.** If anything changed, the skill asks before committing.

## Example Session

```
> /tidy-docs

## Documentation Audit Report

### Changed
1. skills/implement/references/README.md — Updated example to match current CLI flags
2. CLAUDE.md — Fixed skill list ordering to match directory structure

### Needs a decision
- README.md:42 — installation section references a deprecated flag
  (options: document the replacement flag, or restore the old one)

Commit documentation fixes?
> Yes

Committed: "docs: tidy project documentation"
```
