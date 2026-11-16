---
name: review-security
description: White-box security audit. Independent blue-team and red-team passes are synthesized into targets for focused red-team deep dives, iterating on exploit chains. Heavy and thorough. Advisory only; proposes tickets, does not remediate.
model: opus
---

# Review Security — White-Box Security Audit

Orchestrates a comprehensive security assessment of the project's source code using both defensive and offensive analysis. A blue-teamer and a lead red-teamer run in parallel, in isolation — neither sees the other's output during the first pass. The orchestrator then synthesizes their territories into a unified target list with four prescriptive categories, surfacing what each team alone would have missed. Focused red-teamers deep-dive each target. Findings are synthesized, exploit chains are explored, and the process iterates until no new chains emerge.

**This is deliberately heavy.** Thoroughness is the priority, not speed. A complete audit may spawn many agents and take significant time. That's the point — shallow security reviews miss the vulnerabilities that matter.

**Advisory only.** The skill produces findings and proposes tickets; it does not implement remediation. The cognitive seam between "find vulnerability" and "fix vulnerability" is wide enough that mixing them under one workflow degrades both — security findings require fresh threat-model reasoning to remediate correctly, and the discovery agents shouldn't be biased toward findings they could easily fix. Tickets capture findings durably across that seam and compose with `/implement` for remediation.

## Workflow Overview

```
┌──────────────────────────────────────────────────────┐
│                   AUDIT WORKFLOW                     │
├──────────────────────────────────────────────────────┤
│  1. Determine scope                                  │
│  2. Independent first pass (parallel, isolated)      │
│     ├─ Blue-teamer (defense evaluation)              │
│     │   └─ Output: control inventory + gaps + depth  │
│     └─ Lead red-teamer (reconnaissance)              │
│         └─ Input: scope only (no blue-team output)   │
│         └─ Output: attack surface + target list      │
│  3. Reconnaissance synthesis                         │
│     ├─ Categorize: anchoring-suppressed,             │
│     │   convergent, blue-flagged-unverified,         │
│     │   divergent                                    │
│     └─ Output: unified target list (≤25)             │
│  4. For each target on unified list:                 │
│     └─ Spawn focused red-teamer (deep investigation) │
│        └─ Includes blue-team context iff target      │
│           origin includes blue-team data             │
│  5. Findings synthesis + chain analysis              │
│     ├─ If exploit chains found → goto 4 (new vector) │
│     └─ If no new chains → proceed                    │
│  6. Present consolidated findings to user            │
│  7. Cut tickets (proposal, operator-approved)        │
└──────────────────────────────────────────────────────┘
```

## Workflow Details

### 1. Determine Scope

**Default:** Production code only. The following are excluded by default:
- Test code (test files, test fixtures, test helpers)
- Dev-only dependencies and tooling (build tools, linters, bundler configs)
- Generated code, vendored code

Inform the user of these exclusions when presenting the scope. If the user wants to include any of them, respect that.

**If user specifies scope:** Respect it (directory, files, module, feature area). Pass scope to all spawned agents.

If the invocation or caller supplies scope, use it and skip the scope question. Otherwise, **ask the user:**
- "What is the scope of the audit?" (entire codebase, specific module, specific feature)
- "Is there anything you're particularly concerned about?" (auth, file handling, a recent change, etc.)
- "Are there any areas I should skip beyond the defaults?" (additional exclusions)

User concerns inform the prioritization of vectors in later steps, but the blue-teamer and lead red-teamer still perform full analysis — user intuition supplements, not replaces, systematic analysis.

### 2. Independent First Pass — Parallel and Isolated

**Spawn the blue-teamer and lead red-teamer in parallel.** Neither agent sees the other's output during this phase. This is the load-bearing discipline of the skill: a red team briefed by the blue team treats the blue team's defensive map as the salient territory. Real attackers get no defensive briefing; they look at the system fresh and find what defenders missed. Independent reconnaissance surfaces the territory each side alone would miss.

#### 2a. Blue-Teamer — Defense Evaluation

Spawn a `sec-blue-teamer` agent for full defense evaluation:

```
You are the blue-teamer for a white-box security audit. You are running in
parallel with the lead red-teamer; you will not see their output during
this phase. Perform your evaluation from defenders' first principles.

Mode: full review
Scope: [entire codebase | user-specified scope]
User concerns: [any areas of concern mentioned by user, or "none specified"]

Perform every step of your methodology. Pay special attention to
CONSISTENCY. Gaps where a control exists but isn't applied universally are
the highest-value defensive findings.

Output your full report in your standard format.
```

#### 2b. Lead Red-Teamer — Independent Reconnaissance

Spawn a `sec-red-teamer` agent in broad recon mode. **Do not pass any blue-team output.** The lead red-teamer in this phase performs reconnaissance with no defensive briefing — pure attacker perspective on the codebase.

```
You are the lead red-teamer for a white-box security audit. You are running
in parallel with the blue-teamer; you will not see their output during this
phase. Perform reconnaissance from attackers' first principles — fresh eyes
on the codebase, no defensive briefing.

Mode: broad recon
Scope: [entire codebase | user-specified scope]
User concerns: [any areas of concern mentioned by user, or "none specified"]

Perform phases 1–3 of your methodology. Do NOT perform deep exploitation
yet. Your job is to survey the landscape and produce a prioritized target
list.

Output a structured report:

## ATTACK SURFACE
[Entry points discovered, ranked by exposure]

## TRUST BOUNDARIES
[Trust boundaries identified, noting implicit/unguarded ones]

## TARGET LIST
For each promising attack vector, provide:
- Target: [entry point or code path]
- Files: [specific files and line ranges to focus on]
- Hypothesis: [what you think might be exploitable and why]
- Context: [relevant framework protections, validation observed, transformations]
- Priority: [CRITICAL / HIGH / MEDIUM / LOW]
- Investigation approach: [what the focused red-teamer should try]

## NON-SECURITY BUGS (if any)
[One line each: file:line — what's wrong]

Rank targets by a combination of exposure (how easy to reach) and potential
impact (how bad if exploited). Include up to 25 targets — but this is a
MAXIMUM, not a quota. Report only targets that genuinely warrant
investigation. A short list is fine. An empty list means the codebase is
well-defended — that is a positive outcome, not a failure. Do not
manufacture or inflate targets to fill slots.
```

**When both agents report back:** review the blue-team's defense evaluation and the red-team's target list. They are now inputs to step 3 (reconnaissance synthesis). Do not yet act on either independently.

### 3. Reconnaissance Synthesis

Pool the blue-team's defense evaluation and the red-team's target list. **The orchestrator (you) performs this synthesis directly — not via a sub-agent.** The categorization rules are mechanical, the orchestrator already holds both reports, and avoiding an extra agent saves cost and round-trip time.

Categorize each item from the combined material into one of four prescriptive buckets:

#### anchoring-suppressed (highest-value bucket)

Red team flagged this as a target, **but blue team did not account for it in their defensive map**. These are the gaps a briefed red team would have been anchored away from. The red team found them precisely because they had no defensive briefing.

Examples:
- File-upload path-traversal risk where the blue team's inventory listed "upload exists" but did not enumerate the path-construction sink
- Spreadsheet formula injection in CSV exports where the blue team did not enumerate spreadsheet sinks
- Verbose error responses exposing internals where the blue team's logging analysis didn't extend to error-response disclosure

These targets get **the highest priority** in the unified list. They are the discipline's payoff.

#### convergent

Both teams independently identified this territory as risky — red team listed it as a target, **and** blue team flagged a defensive gap covering it. High confidence; investigate.

Examples:
- OAuth state validation flagged by blue as "state generated but not validated" and by red as "state handling looks suspicious"
- Raw SQL queries flagged by blue as "3 queries bypass ORM" and by red as "string-built query"

Convergent targets are robust — both perspectives agreed independently. They merit deep investigation.

#### blue-flagged-unverified

Blue team called out a defensive gap, **but red team did not reach this area in independent recon**. Worth investigating to confirm exploitability.

Two interpretations are possible: (a) the gap exists on paper but is not reachable in practice, or (b) the gap is reachable in ways the red team's first pass missed. Focused investigation discriminates.

Examples:
- Auth middleware missing on internal-only routes that may not be internet-facing
- Rate-limiting absence on endpoints the red team didn't probe in first pass
- CSRF protection inconsistency the red team didn't enumerate state-changing endpoints to surface

#### divergent

One team flagged the area, but the other team explicitly cleared it (red team noted controls present and adequate, or blue team examined the area and found defenses sound). Surface for the report; orchestrator judges priority.

Divergent items are usually low-priority but occasionally significant — when one team is wrong about clearance, divergent findings expose the error.

#### Building the Unified Target List

Merge items across categories. Each entry on the list carries metadata:

- **Origin category** (one of the four above)
- **Origin** (red-team-only, blue-team-only, both)
- **Priority** (CRITICAL / HIGH / MEDIUM / LOW)
- **Files / line ranges** to focus on
- **Hypothesis** (for red-team-origin items) or **defensive gap description** (for blue-team-origin items)
- **Investigation approach**
- **Blue-team context** (the relevant slice of blue-team data, if origin includes blue team) — passed verbatim to the focused red-teamer that takes this target

**Cap the unified list at 25 targets.** When the merged list exceeds 25, triage using category prioritization:

1. **All anchoring-suppressed targets are kept** (highest priority — these are the discipline's payoff).
2. **Convergent targets next** (high confidence, both teams agreed).
3. **Blue-flagged-unverified next** (worth verifying to discriminate paper-only gap from real-world reachability).
4. **Divergent last** (often dropped if over capacity).

A short or empty unified list is a valid outcome. It means both teams found little to attack, independently. Do not manufacture targets to fill slots.

### 4. Deep Investigation — Focused Red-Teamers

**For each target on the unified list, spawn a dedicated `sec-red-teamer` agent:**

```
You are a focused red-teamer investigating a single attack vector.
Mode: focused target

## YOUR TARGET
Target: [from unified list]
Files: [from unified list]
Synthesis category: [anchoring-suppressed | convergent | blue-flagged-unverified | divergent]
Hypothesis: [from unified list]
Defensive context: [included ONLY if the target's origin includes blue-team data —
                    relevant defensive gaps from the blue-team report. Omit
                    for anchoring-suppressed targets and red-team-only divergent
                    targets.]
Context: [from unified list]
Investigation approach: [from unified list]

## PRIOR FINDINGS (if any)
[Findings from other focused red-teamers that might be relevant — especially for chain analysis]

## YOUR MISSION
Go deep on this one target. You have the full methodology available, but your scope is narrow: this single attack vector. Dedicate your full attention to it.

Perform phases 4–7 of your methodology on this target. For each finding:
- Describe the concrete attack (specific enough to reproduce)
- Assess exploitability (how hard is this to actually pull off?)
- Assess impact (what does the attacker get?)
- Note any dependencies on other findings (for chain analysis)

If this vector is a dead end, say so. Don't manufacture findings. A clean report on a well-defended target is valuable.
```

**Run focused agents sequentially, not in parallel.** Each agent's findings may inform the next (chain analysis depends on accumulating findings).

**Pass prior findings to each new agent.** As findings accumulate, each subsequent focused agent receives a summary of what prior agents found. This enables chain discovery — agent 3 might realize that agent 1's low-severity information disclosure combines with agent 2's SSRF to create a critical chain.

### 5. Findings Synthesis and Chain Analysis

After all focused agents have reported, synthesize their findings.

**Chain analysis:**
- Review all findings together. Can any be combined into an exploit chain?
- A chain is two or more individually low/medium-severity findings that combine to create a higher-severity exploit.
- Common chains:
  - Information disclosure + SSRF = access to internal services with knowledge of their endpoints
  - Open redirect + OAuth flow = token theft
  - Low-privilege IDOR + privilege escalation = full account takeover
  - XSS + CSRF = authenticated action without user consent
  - Path traversal + file upload = arbitrary file write → RCE

**If chains are discovered:**
- Create new target entries for each chain
- Return to step 4 with a focused red-teamer dedicated to validating and fully exploiting the chain
- The chain investigator receives all relevant findings from the individual agents and attempts to demonstrate the full chain

**Convergence:** The loop terminates when a synthesis pass produces no new chains. Typically this takes 1–2 chain iterations. If chain analysis keeps producing new chains after 3 iterations, present current findings and let the user decide whether to continue.

### 6. Present Consolidated Findings

Compile all findings from all agents into a single report:

```
## Security Audit Summary

Scope: [what was audited]
Defense evaluation: [summary — N controls inventoried, M gaps found]
Attack surface: [N entry points identified]
Reconnaissance synthesis: N targets across the four categories
  (X anchoring-suppressed, Y convergent, Z blue-flagged-unverified, W divergent)
  [Note any targets dropped during 25-cap triage]
Vectors investigated: [N of M targets from unified list]
Findings: N (X critical, Y high, Z medium, W low)
Exploit chains: N

## DEFENSE POSTURE (from blue-teamer, independent first pass)
[Summary of control inventory and key gaps]
[Defense-in-depth assessment — where security relies on a single control]

## ATTACK SURFACE (from lead red-teamer, independent first pass)
[Entry points discovered, ranked by exposure]

## RECONNAISSANCE SYNTHESIS
[One subsection per category from step 3 (anchoring-suppressed, convergent,
blue-flagged-unverified, divergent), each with its count and one line per
target giving the evidence that placed it there. Then any targets dropped
in 25-cap triage.]

## FINDINGS

### CRITICAL
- **[file:line — target]** — [vulnerability description]
  - Attack: [concrete exploitation path]
  - Impact: [what the attacker gets]
  - Data flow: [entry] → [transformations] → [sink]
  - Defensive gap: [included if blue-team data was relevant to discovery]
  - Fix: [remediation guidance]
  - Discovered by: [blue team independent | red team independent |
                    synthesis (anchoring-suppressed) | focused agent for <target> |
                    chain analysis]

### HIGH
[same format]

### MEDIUM
[same format]

### LOW
[same format]

## EXPLOIT CHAINS
- **[chain name]** — [description of the combined attack]
  - Components: [finding A] + [finding B] + ...
  - Combined impact: [what the chain achieves that individual findings don't]
  - Fix: [which component to fix to break the chain — usually the cheapest link]

## TOOLING RECOMMENDATIONS
[Security tools the project should adopt]

## AREAS NOT COVERED
[Entry points that were deprioritized, limitations of static analysis, things that need runtime testing]

## NON-SECURITY BUGS
[One line each, from any agent's NON-SECURITY BUGS section; route to /bug-fix]
```

**Present to user interactively.** Walk through CRITICAL findings first. For each, explain the attack, the impact, and the recommended fix. Let the user ask questions and discuss before moving to the next finding.

### 7. Cut Tickets

After presenting findings, propose a ticket structure based on the audit's shape. Each audit produces a different finding distribution — concentrated CRITICALs, spread across severity, chain-heavy, defense-in-depth-only — and the right ticket granularity depends on that shape. Rather than prescribe a fixed mapping (one-per-finding, one-per-chain, severity-batched), examine the findings and propose a structure that fits.

#### 7a. Analyze Findings and Propose Structure

Examine the consolidated findings produced in step 6:
- Count by severity (CRITICAL / HIGH / MEDIUM / LOW).
- Count exploit chains.
- Note clustering — multiple findings in the same component, or in the same vulnerability class.
- Note any defense-in-depth observations (typically LOW-severity findings that are not independently exploitable but harden against future regressions).

From that shape, propose a ticket structure. Common shapes:

- **Concentrated CRITICALs:** 1 ticket per CRITICAL/HIGH finding (so each gets dedicated remediation attention); 1 ticket per chain; 1 batch ticket for MEDIUMs/LOWs as "defense-in-depth observations."
- **Spread across severity:** 1 ticket per CRITICAL, 1 ticket per chain, 1 batch per severity for HIGH/MEDIUM/LOW.
- **Defense-in-depth only:** 1 batch ticket listing all observations with a "hardening" framing — no individual tickets.
- **No findings:** No tickets. The audit report stands alone.

Present the proposed structure to the operator with the reasoning, in the shape given by [`references/advisory-tickets.md`](../../references/advisory-tickets.md) § "The proposal step". Wait for the response and dispatch per § "Three outcomes". Approve → proceed to 7b. Edit → loop until approved. Decline → the audit report stands alone, no tracker writes.

#### 7b. Create Tickets

Use the canonical tracker integration documented in [`references/trackers.md`](../../references/trackers.md). For each ticket in the approved structure:

**Title:** `[<SEVERITY>] <concise vulnerability summary>` (e.g., `[CRITICAL] OAuth state parameter not validated on /api/auth/callback`).

**Body sections:**
- **Attack** — concrete reproduction path.
- **Impact** — what the attacker gets.
- **Data flow** — entry → transformations → sink.
- **Defensive gap** (if blue-team data informed the finding) — the relevant blue-teamer observation.
- **Fix guidance** — remediation direction (not concrete code).
- **Discovered by** — `red team independent`, `blue team independent`, `synthesis (anchoring-suppressed)`, `focused agent for <target>`, or `chain analysis`. This is load-bearing: over time it shows whether the parallel-isolated first pass surfaces what a briefed red team would miss. Do not drop it.

**For chain tickets:**
- **Components** — the constituent findings (cite individual finding tickets if they were cut as separate tickets).
- **Combined impact** — what the chain achieves that components alone don't.
- **Cheapest-link fix** — which component to fix first to break the chain.

**For batch tickets:**
- One section per included finding, using the per-finding body structure above.
- A brief intro paragraph explaining the batch theme (e.g., "Defense-in-depth observations — none independently exploitable; addressing these hardens against future regressions and chain construction.").

**Labels:** Apply severity labels (`critical` / `high` / `medium` / `low`) when the tracker supports them. The implementation may also apply a `security` umbrella label if one exists.

After all tickets are created, report the URLs to the operator and exit.

#### Orchestrator-Invoked Behavior

See [`references/advisory-tickets.md`](../../references/advisory-tickets.md) § "Orchestrator-invoked behavior" — the proposal is presented identically to operator and orchestrator; the orchestrator's auto-approval contract is documented in [`references/autonomy.md`](../../references/autonomy.md) § "Auto-approval of sub-skill ticket proposals".

## Agent Coordination

- **Parallel and isolated** in step 2; **orchestrator-direct** synthesis in step 3; **sequential** focused red-teamers in step 4, so findings accumulate for chain analysis.
- **Fresh instances for every agent**, each with its context dedicated to one concern. **No remediation agents:** step 7 cuts tickets; `/implement` remediates against them.
- Hold both first-pass reports, each target's synthesis category, accumulating findings, and the chain-iteration count across steps.

## Abort Conditions

**Abort focused investigation:**
- Agent produces no actionable findings after full investigation (dead end — expected and fine)

**Abort entire workflow:**
- User interrupts
- 3 chain iterations with new chains still being discovered (present findings, ask user)
- Critical system error

**Do NOT abort for:**
- Individual dead-end vectors (skip and continue)
- Low-confidence findings (report at their severity, marked unconfirmed)
- An empty unified target list at phase 3 (this is a positive outcome — the codebase is well-defended; present the synthesis report and stop)

## Integration with Other Skills

**`/review-security` vs `/bug-fix`:** `/review-security` is proactive — a full-depth audit run before major releases or after significant feature additions. `/bug-fix` is reactive — it invokes `sec-blue-teamer` for scoped review of changed code as part of fixing a specific bug.

**`/review-security` vs `/review-release`:** `/review-release` includes basic security checks (secrets, debug artifacts) as part of its pre-release sweep. `/review-security` is the dedicated audit — run it when security assurance is the goal, not as part of routine release prep.

## Example Excerpt — Reconnaissance Synthesis

```
Blue-teamer: 8 controls; gaps include auth middleware missing on /internal/*
  and /ws/*, CSRF on POST only, OAuth state generated but never validated.
Lead red-teamer (no briefing): 14 entry points; 6 targets, including
  /api/auth/callback, /api/upload, /api/export.

ANCHORING-SUPPRESSED (red found; blue's map didn't account for it):
- POST /api/upload — blue listed "upload exists"; red saw the path-
  construction sink. → focused red-teamer gets NO blue-team context.
- GET /api/export — CSV formula injection; blue's output-encoding
  inventory covered HTML only.
CONVERGENT (both flagged independently):
- POST /api/auth/callback — blue: "state not validated"; red: "no
  validation visible". → focused red-teamer gets the blue-team slice.
BLUE-FLAGGED-UNVERIFIED (blue flagged; red didn't reach):
- /internal/* — no auth, but possibly not network-exposed; investigate
  to tell a paper gap from a reachable one.
DIVERGENT: none.

[Step 4 confirms the upload traversal (CRITICAL) and OAuth CSRF
(CRITICAL); /internal/* proves localhost-only (LOW, defense in depth).
Step 5 finds no chain among them; the audit converges.]
```
