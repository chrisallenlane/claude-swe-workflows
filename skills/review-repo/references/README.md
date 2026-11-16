# /review-repo — Reviewing a Codebase as a Whole

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

Several focuses can be named together (`/review-repo value dead-code architecture`); they run in dependency order. A focus naming another review skill (`security`, `test`, `perf`, `a11y`, `release`) is routed to that skill.

Before v12 these focuses were separate skills: `/review-arch`, `/review-dead`, `/review-value` and `/review-namespace`. Their methods live in their agents and are unchanged; only the entry point moved.

## Core Design

**OODA-structured workflow.** Observe → Orient → Decide → Act, with strict phase gates. The Observe phase collects signals without interpretation; Orient applies the calibration rubric; Decide generates strategic options for your context; Act produces a concrete next-step queue. Later phases cite earlier phases. An optional fifth phase, Follow Up, runs only with authority.

**Reference-class calibration.** "Good" is a relational claim — a 34% test-coverage finding means something different for a research prototype than for an OSS library. The skill classifies the target repo into a reference class first (see `classes/`), then applies class-specific rubrics to each dimension.

**Evidence-cited findings.** Every claim carries a `file:line` citation or a tool-output reference. A finding without evidence is dropped or moved to the Coverage Manifest.

**Coverage Manifest as first-class output.** Tools that couldn't run, signals that couldn't be computed, and dimensions that couldn't be assessed are explicitly named with the reasons they couldn't be resolved. Named unknowns beat silent unknowns.

**Debt located by its interest, not its look.** Technical debt can't be read off a snapshot: ugly code that nobody changes costs nothing. The Observe phase crosses per-file complexity with change frequency from git history to find *hotspots* — complex code that keeps changing, where every change pays interest — and finds *change coupling*: files that keep changing together with no static dependency between them, a hidden contract. Orient reads them as a quadrant: debt being paid (engage), dormant cruft (usually leave alone), active healthy code, settled code. Confirmed hotspots become scoped `/refactor` recommendations; hidden coupling routes to the `architecture` focus. On thin or squash-merged history the signals are weak, and the Coverage Manifest says so.

**Context-aware output.** The map elicits your context at invocation (inheriting a work repo / evaluating FOSS / revisiting your own / onboarding a teammate / other) and shapes the Decide-phase options accordingly.

**The map decides the depth.** There is no fixed sequence of deeper reviews. With follow-up authority, the skill runs one because the map gives it something to look at, scoped to the region the findings point at — and gives a one-line reason for every review that plausibly applied but did not run.

## Authority

For the map only, asked in the same exchange as the context. Both grants default to no.

| Grant             | Question                                                                                            | If granted                                                       | If not                                                        |
|-------------------|-----------------------------------------------------------------------------------------------------|------------------------------------------------------------------|---------------------------------------------------------------|
| Follow-up reviews | May I run the deeper reviews the map calls for? Some, like `/review-security`, are heavy            | Phase 5 runs them                                                | Phase 4 recommends them; the run ends by offering to run them |
| Tickets           | May I create tickets at or above a severity floor without asking again? Which floor (default High)? | Reviews' ticket proposals at or above the floor are approved     | One consolidated ticket set is proposed for your approval     |

| Follow-up | Tickets | What you get                                                                                                            |
|-----------|---------|-------------------------------------------------------------------------------------------------------------------------|
| no        | no      | The cheap, fast orientation map, ending with recommendations and an offer to run the follow-ups                         |
| no        | yes     | Not offered: the ticket question is asked only when follow-ups are granted                                              |
| yes       | no      | Map plus the deeper reviews it calls for; one consolidated ticket set proposed at the end, created only on approval     |
| yes       | yes     | Map plus deeper reviews; tickets at or above the floor created as the run goes, the rest reported                       |

Granting tickets *is* the approval to create them. Without the grant, nothing is created unasked.

## Workflow

```
┌──────────────────────────────────────────────────────────────┐
│                  REVIEW-REPO (the map)                       │
├──────────────────────────────────────────────────────────────┤
│  Phase 0 — Preflight                                         │
│    • Context, scope, and the two grants                      │
│  Phase 1 — OBSERVE (no interpretation)                       │
│    • Repo, git history, change cost, tooling, docs; Coverage │
│      Manifest                                                │
│  Phase 2 — ORIENT                                            │
│    • Reference class; rubric per dimension; severity tiers;  │
│      where the debt interest is paid                         │
│  Phase 3 — DECIDE                                            │
│    • 2-4 strategic options for your context                  │
│  Phase 4 — ACT                                               │
│    • Top 3-5 recommendations; scoped sibling routing         │
│              │                                               │
│     follow-up authority? ── no ──▶ offer follow-ups; stop    │
│              │ yes                                           │
│              ▼                                               │
│  Phase 5 — FOLLOW UP                                         │
│    • Run the reviews the map calls for, scoped               │
│    • Consolidate and dedupe findings                         │
│    • Tickets: create (granted) or propose (not granted)      │
│    • Breaking changes / contradictions → you                 │
└──────────────────────────────────────────────────────────────┘
```

### Phase 5 — Follow Up

**Candidates:** the `dead-code` and `architecture` focuses, `/review-security`, `/review-perf`, `/review-a11y`, `/review-test`, `/review-release` — each run only if the map gives it something to look at, and scoped to the region its findings point at.

**Order** so that earlier reviews inform later ones: dead code before architecture, so the blueprint isn't built around code that should be deleted; release readiness last.

**Never run here:**

| Skill                      | Why                                                                   |
|----------------------------|-----------------------------------------------------------------------|
| `/refactor`, `/implement`  | They change code; recommended in Phase 4, never run                   |
| The `value` focus          | Only if your intent asks for it — its trade menu is product decisions |
| `namespace` in search mode | Search mode needs operator calibration; audit mode may run            |

**Tickets.** Each deeper review ends with a ticket proposal. With ticket authority, the skill approves proposals at or above the floor and declines the rest, recording them for the report. Without it, every proposal is declined within the run and one consolidated set is proposed at the end — every finding, ordered by severity, for you to trim — created only on approval.

**Consolidation.** Findings several reviews raised are deduped — a confirmation is not a second finding. Deeper findings are reconciled with the map; where a deeper review contradicts the map, the deeper review wins and the contradiction is reported.

**Escalation.** A recommended fix that would need a breaking change, or two reviews contradicting each other on the same code, goes to you with both positions. Long runs keep `REVIEW_REPO_STATE.md` (gitignored) with the pinned intent and which reviews have run, so they can resume after compaction.

## Focused Reviews

Every focus runs one fresh agent through the same protocol: scope, analysis, presentation, iteration with you, a ticket offer per the shared advisory pattern, and a summary. During iteration, what you know about liveness, intent, or history counts as evidence. An honest zero is a valid result, and so is declining tickets; the analysis then stands as a planning artifact.

**`architecture`** (`swe-arch-reviewer`) presents three things:
- (a) the noun-frequency table and the per-noun namespace evaluation;
- (b) proposed changes with their rationale: mechanism downgrades, renames, moves, absorptions, dissolutions, and new modules;
- (c) the modules deliberately left alone.

It iterates until you're satisfied, because architectural decisions are consequential. It proposes one ticket per blueprint item, grouped where that makes the work cohesive; cross-module moves recommend `/scope` before `/implement`.

**`dead-code`** (`swe-dead-code-auditor`) leads with the calibration: the dynamic-dispatch survey and the reference roots (entry points, or a library's public API). These tell you how far to trust the rest. Findings are tiered PROVEN / LIKELY / UNVERIFIABLE with evidence, and intentionally retained code is shown separately. UNVERIFIABLE findings become verification tickets, never removal tickets.

**`value`** (`swe-value-engineer`) discovers requirements across provenance tiers (documented, pinned by tests, inferred from behavior), prices them, and presents a trade menu ranked by leverage. Each trade shows its user-visible change, what dissolves, and the estimated savings.

Trades are product decisions. The skill never advocates for a trade, and an orchestrator never rules on one flagged core-requirement, correctness, or security. For an approved trade, the ticket's first acceptance criterion amends the requirement's record (design doc, ADR, README, or spec). An approved trade that changes only code gets rebuilt by the next agent to read the old requirement.

**`namespace`** (`swe-namespace-reader` and `swe-namespace-canary`, following [`namespace.md`](namespace.md)) turns "easy to reason about" into a measurement. A blind writer generates navigation questions from the purpose docs alone. The skill pins each question's ground truth in the code and pre-registers the scoring rules. Cold readers then answer from the file listing alone; they never see the repository. Misses are classified as deceptive locations, placement problems, attractor traps, homonym tax, one-hop conventions, or blind spots, and the readers' own wrong answers are the evidence. A second reader pool primed with the project's style guide stands in for the maintainer.

Audit is the default. **Search** (`/review-repo namespace search`) evolves hypothetical trees, each with an old→new mapping, against the probe battery until it converges. It is heavy (millions of tokens), runs only on explicit opt-in with a round cap, and includes owner-calibration checkpoints where your vetoes outrank every score. The nine Laws of the Instrument, drawn from the field pilot, are in `namespace.md`.

**Combined focuses** run value, then dead code, then architecture, then namespace, each receiving the previous one's output. In search mode, the architecture blueprint is seeded as a candidate tree, so the analyst's proposal is tested by the measurement. Restructuring a requirement you're about to drop is wasted work, and the blueprint shouldn't be built around dead code.

## Reference Materials

| File                            | Purpose                                                                                                |
|---------------------------------|--------------------------------------------------------------------------------------------------------|
| `severity-tiers.md`             | ASHI-style severity taxonomy (Safety Hazard / Major / Minor / Cosmetic) applied to individual findings |
| `classes/README.md`             | Classification philosophy + how-to-add-a-class guide                                                   |
| `classes/solo-utility.md`       | Solo or small-team CLI / utility / internal tool                                                       |
| `classes/production-service.md` | Team-maintained production service or backend                                                          |
| `classes/oss-library.md`        | OSS library with external consumers                                                                    |
| `classes/prototype.md`          | Prototype / research / pre-production exploratory codebase                                             |
| `namespace.md`                  | The `namespace` focus's procedure, loaded only when that focus runs                                    |

## When to Use

**Use `/review-repo` for:**

- Strategic overview of a repo you've just inherited
- Evaluating a FOSS project for adoption or contribution
- Revisiting your own project to decide where to invest effort
- Generating an onboarding map for a new teammate
- A comprehensive review that produces a backlog: grant follow-up and ticket authority
- A structural blueprint (`architecture`), a dead-code audit (`dead-code`), a requirements price list (`value`), or a measured legibility audit of the file tree (`namespace`)
- Finding where technical debt is costing you — and where to aim `/refactor`
- Any "where am I, where should I start, what should I avoid" question

**Don't use `/review-repo` for:**

- Finding specific bugs → `/bug-hunt`, or `/bug-fix` for a known one
- Making changes → `/implement`, `/refactor`
- Reviewing a specific diff: `/implement` and `/bug-fix` run the correctness gate on their own diffs; for anything else, use Claude Code's built-in `/code-review`
- Redesigning toward less machinery: `/refactor` (it changes code on its own branch)

**Rule of thumb:** the map answers "what is this repo, and what does that mean for me?" A focus, or a specialist skill, answers a deeper and narrower question. With authority, the map decides which of those questions are worth asking and asks them.

## What the Output Looks Like

For the map, the skill presents its report inline as structured markdown, in this order:

1. **Context** — your review context, scope, grants, and the repo's reference class (with evidence and override instructions)
2. **Observation Record** — factual signals grouped by category, ID-referenced (`O1`, `O2`, ...)
3. **Findings (Orient)** — per-dimension rubric placement (Foundational / Adequate / Strong) with cited evidence; severity-tiered individual findings within each dimension; cross-cutting synthesis; where the debt interest is paid (hotspots, hidden coupling, dormant cruft)
4. **Coverage Manifest** — what couldn't be assessed, with reasons
5. **Strategic Options (Decide)** — context-specific engagement options, each citing Orient findings
6. **Next Steps (Act)** — top 3-5 prioritized recommendations, including deeper reviews with scoped arguments
7. **Follow-up results** (Phase 5 only) — per review: scope, headline findings, tickets created or proposed; reviews not run, each with a one-line reason; contradictions and breaking-change findings awaiting you

## Worked Examples

### Example 1: Default orientation run

```
User: /review-repo
Skill: What's the context? ... May I run follow-up reviews? May I create tickets?
User: Inheriting a work repo. No to both for now.

[Phases 1–4]
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

[Phases 1–4 as usual]
[Phase 5]
dead-code src/          — 14 PROVEN dead symbols, 3 dead files
architecture services/billing/ — 2 Major coupling findings; built on the
                          dead-code audit rather than re-cataloging it
/review-security        — 1 High (unvalidated redirect, web/auth.go:88); 2 CVEs confirmed
Not run:
  /review-a11y   — no web UI in scope (server-rendered JSON API only, O9)
  /review-perf   — no perf-sensitive signals in Observe
  /review-test   — coverage gaps already specific enough to act on (O18)
  /review-release — not preparing a release

Proposed ticket set (7 tickets):
  - Rotate and remove committed credentials (Safety Hazard)
  - Fix unvalidated redirect in web/auth.go (High)
  - Upgrade lib-x and lib-y past CVE versions (High)
  - Remove 14 dead symbols and 3 dead files
  - Break billing → invoices cyclic dependency (Major)
  - Extract pricing rules from billing handler (Major)
  - Add tests for src/billing/ and src/invoices/ (Foundational test health)
Create these?
```

### Example 3: Both grants

```
Grants: follow-up yes; tickets yes, floor High.

[Phase 5]
/review-security — 1 High → ticket #212 created; 3 Medium recorded
/review-test     — 2 High coverage gaps on payment paths → #213, #214; 5 Low recorded
architecture     — proposes moving pricing into its own module, which would
                   rename an exported package used by two other services:
                   breaking change → escalated, not ticketed

Report ends with:
  Tickets created: #212, #213, #214
  Below floor (reported, not ticketed): 3 Medium, 5 Low
  Awaiting you: the architecture focus's breaking-change recommendation (both options laid out)
```

## Cognitive Failure Modes the Skill Countermands

Each element of the design is a countermeasure to a specific predictable failure of informal repo review:

| Failure mode                                                            | Countermeasure                                                                    |
|-------------------------------------------------------------------------|-----------------------------------------------------------------------------------|
| Inheritor's paralysis / availability bias — fixate on first file opened | Systematic Observe phase with fixed signal battery                                |
| Unknown-unknowns dominance                                              | Coverage Manifest elevates missing tooling to first-class output                  |
| Premature closure                                                       | Phase-integrity gates (Orient cites Observe; Decide cites Orient)                 |
| Expert deference — accept prior-author choices unexamined               | Differential-diagnosis classification forces candidate alternatives with evidence |
| Free-floating adjectives ("health: good")                               | Reference-class calibration with cited per-class rubrics                          |
| Confident false positives ("no references" taken as proof of death)     | The `dead-code` focus surveys dynamic dispatch before tiering anything            |

## Intellectual Foundations

The skill draws on practitioner traditions that have solved "rapid assessment of unfamiliar systems under uncertainty" at higher stakes than software review:

- **OODA loop** (Boyd) — Observe before Orient; Orient is the step most commonly skipped
- **Medical differential diagnosis** — enumerate candidates with evidence for/against before committing
- **Home inspection (ASHI)** — severity-tiered findings with mandatory evidence
- **Marine surveying** — reference-class calibration ("good for a 30-year cargo ship" ≠ "good for a 2-year yacht")
- **Behavioral code analysis** (Tornhill, *Your Code as a Crime Scene*) — change history prices complexity: hotspots and change coupling
- **Technical due diligence (M&A)** — decision-oriented report structure; known-risks and known-unknowns both surfaced
- **Intelligence situational-awareness briefings** — BLUF + confidence-calibrated assessments + collection gaps
- **Value engineering** (Miles, GE, 1947) — price each function the product commits to, and what else would serve

## Agent Usage

The map is primarily produced by the main Claude instance. Subagents are used narrowly:

- **Observe-phase scouts (optional):** parallel subagents for discrete signal-collection tasks on large repos
- **Focused consultation (optional, narrow):** a fresh subagent briefed on a single dimension that needs a deeper look
- **Focus agents:** `swe-arch-reviewer`, `swe-dead-code-auditor`, `swe-value-engineer`, and the namespace reader fleet (`swe-namespace-reader` ×2, `swe-namespace-canary`), with fresh instances for each focus or battery
- **Specialist skills (Phase 5, with authority):** each runs as its own skill with its own agents

Per-language dispatch is *not* the default. That was an earlier version's failure mode.

## Resource Profile

Never changes code. Without follow-up authority it is read-only and fast: a small repo (<5k LOC) completes in minutes; a large monorepo takes longer, mostly in Observe. With follow-up authority, cost is dominated by the deeper reviews it runs — `/review-security` in particular is heavy by design — which is why the grant is asked for explicitly. Scope can be narrowed at Preflight to manage cost.
