# /pre-compact — Session Housekeeping Before Compaction

## Overview

Compaction replaces the live conversation with a lossy summary. Anything that matters but lives only in the conversation — a decision, an open question, the reason behind a change — is gone afterward unless it was written down somewhere durable.

`/pre-compact` is the last-chance pass before you run `/compact`. It walks a fixed checklist as a floor (persistent memory, git state, scratch files), then uses judgment for whatever the checklist doesn't anticipate, and ends with a go/no-go SBAR and a resume prompt for the post-compaction session.

**It never runs `/compact` itself.** Compaction is your call.

## When to Use

**Use `/pre-compact`:**
- Immediately before `/compact`, whenever the session produced decisions, preferences, or in-flight work worth keeping.
- Before abandoning a long session you might resume later.

**Don't bother when:**
- The session was a one-off question with nothing to carry forward.

## Workflow

```
1. Persistent memory pass   — save user facts, feedback (with its why),
                              project state, references; update rather
                              than duplicate; skip what git or the code
                              already records
2. Git hygiene pass         — surface uncommitted and untracked work and
                              unusual branch state; commit only with your
                              permission
3. Trash cleanup pass       — delete scratch files that are clearly trash
                              and clearly the session's own; ask about
                              anything ambiguous
4. Open audit (judgment)    — undocumented decisions, unanswered questions,
                              background processes, stashes, branches
5. SBAR                     — Situation / Background / Assessment /
                              Recommendation: "Safe to compact",
                              "Safe to compact after X", or
                              "Do not compact yet — Y"
6. Resume prompt            — one copy-pasteable block telling the next
                              session exactly what to do next, or
                              "No resume prompt — work is sealed."
7. Stop                     — waits for you
```

## Design Notes

**Memory is the point.** The memory pass is never skipped or treated as optional; it is why the skill exists.

**Bias toward keeping.** A wrongly deleted file loses your work in progress; a wrongly kept one costs nothing. Anything of uncertain origin is asked about, not deleted.

**The resume prompt is written now, not later.** The post-compaction session sees only the summary. A handoff drafted while the full context is still present is far better than one it could reconstruct — so the skill always emits one, or says explicitly that there is nothing to resume.
