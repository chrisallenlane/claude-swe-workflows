# /review-security - White-Box Security Audit

## Overview

The `/review-security` skill orchestrates a comprehensive security assessment of the project's source code using both defensive and offensive analysis. The blue-teamer and lead red-teamer run their first pass **in parallel and in isolation** — neither sees the other's output during reconnaissance. The orchestrator then synthesizes their reports into a unified target list, classifying each target by how it was discovered. Dedicated red-teamers investigate each target in depth. Findings are synthesized, exploit chains are explored, and the process iterates until no new chains emerge.

**Key benefits:**
- **NGT discipline** — independent generation followed by synthesis, designed to surface the gaps anchoring would otherwise suppress
- Deep investigation: each attack vector gets a dedicated agent with full context
- Synthesis triage: every target is categorized (anchoring-suppressed, convergent, blue-flagged-unverified, divergent), making the rationale for investigation explicit
- Chain discovery: findings are cross-referenced to identify multi-step exploit chains
- Iterative convergence: the process loops until no new chains emerge
- Actionable output: findings include concrete attacks, not abstract warnings

## When to Use

**Use `/review-security` for:**
- Pre-release security assurance on important releases
- After significant feature additions that change the attack surface
- When onboarding a new codebase and you want to understand its security posture
- Periodic security audits (quarterly, annually, etc.)
- When you need to understand both what's exploitable and why the defenses failed

**Don't use `/review-security` for:**
- Routine development (the blue-teamer runs automatically during `/implement` and `/bug-fix`)
- Quick security sanity checks (spawn `sec-blue-teamer` directly)
- Runtime security testing (this is static source analysis only)

**Rule of thumb:** If you'd hire a pentester for this, `/review-security` is the right tool. If you just want a security review of your latest changes, `/implement` and `/bug-fix` already include one.

## Why NGT Isolation

The earlier sequential design ran the blue-teamer first and then a lead red-teamer informed by the blue-team report. This was deliberate, but had a hidden failure mode: **anchoring**. Whatever the blue team flagged became the salient territory for the red team. Real attackers don't get a defensive briefing — they look at the system fresh and find what defenders missed. The sequential design optimized for *exploit the known gaps* but underweighted *find the gaps the defenders never considered*.

The current design treats anchoring as a specific cognitive failure mode, with **Nominal Group Technique** (independent generation, then synthesis) as the structured countermeasure. The lead red-teamer's first pass runs without blue-team input — pure attacker perspective. The orchestrator then pools both reports and triages targets by category. Focused red-teamers in the deep-investigation phase still receive blue-team context for targets where it's relevant; the discipline is to keep the *first-pass reconnaissance* uncontaminated.

## Workflow

```
┌──────────────────────────────────────────────────────────┐
│                   AUDIT WORKFLOW                          │
├──────────────────────────────────────────────────────────┤
│  1. Determine scope                                       │
│  2. Independent first pass — parallel and isolated        │
│     ├─ Blue-teamer: defense evaluation                    │
│     └─ Lead red-teamer: recon (NO blue-team input)        │
│  3. Reconnaissance synthesis                              │
│     ├─ Pool both reports                                  │
│     ├─ Categorize each target:                            │
│     │  • anchoring-suppressed                             │
│     │  • convergent                                       │
│     │  • blue-flagged-unverified                          │
│     │  • divergent                                        │
│     └─ Output: unified prioritized target list            │
│  4. For each target:                                      │
│     └─ Spawn focused red-teamer (deep investigation)      │
│        Blue-team context passed only when target's        │
│        origin includes blue-team data                     │
│  5. Synthesize findings + chain analysis                  │
│     ├─ If exploit chains found → goto 4 (new vector)      │
│     └─ If no new chains → proceed                         │
│  6. Present consolidated findings to user                 │
│  7. Optionally route findings to fixers                   │
└──────────────────────────────────────────────────────────┘
```

### 1. Determine Scope

The skill asks about scope, areas of concern, and areas to skip. By default, the audit targets production code only — test code, dev-only dependencies, generated code, and vendored code are excluded. Users can override these defaults. User concerns inform prioritization but don't replace systematic analysis.

### 2. Independent First Pass — Parallel and Isolated

Two agents spawn **in parallel**. Neither sees the other's output during this phase.

- A `sec-blue-teamer` agent performs a full defense evaluation: control inventory, consistency checking, defense-in-depth assessment, configuration review, dependency hygiene, and secrets audit.
- A `sec-red-teamer` agent runs phases 1–3 of its methodology (reconnaissance, data flow, trust boundaries) **without any blue-team input**. Pure attacker perspective from a cold read of the codebase.

This is the load-bearing discipline. The lead red-teamer's recon is less targeted than it would be in the old informed design — that's intentional. The job is to surface what the blue team didn't anticipate.

### 3. Reconnaissance Synthesis

The orchestrator pools both reports and produces a unified target list. **This step is orchestrator-direct, not a sub-agent** — the categorization rules are mechanical, the orchestrator already holds both reports, and avoiding an extra agent invocation saves cost.

Each target is categorized as one of four types:

| Category                     | Meaning                                                                            | Priority |
|------------------------------|------------------------------------------------------------------------------------|----------|
| **anchoring-suppressed**     | Red team flagged but blue team didn't account for. **The highest-value category** — these are the gaps anchoring would have suppressed under the old sequential design. | Highest  |
| **convergent**               | Both teams independently flagged the same target. High confidence; investigate.    | High     |
| **blue-flagged-unverified**  | Blue team called a gap but red team didn't reach in independent recon. Worth investigating to confirm exploitability. | Medium   |
| **divergent**                | One team flagged, the other explicitly cleared. Noteworthy; orchestrator judges priority. | Variable |

The unified target list is capped (typically at 25). The orchestrator triages by category, prioritizing anchoring-suppressed and convergent over blue-flagged-unverified and divergent. Each target carries its synthesis category as metadata, which is preserved in the final report.

### 4. Deep Investigation (Focused Red-Teamers)

Each prioritized target gets a dedicated `sec-red-teamer` agent with a full context window focused on that single attack vector. Agents run sequentially so findings accumulate for chain analysis.

**Blue-team context is passed selectively.** Focused red-teamers receive relevant blue-team observations only for targets whose origin includes blue-team data (convergent and blue-flagged-unverified categories). Targets discovered solely by the red team (anchoring-suppressed) get no blue-team context — the discipline of independent perspective continues into the deep-investigation phase for these targets.

### 5. Chain Analysis

Findings are cross-referenced to identify exploit chains — combinations of individually low/medium-severity findings that together create a high/critical-severity exploit. New chains trigger additional focused investigation. The loop converges when no new chains are found (capped at 3 iterations).

### 6. Consolidated Report

A single report combining the blue team's defensive assessment, the red team's offensive findings, the reconnaissance synthesis (with target categorization), and any exploit chains discovered. Findings carry an expanded `Discovered by:` attribution: *blue team independent*, *red team independent*, *synthesis (anchoring-suppressed)*, *focused agent*, or *chain analysis*. Presented interactively — CRITICAL findings first.

### 7. Remediation Routing (Optional)

Findings can be routed to appropriate SME agents for implementation. Each fix is verified by `qa-engineer` and committed atomically.

## Agents Used

| Agent             | Role                                                                          |
| ----------------- | ----------------------------------------------------------------------------- |
| `sec-blue-teamer` | Defensive posture evaluation (independent first pass)                         |
| `sec-red-teamer`  | Offensive reconnaissance and exploitation (lead first pass + focused targets) |
| `swe-sme-*`       | Implement remediation fixes (optional)                                        |
| `qa-engineer`     | Verify fixes don't break functionality (optional)                             |

## Resource Usage

This skill is deliberately heavy. A full audit of a medium-sized codebase may spawn 5–10+ agents and take significant time. That's by design — shallow security reviews miss the vulnerabilities that matter.

The parallel first pass roughly doubles the first-pass token cost compared to the older sequential design, where the lead red-teamer's recon was more targeted because it was informed. This is a calculated trade-off — the discipline is worth the cost given the value of surfacing anchoring-suppressed targets.
