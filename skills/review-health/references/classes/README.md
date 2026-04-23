# Reference Classes for /review-health

This directory contains per-class rubrics used by `/review-health` during the Orient phase. The skill classifies the target repository into a reference class and applies the matching rubric to each dimension.

## Why Reference Classes

"Good" is a relational claim, not an absolute one. A 34% test-coverage finding means something different for a research prototype than for an OSS library with external consumers. Practitioner traditions that evaluate heterogeneous artifacts — marine surveying, building inspection, credit rating, medical triage, actuarial rating — converge on class-first evaluation for the same reason: absolute scales produce misleading verdicts often enough to be unworkable.

Per-class rubrics keep the calibration anchor explicit, visible, and overridable. When the skill reports a finding, it cites both the class it applied and the evidence within that class's rubric. A user who disagrees with the classification can override it in one line; every downstream finding reflows against the new class.

## Available Classes

| File | Class | Primary Audience |
|------|-------|------------------|
| `solo-utility.md` | Solo or small-team utility / CLI / internal tool | Author + small known user base |
| `production-service.md` | Team-maintained production service or backend | Live users; on-call rotation |
| `oss-library.md` | OSS library with external consumers | Strangers depending on a stable contract |
| `prototype.md` | Prototype / research / pre-production exploratory work | The author(s); learning, not serving |

## Schema (Every Class File Has These Sections)

- **Signals That Indicate This Class** — observable characteristics that place a repo in this class
- **Counter-Signals** — when observed, route to a different class
- **Class-Relevant Strategic Concerns** — what matters most for this class specifically
- **Dimension Rubrics** — five dimensions (test health, dependency health, CI/automation health, documentation, architecture hygiene), each at three levels (Foundational / Adequate / Strong) with criteria and signals

The three-level scale is deliberately coarse. The purpose is to place a repo on a ladder of sufficiency for its class, not to produce a fine-grained grade. For individual findings that deserve more granular weighting, see `../severity-tiers.md` (Safety Hazard / Major / Minor / Cosmetic).

## Classification in the Orient Phase

The skill uses a differential-diagnosis procedure to classify:

1. **Enumerate candidate classes** based on observable signals (metadata, repo structure, publishability, deployment artifacts, commit patterns) and the lens the user supplied at invocation.
2. **Gather evidence for and against** each candidate.
3. **Rank by weight of evidence** with an explicit confidence hedge.
4. **Report the classification as cited output** — the user sees both the chosen class and the signals that placed the repo there.
5. **Offer override** — one line from the user reclassifies and recomputes.

Ambiguous cases (hybrid repos — a CLI that's also an OSS library, for example) are handled by applying multiple class expectations where they differ and flagging the hybrid explicitly. Marine surveyors, medical triagers, and actuaries all do this routinely; the skill mirrors the tradition.

## Adding a New Class

A new reference class is warranted when:

- The skill is repeatedly applied to a kind of repo that fits none of the existing classes well
- The existing classes would force a systematic miscalibration (e.g., a data-pipeline repo evaluated as a `production-service` would over-weight HTTP-handling concerns that don't apply)
- A meaningful practitioner tradition exists for the new class that would sharpen the rubric

To add a class:

1. Create `references/classes/<class-name>.md` following the schema above.
2. Write the **Signals That Indicate This Class** section first — this drives classification. Make it observable, not aspirational.
3. Write the **Counter-Signals** section — be explicit about when *this* class is wrong.
4. Write the **Class-Relevant Strategic Concerns** section — what a reader should weigh more heavily for this class specifically.
5. Write the per-dimension rubrics. Keep the five dimensions consistent across classes. Adjust criteria to reflect class realities.
6. Add the class to the table in this README.

**Keep rubrics concrete.** Observable signals, named tools, cited thresholds where meaningful. Avoid adjective-stacking ("comprehensive, thorough, robust") — criteria should be falsifiable.

**Avoid grade inflation.** The three levels represent real differences, not hair-splitting. Most repos sit at Adequate; Strong should feel earned; Foundational should feel like a floor the repo has cleared.

**Resist adding dimensions.** Five is already a lot. New dimensions should be justified by class-specific needs that don't fit within the existing five.
