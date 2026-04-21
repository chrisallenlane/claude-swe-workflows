# Changelog

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
