# /scope — From a Problem to Tickets

## Overview

`/scope` helps you understand a problem space — through codebase exploration and dialogue — and turns it into the tickets that implementing it will need. A small bug fix may produce one ticket; a new subsystem may produce a dozen with dependencies between them. It covers what `/scope-project` used to do; there is now one planning skill at every scale.

**It writes no code.** It explores, questions, designs with you, and documents.

**Judgment over checklists.** There is no fixed sequence of review loops. The skill decides how many tickets the work needs and which reviewers to bring in; review then repeats until it converges. The reviewer agents are there to support that judgment, not to be walked through in order.

**Two rules are fixed:**

| Rule                                              | Why                                                                                                             |
|---------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|
| Drafts go upstream only after review converges    | The author of a plan anchors on what it just wrote; fresh reviewers re-run until a round finds nothing material |
| Nothing is created upstream without your approval | The final ticket set is yours to accept                                                                         |

**Planning is cheaper than rework.** A gap found in a ticket costs minutes; the same gap found mid-implementation costs hours and may cascade.

## When to Use

**Use `/scope` for:**
- A feature, refactoring, or bug you want understood and specified before anyone builds it
- A whole project you want broken into dependent, implementable tickets
- Work that will be handed to someone else, or to `/implement`, later

**Don't use `/scope` for:**
- Work you want built now — `/implement` will clarify and scope inline when the shape is obvious
- Questions about the code with no ticket in mind — just ask

## Workflow

```
┌──────────────────────────────────────────────────────────────┐
│                       /scope WORKFLOW                        │
├──────────────────────────────────────────────────────────────┤
│  1. Discover — what are we exploring, and why?               │
│  2. Explore — learn the relevant code first                  │
│  3. Design with you — approaches, trade-offs, criteria;      │
│     decide one ticket or several                             │
│  4. Draft — tickets that meet the quality bar                │
│  5. Review — fresh-context reviewers (≥1, always);           │
│     revise; re-review fresh until nothing material           │
│  6. Approve and create — your approval, then the tracker     │
└──────────────────────────────────────────────────────────────┘
```

## Workflow Details

### 1. Discover

What you want to explore — a feature, a refactoring, a bug, a project — and its scope, boundaries, problem, and desired outcome. Not the implementation yet.

### 2. Explore

The skill learns the relevant code before proposing anything: where the change fits, what it affects, established conventions, integration points, similar features. It uses `Explore` agents for broad sweeps, reads key files directly, and reads third-party docs or clones dependencies to a scratch directory when an integration matters.

### 3. Design With You

It presents what it found, then works the design out with you: approaches and trade-offs, edge cases, constraints, acceptance criteria. Expect it to challenge assumptions and propose alternatives — this is collaborative design, not transcription.

This is also where the work gets cut. Several tickets rather than one when the work has independently verifiable parts, when parts depend on others landing first, or when a single ticket would be too large to implement and review as a unit.

### 4. Draft

Each ticket is written so someone else could implement it tomorrow without guessing. Content adapts to the kind of work:

| Kind        | Contents                                                                                                                                                                                                                    |
|-------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Feature     | Problem; proposed solution; testable acceptance criteria ("run X, expect Y"); technical notes (affected components, current signatures); security considerations where relevant; dependencies; out of scope; open questions |
| Refactoring | Current state and what's wrong; desired state; motivation; approach; risks; affected areas                                                                                                                                  |
| Bug fix     | Observed behavior; root cause; proposed fix; why it happened; verification; recurrence prevention                                                                                                                           |

A multi-ticket set states each ticket's dependencies explicitly and has an execution order. Large sets are drafted in a gitignored `.tickets/` staging directory, removed when done.

**The quality bar** every ticket must meet — and reviewers check against:

| Criterion                      | Meaning                                                                                    |
|--------------------------------|--------------------------------------------------------------------------------------------|
| Implementable without guessing | Two developers would build substantially the same thing                                    |
| Testable acceptance criteria   | Each is a concrete check, not a judgment ("it should be fast")                             |
| Explicit dependencies          | Each ticket says what must exist first; no forward dependencies within the execution order |
| No gaps, no overlaps           | All necessary work assigned to exactly one ticket; no conflicting changes to the same code |
| Accurate code references       | Paths, functions, and modules named in tickets exist as described                          |
| Appropriate scope              | Each ticket is a coherent unit — not unmanageable, not trivial                             |

### 5. Review

At least one fresh-context reviewer reads the drafts, always. Beyond that, the skill chooses by what the work needs:

| Reviewer                                    | When                                                                            | Asks                                                                    |
|---------------------------------------------|---------------------------------------------------------------------------------|-------------------------------------------------------------------------|
| Implementer (`swe-implementer`)            | The default cold reader                                                         | "Could I build this tomorrow?" — gaps, ambiguity, wrong references      |
| `ux-reviewer`                               | The work changes what a user of a CLI, MCP server, web app, or API sees or does | "Should we build this?" — mental-model fit, dead ends, recovery, naming |
| `sec-blue-teamer`                           | The design shapes auth, authorization, trust boundaries, or data handling       | What controls does this design need? (spec-time, not a code audit)      |
| `swe-perf-reviewer`                         | The design has architectural performance implications                           | Data structures at scale, caching, hot-path shape                       |
| `swe-arch-reviewer`, `swe-value-engineer`   | The structure, or the requirements themselves, deserve a challenge              | Is this the right shape? Is this requirement worth its cost?            |

Review repeats until it converges. The skill revises from the findings, then re-reviews with a **fresh** instance of each lens that raised material findings, so reviewers don't anchor on their own prior findings. It stops when a round finds nothing material — nothing that would change what gets built, how it is verified, or how the work is cut; wording nits don't count. Simple work usually converges in one round. A lens still raising material findings after three rounds comes to you, because a disagreement that persistent is usually a requirements question.

**Signed-off elements are constraints.** When a lens approves something — a command name, a required security control — later reviewers may raise a conflict with it but don't silently trade it away. A conflict between lenses the skill can't resolve comes to you.

### 6. Approve and Create

You see the final set — each ticket in full, or summarized with the files available for a large set — plus the execution order, dependencies, and a summary of what reviewers found and how it was resolved. Remaining uncertainty is highlighted. It iterates until you approve.

Then it creates the tickets in your tracker in execution order, so later tickets can link to the earlier ones they depend on, applies any labels you want, reports each number and URL, and cleans up its staging directory.

## Examples

### Example 1: One ticket, one cold read

```
You: /scope — the `--since` flag ignores timezones

1. Discover: bug; desired outcome is that --since respects the
   user's local zone.
2. Explore: parseSince() in cmd/log.go uses time.Parse (UTC);
   the display path uses time.Local. Two call sites.
3. Design: agree on time.ParseInLocation with time.Local; RFC 3339
   input with an explicit offset keeps its offset. One ticket.
4. Draft: bug-fix ticket with root cause, fix, and acceptance
   criteria ("TZ=America/New_York log --since 2026-01-01 includes
   an entry at 2026-01-01T02:00-05:00").
5. Review: swe-implementer cold-reads it — flags that a third call
   site in cmd/export.go also parses --since. Added; fresh reviewer
   finds nothing further.
6. You approve; ticket #88 created.
```

### Example 2: Multi-ticket project, conflicting lenses

```
You: /scope — add API tokens so scripts can call the server

1–3. Explore and design: personal tokens, scoped read/write,
     revocable. Cut into 5 tickets: token model, issue/revoke CLI,
     auth middleware, scope enforcement, docs. Order and
     dependencies stated.
4. Draft in .tickets/.
5. Review:
   - ux-reviewer: the CLI shows the token once, at creation, with
     no way to tell tokens apart later — add a user-chosen label.
     Approved: `token create --label`, token shown once. Locked.
   - sec-blue-teamer (spec-time): tokens must be stored hashed;
     constant-time comparison; scope checked on every request.
     Locked.
   - Implementer (swe-implementer): hashed storage means the CLI
     can't list a token's value — fine — but the ux-locked "show
     a token prefix in `token list`" needs a stored, unhashed prefix,
     which security asked to avoid.
   Conflict between two signed-off elements → brought to you:
     A. Store a 6-char prefix (identifiable; small leak)
     B. Labels only, no prefix (no leak; less identifiable)
   You pick B. Tickets revised; fresh implementer finds no gaps.
6. You approve the set; #120–#124 created in order, dependencies
   linked; .tickets/ removed.
```

## Tips

1. **Bring the problem, not the solution.** Exploration and design go better when the skill can propose approaches.
2. **Push back during design.** The tickets are only as good as the shared understanding behind them.
3. **Let it decide how to cut the work** — but say so if you need a particular grouping.
4. **Read the review summary before approving.** It tells you what the cold readers caught and what got locked.
5. **Hand the set to `/implement`.** `/scope` writes the tickets; `/implement` builds them — one, or the whole set.
