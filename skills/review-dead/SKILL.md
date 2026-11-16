---
name: review-dead
description: Dead-code audit. Dispatches a focused auditor that finds unreferenced, unreachable, and unused code — with per-finding confidence tiers calibrated against the codebase's dynamic-dispatch patterns, and language tooling leveraged when present. Advisory only — produces findings and proposes tickets; does not remove code.
model: opus
---

# Dead-Code Review — Focused Audit

Audits a codebase for dead code: unreferenced symbols, dead files, unreachable branches, unused imports and dependencies, commented-out blocks, tests-only code, and dead configuration. **Advisory only** — the skill catalogs and proposes; removal happens through ticketed work in `/implement`, or as part of a whole-codebase reduction by `/refactor`.

## Philosophy

**Dead code is complexity for free, but false positives cost more.** Deleting live code breaks the product, so the audit's value is calibration: every finding carries cited evidence and a confidence tier (PROVEN / LIKELY / UNVERIFIABLE), and the tiers are calibrated by first surveying the codebase's dynamic-dispatch patterns — the classic way "no references found" turns out to be a lie.

**Focused and cheap, by design.** `/review-arch` also catalogs dead code, but only as step one of a full architectural blueprint. This skill is the way to get *just* the dead-code audit without paying for noun analysis — run it before a refactoring pass, after a feature removal, or on inherited code.

**Honest zero is a valid outcome.** A clean codebase gets a short report saying so.

## Workflow

```
1. Determine scope        entire codebase, or caller-specified path
2. Spawn auditor          swe-dead-code-auditor (fresh instance)
                          → dynamic-dispatch survey, roots determination,
                            tooling pass, findings with confidence tiers
3. Present findings       grouped by category; survey and roots shown first,
                          because they calibrate everything below
4. Iterate with operator  challenge findings, adjust, drop false positives
5. Offer to cut tickets   per references/advisory-tickets.md
6. Completion summary
```

### 1. Determine Scope

Default is the entire codebase. Respect a caller-specified path or module. Pass scope to the auditor.

### 2. Audit

Spawn a fresh `swe-dead-code-auditor`:

```
Perform a dead-code audit of this codebase.
Scope: [entire codebase | caller-specified scope]
Survey dynamic-dispatch patterns first, determine the reference roots
(application entry points vs. library public API), run available language
tooling, and return findings with per-finding confidence and evidence.
```

**If the auditor reports honest zero:** workflow complete; skip to step 6.

### 3. Present Findings

Present the report leading with the two calibration facts — the dynamic-dispatch survey and the roots determination — because they tell the operator how much to trust everything below. Then the findings by category, each with confidence tier, evidence, and estimated line count. Intentionally-retained items (suppressions, ADR-protected code) are shown separately, not proposed for removal.

### 4. Iterate with Operator

The operator may know liveness the audit can't see (a symbol reached by an external consumer, a config key read by a deployment system). Drop or downgrade findings accordingly; the operator's knowledge is evidence.

### 5. Offer to Cut Tickets

Per the shared advisory pattern ([`references/advisory-tickets.md`](../../references/advisory-tickets.md)). Sensible shapes:

- **One removal ticket per subsystem or category** when findings cluster (e.g., "remove dead config plumbing": the keys, their readers, their docs).
- **A single sweep ticket** for scattered PROVEN findings — recommend working it with `/implement`, which removes the code under its verification and correctness gates.
- **UNVERIFIABLE findings** go in a verification ticket (what a human must confirm), never a removal ticket.

On approval, create tickets per [`references/trackers.md`](../../references/trackers.md). Declining is valid — the audit stands as a planning artifact.

### 6. Completion Summary

```
## Dead-Code Review Complete

### Scope: [entire codebase | path]
### Findings: N (PROVEN: a, LIKELY: b, UNVERIFIABLE: c) — ~N lines removable (estimate)
### Dropped in iteration: N (operator knowledge)
### Tickets created: [#s with recommended skill] | none — audit stands as planning artifact
### Recommended next steps: [e.g., "/implement on the PROVEN sweep ticket for src/legacy/"]
```

## Agent Coordination

One `swe-dead-code-auditor` per invocation, fresh instance. No implementation or QA agents — the skill changes nothing.

## Abort Conditions

**Abort:** auditor failure after one retry; operator interrupt; tracker unavailable after ticket approval (surface the approved set for manual creation).

**Do NOT abort for:** honest zero, or the operator declining tickets.

## Integration with Other Skills

**`/review-dead` vs `/review-arch`:** `/review-arch` catalogs dead code incidentally, as input to a full blueprint. Use `/review-dead` when you want only the audit — it's focused and cheap. Running `/review-arch` afterward on a cleaned codebase gives its noun analysis less noise to see through.

**`/review-dead` vs `/refactor`:** `/refactor` deletes dead code too, but as one move in a whole-codebase redesign on its own branch. Use `/review-dead` when you want the audit without the mutation — to review before deleting, or to cut tickets for `/implement`.

**Runs inside `/review-health`'s follow-up, before `/review-arch`.** The caller answers the ticket-proposal step per the autonomy contract ([`references/autonomy.md`](../../references/autonomy.md) § "Auto-approval of sub-skill ticket proposals"). `/review-arch`, running later, re-catalogs dead code incidentally in its Step 1 — `/review-health` treats those re-findings as confirmations and dedupes them in the consolidated report.
