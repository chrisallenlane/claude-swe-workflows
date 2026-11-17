# Changelog

## v12.0.0

### Removed

- **BREAKING: `/review-health` is renamed `/review-repo` and absorbs `/review-arch`, `/review-dead`, `/review-value`, and `/review-namespace` as focuses. `/review-code` is removed.** Six whole-codebase review commands become one. Most of the folded skills were thin wrappers around one agent, and in practice their methods reached users through the agents: `/scope` dispatches the value engineer, and the map's follow-up runs the dead-code and architecture reviewers. All of that method lives in the agents, which the consolidation keeps whole; their later contract fixes are listed under Fixed.
  - **Migration:**

    | Before                       | After                                                                                                                                                    |
    |------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
    | `/review-health [scope]`     | `/review-repo [scope]`, the same orientation map. Its "lens" question is now called the review *context*                                                 |
    | `/review-arch [scope]`       | `/review-repo architecture [scope]`                                                                                                                      |
    | `/review-dead [scope]`       | `/review-repo dead-code [scope]`                                                                                                                         |
    | `/review-namespace [search]` | `/review-repo namespace [search] [scope]`. The procedure moved verbatim to `skills/review-repo/references/namespace.md`, loaded only for this focus      |
    | `/review-value [scope]`      | `/review-repo value [scope]`                                                                                                                             |
    | `/review-code [range]`       | Removed. `/implement` and `/bug-fix` still run `swe-correctness-reviewer` as a blocking gate; for other diffs, use Claude Code's built-in `/code-review` |

  - **What each focus keeps.**
    - `architecture` presents the blueprint in four parts: noun analysis, proposed changes, the modules left alone, and behavior-altering changes flagged for approval.
    - `dead-code` presents its calibration first and sends uncertain findings to verification tickets, never removal tickets.
    - `value` never advocates, never lets an orchestrator rule on a flagged trade, and makes amending the requirement's record the first acceptance criterion of every approved trade.
    - `namespace` keeps its whole instrument, Laws of the Instrument included, and search mode still runs only on explicit opt-in.
  - **Several focuses together** (`/review-repo value dead-code architecture namespace`) run in dependency order, each receiving the previous one's output. In namespace search mode, the architecture blueprint is seeded as a candidate tree, so the analyst's proposal is tested by the measurement.
  - **Also:** `REVIEW_HEALTH_STATE.md` is now `REVIEW_REPO_STATE.md`. `/implement`'s repertoire, the autonomy and advisory-ticket references, the README, and `CLAUDE.md` are updated.

- **BREAKING: `/think-reframe` and `/think-ach` become phases of the skills they always fed.** Under `references/think.md`'s "skill versus phase" test, neither earned its own command: reframing only ever ran upstream of brainstorming, and ACH only ever narrowed diagnose's candidates.
  - **`/think-reframe` is now `/think-brainstorm`'s framing check.** It runs when assumption validation leaves the framing itself in doubt, when the problem is stuck or the debate won't converge, or when you ask "is this even the right problem?". It spawns the same isolated `thk-reframer` agents with the same eight lenses, classifies each reframing (shifts / refines / holds), and you choose the framing to brainstorm. `/scope` can also spawn reframers while it is still understanding a contested problem, before it explores the code.
  - **`/think-ach` is now `/think-diagnose`'s narrowing step.** It runs when 3 or more candidates survive at moderate fit or better, or are tied, and evidence can discriminate among them. It keeps Heuer's procedure intact: null and deceptive hypotheses added, isolated `thk-ach-evidence-gatherer` agents per evidence class, the C / I / N/A matrix with independent cells, diagnosticity, ranking by **least** disconfirmation (non-negotiable), sensitivity analysis, and falsification milestones.
  - **`thk-ach-hypothesizer` is removed.** Diagnose's own diagnosticians generate the candidates, and the two angles they rarely produce (null and deceptive) are added in the narrowing step: null unless something demonstrably needs explaining, deceptive when trust, security, or manipulable signals are involved.
  - **Lost:** standalone ACH for non-causal questions (forecasting, attribution among actors). To approximate it, frame the competing explanations as candidates for `/think-diagnose`.

### Fixed

- **A correctness pass over all 22 skills**, run after the consolidation. Four independent reviewers made about 85 findings, and every one was checked against the file before it was fixed. The ones with behavioral consequences:
  - **`/test-mutation` could delete your untracked files.** Its rollback now deletes only files created since the implementer was spawned.
  - **`/test-mutation` and a red suite.** A failing baseline now stops the run instead of marking every module blocked.
  - **`/test-mutation` and a gitignored tracking file.** It no longer fails to commit when the tracking file is gitignored.
  - **`/release` preflight blocked every release.** The preflight ran before the version bump, so manifests still at the old version looked like errors. `/release`, `/review-release`, and `qa-release-engineer` now agree that a pending bump is INFO.
  - **`/bug-fix` called by another skill.** It gains an "Invoked by Another Skill" contract, so `/implement` running it no longer closes tickets or rebases.
  - **`/implement` running `/bug-hunt`.** `/implement` now answers `/bug-hunt`'s up-front intent questions itself.
  - **`/bug-hunt`'s floor.** It is consistently "at or above the floor".
  - **`/review-repo` and `/review-release`.** `/review-repo` runs `/review-release` report-only, so it truly never changes code. Its ticket floor is mapped onto every scale its follow-up reviews produce.
  - **Findings that were being dropped:**
    - non-security bugs that the security agents find;
    - `qa-test-reviewer`'s Other category;
    - the perf reviewer's hot-path and over-provisioning evidence;
    - the architecture reviewer's behavior-altering changes.
  - **`/scope` reviewers.** The perf, architecture, and value agents gain a spec-time mode for reviewing draft tickets, which `/scope` was already asking them to do.
  - **`/think-premortem`** now passes the time horizon and system context its agent requires.
  - **`/think-diagnose`'s narrowing trigger** is stated one way everywhere.
  - **`/tidy-git`.**
    - It finds squash-merged branches whose upstream is gone (a new "upstream gone" category).
    - It checks for an in-progress rebase or merge before acting.
    - It excludes branches checked out in other worktrees.
  - **`/tidy-docs`** now dispatches `doc-maintainer`'s full-audit mode.
- **Every agent was checked against its callers.** Each of the 37 agents was traced to every skill that dispatches it. Agents now accept the inputs their callers send, use the exact mode names callers invoke, and emit the output sections callers read. None is orphaned. Notable fixes:
  - `swe-implementer`'s modes match each caller's wording.
  - `swe-arch-reviewer` accepts the dead-code audit and the hidden-coupling pairs `/review-repo` passes it.
  - `sec-red-teamer` reports exploitability and chain dependencies for each finding.
  - `swe-correctness-reviewer` knows `/refactor`'s lost-guarantee rule.
  - `swe-refactor-dx` drops the multi-round machinery that contradicted `/refactor`'s single finishing pass.
  - `qa-test-mutator` reports partial coverage explicitly.
  - The namespace readers' contract fits the optional batteries.
  - The `qa-*` test reviewers' modes use their callers' names.
  - `thk-reflector`'s decision grid no longer contradicts itself.
  - On the skill side, the dispatches are explicit:
    - the reviewers that `/bug-fix` and `/implement` spawn now name their mode;
    - `/bug-fix` passes the diagnostician's related failure modes to QA as acceptance criteria;
    - the namespace focus asks readers for the confidence its severity rules depend on.
- **Trimmed.**
  - `/review-security` went from 701 lines to 435, `/review-test` from 643 to 433, and `/bug-fix` from 412 to 315.
  - The example sessions in `/test-mutation` and `/release` that repeated their steps are cut.
  - The `/think-premortem` README went from 618 lines to 387.
  - `/pre-compact` is condensed by about 40 lines with no change in behavior.
  - Every SKILL.md is now within the house 500-line limit.

### Changed

- **`make lint` and CI.**
  - **What it checks:** `scripts/lint.py` (standard library only) checks skill and agent frontmatter, description length, the 500-line limit, markdown table alignment, that every agent and skill a doc cites exists, and that no agent is orphaned.
  - **Where it runs:** `.gitea/workflows/lint.yml` runs it on every push to master and on every pull request.
  - **Why:** every check it runs was done by hand repeatedly during the v12 consolidation, and the two reference checks still caught stale `/review-*` references that had survived several review passes.
- **Explicit mode contracts for agents.** The 12 agents that have modes declare them in frontmatter (`modes: [...]`), and `make lint` checks both sides of the contract.
  - **Callers:** every mode a skill invokes, as a `Mode: X` line in a dispatch prompt or as "`agent` in X mode" prose, must be a mode the agent declares.
  - **Agents:** every declared mode must appear in the agent's own body.

  Mismatched mode names were the most common defect in the v12 agent-fit pass, and they are now caught mechanically. The check covers 25 mode references. `swe-perf-reviewer`'s "Spec-time review" is renamed "Spec-time" to match what callers say.
- **Each skill's `references/README.md` is now a guide, not a second copy of the procedure.** The 22 guides drop from about 5,800 lines to about 2,300. They keep:
  - the rationale and lineage;
  - when to use and not to use the skill;
  - what it asks and returns;
  - worked examples;
  - at most one diagram at phase level.

  They link to `SKILL.md` for the steps. A procedure change no longer needs a matching README edit, which removes the sync gap that kept producing drift.
- **Shorter descriptions.** Skill and agent descriptions now run one or two sentences and at most 250 characters (the linter allows 300). The total across all of them drops from about 20,500 to 12,000 characters, all of which load into every session's context. Trigger words and selection-critical qualifiers are kept: focus names, "Never changes code", "blocking", "read-only", "used only by /refactor".

- **The remaining agents are realigned with the skills that call them.** In v10 and v11 the skills were redesigned while many of their agents kept the old contracts, and most real defects sat in that gap. Agent names are internal, so none of these changes is breaking.
  - **`swe-code-reviewer` is now a scope auditor.** `/implement` had used it for the concept-inventory audit, but the agent never mentioned an inventory: it searched the whole codebase for refactoring ideas. It now checks a diff against its license, which is the inventory in `/implement` and the diagnosis's narrow fix in `/bug-fix`. It reports unlicensed concepts, elaborated forms, duplicated mechanisms (citing the search that found the original), and exports with no outside caller. Step 6b of `/bug-fix` uses it that way.
  - **`qa-engineer` is independent of what it verifies.** It no longer fixes product code or adds test infrastructure; failures go back to the implementer. It drives MCP servers over JSON-RPC itself, because a subagent cannot spawn one. It uses browser tooling when available, and UNVERIFIED is now a valid result. It runs on Opus.
  - **`/test-mutation` no longer reports false kills.** Before mutating, the mutator checks that the file is clean and that a timed baseline run passes. Its timeout is now a multiple of the baseline instead of a fixed 60 seconds. Likely-equivalent mutants are flagged rather than sent to the implementer as tasks it can't complete. Failed new test files are deleted, not just restored.
  - **`swe-planner` is removed.** `/implement` writes its own plan as ordered, verifiable sub-tasks over the inventoried concepts.
  - **Rewritten:**
    - `swe-perf-reviewer` is built on proportionality ("what is n?" at actual scale). It runs the project's existing benchmarks when they exist and labels static estimates as such.
    - `swe-web-perf-reviewer` judges by application context, without fixed byte thresholds or HTTP/1-era advice.
    - `qa-web-a11y-reviewer` covers the criteria new in WCAG 2.2, with corrected legal claims.
    - `doc-maintainer` searches for every doc that describes a changed file or symbol, not just docs near the diff, and has explicit targeted, full-audit and assessment-only modes.
    - `sec-blue-teamer` gains a spec-time mode for `/scope`.
  - **Contract fixes:**
    - The blue and red teamers drop their dead modes and share one four-level severity scale matching `/review-security`.
    - `swe-arch-reviewer` defers dead code to `swe-dead-code-auditor`.
    - `qa-test-reviewer` defers missing coverage to `qa-test-coverage-reviewer`.
    - `qa-test-fuzz-reviewer` produces candidates even when there is no fuzz tooling, and emits the LOW tier `/review-test` expects.
    - `swe-bug-assessor` treats change history as a primary signal, matching `/review-repo`'s map.
    - `thk-advocate` has explicit compete and defend modes.
    - `thk-premortemer`'s general method applies to every lens, not just `first-principles`.
    - `ux-reviewer` no longer tries to pause and ask mid-run.
  - **Overfitting and staleness:**
    - A user-specific `~/Source/lang` path is removed from nine agents.
    - Stale tool advice is corrected: `ts-prune` is now `knip`, `jsfuzz` is now Jazzer.js, `yarn audit` is now `yarn npm audit`, and `safety` is now `pip-audit`.
    - `qa-release-engineer` no longer treats `console.warn` or a bare `=======` as blockers, and copyleft dependencies are a warning for human review.
    - The repeated boilerplate tails in the `thk-*` agents are trimmed.

- **The ten `swe-sme-*` agents are replaced by a single `swe-implementer`.** The SMEs (Ansible, CSS, Docker, Go, GraphQL, HTML, JavaScript, Makefile, TypeScript, Zig) mostly restated best practice the model already knows. Some taught stale APIs: Zig's pre-0.15 build API, golangci-lint v1 config, Apollo v2/v3 imports, and long-outdated Docker base-image tags. The Makefile agent contained technical errors. The Go and Zig agents imposed one maintainer's conventions on every project they touched, such as always vendoring, docopt, and adding a Makefile when none existed. Delegating to them also moved implementation from the caller's model down to Sonnet. The new agent is language-agnostic and targets the ways implementation agents actually fail. It grounds APIs in the installed toolchain version, reading the module cache, `node_modules` types, or std-library source rather than recalling them. It follows the project's conventions and adds no tooling unasked. It builds only the concepts its brief calls for. It reports nothing as done that it has not run. Its modes cover every former SME use: implement, reproduce a bug, kill mutants, peer review, and cold-read tickets. `/implement`, `/bug-fix`, `/test-mutation`, and `/scope` dispatch it in place of the per-language table, and `references/swe-sme-pattern.md` is removed. Agent names are internal, so this is not a breaking change.

- **`/review-repo`'s map (formerly `/review-health`) locates technical debt by the interest it charges.** A snapshot shows cruft, not debt: ugly code nobody changes costs nothing. The Observe phase gains change-cost signals — per-file complexity (`scc`, `lizard`, or line count) crossed with 12-month change frequency into a ranked hotspot list, change-coupled file pairs with or without a static dependency between them, fix density in hotspots, and a history-adequacy check. A new Orient step reads them as a quadrant (debt being paid / dormant cruft / active / settled): hotspots are called debt only when fix density or cross-cutting findings corroborate them, hidden coupling routes to the `architecture` focus, and confirmed hotspots become scoped `/refactor` recommendations. `/refactor` and `/implement` are recommended, never run, so the skill still never changes code. Drawn from Tornhill's behavioral code analysis.

## v11.0.0

### Removed

- **BREAKING: `/implement-batch`, `/implement-project`, `/lead-project`, and `/scope-project` are folded into `/implement` and `/scope`; `/lead-bug-hunt` into `/bug-hunt`; `/lead-review` into `/review-health`.** The `/lead-*` namespace is gone: autonomy is now something you grant a skill in its commander's intent, not a separate tier of skills. `references/lead-startup.md` is removed with it. The implementation and planning skills were layered like nested `for` loops — `/lead-project` → `/implement-project` → `/implement-batch` → `/implement`, and `/scope-project` beside `/scope` — because earlier models needed each loop body spelled out to stay correct. That structure is now ceremony. `/implement` takes one ticket, a batch, or an open-ended goal; `/scope` produces one ticket or a project's worth (see Changed). The `/scope` → `/implement` pair remains the planning-to-execution path at every scale. Multi-ticket runs keep their state in `PROJECT_STATE.md`.

- **BREAKING: `/lead-refactor` is retired.** It was built around two passes of the old tactical `/refactor`, with an architectural `/review-arch` + `/implement-batch` loop between them. The redesigned `/refactor` does design-level work itself (blind regeneration dissolves parallel machinery and invented requirements), so the orchestrator no longer earned its keep. Run `/refactor` directly, or chain `/review-arch` → `/implement` by hand when you want the architectural loop. References are removed from the README, `CLAUDE.md`, `references/autonomy.md`, and the skills that listed it.

### New Skills

- **`/review-namespace` — empirical namespace-legibility review.** Converts "easy to reason about" from a feeling into a measurement: cold reader agents receive only the file listing — pasted inline, no tools, no repository path — and answer navigation questions ("which file would you open first for task X?") scored against ground truth the skill pins in the actual code before grading anyone. Fresh eyes are a renewable resource, so the user study that human teams can't afford runs on demand; and because probes need only a *listing*, hypothetical restructures are testable at full fidelity — taxonomy search becomes offline, testing dozens of restructures to perform one.

  Two modes. **Audit** (default): one battery against the actual tree, findings classified by severity (deceptive locations — unanimous confident misses; placement problems — universal mispredictions, where the remedy is moving code, not renaming it; attractor traps; homonym taxes; one-hop conventions), ticket proposal per the advisory pattern. **Search** (explicit opt-in, heavy — millions of tokens): an evolutionary loop — blind probe-bank generation from purpose docs, noise-floor calibration, candidate trees each carrying an old→new mapping, a feasibility gate that resolves technical-boundary conflicts by proposing reachability specs over the import graph ("trees are for humans, specs are for machines") rather than bending the tree back toward runtime contracts, per-question paired selection, mutation from reader rationales, and owner-calibration checkpoints where the maintainer's vetoes outrank every score.

  The design is derived from a five-round field pilot: probe scores discriminated a deliberately degraded tree, converged an ontology-organized champion from 83% to 95% cold-reader navigation accuracy across both conventional and style-primed reader pools, and the style-primed pool converged to reproducing the maintainer's own misses — validating it as an owner proxy. The pilot's nine operating rules ("Laws of the Instrument": pre-registered scoring, sighted ground-truth pinning, noise floors before comparisons, per-question pairing over saturating aggregates, attractor re-probing after every rename, universal-miss-means-move, the haiku canary) are encoded in the skill verbatim. `/review-health`'s follow-up never runs search mode: its calibration checkpoints require the operator.

- **`/review-dead` — focused dead-code audit.** The cheap way to get *just* a dead-code audit: `/review-arch` also catalogs dead code, but only as step one of a full architectural blueprint, and `/refactor` finds-and-removes rather than reporting. `/review-dead` audits without mutating — unreferenced symbols, dead files, unreachable branches, unused imports and manifest dependencies, commented-out blocks, tests-only code (source whose only references are its own tests), and dead configuration.

  The discipline is calibration, because a false dead-code finding costs more than a missed one. The auditor surveys the codebase's dynamic-dispatch patterns *first* (reflection, string-built names, registries, convention-based loading — the classic ways "no references found" lies), determines the reference roots (an application's entry points vs. a library's exported public API, which is never dead merely for being uncalled in-repo), then tiers every finding PROVEN / LIKELY / UNVERIFIABLE with cited evidence. Language tooling (`deadcode`/`staticcheck`, `knip`, `vulture`, `luacheck`) is leveraged when present, never installed. UNVERIFIABLE findings route to verification tickets, never removal tickets; intentionally-retained code (lint suppressions, ADR-protected) is reported separately, not proposed for removal.

  **`/review-health`'s follow-up runs it before `/review-arch`**, rather than relying on `/review-arch`'s incidental Step-1 dead-code catalog — the follow-up composes the dedicated skill, and `/review-arch`'s later re-findings are treated as confirmations and deduped in the consolidated report. The auto-approval contract in `references/autonomy.md` gains `/review-dead`; `advisory-tickets.md` adds it to the family.

### New Agents

- **`swe-namespace-reader` / `swe-namespace-canary` — cold readers for legibility probes.** Two minimal internal agents (sonnet and haiku respectively) encoding the cold-reading contract: no tools, no repository access, answer only from the inline listing, commit to one path per question, never meta-reason about the experiment — a wrong guess is a finding about the tree, not the reader. The canary is the sensitivity instrument: field trials showed the smaller model degrades first on vague names and scores highest on genuinely legible trees, so its movement is weighted in tree comparisons. Both accept an optional conventions preamble, which is how the style-primed (owner-proxy) pool is constructed from the same agents.

- **`swe-refactor-deleter` / `swe-refactor-minimizer` / `swe-refactor-dx` — the redesigned `/refactor`'s three workers.** Internal agents. The deleter (fable) is a deletion-stance hunter whose only remedy is removal: it runs the classic optimizer passes (dead-code elimination, copy propagation, inlining, constant folding, common-subexpression elimination, branch simplification) as mechanical detectors and files strip proposals, each adjudicated downstream by the gates rather than argued. The minimizer (opus) is a blind whole-target designer: it receives the pinned behavior, the surviving requirements, and the incumbent's size as numbers — never its source, tests, or design — and builds the minimum machine, concept inventory first. The DX reviewer (opus) is the reader advocate for the single finishing pass: a think-aloud newcomer read plus a seven-concern comprehension spine, with local edits only.

- **`swe-dead-code-auditor` — focused dead-code auditor.** Internal agent (opus) backing `/review-dead`. Runs the calibration sequence (dynamic-dispatch survey → roots determination → tooling pass → agent analysis for the categories tools miss), carries the confidence-tier and evidence-citation disciplines, and checks `adr/` before assuming absence of intent. Advisory only; honest zero is a valid result.

### Changed

- **BREAKING: `/implement` implements anything from one ticket to a project, by judgment over a fixed floor.** It used to be a twelve-step checklist for one ticket, wrapped by batch and project orchestrators. It now takes one ticket, a batch, or an open-ended goal it scopes first, and holds a repertoire it chooses from as the work warrants: `swe-planner`, the language SMEs, `sec-blue-teamer`, `swe-perf-reviewer`, SME peer review, `doc-maintainer`/`/tidy-docs`, `/refactor`, the `/review-*` skills, `/bug-hunt`, `/bug-fix`, a smoke-test procedure, `/review-release`, and the `/think-*` skills. Five things hold on every run because they are cheap and carry the correctness. The first is a **concept inventory** before code: every concept cites the requirement that forces it, the naive form is the default, existing mechanisms are searched for before anything is built, and no symbol is exported without a caller. A `swe-code-reviewer` audit of the diff against the inventory is resolved, not advisory. The other four: practical verification of the acceptance criteria before trusting tests; tests and linters green at every commit and merge; an independent `swe-correctness-reviewer` pass (run unless trivial, mandatory when the feature can't be run or there are no tests; findings blocking, up to three fresh rounds); and no irreversible actions. The final report names every pass that ran and gives a reason for each plausible one that didn't.

  The skill asks what only the user can answer, presents its understanding and plan once, scaled to the work, and then runs to completion. Multi-ticket work runs on a project branch with one topic branch per ticket. When `/refactor` is warranted, it runs unattended with its requirements menu answered from the approved intent. The stakes questions are asked up front; the smoke procedure and acceptance criteria become its probes; ticket-specified behavior and constraints are ratified, documented requirements kept, invented ones presumed dead, and no trades taken. The refactor branch is merged when its oracle is green. Tickets are referenced in commits (`Fixes #N`) and never closed by the skill, so they close when the user merges.

- **BREAKING: `/scope` scopes anything from one ticket to a project, by judgment.** It decides how many tickets the work needs and which reviewers the drafts need: an implementer cold-read (the language SME), `ux-reviewer`, `sec-blue-teamer`, `swe-perf-reviewer`, `swe-arch-reviewer`, `swe-value-engineer`. This replaces `/scope-project`'s fixed sequence of mandatory and discretionary loops. Two rules are fixed: drafts go upstream only after review converges — fresh-context reviewers re-run until a round finds nothing material, with a lens still objecting after three rounds escalated to the user — and nothing is created without the user's approval. A lens's sign-off becomes a constraint later reviewers may challenge but not silently trade away. Ticket sets carry explicit dependencies and an execution order instead of batch labels.

- **BREAKING: `/refactor` is replaced by a redesign workflow.** The tactical cleanup loop (DRY, dead code, naming, complexity, with Low / High / Maximum aggression ceilings) is gone. It was structurally incapable of radical simplification: its agents read the existing code first, so the existing shape anchored every proposal and the loop produced well-groomed versions of over-built designs. The new `/refactor` treats reduction as the goal and runs the five-step design algorithm as its spine, in order: question the requirements, delete the part, simplify what survives, accelerate the cycle, automate last.

  The run isolates itself on a fresh `refactor/<slug>` branch and never touches the operator's tree; merging is the operator's call. There is one interactive step, near the start: a requirements menu that opens with two stakes questions and returns a verdict per requirement (ratified, documented, invented, or priced as a trade). Everything the operator kills takes its machinery with it. Behavior is then pinned by a **differential oracle** — the original implementation, run live and diffed at the user-visible boundary — not by the existing test suite, so tests pinned to the old internals retire with them. Each iteration recounts the machine, then interleaves two moves: **strip** (`swe-refactor-deleter` removes everything the gates permit) and **regenerate** (a fresh, blind `swe-refactor-minimizer` builds the minimum machine for the surviving requirements). A strip that breaks pinned behavior is repaired by restoring the part or rebuilding a smaller one, whichever measures less. Adoption is mechanical: a candidate that passes three gates (behavior, correctness via `swe-correctness-reviewer`, structure with a density check that catches golf) and shrank the machine is adopted, and nothing is argued. The run finishes with one `swe-refactor-dx` pass for human readers, converts the oracle into a standing conformance suite, and reports the per-iteration series, the requirement verdicts, a trade menu, and a side memo of bugs found but not touched.

  Breaking because every part of the old contract changed: there are no aggression ceilings, the run is not in-place, and it has an operator checkpoint.

- **BREAKING: `/bug-hunt` takes commander's intent and can act on it; `/lead-bug-hunt` is folded in.** The skill asks once for scope, a severity floor, constraints, and two grants of authority: create tickets, and fix. It then hunts in rounds until one confirms nothing above the floor. Each round follows confirmed bugs to their siblings and widens to the next risk tier; with fix authority it also re-hunts the code its fixes changed. Hard cap: 10 rounds. Hunters still never fix. With fix authority, confirmed findings go to `/implement` under its "Invoked by Another Skill" contract, so every fix passes `/implement`'s floor, with the reproducing test as the acceptance criterion. With ticket authority, tickets are created without asking again; without it, nothing changes outside the report and a ticket set is proposed for approval, as before. Reproducing tests for bugs not fixed in the run are now committed marked as expected failures, referencing their ticket, so the suite stays green for `/implement`. Hunters must now assert at the boundary a caller sees, not against internals, since their tests become fixes' acceptance criteria. That replaces `/lead-bug-hunt`'s mandatory end-of-run `/review-test` pass, which is now a judgment call. Contested findings and fixes that would need a breaking change go to the user.

- **`/review-health` can run the reviews it recommends.** Its preflight now asks for two grants alongside the lens: running follow-up reviews, and creating tickets at or above a severity floor. Both default to no, and without them the skill is the same cheap orientation pass. With follow-up authority, a new Phase 5 runs the specialist reviews the map calls for (`/review-dead`, `/review-arch`, `/review-security`, `/review-perf`, `/review-a11y`, `/review-test`, `/review-release`), each scoped to where its findings point and ordered so earlier reviews inform later ones. A specialist that plausibly applied but wasn't run gets a one-line reason. Phase 5 then dedupes the findings across reviews and reconciles them with the map; tickets are created with ticket authority, or proposed as one consolidated set for approval without it. This replaces `/lead-review`'s fixed eight-phase pipeline: the map, not a list, decides which reviews are worth their cost. The skill still never changes code.

- **`/review-health`'s follow-up runs `/review-value` only when intent asks.** Its output is a menu of product decisions the operator must rule on, so it is never run by default.

- **`ux-reviewer` now serves `/scope`.** Its description and framing were retargeted from the removed `/scope-project`.

- **`.gitignore` ignores `PROJECT_STATE.md` instead of `PROJECT_PROGRESS.md`,** matching `/implement`'s multi-ticket state file.

- **BREAKING: `/review-requirements` renamed to `/review-value`.** One release after shipping — the cheapest moment a skill rename will ever have. The new name is truer to what the skill audits: value-for-cost, which exists in every codebase, where "requirements" faintly promised a document artifact most projects don't have (the skill's provenance-tier discovery exists precisely because requirements must be excavated, not read). It also aligns with the value-engineering discipline the skill explicitly practices and with its backing `swe-value-engineer` agent. The discoverability cost of the more opaque name is carried by the README capability table and skill description. Per the "skills are user-facing" contract, the rename is a breaking change and gates the next release to a MAJOR bump. Historical changelog entries below retain the original name.

## v10.5.0

### New Skills

- **`/review-requirements` — value-engineering review.** The pipeline's first descoping voice, filling a structural gap: every other skill treats requirements as fixed input — the correctness gate enforces the spec, `/refactor` preserves behavior by definition, and `/review-arch`'s mechanism audit stops at "keep — serves requirement X" and salutes. After scoping ends, requirements only accrete; no skill was permitted to ask whether a requirement is worth what it costs. The skill applies value engineering (Miles, GE, 1947) — attribute cost to function, ask what else would serve — and presents a **trade menu**: each entry names the current commitment, a proposed relaxation, a *concrete* user-visible delta a product owner can rule on, the machinery (or requirement chain) that dissolves, and estimated savings presented as estimates with citations.

  Requirements are **discovered, not assumed** — not every project has a design document, and documents drift. The analysis agent inventories them across three provenance tiers: documented (design docs, ADRs, README promises), pinned (test-suite assertions), and inferred (observed behavior nothing records, presumed intentional per Chesterton's fence). The tier shapes the trade: renegotiate the document, amend the spec, or simply confirm the behavior was ever wanted. Documented-vs-observed drift is itself reported. Approved trades produce tickets whose *first* acceptance criterion amends the requirement's record — otherwise the next agent to read the unamended requirement faithfully rebuilds the machinery.

  The skill is advisory in a stronger sense than its siblings: its findings are product decisions, so it is **excluded from `/lead-review`'s autonomous pipeline**, and orchestrators treat core-requirement/correctness/security-flagged trades as andon-cord material. It chains ahead of `/review-arch` and `/refactor` — deleting a requirement before polishing its implementation.

### New Agents

- **`swe-value-engineer` — value-engineering analyst.** Internal agent (opus) backing `/review-requirements`. Works cost attribution from both ends: requirement-down (what exists to satisfy each commitment) and mass-up (what requirement forces each heavy artifact — anything forced by *none* routes to `/review-arch`'s mechanism audit rather than being priced here). Hunts requirement chains especially — the most expensive requirements are rarely expensive directly, but force a design choice that forces a compensating mechanism that forces defenses of the compensation; the chain is priced back to its root commitment. Catalogs the recurring hiding places of requirement-shaped cost: edge-case absolutism, unshipped futures, uniformity commitments, precision beyond perception, generality beyond use. Consumes `/review-arch` mechanism-audit output as pre-computed attribution when available. Discipline mirrors the plugin's other analysts: estimates presented as estimates, concrete scenario-shaped deltas only, core/correctness/security trades flagged, honest zero valid.

### Changed

- **`/review-arch` — the Proportionality Rule and mechanism audit.** The plugin's pipeline is a complexity ratchet: agents pattern-match to solutions from codebases at scales the project will never reach, and adversarial review rewards machinery that pre-empts hypothetical objections — an implementation with a termination proof survives review more easily than a plain loop, even when the plain loop is sufficient. No discipline anywhere in the plugin caught *used-but-unnecessary* machinery; Step 1's prune only caught dead code. Observed in the field: a binary min-heap scheduling 255 bots at 30 Hz whose own header comment measured the entire scheduling path at 0.47 µs against a 33,333 µs tick budget — machinery justified by a measurement that refutes it.

  `swe-arch-reviewer` gains a top-level Proportionality Rule: every mechanism (custom data structure, cache, pool, ring, event indirection, scheduling scheme, abstraction layer) must cite the requirement it serves and survive comparison against the simplest implementation meeting the same acceptance criteria at actual scale. Step 1 gains the mechanism audit that operationalizes it — requirement served (a design-doc or ticket citation; "performance" without a number is not a requirement, and an unshipped future feature counts only if the design document commits to it), actual n and the simple alternative's cost at that n, and the simplest sufficient implementation — with a required output section rendering keep/downgrade verdicts. Two sharpened sub-rules: a negligible-cost measurement is evidence *for* downgrade, and "it works and is well-built" is not a defense — well-built machinery no requirement demands is dead code one step removed. SKILL.md and references/README.md are synced.

- **`swe-correctness-reviewer` — proportionality counterweight.** The generative half of the same fix: the correctness gate now states explicitly that a finding must cite a concrete failure at the diff's actual scale and inputs — hypothetical-scale objections must name the N, show it reachable, and show the failure — and that a diff replacing machinery with something simpler is not suspect for being simpler. Implementers should never need to armor code with speculative rigor to survive the gate; disproportionate machinery the reviewer notices routes to `/review-arch`'s mechanism audit as an out-of-scope observation rather than padding findings.

## v10.4.0

### Changed

- **`/review-arch` — the auditability ceiling becomes an enforced rule in the module audit.** The `swe-arch-reviewer` agent has long stated the principle that humans cannot audit large files ("You can reason about a 500-line file with ease. A human cannot.") but carried it only as preamble philosophy — nothing in the workflow collected line counts, and a large module could earn a "no change" verdict on the strength of a persuasive cohesion story. Observed in the field: a plugin-built project shipped a 3,702-line module that sailed through architectural review on exactly that failure mode.

  The principle is now a top-level rule with mechanical teeth. A source file exceeding the auditability ceiling (default 500 lines; caller-adjustable) may not receive a "no change" verdict — its only available verdicts are "split files" or a written cohesion exception stating what shared state or invariants a split would shatter and why no facet boundary avoids the damage. The burden of proof sits with the exception, because in a cohesive module everything is related, so "the pieces are related" can never suffice. Mechanically: the survey step now collects `wc -l` for every source file, and every module-audit entry carries a required `lines:` field, so the audit cannot satisfy the rule by philosophy alone.

  The rationale is encoded beside the rule: a human is always the maintainer of last resort, and an agent-driven project whose output its owner cannot audit is asking for trust it hasn't earned — human auditability is an engineering requirement, not a style preference. Only the ceiling's numeric value is taste, which is why it is a parameter. `/review-arch`'s SKILL.md gains the ceiling as a pass-through parameter (step 1 and the agent prompt template), and the skill's references/README.md is synced in the same change.

## v10.3.0

### Changed

- **`/bug-fix` — gains the correctness review gate as new step 10** (closes #20), completing the rollout begun in v10.2.0 when `/implement` gained the equivalent step 9. The gate slots between coverage QA and documentation, renumbering downstream steps 10–12 → 11–13. The pattern is `/implement`'s, instantiated with three bug-fix-specific contracts: the reviewer receives the **original bug report** (user-supplied symptom — ground truth that explains what the diff is for) but **not the step-3 diagnosis report** — the diagnosis is the implementing SME's adopted theory of the bug, and passing it would anchor the reviewer to the frame that produced the fix; the convergence loop's mechanical re-verification names the **step-2 reproducing test explicitly** (it is the workflow's contract artifact and must still pass after correctness fixes); and the degraded-verification override notes that in a repo with no test infrastructure, the reproduction contract itself collapses — making the gate the only correctness check between the fix and production, which is precisely the environment class (the zero-test legacy remediation) that motivated the gate's design.

  Run-unless conditionality matches `/implement` (skip only typo-class diffs; when in doubt, run), as do the 3-round convergence cap and escalation semantics. The overall agent-spawn safety limit rises 12 → 16 — one above `/implement`'s 15 because `/bug-fix`'s worst-case once-through pipeline spawns one more agent (the step-3 investigator: 12 agents vs 11), leaving both skills the same four-spawn headroom for convergence-loop rounds. The previous caps (10 for `/implement`, 12 for `/bug-fix`) predate the gate and carried inconsistent margins; the new caps are derived from pipeline size, not from the old caps. The references/README.md is synced in the same change — including correcting the "Identical to `/implement` steps 5-11" claim and step mapping table, both stale since v10.2.0's renumbering. `swe-correctness-reviewer`'s Team Coordination section now documents all three callers (`/implement` step 9, `/bug-fix` step 10, `/review-code` standalone) and the bug-report-in / diagnosis-out context contract.

## v10.2.0

### New Skills

- **`/review-code` — adversarial correctness review of a diff.** The user-facing wrapper around `swe-correctness-reviewer`, filling a catalog gap: every other `/review-*` skill audits the whole repository; none reviewed a *change*. The skill resolves the diff under review (explicit commit range, branch, PR number, or "uncommitted"; otherwise inferred from git state — dirty tree → working-tree changes, feature branch → merge-base..HEAD, main → last commit — and confirmed with the operator), dispatches a single fresh-context reviewer pass, and relays the evidence-cited report verbatim: assumption ledger, findings, residual risks, coverage notes, verdict.

  The skill is advisory per the `/review-*` namespace contract — in standalone use the agent's "blocking" classification translates to severity, not authority, and there is no convergence loop (that belongs to `/implement` step 9, where an implementation agent exists to resolve findings; standalone, the operator owns resolution and re-invokes for a fresh pass after fixing). It joins the `references/advisory-tickets.md` family with its own shape catalog (per-finding tickets for small independent sets, per-cluster tickets for shared root causes, a verification ticket for residual risks, and an explicit no-proposal path for clean reviews) and per-ticket body schema (Finding / Why it's a bug / Evidence / Fix direction / Acceptance criteria).

  `/review-code` is structurally excluded from `/lead-review`'s pipeline — a repository audit has no diff under review — and `/lead-review`'s docs now say "every repo-scoped `/review-*` sub-skill" accordingly. Disambiguation from `/bug-hunt`: that skill is repo-wide, risk-ranked, and writes reproducing tests; `/review-code` is one diff, exhaustive, single-pass.

### New Agents

- **`swe-correctness-reviewer` — adversarial diff-scoped correctness review.** A new internal agent (opus) that fills a structural gap in the `/implement` pipeline: every existing gate was either empirical (run the feature in step 4, run the test suite in step 8) or quality-focused (clarity via `swe-code-reviewer`, security posture via `sec-blue-teamer`, idiom nits via SME peer review) — no agent was ever assigned the question "is this diff *correct*?" The gap was discovered in the field: on a legacy codebase with zero test coverage and no way to run the application locally, both empirical gates silently collapsed, and patches shipped with bugs (unverified import-path assumptions) that an external PR reviewer had to catch.

  The agent borrows two techniques from `/think-premortem`, minus the heavyweight multi-agent machinery. First, prospective hindsight as the review framing: not "does this look right?" but "this diff was merged and caused a production incident — the bug is in there; reconstruct it," which counters the rubber-stamping failure mode of confirmation-oriented review. Second, scenario-mode's evidence discipline: read before claiming, cite file:line, never assert a defect without verifying it against the actual code — paired with calibration honesty ("honest zero is a valid verdict") so the agent doesn't manufacture findings to look thorough.

  The review walks a fixed six-concern spine: (1) **assumptions** — every path, symbol, signature, and config key the diff references, mechanically verified against the repo and recorded in an assumption ledger with per-assumption verdicts; (2) **runtime semantics** — features used must exist in the *target* language/framework version (PHP 5.3, not "PHP"), verified against manifests and local language references rather than recall; (3) **call sites** — every caller of every changed function; (4) **data flow** — traced forward to consumers and backward to producers; (5) **error paths**; (6) **first-principles residual** — whatever is idiosyncratic about this diff that the taxonomy misses. Output classifies findings (blocking, with cited evidence) separately from residual risks (unverifiable-in-repo items, non-blocking, surfaced to a human). The agent receives the diff and the repo only — never the implementation conversation — so the implementing agent's rationalizations can't anchor the review.

### Changed

- **`/implement` — new step 9, the analytical correctness gate.** Runs after all mechanical/empirical gates (steps 4–8) and before documentation, on the reasoning that mechanical verification is cheap and analytical review is expensive — don't spend opus review rounds on code that fails its own test suite. Invocation is **run-unless** at the orchestrator's discretion: the default is to run, with skips reserved for trivial diffs (typo fixes, comment-only changes), plus a **degraded-verification override** that makes the step mandatory regardless of diff size when step 4's practical verification was impossible or the project has no meaningful test suite — exactly the conditions under which the rest of the pipeline silently stops checking correctness.

  Findings are blocking, not advisory: each must be fixed or refuted with cited evidence. Resolution runs as a convergence loop — findings → implementation agent resolves → tests/linters re-run → a *fresh* reviewer instance re-reviews the full diff — until a round reports zero findings, capped at 3 rounds before escalating to the user. This internalizes the converge-with-an-independent-reviewer protocol that previously required an external review tool. Downstream steps renumber 9–11 → 10–12, and the overall agent-spawn safety limit rises from 10 to 15 to accommodate the new gate and its loop rounds.

- **`/implement-batch` — adapts to the new gate.** The autonomous-override table gains a Step 9 row (follow normal logic, run-unless with the degraded-verification override) and renumbers the rest; convergence-cap exhaustion and reviewer-vs-implementer contested findings join the andon-cord triggers, cascading to the batch level per the existing protocol.

## v10.1.0

### New Skills

- **`/release` — Cut a project release.** A new standalone skill for executing the project's release procedure with safety guards appropriate to a high-blast-radius operation. The skill discovers the procedure from the project itself (Makefile target → RELEASING.md → CONTRIBUTING.md release section → CLAUDE.md → package.json scripts → packaging configs → CI workflow → git tag history) rather than dictating one, and offers durable capture (preferring an executable Makefile target over a prose RELEASING.md over a CLAUDE.md note) when no procedure is discoverable. Releases that happen often enough to warrant automation become discoverable on the next run.

  The skill always invokes `/review-release` as preflight — categorically, with no skip flag, no recently-run cache, no force-release override. The asymmetry is intentional: an irreversible action warrants friction proportional to its blast radius. If `/review-release` reports BLOCKERs, `/release` aborts with the suggestion to address them and re-run. WARNINGs are carried forward into the plan presentation so the operator has the full picture at the high-leverage decision point.

  Version-bump proposal reads CHANGELOG and scans conventional-commit markers since the last tag (`feat!:`, `BREAKING CHANGE:`, `feat:`, `fix:`) to propose a semver bump; the operator confirms or overrides. An idempotence check scans for partial prior-run artifacts (local tag, remote tag, GitHub release, registry publication) and offers resume / abort / new-version when found. The skill never undoes existing artifacts.

  Plan presentation is the design's center of gravity. Every step is annotated with a reversibility class — `reversible`, `reversible-locally`, `irreversible-on-publish`, `partially-reversible` — and the boundary between local and remote operations is rendered as a visible divider in the plan. Execution proceeds without intra-step prompts except at that one boundary, where the skill pauses for a final confirmation before any push or publish. Per-step prompts would be friction noise; the boundary pause corresponds to a real semantic transition (before: everything is `git reset`'able; after: anything pushed is in the wild). On failure mid-execution, the skill halts and reports partial state honestly — completed steps, the failed step with exact error, current state by location (local repo / remote / registry / GitHub), and concrete recovery options. No automatic rollback is attempted because recovery is judgment-laden and wrong rollback is worse than no rollback.

  `/release` is a leaf skill, not an orchestrator: it composes `/review-release` linearly and does not iterate or make dynamic decisions across multiple sub-skills. It sits alongside `/refactor` and `/pre-compact` as standalone supporting workflows that don't share a namespace, and pairs with `/review-release` across the act/check seam — `/review-release` is the advisory side, `/release` is the mutator side. Operators do not need to invoke `/review-release` manually before `/release`; the composition is internal.

### Infrastructure

- **README, `CLAUDE.md`, and skill listings updated** to surface `/release` in the namespace table (added to the standalone row alongside `/refactor` and `/pre-compact`), the "Choosing a Workflow" decision table, the Skills→Standalone section, and a new "Releases:" subsection in `CLAUDE.md`'s supporting-workflows listing.

## v10.0.0

### Breaking Changes

- **`/refactor-deep` renamed to `/lead-refactor` and redesigned as a loop-to-convergence orchestrator.** The previous `/refactor-deep` was a once-through pipeline — Phase 1 tactical `/refactor` followed by Phase 2 advisory `/review-arch` (with optional ticket creation) and a `/tidy-docs` wrap-up. The new `/lead-refactor` is a three-phase autonomous pipeline that earns the `/lead-*` namespace by actually orchestrating to convergence: Phase 1 invokes `/refactor` (which loops internally to tactical convergence), Phase 2 loops `/review-arch` + `/implement-batch` until architectural findings converge below an operator-set severity floor (bounded to 5 iterations), and Phase 3 invokes `/refactor` again to clean up tactical issues introduced by Phase 2's restructuring.

  The auto-approval contract from `/lead-bug-hunt` extends here: `/review-arch`'s ticket proposals are auto-approved per commander's intent rather than requiring per-iteration operator confirmation. The skill pulls the andon cord on contested findings, breaking-change requirements, repeated implementation failure, or Phase-2 hard-cap exhaustion.

  Four-field commander's intent (scope, severity floor, constraints, refactor aggression) replaces the previous six-field upfront-input schema. The `/tidy-docs` wrap-up step is dropped — out-of-axis for `/lead-refactor`'s outcome contract; operators run `/tidy-docs` separately if doc cleanup is wanted. State lives in gitignored `LEAD_REFACTOR_STATE.md` with a findings ledger and andon-cord history.

  This restores the Phase-3 final-refactor pass that was dropped when `/review-arch` became advisory in v8 — with `/implement-batch` now doing the architectural work, Phase 3 earns its keep again as a tactical cleanup over the restructured code.

  Operators with muscle memory for `/refactor-deep` should switch to `/lead-refactor`. No deprecation alias — clean break, consistent with how `/review-doc` → `/tidy-docs` was handled in v9.

- **`/review-deep` renamed to `/lead-review` and redesigned as an autonomous orchestrator-family variant.** The previous `/review-deep` was interactive throughout — the operator participated in each sub-skill's decision points. The new `/lead-review` is autonomous from startup to termination, joining the `/lead-*` orchestrator family alongside `/lead-project`, `/lead-bug-hunt`, and `/lead-refactor`. The shape is once-through over the `/review-*` sub-skills: `/review-health` → `/review-arch` → `/review-security` → `/review-perf` → `/review-a11y` (if applicable) → `/review-test` → `/review-release`. Each sub-skill's interactive ticket-proposal prompts are answered uniformly by the orchestrator per a startup choice.

  Four-field commander's intent (scope, ticket creation yes/no, severity floor if tickets ON, constraints). The ticket-creation toggle is the mode-defining field — `yes` enables backlog generation (auto-approve at/above floor, tracker writes), `no` enables audit-report mode (auto-decline uniformly, no tracker writes). This serves both "produce a comprehensive backlog" and "just tell me what's wrong" use cases from one workflow.

  Operator intent is sovereign: a CRITICAL finding in tickets-OFF mode is surfaced prominently in the completion report, not silently overridden into a ticket. The autonomy contract honors what was authorized at startup; no paternalistic exceptions.

  `/tidy-docs` is dropped from the pipeline. It was Phase 7 in `/review-deep` but is `/tidy-*` (mechanical mutations), not `/review-*` (advisory). Including it would muddy the contract — operators in tickets-OFF mode expect "evaluation only" and `/tidy-docs` would commit doc changes regardless. The `/tidy-docs` README's pairing guidance now reflects this; run `/tidy-docs` separately if doc cleanup is wanted.

  State doc: `LEAD_REVIEW_STATE.md` (gitignored), full findings ledger and andon-cord history. Andon protocol with skill-specific extensions (current phase, phases complete/remaining).

  Operators who relied on `/review-deep`'s interactive walkthrough now invoke individual `/review-*` skills directly — that's the same experience without the orchestration glue. The autonomy doc's "What this discipline does NOT do" exclusion for `/review-deep` is removed since `/lead-review` is in the family.

### Infrastructure

- **`references/autonomy.md` — `/lead-refactor` and `/lead-review` added to the orchestrator-family roster.** The opening paragraph's enumeration of skills governed by the autonomy discipline now includes both new members. New schema subsections under "Commander's-intent schemas per skill" document the four-field schemas for each: `/lead-refactor` (scope, severity floor, constraints, refactor aggression) and `/lead-review` (scope, ticket creation, severity floor, constraints). The `/review-deep` exclusion in "What this discipline does NOT do" is removed.

- **README, `CLAUDE.md`, and workflow listings updated** to surface `/lead-refactor` and `/lead-review` in the layered workflow diagrams, the "Choosing a Workflow" decision table, the orchestrator-family description, and the Skills→Orchestration section. The corresponding `/refactor-deep` and `/review-deep` references in cross-skill documentation (`skills/review-arch/`, `skills/review-security/`, `skills/review-test/`, `skills/lead-project/`, `skills/tidy-docs/`) are updated to point at the new skills, with the `/tidy-docs` ↔ `/lead-review` pairing guidance reflecting the `/tidy-docs` drop from the pipeline.

## v9.1.0

### New Skills

- **`/lead-bug-hunt` — Autonomous bug-elimination loop.** A new orchestrator-family skill that drives a codebase toward "no bugs above a stated severity floor" without operator involvement between startup and termination. The operator states scope, severity floor, constraints, and optional refactor-finisher aggression at startup; the skill then loops `/bug-hunt` → triage → `/implement-batch` until two consecutive hunt passes produce no findings above the floor, or until a hard cap (10 hunt-cycles) or andon cord halts the run. Auto-approves `/bug-hunt`'s ticket proposals (a contract shift authorized by commander's intent); reproducing tests committed by `/bug-hunt` serve as durable acceptance criteria. At termination, always runs `/review-test` scoped to the run's new reproducing tests — those tests become permanent regression artifacts and their quality is treated as core, not adjacent — and optionally runs `/refactor` as a finisher to clean up defensive code introduced by fixes.

  The skill is a narrower sibling of `/lead-project`. Where `/lead-project` takes open-ended commander's intent and decides which skills to invoke from a broad repertoire, `/lead-bug-hunt` has a fixed loop shape and a bounded sub-skill repertoire (`/bug-hunt`, `/implement-batch`, `/implement`, `/bug-fix`, `/think-diagnose`, `/refactor`, `/review-test`). Other `/review-*` skills, `/scope-project`, `/test-mutation`, `/tidy-docs`, and `/tidy-git` are explicitly out-of-axis — use `/lead-project` when bug-hunting is one of several concerns. The skill exists because "iterate `/bug-hunt` → fix tickets → re-hunt" was a recurring manual workflow worth canonizing.

  The four-field commander's intent omits `/lead-project`'s purpose, key tasks, end state, and non-goals because the work is fixed-shape: purpose is "eliminate bugs above the floor"; key task is convergence; end state is two consecutive empty passes; non-goals fall out of the bounded sub-skill list. The dominant judgment call the operator makes at startup is the severity floor — too low (e.g., "All severities") and the loop never converges because `/bug-hunt` finds Low-severity opportunities indefinitely; too high (e.g., "Critical only") and the run ships with known High-severity bugs deferred. Default is Critical+High.

  Triage is mechanical, not judgment-based, to forestall rationalization: findings at or above the floor enter the fix-list; findings below the floor go to deferred; findings the skill genuinely believes are wrong on substance pull the andon cord rather than getting silently dismissed. The "no escape hatches" discipline carries through — the skill cannot bargain findings down to make convergence easier.

  The optional `/refactor` finisher is opt-in (default off) because cleanup is adjacent to bug elimination; the `/review-test` step at termination is always-on (no opt-out) because the reproducing tests are this skill's unique durable output and treating their quality as adjacent would be inconsistent with the framing. No re-hunt runs after the finisher or test-review steps — that would risk an infinite loop (re-hunt → find → fix → re-review → re-hunt …). The test suite catches any regressions introduced by termination-phase changes.

  Andon-cord triggers extend `/lead-project`'s set with bug-specific shapes: contested findings (skill disagrees with `/bug-hunt` on substance), breaking-change requirements (per the autonomy-doc guardrail), regression introduced by a batch fix, stale reproducing test (test does not fail on current HEAD when triaged), hunt-with-high-uncertainty (assessment surfaced hotspots but hunters could not confirm findings), hard cap, sub-skill cord cascade, and resume-time HEAD divergence. State lives in `LEAD_BUG_HUNT_STATE.md` at the repo root (gitignored), with a findings ledger (fixed / deferred / contested / breaking-change-required), per-cycle log, and andon-cord history for resume across sessions.

### Infrastructure

- **`references/autonomy.md` — `/lead-bug-hunt` added to the orchestrator-family roster.** The opening paragraph's enumeration of skills governed by the autonomy discipline now includes `/lead-bug-hunt`. A new schema subsection under "Commander's-intent schemas per skill" documents the four-field schema (Scope, Severity floor, Constraints, Refactor finisher) and notes which canonical fields the skill drops and why (purpose, key tasks, end state, non-goals are implicit because the work is fixed-shape and the implicit values are stable across runs). This keeps the autonomy doc's stated invariant intact: every orchestrator-family skill that elicits its own schema has a corresponding entry.

- **README, `CLAUDE.md`, and workflow listings updated** to surface `/lead-bug-hunt` in the layered workflow diagrams, the "Choosing a Workflow" decision table, the Skills→Orchestration section, and the Bug-work supporting-workflows list.

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

- **`/refactor-deep` — adapts to advisory `/review-arch`; Phase 3 dropped.** The skill previously ran three phases: tactical refactor, advisory architectural review with optional ticket creation, then a re-run of tactical refactor over architectural restructuring. With `/review-arch` no longer implementing changes itself, the third phase has no architectural restructuring to clean up — it is removed. The v8.0.0 shape is Phase 1 (tactical `/refactor`) followed by Phase 2 (`/review-arch` in advisory mode, with the operator deciding what to do with the findings), then a wrap-up `/review-doc` pass. Phase 2 offers to cut tickets when warranted, which can then be fed to `/implement` or `/implement-project`. The ticket-creation preference is collected upfront alongside other Phase-1 inputs so the workflow runs without mid-run interruptions except the one ticket-review pause.

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

- **GitHub release automation removed.** `.github/workflows/release.yml` and the entire `.github/` directory have been deleted. Claude Code plugins are distributed by git ref — consumers pin to a tag or branch and the marketplace files in the repo are the actual distribution mechanism — so the GitHub Releases artifact carried no functional payload. Its presence was also actively confusing on the Gitea side: Gitea Actions scans `.github/workflows/` as a fallback and was queuing phantom jobs against a non-existent runner on every tag push. Existing GitHub releases (v1.0.0 through v7.0.0) were deleted out of band; tags are preserved on both Gitea and the GitHub mirror. `HACKING.md` updated to reflect the simplified procedure. *(`HACKING.md` has since been deleted; release procedure now lives in the `/release` skill.)*

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

- **`THINK.md` design discipline document.** Repo-root document that captures the design discipline for the `/think-*` skill family. Includes the **five-test admission gate** for new `/think-*` skills (specific failure mode, practitioner tradition, unskippable questions, NGT discipline, honest "didn't apply"), cross-cutting practices (steelmanning, observation/recollection split, process-vs-luck attribution, calibrated qualitative confidence, prospective hindsight), and intellectual lineage (Kahneman, Tetlock, Schön, Klein, Taleb, de Bono, Delbecq & Van de Ven, Peirce). New `/think-*` skills must clear the five tests; existing `/scope`, `/implement`, `/refactor`, etc. are admitted by different criteria. A "spillover" section notes which practices apply across the plugin. *(File has since been relocated to `references/think.md`.)*

- **`CLAUDE.md` updated** to reference `THINK.md` *(later relocated to `references/think.md`)* and require new `/think-*` skills to pass its admission gate.

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

- **Release automation moved from `Makefile` to a Claude-assisted procedure.** The top-level `Makefile` has been removed; release cutting is now driven by a procedure documented in `HACKING.md`. This is an internal workflow change — no effect on the public skill interface. *(`HACKING.md` has since been deleted; release procedure now lives in the `/release` skill.)*

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
