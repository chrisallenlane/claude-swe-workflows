# /review-health — Holistic Repository Review

## Overview

`/review-health` is the holistic review for a repository. By default it produces an evidence-cited map of the repo's state, calibrated to a reference class, designed to inform strategic decisions about how to engage with the project. Given authority up front, it also runs the specialist reviews the map calls for, consolidates what they find, and tickets it — the comprehensive review that `/lead-review` used to provide, without its fixed pipeline. It never changes code.

Use it when you want to step back and assess a repo *strategically*, and optionally to go deep exactly where the map says depth is warranted.

## Core Design

**OODA-structured workflow.** Observe → Orient → Decide → Act, with strict phase gates. The Observe phase collects signals without interpretation; Orient applies the calibration rubric; Decide generates strategic options for the user's lens; Act produces a concrete next-step queue. Later phases cite earlier phases. An optional fifth phase, Follow Up, runs only with authority.

**Reference-class calibration.** "Good" is a relational claim — a 34% test-coverage finding means something different for a research prototype than for an OSS library. The skill classifies the target repo into a reference class first (see `classes/`), then applies class-specific rubrics to each dimension.

**Evidence-cited findings.** Every claim carries a `file:line` citation or a tool-output reference. A finding without evidence is dropped or moved to the Coverage Manifest.

**Coverage Manifest as first-class output.** Tools that couldn't run, signals that couldn't be computed, and dimensions that couldn't be assessed are explicitly named with the reasons they couldn't be resolved. Named unknowns beat silent unknowns.

**Lens-aware output.** The skill elicits your context at invocation (inheriting a work repo / evaluating FOSS / revisiting your own / onboarding a teammate / other) and shapes the Decide-phase options accordingly.

**The map decides the depth.** There is no fixed sequence of specialist reviews. With follow-up authority, the skill runs a specialist because the map gives it something to look at, scoped to the region the findings point at — and gives a one-line reason for every specialist that plausibly applied but did not run.

## Authority

Asked in the same exchange as the lens. Both grants default to no.

| Grant             | Question                                                                                            | If granted                                                       | If not                                                        |
|-------------------|-----------------------------------------------------------------------------------------------------|------------------------------------------------------------------|---------------------------------------------------------------|
| Follow-up reviews | May I run the specialist reviews the map calls for? Some, like `/review-security`, are heavy        | Phase 5 runs them                                                | Phase 4 recommends them; the run ends by offering to run them |
| Tickets           | May I create tickets at or above a severity floor without asking again? Which floor (default High)? | Specialists' ticket proposals at or above the floor are approved | One consolidated ticket set is proposed for your approval     |

| Follow-up | Tickets | What you get                                                                                                            |
|-----------|---------|-------------------------------------------------------------------------------------------------------------------------|
| no        | no      | The cheap, fast orientation map, ending with recommendations and an offer to run the follow-ups                         |
| no        | yes     | Not offered: the ticket question is asked only when follow-ups are granted                                              |
| yes       | no      | Map plus the specialist reviews it calls for; one consolidated ticket set proposed at the end, created only on approval |
| yes       | yes     | Map plus specialist reviews; tickets at or above the floor created as the run goes, the rest reported                   |

Granting tickets *is* the approval to create them. Without the grant, nothing is created unasked.

## Workflow

```
┌──────────────────────────────────────────────────────────────┐
│                       REVIEW-HEALTH                          │
├──────────────────────────────────────────────────────────────┤
│  Phase 0 — Preflight                                         │
│    • Lens, scope, and the two grants                         │
│  Phase 1 — OBSERVE (no interpretation)                       │
│    • Repo, git history, tooling, docs; Coverage Manifest     │
│  Phase 2 — ORIENT                                            │
│    • Reference class; rubric per dimension; severity tiers   │
│  Phase 3 — DECIDE                                            │
│    • 2-4 strategic options for your lens                     │
│  Phase 4 — ACT                                               │
│    • Top 3-5 recommendations; scoped sibling routing         │
│              │                                               │
│     follow-up authority? ── no ──▶ offer follow-ups; stop    │
│              │ yes                                           │
│              ▼                                               │
│  Phase 5 — FOLLOW UP                                         │
│    • Run the specialists the map calls for, scoped           │
│    • Consolidate and dedupe findings                         │
│    • Tickets: create (granted) or propose (not granted)      │
│    • Breaking changes / contradictions → you                 │
└──────────────────────────────────────────────────────────────┘
```

### Phase 5 — Follow Up

**Candidates:** `/review-dead`, `/review-arch`, `/review-security`, `/review-perf`, `/review-a11y`, `/review-test`, `/review-release` — each run only if the map gives it something to look at, and scoped to the region its findings point at.

**Order** so that earlier reviews inform later ones: dead code before architecture, so `/review-arch` isn't analyzing code that should be deleted; release readiness last.

**Never run here:**

| Skill                        | Why                                                                   |
|------------------------------|-----------------------------------------------------------------------|
| `/review-code`               | It reviews a diff; a repository review has none                       |
| `/review-value`              | Only if your intent asks for it — its trade menu is product decisions |
| `/review-namespace` (search) | Search mode needs operator calibration                                |

**Tickets.** Each specialist ends with a ticket proposal. With ticket authority, the skill approves proposals at or above the floor and declines the rest, recording them for the report. Without it, every proposal is declined within the run and one consolidated set is proposed at the end — every finding, ordered by severity, for you to trim — created only on approval.

**Consolidation.** Findings several reviews raised are deduped — `/review-arch` re-finding dead code that `/review-dead` already reported is a confirmation, not a second finding. Specialist findings are reconciled with the map; where a specialist contradicts the map, the deeper review wins and the contradiction is reported.

**Escalation.** A recommended fix that would need a breaking change, or two specialists contradicting each other on the same code, goes to you with both positions. Long runs keep `REVIEW_HEALTH_STATE.md` (gitignored) with the pinned intent and which reviews have run, so they can resume after compaction.

## Reference Materials

| File                            | Purpose                                                                                                |
|---------------------------------|--------------------------------------------------------------------------------------------------------|
| `severity-tiers.md`             | ASHI-style severity taxonomy (Safety Hazard / Major / Minor / Cosmetic) applied to individual findings |
| `classes/README.md`             | Classification philosophy + how-to-add-a-class guide                                                   |
| `classes/solo-utility.md`       | Solo or small-team CLI / utility / internal tool                                                       |
| `classes/production-service.md` | Team-maintained production service or backend                                                          |
| `classes/oss-library.md`        | OSS library with external consumers                                                                    |
| `classes/prototype.md`          | Prototype / research / pre-production exploratory codebase                                             |

## When to Use

**Use `/review-health` for:**

- Strategic overview of a repo you've just inherited
- Evaluating a FOSS project for adoption or contribution
- Revisiting your own project to decide where to invest effort
- Generating an onboarding map for a new teammate
- A comprehensive review that produces a backlog — grant follow-up and ticket authority
- Any "where am I, where should I start, what should I avoid" question

**Don't use `/review-health` for:**

- Finding specific bugs → `/bug-hunt`, or `/bug-fix` for a known one
- Making changes → `/implement`, `/refactor`
- Reviewing a specific diff → `/review-code`
- A single deep review you already know you want → run that specialist directly (`/review-arch`, `/review-test`, `/review-security`, `/review-perf`)

**Rule of thumb:** `/review-health` answers "what is this repo, and what does that mean for me?" Every specialist answers a deeper, narrower question. With authority, `/review-health` decides which of those questions are worth asking and asks them.

## What the Output Looks Like

The skill presents its report inline as structured markdown, in this order:

1. **Context** — your lens, scope, grants, and the repo's reference class (with evidence and override instructions)
2. **Observation Record** — factual signals grouped by category, ID-referenced (`O1`, `O2`, ...)
3. **Findings (Orient)** — per-dimension rubric placement (Foundational / Adequate / Strong) with cited evidence; severity-tiered individual findings within each dimension; cross-cutting synthesis
4. **Coverage Manifest** — what couldn't be assessed, with reasons
5. **Strategic Options (Decide)** — lens-specific engagement options, each citing Orient findings
6. **Next Steps (Act)** — top 3-5 prioritized recommendations, including sibling-skill invocations with scoped arguments
7. **Follow-up results** (Phase 5 only) — per specialist: scope, headline findings, tickets created or proposed; specialists not run, each with a one-line reason; contradictions and breaking-change findings awaiting you

## Worked Examples

### Example 1: Default orientation run

```
User: /review-health
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
  3. /review-arch services/billing/
  4. /review-security — dependency audit flagged 2 high CVEs (O27)

I can run /review-test, /review-arch, and /review-security on those scopes now. Want me to?
```

### Example 2: Follow-up authority, no ticket authority

```
Grants: follow-up yes; tickets no.

[Phases 1–4 as usual]
[Phase 5]
/review-dead src/       — 14 PROVEN dead symbols, 3 dead files
/review-arch services/billing/ — 2 Major coupling findings; its dead-code
                          catalog matched /review-dead (deduped as confirmation)
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
/review-arch     — proposes moving pricing into its own module, which would
                   rename an exported package used by two other services:
                   breaking change → escalated, not ticketed

Report ends with:
  Tickets created: #212, #213, #214
  Below floor (reported, not ticketed): 3 Medium, 5 Low
  Awaiting you: /review-arch's breaking-change recommendation (both options laid out)
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

## Intellectual Foundations

The skill draws on practitioner traditions that have solved "rapid assessment of unfamiliar systems under uncertainty" at higher stakes than software review:

- **OODA loop** (Boyd) — Observe before Orient; Orient is the step most commonly skipped
- **Medical differential diagnosis** — enumerate candidates with evidence for/against before committing
- **Home inspection (ASHI)** — severity-tiered findings with mandatory evidence
- **Marine surveying** — reference-class calibration ("good for a 30-year cargo ship" ≠ "good for a 2-year yacht")
- **Technical due diligence (M&A)** — decision-oriented report structure; known-risks and known-unknowns both surfaced
- **Intelligence situational-awareness briefings** — BLUF + confidence-calibrated assessments + collection gaps

## Agent Usage

The map is primarily produced by the main Claude instance. Subagents are used narrowly:

- **Observe-phase scouts (optional):** parallel subagents for discrete signal-collection tasks on large repos
- **SME consultation (optional, narrow):** for single dimensions requiring specialized language/domain knowledge
- **Specialist reviews (Phase 5, with authority):** each runs as its own skill with its own agents

Per-language SME dispatch is *not* the default. That was an earlier version's failure mode.

## Resource Profile

Never changes code. Without follow-up authority it is read-only and fast: a small repo (<5k LOC) completes in minutes; a large monorepo takes longer, mostly in Observe. With follow-up authority, cost is dominated by the specialists it runs — `/review-security` in particular is heavy by design — which is why the grant is asked for explicitly. Scope can be narrowed at Preflight to manage cost.
