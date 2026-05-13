# Advisory Skill Ticket-Proposal Pattern

This document codifies the runtime ticket-proposal pattern shared by the advisory review-shaped skills: `/bug-hunt`, `/review-arch`, `/review-security`, `/review-test`. Each cites this document and supplies only its bespoke content — the ticket-shape catalog applicable to its findings, the per-ticket body schema, and any skill-specific fallback when the operator declines.

The pattern exists because review-shaped skills produce findings that need to be durably documented in the tracker for any subsequent fix work — but the operator (or invoking orchestrator) must approve the proposed structure. The skill does not unilaterally cut tickets; it proposes and waits.

## The proposal step

After all analysis phases complete, the skill examines the shape of the findings (count by severity, clustering, type-mix) and proposes a ticket structure. The proposal uses this form:

```
Proposed ticket structure for this <hunt | audit | review>:

<one-line shape summary — e.g., "8 findings (3 CRITICAL, 2 HIGH, 1 MEDIUM, 1 LOW), 1 chain.">

Proposed: N tickets
  - <ticket 1 description + reasoning>
  - <ticket 2 description + reasoning>
  - ...

Approve / edit / decline?
```

The skill **waits for the response** before proceeding. The shape catalog (which proposed structure to recommend given the finding mix) is skill-specific and lives in the skill's own SKILL.md.

## Three outcomes

The dispatcher accepts exactly three outcomes:

- **Approve** — proceed to ticket creation. The proposed structure is the structure that gets created.
- **Edit** — the operator modifies the structure (merge two tickets, split one, drop a finding, change granularity). Apply the edits, present the revised structure, and repeat until approved.
- **Decline** — the analysis report stands alone. The operator can act on findings at their discretion. The skill exits cleanly; no tracker writes occur.

Skill-specific behavior on decline:

- `/bug-hunt` — falls through to a reproducing-test commit step. The tests have standalone coverage value regardless of ticket creation, so the skill offers to commit them even after a declined ticket proposal.
- `/review-arch`, `/review-security`, `/review-test` — exit cleanly with the analysis report; no further actions.

## Orchestrator-invoked behavior

When invoked by an orchestrator (`/lead-project`, `/lead-bug-hunt`, `/lead-refactor`, `/lead-review`, `/implement-project`, etc.), the workflow above is unchanged. The skill proposes the ticket structure to the orchestrator, which applies its own autonomy judgment per [`autonomy.md`](autonomy.md) § "Auto-approval of sub-skill ticket proposals" — approving, editing, or declining the proposal, then deciding which of any created tickets to work in the current flow versus defer.

The skill does not branch on "interactive operator vs orchestrator." The proposal is the same. The receiver decides.

## What the skill carries

Each advisory skill's SKILL.md is responsible for:

- The **shape catalog** — the menu of proposed ticket structures the skill chooses among given its finding mix (e.g., "Concentrated CRITICALs" → 1 ticket per finding; "Spread across severity" → batch tickets; "Defense-in-depth only" → single hardening ticket).
- The **per-ticket body schema** — the section headings each created ticket uses (Bug/Attack/Gap; Root cause/Defensive gap/Risk; Reproducing test/Acceptance criteria; Fix guidance; etc.).
- Any **commit-step boundary** — `/bug-hunt` commits reproducing tests *before* ticket creation so ticket bodies can reference them by path; other advisory skills don't have a commit dependency.

What this document carries is uniform across the family: the proposal form, the three-outcome dispatcher, and the orchestrator-invoked behavior paragraph.
