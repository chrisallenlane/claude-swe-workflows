---
name: think-diagnose
description: Abductive reasoning about the causes of a bug, incident, or phenomenon. Parallel diagnosticians apply different lenses; surviving candidates are narrowed by Analysis of Competing Hypotheses (ACH) when needed. Reports leading causes. Feedback only.
model: opus
---

# Think-Diagnose - Abductive Reasoning About Causes

Takes a phenomenon — something that was observed and that the user wants to understand — and produces a ranked set of candidate causes with evidence-based confidence calibration. Uses **abductive reasoning**: inference to the best explanation. Distinct from `/bug-fix` (which handles code-specific diagnosis with artifact output and execution tooling); `/think-diagnose` is pure reasoning about causes, applicable to non-code phenomena as readily as code ones.

**This skill produces no tangible artifacts.** It is a consultant, not an implementer. No code, no tickets, no commits. The output is a structured diagnosis report that the user can act on by gathering more evidence, adopting a leading cause, or piping to `/think-brainstorm` for remediation.

## Roles

**Judge (you, running this skill):**
- Capture the phenomenon in a written brief
- Elicit evidence, rigorously separating observation from interpretation
- Choose appropriate reasoning lenses
- Spawn diagnosticians in isolation
- **Evaluate** candidate causes against evidence (this skill has a real evaluative phase, unlike purely-divergent think-* skills)
- Calibrate confidence honestly
- When candidates won't separate, narrow them by ACH (step 7)
- Report

**Diagnosticians:** Each receives a specific reasoning lens and generates candidate causes (with mechanisms, predictions, refuters, and plausibility) in isolation from other diagnosticians.

**Evidence-gatherers** (narrowing only): `THK - ACH Evidence Gatherer`. Each receives the candidate set and one evidence class, and enumerates confirming and disconfirming evidence neutrally, in isolation. Gatherers never pick a hypothesis.

## Workflow

### 1. Receive the Phenomenon

The phenomenon may arrive as:
- **Conversation context** — summarize it back, confirm
- **A document** — read the file (incident report, data summary, observation log)
- **Fresh user input** — capture verbatim

**Produce a written brief** of the phenomenon. Precisely what is the thing to explain? Vague phenomena produce vague diagnoses.

### 2. Gather Evidence — Separate Observation from Interpretation

**This is the most failure-prone step in the entire workflow, and it has enforced structure.** Most bad diagnoses start by accepting interpretations as observations.

**Elicit from the user, in three distinct buckets:**

- **Observations** — concrete things that were measured, seen, or experienced. "The metric dropped 30% on March 14th." "Three customers mentioned X in surveys." "The build broke at commit abc123."
- **Interpretations already held** — what the user or others have already *inferred* from the observations. "The team thinks it's because of the migration." "We believe the drop is due to seasonality." Flag these explicitly so diagnosticians know not to accept them as given.
- **Unavailable / unknown evidence** — what's unknown, wasn't measured, or can't be retrieved. "We don't have per-user data before April." "We didn't log the old config."

**Push back on smuggled interpretations.** If the user says "the metric dropped because of the migration," that's two claims: (a) the metric dropped (observation) and (b) the migration caused it (interpretation). Separate them before proceeding.

**3-6 clarifying questions is typical** to establish this split. Stop when you have enough to pass diagnosticians material they can work with.

### 3. Choose Reasoning Lenses

Select 3-6 lenses from the palette based on the phenomenon's shape.

**Available lenses:**
- **technical** — engineering-level causes (code, infra, config, capacity, dependencies)
- **human-factors** — people, skills, fatigue, turnover, miscommunication, team dynamics
- **process** — broken or missing process, handoffs, approvals, ownership, rituals
- **incentive-structure** — the system rewards the behavior we're diagnosing (Goodhart territory)
- **environmental** — external factors (market, regulation, customer mix, vendor, upstream)
- **temporal** — something changed in time that correlates with the phenomenon
- **measurement-artifact** — the phenomenon isn't real, it's a metric/instrumentation issue
- **statistical** — base rates, regression to mean, Simpson's paradox, confounders, selection

**Selection heuristics:**
- Phenomenon is metric-based? **Always include measurement-artifact.** Underrated; catches a large share of false phenomena.
- Phenomenon has a clear onset date? Include temporal.
- Phenomenon involves aggregate data (averages, ratios)? Include statistical.
- Phenomenon is in a team/org context? Include human-factors, process, incentive-structure.
- Phenomenon is in a codebase or system? Include technical.
- Phenomenon occurs in a context with external inputs (customers, markets, vendors)? Include environmental.

**Drop lenses that don't fit.** A phenomenon in a closed system without external dependencies probably doesn't need environmental. A phenomenon observed directly (not through metrics) probably doesn't need measurement-artifact.

### 4. Spawn Diagnosticians (Parallel, Isolated)

Spawn one `THK - Diagnostician` agent per chosen lens, in parallel. Each receives:
- The phenomenon brief
- The observations
- The interpretations already held (flagged — not to be accepted as given)
- The unavailable evidence
- Its assigned lens
- Instruction to generate 3-8 candidate causes, each with mechanism / predictions / refuters / plausibility

**No cross-talk between diagnosticians.** NGT principle — independent reasoning first, evaluation second. Isolated diagnosticians produce more distinct candidate causes; coordinated ones anchor on the first compelling story.

Collect all candidate causes.

### 5. Evaluate Fit — Orchestrator's Work

Unlike the purely divergent `/think-*` skills, this phase requires the orchestrator to evaluate candidates against evidence.

**For each candidate cause from step 4, evaluate:**

- **Explanatory fit** — does this cause explain the observed phenomenon? Does it explain *all* the observations, or only some?
- **Prediction check** — the diagnostician stated what we'd expect to see if this cause were true. Do we observe those things? (Some predictions may require the user to check; note them.)
- **Refuter check** — the diagnostician stated what would disprove this cause. Do we observe any of those refuters?
- **Parsimony** — is there a simpler cause that fits equally well? Prefer the simpler one if fit is comparable.
- **Domain plausibility** — given what's known about the domain, how plausible is this cause? This uses general reasoning, not just evidence fit.

**Cluster causes across lenses.** Some causes from different lenses are the same underlying mechanism viewed from different angles (e.g., "engineers ship half-finished features" seen through human-factors and incentive-structure may converge on the same root cause). Merge and preserve lens attribution.

**Resist compelling-narrative bias.** Causes with clean stories are dangerous; they feel explanatory even when they don't fit the evidence. Weight evidence fit over story quality. When in doubt, flag "compelling story, weak fit" explicitly.

### 6. Calibrate Confidence

**No fabricated percentages.** Use qualitative categories with clear meaning:

- **Strong fit** — cause explains all observations, predictions confirmed (or testable), no refuters observed, plausible. This is a leading candidate.
- **Moderate fit** — cause explains most observations, some predictions unconfirmed but not contradicted, plausible. Secondary candidate.
- **Weak fit** — cause explains some observations, significant predictions unconfirmed, possibly plausible. Long-shot candidate.
- **Unable to distinguish** — two or more causes fit the evidence equally well. Cannot converge without more evidence.

**Honest uncertainty is valuable.** "Cause A looks most likely but evidence is sparse; disambiguating observation X would shift the picture" is a better output than fake precision.

### 7. Narrow by ACH (when candidates won't separate)

Narrative fit-checking has a known blind spot: it asks "does this evidence fit?", and any compelling candidate can collect fitting evidence. Richards Heuer's **Analysis of Competing Hypotheses** (*Psychology of Intelligence Analysis*, CIA, 1999) asks the opposite question for every cell, "does this evidence *disconfirm* it?", and ranks on the answer.

**Run it when:**
- Step 6 left **3 or more candidates at moderate fit or better**, or an "unable to distinguish" tie.
- Evidence exists, or can be gathered, to discriminate among them.
- The candidates make different predictions. If they don't, they can't be discriminated; merge them or sharpen them first.

Otherwise skip it and say so in one line. This step decides among *these* candidates; it does not generate new ones.

**7a. Complete the hypothesis set.** Use the candidates from step 6, and add:
- a **null** hypothesis ("nothing unusual is happening; this is noise, normal variance, or an artifact"), unless something has demonstrably happened that requires explanation;
- a **deceptive** hypothesis ("appearances are being manipulated"), when trust, security, or signals that could be manipulated are involved.

Diagnostic lenses rarely produce these two, so adding them is required. Aim for 4–7 hypotheses. User-held interpretations are hypotheses too; add them now, not earlier, so they don't anchor the diagnosticians.

**7b. Gather evidence in parallel and in isolation.** Spawn 3–5 `THK - ACH Evidence Gatherer` agents, one per evidence class, with no cross-talk. Give each the brief, the observations, and the hypothesis set.

| Class                  | What it surfaces                                    | Include when                              |
|------------------------|-----------------------------------------------------|-------------------------------------------|
| direct-observational   | Logs, metrics, readings, accounts                   | Any direct observation exists (always)    |
| documentary-historical | Decisions, prior reports, config and change history | The question isn't instantaneous          |
| structural             | What the system or environment makes (im)possible   | Systems, code, architecture               |
| behavioral             | Patterns of action over time                        | People or systems acting over time        |
| absent                 | What's *not* there: the dog that didn't bark        | Always, for security, trust, or deception |
| anomalous              | Data points no obvious story explains               | Unexplained observations were flagged     |

Merge and deduplicate the evidence (typically 8–20 items), keeping each item's reliability note.

**7c. Build the matrix.** For every (hypothesis, evidence) cell, mark:
- **C** (consistent),
- **I** (inconsistent),
- **N/A** (no bearing; silence is not support).

Use **CC** or **II** for unusually decisive cells. **Evaluate each cell on its own.** Work row by row, then check the columns, so earlier cells don't anchor later ones.

**7d. Diagnosticity.** Evidence consistent with every hypothesis tells you nothing; set it aside. Evidence that splits the hypotheses carries the weight. One highly diagnostic item outweighs ten non-diagnostic ones.

**7e. Rank by least disconfirmation.** Order the hypotheses by their inconsistent marks, **never** by their consistent ones. This is non-negotiable: flipping it brings back the confirmation bias the technique exists to remove. A hypothesis can't be proven, only fail to be disproven. Keep every hypothesis on the leaderboard: second place is "currently second", not "wrong".

**7f. Sensitivity.** For each piece of load-bearing evidence, ask: what if it's wrong, misread, planted, or open to another interpretation? If changing a single item changes the leader, that item is the highest-leverage thing to verify before acting.

**7g. Falsification milestones.** For the top 2–3 hypotheses, list the observations that would separate them: "if A, we should see X; if B, Y; Z would rule out A but not B". These fill the report's Distinguishing Evidence section.

### 8. Report

**Final report format:**

```
## Diagnosis Report

**Phenomenon:** [one-line summary]
**Lenses applied:** [list]

### Observations

[Concrete ground-truth observations, as elicited in step 2]

### Interpretations Held Aside

[Interpretations the user or others held, flagged as not-accepted-as-given
for the diagnosis. If any turned out to be correct, that's reported in
the leading candidate section; if not, they remain held aside.]

### Unavailable Evidence

[What's unknown or wasn't measured — constrains what can be concluded]

### Leading Candidate(s)

[1-2 causes with strong fit. For each:]

#### [cause name] — strong fit

**Mechanism:** [how this cause produces the observations]

**Evidence fit:**
- Observations explained: [which]
- Predictions confirmed: [which; or "would need to check X"]
- Refuters: [none observed / note any partial refuters]

**Plausibility:** [brief domain-knowledge assessment]

**Lens(es):** [which diagnostician(s) surfaced this]

### Other Candidates

[Moderate-fit and weak-fit causes, briefly. Include lens attribution.]

### Narrowing (only if step 7 ran)

[Hypotheses, including the null and deceptive ones you added; evidence with its classes; the matrix (C / I / N/A); high- and low-diagnosticity evidence; a leaderboard ordered by least disconfirmation; sensitivity, naming the load-bearing evidence and what flips if it's wrong. If step 7 didn't run, one line saying why.]

### Distinguishing Evidence

[Concrete observations the user could gather to distinguish between the
leading candidates (the falsification milestones, when step 7 ran). This is
the most actionable part of the report: specific tests, not "more data" in the abstract.]

For example:
- To distinguish cause A from cause B: check whether [specific observable].
  If [X], cause A. If [Y], cause B.

### What Remains Unknown

[Questions the diagnosis raised but cannot answer with current evidence.
May include "original interpretation X still possible but no stronger
support than alternatives."]

### Recommendation

One of:
- **Act on leading candidate** — evidence fit is strong; proceed with remediation of [cause]
- **Gather distinguishing evidence first** — leading candidates tie; collect [specific observations] to converge
- **The phenomenon may not be real** — measurement-artifact lens produced a strong candidate; verify the observation before diagnosing further
- **Insufficient evidence for confident diagnosis** — current observations don't distinguish among plausible causes; decision needed on whether to gather more data or accept uncertainty

### Suggested Next Steps

- To remediate the leading cause: `/think-brainstorm` for interventions (or `/bug-fix` if the cause is in code)
- To gather distinguishing evidence: [specific checks listed above]
- To pressure-test the leading cause before acting: `/think-scrutinize`
```

### 9. No Iteration

This skill is one-shot. If the user gathers distinguishing evidence and wants an updated diagnosis, they re-invoke with the new evidence in hand. Each invocation is a clean diagnostic consultation.

## Constraints

- **No artifacts.** No code, tickets, commits, or documents.
- **Separate observation from interpretation.** Non-negotiable in the evidence-gathering phase.
- **Isolated generation.** Diagnosticians do not see each other's output during generation, and neither do evidence-gatherers.
- **Disconfirmation ranks.** When narrowing runs, the leaderboard is ordered by least inconsistent evidence. That rule is non-negotiable.
- **Independent cells.** Each matrix cell is judged on its own.
- **Honest uncertainty.** No fabricated confidence numbers. Qualitative categories only.
- **Evidence fit > story quality.** Compelling narratives are suspect; evidence fit wins.
- **Honest "can't distinguish"** is a valid, valuable outcome.

## When to Use

**Good fit:**
- Unexplained metric changes — "why did engagement drop 15% starting March 1?"
- Recurring problems with unclear cause — "why does this project keep slipping?"
- Behavioral patterns — "why do customer calls go badly when we raise prices?"
- Organizational issues — "why does our goal-setting process keep producing missed goals?"
- Anywhere `/bug-fix` doesn't apply because the phenomenon isn't code-specific
- Several explanations already on the table, which need rigorous narrowing. Pass them in as interpretations; if they survive step 6 without separating, step 7 narrows them.

**Poor fit:**
- Known causes needing intervention design — use `/think-brainstorm`
- Code-specific diagnosis — use `/bug-fix` (artifact output, execution tooling)
- Choosing between options — use `/think-deliberate`
- Stress-testing a plan — use `/think-scrutinize`
- Phenomena so vaguely described that no observations exist (refine the phenomenon first)

**Rule of thumb:**
- "Why is this happening?" → `/think-diagnose`
- "Code is broken, find and fix it" → `/bug-fix`
- "What could I do about this?" → `/think-brainstorm`

## Relationship to Other Skills

**Natural downstreams:**
- If cause is identified → `/think-brainstorm` for remediation interventions
- If cause is in code → `/bug-fix` for targeted investigation and fix
- If cause is uncertain between candidates → gather the distinguishing evidence (or falsification milestones), then re-invoke `/think-diagnose`
- Before acting on the leading cause → `/think-scrutinize` to stress-test the intervention plan

**Natural pipeline (for non-code phenomena):**

```
/think-diagnose → /think-brainstorm → /think-deliberate → /think-scrutinize
    why?            what to do?         which approach?      what's wrong?
```

## Philosophy

When candidates tie, the narrowing step adds Heuer's discipline: ask what *disconfirms*, not what fits. Every candidate can collect fitting evidence. The one that survives is the one hardest to kill.
