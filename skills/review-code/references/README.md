# /review-code - Adversarial Correctness Review of a Diff

## Overview

`/review-code` answers one question about one change: **is this diff correct?** It resolves what diff is under review, dispatches the `swe-correctness-reviewer` agent against it, and presents an evidence-cited report of correctness bugs and unverifiable assumptions. Like every `/review-*` skill, it is advisory — it audits and proposes tickets, never mutates.

The reviewer does not ask "does this look right?" It assumes the diff was merged and caused a production incident, then works backward to the cause — the prospective-hindsight framing borrowed from `/think-premortem`. Concretely, that means mechanically verifying every assumption the diff makes against the actual repository:

- Does every referenced file exist, at that exact path?
- Does every referenced symbol exist, with that signature?
- Does every language/library feature used exist **in the target runtime version** (PHP 5.3, not "PHP")?
- Does every caller of every changed function still hold?
- Do the error paths behave, not just the happy path?

Each assumption gets a ledger entry: verified (with the evidence), false (a finding), or unverifiable-in-repo (a residual risk for a human to check). An honest zero-findings verdict is a valid outcome — the reviewer is explicitly licensed to report nothing rather than manufacture findings.

## When to Use

**Use `/review-code` for:**
- "Is this branch safe to merge?" — pre-merge review of your own or a colleague's work
- Reviewing a PR before approving it
- Auditing a recent commit or commit range you're suspicious of
- Legacy or hostile codebases — no tests, can't run the app locally — where analytical review is the only correctness check available
- A second opinion on AI-generated changes before shipping them

**Don't use `/review-code` for:**
- Repo-wide proactive bug discovery with no specific diff in mind — that's `/bug-hunt` (risk-ranked, writes reproducing tests)
- Style, naming, and refactoring feedback — that's `/refactor` (or the code-review step inside `/implement`)
- Security posture review — that's `/review-security`
- Reviewing code you're about to write — review needs a diff to exist

**Relationship to `/implement` and `/bug-fix`:** the same `swe-correctness-reviewer` agent runs as `/implement`'s step 9 and `/bug-fix`'s step 10, where its findings are blocking and resolved through an automatic fix-and-re-review convergence loop. `/review-code` is the standalone wrapper: one pass, findings routed to you instead of to an implementation agent. If you fix the findings, re-run `/review-code` — the fresh-instance re-review is the part of the protocol that catches bugs introduced by the fixes.

## Workflow

```
┌──────────────────────────────────────────────┐
│  1. RESOLVE DIFF SCOPE                       │
│  ────────────────────────────────────────    │
│  Explicit: range, branch, PR, "uncommitted"  │
│  Inferred: dirty tree → working tree changes │
│            feature branch → merge-base..HEAD │
│            on main → HEAD~1..HEAD            │
│                                              │
│  Present scope + file list, confirm          │
└──────────────────┬───────────────────────────┘
                   ▼
┌──────────────────────────────────────────────┐
│  2. DISPATCH REVIEWER                        │
│  ────────────────────────────────────────    │
│  Agent: swe-correctness-reviewer (fresh)     │
│                                              │
│  "The bug has already shipped. Find it."     │
│  Six-concern spine, assumption ledger,       │
│  file:line evidence. Single pass.            │
└──────────────────┬───────────────────────────┘
                   ▼
┌──────────────────────────────────────────────┐
│  3. PRESENT REPORT                           │
│  ────────────────────────────────────────    │
│  Findings (defects, evidence-cited)          │
│  Residual risks (need human verification)    │
│  Assumption ledger + coverage notes          │
│  Verdict: APPROVE | N FINDINGS               │
└──────────────────┬───────────────────────────┘
                   ▼
┌──────────────────────────────────────────────┐
│  4. PROPOSE TICKETS                          │
│  ────────────────────────────────────────    │
│  Shape proposal → approve / edit / decline   │
│  Decline → report stands alone, no writes    │
└──────────────────────────────────────────────┘
```

## What the Report Contains

- **Assumption ledger** — every external reference the diff makes (paths, symbols, signatures, config keys, version-dependent features), each with how it was verified and a verdict
- **Findings** — verified defects, each with file:line, the concrete failure it produces, the evidence, and a one-line fix direction
- **Residual risks** — assumptions that can't be verified from the repo alone (external service behavior, production-only conditions), each with what *would* verify it
- **Coverage notes** — what the reviewer didn't fully check (dynamic call sites it couldn't rule out, depth limits), so you know the review's edges
- **Verdict** — APPROVE or N FINDINGS

In standalone use, "findings" means **severity, not authority** — nothing blocks you mechanically, but these are the defects the reviewer asserts you should not merge unresolved.

## Examples

### Example 1: Pre-merge branch review

```
User: /review-code feat/payment-retry

1. Scope: merge-base main feat/payment-retry..feat/payment-retry
   (4 files, +210/-35). Confirmed.
2. Reviewer establishes target runtime (Node 18 from package.json engines),
   walks the spine.
3. Report: 2 findings —
   - retry.js:84 assumes processPayment() throws on decline; it resolves
     with {status: "declined"} (evidence: gateway/stripe.js:142). Declined
     payments would be retried as if they were network errors.
   - retry.js:31 references config key "payments.maxRetries"; config
     schema defines "payments.retry.max" (evidence: config/schema.json:77).
   1 residual risk: gateway rate-limit behavior under burst retries is
   not observable from the repo.
4. Proposal: 2 tickets (independent findings) + 1 verification ticket.
   User approves; tickets cut.
```

### Example 2: Hostile legacy codebase

```
User: /review-code HEAD~3..HEAD   (PHP 5.3 app, zero tests, can't run locally)

1. Scope confirmed: 3 remediation commits, 11 files.
2. Reviewer pins target to PHP 5.3 (composer.json + deploy docs), verifies
   every function used against the 5.3 reference — flags one use of
   array_column() (PHP 5.5+) and one require path that doesn't exist in
   the repo (file lives under lib/legacy/, not lib/).
3. Report: 2 findings, both of the unverified-assumption class.
4. User declines tickets, fixes both on the branch, re-runs /review-code.
   Round 2: APPROVE.
```

### Example 3: Clean review

```
User: /review-code   (dirty working tree, small refactor)

1. Inferred scope: uncommitted changes vs HEAD (2 files, +40/-38). Confirmed.
2. Reviewer walks the spine; all 9 ledger assumptions verified.
3. Report: APPROVE, zero findings, zero residual risks.
4. No ticket proposal — report stands alone.
```

## Tips for Effective Use

1. **Re-run after fixing.** The protocol's value comes from fresh-instance re-review — fixes introduce bugs too. A fix-then-re-run cycle that converges to APPROVE is the standalone equivalent of `/implement` step 9's convergence loop.

2. **Don't feed it your rationale.** If you just wrote the code, resist explaining your design to the reviewer. The skill deliberately withholds conversation context from the agent; the diff and the repo are the whole input. Your justifications are exactly the anchoring the review exists to escape.

3. **Trust the residual-risk lane.** Not everything is analytically verifiable. When the reviewer says "this needs a staging run," that's calibration, not weakness — schedule the staging run.

4. **Zero findings is information.** A rigorous APPROVE after a full spine walk is a meaningful signal, especially on changes you were nervous about. The reviewer is licensed to find nothing.

5. **Huge diffs dilute attention.** For a very large range, watch the coverage notes — if the reviewer reports depth limits, split the range and review the riskiest files in a focused pass.
