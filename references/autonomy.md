# Autonomy — Design Discipline for Orchestrator-Family Skills

This document states the autonomy discipline that governs the orchestrator-family skills in this plugin: `/lead-project`, `/implement-project`, `/implement-batch`, `/refactor-deep`. These skills are designed to run for long stretches without operator involvement. The discipline below codifies how they decide when to escalate, what an escalation looks like, and what to do when they can't.

It is opinionated, plugin-wide for the orchestrator family, and cited from each applicable skill. New escalation points or handoff formats invented by a single skill should be reconciled against this document; the goal is a coherent operator experience across the family.

## Thesis

> Autonomy is the default for orchestrator-family skills; escalation is the exception. When escalation happens, it must be high-altitude, structured, and cheap to answer.

The failure mode this discipline counters: the operator runs many parallel sessions, leaves an autonomous skill running, and returns hours later to an interruption — a granular question, a low-altitude judgment call, an open-ended "what should I do?" The operator lacks the context to answer well. Either the operator reloads context for every interruption (defeating autonomy) or rubber-stamps Claude's recommendation (making the escalation ceremonial). Neither outcome is what the discipline of the andon cord is supposed to produce.

The lineage is mixed: the **andon cord** itself comes from the Toyota production system, where any worker on the line could pull the cord to stop production when something was wrong. **Commander's intent** comes from military doctrine — mission command, where subordinates are given the *why* and are trusted to execute the *how* without micromanagement. **The OODA loop** (already used in `/lead-project`) comes from John Boyd. **Reversibility and blast radius** are widely used in operations and incident response. This discipline composes them into a coherent stance: autonomy is the default, the andon cord is the exception, and the exception is structured so it earns its keep.

## The five levers

These five levers govern how an orchestrator-family skill behaves between startup and termination.

### 1. Altitude rule

> Never escalate below the architectural / intent level.

Implementation-detail forks get the skill's best judgment plus a state-doc log entry. Operator escalations are reserved for decisions the operator can answer *cold* — without watching the run.

Worked examples:

 | Situation                                                                         | Altitude                  | Action                                         |
 | --------------------------------------------------------------------------------- | ------------------------- | ---------------------------------------------- |
 | "Use `argon2` or `bcrypt` for password hashing?"                                  | Implementation detail     | Pick one. Log the rationale.                   |
 | "The codebase has no auth model and the ticket assumes one exists."               | Architectural / intent    | Escalate.                                      |
 | "Reviewer suggests renaming `helper.go` to `util.go`. Reasonable but contested."  | Implementation detail     | Pick one. Log the rationale.                   |
 | "Two reviewer skills produce contradictory findings on the same file."            | Intent (product judgment) | Escalate.                                      |
 | "Refactor would move 12 functions across 3 modules. Boldness is set to moderate." | Boldness governed         | Apply the boldness rubric. Log items deferred. |
 | "Refactor proposes deleting a public API that may have external consumers."       | Reversibility / contract  | Escalate.                                      |
 | "Test coverage on a non-critical helper module is 60%."                           | Threshold judgment        | Apply severity threshold. Log if deferred.     |
 | "A constraint in commander's intent appears to conflict with a key task."         | Intent                    | Escalate.                                      |

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

Each orchestrator-family skill has a commander's-intent schema — the structured information it captures from the operator before the autonomous phase begins. The schema is skill-specific, because the skills differ in purpose. The schemas are documented here so they stay aligned across the family and so each skill can cite this section instead of re-defining its own.

The principle: anything not captured in commander's intent becomes implicit, and implicit assumptions are the source of granular escalations later. Invest time at startup. The structure is load-bearing.

### 5. Risk budgets

> Explicit caps the skill spends before escalating.

Two budget categories are blessed plugin-wide:

- **Iteration cap** — maximum cycles, loop iterations, or batches the skill runs before forcing a stop. Examples: `/lead-project` caps at 50 OODA cycles; `/implement-batch` is bounded by its ticket set; per-batch retry attempts bounded.
- **Retry cap** — maximum consecutive failures of the same kind before escalating. Examples: `/implement` retries acceptance verification 3 times; `/refactor` and `/review-arch` abort a batch after 3 QA failures.

Two budget categories are explicitly **not** part of the discipline:

- **File-touch budgets** — "may not modify more than N files." Considered and rejected: a low ceiling breaks legitimate large refactors; a high ceiling provides no real bound.
- **Dependency-change budgets** — "may not add/remove more than N dependencies." Considered and rejected: dependency choices are governed by constraints in commander's intent, not by a count.

Skills can introduce additional skill-specific budgets if they earn their keep, but file-touch and dependency-change budgets should not be reintroduced under different names.

## Cascade rule

> Worker → caller → user. Not worker → user.

When an orchestrator invokes a sub-skill (e.g., `/implement-batch` invokes `/implement`), the sub-skill's escalations cascade up to the orchestrator, not directly to the operator. The orchestrator decides whether to resolve the escalation itself or to pull its own andon cord at a higher altitude.

Today `/implement-batch` already intercepts `/implement` escalations — when `/implement`'s acceptance verification fails 3 times, `/implement-batch` is supposed to pull its own cord rather than allow `/implement` to escalate directly. This pattern generalizes:

- `/implement-project` intercepts `/implement-batch` escalations and decides whether to pull its own cord.
- `/lead-project` intercepts `/implement-project` and any other sub-skill escalations during its OODA loop.

The deepest skill never goes around its caller. The caller has more context about the project than the worker does. Worker escalations are *cause* (something went wrong); caller escalations are *effect* (we couldn't fix it from this altitude).

## No unilateral breaking changes

> Breaking changes must be explicitly authorized by the operator.

This is a categorical guardrail, not an altitude judgment. The five levers describe how a skill decides between options; this rule constrains the option set itself. A skill in the orchestrator family must not introduce a breaking change without operator authorization — no matter how confident it is, how clear the rationale, or how strong the consensus among sub-agents.

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

### `/lead-project` — canonical schema

Five fields, all required:

- **Purpose** — one or two sentences stating why this iteration exists. The underlying motivation, not the tactical outcome.
- **Key tasks** — non-negotiable outcomes that must be true at the end. Written as state, not activity. Listable (2–10 items).
- **End state** — concrete, observable conditions defining completion. Classified as *mechanical* (shell-runnable check) or *subjective* (requires human judgment).
- **Constraints** — hard limits the skill must not violate during the loop.
- **Non-goals** — explicit out-of-scope items.

This schema is the canonical implementation referenced from the rest of this document. Other schemas are lighter variants that drop fields the skill does not need (because the work is more bounded).

### `/implement-project`

Four fields:

- **Tickets** — already gathered during step 1 (batched, fetched from tracker).
- **Acceptance bar** — what defines "ready to merge for this project." Defaults to "all tickets implemented, full pipeline passes." Operator may extend (e.g., "and CHANGELOG mentions every user-visible change").
- **Constraints** — cross-cutting constraints not encoded in individual tickets (e.g., "must remain compatible with library version X").
- **Non-goals** — explicit out-of-scope items.

Purpose and end state are implicit: purpose is "ship this project's tickets"; end state is the acceptance bar plus the quality pipeline.

### `/refactor-deep`

Six fields (mostly already elicited today; this formalizes them):

- **Scope** — entire codebase or user-specified subset.
- **Aggression ceiling** — for the tactical `/refactor` phase.
- **QA instructions** — special verification steps beyond the standard test suite.
- **Ticket-creation preference** — whether `/review-arch` should offer to cut tickets at Phase 2.
- **Constraints** — paths or patterns not to touch.
- **Non-goals** — refactoring categories explicitly out of scope.

### `/implement-batch`

**No separate elicitation.** `/implement-batch` is a for-loop, not an orchestrator. Tickets are the intent. Constraints inherit from the caller if the skill was invoked by `/implement-project` or `/lead-project`. When invoked directly by the operator, additional constraints can be expressed in the initial invocation or by editing the tickets themselves; the skill does not elicit them separately.

This is a deliberate exception to the schema list. Adding a schema here would be ceremony without substance — the tickets carry the work definition, and cross-ticket constraints are rare enough that prompting on every invocation would be noise.

## Shared handoff template

The template below is the canonical structure for andon-cord pulls across the orchestrator family. Skills must use this structure when escalating to the operator; skill-specific extensions go inline as additional fields, not as replacements.

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

Skills may add fields below "Current state" that are specific to their workflow (e.g., `/lead-project` includes cycle-log pointer; `/implement-project` includes batch progress). They should not add fields *between* "Pre-loaded options" and "Recommendation" — that ordering is load-bearing.

## What to log instead of escalate

The altitude rule (lever 1) says "implementation-detail forks get the skill's best judgment plus a state-doc log entry." This section enumerates concrete examples so future skill maintainers know what *doesn't* warrant escalation.

 | Situation                                                                             | Resolution                                                                      | Log entry                                                                                      |
 | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
 | SME proposes function name `parseInput` vs `parseRequest` — conventions don't dictate | Pick the more specific one.                                                     | "Named `parseRequest` for clarity; `parseInput` was equally idiomatic."                        |
 | Refactor reviewer suggests deleting a helper; another invocation argues to keep       | Apply default policy (refactor wins if no caller references and no test fails). | "Removed `unusedHelper`; refactor-reviewer flagged unused; no callers found."                  |
 | Test review surfaces a coverage gap on a non-critical helper, severity low            | Defer to final report. Do not block termination.                                | "Deferred: low-coverage helper `pkg/util/format`; rationale: non-critical, no recent changes." |
 | Two SMEs return functionally equivalent implementations                               | Pick one (the simpler diff).                                                    | "Chose SME A's implementation; SME B's was equivalent but had two more lines."                 |
 | Review-doc says wording is unclear; reviewer didn't propose a rewrite                 | Improve wording with judgment; commit if improvement is clear.                  | "Rewrote intro paragraph; review-doc flagged ambiguity in two sentences."                      |
 | Severity classification of a finding is borderline (medium vs low)                    | Use the lower severity if either is defensible.                                 | "Classified `<finding>` as low; review-arch borderline medium."                                |

The log entry is the contract: the operator can grep the state doc post-run to see what the skill decided unilaterally and why. If the operator disagrees, they can revert the specific commit or revisit the decision. The cost of a log entry is much less than the cost of an interruption.

## Advisory aspiration for `/review-*` skills

Direction, not strictly enforced today. Review skills should produce reports and not implement changes. The principle: review and implementation are different concerns. A skill that does both makes both worse — implementation pressure can compromise the review, and review pressure can compromise the implementation.

Status as of this document:

 | Skill              | Status                                                                  |
 | ------------------ | ----------------------------------------------------------------------- |
 | `/review-arch`     | Advisory as of v8.0.0. First concrete step.                             |
 | `/review-doc`      | Still implements (fixes docs via `doc-maintainer` agent). Future scope. |
 | `/review-test`     | Advisory as of v9.0.0.                                                  |
 | `/review-a11y`     | Already advisory.                                                       |
 | `/review-health`   | Already advisory.                                                       |
 | `/review-perf`     | Already advisory.                                                       |
 | `/review-security` | Advisory as of v8.0.0.                                                  |
 | `/review-release`  | Effectively advisory (presents findings for operator review).           |

The path forward: when a `/review-*` skill becomes advisory, its findings should name specific implementation skills with scope hints so the operator (or a calling orchestrator) can chain the right next step. Example: "Dead code in `src/foo/`: run `/refactor` scoped to that directory."

## What this discipline does NOT do

- **It does not apply to user-facing exploration skills.** `/scope` and `/scope-project` are intrinsically interactive; the operator is figuring out what to build. The discipline of pre-loaded options and pre-rebutted recommendations may still be valuable in those skills, but the autonomy framing does not.
- **It does not apply to `/implement`.** `/implement` works well as a directly-invoked skill, often run with the operator at the keyboard. Forcing autonomy discipline on it would change a working skill for marginal gain. When `/implement` is invoked by `/implement-batch` or higher, the autonomy comes from the caller, not from `/implement` itself.
- **It does not apply to `/review-deep`.** `/review-deep` is deliberately interactive throughout — the operator participates in every sub-skill's decision points. The autonomy alternative is to invoke individual `/review-*` skills directly.
- **It does not eliminate operator touchpoints.** It eliminates *granular* operator touchpoints. Commander's intent at startup is a touchpoint. The completion report is a touchpoint. Andon-cord pulls are touchpoints — they're just structured to be cheap to answer.
- **It does not pursue agent-side completeness.** Sub-agents (`swe-sme-*`, `qa-engineer`, etc.) are workers, not orchestrators. They report findings and complete tasks; they do not escalate. Escalation logic lives at the skill layer.

## Sources

The intellectual lineage of this discipline, in rough order of how directly the ideas are borrowed:

- **Toyota Production System** — the andon cord. Any worker can stop the line when something is wrong. Stopping is virtuous because it surfaces problems before they propagate.
- **Mission command (military doctrine)** — commander's intent. Subordinates are given the *why* and are trusted to execute the *how*. Variants exist across NATO doctrine, the U.S. Marine Corps' MCDP 6, and the German *Auftragstaktik* tradition that precedes both.
- **John Boyd — OODA loop** (1976+). Observe, Orient, Decide, Act. The decision-cycle framework that anchors `/lead-project`. Useful here as the mental model for what happens *between* andon-cord pulls.
- **Site Reliability Engineering / incident response practice** — blast radius, reversibility, "do-no-harm" defaults. The notion that some actions are cheap to take back and others aren't, and that the difference should drive how cautiously the skill behaves.
- **Rationalist tradition (steelmanning)** — feeds the pre-rebutted-recommendation lever. The recommendation should be tested against its strongest critique before it reaches the operator.

## Evolution

This document changes with the orchestrator family, but deliberately. A change to autonomy.md is a meaningful event that should be reflected in the cited skills. New escalation patterns invented in a single skill should either be reconciled here or rejected.

Skills that drift from this discipline are candidates for revision. The cost of the discipline is uniformity and a slightly higher bar for new escalation points; the benefit is that an operator who has used one orchestrator-family skill knows what to expect from another.
