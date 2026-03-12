---
name: audit-source
description: White-box security audit. Spawns a lead red-teamer for reconnaissance, then dedicated red-teamers per attack vector for deep exploitation analysis. Iterates when exploit chains are discovered. Heavy and thorough by design.
model: opus
---

# Audit Source — White-Box Security Audit

Orchestrates an adversarial security assessment of the project's source code. A lead red-teamer performs reconnaissance and identifies attack vectors, then dedicated red-teamers investigate each vector in depth. Findings are synthesized, exploit chains are explored, and the process iterates until no new chains emerge.

**This is deliberately heavy.** Thoroughness is the priority, not speed. A complete audit may spawn many agents and take significant time. That's the point — shallow security reviews miss the vulnerabilities that matter.

## Workflow Overview

```
┌──────────────────────────────────────────────────────┐
│                   AUDIT WORKFLOW                     │
├──────────────────────────────────────────────────────┤
│  1. Determine scope                                  │
│  2. Spawn lead red-teamer (reconnaissance)           │
│     └─ Output: attack surface + ranked vector list   │
│  3. For each high-confidence vector:                 │
│     └─ Spawn focused red-teamer (deep investigation) │
│  4. Synthesize findings                              │
│     ├─ If exploit chains found → goto 3 (new vector) │
│     └─ If no new chains → proceed                    │
│  5. Present consolidated findings to user            │
│  6. Optionally route findings to fixers              │
└──────────────────────────────────────────────────────┘
```

## Workflow Details

### 1. Determine Scope

**Default:** Entire codebase.

**If user specifies scope:** Respect it (directory, files, module, feature area). Pass scope to all spawned agents.

**Ask the user:**
- "What is the scope of the audit?" (entire codebase, specific module, specific feature)
- "Is there anything you're particularly concerned about?" (auth, file handling, a recent change, etc.)
- "Are there any areas I should skip?" (vendored code, generated code, test fixtures)

User concerns inform the prioritization of vectors in step 2, but the lead red-teamer still performs full reconnaissance — user intuition supplements, not replaces, systematic analysis.

### 2. Reconnaissance — Lead Red-Teamer

**Spawn a `sec-red-teamer` agent in broad recon mode:**

```
You are the lead red-teamer for a white-box security audit.

Scope: [entire codebase | user-specified scope]
User concerns: [any areas of concern mentioned by user, or "none specified"]

Perform phases 1–3 of your methodology:
1. Reconnaissance — map the full attack surface (every entry point, what it accepts, who can reach it)
2. Data flow tracing — for each entry point, trace input to its final destination. Note validation gaps, dangerous sinks, and transformation hazards. You don't need to fully exploit yet — identify where the promising targets are.
3. Trust boundary mapping — identify where trust transitions occur and which boundaries look weakest.

Do NOT perform deep exploitation yet. Your job is to survey the landscape and produce a prioritized target list.

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
- Priority: [CRITICAL / HIGH / MEDIUM]
- Investigation approach: [what the focused red-teamer should try]

Rank targets by a combination of exposure (how easy to reach) and potential impact (how bad if exploited). Limit to the top 10 targets — quality over quantity.
```

**When the lead reports back:** Review the target list. This is the basis for the deep-dive phase.

### 3. Deep Investigation — Focused Red-Teamers

**For each target in the lead's list (CRITICAL and HIGH priority), spawn a dedicated `sec-red-teamer` agent:**

```
You are a focused red-teamer investigating a single attack vector.

## YOUR TARGET
Target: [from lead's report]
Files: [from lead's report]
Hypothesis: [from lead's report]
Context: [from lead's report]
Investigation approach: [from lead's report]

## PRIOR FINDINGS (if any)
[Findings from other focused red-teamers that might be relevant — especially for chain analysis]

## YOUR MISSION
Go deep on this one target. You have the full methodology available, but your scope is narrow: this single attack vector. Dedicate your full attention to it.

Perform phases 4–7 of your methodology on this target:
4. Break assumptions — systematically challenge what the developer assumed about input to this entry point
5. Exploit error paths — trigger errors in this code path and see what breaks
6. Attack state and timing — look for race conditions, replay, sequence bypass specific to this target
7. Git archaeology — check the history of these specific files for security smells

For each finding:
- Describe the concrete attack (specific enough to reproduce)
- Assess exploitability (how hard is this to actually pull off?)
- Assess impact (what does the attacker get?)
- Note any dependencies on other findings (for chain analysis)

If this vector is a dead end, say so. Don't manufacture findings. A clean report on a well-defended target is valuable.
```

**Run focused agents sequentially, not in parallel.** Each agent's findings may inform the next (chain analysis depends on accumulating findings).

**Pass prior findings to each new agent.** As findings accumulate, each subsequent focused agent receives a summary of what prior agents found. This enables chain discovery — agent 3 might realize that agent 1's low-severity information disclosure combines with agent 2's SSRF to create a critical chain.

### 4. Synthesize and Chain

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
- Return to step 3 with a focused red-teamer dedicated to validating and fully exploiting the chain
- The chain investigator receives all relevant findings from the individual agents and attempts to demonstrate the full chain

**Convergence:** The loop terminates when a synthesis pass produces no new chains. Typically this takes 1–2 chain iterations. If chain analysis keeps producing new chains after 3 iterations, present current findings and let the user decide whether to continue.

### 5. Present Consolidated Findings

Compile all findings from all agents into a single report:

```
## Security Audit Summary

Scope: [what was audited]
Attack surface: [N entry points identified]
Vectors investigated: [N of M targets from recon]
Findings: N (X critical, Y high, Z low)
Exploit chains: N

## ATTACK SURFACE
[Summary from lead red-teamer]

## FINDINGS

### CRITICAL
- **[file:line — target]** — [vulnerability description]
  - Attack: [concrete exploitation path]
  - Impact: [what the attacker gets]
  - Data flow: [entry] → [transformations] → [sink]
  - Fix: [remediation guidance]
  - Discovered by: [lead recon | focused agent for <target> | chain analysis]

### HIGH
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
```

**Present to user interactively.** Walk through CRITICAL findings first. For each, explain the attack, the impact, and the recommended fix. Let the user ask questions and discuss before moving to the next finding.

### 6. Route to Fixers (Optional)

After presenting findings, ask the user: "Would you like to route these findings to agents for remediation?"

**If yes:**
- For each finding, determine the appropriate fixer:
  - Web vulnerabilities (XSS, CSRF, clickjacking) → `swe-sme-html`, `swe-sme-javascript`, or `swe-sme-css` depending on the fix
  - Injection vulnerabilities (SQL, command, path) → language-appropriate SME
  - Auth/crypto issues → `sec-reviewer` for defensive remediation guidance, then language SME for implementation
  - For exploit chains → fix the cheapest link (the component that's easiest to remediate and breaks the chain)

- Spawn the appropriate agent with the finding details and remediation guidance
- After each fix, spawn `qa-engineer` to verify the fix doesn't break functionality
- Commit each fix atomically

**If no:** The audit report stands on its own. The user can act on findings at their discretion.

## Agent Coordination

**Sequential execution within each phase.** Focused red-teamers run sequentially so findings accumulate for chain analysis.

**Fresh instances for every agent.** Each red-teamer gets a clean context window dedicated entirely to its target. This is the core design principle — full context dedicated to a single vector.

**State to maintain (as orchestrator):**
- Lead red-teamer's attack surface report and target list
- Each focused agent's findings (accumulating)
- Chain analysis results
- Current iteration count (for convergence limit)
- Running totals for the summary

## Abort Conditions

**Abort focused investigation:**
- Agent produces no actionable findings after full investigation (dead end — expected and fine)

**Abort entire workflow:**
- User interrupts
- 3 chain iterations with new chains still being discovered (present findings, ask user)
- Critical system error

**Do NOT abort for:**
- Individual dead-end vectors (skip and continue)
- Low confidence findings (include in report as LOW)

## Integration with Other Skills

**Relationship to `/bugfix`:**
- `/bugfix` invokes `sec-reviewer` for scoped security review of changed code
- `/audit-source` is a dedicated, full-depth security audit
- Use `/audit-source` proactively; `/bugfix` handles security reactively

**Relationship to `/implement`:**
- `/implement` may invoke `sec-reviewer` as part of its review phase
- `/audit-source` is independent and deeper — run it when security assurance matters, not as part of routine development

**Relationship to `/review-release`:**
- `/review-release` includes basic security checks (secrets, debug artifacts)
- `/audit-source` is a comprehensive pre-release security audit — run it before major releases or after significant feature additions

## Example Session

```
> /audit-source

What is the scope of the audit?
> Entire codebase

Anything you're particularly concerned about?
> We just added OAuth support and I'm worried about the token handling

Any areas to skip?
> vendor/ and testdata/

Starting white-box security audit...

[Phase 1 — Reconnaissance]
Spawning lead red-teamer...

Lead red-teamer report:
  Attack surface: 14 entry points (8 API, 3 WebSocket, 2 CLI, 1 file upload)
  Trust boundaries: 5 identified (2 implicit — database trust, env var trust)
  Targets identified: 7 (3 critical, 3 high, 1 medium)

Target list:
  CRITICAL-1: POST /api/auth/callback — OAuth token exchange, token stored in session
  CRITICAL-2: POST /api/upload — file upload with path construction from user input
  CRITICAL-3: WebSocket /ws/chat — message handler with no auth check
  HIGH-1: GET /api/users/:id — IDOR candidate, auth present but no ownership check
  HIGH-2: POST /api/search — query parameter passed to raw SQL
  HIGH-3: PUT /api/settings — admin endpoint, middleware applied inconsistently
  MEDIUM-1: GET /api/export — CSV generation with user-controlled column names

[Phase 2 — Deep Investigation]

Spawning focused red-teamer for CRITICAL-1 (OAuth callback)...
  Finding: OAuth state parameter not validated — CSRF on auth callback
  allows attacker to link victim's account to attacker's OAuth identity.
  Severity: CRITICAL
  Attack: Attacker initiates OAuth flow, captures callback URL with their
  code, sends victim to that URL. Victim's session now linked to attacker's
  OAuth account.

Spawning focused red-teamer for CRITICAL-2 (file upload)...
  Finding: Path traversal in upload destination. Filename from multipart
  form used directly in path.join() — ../../etc/cron.d/backdoor writes
  to arbitrary location.
  Severity: CRITICAL

Spawning focused red-teamer for CRITICAL-3 (WebSocket)...
  Finding: Dead end. WebSocket handler does check auth via upgrade
  headers. Lead misread the middleware chain. No finding.

Spawning focused red-teamer for HIGH-1 (IDOR)...
  Finding: Confirmed. GET /api/users/:id returns full user record
  including email, hashed password, and API keys for any valid user ID.
  Severity: HIGH (requires authentication)

Spawning focused red-teamer for HIGH-2 (SQL injection)...
  Finding: Confirmed. Search parameter reaches raw SQL via template
  string. POST /api/search with body {"q": "' UNION SELECT * FROM
  users--"} dumps user table.
  Severity: CRITICAL (upgraded from HIGH — unauthenticated endpoint)

Spawning focused red-teamer for HIGH-3 (admin settings)...
  Finding: PUT /api/settings/theme has admin middleware. PUT
  /api/settings/notifications does not. Regular user can modify
  notification settings for all users.
  Severity: HIGH

[Phase 3 — Chain Analysis]

Analyzing 5 findings for chains...

Chain found: IDOR (HIGH-1) + OAuth CSRF (CRITICAL-1)
  → Attacker reads victim's email via IDOR, initiates OAuth link for
  that email, sends CSRF callback to victim. Result: attacker gains
  OAuth access to victim's account without knowing their password.

Spawning chain investigator...
  Chain confirmed. Full exploitation path validated.
  Combined severity: CRITICAL

No further chains discovered. Audit converging.

## Security Audit Summary
Scope: entire codebase (excluding vendor/, testdata/)
Attack surface: 14 entry points
Vectors investigated: 6 of 7 targets
Findings: 6 (3 critical, 2 high, 0 low)
Exploit chains: 1

[Detailed findings presented to user...]

Would you like to route these findings to agents for remediation?
> Yes, let's fix the criticals

[Routing CRITICAL findings to appropriate SMEs...]
```
