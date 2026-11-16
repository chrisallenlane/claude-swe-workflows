# /review-dead - Dead-Code Audit

## Overview

The `/review-dead` skill audits a codebase for dead code — unreferenced symbols, dead files and modules, unreachable branches, unused imports and dependencies, commented-out blocks, tests-only code, and dead configuration. It is **advisory only**: it catalogs and proposes tickets; removal happens through `/refactor` or ticketed work.

**Key benefits:**
- The focused, cheap way to get a dead-code audit — `/review-arch` also finds dead code, but only as step one of a full architectural blueprint
- Per-finding confidence tiers (PROVEN / LIKELY / UNVERIFIABLE), calibrated by surveying the codebase's dynamic-dispatch patterns before any finding is made
- Leverages language tooling when present (`deadcode`/`staticcheck`, `knip`, `vulture`, `luacheck`, compiler warnings) — never installs anything
- Library-aware: exported public API is a reference root, not dead code
- Respects intentional retention (lint suppressions, ADR-protected code) — reported separately, never proposed for removal

## When to Use

**Use `/review-dead`:**
- Before a refactoring pass — less noise for everything downstream
- After removing a feature — sweep for what it stranded
- On inherited or long-lived code where cruft has accumulated
- When you want removal *tickets* rather than immediate removal

**Don't use it for:**
- Removing the code — work the tickets with `/implement`, or shrink the whole codebase with `/refactor`
- Live-but-unnecessary machinery — that's `/review-arch`'s mechanism audit or `/review-value`
- Duplicate code — `/refactor`

**Rule of thumb:** `/review-dead` answers "what could be deleted?" without deleting anything.

## The Confidence Discipline

Dead-code auditing's classic failure is dynamic dispatch: reflection, string-built symbol names, plugin registries, and convention-based loading make "no references found" unreliable. The auditor therefore:

1. **Surveys dynamic-dispatch patterns first** — their presence caps the confidence any reference-search finding can earn, and the survey leads the report.
2. **Determines the reference roots** — an application's entry points, or a library's exported API. A library's unused export is not a finding.
3. **Tiers every finding:**

| Tier         | Meaning                                                                          |
| ------------ | -------------------------------------------------------------------------------- |
| PROVEN       | Tool-verified, or exhaustive search with no dynamic dispatch that could reach it |
| LIKELY       | No references found; dynamic patterns checked and appear not to apply            |
| UNVERIFIABLE | No references found, but a dynamic pattern could plausibly reach it              |

Every finding cites its evidence — the tool that flagged it, or the searches performed and their results. UNVERIFIABLE findings route to verification tickets, never removal tickets.

## Workflow

```
1. Determine scope   →  2. Spawn swe-dead-code-auditor  →  3. Present findings
→  4. Iterate with operator  →  5. Offer to cut tickets  →  6. Summary
```

The iteration step matters: the operator may know liveness the audit can't see (external consumers, deployment-read config). Operator knowledge is evidence; findings get dropped or downgraded accordingly.

Ticket shapes follow the shared advisory pattern (`references/advisory-tickets.md`): per-cluster removal tickets, a single sweep ticket for scattered PROVEN findings (recommend working it with `/implement`), and a verification ticket for UNVERIFIABLE items. Declining tickets is valid — the audit stands as a planning artifact.

## Tips for Effective Use

1. **Chain it ahead of `/review-arch`.** Dead code perturbs noun frequencies; auditing (and removing) first gives the blueprint cleaner input.
2. **Trust the tiers, not the totals.** Act on PROVEN freely, review LIKELY, and treat UNVERIFIABLE as questions for a human, not cleanup work.
3. **Watch the tests-only category.** Source whose only references are its own tests looks alive to naive search — the tests keep it warm — but no production path reaches it. Deleting it removes the tests too.
4. **Runs inside `/review-health`'s follow-up, before `/review-arch`.** The caller answers ticket proposals per the autonomy contract; `/review-arch`'s incidental dead-code findings are deduped as confirmations.

## Agent Coordination

**Single agent invocation.** The skill spawns `swe-dead-code-auditor` once per invocation. No implementation agents, no QA agents (no changes to verify).

## Abort Conditions

**Abort:** auditor failure after one retry; operator interrupt; tracker unavailable after ticket approval (surface the approved set for manual creation).

**Do NOT abort for:** an honest-zero report, or the operator declining tickets — both are valid outcomes.
