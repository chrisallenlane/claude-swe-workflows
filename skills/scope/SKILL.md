---
name: scope
description: Explores a problem with the user and turns it into well-specified tickets in the issue tracker, from one ticket to a whole project. Every draft gets a fresh-context review; nothing is created without approval. Writes no code.
model: opus
---

# Scope — From a Problem to Tickets

Helps the user understand a problem space through codebase exploration and dialogue, then writes the tickets that implementing it will need. A small bug fix may produce one ticket; a new subsystem may produce a dozen with dependencies between them. The work decides how many, and which reviewers the draft needs before it goes upstream.

**This skill does not write code.** It explores, questions, designs with the user, and documents.

## Philosophy

**Planning is cheaper than rework.** A gap found in a ticket costs minutes; the same gap found mid-implementation costs hours and may cascade.

**Judgment over checklists.** There is no fixed sequence of review loops. The skill decides what the work needs — how many tickets, which lenses — and the reviewers below are there to support it, not to be walked through in order.

**Two rules are fixed:**

1. **Drafts go upstream only after review converges.** The author of a plan anchors on what they just wrote; self-review is where planning judgment is weakest. Every draft is reviewed by at least one fresh-context reader, and review repeats — revise, then a *fresh* reviewer — until a round finds nothing material. Which reviewers is judgment; convergence is not.
2. **Nothing is created upstream without the user's approval** of the final ticket set.

## 1. Discover

Understand what the user wants to explore — a feature, a refactoring, a bug that needs investigation, a whole project — and ask about scope, boundaries, the problem, and the desired outcome (not the implementation yet). When the stated problem looks like a symptom, or its framing is contested, spawn a few `thk-reframer` agents in isolation, each on a different lens (problem-vs-symptom, scope-shift, stakeholder-shift, category-shift), and settle the framing with the user before exploring. Turning the wrong problem into tickets is the most expensive way to solve it.

## 2. Explore

Learn the relevant code before proposing anything: where the change fits, what it affects, the conventions already established, the integration points, and similar features to learn from. Use `Explore` agents for broad sweeps, read key files directly, and read third-party docs or clone dependencies to a scratch directory when the integration matters.

## 3. Design With the User

Present what exploration found, then work the design out together: the approaches and their trade-offs, edge cases, constraints, and acceptance criteria. Challenge assumptions and propose alternatives — this is collaborative design, not requirements transcription. Continue until both sides share a precise understanding of what to build and why.

Decide here how the work should be cut: one ticket, or several. Several when the work has independently verifiable parts, when parts depend on others landing first, or when one ticket would be too large to implement and review as a unit.

## 4. Draft

Write each ticket so that someone else could implement it tomorrow without guessing. Adapt the content to the kind of work:

- **Feature:** problem statement; proposed solution; acceptance criteria (specific and testable — "run X, expect Y"); technical notes (affected components, current signatures and modules the implementer will need); security considerations where the change adds attack surface, handles input, or crosses a trust boundary; dependencies; out of scope; open questions.
- **Refactoring:** current state and what is wrong with it; desired state; motivation; approach; risks; affected areas.
- **Bug fix:** observed behavior; root cause from exploration; proposed fix; why it happened; how to verify; how to prevent recurrence.

For a multi-ticket set, state each ticket's dependencies explicitly and give the set an execution order. Draft in a gitignored `.tickets/` staging directory when the set is large enough that files beat holding it in context; remove it when done.

**Quality bar.** Every ticket meets these; reviewers check against them:

| Criterion                      | Meaning                                                                                                       |
|--------------------------------|---------------------------------------------------------------------------------------------------------------|
| Implementable without guessing | Two developers would build substantially the same thing                                                       |
| Testable acceptance criteria   | Each criterion is a concrete check, not a judgment ("it should be fast")                                      |
| Explicit dependencies          | Every ticket says what must exist before it starts; no forward dependencies within the execution order        |
| No gaps, no overlaps           | All necessary work is assigned to exactly one ticket; no two tickets change the same code in conflicting ways |
| Accurate code references       | Paths, functions, and modules named in the tickets exist as described                                         |
| Appropriate scope              | Each ticket is a coherent unit — not unmanageable, not trivial                                                |

## 5. Review

Spawn fresh-context reviewers on the drafts — at least one, always (rule 1). Choose by what the work needs:

- **Implementer** — the default cold reader. Spawn `swe-implementer` in cold-read mode, told to review every ticket as if assigned to implement it tomorrow: every gap, ambiguity, missing dependency, wrong code reference, and unanswered question, with a specific fix for each.
- **`ux-reviewer`** — whenever the work changes what a user (of a CLI, MCP server, web app, or library API) sees or does: mental-model fit, dead ends, missing recovery paths, naming. Asks "will users be able to use this?"
- **`sec-blue-teamer`** in spec-time mode — when the work shapes authentication, authorization, trust boundaries, or data handling at the design level. Frame it as a spec-time review: the controls the design needs, not an audit of existing code.
- **`swe-perf-reviewer`** in spec-time mode — when the design has architectural performance implications: what it will cost at the codebase's actual scale (data structures, caching strategy, hot-path shape).
- **`swe-arch-reviewer`** in spec-time mode — when the design's structure deserves a challenge: where the proposed concepts belong and what they duplicate.
- **`swe-value-engineer`** in spec-time mode — when the requirements themselves deserve a challenge: which drafted requirements cost more than they're worth.

**Iterate to convergence.** Revise from the findings, then re-review with a **fresh** instance of each lens that raised material findings — a fresh reader doesn't anchor on its own prior findings. Stop when a round finds nothing material: nothing that would change what gets built, how it is verified, or how the work is cut. Wording nits are not material. Simple work usually converges in one round; complex work may take several. A lens still raising material findings after three rounds goes to the user — the disagreement is probably a requirements question, not a drafting one.

**Sign-offs are constraints.** When a lens signs off on something — an approved command name, a required security control — later reviewers may raise a conflict with it, but they don't silently trade it away. A conflict between lenses the skill cannot resolve goes to the user.

## 6. Approve and Create

**Present the final set** to the user: each ticket in full (or summarized, with the files available, for a large set), the execution order and dependencies, and a summary of what the reviewers found and how it was resolved. Highlight remaining uncertainty. Iterate until the user approves (rule 2).

**Create the tickets** per [`references/trackers.md`](../../references/trackers.md) (Detection Procedure + "Create"). Create them in execution order, so later tickets can link to the earlier ones they depend on. Apply labels the user wants. Report each ticket's number and URL, and clean up any staging directory.

## Boundaries

**Will:** explore code extensively, ask many questions, challenge assumptions, propose alternatives, spawn reviewers, and create tickets in the tracker on approval.

**Will not:** write production code, commit, run tests, or modify files other than its own staging drafts (and the `.gitignore` entry that keeps them out of commits).

## Relationship to Other Skills

**`/scope` → `/implement`** is the planning-to-execution pair: this skill writes the tickets; `/implement` builds them — one, or the whole set.
