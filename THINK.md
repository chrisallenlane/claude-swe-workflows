# /think-\* Skills — Design Discipline

This document states the design discipline that governs the `/think-*` skill family — a namespace of structured-reasoning skills that formalize specific cognitive countermeasures to predictable failure modes of informal human thinking.

It is the standard against which existing `/think-*` skills should be measured and against which new ones should be admitted. The discipline is opinionated, intellectually load-bearing, and specific to this family. **It is not a plugin-wide gating standard.** Other skill families (`/scope`, `/implement`, `/refactor`, `/review-*`, and others) are admitted by different criteria — primarily, whether they earn their keep in real software-engineering work.

## The thesis

> Human reasoning is systematically miscalibrated in predictable ways. Structured discipline is the only reliable countermeasure.

This thesis runs through Kahneman, Tetlock, Klein, Taleb, Schön, and the rationalist tradition. The `/think-*` namespace inherits it. Each skill in the family formalizes a specific procedure that humans habitually cut corners on — and that, when applied, produces better outcomes than informal thinking.

## What makes a `/think-*` skill belong here

A `/think-*` skill is admitted to the namespace if it meets all five tests.

### 1. It targets a specific cognitive failure mode

The skill must answer: *what does informal human reasoning do wrong here, and how does this skill counter it?* Vague rationales like "improves quality" or "helps you think" do not qualify. The countermeasure must be specific and nameable.

Examples from the existing namespace:

- `/think-brainstorm` counters anchoring and evaluation apprehension via Nominal Group Technique.
- `/think-reflect` counters narrative fallacy and luck-mistaken-for-skill via the observation/recollection split.
- `/think-scrutinize` counters confirmation bias via adversarial steelmanning.
- `/think-diagnose` counters narrative preference via observation/interpretation separation.
- `/think-premortem` counters planning fallacy and optimism bias via prospective hindsight.

### 2. Its method comes from a practitioner tradition

The namespace's primary contribution is curatorial. When designing a `/think-*` skill, the first move is to find the practitioner tradition that has already studied this problem. Decision research (Klein, Tetlock), reflective practice (Schön, Kerth), legal proceduralism (adversarial systems), creativity research (Osborn, de Bono, Delbecq & Van de Ven), and the rationalist tradition (steelmanning, calibrated uncertainty) all live in the namespace's lineage.

A new `/think-*` skill should be able to cite the lineage it inherits from. The namespace builds on practitioner traditions; it does not aim to invent reasoning frameworks from scratch.

### 3. It makes uncomfortable questions unskippable

Flexible frameworks get short-circuited. Structured procedures do not. The skill must force the user — or the agent acting on their behalf — to answer the question that informal practice would skip.

- `/think-reflect`'s observation/recollection split is non-negotiable. The user cannot skip to interpretation without first separating record from memory.
- `/think-deliberate` requires advocates to argue every option before the judge rules. Single-option railroading is structurally prevented.
- `/think-premortem` requires the failure to be treated as already-having-happened, not as a forward-looking risk. The framing is load-bearing.

If a `/think-*` skill could be replaced by "the agent thinks about it for a while," it does not belong in the namespace.

### 4. Generation is parallel and isolated; synthesis comes after

The Nominal Group Technique principle: independent generation followed by pooling outperforms coordinated group work on both quantity and quality. The mechanisms it counters are production blocking, evaluation apprehension, and anchoring (Delbecq & Van de Ven, 1971; refined by Paulus, Diehl, Stroebe, and others over decades).

Every `/think-*` skill that *generates* ideas, critiques, diagnoses, reflections, or imagined failures does so via parallel agents in isolation, then synthesizes in a separate phase. Generation and evaluation must not interleave within a generative phase.

This is the most distinctive structural test of the namespace, and the one that most clearly distinguishes `/think-*` skills from other skill families.

### 5. Honest "this didn't apply" is allowed; padding is not

A lens, technique, or reflector that produces little for a specific input must report that, not manufacture content. The orchestrator would rather know a lens did not fit than receive filler. This is the calibration discipline applied to the skill's own behavior.

Calibration of confidence is qualitative throughout. Skills use categories like *high / moderate / low / uncertain* rather than fabricated percentages. If a question cannot be answered from the evidence at hand, that is reported plainly.

## Cross-cutting practices

Several practices recur across the namespace. They are listed here so they can be cited rather than re-explained in each SKILL.md.

**Steelmanning** — when an idea, plan, or position is being critiqued or argued against, the strongest version of it is the target. Strawmen are not allowed. Sourced from the rationalist tradition.

**Observation/recollection split** — when memory and record disagree, prefer the record and surface the disagreement. The gap is itself signal. Sourced from `/think-reflect`'s ground-truth-gathering phase; reusable elsewhere.

**Process-vs-luck attribution** — a good outcome from a bad process reinforces the bad process; a bad outcome from a good process looks like process failure. Attribute honestly, even when uncomfortable. Sourced from Taleb (*Fooled by Randomness*) and Tetlock (*Superforecasting*).

**Decision-quality vs. outcome-quality** — a good decision can have a bad outcome and vice versa. Reflective and pre-mortem skills separate the two. Sourced from Tetlock.

**Calibrated uncertainty** — qualitative confidence categories, not fabricated percentages. Sourced from Tetlock and the broader forecasting literature.

**Prospective hindsight** — treating a hypothetical failure as already-having-happened produces more concrete and better-calibrated cause identification than imagining it as a forward-looking risk. Sourced from Klein.

## Skill versus phase

Some valuable disciplines belong as *phases inside* skills, not as skills of their own. A surgical timeout is a phase. A pre-flight checklist is a phase. The bar for promoting a phase to a standalone `/think-*` skill is twofold: the discipline produces a transferable artifact that other skills could consume, *or* it can be invoked at multiple distinct points in workflows. Otherwise it lives inside a skill, not next to it.

## Spillover: values across the plugin

The five tests above gate `/think-*` admission. They do not gate other skill families. That said, several values from this document apply across the plugin even without strict gating:

- **Practitioner-methodology bias.** When designing any new skill, look for the practitioner tradition that has already studied this problem. `/scope` inherits from agile/XP spike practice; `/implement` from TDD and incremental feature delivery; `/refactor` from Fowler. The bias toward citing lineage is plugin-wide — it's how the plugin avoids reinventing what practitioner traditions have already worked out.

- **Structured discipline beats flexible framework.** Make uncomfortable questions unskippable where a skill's purpose warrants it. `/lead-project`'s commander's-intent elicitation applies this discipline outside the `/think-*` namespace, to good effect.

- **Specific countermeasures over vague aspirations.** Designing a skill against a *specific failure mode* it counters — even informally — produces sharper skills than designing for "improvement" generically.

`/think-*` structural patterns can also be borrowed by other skills where they fit:

- NGT-style isolated parallel agents during generation phases
- Observation/recollection splits where memory and record might disagree
- Calibrated qualitative confidence instead of fabricated percentages
- Steelmanning before critique

The discipline this document codifies is for `/think-*`; the values behind it are for the whole plugin.

## What the `/think-*` namespace deliberately doesn't do

- **It does not invent novel reasoning frameworks.** Skills inherit from existing traditions.
- **It does not pursue completeness for its own sake.** Skills are admitted by need, not by symmetry.
- **It does not optimize for speed at the expense of discipline.** A structured procedure that takes longer than informal thinking is paying the cost of the discipline. Users who want speed have other tools.
- **It does not measure itself in metrics that would be gameable.** Token counts, finding counts, lines changed — these are throughput measures, not quality measures. Calibration matters more than throughput.

## Sources

The namespace's intellectual lineage. In rough priority for someone wanting to dig deeper:

1. **Daniel Kahneman** — *Thinking, Fast and Slow* (2011). The single most load-bearing source.
2. **Philip Tetlock & Dan Gardner** — *Superforecasting* (2015). Decision quality vs. outcome quality; calibrated forecasting.
3. **Donald Schön** — *The Reflective Practitioner* (1983). Reflection as professional discipline.
4. **Gary Klein** — *Sources of Power* (1998); pre-mortem methodology (HBR, 2007). Decision-making under uncertainty.
5. **Nassim Nicholas Taleb** — *Fooled by Randomness* (2001) or *The Black Swan* (2007). Survivorship bias, narrative fallacy, luck-vs-skill.
6. **Edward de Bono** — *Lateral Thinking* (1967), *Six Thinking Hats* (1985). Generative technique palette.
7. **Delbecq & Van de Ven** — "A Group Process Model for Problem Identification and Program Planning" (1971). The original NGT paper.
8. **Charles Sanders Peirce** — essays on abductive reasoning. Philosophical root of `/think-diagnose`.

Adjacent: the **rationalist / LessWrong** tradition (Yudkowsky, Alexander, et al.) for steelmanning and calibrated uncertainty; **Karl Popper** (*Conjectures and Refutations*) for falsifiability; **Norman Kerth** (*Project Retrospectives*) for structured retrospective practice.

## Evolution

This document changes with the namespace, but deliberately. A change to THINK.md is a meaningful event. `/think-*` skills that no longer pass the five tests are candidates for revision or removal — being already shipped does not exempt them.

When a proposed `/think-*` skill seems valuable but cannot meet the five tests, the right response is usually to reformulate it until it can — or to recognize that it belongs as a phase inside an existing skill, in another skill family, or not in the plugin at all.
