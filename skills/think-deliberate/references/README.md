# /think-deliberate - Adversarial Decision Making

## Overview

`/think-deliberate` makes a decision among two or more options by adversarial representation. One advocate agent argues for each option, the advocates rebut each other and answer the judge's questions, and the judge (the Claude running the skill) renders a verdict with reasoning, trade-offs, and confidence.

It counters premature closure and single-option railroading: no option is dismissed before its strongest case has been made. The lineage is the legal adversarial system, where truth emerges from the collision of well-argued positions. The namespace-wide rationale lives in [`references/think.md`](../../../references/think.md).

The step-by-step procedure lives in [`SKILL.md`](../SKILL.md); this guide covers when to use the skill and what to expect.

## When to Use

**Use `/think-deliberate` for:**
- Vendor/tool/library selection
- Architectural decisions with multiple valid approaches
- Build vs buy decisions
- Technology stack choices
- Strategic decisions with trade-offs

**Don't use `/think-deliberate` for:**
- Decisions with a clearly correct answer
- Simple preferences (just decide)
- Decisions that only real-world testing can resolve
- Ethical dilemmas (advocacy framing may be inappropriate)
- Generating options you don't have yet (use `/think-brainstorm`)
- Stress-testing a single idea you've already chosen (use `/think-scrutinize`)

**Natural pipeline:** `/think-brainstorm` → `/think-deliberate` → `/think-scrutinize` (generate → choose → stress-test).

## Flow

```
Parse the decision → Fact-finding (with you) → Opening arguments (parallel)
  → Rebuttals (parallel) → Judge's questions ⇄ Pre-judgment disclosure
  → Verdict (or "unable to decide")
```

**Fact-finding is interactive.** Expect a few clarifying questions about constraints, history, non-negotiables, and success criteria before any advocate is spawned. Three to five is typical.

**The judge is not passive.** It probes weak points and, before ruling, discloses which way it is leaning so every advocate gets a final chance to respond. The question-and-disclosure cycle repeats as needed, up to 10 rounds.

Advocates have full tool access for research, and they argue in good faith: no fabricated facts, and genuine weaknesses are conceded when challenged.

## What You Get Back

A **Judgment**:
- **Recommendation**: the winning option
- **Reasoning**: why it wins
- **Trade-offs**: what you give up by not choosing the alternatives
- **Confidence**: high / moderate / low / uncertain, with a brief explanation
- **Key factors**: what most influenced the decision

Or, when the options are genuinely equivalent, critical information is missing, or the choice turns on preferences the judge can't infer, an **Unable to Render Judgment** report: what the deliberation revealed, what the decision hinges on, and "if you value X, choose A; if you value Y, choose B."

## Example Session

```
> /think-deliberate Redis vs Memcached for our session store

[Fact-finding: 3 questions about scale, persistence needs, existing infra]

[Advocate A - Redis]:
Redis offers persistence, data structures beyond key-value,
pub/sub for session events, and Lua scripting...

[Advocate B - Memcached]:
Memcached is simpler, faster for pure key-value at scale,
multi-threaded, and has a smaller operational footprint...

[Rebuttal round]
[Judge's questions about failure modes and operational complexity]
[Pre-judgment disclosure: leaning Redis]
[Final arguments]

## Judgment

**Recommendation:** Redis

**Reasoning:**
Session persistence across restarts outweighs Memcached's
raw throughput advantage at our scale...

**Trade-offs:**
Higher memory overhead, more operational surface area...

**Confidence:** high — persistence requirement is decisive
```
