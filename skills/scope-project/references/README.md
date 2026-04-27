# /scope-project - Adversarial Project Planning

## Overview

The `/scope-project` skill plans an entire project through two sequential adversarial review loops. It explores the problem space, drafts tickets organized into batches, then runs a UX reviewer loop ("should we build this?") followed by an implementer loop ("could we build this?") to find gaps, traps, ambiguities, and missing work. Only when both loops sign off do the tickets go upstream — already tagged with batch labels ready for `/implement-project` to consume.

**Key benefits:**
- Two adversarial review loops catch different classes of planning gap: UX (step 6) for design cogency, implementation (step 7) for technical viability
- UX issues become hard constraints on the implementation discussion, not items the implementer can negotiate away
- Batch structure is a first-class planning artifact, not an afterthought
- Implementation notes give implementers a head start on codebase context
- Draft tickets are staged locally before going upstream — easy to revise
- Human clarification is surfaced during planning, not during implementation

## When to Use

**Use `/scope-project` for:**
- Multi-ticket projects that need careful planning before implementation
- Work that naturally divides into phases or batches
- Projects where you want to hand off a complete, well-specified plan to `/implement-project`
- Complex features where gaps between tickets could cause implementation problems

**Don't use `/scope-project` for:**
- A single feature or bug fix (use `/scope` directly)
- Work where the scope is already well-understood and tickets already exist
- Exploratory work where you're not ready to commit to a project structure
- Quick prototypes or throwaway code

**Rule of thumb:** If you'd create more than 3 tickets and they have dependencies between them, use `/scope-project`. If it's a single ticket, use `/scope`.

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ /scope-project Workflow                                         │
└─────────────────────────────────────────────────────────────────┘

 ┌──────────────────────────────────────────────┐
 │  1. PROJECT DISCOVERY                        │
 │  ────────────────────────────────────────    │
 │  • Dialogue with user about project goals    │
 │  • Probing questions on scope, constraints   │
 │  • Push back on vagueness                    │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  2. CODEBASE EXPLORATION                     │
 │  ────────────────────────────────────────    │
 │  • Map current architecture                  │
 │  • Identify affected code areas              │
 │  • Understand existing patterns              │
 │  • Review third-party dependencies           │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  3. DRAFT PROJECT PLAN                       │
 │  ────────────────────────────────────────    │
 │  • Batch structure with ordering rationale   │
 │  • Ticket inventory per batch                │
 │  • Dependencies and risk areas               │
 │  • Present to user for approval              │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  4-5. DRAFT TICKETS                          │
 │  ────────────────────────────────────────    │
 │  Create .tickets/ staging directory          │
 │  Spawn one subagent per ticket:              │
 │  • Problem statement                         │
 │  • Proposed solution                         │
 │  • Acceptance criteria                       │
 │  • Technical notes + implementation notes    │
 │  • Dependencies and out-of-scope             │
 └──────────────────┬───────────────────────────┘
                    ▼
    ┌───────────────────────────┐
    │  UX ADVERSARIAL REVIEW    │◄──────────────┐
    └─────────────┬─────────────┘               │
                  ▼                             │
 ┌──────────────────────────────────────────────┐
 │  6a. UX REVIEWER REVIEWS ALL TICKETS         │
 │  ────────────────────────────────────────    │
 │  Agent: ux-reviewer (auto-detects target)    │
 │                                              │
 │  Walks the seven-concern spine:              │
 │  • Coherence                                 │
 │  • Completeness                              │
 │  • Mental-model fit                          │
 │  • Implicit knowledge                        │
 │  • Failure paths                             │
 │  • Power/novice tension                      │
 │  • Orientation                               │
 │                                              │
 │  Findings: blocker / concern / suggestion    │
 │  Verdict: APPROVED or NEEDS REVISION         │
 ├──────────────────────────────────────────────┤
 │  6b. PLANNER ADDRESSES UX FEEDBACK           │
 │  ────────────────────────────────────────    │
 │  • Resolve blockers (revise tickets)         │
 │  • Address concerns or document why not      │
 │  • Accept/decline suggestions                │
 │  • UX-locked elements become hard            │
 │    constraints for step 7                    │
 └──────────────────┬───────────────────────────┤
                    ▼                           │
            UX reviewer approved?               │
            ├─ No  → Fresh ux-reviewer ─────────┘
            │        (or escalate if stalemated)
            └─ Yes ▼
    ┌───────────────────────────┐
    │ IMPL ADVERSARIAL REVIEW   │◄──────────────┐
    └─────────────┬─────────────┘               │
                  ▼                             │
 ┌──────────────────────────────────────────────┐
 │  7a. IMPLEMENTER REVIEWS ALL TICKETS         │
 │  ────────────────────────────────────────    │
 │  Agent: Language SME or general-purpose      │
 │                                              │
 │  Checks:                                     │
 │  • Can I implement without guessing?         │
 │  • Are acceptance criteria testable?         │
 │  • Are dependencies explicit?                │
 │  • Any missing tickets? Overlaps?            │
 │  • Batch assignments sound?                  │
 │  • Code references accurate?                 │
 │                                              │
 │  Verdict: APPROVED or NEEDS REVISION         │
 ├──────────────────────────────────────────────┤
 │  7b. PLANNER ADDRESSES FEEDBACK              │
 │  ────────────────────────────────────────    │
 │  • Resolve blockers (revise tickets)         │
 │  • Answer questions (or ask human)           │
 │  • Accept/decline suggestions                │
 │  • Draft missing tickets if needed           │
 │  • Adjust batch structure if needed          │
 │                                              │
 │  ESCAPE HATCH: if a finding requires         │
 │  changing UX-locked elements, return to      │
 │  step 6 with the constraint, then resume     │
 └──────────────────┬───────────────────────────┤
                    ▼                           │
            Implementer approved?               │
            ├─ No  → Fresh implementer ─────────┘
            │        (or escalate if stalemated)
            └─ Yes ▼
 ┌──────────────────────────────────────────────┐
 │  8. PRESENT FINAL TICKETS TO USER            │
 │  ────────────────────────────────────────    │
 │  Summary view of all tickets and batches     │
 │  Review round counts and clarifications      │
 │  Wait for user approval                      │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  9. CUT TICKETS UPSTREAM                     │
 │  ────────────────────────────────────────    │
 │  • Create batch labels (batch-1, batch-2)    │
 │  • Spawn one subagent per ticket             │
 │  • Apply batch labels + other tags           │
 │  • Present issue URLs                        │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  10. CLEAN UP                                │
 │  ────────────────────────────────────────    │
 │  Remove .tickets/ directory                  │
 │  Remove .gitignore entry                     │
 └──────────────────────────────────────────────┘
```

## Workflow Details

### 1. Project Discovery

A dialogue with you about the project's goals, scope, and constraints. The orchestrator asks probing questions and pushes back on vagueness — "add authentication" isn't specific enough; "add JWT-based authentication with refresh tokens and role-based access control" is.

### 2. Codebase Exploration

Deep exploration of the codebase to understand the current architecture, affected code areas, existing patterns, and integration points. This happens once at the project level — individual tickets benefit from this shared context rather than each doing their own exploration.

### 3. Draft Project Plan

The orchestrator synthesizes discovery and exploration into a structured plan: batch structure with ordering rationale, ticket inventory per batch, dependencies, and risk areas.

**This is presented to you for approval** — the primary human checkpoint. You can adjust batches, add/remove tickets, reorder, or ask questions. The plan must be approved before ticket drafting begins.

### 4-5. Draft Tickets

One subagent per ticket drafts detailed ticket content into a `.tickets/` staging directory. Each ticket includes:

- **Problem statement** — what problem this ticket solves
- **Proposed solution** — high-level approach
- **Acceptance criteria** — specific, testable
- **Technical notes** — affected files, key functions, patterns to follow
- **Implementation notes** — current function signatures, module boundaries, integration points (the kind of context that saves the implementer from rediscovery)
- **Dependencies** — what must exist before this ticket can start
- **Out of scope** — what explicitly won't be done

### 6. UX Adversarial Review Loop

The first of two adversarial loops. This one runs **before** the implementer review, so UX issues become hard constraints on the implementation discussion — not items the implementer can negotiate away on grounds of effort.

A `ux-reviewer` agent reads the entire ticket set as a UX advocate, walking a fixed seven-concern spine:

| Concern                | What it catches                                                    |
|------------------------|--------------------------------------------------------------------|
| Coherence              | Inconsistent mental models or vocabulary across tickets             |
| Completeness           | Implicit user needs unaddressed; dead ends with no recovery        |
| Mental-model fit       | Surfaces that expose internals rather than the user's task model   |
| Implicit knowledge     | What users must already know but the design assumes                |
| Failure paths          | Recovery legibility when users do the wrong thing                  |
| Power/novice tension   | Designs tuned for one tier at the other's expense                  |
| Orientation            | Whether users know where they are and what's next at each step     |

The agent auto-detects target type (CLI / MCP server / webapp / library / mixed) from project signals and adapts the *evidence it inspects* by type, while walking all seven concerns regardless. Ambiguous targets prompt a question to you.

Findings are categorized as **blocker / concern / suggestion** with a verdict of `APPROVED` or `NEEDS REVISION`. The planner addresses each: revise tickets, ask the user for clarification on user populations or design intent, or accept/decline suggestions. A fresh `ux-reviewer` re-reviews each round. UX-locked elements approved by the loop become hard constraints for step 7.

### 7. Implementation Adversarial Review Loop

The second adversarial loop, focused on technical viability. An implementer agent reviews all tickets as if assigned to implement them tomorrow, looking for:

| Check                          | What it catches                           |
|--------------------------------|-------------------------------------------|
| Implementable without guessing? | Vague requirements, undefined behaviors  |
| Testable acceptance criteria?  | Subjective criteria ("it should be fast") |
| Explicit dependencies?         | Implicit ordering assumptions             |
| Missing tickets?               | Work that falls through the cracks       |
| Overlapping tickets?           | Conflicting changes to the same code     |
| Sound batch assignments?       | Forward dependencies within a batch      |
| Accurate code references?      | Stale file paths, wrong function names   |

The implementer is a language-specific SME when available (Go SME for Go projects, etc.), giving it real implementation perspective.

**The planner addresses each finding** by revising tickets, asking you for clarification, or pushing back. A fresh implementer then re-reviews. This continues until the implementer approves or the process stalemates (at which point you're brought in).

**Asking you for clarification is normal.** The adversarial review surfaces questions that should be answered during planning, not during implementation. A question surfaced here saves much more time than the same question surfaced mid-implementation.

**Escape hatch back to step 6.** If the implementer surfaces a finding that cannot be addressed without changing UX-locked elements (e.g., "the proposed UX requires synchronous network calls that aren't possible here"), the planner returns to step 6 with the new constraint as input. The UX reviewer iterates with the constraint in scope, the loop converges, and step 7 resumes. This prevents implementer-wins-by-default — UX requirements stand unless physically infeasible.

### 8. Present Final Tickets

After both loops approve, the complete ticket set is presented for your final review. You can inspect any ticket in detail and request adjustments before creation.

### 9. Cut Tickets Upstream

Batch labels are created first, then tickets are created with labels applied. Each ticket includes the batch tag so `/implement-project` can consume them directly.

### 10. Clean Up

The `.tickets/` staging directory is removed.

## The `.tickets/` Staging Directory

Draft tickets are staged locally before going upstream:

```
.tickets/
├── batch-1/
│   ├── 01-add-mcp-subcommand.md
│   ├── 02-protocol-handshake.md
│   └── 03-define-tool-schema.md
└── batch-2/
    ├── 01-expose-read-commands.md
    └── 02-expose-write-commands.md
```

Each file is a markdown document with YAML frontmatter (title, batch, order, dependencies, labels) and structured sections. The staging directory is gitignored and deleted after tickets go upstream.

**Why stage locally?** Revising a local file during adversarial review is cheap. Revising an upstream ticket means editing, re-reading, coordinating — more friction. Local staging lets the planner and implementer iterate freely.

## The Adversarial Reviews

The two adversarial review loops are the distinguishing feature of `/scope-project`. Together they answer two questions:

- **Step 6 (UX loop): "Should we build this?"** — surfaces user-experience problems before implementation begins. Catches mental-model misfits, dead ends, missing recovery paths, power/novice imbalances, and the kind of UX defects that ship as bugs.
- **Step 7 (Implementation loop): "Could we build this?"** — surfaces technical gaps. Catches vague requirements, unclear dependencies, missing tickets, batch-ordering issues, and stale code references.

The loops are sequential, not concurrent — UX issues become hard constraints on the implementation discussion. The implementer cannot negotiate UX away on grounds of effort. If the implementer surfaces an infeasibility that breaks UX-locked design, the planner returns to step 6 with the constraint as input (the escape hatch).

**Different perspectives catch different gaps.** The planner thinks about what needs to be done. The UX reviewer thinks about whether users will succeed. The implementer thinks about what they'd need to know to do it. These are fundamentally different lenses.

**Fresh instances prevent anchoring.** Each review round spawns a new agent with a clean context. The new instance isn't anchored to the previous round's findings — it sees the tickets fresh and may notice different issues.

**Convergence, not perfection.** The goal isn't to document every conceivable edge case — it's to reach a state where the design is UX-cogent (step 6) and implementable without guessing (step 7). Most projects converge in 1-2 rounds at the UX loop and 2-3 at the implementation loop.

**Stalemate triggers human involvement.** If a loop keeps cycling on the same issues, something fundamental is ambiguous. UX stalemate usually means a design intent the user has not made explicit; implementation stalemate usually means the planner and implementer have a legitimate disagreement requiring human judgment. Either way, bringing the user in is the right move — the adversarial process has done its job by surfacing exactly what needs human judgment.

## Examples

### Example 1: MCP Server Project

```
User: /scope-project

I want to add MCP server support to our CLI tool — expose core
functionality as MCP tools over stdio transport.

[Discovery dialogue, codebase exploration...]

## Project Plan

### Batch 1: Core MCP Infrastructure (4 tickets)
1. MCP server subcommand — entry point, stdio, JSON-RPC
2. Protocol handshake — initialize/initialized
3. Tool schema definitions — CLI→MCP mapping
4. Tool dispatch — route calls to handlers

### Batch 2: Tool Implementations (3 tickets)
5. Read commands as MCP tools
6. Write commands as MCP tools
7. MCP resource support

### Batch 3: Polish (3 tickets)
8. Error handling — CLI→JSON-RPC error mapping
9. Integration tests
10. Documentation

Approve?
> Yes

[Drafting tickets...]
[UX review — round 1: 1 blocker on mental-model fit, 2 concerns on failure paths]
[Planner revises, asks human about MCP-vs-CLI semantics]
[UX review — round 2: APPROVED]
[Implementation review — round 1: 2 blockers, 1 missing ticket found]
[Planner revises, asks human about MCP resources]
[Implementation review — round 2: APPROVED with minor suggestions]

## Tickets Created (11 tickets, 3 batches)
- batch-1: #31-#34
- batch-2: #35-#37
- batch-3: #38-#41

Ready for: /implement-project all tickets tagged batch-1, batch-2, batch-3
```

### Example 2: UX Loop Catches a Trap Before Implementation

```
[UX Review — Round 1]
Target type detected: CLI (with MCP server subcommand surface)

UX reviewer findings:
- BLOCKER (mental-model fit): Tickets #1-3 use "MCP tool" interchangeably
  with "CLI command". An MCP-tool-calling agent and a CLI-typing user
  have different expectations about idempotency, side effects, and
  return shape. The ticket set does not clarify which model governs.
- CONCERN (failure paths): Ticket #7 specifies error code mapping but
  no ticket covers what an MCP client sees when the underlying CLI
  command requires interactive input (confirmation prompts).
- CONCERN (orientation): No ticket addresses how an MCP client knows
  whether a long-running operation is still in progress.
- Verdict: NEEDS REVISION

Without this loop, the interactive-input issue would have been a UX
trap shipped as a bug — technically working, behaviorally broken for
real MCP clients. The planner revises, asks the user about the right
default behavior, and adds a missing ticket for status reporting.
```

### Example 3: Implementation Loop Catches Missing Work

```
[Implementation Review — Round 1]

Implementer findings:
- BLOCKER: Ticket #3 says "map CLI commands to MCP tool definitions"
  but no ticket covers the JSON Schema format MCP requires.
- MISSING TICKET: No ticket for graceful shutdown handling. If the
  stdio pipe closes mid-operation, what happens?
- QUESTION: Ticket #7 says "expose config as MCP resource" but the
  config file contains API keys. Should resources be filtered?

These are all questions that would have blocked implementation.
The planner revises, asks the human about the config filtering,
and adds a missing ticket for shutdown handling.
```

## Integration with Other Skills

| Skill               | Relationship                                                                                                                                       |
|---------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| `/scope`            | Plans a single ticket interactively. `/scope-project` plans an entire project with adversarial review.                                             |
| `/implement-project`     | Implements what `/scope-project` plans. Tickets go upstream with batch labels that `/implement-project` consumes directly. Typical flow: `/scope-project` → `/implement-project`. |
| `/lead-project`     | May invoke `/scope` to draft new tickets when gaps emerge mid-run. `/scope-project` is typically run by the user before `/lead-project` to establish the initial backlog. |
| `/implement-batch`       | Can also consume `/scope-project`'s tagged tickets if only one batch needs implementation.                                                         |
| `/implement`        | Can implement individual tickets from `/scope-project` if full `/implement-project` orchestration isn't needed.                                    |
| `/think-deliberate` | Available within `/scope-project` for difficult design decisions during planning.                                                                   |

**The full pipeline:**
```
/scope-project  →  /implement-project
    plan             implement

/scope-project  →  /lead-project
    plan             autonomous orchestration (intent-driven)
```

## Tips

1. **Be specific during discovery.** The more precise your project description, the better the initial plan. Vagueness at step 1 becomes blockers at steps 6 and 7.

2. **Engage with the plan review.** Step 3 is your chance to shape the project structure. Catch batch ordering issues and missing work here — it's cheaper than finding them during adversarial review.

3. **Welcome reviewer questions from both loops.** When either the UX reviewer or the implementer surfaces questions for you, that's the workflow working. UX questions in particular surface design intent the user has not made explicit — exactly the gaps that produce shipped traps. A question answered during planning saves far more time than the same question asked mid-implementation, or worse, after release.

4. **Trust the convergence process.** Multiple review rounds in either loop are normal, not a sign of failure. Each round improves ticket quality.

5. **Don't be surprised by the escape hatch.** When the implementer surfaces an infeasibility that breaks UX-locked design, returning to step 6 is normal and productive — not a process failure. It is the workflow surfacing a real conflict between UX intent and implementation feasibility, which is precisely what either loop running alone would miss.

6. **Check the implementation notes.** These are what make `/scope-project` tickets superior to hand-written ones — they contain codebase context (file paths, function signatures, patterns) that an implementer would otherwise have to rediscover.

7. **The batch structure matters.** Tickets go upstream with batch labels. Think about what each batch delivers as a coherent increment — batch 1 should be useful on its own, not just a foundation for batch 2.

## Requirements

- `git` repository (for issue tracker detection and codebase exploration)
- Issue tracker integration (GitHub `gh`, Gitea MCP, GitLab `glab`)
- If no integration is available, ticket content is output for manual creation
