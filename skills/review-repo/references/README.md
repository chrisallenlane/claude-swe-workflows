# /review-repo — Reviewing a Codebase as a Whole

The step-by-step procedure lives in [`SKILL.md`](../SKILL.md); this guide covers when to use the skill and what to expect.

## Overview

`/review-repo` is the single entry point for reviewing a codebase as a whole. It never changes code. It works in two shapes:

- **`/review-repo [scope]` gives the orientation map.** This is an evidence-cited map of the repo's state, calibrated to a reference class, built to inform strategic decisions about how to engage with the project. Given authority up front, it also runs the deeper reviews the map calls for, consolidates what they find, and tickets it.
- **`/review-repo <focus> [scope]` gives a focused review**, going straight to one deep pass:

| Focus          | Question                                             | What you get                                                                                                                    |
|----------------|------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| `architecture` | Where should everything live?                        | Noun analysis, mechanism audit, and a target blueprint covering every module                                                    |
| `dead-code`    | What can be deleted, and how sure are we?            | Findings tiered PROVEN / LIKELY / UNVERIFIABLE, calibrated by a dynamic-dispatch survey                                         |
| `value`        | Which requirements cost more than they're worth?     | A trade menu of small behavior relaxations that dissolve disproportionate machinery                                             |
| `namespace`    | Can a newcomer find things from the file tree alone? | Cold-reader navigation probes against verified ground truth; misses become findings; optional search mode evolves a better tree |

Several focuses can be named together (`/review-repo value dead-code architecture`); they run in dependency order, each feeding the next. A focus naming another review skill (`security`, `test`, `perf`, `a11y`, `release`) is routed to that skill.

Before v12 these focuses were separate skills: `/review-arch`, `/review-dead`, `/review-value` and `/review-namespace`. Their methods live in their agents and are unchanged; only the entry point moved.

## Why It's Shaped This Way

- **Observation before interpretation.** The map follows Boyd's OODA loop (Observe → Orient → Decide → Act) with strict phase gates: Observe collects signals with no verdicts, and each later phase may cite only the one before it.
- **"Good" is relational.** 34% test coverage means something different in a research prototype than in an OSS library. The repo is classified into a reference class first (see `classes/`), and each dimension is judged against that class. The classification is cited and you can override it.
- **Every claim carries evidence.** A finding without a `file:line` or tool-output citation is dropped or moved to the Coverage Manifest.
- **Named unknowns beat silent unknowns.** The Coverage Manifest names every tool that couldn't run and every question that couldn't be answered.
- **Debt is located by its interest, not its look.** Ugly code nobody changes costs nothing. The map crosses per-file complexity with git change frequency to find *hotspots* (complex code that keeps changing) and *hidden change coupling* (files that change together with no static dependency). Confirmed hotspots become scoped `/refactor` recommendations; dormant cruft is usually left alone. On thin or squash-merged history, the Coverage Manifest says the signal is weak.
- **The map decides the depth.** There is no fixed sequence of deeper reviews; each runs only if the map gives it something to look at, and every review that plausibly applied but didn't run gets a one-line reason.

| Failure mode                                                            | Countermeasure                                                                    |
|-------------------------------------------------------------------------|-----------------------------------------------------------------------------------|
| Inheritor's paralysis / availability bias — fixate on first file opened | Systematic Observe phase with fixed signal battery                                |
| Unknown-unknowns dominance                                              | Coverage Manifest elevates missing tooling to first-class output                  |
| Premature closure                                                       | Phase-integrity gates (Orient cites Observe; Decide cites Orient)                 |
| Expert deference — accept prior-author choices unexamined               | Differential-diagnosis classification forces candidate alternatives with evidence |
| Free-floating adjectives ("health: good")                               | Reference-class calibration with cited per-class rubrics                          |
| Confident false positives ("no references" taken as proof of death)     | The `dead-code` focus surveys dynamic dispatch before tiering anything            |

Practitioner lineage: OODA (Boyd), medical differential diagnosis, home inspection (ASHI severity tiers), marine surveying (reference-class calibration), technical due diligence, behavioral code analysis (Tornhill, *Your Code as a Crime Scene*), and value engineering (Miles, GE).

```
Preflight ──▶ OBSERVE ──▶ ORIENT ──▶ DECIDE ──▶ ACT ──┬── no follow-up authority ──▶ offer follow-ups; stop
                                                      └── follow-up authority ──▶ FOLLOW UP (run, consolidate, ticket)
```

## When to Use

**Use `/review-repo` for:**

- A strategic overview of a repo you've just inherited
- Evaluating a FOSS project for adoption or contribution
- Revisiting your own project to decide where to invest effort
- Generating an onboarding map for a new teammate
- A comprehensive review that produces a backlog: grant follow-up and ticket authority
- A structural blueprint (`architecture`), a dead-code audit (`dead-code`), a requirements price list (`value`), or a measured legibility audit of the file tree (`namespace`)
- Finding where technical debt is costing you, and where to aim `/refactor`

**Don't use `/review-repo` for:**

- Finding specific bugs → `/bug-hunt`, or `/bug-fix` for a known one
- Making changes or redesigning toward less machinery → `/implement`, `/refactor`
- Reviewing a specific diff: `/implement` and `/bug-fix` run the correctness gate on their own diffs; for anything else, use Claude Code's built-in `/code-review`

**Rule of thumb:** the map answers "what is this repo, and what does that mean for me?" A focus, or a specialist skill, answers a deeper and narrower question. With authority, the map decides which of those questions are worth asking and asks them.

## What You'll Be Asked

For the map, one exchange up front:

- **Context:** inheriting a work repo, evaluating a FOSS project, revisiting your own repo, onboarding a teammate, or other. This shapes the classification and the strategic options.
- **Authority:** two grants, both defaulting to no.
- **Scope**, only if the repo is very large (>100k LOC or >10 top-level subsystems).

| Grant             | Question                                                                                            | If granted                                                   | If not                                                         |
|-------------------|-----------------------------------------------------------------------------------------------------|--------------------------------------------------------------|----------------------------------------------------------------|
| Follow-up reviews | May I run the deeper reviews the map calls for? Some, like `/review-security`, are heavy            | The deeper reviews run                                       | They're recommended; the run ends by offering to run them      |
| Tickets           | May I create tickets at or above a severity floor without asking again? Which floor (default High)? | Reviews' ticket proposals at or above the floor are approved | One consolidated ticket set is proposed for your approval      |

| Follow-up | Tickets | What you get                                                                                                        |
|-----------|---------|---------------------------------------------------------------------------------------------------------------------|
| no        | no      | The cheap, fast orientation map, ending with recommendations and an offer to run the follow-ups                     |
| no        | yes     | Not offered: the ticket question is asked only when follow-ups are granted                                          |
| yes       | no      | Map plus the deeper reviews it calls for; one consolidated ticket set proposed at the end, created only on approval |
| yes       | yes     | Map plus deeper reviews; tickets at or above the floor created as the run goes, the rest reported                   |

Granting tickets *is* the approval to create them. The floor is mapped across the reviews' different scales: **High = CRITICAL/HIGH, ASHI Safety Hazard/Major, release BLOCKER.** Architecture, dead-code, and value items are always proposed, never auto-created.

Even with follow-up authority, the map never runs `/refactor` or `/implement` (they change code), never runs the `value` focus unless your intent asks for it (its trades are product decisions), and never runs `namespace` search mode (it needs you for calibration). `/review-release` runs report-only.

A focused review asks nothing up front. It presents its findings, iterates with you (what you know about liveness, intent, or history counts as evidence), then offers tickets. `namespace` search mode (`/review-repo namespace search`) runs only on explicit opt-in, after you confirm its cost (millions of tokens) and a round cap.

## What You Get Back

The map, inline, in this order:

1. **Context:** your review context, scope, grants, and the repo's reference class (with evidence and how to override it)
2. **Observation Record:** factual signals with IDs (`O1`, `O2`, …)
3. **Findings:** per-dimension rubric placement (Foundational / Adequate / Strong), severity-tiered findings, cross-cutting synthesis, and where the debt interest is paid
4. **Coverage Manifest:** what couldn't be assessed, and why
5. **Strategic Options:** 2–4 engagement options for your context; you pick
6. **Next Steps:** the top 3–5 recommendations, including deeper reviews with scoped arguments
7. **Follow-up results** (with authority): per review, its scope, headline findings, and tickets; reviews not run, each with a reason; contradictions and breaking-change findings awaiting you

A focused review gives that focus's presentation (for example, the architecture focus's blueprint, or the dead-code focus's calibration followed by tiered findings) and a summary. An honest zero is a valid result, and so is declining tickets.

Cost: without follow-up authority the map is read-only and fast, minutes for a small repo. With it, cost is dominated by the deeper reviews, `/review-security` in particular.

## Worked Examples

### Example 1: Default orientation run

```
User: /review-repo
Skill: What's the context? ... May I run follow-up reviews? May I create tickets?
User: Inheriting a work repo. No to both for now.

Context: inheriting; whole repo; class: production-service (O3, O7, O12)
Findings: test health Foundational (34% coverage, O18); architecture Adequate
  with billing/ coupling (O22, O24); one Safety Hazard — secrets in config/dev.env (O31)
Options: A. Adopt with compensating controls  B. Remediate before extending
Next steps:
  1. Rotate the credentials in config/dev.env (O31)
  2. /review-test src/billing/ src/invoices/
  3. /review-repo architecture services/billing/
  4. /review-security — dependency audit flagged 2 high CVEs (O27)

I can run /review-test, the architecture focus, and /review-security on those scopes now. Want me to?
```

### Example 2: Follow-up authority, no ticket authority

```
Grants: follow-up yes; tickets no.

dead-code src/          — 14 PROVEN dead symbols, 3 dead files
architecture services/billing/ — 2 blueprint items (coupling); built on the
                          dead-code audit rather than re-cataloging it
/review-security        — 1 HIGH (unvalidated redirect, web/auth.go:88); 2 CVEs confirmed
Not run:
  /review-a11y   — no web UI in scope (server-rendered JSON API only, O9)
  /review-perf   — no perf-sensitive signals in Observe

Proposed ticket set (7 tickets):
  - Rotate and remove committed credentials (map: Safety Hazard)
  - Fix unvalidated redirect in web/auth.go (security: HIGH)
  - Remove 14 dead symbols and 3 dead files (dead-code: PROVEN)
  - Break billing → invoices cyclic dependency (architecture)
  ...
Create these?
```

### Example 3: Both grants

```
Grants: follow-up yes; tickets yes, floor High.

/review-security — 1 HIGH → ticket #212 created; 3 MEDIUM recorded
/review-test     — 2 HIGH coverage gaps on payment paths → #213, #214; 5 LOW recorded
architecture     — proposes renaming an exported package used by two other services:
                   breaking change → escalated, not ticketed

Report ends with:
  Tickets created: #212, #213, #214
  Below floor (reported, not ticketed): 3 MEDIUM, 5 LOW
  Awaiting you: the architecture focus's breaking-change recommendation (both options laid out)
```

## Reference Classes

The reference classes live in `classes/` (`solo-utility`, `production-service`, `oss-library`, `prototype`). [`classes/README.md`](classes/README.md) explains the classification philosophy and how to add a class.
