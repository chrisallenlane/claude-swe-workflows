# /tidy-docs - Documentation Hygiene

## Overview

The `/tidy-docs` skill spawns a `doc-maintainer` agent to comprehensively audit all project documentation. It audits every documentation file for correctness, completeness, freshness, and consistency — then fixes what it can within its authority and reports anything requiring user approval.

The skill lives in the `/tidy-*` namespace because the find→fix seam is small for most documentation issues — typos, stale code examples, broken links, freshness drift are all mechanical to correct. Anything genuinely judgment-laden (a deprecation that needs a stakeholder decision, an architectural claim that may no longer be true) surfaces in the agent's "Needs a decision" section rather than being auto-fixed.

**Key benefits:**
- Catches stale docs, broken links, and code-documentation drift in one sweep
- Autonomous fixes within the agent's authority — no per-fix approval interrupts
- Comprehensive: reviews all docs, not just recently changed ones
- Surfaces judgment-laden items separately so the operator can make those calls
- Offers to commit changes when done

## When to Use

**Use `/tidy-docs` for:**
- After a major feature or refactoring pass
- Before a release (catch stale docs)
- Periodic documentation hygiene
- When you suspect docs have drifted from the code

**Don't use `/tidy-docs` for:**
- Updating docs for a specific change (the `/implement` and `/bug-fix` workflows do this as part of their flow)
- Writing new documentation from scratch (just ask directly)

## Workflow

```
┌─────────────────────────────────────────────────────┐
│                  TIDY-DOCS                          │
├─────────────────────────────────────────────────────┤
│  1. Spawn doc-maintainer agent (full-audit mode)    │
│     • Checks every doc in the project against code: │
│       - Accuracy                                    │
│       - Examples                                    │
│       - Links                                       │
│       - Freshness                                   │
│       - Completeness                                │
│       - Consistency                                 │
│     • Fixes issues autonomously (within authority)  │
│  2. Report results to user                          │
│     • What was reviewed                             │
│     • What was changed                              │
│     • Items that need a decision                    │
│  3. Commit (optional, if changes were made)         │
└─────────────────────────────────────────────────────┘
```

## Example Session

```
> /tidy-docs

Spawning doc-maintainer agent for comprehensive audit...

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

## Tips

1. **Run after `/refactor`, or after acting on `/review-repo architecture`'s recommendations.** Code restructuring — tactical or architectural — often makes docs stale.

2. **Run before releases.** Stale docs in a release are embarrassing. A quick `/tidy-docs` pass catches drift. Pair with `/review-repo` (with follow-up authority) for a full pre-release sweep across every review dimension — it never changes files, so run `/tidy-docs` separately.

3. **Different from `/implement`'s documentation pass.** When `/implement` runs `doc-maintainer`, it is scoped to the git diff. `/tidy-docs` audits everything regardless of recent changes.
