# Lead-* Startup Protocol

This document codifies the startup procedure shared by the `/lead-*` orchestrator-family skills (`/lead-project`, `/lead-bug-hunt`, `/lead-refactor`, `/lead-review`). Each `/lead-*` SKILL.md cites this document and supplies only its skill-specific values: branch-name pattern, state-doc filename, the semantics of "Resume as-is," and any bespoke push-back examples during intent elicitation.

The protocol is fixed across the family. The operator experience depends on uniformity — one `/lead-*` skill should feel like the others at startup.

## 0a. Branch and working-tree check

- Identify the main branch (`main` or `master`).
- If currently on `main`/`master`: create the skill's working branch from current HEAD and check it out. Confirm the branch name with the operator before creating. The branch-name pattern is skill-specific (e.g., `lead-bug-hunt/<date>`, `lead-refactor/<date>`, `lead-review/<date>`, `lead-project/<descriptive-name>`).
- Check working tree status:
  - Clean → proceed.
  - Dirty → **ask the operator** how to handle uncommitted work: commit as-is, stash, discard, or abort. Do not guess.

## 0b. Resume existing run or start fresh

Check for the skill's state document at the repo root (e.g., `LEAD_BUG_HUNT_STATE.md`, `LEAD_REFACTOR_STATE.md`):

- **If absent:** proceed to intent elicitation (0c).
- **If present:** read it. Verify the recorded branch still exists, is currently checked out, and the current HEAD matches `Last cycle HEAD` from the state doc.
  - **HEAD matches and branch is current** — summarize the current phase/cycle, pinned intent, and last action to the operator. Offer three options:
    1. **Resume** as-is. The semantic of "as-is" depends on the skill (re-run the most recent loop step, re-verify the current phase, continue from the next enabled sub-skill, etc.) — the skill states it explicitly in the offer.
    2. **Resume with updated intent** — re-elicit, preserving the cycle log.
    3. **Start fresh** — archive the existing state doc to `<STATE_FILENAME>.<timestamp>.md` and re-elicit intent.
  - **HEAD has moved or branch has changed** — do NOT auto-resume. Pull the andon cord with a handoff explaining the divergence and let the operator decide.

## 0c. Elicit commander's intent

The intent schema is skill-specific — see [`autonomy.md`](autonomy.md) § "Commander's-intent schemas per skill" for the per-skill field list.

The framing for elicitation is shared:

- **Walk the operator through each field, one at a time.** Do not accept a single free-form paragraph — the structure is load-bearing.
- **Push back on vague answers.** "Find all the bugs" is not a scope. "Whatever severity" is not a floor. "Make it better" is not a purpose. Propose sharper phrasings and ask the operator to confirm or refine. Several rounds of dialogue is normal — do not rush.
- **Read back the complete intent statement** and ask for confirmation before proceeding to 0d.

This is the primary human-interaction point for the run. Invest the time. Implicit assumptions surface later as granular escalations; explicit intent prevents them.

## 0d. Seed the state doc

Create the state document at the repo root. Top-matter is uniform across the family:

```markdown
# <Skill name> State

Started: <timestamp>
Branch: <branch-name>
Branch SHA at startup: <short SHA>
Base branch: <main-branch>
Base SHA at startup: <short SHA>
Last cycle HEAD: <short SHA>
Current phase: <skill-specific value>   (or "Cycle: N" for cycle-oriented skills)
Status: <active | paused-on-andon | complete>

## Commander's Intent

[Pinned intent, verbatim, one heading per field per the skill's schema]

## Cycle log

[Skill-specific structure — entries per cycle or per phase]

## Findings ledger

[Optional, skill-specific]

## Andon cord history

[Empty at startup]

## Open questions

[Empty at startup]
```

Skills add sections below the shared top-matter for their bespoke state (trajectory audits, review-invocation log, deferred items, phase-specific subsections, etc.).

**Gitignore the state doc.** Add the state-doc filename to `.gitignore` if not already present. Commit the `.gitignore` change separately on the working branch.

## Updates during the run

- Update the state doc at every phase transition (or cycle transition, depending on skill shape).
- Maintain `Last cycle HEAD` after every commit on the working branch — the resume protocol in 0b depends on it.
- Pin commander's intent verbatim and do not modify it mid-run. If the operator wants to modify, that's a 0b option-2 path on a subsequent invocation, not a mid-run mutation.
