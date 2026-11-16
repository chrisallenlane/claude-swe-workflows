# /review-security - White-Box Security Audit

The step-by-step procedure lives in [`SKILL.md`](../SKILL.md); this guide covers when to use the skill and what to expect.

## Overview

`/review-security` is a full-depth static security audit of a project's source code, combining defensive and offensive analysis. A blue-teamer and a lead red-teamer make an independent first pass **in parallel and in isolation**. Their reports are then pooled into one target list, each target gets a dedicated red-teamer, and findings are cross-referenced for exploit chains until no new chains emerge.

The skill is **advisory only**. It produces findings and proposes tickets; it does not implement remediation. Finding a vulnerability and fixing one take different reasoning, and the discovery agents shouldn't be biased toward findings they could easily fix. Tickets carry the findings across that seam, and `/implement` remediates against them.

```
Scope ──▶ Independent first pass (blue ∥ red, isolated) ──▶ Reconnaissance synthesis
      ──▶ Focused red-teamers ──▶ Chain analysis ──┬── new chains ──▶ (back to focused red-teamers)
                                                   └── converged ──▶ Report ──▶ Ticket proposal
```

## Why the First Pass Is Isolated

An earlier design ran the blue-teamer first and briefed the red-teamer with its report. That had a hidden failure mode, **anchoring**: whatever the blue team flagged became the territory the red team looked at. Real attackers get no defensive briefing. They look at the system fresh and find what defenders never considered.

The current design uses **Nominal Group Technique** (independent generation, then synthesis) as the countermeasure. The red-teamer's reconnaissance runs with no blue-team input, and the synthesis sorts every target by how it was found:

| Category                    | Meaning                                                                             | Priority |
|-----------------------------|-------------------------------------------------------------------------------------|----------|
| **anchoring-suppressed**    | Red team flagged it; blue team's map didn't account for it. The discipline's payoff | Highest  |
| **convergent**              | Both teams flagged it independently. High confidence                                | High     |
| **blue-flagged-unverified** | Blue team called a gap the red team didn't reach. Paper gap or reachable?           | Medium   |
| **divergent**               | One team flagged it; the other explicitly cleared it                                | Variable |

Focused red-teamers get blue-team context only for targets the blue team helped find, so the independent perspective carries into the deep investigation for red-only targets. Every finding and ticket keeps a `Discovered by:` attribution, which over time shows whether the isolated first pass is earning its cost.

## When to Use

**Use `/review-security` for:**
- Pre-release security assurance on important releases
- After significant feature additions that change the attack surface
- Understanding the security posture of a codebase you've just taken on
- Periodic security audits (quarterly, annually, etc.)
- Understanding both what's exploitable and why the defenses failed

**Don't use `/review-security` for:**
- Routine development: `/implement` and `/bug-fix` run the blue-teamer on their own diffs when security-sensitive code changed
- Quick security sanity checks: spawn `sec-blue-teamer` directly
- Runtime security testing: this is static source analysis only
- Release prep: `/review-release` includes basic security checks (secrets, debug artifacts); `/review-security` is the dedicated audit for when security assurance is the goal

**Rule of thumb:** if you'd hire a pentester for this, `/review-security` is the right tool.

## What You'll Be Asked

Unless the invocation or a caller (such as `/review-repo`'s follow-up) supplies scope, the skill asks:

- What to audit: the entire codebase, a module, or a feature area
- Whether anything particularly concerns you (auth, file handling, a recent change). Concerns inform prioritization but don't replace the systematic analysis
- What to skip beyond the defaults

By default the audit covers production code only. Test code, dev-only dependencies and tooling, generated code, and vendored code are excluded unless you ask for them.

## What You Get Back

- **A consolidated report:** the blue team's defense posture, the red team's attack surface, the reconnaissance synthesis by category, findings by severity (each with a concrete attack, impact, data flow, fix guidance, and `Discovered by:`), exploit chains with the cheapest link to break, tooling recommendations, areas not covered, and non-security bugs noticed in passing (routed to `/bug-fix`).
- **An interactive walkthrough,** CRITICAL findings first, with room for your questions.
- **A ticket proposal** shaped to the audit's findings (for example, one ticket per CRITICAL plus one per chain plus a defense-in-depth batch; a single hardening ticket when that's all there is; nothing for a clean audit). You approve, edit, or decline. When an orchestrator invokes the skill, it receives the same proposal and applies its own autonomy judgment.

An empty target list is a positive outcome: both teams independently found little to attack. The skill never changes code.

**Cost:** deliberately heavy. A medium-sized codebase may spawn 5–10+ agents and take significant time. The parallel first pass roughly doubles first-pass cost compared to the old sequential design; that is the price of surfacing anchoring-suppressed targets. If chain analysis is still finding new chains after three iterations, the skill stops and asks whether to continue.

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

[Deep investigation confirms the upload traversal (CRITICAL) and OAuth CSRF
(CRITICAL); /internal/* proves localhost-only (LOW, defense in depth).
Chain analysis finds no chain among them; the audit converges.]
```
