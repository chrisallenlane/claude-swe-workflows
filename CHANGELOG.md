# Changelog

## v9.0.0

### New Skills

- **`/tidy-git` — Mechanical local repo hygiene.** A utility skill in the new `/tidy-*` namespace for cleanup operations where the find→fix seam is small enough that running them in one motion is appropriate. Defaults to acting on safe categories (`git remote prune`, `git worktree prune`) and previews-then-confirms borderline-safe categories (merged-branch deletion with `git branch -d` — never `-D`). Reports — without acting on — informational state where judgment is required: stashes, branches with no upstream, branches ahead of upstream, local-only tags, untracked files. Categorical safety invariants forbid force-delete, remote-touching operations, stash drops, `git clean`, and `git gc`; the skill has no flags to override these. Branches deleted by the skill are recoverable from `git reflog` for ~90 days. The skill's three-tier action model (zero-risk auto, borderline-safe preview-and-confirm, report-only) is the design discipline that separates a tidy skill from the underlying git commands it composes.

  The `/tidy-*` namespace is established by this release alongside `/tidy-docs` (renamed from `/review-doc`, see Breaking Changes). The intent is to encode outcome contract in the verb prefix per issue #15: `/review-*` = produces a report, no mutations; `/tidy-*` = mechanical mutations with operator approval where warranted; `/implement-*` = substantive mutations driven by tickets. The namespace will grow organically as concrete candidates earn their keep.

### Breaking Changes

- **`/review-doc` renamed to `/tidy-docs`.** The skill's behavior is unchanged — it still spawns the `doc-maintainer` agent to audit all project documentation and fix issues autonomously within the agent's authority. The rename reflects that the skill is fundamentally a tidy operation, not a review: it does not produce a report-and-stop output the way `/review-*` skills do (and increasingly do — see `/review-arch`, `/review-security`, `/review-test`). The find→fix seam for documentation issues (typos, stale code examples, broken links, freshness drift) is small enough that running find-and-fix in one motion is the right shape.

  The plural ending is intentional: `/tidy-docs` operates on the documentation *corpus* as a whole, not on a single doc. The rule that emerged when naming the new family: singular for uncountable nouns and domain concepts (`/tidy-git`, `/review-test`, `/review-arch`); plural for collection nouns (`/tidy-docs`). Both forms read naturally for their respective domains.

  Operators with muscle memory for `/review-doc` will need to update to `/tidy-docs`. The `doc-maintainer` agent it spawns is unchanged (same name, same prompt, same authority).


- **`/review-test` is now advisory only.** The skill previously surveyed test coverage across five phases (unit, integration, E2E, fuzz, quality) and *implemented* the resulting test changes — writing tests via language SMEs, deleting tautological tests, rewriting brittle ones, running the test suite to verify. In v9.0.0 it is strictly advisory: each phase records its findings into a consolidated report, and after the report is presented, a final step proposes a ticket structure tailored to the review's shape (unit-gap distribution, Mode A vs. Mode B starter strategies in Phases 2 and 3, Phase-5 churn, fuzz-tooling absence), presents the proposal to the operator for approve / edit / decline, and on approval cuts tickets via the canonical tracker integration (`references/trackers.md`). It does not implement test changes.

  The five-phase methodology that defines this skill is untouched. The only change is what happens after findings are produced.

  The principle is the same one driving the v8.0.0 transformations of `/review-arch`, `/review-security`, and `/bug-hunt`: review and implementation are different cognitive concerns, and skills that do both make both worse. For tests specifically, the seam between "find a coverage gap" and "design a test for it" is wide — test design requires fresh reasoning about edge cases, mocking strategy, and assertion shape — and the discovery agents shouldn't be biased toward gaps whose fixes are easy. The same logic applies in reverse to test-quality findings (DELETE / REWRITE / SIMPLIFY): the operator should approve removing or rewriting an existing test explicitly, via a ticket, rather than have a workflow do it as a side effect of running a review.

  Like the v8.0.0 advisory skills, `/review-test` offers ticket creation regardless of caller — orchestrators (`/review-deep`, `/lead-project`, `/implement-project`) receive the proposal and apply their own autonomy judgment per `references/autonomy.md` to approve / edit / decline, then decide which of any created tickets to work in the current flow versus defer.

  Operators who relied on `/review-test` writing tests directly should now invoke `/implement` against the cut tickets, or use `/implement-project` to batch them. The DELETE-containing tickets preserve the reviewer's "rewrite-if-still-valuable" caveat so implementers do not blindly remove tests with hidden value.

### Behavior Changes

- **`/review-deep`, `/implement-project`, and `/lead-project` — adapt to advisory `/review-test`.** The orchestrators that compose `/review-test` (`/review-deep` as Phase 6, `/implement-project` as step 7c, `/lead-project` as part of the targeted-review set and the pre-termination review re-run) now receive a ticket-structure proposal instead of an inline implementation outcome. Each orchestrator applies its own autonomy judgment per `references/autonomy.md` to the proposal. `/implement-project`'s "tests added" tallies in the final report are replaced by "test tickets created / declined / approved-inline." `/lead-project`'s pre-termination review re-run still uses `/review-test` to confirm that no new high-severity findings exist — the contract change is that any such findings would now surface as proposed tickets rather than as in-skill test writes.

- **`/test-mutation` and `/review-test` pairing description updated.** The recommended sequence `/review-test` → `/test-mutation` now includes a `/implement` (or `/implement-project`) step in the middle: `/review-test` surfaces ticket-shaped work; implementation skills work the tickets; then `/test-mutation` strengthens. The pairing is unchanged; only the framing reflects that `/review-test` no longer fills gaps in-skill.

## v8.0.0

### Breaking Changes

- **`/review-arch` is now advisory only.** The skill previously analyzed architecture and *implemented* the resulting blueprint — restructuring modules, moving functions, creating new modules — within the same invocation. In v8.0.0 it is strictly advisory: it produces the target blueprint via noun analysis and offers to cut tickets for the recommended work. The operator (human or orchestrator) approves, edits, or declines the proposal. It does not modify code.

  The principle is that review and implementation are different cognitive concerns, and skills that do both make both worse — implementation pressure compromises the review, and review pressure compromises the implementation. `/review-arch` is the first plugin skill to commit fully to this split; v8.0.0 extends the pattern to `/review-security` and `/bug-hunt` (see below). Future releases may extend further (issue #15 captures the planned namespace restructure).

  All three transformed skills share a single workflow regardless of caller — orchestrators (`/refactor-deep`, `/implement-project`, `/lead-project`) receive the ticket-structure proposal and apply their own autonomy judgment per `references/autonomy.md` to approve, edit, or decline. There is no separate "autonomous mode"; the orchestrator is just another receiver of the same offer.

  Operators who relied on `/review-arch` making changes should either invoke `/implement` against the cut tickets, or use `/refactor-deep` and `/implement-project` — both updated in this release to consume `/review-arch`'s advisory output and implement the parts the orchestrator declines to defer (see Behavior Changes below).

- **`/review-security` is now advisory only.** The skill previously included a Phase 7 "Route to Fixers (Optional)" that spawned language-SME agents to remediate findings, ran `qa-engineer` to verify, and committed each fix atomically. In v8.0.0 it is strictly advisory: after the audit produces consolidated findings, Phase 7 proposes a ticket structure tailored to the audit's shape (severity distribution, chain count, defense-in-depth findings), presents the proposal to the operator for approve / edit / decline, and on approval cuts tickets via the canonical tracker integration (`references/trackers.md`). It does not implement remediation.

  The parallel-isolated blue/red methodology that defines this skill is untouched — Phases 1–6 are unchanged. The only change is what happens after findings are produced.

  Each cut ticket preserves the `Discovered by:` attribution introduced in v7.1.0, so the empirical signal about whether the parallel-isolated first pass is producing value (especially anchoring-suppressed findings) survives the handoff to the tracker.

  Like `/review-arch` (above) and `/bug-hunt` (below), `/review-security` offers ticket creation regardless of caller — orchestrators (`/review-deep`, `/lead-project`, `/implement-project`) receive the proposal and apply their own autonomy judgment per `references/autonomy.md` to approve / edit / decline, then decide which of any created tickets to work in the current flow versus defer. The cognitive seam between "find vuln" and "fix vuln" is wide enough that durable handoff via tickets is valuable even mid-orchestrator-workflow.

  Operators who relied on `/review-security` routing fixes to SMEs should now invoke `/implement` against the cut tickets, or use `/implement-project` to batch the tickets.

- **`/bug-hunt` is now advisory only.** The skill previously included a Phase 6 "Route to Fixers (Optional)" that spawned language-SME agents to remediate confirmed bugs (using the reproducing tests as acceptance criteria), ran `qa-engineer` to verify, and committed each fix atomically. In v8.0.0 it is strictly advisory: after the hunt produces consolidated findings, Phase 6 proposes a ticket structure tailored to the hunt's shape (severity distribution, systemic patterns, reproducing-test count), commits the reproducing tests in a single commit, then cuts tickets that reference the test paths as acceptance criteria.

  The risk-assessment and focused-investigation methodology that defines this skill is untouched — Phases 1–5 are unchanged. The only change is what happens after findings are produced.

  Phase 7 (commit reproducing tests) is preserved as a fallback for when the operator declines ticket creation — the coverage benefit of the reproducing tests isn't lost.

  Like `/review-arch` and `/review-security`, `/bug-hunt` offers ticket creation regardless of caller — orchestrators receive the proposal and apply their own autonomy judgment per `references/autonomy.md` to approve / edit / decline, then decide which of any created tickets to work in the current flow versus defer.

  Operators who relied on `/bug-hunt` routing fixes to SMEs should now invoke `/implement` against the cut tickets, or use `/implement-project` to batch them. The reproducing tests still serve as the acceptance criteria for remediation.

### Behavior Changes

- **`/refactor-deep` — adapts to advisory `/review-arch`; Phase 3 dropped.** The skill previously ran three phases: tactical refactor, advisory architectural review with optional ticket creation, then a re-run of tactical refactor over architectural restructuring. With `/review-arch` no longer implementing changes itself, the third phase has no architectural restructuring to clean up — it is removed. The current shape is Phase 1 (tactical `/refactor`) followed by Phase 2 (`/review-arch` in advisory mode, with the operator deciding what to do with the findings), then a wrap-up `/review-doc` pass. Phase 2 offers to cut tickets when warranted, which can then be fed to `/implement` or `/implement-project`. The ticket-creation preference is collected upfront alongside other Phase-1 inputs so the workflow runs without mid-run interruptions except the one ticket-review pause.

- **`/implement-project` — adopts the autonomy discipline; adapts step 7 to advisory `/review-arch`.** Step 7b previously invoked `/review-arch` to implement architectural changes; the orchestrator now receives `/review-arch`'s ticket-structure proposal and applies its own autonomy judgment to approve / edit / decline. Approved tickets surface in the final report under "Deferred Items / Architectural Recommendations" with ticket numbers; declined items that the orchestrator implemented inline surface under "Architectural Recommendations Acted On." The skill also gains the commander's-intent header now shared across orchestrator-family skills (purpose, key tasks, end state, constraints, non-goals), per the new `references/autonomy.md` discipline. A conditional second `/refactor` pass was removed from the pipeline as part of the rework.

- **`/implement-batch` and `/lead-project` — adopt the shared autonomy discipline.** Both skills now reference `references/autonomy.md` for the altitude rule, cascade rule, no-unilateral-breaking-changes guardrail, pre-loaded options, pre-rebutted recommendations, and risk-budgeted autonomy. These were editorial alignments to the new discipline doc — neither skill's mainline workflow changed.

### Infrastructure

- **`references/autonomy.md` — shared autonomy discipline for orchestrator-family skills.** New top-level reference doc capturing the discipline that governs how orchestrator-family skills (`/lead-project`, `/implement-project`, `/implement-batch`, `/refactor`, `/refactor-deep`, `/review-deep`) decide between acting autonomously and escalating to the operator. Five levers:
  - **Altitude rule** — no andon-cord pulls below architectural / intent level; implementation forks below that line get the skill's best judgment plus a log entry, not a user prompt.
  - **Cascade rule** — when a sub-skill escalates, the parent decides whether the escalation is local to the sub-skill or warrants pulling the cord one level higher.
  - **Pre-loaded options with tradeoffs** — when escalation does happen, always present 2–3 named options with a recommendation and the one tradeoff that would flip it. Never ask "what should I do?"
  - **Pre-rebutted recommendation** — the skill argues against its own pick before presenting.
  - **Risk-budgeted autonomy** — explicit budgets (refactor scope, file count, dep changes) the skill spends before escalating.

  Plus per-skill **commander's-intent schemas** — structured headers (purpose, key tasks, end state, constraints, non-goals) the operator fills at startup so the skill can self-direct.

  Also includes a top-level **no unilateral breaking changes** section as a categorical guardrail: a breaking change to public APIs, function signatures, CLI flags, configuration keys, schemas, wire-protocol fields, or observability fields must be explicitly authorized by the operator. This is a guardrail, not an altitude judgment — the five levers describe how a skill picks among options; this rule constrains the option set itself.

- **`references/trackers.md` — issue-tracker detection convention.** Extracts the detection block (CLAUDE.md > git remote > integration availability) and platform-to-tool map (GitHub → `gh`, Gitea → `mcp__gitea__*`, GitLab → `glab`) that was duplicated across six skills (`/scope`, `/scope-project`, `/implement`, `/implement-batch`, `/implement-project`, `/bug-fix`) into a single shared reference. Per-operation details (fetching, creating, comment-updating, closing tickets) also move to the reference; skill-specific content (which fields each skill fetches, what each skill includes in a close-out comment) stays inline in the citing skill. Adding a new tracker now touches one file instead of six.

- **`references/swe-sme-pattern.md` — SWE SME contract.** Extracts the shared scaffolding that was duplicated across all ten `swe-sme-*` agents (Ansible, CSS, Docker, Go, GraphQL, HTML, JavaScript, Makefile, TypeScript, Zig) into a single canonical reference. Each agent now carries a one-paragraph Operating Contract citation right after `# Purpose` pointing at the canonical doc, with language-specific specializations (best practices, quality checks, idioms) staying inline. The contract covers the 5-step workflow (Understand / Scan / Implement / Test / Verify), Implementation Mode vs. Audit Mode, skip-work protocol, layered testing with `qa-engineer`, refactoring authority bounds, and team coordination with `swe-code-reviewer`. The verbatim `Preserve functionality` line that appeared in eight of ten agents was stripped (CSS and Ansible retain domain-specific variants because their wording specializes the universal rule rather than restating it).

- **README, `CLAUDE.md`, and skill-level documentation updated** to reflect the advisory transformation of `/review-arch`, the revised `/refactor-deep` two-phase shape, the updated `/implement-project` step-7 sequence, and the new reference docs. The `/review-deep` composition description was corrected where it had drifted from current behavior.

## v7.4.0

### New Skills

- **`/pre-compact` — Pre-compaction housekeeping.** A utility skill the user invokes immediately before `/compact` to seal session state that compaction would otherwise destroy. Walks a fixed three-step floor — persistent memory pass (always-on, never conditional: the skill's core promise), git hygiene pass (surface dirty state, ask before committing on the user's behalf), trash cleanup pass (conservative: when in doubt, do not delete) — followed by an open-judgment audit that looks past the checklist for session-specific items the floor cannot anticipate (open threads, undocumented decisions, background processes, stashes, in-flight worktrees). Ends with two outputs: an SBAR-formatted handoff with one of three explicit recommendations (**safe to compact**, **safe after [X]**, or **do not compact yet**), plus a copy-pasteable resume prompt for the post-compaction agent if pending work remains. The resume prompt is drafted while full conversation context is still in scope, producing a much higher-quality handoff than the post-compact agent could reconstruct from the lossy summary; if no work is pending, the skill emits the explicit line "No resume prompt — work is sealed." rather than skipping silently. The skill never invokes `/compact` itself — compaction is the user's call. Designed against an explicit no-escape-hatches discipline: users opt in by invoking, so the skill must reliably do what its name promises rather than offer conditional opt-outs that defeat its core purpose.

## v7.3.0

### Behavior Changes

- **`/scope-project` — discretionary specialist adversarial loops added between the UX loop and the implementer loop.** Previously the skill ran exactly two adversarial loops (UX in step 6, implementer in step 7). v7.3.0 inserts a new step 7 that runs zero or more discretionary specialist adversarial loops — security (`sec-blue-teamer`) and performance (`swe-perf-reviewer`) — between them, renumbering the implementer loop to step 8 and steps 8–10 to 9–11. Each loop structurally mirrors the UX loop: one agent, multi-round converge-to-approval, fresh agent per round, stalemate escalates to user. Existing agents are reused with **spec-time prompt adaptation** in `/scope-project`'s invocation guidance — `sec-blue-teamer` and `swe-perf-reviewer` continue to operate code-time when invoked from other skills. No new agent files were introduced. The discretion is governed by an **architectural filter** as the load-bearing meta-rule: invoke a specialist loop only when the concern would require an architectural change to fix later, not a localized code edit. Triggers (auth/sessions/PII for security, hot paths/scale for performance) operationalize the filter as necessary-but-not-sufficient signals. Loop applicability is decided at step 3 (project plan approval) and surfaced to the user for confirmation/override before drafting begins, locking the choice and giving full visibility upstream of any work. When multiple loops apply, security runs first (rarely negotiable; performance often trades off against security), performance second. Specialist-loop-approved findings become **specialist-locked** (security-locked, performance-locked) — the existing UX escape hatch is generalized so any locked element triggers a return to the loop that locked it, preserving the discipline that downstream loops cannot negotiate prior locks away on grounds of effort. The planner is given **andon-cord** authority to escalate proactively at any round if findings exceed what planning can resolve, the loop seems off-rails, or a finding warrants human judgment — broader than stalemate escalation. A11y is explicitly excluded from the initial pool: most accessibility work (color contrast, alt text, form labels, ARIA attributes) is implementation-time and fails the architectural filter; `qa-web-a11y-reviewer` can still be spawned ad-hoc when a project has a genuinely architectural a11y concern. Validated by an active `/scope-project` run on a user-registration / auth project where planning-time security review caught threat-model gaps, session-storage ambiguity, and three missing tickets (audit logging, account lockout, pepper rotation) before any code was written — each of which would have been an architectural rework if discovered post-implementation.

## v7.2.0

### New Agents

- **`ux-reviewer`** — methodical UX advocate for `/scope-project`'s new first adversarial loop. Walks a fixed seven-concern spine (coherence, completeness, mental-model fit, implicit knowledge, failure paths, power/novice tension, orientation), auto-detecting target type (CLI / MCP / webapp / library / mixed) to choose what evidence to inspect. UX-locked elements become hard constraints on the implementation discussion.

### Behavior Changes

- **`/scope-project` — UX adversarial loop added before the implementer loop.** Previously the skill ran a single adversarial loop pitting a planner against an implementer agent to find gaps, ambiguities, and missing work. v7.2.0 inserts a sequential UX adversarial loop ahead of it: a fresh `ux-reviewer` agent walks the draft ticket set across a seven-concern spine (coherence, completeness, mental-model fit, implicit knowledge, failure paths, power/novice tension, orientation), with target-type auto-detection (CLI / MCP / webapp / library / mixed) governing what evidence to inspect. UX-locked elements become hard constraints on the subsequent implementation discussion, and an escape hatch routes implementer-surfaced UX-breaking infeasibilities back to the UX loop — the implementer cannot negotiate UX away on grounds of effort. The plugin had no UX advocate at any point in any workflow before this change.

### Infrastructure

- **GitHub release automation removed.** `.github/workflows/release.yml` and the entire `.github/` directory have been deleted. Claude Code plugins are distributed by git ref — consumers pin to a tag or branch and the marketplace files in the repo are the actual distribution mechanism — so the GitHub Releases artifact carried no functional payload. Its presence was also actively confusing on the Gitea side: Gitea Actions scans `.github/workflows/` as a fallback and was queuing phantom jobs against a non-existent runner on every tag push. Existing GitHub releases (v1.0.0 through v7.0.0) were deleted out of band; tags are preserved on both Gitea and the GitHub mirror. `HACKING.md` updated to reflect the simplified procedure.

## v7.1.0

### New Skills

- **`/think-premortem` — Prospective failure imagination.** Treats a catastrophic failure as already-having-happened and reasons backward to the causes. Two modes: **plan mode** (a not-yet-committed plan; imagine its failure broadly across lenses) and **scenario mode** (a specific catastrophic scenario posed against an existing system; investigate the actual code and architecture for causes that could have allowed it). Spawns parallel pre-mortemers in isolation across failure-class lenses (technical, operational, estimation, scope, adoption, dependency-and-environment, team-and-coordination, incentive, detection, reversibility, adversarial), plus an always-on `first-principles` lens and 0–3 ad-hoc target-specific lenses. Synthesizes into a prioritized risk register with early-warning signals, calibrated qualitatively (high/moderate/low/uncertain). Sourced from Klein's pre-mortem methodology and the *prospective hindsight* finding from decision research.

- **`/think-ach` — Analysis of Competing Hypotheses.** Operationalizes Richards Heuer's ACH technique (CIA tradition) to systematically narrow among multiple hypotheses against evidence. Spawns parallel hypothesizers across angles (leading, alternative, adversarial, null, deceptive, surprise) and parallel evidence-gatherers across classes (direct-observational, documentary-historical, structural, behavioral, absent, anomalous). Builds an explicit hypothesis-vs-evidence matrix with a four-value scoring system (C/I/N/A, with optional CC/II intensity). **Ranks hypotheses by least disconfirming evidence** — the central methodological insight: hypotheses cannot be proven, only failed-to-be-disproven. Includes diagnosticity analysis, sensitivity analysis, and falsification milestones. Designed to counter confirmation bias, premature closure, anchoring, and cherry-picking. Natural composition: `/think-diagnose` generates candidate causes, `/think-ach` rigorously narrows among them.

### New Agents

- **`thk-premortemer`** — failure imaginer for `/think-premortem` proceedings, parameterized by an assigned failure-class lens. Mode-aware (plan vs scenario) — investigates actual code with file:line citations in scenario mode.
- **`thk-ach-hypothesizer`** — good-faith hypothesis generator for `/think-ach` proceedings, parameterized by a hypothesis-generation angle.
- **`thk-ach-evidence-gatherer`** — good-faith evidence enumerator for `/think-ach` proceedings, parameterized by an evidence class.
- **`qa-test-integration-reviewer`** — integration test gap reviewer. Surveys integration seams and recommends gaps within an existing strategy or, when none exists, proposes a starter strategy with infrastructure and ~5–8 starter tests anchored in critical flows.
- **`qa-test-e2e-reviewer`** — end-to-end browser test gap reviewer. Detects whether the project is a webapp, surveys critical user journeys with Critical/Important/Nice-to-have classification, and prescribes Playwright unconditionally for greenfield Mode A while respecting existing Selenium/Cypress in Mode B (no migration push).

### Behavior Changes

- **`/review-security` — NGT isolation between blue and red first-pass.** The skill previously ran blue-teamer first and then a lead red-teamer informed by the blue-team report — sequential, with explicit information flow blue → red. This created an anchoring failure mode: whatever the blue team flagged became the salient territory for the red team, and gaps the defenders never considered were systematically suppressed. v7.1.0 introduces a parallel-isolated first pass (Nominal Group Technique discipline) followed by a synthesis step that categorizes each finding as **anchoring-suppressed** (red found, blue didn't account for — highest value), **convergent** (both teams independently flagged), **blue-flagged-unverified** (blue flagged, red didn't reach), or **divergent** (one team cleared what the other flagged). The lead red-teamer prompt is rewritten to remove blue-team input dependency for the first pass; focused red-teamers continue to receive blue-team context for targets whose origin includes blue-team data. The final report includes a synthesis section and expanded `Discovered by:` attribution values.

- **`/review-test` — Two new phases (integration, E2E) and inside-out phase ordering.** The skill previously addressed unit coverage gaps, fuzz coverage, and test quality audit — and was fully blind to integration tests and in-browser tests. v7.1.0 inserts Phase 2 (integration coverage) and Phase 3 (E2E coverage, conditional on webapp detection) between unit coverage and fuzz, renumbering the existing fuzz phase to 4 and quality audit to 5. The new phases verify by compile-check only and prompt the user to run the suite ad-hoc — integration and E2E suites are not auto-run, recognizing that they are slow, may require fixtures up, and are often run only pre-release. Phase 3 includes an explicit user-confirmation step on journey classification (the most subjective input in the analysis) before any implementation begins. Mode A E2E recommendations prescribe Playwright unconditionally; Mode B respects existing Selenium/Cypress investment.

### Infrastructure

- **`THINK.md` design discipline document.** Repo-root document that captures the design discipline for the `/think-*` skill family. Includes the **five-test admission gate** for new `/think-*` skills (specific failure mode, practitioner tradition, unskippable questions, NGT discipline, honest "didn't apply"), cross-cutting practices (steelmanning, observation/recollection split, process-vs-luck attribution, calibrated qualitative confidence, prospective hindsight), and intellectual lineage (Kahneman, Tetlock, Schön, Klein, Taleb, de Bono, Delbecq & Van de Ven, Peirce). New `/think-*` skills must clear the five tests; existing `/scope`, `/implement`, `/refactor`, etc. are admitted by different criteria. A "spillover" section notes which practices apply across the plugin.

- **`CLAUDE.md` updated** to reference `THINK.md` and require new `/think-*` skills to pass its admission gate.

- **README.md and skill-level documentation updated** to position the new skills, agents, and workflow changes in the catalog and rules-of-thumb table.

## v7.0.0

### Breaking Changes

- **`/review-health` completely redesigned as a strategic-orientation skill.** The skill's behavior has changed substantially. In prior versions (introduced at v4.2.0), `/review-health` dispatched language-specific SME agents to evaluate idiomatic usage, consistency, and code quality, producing a consolidated health report with per-language ratings. In v7.0.0 it is a first-pass strategic-orientation review: it classifies the repository against a reference class and produces an evidence-cited map — not a grade — calibrated to that class. Output is advisory, intended to help the operator decide where to engage, where to tread carefully, and where to leave alone.

  Operators who relied on the prior per-language code-health ratings should switch to `/review-arch` (architectural analysis) and `/review-security` / `/review-perf` (quality dimensions previously folded into the health skill). Operators invoking `/review-deep` will see the new strategic-orientation behavior as Phase 1 of that pipeline.

### New Skills

- **`/lead-project` — Autonomous technical lead.** Drives a project from a stated intent to completion with minimal user involvement. The user provides **commander's intent** at startup in five structured fields (purpose, key tasks, end state, constraints, non-goals); the skill then runs an **OODA loop** (Observe → Orient → Decide → Act) invoking other skills (`/scope`, `/implement`, `/refactor`, `/review-*`, `/bug-*`, `/think-*`) as it judges appropriate.

  Termination is mechanically gated: every end-state condition classified as "mechanical" (shell-runnable) must actually execute and pass; a pre-termination review re-run (at minimum `/review-test` + `/review-release`) must produce no new high-severity findings; constraint violations must be clean; and two-cycle quiescence over git diff must hold. Subjective end-state conditions are surfaced to the user in the completion report rather than self-declared met. Trajectory audits every 10 cycles read git log / diff / intent directly (not the cycle log narrative) and can pull the andon cord on drift or thrash. Reviewer tie-breaker: contradictory review findings on the same file pull the cord rather than oscillate. State persisted in `LEAD_PROJECT_STATE.md` (gitignored) with branch SHAs recorded for resume safety. Hard cap of 50 cycles.

  Sits one layer above `/implement-project` in the plugin hierarchy. User acts as product owner; the skill fills the project-manager / tech-lead role.

### Infrastructure

- **README, `CLAUDE.md`, and downstream skill READMEs updated** to position `/lead-project` at the top of the orchestration hierarchy and cross-reference from `/implement-project`, `/refactor-deep`, `/review-deep`, and `/scope-project`.

## v6.1.0

### New Skills

- **`/review-deep` — Comprehensive pre-release review pipeline.** Thin orchestrator that runs every `/review-*` skill in sequence: `/review-health`, `/review-arch`, `/review-security`, `/review-perf`, `/review-a11y`, `/review-test`, `/review-doc`, `/review-release`. Each sub-skill keeps its normal interactive behavior — the operator participates throughout. The orchestrator auto-detects phases that do not apply (no web content → no a11y; no tests → no test review; no executable source → no security/perf) and asks for confirmation on the skip list before starting. Includes branch safety check to avoid committing directly to main/master, and ends with a consolidated report that synthesizes findings across all phases.

### Infrastructure

- **Release automation moved from `Makefile` to a Claude-assisted procedure.** The top-level `Makefile` has been removed; release cutting is now driven by a procedure documented in `HACKING.md`. This is an internal workflow change — no effect on the public skill interface.

## v6.0.0

### Breaking Changes

- **Two skills renamed:**
  - `/deliberate` → `/think-deliberate` (moved into the new `/think-*` namespace for pure-reasoning skills that produce no tangible artifacts)
  - `/audit-security` → `/review-security` (the `audit-*` namespace is reserved for heavier tooling; security review fits the `/review-*` naming pattern alongside `/review-arch`, `/review-test`, `/review-health`, etc.)

  Update any invocations or scripts that reference the old names.

### New Skills

The v6.0.0 release introduces a complete `/think-*` namespace for structured reasoning skills. Each skill formalizes a specific cognitive discipline that humans habitually skip, using parallel specialist agents with Nominal Group Technique (independent generation, then synthesis) to avoid anchoring. All `/think-*` skills produce feedback only — no code, tickets, or artifacts.

- **`/think-reframe` — Problem redefinition before problem solving.** Extracts premises from a stated problem, then spawns parallel reframers applying different lenses (problem-vs-symptom, scope-shift, stakeholder-shift, level-of-abstraction, time-horizon, inversion, category-shift, constraints-shift), and synthesizes with an orchestrator recommendation (keep original / adopt reframing / further explore). Sits upstream of `/think-brainstorm` in the natural reasoning pipeline.

- **`/think-brainstorm` — Divergent idea generation.** Validates assumptions in a goal, then spawns parallel brainstormers running different techniques in isolation (first-principles, working-backwards, lateral, analogical, constraints-shift, worst-possible-idea, six-hats-green, SCAMPER). Synthesizes into a catalog of standouts, hybrid ideas, and clustered alternatives.

- **`/think-diagnose` — Abductive reasoning about causes.** Takes a phenomenon, separates observations from interpretations (enforced three-bucket split), then spawns parallel diagnosticians across reasoning lenses (technical, human-factors, process, incentive-structure, environmental, temporal, measurement-artifact, statistical). Hybrid generative + evaluative — the orchestrator evaluates candidate causes against evidence and calibrates confidence qualitatively (no fabricated percentages).

- **`/think-scrutinize` — Devil's advocate for ideas.** Stress-tests an idea through parallel skeptics applying different critical lenses, pairs them with an advocate defending the idea in good faith, runs counter-rebuttal, and synthesizes a report of faults that survived cross-examination.

- **`/think-reflect` — Retrospective learning from completed experience.** Extracts learnings from a completed project, incident, decision, or time period. Enforces observation-vs-recollection split during ground-truth gathering (memory drifts; git logs don't). Spawns parallel reflectors (what-worked-vs-got-lucky, what-didn't, what-surprised, system-rewards-vs-intent, decisions-that-aged, what-to-tell-past-self, patterns-that-recur) and surfaces **updated mental models** as first-class output.

- **`/think-deliberate` — Adversarial decision-making.** (Renamed from `/deliberate`.) Spawns advocate agents per option who argue their cases, rebut each other, and respond to probing questions before a judge renders a verdict.

### New Agents

- **`thk-brainstormer`** — Good-faith idea generator parameterized by brainstorming technique.
- **`thk-diagnostician`** — Good-faith abductive reasoner that generates candidate causes through an assigned reasoning lens.
- **`thk-reflector`** — Good-faith reflector that extracts learnings from an experience through an assigned reflection lens.
- **`thk-reframer`** — Good-faith reframer that restates a problem through an assigned reframing lens.
- **`thk-skeptic`** — Good-faith skeptic that identifies faults in an idea through an assigned critical lens. (Replaces `scrutinizer`.)
- **`thk-advocate`** — Argues in good faith for an assigned position in adversarial proceedings. Used by both `/think-deliberate` and `/think-scrutinize`. (Renamed from `advocate`.)

Agent names are internal implementation details per the [Versioning](README.md#versioning) policy.

### Design Pattern

All `/think-*` skills share a consistent architecture: one generalist agent parameterized by lens/technique, spawned in parallel and isolation (Nominal Group Technique — independent generation prevents anchoring), with orchestrator-led synthesis. This pattern is documented in each skill's `SKILL.md` and should be followed for any future `/think-*` additions.

## v5.1.0

### New Skills

- **`/refactor-deep` — Comprehensive tactical + architectural refactoring.** Convenience workflow that runs `/refactor` (tactical cleanup), `/review-arch` (architectural restructuring), then `/refactor` again (post-restructuring cleanup). All user input gathered upfront; fully autonomous after that. Includes branch safety check to avoid committing directly to main/master.

## v5.0.0

### Breaking Changes

- **Three skills renamed for consistency:**
  - `/bugfix` → `/bug-fix`
  - `/audit-source` → `/audit-security`
  - `/review-source` → `/review-health`

  Update any invocations or scripts that reference the old names.

### New Skills

- **`/bug-hunt` — Proactive bug discovery.** Systematically hunts for bugs before they reach users. An assessor cross-references code complexity, test coverage gaps, and structural risk factors to produce a ranked hotspot list. Focused hunters then deep-dive into each hotspot, writing reproducing tests to validate or invalidate suspected bugs. Every confirmed finding is backed by a reproducing test. Optionally routes confirmed bugs to SME agents for fixing.

### New Agents

- **`swe-bug-assessor`** — Codebase risk assessor. Cross-references complexity, coverage, structural risk factors, and git history to identify where bugs are most likely to lurk. Produces a ranked hotspot list for focused investigation.
- **`swe-bug-hunter`** — Focused bug investigator. Deep-dives into specific code regions identified by the assessor, writes reproducing tests for suspected bugs, and validates findings through test execution. Keeps valuable tests even when they invalidate a suspicion.

## v4.4.1

### Improvements

- **`/test-mutation` now runs on autopilot.** After initial setup, the workflow processes all pending modules unattended and commits per module, rather than pausing for user selection at each step.
- **`/review-release` simplified.** Removed the Phase 1 pause between static analysis and execution checks for a smoother review flow.
- **Web SMEs now dispatched by all skills.** The TypeScript, JavaScript, HTML, and CSS SME agents (added in v4.0.0) are now listed in the operational instructions for `/refactor`, `/review-arch`, `/bug-fix`, `/test-mutation`, and `/review-test`. Previously these skills would fall back to direct implementation for web languages despite dedicated SMEs being available.
- **`/review-perf` agent references standardized.** Now uses kebab-case agent identifiers consistent with all other skills.
- **Co-Authored-By lines removed from commit templates** across all skills.
- **Skill reference docs renamed** from `references/guide.md` to `references/README.md` for consistency.

## v4.4.0

### New Skills

- **`/review-perf` — Performance review.** Detects whether a project contains web content, non-web source code, or both, and dispatches the appropriate performance reviewer(s) in parallel. Produces a consolidated report with cross-domain synthesis. Advisory only.

### New Agents

- **`swe-web-perf-reviewer`** — Web performance reviewer. Identifies network, caching, loading, and asset delivery issues from source code analysis. Covers caching strategy, asset delivery, critical rendering path, resource hints, image optimization, JS/CSS cost, network overhead, and Core Web Vitals risk factors. Advisory only.

### Improvements

- **Agent naming standardized.** All advisory "examine and report" agents now use the `reviewer` suffix. Test-related QA agents grouped under `qa-test-*` namespace. Web-specific agents namespaced with `web`. Full rename list:
  - `swe-review-arch` → `swe-arch-reviewer`
  - `swe-refactor` → `swe-code-reviewer`
  - `swe-diagnostician` → `swe-bug-investigator`
  - `swe-perf-engineer` → `swe-perf-reviewer` (now advisory only)
  - `qa-release-eng` → `qa-release-engineer`
  - `qa-accessibility-auditor` → `qa-web-a11y-reviewer`
  - `qa-test-auditor` → `qa-test-reviewer`
  - `qa-coverage-analyst` → `qa-test-coverage-reviewer`
  - `qa-fuzz-analyst` → `qa-test-fuzz-reviewer`
- **`swe-perf-reviewer` is now advisory only.** Formerly `swe-perf-engineer` with implementation authority. Now follows the same advisory pattern as all other reviewers, routing findings to language SMEs.
- **Versioning policy documented.** Skills (slash commands) are the public interface. Agent names are internal implementation details and may change without a major version bump.

## v4.3.0

### New Skills

- **`/review-a11y` — WCAG accessibility audit.** Advisory-only skill that dispatches an accessibility auditor to identify WCAG conformance gaps, prioritize findings by user impact, and recommend fixes. No changes are made — the output is an assessment report.

### Improvements

- **`/audit-security` now defaults to production-only scope.** Test code, dev-only dependencies, generated code, and vendored code are excluded by default. Users can override these exclusions during scope selection.
- **`/audit-security` now reports all severity levels.** LOW findings are no longer suppressed when CRITICAL or HIGH findings exist. All priority levels (CRITICAL, HIGH, MEDIUM, LOW) now get dedicated focused red-teamer agents, with a target cap increased from 10 to 25.

## v4.2.0

### New Skills

- **`/review-health` — Code health assessment.** Advisory-only skill that detects all languages in a project, dispatches language-specific SME agents (or generalists for unsupported languages) to evaluate idiomatic usage, consistency, and quality, and produces a consolidated health report with per-language ratings. Use to decide whether `/refactor` is needed.

## v4.1.0

### New Skills

- **`/audit-security` — White-box security audit.** Orchestrates a comprehensive security assessment using both defensive and offensive analysis. The blue-teamer evaluates defensive posture first; the lead red-teamer performs reconnaissance informed by those gaps; focused red-teamers investigate each vector in depth; findings are synthesized and exploit chains explored until no new chains emerge.

### New Agents

- **`sec-red-teamer`** — Adversarial security analyst. Attacks the codebase from an attacker's perspective to find concrete exploitable vulnerabilities. Works as the offensive counterpart to `sec-blue-teamer`.
- **`sec-blue-teamer`** — Defensive security analyst (renamed from `sec-reviewer`). Evaluates security posture through control inventory, consistency checking, defense-in-depth assessment, and dependency hygiene. Runs as the first step in `/audit-security`, feeding its defense evaluation to the red team.

### Improvements

- Both `sec-blue-teamer` and `sec-red-teamer` report incidental non-security bugs discovered during their analysis in a dedicated `NON-SECURITY BUGS` section.
- **`/scope`** and **`/scope-project`** ticket templates now include a **Security considerations** field, prompting authors to note new attack surface, input handling, auth/authz changes, and trust boundary impacts.

## v4.0.0

### Breaking Changes

- **Five skills and agents renamed for verb-noun consistency:**
  - `/arch-review` → `/review-arch` (agent `swe-arch-review` → `swe-review-arch`)
  - `/doc-review` → `/review-doc`
  - `/release-review` → `/review-release`
  - `/test-review` → `/review-test`
  - `/test-mutate` → `/test-mutation`

  Update any invocations or scripts that reference the old names.

### New Agents

- **`swe-sme-html`** — HTML structure, semantics, and accessibility specialist. Dispatched by `/implement`, `/refactor`, `/review-arch`, and `/bug-fix` for web projects.
- **`swe-sme-css`** — CSS styling, layout, and responsive design specialist. Covers Flexbox, Grid, custom properties, and modern CSS features.
- **`swe-sme-javascript`** — Vanilla JavaScript implementation specialist (ES modules, async/await, DOM APIs). Defers to TypeScript SME when the project uses TypeScript.
- **`swe-sme-typescript`** — TypeScript implementation specialist. Covers strict-mode configuration, type design, generics, and compiler discipline.
- **`qa-accessibility-auditor`** — WCAG 2.2 AA accessibility auditor. Advisory-only role: identifies barriers, prioritizes by user impact, and provides remediation guidance for HTML/CSS/JS implementers.

## v3.0.0

### Breaking Changes

- **`/iterate` renamed to `/implement`.** The single-ticket implementation workflow is now
  `/implement`. If you were using `/iterate`, use `/implement` instead.

- **`/batch` renamed to `/implement-batch`.** The multi-ticket orchestration workflow is now
  `/implement-batch`. If you were using `/batch`, use `/implement-batch` instead.

- **`/project` renamed to `/implement-project`.** The full-lifecycle project workflow is now
  `/implement-project`. If you were using `/project`, use `/implement-project` instead.

The skill directories have been renamed accordingly (`skills/iterate/` → `skills/implement/`,
etc.). Any local references to the old skill names in scripts or documentation should be updated.

## v2.0.0

### Breaking Changes

- **`/implement-project` renamed to `/implement-batch`.** The v1.x `/implement-project` skill (single-batch
  ticket orchestration) is now `/implement-batch`. The `/implement-project` name is used by a new,
  higher-level workflow (see below). If you were using `/implement-project` to implement
  a single batch of tickets, use `/implement-batch` instead.

### New Skills

- **`/implement-project` — Full-lifecycle project workflow.** Orchestrates an entire
  multi-batch project: implements batches via `/implement-batch`, runs smoke tests, then
  executes a comprehensive quality pipeline (refactor, review-arch,
  review-test, review-doc, review-release). Maximizes autonomy with andon cord
  escalation.

- **`/scope-project` — Adversarial project planning.** Plans a multi-batch
  project through adversarial review. Drafts tickets organized into batches,
  then pits a planner against an implementer agent to find gaps and
  ambiguities. Produces tagged tickets ready for `/implement-project` consumption.

### Improvements

- Rewrote top-level README to present skills as a cohesive layered system
  rather than a flat list
- Added `make release` target for tagging and publishing releases

## v1.1.0

Initial tagged release.
