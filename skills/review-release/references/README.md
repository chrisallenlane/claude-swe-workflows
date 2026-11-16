# /review-release - Pre-Release Readiness Check

The step-by-step procedure lives in [`SKILL.md`](../SKILL.md); this guide covers when to use the skill and what to expect.

## Overview

`/review-release` is a pre-flight check before cutting a release. A scanner agent does the static analysis, the skill runs the tests, the build, and a doc-freshness check, and every finding lands in one consolidated report for you to review.

Why it's shaped this way:

- **Surface issues, don't silently fix them.** A release is a commitment to users, so every issue gets human review. The only fixes offered are mechanical (removing debug statements and work markers, bumping manifest versions), and only for items you select.
- **Run everything, then report.** All checks run without mid-scan pauses, so you decide with the full picture.
- **Err toward reporting.** A false positive costs seconds; a missed issue ships to users.

```
Release context ──▶ Static scan ──▶ Tests ──▶ Build ──▶ Doc freshness ──▶ Report
               ──▶ (your selection) Fixes ──▶ Re-verify ──▶ Summary + recommendation
```

## When to Use

**Use `/review-release` for:**
- Checking whether a codebase is ready for distribution, without committing to cut yet
- A standalone audit that catches what development workflows don't focus on
- Checking readiness ahead of a planned release window

**Don't use `/review-release` for:**
- Cutting the release: use [`/release`](../../release/references/README.md), which always runs `/review-release` as preflight. Running this manually and then `/release` doubles the same check.
- Test quality: `/review-test` or `/test-mutation`
- Updating docs: `/tidy-docs` (this skill only flags staleness)
- Security audits: `/review-security` (this skill checks only for tracked secrets and debug artifacts)

**`/review-release` vs `/release`:** they sit on opposite sides of the check/act seam. `/review-release` tells you whether the release is ready; `/release` actually cuts it. If you intend to ship, go straight to `/release`.

## What It Checks

| Check                   | What it looks for                                                | Severity |
|-------------------------|------------------------------------------------------------------|----------|
| **Debug artifacts**     | console.log, print(), breakpoint(), debugger statements          | BLOCKER  |
| **Work markers**        | TODO, FIXME, HACK, XXX, REMOVEME                                 | WARNING  |
| **Hardcoded URLs**      | localhost, 127.0.0.1 in production code                          | WARNING  |
| **Version consistency** | Mismatched versions across manifests (source constants: WARNING) | BLOCKER  |
| **Changelog coverage**  | Changelog not updated since last tag                             | WARNING  |
| **Git hygiene**         | Merge conflict markers, tracked secrets                          | BLOCKER  |
| **Working tree**        | Uncommitted changes, large binaries outside Git LFS              | WARNING  |
| **Breaking changes**    | Removed public API without changelog mention                     | BLOCKER  |
| **License compliance**  | New copyleft or unknown-license deps (human review)              | WARNING  |
| **Test suite**          | Test failures                                                    | BLOCKER  |
| **Build verification**  | Build failures                                                   | BLOCKER  |
| **Doc freshness**       | Documentation referencing removed/renamed code                   | WARNING  |

## What You'll Be Asked

- **What version are you releasing?** Optional. With a target, every version is checked against it; without one, the skill still checks that discovered versions agree. Run standalone, the manifests are expected to carry the target already. Under `/release`, which bumps after the preflight, manifests still at the previous version are reported as INFO.
- **Any checks to skip?** Run everything (recommended), or skip build verification, doc freshness, or license compliance.
- **Which items to address,** after the report: specific numbers, "all blockers", "all warnings", or "all".
- **Whether to commit,** if any fixes were made.

## What You Get Back

1. **A readiness report:** findings numbered BLOCKERS → WARNINGS, then what passed.
2. **Fixes for the items you select,** where they're mechanical. Everything else is report-only with a pointer: merge conflicts need manual resolution, test and build failures need investigation, changelog gaps get an offered scaffold from git history, license and breaking-change calls are yours, and stale docs point to `/tidy-docs`.
3. **A final summary** with what was resolved, what changed, what remains, and a recommendation:
   - **HOLD:** any unresolved BLOCKER
   - **PROCEED WITH CAUTION:** only WARNINGs remain
   - **READY TO RELEASE:** nothing remains

When a caller asks for report-only (as `/review-repo`'s follow-up does), the skill stops after the report and recommendation: no fixes, no commit.

## Example — Issues Found

```
User: /review-release

What version?
> 2.0.0

## Release Readiness Report

Last tag: v1.9.2 → Target: v2.0.0
89 commits, 42 files changed

### BLOCKERS (3)
1. [DEBUG] src/api/handler.go:15 — debug statement
2. [VERSION] Not bumped to 2.0.0
3. [BREAKING] ParseConfig() removed, not in changelog

### WARNINGS (3)
4. [CHANGELOG] Not updated
5. [DEBUG] TODO markers in 2 files
6. [DOCS] README references removed function

Select items to address:
> 1, 2, 5

[Fixes applied]

## Release Review Complete
- BLOCKERS resolved: 2/3
- WARNINGS addressed: 1/3
- Recommendation: HOLD — undocumented breaking change remains
```

## Tips

1. **Start from a clean state.** Run it on a ready release branch, and fix obvious blockers (merge conflicts, tracked secrets) first to keep the report focused.
2. **Provide the target version.** It turns "do the versions agree?" into "are they all the right version?"
3. **Write the changelog yourself.** The skill can scaffold entries from git history, but meaningful release notes need human authorship.
4. **Run it periodically, not just at release time.** Issues are cheaper to fix early.
5. **Don't ignore warnings.** PROCEED WITH CAUTION means making a conscious decision about each one.
