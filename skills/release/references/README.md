# /release — Cut a Project Release

The step-by-step procedure lives in [`SKILL.md`](../SKILL.md); this guide covers when to use the skill and what to expect.

## Overview

`/release` executes the project's own release procedure with safety guards suited to a high-blast-radius operation. It discovers the procedure from the project (Makefile target, RELEASING.md, package scripts, CI workflow, git tag history) rather than imposing one, always runs `/review-release` as preflight, and presents an exact command plan before running anything.

It is shaped by three convictions:

- **High blast radius warrants high friction.** Nothing is pushed without two confirmations: the plan, and the local → remote boundary.
- **Discover, don't dictate.** Release procedures differ (goreleaser, `npm publish`, `cargo publish`, `twine upload`, `make release`). Executable sources beat prose, and prose beats inference from tag history. If nothing is found, the skill asks you to describe the steps and offers to record them (a Makefile target is recommended) so the next release needs no description.
- **Halt, don't roll back.** Release sequences aren't atomic. A wrong rollback is worse than none: a transient push failure followed by an automatic re-tag can produce a different SHA. On failure the skill stops, reports exactly what completed, and leaves the decision to you.

`/review-release` is advisory (is the release ready?); `/release` is the mutator (cut it). `/release` runs `/review-release` internally, so don't run them in sequence by hand.

## When to Use

**Use `/release` for:**
- Cutting a new release (patch, minor, major, pre-release) once the work is merged.
- Re-attempting a release that halted midway. The skill detects artifacts from the prior run (local or remote tag, GitHub release, registry publication) and offers to resume.

**Don't use `/release` for:**
- Checking readiness only. Use `/review-release`.
- Rolling back a published release. That is human-judgment territory.
- Shipping past a preflight BLOCKER. There is no bypass. If the BLOCKER is a false positive, fix `/review-release`; otherwise fix the issue.

## Flow

```
detect repo context → discover procedure (offer capture if missing)
  → choose version → check for prior partial run → /review-release preflight
  → build plan → confirm → execute local steps
  → confirm at local→remote boundary → execute remote steps → summary
```

## What It Asks You

- **Intent, if you're not on the main branch.** Backport release lines are valid; the skill confirms instead of aborting.
- **The release steps, if none are discoverable**, and where to record them (Makefile target, RELEASING.md, CLAUDE.md, or skip). The recording lands as its own commit before the release.
- **The target version.** It proposes a semver bump from the CHANGELOG and conventional-commit markers. With no CHANGELOG, it simply asks.
- **Resume, abort, or a different version**, if a prior partial run is detected.
- **Proceed or stop** on the full plan. There is no inline editing. To change the steps, change the procedure source and re-run.
- **Final confirmation at the local → remote boundary.** This is the only pause during execution, and your last cheap off-ramp.

## Reversibility Tiers

Each plan step is labeled with one of four tiers:

| Tier                      | Examples                                   | How to undo                                                     |
|---------------------------|--------------------------------------------|-----------------------------------------------------------------|
| `reversible`              | Manifest and CHANGELOG edits pre-commit    | `git checkout -- <file>`                                        |
| `reversible-locally`      | Local commit, local tag                    | `git reset --hard HEAD~1`, `git tag -d <name>`                  |
| `irreversible-on-publish` | `git push`, `npm publish`, `cargo publish` | Effectively permanent once fetched; registries yank, not delete |
| `partially-reversible`    | `gh release create`                        | Deletable, but notifications have already gone out              |

The version bump covers every manifest that carries the version. Watch for projects with more than one. In a Claude Code plugin, both `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` must agree.

## Safety Guarantees

These are categorical, with no override flags. The skill never:

- Releases from a dirty working tree, or from a branch behind origin.
- Skips the `/review-release` preflight or pushes past one of its BLOCKERs. WARNINGs are carried into the plan, not blocking.
- Force-pushes.
- Skips the local → remote boundary confirmation, or bundles bump, commit, tag, and push into one unpausable operation.
- Attempts automatic rollback of a partial release.

If you need to bypass any of these, run the underlying commands yourself. Having to type them out is the safety mechanism.

## Tips

1. **Read the plan.** It is the high-leverage decision point. The reversibility labels tell you what's at stake on each line.
2. **Treat the boundary as the last off-ramp.** Before it, `git reset` undoes everything. Inspect `git log` / `git show <tag>` there if anything looks off.
3. **On a halt, fix the cause and re-run.** The prior-run detection makes resuming safe. Abandoning (`git tag -d <tag>`, `git reset --hard HEAD~1`) is rarely necessary.
4. **Capture the procedure on the first run.** A `make release` target serves humans and future runs alike.

## Example: Halted Release

A push fails on authentication after the local steps complete. The summary reads, in part:

```
## Release Halted: v1.3.0

### Completed
  3. Committed: "chore: release v1.3.0" (sha 7a8b9c0) — local only
  4. Tagged v1.3.0 — local only

### Failed
  Step 5: git push origin main
  Error: permission denied (publickey)

### Recovery options
  - Fix push authentication and re-run /release; it will offer to resume
    from the push.
  - Or abandon: git tag -d v1.3.0 && git reset --hard HEAD~1
```

When `gh` is unavailable, the GitHub-release step is dropped from the plan with a note, and you create the release by hand.
