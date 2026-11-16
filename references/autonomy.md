# Autonomy — Design Discipline for Skills That Act on Granted Authority

This document states the autonomy discipline that governs the plugin's autonomous skills — the ones that act on authority granted up front: `/implement` when it runs multi-ticket or unattended work, `/bug-hunt` when its commander's intent grants ticket or fix authority, and `/review-repo` when its intent grants follow-up or ticket authority. These skills are designed to run for long stretches without operator involvement. The discipline below codifies how they decide when to escalate, what an escalation looks like, and what to do when they can't.

It is opinionated, plugin-wide for these autonomous skills, and cited from each of them. New escalation points or handoff formats invented by a single skill should be reconciled against this document; the goal is a coherent operator experience across them.

## Thesis

> Autonomy is the default for autonomous skills; escalation is the exception. When escalation happens, it must be high-altitude, structured, and cheap to answer.

The failure mode this discipline counters: the operator runs many parallel sessions, leaves an autonomous skill running, and returns hours later to an interruption — a granular question, a low-altitude judgment call, an open-ended "what should I do?" The operator lacks the context to answer well. Either the operator reloads context for every interruption (defeating autonomy) or rubber-stamps Claude's recommendation (making the escalation ceremonial). Neither outcome is what the discipline of the andon cord is supposed to produce.

The lineage is mixed: the **andon cord** itself comes from the Toyota production system, where any worker on the line could pull the cord to stop production when something was wrong. **Commander's intent** comes from military doctrine — mission command, where subordinates are given the *why* and are trusted to execute the *how* without micromanagement. **The OODA loop** (behind the autonomous skills' work loops) comes from John Boyd. **Reversibility and blast radius** are widely used in operations and incident response. This discipline composes them into a coherent stance: autonomy is the default, the andon cord is the exception, and the exception is structured so it earns its keep.

## The five levers

These five levers govern how an autonomous skill behaves between startup and termination.

### 1. Altitude rule

> Never escalate below the architectural / intent level.

Implementation-detail forks get the skill's best judgment plus a state-doc log entry. Operator escalations are reserved for decisions the operator can answer *cold* — without watching the run.

Worked examples:

 | Situation                                                                        | Altitude                  | Action                                     |
 |----------------------------------------------------------------------------------|---------------------------|--------------------------------------------|
 | "Use `argon2` or `bcrypt` for password hashing?"                                 | Implementation detail     | Pick one. Log the rationale.               |
 | "The codebase has no auth model and the ticket assumes one exists."              | Architectural / intent    | Escalate.                                  |
 | "Reviewer suggests renaming `helper.go` to `util.go`. Reasonable but contested." | Implementation detail     | Pick one. Log the rationale.               |
 | "Two reviewer skills produce contradictory findings on the same file."           | Intent (product judgment) | Escalate.                                  |
 | "Refactor proposes deleting a public API that may have external consumers."      | Reversibility / contract  | Escalate.                                  |
 | "Test coverage on a non-critical helper module is 60%."                          | Threshold judgment        | Apply severity threshold. Log if deferred. |
 | "A constraint in commander's intent appears to conflict with a key task."        | Intent                    | Escalate.                                  |

The principle: if a competent operator could answer the question after a 30-second skim of the state doc, it might be high enough altitude to escalate. If answering requires watching the last hour of the run, it's too low.

### 2. Pre-loaded options

> Every escalation includes 2–3 named options, an explicit recommendation, and the one tradeoff that would flip the recommendation.

Never "what should I do?" The operator should be able to decide in 30 seconds rather than think from scratch.

Each option has:

- **A short name** (e.g., "Defer," "Rewrite," "Punt to follow-up").
- **A one-sentence rationale** — why this option exists, what it would look like to take it.
- **The expected outcome** if the option is selected — what the run does next.

The escalation must end with:

- **Recommendation** — which option the skill prefers, and the one short reason.
- **What would flip it** — a single sentence describing the consideration that, if true, would make a different option preferable. The operator can scan this and confirm the recommendation or override based on knowledge the skill doesn't have.

### 3. Pre-rebutted recommendation

> The recommendation arrives with its own counterargument.

Before the operator reads the recommendation, the skill has already steelmanned the strongest case against it. The operator does not have to ask "is there a flaw I'm missing?" — the flaw is on the page.

This serves two purposes:

- It saves the operator a thinking cycle (the "what's wrong with this?" reflex).
- It forces the skill to actually consider whether its recommendation is right, rather than producing the most plausible-sounding output.

The pre-rebuttal should be specific and substantive. "It has trade-offs" is not a pre-rebuttal. "Choosing option A locks us into the schema migration before we know whether the v2 API will actually need it" is.

### 4. Commander's intent

> What is elicited upfront and frozen for the duration.

Each autonomous skill has a commander's-intent schema — the structured information it captures from the operator before the autonomous phase begins. The schema is skill-specific, because the skills differ in purpose. The schemas are documented here so they stay aligned across these skills and so each skill can cite this section instead of re-defining its own.

The principle: anything not captured in commander's intent becomes implicit, and implicit assumptions are the source of granular escalations later. Invest time at startup. The structure is load-bearing.

### 5. Risk budgets

> Explicit caps the skill spends before escalating.

Two budget categories are blessed plugin-wide:

- **Iteration cap** — maximum cycles, loop iterations, or batches the skill runs before forcing a stop. Examples: `/implement` caps at 50 actions; `/bug-hunt` caps at 10 hunt rounds; per-ticket retry attempts bounded.
- **Retry cap** — maximum consecutive failures of the same kind before escalating. Examples: `/implement` retries acceptance verification 3 times; the correctness review in `/implement` escalates after 3 rounds.

Two budget categories are explicitly **not** part of the discipline:

- **File-touch budgets** — "may not modify more than N files." Considered and rejected: a low ceiling breaks legitimate large refactors; a high ceiling provides no real bound.
- **Dependency-change budgets** — "may not add/remove more than N dependencies." Considered and rejected: dependency choices are governed by constraints in commander's intent, not by a count.

Skills can introduce additional skill-specific budgets if they earn their keep, but file-touch and dependency-change budgets should not be reintroduced under different names.

## Cascade rule

> Worker → caller → user. Not worker → user.

When an orchestrator invokes a sub-skill (e.g., `/bug-hunt` with fix authority invokes `/implement`), the sub-skill's escalations cascade up to the orchestrator, not directly to the operator. The orchestrator decides whether to resolve the escalation itself or to pull its own andon cord at a higher altitude.

`/implement`'s "Invoked by Another Skill" contract makes this explicit: when a caller supplies the tickets and constraints, `/implement`'s escalations go to the caller, which decides whether to escalate further. The same holds inside `/implement` itself: escalations from the agents and skills it runs come to it first.

The deepest skill never goes around its caller. The caller has more context about the project than the worker does. Worker escalations are *cause* (something went wrong); caller escalations are *effect* (we couldn't fix it from this altitude).

## Auto-approval of sub-skill ticket proposals

Advisory sub-skills (`/bug-hunt` by default, `/review-repo` and its focused reviews, `/review-security`, `/review-test`) produce ticket *proposals* that require operator approval in their native contract. Under an autonomous skill, those approvals are answered automatically by the orchestrator rather than escalated to the operator.

This is a deliberate contract shift consistent with the autonomy discipline:

- **Commander's intent authorizes the work.** The operator's startup choices (scope, severity floor, ticket and follow-up authority) are the standing answer to whatever approval prompts the sub-skills would have asked.
- **Sub-skill prompts are answered by the orchestrator** per the cascade rule — the operator is not in the loop between cycles or phases.
- **The completion report lists every ticket action** (created, declined, modified) so the operator can audit the contract shift after the run.

How each autonomous skill handles the contract shift:

| Skill          | Behavior                                                                                                                                                                                 |
|----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `/bug-hunt`    | With ticket authority, creates tickets for its own confirmed findings at or above the severity floor; without it, proposes them for operator approval.                                   |
| `/review-repo` | With ticket authority, approves its deeper reviews' proposals at or above the floor and declines the rest; without it, declines them all and proposes one consolidated set for approval. |
| `/implement`   | Approves, edits, or declines with judgment; prefers cutting a ticket when in doubt, since a decline commits the run to doing the work inline.                                            |

Sub-skills surface contested findings and breaking-change requirements as andon-cord triggers rather than auto-approval candidates. The contract shift covers ordinary approval prompts; substantive disagreement still routes through the operator.

## No unilateral breaking changes

> Breaking changes must be explicitly authorized by the operator.

This is a categorical guardrail, not an altitude judgment. The five levers describe how a skill decides between options; this rule constrains the option set itself. An autonomous skill must not introduce a breaking change without operator authorization — no matter how confident it is, how clear the rationale, or how strong the consensus among sub-agents.

A breaking change is any modification that requires downstream consumers — humans, scripts, or systems — to update to keep working. Concrete examples:

- Removing or renaming a public API symbol (exported function, type, module).
- Changing the signature of a public function in a non-additive way.
- Removing or renaming a CLI flag, command, or subcommand.
- Removing or renaming a configuration key.
- Non-backwards-compatible schema migrations.
- Changes to wire-protocol fields, message types, or serialization formats that break existing payloads.
- Removing or renaming an emitted event, log field, or metric that consumers may depend on.

When a sub-skill or sub-agent proposes a breaking change as part of a larger plan, the orchestrator pulls the andon cord — even if the rest of the plan is sound. The escalation lists the breaking change explicitly as one option, presents the non-breaking alternative as another, and recommends per the pre-loaded-options conventions of lever 2.

The bound is categorical because breaking changes are reversible only by reverting commits — and sometimes only by coordinating with downstream consumers. A state-doc log entry cannot recover from one after the fact the way it can for, say, a rename inside an internal package. The cost of asking is small; the cost of finding out an unannounced break shipped is large.

This rule does not apply when the operator has authorized the break — in commander's intent, in the ticket body, or in an answer to a prior andon-cord pull. It also does not apply to internal refactors that touch only private APIs; those are governed by the altitude rule.

## Commander's-intent schemas per skill

The schemas below define what each skill elicits upfront. A skill may extend its schema with additional fields, but should not reduce the listed fields without revising this document.

### `/implement`

**No fixed schema.** `/implement` asks only what the user can answer and the work needs: the requirements or tickets; constraints and non-goals, for multi-ticket work the tickets don't already bound; `/refactor`'s two stakes questions (*what happens if this breaks?* and *who maintains it, for how long?*), when `/refactor` is likely to run; and a smoke-testing procedure, when the work spans user-visible features. It presents these with its plan in one interaction and records the result as the **approved intent**, which anchors every later decision. When a calling skill supplies the tickets and constraints, the caller's intent is the approved intent and nothing is elicited.

### `/bug-hunt`

Five fields:

- **Scope** — what to hunt, with exclusions (defaults: production code; tests, dev tooling, generated and vendored code excluded).
- **Severity floor** — findings at or above it block convergence; findings below it are reported only. Defaults to High. This is the dominant judgment call: too low and the hunt never converges; too high and known bugs are left standing.
- **Constraints** — hard limits beyond the always-on guardrails (no breaking changes, no main/master writes).
- **Tickets** — authority to create tickets for confirmed findings without asking again. Defaults to no: a ticket proposal is presented for approval at the end.
- **Fix** — authority to fix confirmed findings on a branch via `/implement` and re-hunt. Defaults to no.

With both authority fields at their defaults the skill is advisory and changes nothing outside its report until the operator approves. Purpose and end state are implicit: find the bugs at or above the floor; end when a hunt round confirms nothing at or above it, or at the 10-round cap.

### `/review-repo`

The lens (what the operator is doing — inheriting, evaluating, revisiting, onboarding), the scope, and two grants, both defaulting to no:

- **Follow-up reviews** — authority to run the deeper reviews the map calls for (the `dead-code`, `architecture`, and `namespace` (audit mode) focuses, `/review-security`, `/review-perf`, `/review-a11y`, `/review-test`, `/review-release`). Without it, they are recommended only.
- **Tickets** — authority to create tickets at or above a severity floor (default High) without asking again. Without it, one consolidated ticket set is proposed for approval.

With neither grant the skill is a fast orientation pass that changes nothing.

## Shared handoff template

The template below is the canonical structure for andon-cord pulls across the autonomous skills. Skills must use this structure when escalating to the operator; skill-specific extensions go inline as additional fields, not as replacements.

```markdown
## Andon Cord — <Skill> — <Phase / Cycle>

### Project orientation (30-second reorient)

[One paragraph for an operator returning cold. What is this project, where
 does it stand right now, what has changed since they last looked.
 Key-task status: done / in progress / deferred. Major recent milestones.
 Skip project background the operator already knows — focus on state that
 has changed during this run.]

### What I was trying to do

[The key task, intent item, or sub-skill goal driving this cycle.]

### What went wrong

[Specific failure mode. Concrete, not vague. Cite commits, file paths,
 test names, error messages.]

### Pre-loaded options

**Option A — <short name>**
[One sentence: what this option does. What the run looks like if chosen.]

**Option B — <short name>**
[One sentence: what this option does. What the run looks like if chosen.]

**Option C — <short name>** (if applicable)
[One sentence: what this option does. What the run looks like if chosen.]

### Recommendation

**[Option chosen]** — [one short reason].

**Pre-rebutted counterargument:** [the strongest case against the
recommendation, specifically. Not "trade-offs exist" — the actual flaw.]

**What would flip this:** [a single sentence describing the consideration
that, if true, would change the recommendation.]

### Current state

- Branch: <name> (at SHA <short>)
- Commits on branch: N
- Tests: <pass/fail with detail>
- Build: <pass/fail>
- Key tasks: <K of M complete>
- Sub-skill state: <if applicable, what the sub-skill was doing>

### To resume

[Concrete instructions: how to re-invoke the skill after the blocker
 is resolved. Reference any state docs.]
```

Skills may add fields below "Current state" that are specific to their workflow (e.g., `/implement` includes what is merged, what is in flight, and which tickets remain). They should not add fields *between* "Pre-loaded options" and "Recommendation" — that ordering is load-bearing.

## Per-skill handoff extensions

Each autonomous skill extends the shared template in two predictable ways:

1. **Title** — `## Andon Cord — /<skill> — <phase identifier>` where the phase identifier varies per skill (round number for `/bug-hunt`; current phase or deeper review for `/review-repo`; current action for `/implement`). The phase identifier is load-bearing — the same skill may pull the cord at different points and the operator needs to know which one.
2. **Current-state additions** — skill-specific fields appended after the shared baseline (typically convergence counters, findings-ledger summaries, a state-doc pointer). Skills should not add fields *between* "Pre-loaded options" and "Recommendation" — that ordering is load-bearing.

After pulling the cord, the skill stops. It does not attempt additional cycles or phases. It waits for operator input.

The opening framing in each autonomous skill's andon-cord section is uniform: *the andon cord is the only planned escalation path; pull sparingly but decisively; use the shared handoff template, with the skill-specific extensions below.* Skills should not re-litigate the autonomy discipline at this point — it has already been established by the citation back to this document at the top of the skill.

## What to log instead of escalate

The altitude rule (lever 1) says "implementation-detail forks get the skill's best judgment plus a state-doc log entry." This section enumerates concrete examples so future skill maintainers know what *doesn't* warrant escalation.

 | Situation                                                                          | Resolution                                                                      | Log entry                                                                                      |
 |------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|
 | Implementer names a function `parseInput` vs `parseRequest`; no convention decides | Pick the more specific one.                                                     | "Named `parseRequest` for clarity; `parseInput` was equally idiomatic."                        |
 | Code reviewer suggests deleting a helper; another invocation argues to keep        | Apply default policy (deletion wins if no caller references and no test fails). | "Removed `unusedHelper`; code reviewer flagged unused; no callers found."                      |
 | Test review surfaces a coverage gap on a non-critical helper, severity low         | Defer to final report. Do not block termination.                                | "Deferred: low-coverage helper `pkg/util/format`; rationale: non-critical, no recent changes." |
 | Two implementers return functionally equivalent implementations                    | Pick one (the simpler diff).                                                    | "Chose implementer A's version; B's was equivalent but had two more lines."                    |
 | `/tidy-docs` flags wording as unclear; the agent didn't propose a rewrite          | Improve wording with judgment; commit if improvement is clear.                  | "Rewrote intro paragraph; `/tidy-docs` flagged ambiguity in two sentences."                    |
 | Severity classification of a finding is borderline (medium vs low)                 | Use the lower severity if either is defensible.                                 | "Classified `<finding>` as low; architecture review borderline medium."                        |

The log entry is the contract: the operator can grep the state doc post-run to see what the skill decided unilaterally and why. If the operator disagrees, they can revert the specific commit or revisit the decision. The cost of a log entry is much less than the cost of an interruption.

## Advisory aspiration for `/review-*` skills

Direction, not strictly enforced today. Review skills should produce reports and not implement changes. The principle: review and implementation are different concerns. A skill that does both makes both worse — implementation pressure can compromise the review, and review pressure can compromise the implementation.

Status as of this document:

 | Skill              | Status                                                                                                                          |
 |--------------------|---------------------------------------------------------------------------------------------------------------------------------|
 | `/review-test`     | Advisory as of v9.0.0.                                                                                                          |
 | `/review-a11y`     | Already advisory.                                                                                                               |
 | `/review-repo`     | Advisory; absorbed `/review-arch` (advisory since v8.0.0), `/review-dead`, `/review-value`, and `/review-namespace` in v12.0.0. |
 | `/review-perf`     | Already advisory.                                                                                                               |
 | `/review-security` | Advisory as of v8.0.0.                                                                                                          |
 | `/review-release`  | Effectively advisory (presents findings for operator review).                                                                   |

The path forward: when a `/review-*` skill becomes advisory, its findings should name specific implementation skills with scope hints so the operator (or a calling orchestrator) can chain the right next step. Example: "Dead code in `src/foo/`: work the sweep ticket with `/implement`."

Skills whose find→fix seam is small enough to keep find-and-fix fused live in the `/tidy-*` namespace instead (e.g., `/tidy-docs`, `/tidy-git`). Those skills are not advisory by design — they default to acting on safe categories. The principled distinction: `/review-*` = produces a report, no mutations; `/tidy-*` = mechanical mutations with operator approval for borderline-safe categories; `/implement` = substantive mutations driven by tickets.

## What this discipline does NOT do

- **It does not apply to user-facing exploration skills.** `/scope` is intrinsically interactive; the operator is figuring out what to build. The discipline of pre-loaded options and pre-rebutted recommendations may still be valuable in those skills, but the autonomy framing does not.
- **It applies to `/implement` only at scale.** A single ticket run with the operator at the keyboard needs none of this; the operator is right there. The discipline matters when `/implement` runs multi-ticket work after its one planned interaction, or is invoked unattended by another skill.
- **It does not eliminate operator touchpoints.** It eliminates *granular* operator touchpoints. Commander's intent at startup is a touchpoint. The completion report is a touchpoint. Andon-cord pulls are touchpoints — they're just structured to be cheap to answer.
- **It does not pursue agent-side completeness.** Sub-agents (`swe-implementer`, `qa-engineer`, etc.) are workers, not orchestrators. They report findings and complete tasks; they do not escalate. Escalation logic lives at the skill layer.

## Sources

The intellectual lineage of this discipline, in rough order of how directly the ideas are borrowed:

- **Toyota Production System** — the andon cord. Any worker can stop the line when something is wrong. Stopping is virtuous because it surfaces problems before they propagate.
- **Mission command (military doctrine)** — commander's intent. Subordinates are given the *why* and are trusted to execute the *how*. Variants exist across NATO doctrine, the U.S. Marine Corps' MCDP 6, and the German *Auftragstaktik* tradition that precedes both.
- **John Boyd — OODA loop** (1976+). Observe, Orient, Decide, Act. The decision-cycle framework behind the orchestrators' work loops. Useful here as the mental model for what happens *between* andon-cord pulls.
- **Site Reliability Engineering / incident response practice** — blast radius, reversibility, "do-no-harm" defaults. The notion that some actions are cheap to take back and others aren't, and that the difference should drive how cautiously the skill behaves.
- **Rationalist tradition (steelmanning)** — feeds the pre-rebutted-recommendation lever. The recommendation should be tested against its strongest critique before it reaches the operator.

## Evolution

This document changes with the autonomous skills, but deliberately. A change to autonomy.md is a meaningful event that should be reflected in the cited skills. New escalation patterns invented in a single skill should either be reconciled here or rejected.

Skills that drift from this discipline are candidates for revision. The cost of the discipline is uniformity and a slightly higher bar for new escalation points; the benefit is that an operator who has used one autonomous skill knows what to expect from another.
