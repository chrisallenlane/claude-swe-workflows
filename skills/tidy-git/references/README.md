# /tidy-git — Mechanical Repo Hygiene

The step-by-step procedure lives in [`SKILL.md`](../SKILL.md); this guide covers when to use the skill and what to expect.

## Overview

`/tidy-git` cleans up the local git state that piles up over time. It runs zero-risk operations automatically, asks before deleting merged local branches, and reports other state worth knowing about without acting on it: stashes, untracked files, unpushed work, local-only tags.

It's a `/tidy-*` skill because the find → fix seam is small. Detecting a stale remote-tracking ref and removing it is one operation, and a per-item approval step would turn a 5-second cleanup into a 5-minute session. So it **defaults to action** on safe categories and asks only where a preview is genuinely useful.

**Local only.** It never touches remote state: no push, no force-push, no remote deletes. Remote-side cleanup has non-local effects and deserves an explicit decision per action.

## When to Use

**Use `/tidy-git` for:**
- After a merge or release, when feature branches have piled up
- Before a long session, to start from a clean baseline
- Periodic hygiene, whenever `git branch` shows more than you can track

**Don't use it for:**
- Remote cleanup (deleting remote branches or tags). Use the platform UI or `git push --delete`.
- Rewriting history. Use the git commands yourself.
- Removing untracked files or dropping stashes. It reports these but never deletes them. For session trash, use `/pre-compact`, which cleans it up with judgment.

**Rule of thumb:** if the action affects only local refs and is recoverable from the reflog, `/tidy-git` handles it. Anything touching the remote, history, or unrecoverable state, you run yourself.

## Flow

```
detect repo context → zero-risk prunes → inventory
  → preview + confirm merged-branch deletion → delete → summary
```

It aborts if you're not in a repo, or if a rebase, merge, or cherry-pick is in progress. Resolve that first.

## The Three Action Tiers

Every operation falls into exactly one tier.

**Tier 1: zero-risk, runs without asking.** These remove only references, never commits or files.

| Operation                        | What it removes                                                          |
|----------------------------------|--------------------------------------------------------------------------|
| Prune stale remote-tracking refs | Local refs for branches that no longer exist on the remote (each remote) |
| Prune stale worktree refs        | References to worktrees whose directories are already gone               |

**Tier 2: borderline-safe, preview then confirm.** Local branches fully merged into main, excluding main itself, the current branch, and branches checked out in another worktree. You choose delete all (the default), select specific, or keep all. Deletion uses safe `git branch -d`, never `-D`. `-d` runs its own merge check against the branch's upstream (or the current `HEAD`), not against main, so it can refuse a branch the preview listed. If it refuses, the branch is skipped, not forced.

**Tier 3: report only.** The cleanup is judgment-laden or hard to reverse, so the skill never acts.

| Category                    | Why report-only                                                                         |
|-----------------------------|-----------------------------------------------------------------------------------------|
| Stashes                     | A stash is by definition undecided work                                                 |
| Branches with no upstream   | May be intentional local-only work or forgotten branches; you know which                |
| Branches ahead of upstream  | Forgotten pushes — push, abandon, or keep working                                       |
| Branches with upstream gone | Usually squash/rebase-merged and deleted remotely; deleting needs `-D`, never automated |
| Local-only tags             | Often intentional backups (e.g., `pre-rebase-backup-*`)                                 |
| Untracked files             | `git clean` is destructive and context-dependent                                        |

## Safety Guarantees

These are categorical, with no override flags. The skill never:

- Deletes the main branch or the current branch.
- Uses `git branch -D`.
- Runs any operation that affects the remote.
- Drops or clears stashes, deletes tags, or runs `git clean`.
- Runs `git gc` or `git prune` on the object database.

To do any of these, run `git` directly. Typing the command yourself is the safety mechanism.

## Why Squash-Merged Branches Aren't Deleted

Merged-branch detection catches only branches whose tip is reachable from main (plain merges and fast-forwards). Squash- and rebase-merged branches get new SHAs on main, so they're missed. Once their remote branch is deleted and pruned, they show up under "upstream gone." Confirm the work is on main, then delete them yourself with `git branch -D`. The skill deliberately doesn't guess. Tree-matching heuristics produce false positives, and a wrong guess loses unmerged work.

## Recovering a Wrong Delete

Deleted branches stay in the reflog for about 90 days. The summary lists each deleted branch's SHA so you can restore it:

```
git branch <branch-name> <sha>
# or find it:
git reflog | grep <branch-name>
```

## Tips

1. **Run it after every merge to main.** One pass cleans up the stale branch, the pruned remote ref, and the dangling upstream.
2. **"Upstream gone" is your squash-merge signal.** "Ahead of upstream" is your forgotten-push signal.
3. **Keep backup tags until you've verified the operation they guard**, then drop them with `git tag -d`.
4. **Review old stashes yourself** with `git stash list --date=relative` and `git stash show -p stash@{N}`.
5. **Avoid the main-branch prompt.** If `origin/HEAD` isn't set, the skill asks which branch is main. `git remote set-head origin <main-branch-name>` fixes that for future runs.

## Example Session

See [`SKILL.md`](../SKILL.md#example-session) for a full worked example.
