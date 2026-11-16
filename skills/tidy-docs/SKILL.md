---
name: tidy-docs
description: Mechanical documentation hygiene. A doc-maintainer audits all project docs and fixes correctness, completeness, freshness, and consistency issues within its authority; anything needing user judgment is surfaced for approval.
model: opus
---

# Tidy-Docs - Documentation Hygiene

Spawns a `doc-maintainer` agent to comprehensively audit all project documentation and fix the issues it finds. The find→fix seam is small — typos, stale code examples, broken links, freshness drift — so the skill runs as a tidy rather than a review.

## Workflow

### 1. Spawn doc-maintainer agent

Spawn a `DOC - Maintainer` agent with the following prompt:

```
Mode: full audit. Check every doc in the project against the code.
Report per your Report section.
```

### 2. Report results

After the agent completes, present its findings to the user:
- What was reviewed
- What was changed (if anything)
- Items that need a decision (if any)

### 3. Commit (optional)

If changes were made, ask the user if they want to commit. If yes:

```bash
git add [specific files]
git commit -m "$(cat <<'EOF'
docs: tidy project documentation

[Brief description of changes made]
EOF
)"
```
