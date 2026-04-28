# /scope-project - Adversarial Project Planning

## Overview

The `/scope-project` skill plans an entire project through sequential adversarial review loops. It explores the problem space, drafts tickets organized into batches, then runs a mandatory UX loop ("should we build this?"), zero or more discretionary specialist loops (security, performance) for projects with architectural implications in those domains, and a mandatory implementer loop ("could we build this?"). Only when every applicable loop signs off do the tickets go upstream — already tagged with batch labels ready for `/implement-project` to consume.

**Key benefits:**
- Layered adversarial review catches different classes of planning gap: UX (step 6) for design cogency, specialist loops (step 7) for architectural quality concerns, implementation (step 8) for technical viability
- The architectural filter governs specialist loop invocation, preventing checklist behavior on projects where the domain isn't load-bearing
- Locked elements (UX-locked, security-locked, performance-locked) become hard constraints on downstream loops, not items later reviewers can negotiate away
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
 │    constraints for steps 7 and 8             │
 └──────────────────┬───────────────────────────┤
                    ▼                           │
            UX reviewer approved?               │
            ├─ No  → Fresh ux-reviewer ─────────┘
            │        (or escalate if stalemated)
            └─ Yes ▼
    ┌────────────────────────────────────┐
    │ SPECIALIST LOOPS (DISCRETIONARY)   │
    │ Architectural filter governs       │
    │ invocation. Skip if none apply.    │
    │                                    │
    │ Per loop (security, then perf):    │
    │ • Spawn specialist agent           │
    │ • Planner addresses findings       │
    │ • Fresh agent per round            │
    │ • Andon cord: planner can          │
    │   escalate any time                │
    │ • Approved findings → locked       │
    │   elements (constraints for        │
    │   step 8)                          │
    └─────────────┬──────────────────────┘
                  ▼
    ┌───────────────────────────┐
    │ IMPL ADVERSARIAL REVIEW   │◄──────────────┐
    └─────────────┬─────────────┘               │
                  ▼                             │
 ┌──────────────────────────────────────────────┐
 │  8a. IMPLEMENTER REVIEWS ALL TICKETS         │
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
 │  8b. PLANNER ADDRESSES FEEDBACK              │
 │  ────────────────────────────────────────    │
 │  • Resolve blockers (revise tickets)         │
 │  • Answer questions (or ask human)           │
 │  • Accept/decline suggestions                │
 │  • Draft missing tickets if needed           │
 │  • Adjust batch structure if needed          │
 │                                              │
 │  ESCAPE HATCH: if a finding requires         │
 │  changing any locked element (UX, security,  │
 │  performance), return to the loop that       │
 │  locked it (step 6 or step 7) with the       │
 │  constraint, then resume                     │
 └──────────────────┬───────────────────────────┤
                    ▼                           │
            Implementer approved?               │
            ├─ No  → Fresh implementer ─────────┘
            │        (or escalate if stalemated)
            └─ Yes ▼
 ┌──────────────────────────────────────────────┐
 │  9. PRESENT FINAL TICKETS TO USER            │
 │  ────────────────────────────────────────    │
 │  Summary view of all tickets and batches     │
 │  Review round counts and clarifications      │
 │  Wait for user approval                      │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  10. CUT TICKETS UPSTREAM                    │
 │  ────────────────────────────────────────    │
 │  • Create batch labels (batch-1, batch-2)    │
 │  • Spawn one subagent per ticket             │
 │  • Apply batch labels + other tags           │
 │  • Present issue URLs                        │
 └──────────────────┬───────────────────────────┘
                    ▼
 ┌──────────────────────────────────────────────┐
 │  11. CLEAN UP                                │
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

The orchestrator synthesizes discovery and exploration into a structured plan: batch structure with ordering rationale, ticket inventory per batch, dependencies, risk areas, and **applicable specialist loops**.

**Applicable specialist loops.** As part of the plan, the orchestrator applies the architectural filter (see step 7) to identify which discretionary specialist loops will run. For each candidate (security, performance), it states whether the loop applies, with architectural rationale. This locks the decision before drafting begins and gives you full visibility — you can override the planner's selection (add a loop it skipped, or skip a loop it included).

**The plan is presented to you for approval** — the primary human checkpoint. You can adjust batches, add/remove tickets, reorder, override specialist-loop selection, or ask questions. The plan must be approved before ticket drafting begins.

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

Findings are categorized as **blocker / concern / suggestion** with a verdict of `APPROVED` or `NEEDS REVISION`. The planner addresses each: revise tickets, ask the user for clarification on user populations or design intent, or accept/decline suggestions. A fresh `ux-reviewer` re-reviews each round. UX-locked elements approved by the loop become hard constraints for steps 7 and 8.

### 7. Specialist Adversarial Review Loops

Zero or more discretionary specialist loops, governed by an **architectural filter**: invoke a specialist loop only when the concern would require an architectural change to fix later, not a localized code edit. Most projects skip this step entirely; the discipline is in *not* invoking when the concern isn't architectural.

Initial pool: security and performance. Each loop structurally mirrors the UX loop (one agent, multi-round converge-to-approval, fresh agent per round, stalemate escalates to user).

| Loop          | Trigger heuristics (necessary but not sufficient)                                                | Agent (spec-time)    |
|---------------|--------------------------------------------------------------------------------------------------|----------------------|
| Security      | Auth, registration, sessions, crypto, PII, payments, file uploads, multi-tenancy, trust boundaries | `sec-blue-teamer`    |
| Performance   | Hot paths, large-scale data, real-time / latency-sensitive, batch processing at scale            | `swe-perf-reviewer`  |

Applicability is decided at step 3 (project plan approval), not later — locking the choice before drafting prevents mid-flow renegotiation. When multiple loops apply, security runs first (rarely negotiable; performance often trades off against security), performance second.

The agents are reused with **spec-time prompt adaptation**: each loop's invocation prompt frames the task as design review, not code audit. Findings should be design-shaping (architectural choices, missing controls, threat-model gaps) rather than code-level (library choice, micro-optimizations). Findings approved by the loop become **specialist-locked** (security-locked, performance-locked) — hard constraints for step 8.

**Andon cord.** The planner has authority to escalate to you at any point during a specialist loop, not just on stalemate. Pull the cord when findings exceed what planning can resolve, when the loop seems off-rails, or when a finding warrants human judgment.

**A11y is not in the initial pool.** Most accessibility work is implementation-time and fails the architectural filter. Genuinely architectural a11y concerns exist but are rare; if a project has one, the planner can spawn `qa-web-a11y-reviewer` ad-hoc rather than codifying a standing loop.

### 8. Implementation Adversarial Review Loop

The mandatory feasibility loop. An implementer agent reviews all tickets as if assigned to implement them tomorrow, looking for:

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

**Locked elements from steps 6 and 7 are constraints, not items the implementer can negotiate away.** UX-locked, security-locked, and performance-locked elements stand. The implementer reviews implementability against those constraints; it does not get a second pass at design intent or quality posture.

**The planner addresses each finding** by revising tickets, asking you for clarification, or pushing back. A fresh implementer then re-reviews. This continues until the implementer approves or the process stalemates (at which point you're brought in).

**Asking you for clarification is normal.** The adversarial review surfaces questions that should be answered during planning, not during implementation. A question surfaced here saves much more time than the same question surfaced mid-implementation.

**Escape hatch to the relevant prior loop.** If the implementer surfaces a finding that cannot be addressed without changing a locked element (UX-locked, security-locked, or performance-locked), the planner returns to the loop that locked the element with the new constraint as input. That loop reconverges; step 8 then resumes. This prevents implementer-wins-by-default — design and quality requirements stand unless physically infeasible.

### 9. Present Final Tickets

After every applicable loop approves, the complete ticket set is presented for your final review. You can inspect any ticket in detail and request adjustments before creation.

### 10. Cut Tickets Upstream

Batch labels are created first, then tickets are created with labels applied. Each ticket includes the batch tag so `/implement-project` can consume them directly.

### 11. Clean Up

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

The layered adversarial review loops are the distinguishing feature of `/scope-project`. Together they answer three questions:

- **Step 6 (UX loop, mandatory): "Should we build this?"** — surfaces user-experience problems before implementation begins. Catches mental-model misfits, dead ends, missing recovery paths, power/novice imbalances, and the kind of UX defects that ship as bugs.
- **Step 7 (Specialist loops, discretionary): "Is this sound on quality dimension X?"** — surfaces architectural quality concerns in domains where the project is load-bearing (security, performance). Skipped entirely when no specialist loops apply.
- **Step 8 (Implementer loop, mandatory): "Could we build this?"** — surfaces technical gaps. Catches vague requirements, unclear dependencies, missing tickets, batch-ordering issues, and stale code references.

The loops are sequential — earlier loops produce locked elements that downstream loops cannot negotiate away. Locked elements (UX-locked, security-locked, performance-locked) stand unless physically infeasible. If the implementer surfaces an infeasibility against any locked element, the planner returns to the loop that locked it (the generalized escape hatch).

**Different perspectives catch different gaps.** The planner thinks about what needs to be done. The UX reviewer thinks about whether users will succeed. The security reviewer thinks about threat models and trust boundaries. The performance reviewer thinks about scaling and contention. The implementer thinks about what they'd need to know to do it. These are fundamentally different lenses.

**Fresh instances prevent anchoring.** Each review round spawns a new agent with a clean context. The new instance isn't anchored to the previous round's findings — it sees the tickets fresh and may notice different issues.

**The architectural filter prevents checklist behavior.** Specialist loops exist for projects where security or performance has *architectural* implications — concerns that would require rework to fix later. The filter is asked first, before any trigger heuristic. Most projects skip this step; for those that warrant it, the planning-time review prevents the kind of architectural defect that's catastrophic to bolt on later.

**Convergence, not perfection.** The goal isn't to document every conceivable edge case — it's to reach a state where the design is UX-cogent, sound on every applicable quality dimension, and implementable without guessing. Most projects converge in 1-2 rounds at each loop.

**Stalemate triggers human involvement.** If a loop keeps cycling on the same issues, something fundamental is ambiguous. UX stalemate usually means design intent the user has not made explicit; specialist stalemate usually means a quality requirement the user has not stated; implementation stalemate usually means the planner and implementer have a legitimate disagreement requiring human judgment. The planner can also pull the andon cord proactively during a specialist loop without waiting for stalemate. Either way, bringing the user in is the right move — the adversarial process has done its job by surfacing exactly what needs human judgment.

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

### Example 4: Security Loop on an Auth Project

Specialist loops only run when the architectural filter admits them. This example shows the security loop catching architectural gaps in a user-registration project before any code was written.

```
## Project Plan: user registration and authentication

### Batch 1: Auth foundations (4 tickets)
1. Schema and password hashing
2. Registration with email verification
3. Login and session creation
4. Logout and session invalidation
[...]

Applicable specialist loops:
- Security: YES. Auth model, session storage, token generation, and
  trust boundaries are architectural choices. Getting these wrong
  would require rework, not localized fixes — architectural filter
  passes.
- Performance: NO. Auth flows are not performance-critical at expected
  scale; rate limiting is in scope but doesn't require architectural
  performance review.

[UX loop — converged in 1 round]

[Security Loop — Round 1]
Spawning sec-blue-teamer (spec-time mode)...

Security findings:
- BLOCKER: No threat model documented. Tickets imply protection against
  credential stuffing and account takeover but never state it.
- BLOCKER: Session storage strategy unspecified. Server-side sessions?
  Stateless JWTs? Choice has architectural consequences for logout
  semantics, revocation, and horizontal scaling.
- CONCERN: Email verification token generation unspecified — random
  source, length, expiry.
- MISSING TICKET: No audit logging ticket. Auth events without an audit
  trail are an architectural gap.
- MISSING TICKET: No account lockout policy after repeated failed logins.
- Verdict: NEEDS REVISION

Addressing security findings — added explicit threat model, locked
session strategy to server-side rotation, specified token generation
parameters, added audit logging ticket, added lockout policy ticket.

[Security Loop — Round 2: APPROVED]

Security-locked elements: threat model, session strategy, token
parameters, audit logging requirements, lockout policy.

[Implementation loop respected security-locked elements; no escape-hatch
loop-back required.]
```

The security loop caught the threat-model gap, the session-storage ambiguity, and three missing tickets before any code was written. Each would have been an architectural rework if discovered post-implementation — exactly the kind of catastrophic-to-bolt-on concern this loop exists to catch.

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

1. **Be specific during discovery.** The more precise your project description, the better the initial plan. Vagueness at step 1 becomes blockers at steps 6, 7, and 8.

2. **Engage with the plan review and specialist-loop selection.** Step 3 is your chance to shape the project structure *and* override the planner's specialist-loop selection. If the planner skipped a loop you think applies, add it. If the planner included one that doesn't, skip it. Catch batch ordering issues and missing work here too — it's cheaper than finding them during adversarial review.

3. **Welcome reviewer questions from any loop.** When the UX reviewer, a specialist reviewer, or the implementer surfaces questions for you, that's the workflow working. UX questions surface design intent; specialist questions surface quality requirements you may not have stated; implementer questions surface technical ambiguity. A question answered during planning saves far more time than the same question asked mid-implementation, or worse, after release.

4. **Trust the convergence process.** Multiple review rounds in any loop are normal, not a sign of failure. Each round improves ticket quality.

5. **Don't be surprised by the escape hatch.** When the implementer surfaces an infeasibility that breaks any locked element (UX, security, performance), returning to the loop that locked it is normal and productive — not a process failure. It is the workflow surfacing a real conflict between intent and implementation feasibility, which is precisely what either loop running alone would miss.

6. **Trust the architectural filter.** Most projects skip step 7 entirely. That's the filter working as intended — discretionary loops should be invoked only when concerns are architectural, not when they're code-level. Resist the urge to add specialist loops "just to be thorough."

7. **Check the implementation notes.** These are what make `/scope-project` tickets superior to hand-written ones — they contain codebase context (file paths, function signatures, patterns) that an implementer would otherwise have to rediscover.

8. **The batch structure matters.** Tickets go upstream with batch labels. Think about what each batch delivers as a coherent increment — batch 1 should be useful on its own, not just a foundation for batch 2.

## Requirements

- `git` repository (for issue tracker detection and codebase exploration)
- Issue tracker integration (GitHub `gh`, Gitea MCP, GitLab `glab`)
- If no integration is available, ticket content is output for manual creation
