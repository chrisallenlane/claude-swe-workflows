# /pre-compact — Session Housekeeping Before Compaction

The step-by-step procedure lives in [`SKILL.md`](../SKILL.md); this guide covers when to use the skill and what to expect.

## Overview

Compaction replaces the live conversation with a lossy summary. Anything that matters but lives only in the conversation is gone afterward unless it was written down somewhere durable. That includes decisions, open questions, and the reasons behind changes.

`/pre-compact` is the last-chance pass before you run `/compact`. It walks a fixed checklist as a floor: persistent memory, git state, and scratch files. Then it uses judgment for whatever the checklist doesn't anticipate. It ends with a go/no-go SBAR and a resume prompt for the post-compaction session.

## When to Use

**Use `/pre-compact`:**
- Immediately before `/compact`, whenever the session produced decisions, preferences, or in-flight work worth keeping.
- Before abandoning a long session you might resume later.

**Don't bother when:**
- The session was a one-off question with nothing to carry forward.

**vs. `/tidy-git`:** `/tidy-git` is mechanical repo hygiene (stale refs, merged branches) and never deletes untracked files. `/pre-compact` judges which of this session's scratch files are trash.

## Flow

```
memory → git hygiene → trash cleanup → open audit → SBAR → resume prompt → stop
```

## What to Expect

- **Memory is always updated.** It's the reason the skill exists, so the pass is never skipped.
- **Nothing is committed without your permission.** Uncommitted and untracked work is surfaced, and you're asked before any commit.
- **Only clear trash is deleted.** That means scratch files that are clearly throwaway and clearly the session's own. Anything ambiguous is asked about, and files that aren't the session's are left alone. A wrongly deleted file loses your work, while a wrongly kept one costs nothing.
- **The SBAR ends in one of three verdicts:** "Safe to compact", "Safe to compact after X", or "Do not compact yet — Y".
- **A resume prompt is always emitted**, or the explicit line "No resume prompt — work is sealed." The prompt is written now because the post-compaction session sees only the summary, and a handoff drafted with full context is far better than one reconstructed from it. It's a single copy-pasteable block naming one concrete next action.
- **It never runs `/compact` itself** and starts no new work. It stops and waits for you.
