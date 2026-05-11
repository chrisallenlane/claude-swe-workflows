# Issue Tracker Detection and Operations

Shared convention for detecting the project's issue tracker and operating against it. Cited by skills that read, create, comment on, or close tickets — including `/scope`, `/scope-project`, `/implement`, `/implement-batch`, `/implement-project`, and `/bug-fix`.

## Detection Procedure

Check sources in this order. Stop at the first one that yields a usable answer.

1. **Explicit specification in repo config.** Look for tracker preference and integration method in `CLAUDE.md` first, then `README.md`. The user often pins the tracker explicitly when it isn't inferable from the remote (e.g., self-hosted Gitea with a generic git remote URL).
2. **Git remote URL.** Run `git remote -v` and inspect the URL. Use the platform-to-tool map below.
3. **Confirm the integration is actually available.** A platform match is not the same as a working integration. Verify the relevant CLI/MCP tool responds before issuing real calls.

If no usable integration is found, fall back to the "Manual fallback" section.

## Platform → Tool Mapping

| Platform | Detection signal                              | Preferred integration            | Fallback                       |
|----------|-----------------------------------------------|----------------------------------|--------------------------------|
| GitHub   | `github.com` in remote URL                    | `gh` CLI                         | GitHub REST API                |
| Gitea    | Self-hosted git or generic; check `CLAUDE.md` | `mcp__gitea__*` MCP tools        | Gitea REST API                 |
| GitLab   | `gitlab.com` or self-hosted GitLab            | `glab` CLI                       | GitLab REST API                |
| Other    | Anything else                                 | None (fall through)              | Manual fallback section below  |

**Andon cord** if the tracker matches a known platform but the integration is unavailable (CLI missing, MCP server down, API credentials absent). Surface the proposed ticket operation in the handoff so the operator can either fix the integration or take the action manually.

## Operations

### Fetch (read)

When fetching tickets for a skill that consumes them (`/implement-batch`, `/implement-project`):

- Title
- Description / body
- Acceptance criteria (if explicitly present as a section or list)
- Labels / tags
- Dependencies — referenced issues, "depends on" / "blocks" / "blocked by" links

Fetch each ticket individually rather than relying on a search payload — search results are often truncated and miss the full body.

### Create

For `/scope` and `/scope-project`:

- Pass `title` and `body` to the integration.
- Apply default labels if specified in `CLAUDE.md` (e.g., `bug`, `arch`, batch tags).
- Capture and present the resulting URL and issue number.
- When creating multiple related tickets, create them sequentially within a dependency group so later tickets can reference earlier ones by number.

### Comment / update (close-out)

For `/implement` and `/bug-fix` after merging:

- **Determine ticket number** in this order:
  1. Extract from current branch name (e.g., `feature/123-add-auth` → `#123`, `fix/456-pagination` → `#456`).
  2. Scan commit messages on the branch for `Fixes #N`, `Closes #N`, or `#N` references.
  3. Ask the user if the skill knows a ticket exists but the number isn't recoverable.

- **Ask the user** what to do with the identified ticket: "Update only", "Update and close", or "Skip". Do not auto-close — closing is a one-way signal to other humans.

- **Update content** should summarize what shipped:
  - Files changed (terse list)
  - Key changes / root cause (for `/bug-fix`)
  - Tests added
  - Documentation updated

### Close

Close the ticket via the integration after posting the final comment. Do not delete tickets — closing preserves history.

## Manual Fallback

When no integration is available for the detected platform:

- For **create** operations: output the ticket title and body to the user and instruct them to paste into the tracker. Do not pretend the operation succeeded.
- For **read** operations: andon-cord. The skill cannot proceed without the ticket data.
- For **comment / close** operations: surface the intended comment and ticket number to the user and let them apply it manually.

## What This Doc Does NOT Cover

- Ticket *content* conventions — those belong with the skill that creates the ticket (e.g., `/scope`'s ticket schema, `/bug-fix`'s root-cause section).
- Branch-to-ticket linkage conventions — those belong with the skill that creates the branch.
- Commit-message conventions (`Fixes #N` etc.) — those are per-skill, since `/refactor` uses `refactor:` prefix and `/implement` uses `Fixes #N`.
