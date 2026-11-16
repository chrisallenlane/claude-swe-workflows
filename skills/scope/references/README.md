# /scope — From a Problem to Tickets

The step-by-step procedure lives in [`SKILL.md`](../SKILL.md); this guide covers when to use the skill and what to expect.

## Overview

`/scope` helps you understand a problem space — through codebase exploration and dialogue — and turns it into the tickets that implementing it will need. A small bug fix may produce one ticket; a new subsystem may produce a dozen with dependencies between them.

**It writes no code.** It explores, questions, designs with you, and documents.

**Planning is cheaper than rework.** A gap found in a ticket costs minutes; the same gap found mid-implementation costs hours and may cascade.

**Judgment over checklists.** The skill decides how many tickets the work needs and which reviewers (implementer, UX, security, performance, architecture, value) to bring in. Two rules are fixed:

| Rule                                              | Why                                                                                                             |
|---------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|
| Drafts go upstream only after review converges    | The author of a plan anchors on what it just wrote; fresh reviewers re-run until a round finds nothing material |
| Nothing is created upstream without your approval | The final ticket set is yours to accept                                                                         |

## When to Use

**Use `/scope` for:**
- A feature, refactoring, or bug you want understood and specified before anyone builds it
- A whole project you want broken into dependent, implementable tickets
- Work that will be handed to someone else, or to `/implement`, later

**Don't use `/scope` for:**
- Work you want built now — `/implement` will clarify and scope inline when the shape is obvious
- Questions about the code with no ticket in mind — just ask

## The Flow

```
Discover → Explore → Design with you → Draft → Review (fresh, until converged) → Approve and create
```

## What to Expect

- **A conversation, not a form.** Expect questions about scope, boundaries, and desired outcome before implementation, and pushback on assumptions during design. If the stated problem looks like a symptom, the skill may reframe it with you before exploring.
- **Tickets someone could implement tomorrow without guessing** — testable acceptance criteria ("run X, expect Y"), accurate code references, explicit dependencies, and an execution order for multi-ticket sets.
- **Conflicts brought to you.** When two reviewers' signed-off positions collide, or a lens keeps raising material findings after three rounds, the decision comes to you — it's usually a requirements question.
- **A final review before anything is created:** each ticket, the execution order, and a summary of what reviewers found and how it was resolved. Tickets are created in your tracker only after you approve, in execution order, with numbers and URLs reported.

## Examples

### Example 1: One ticket, one cold read

```
You: /scope — the `--since` flag ignores timezones

Discover: bug; desired outcome is that --since respects the
  user's local zone.
Explore: parseSince() in cmd/log.go uses time.Parse (UTC);
  the display path uses time.Local. Two call sites.
Design: agree on time.ParseInLocation with time.Local; RFC 3339
  input with an explicit offset keeps its offset. One ticket.
Draft: bug-fix ticket with root cause, fix, and acceptance
  criteria ("TZ=America/New_York log --since 2026-01-01 includes
  an entry at 2026-01-01T02:00-05:00").
Review: swe-implementer cold-reads it — flags that a third call
  site in cmd/export.go also parses --since. Added; fresh reviewer
  finds nothing further.
You approve; ticket #88 created.
```

### Example 2: Multi-ticket project, conflicting lenses

```
You: /scope — add API tokens so scripts can call the server

Explore and design: personal tokens, scoped read/write, revocable.
  Cut into 5 tickets: token model, issue/revoke CLI, auth
  middleware, scope enforcement, docs. Order and dependencies stated.
Review:
  - ux-reviewer: add a user-chosen label and show a token prefix
    in `token list`. Locked.
  - sec-blue-teamer (spec-time): tokens stored hashed. Locked.
  - swe-implementer: the ux-locked prefix needs a stored, unhashed
    prefix, which security asked to avoid.
  Conflict between two signed-off elements → brought to you:
    A. Store a 6-char prefix (identifiable; small leak)
    B. Labels only, no prefix (no leak; less identifiable)
  You pick B. Tickets revised; fresh implementer finds no gaps.
You approve the set; #120–#124 created in order, dependencies linked.
```

## Tips

1. **Bring the problem, not the solution.** Exploration and design go better when the skill can propose approaches.
2. **Push back during design.** The tickets are only as good as the shared understanding behind them.
3. **Let it decide how to cut the work** — but say so if you need a particular grouping.
4. **Read the review summary before approving.** It tells you what the cold readers caught and what got locked.
5. **Hand the set to `/implement`.** `/scope` writes the tickets; `/implement` builds them — one, or the whole set.
