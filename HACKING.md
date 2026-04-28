# Hacking

## Local Development

To install from a local clone, add the following to `~/.claude/settings.json`:

```json
{
  "enabledPlugins": {
    "claude-swe-workflows@claude-swe-workflows": true
  }
}
```

And register the local directory as a marketplace in `~/.claude/plugins/known_marketplaces.json`:

```json
{
  "claude-swe-workflows": {
    "source": {
      "source": "directory",
      "path": "/path/to/claude-swe-workflows"
    },
    "installLocation": "/path/to/claude-swe-workflows",
    "lastUpdated": "2026-01-01T00:00:00.000Z"
  }
}
```

## Cutting a Release

Claude Code plugins are distributed by git ref — consumers pin to a tag or branch and the marketplace files in the repo do the rest. There is no release artifact to publish; "cutting a release" means bumping the manifest versions, updating the changelog, and pushing a tag. The Gitea release row is a human-readable changelog mirror, nothing more. Tags pushed to Gitea propagate to the GitHub mirror automatically; no GitHub release is created or needed.

### Procedure

1. **Pick the version** (SemVer). MAJOR = breaking changes to public skill names or behavior. MINOR = new skills or new non-breaking capabilities. PATCH = bug fixes / docs. Per the Versioning policy in `README.md`, skills are the public interface; agent names are internal.

2. **Prepare the release commit:**
   - Bump `version` in both `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`
   - Update `description` / `keywords` in both manifests if scope has shifted meaningfully
   - Add a `## vX.Y.Z` section to `CHANGELOG.md` covering Breaking Changes, New Skills, and New Agents (see prior entries for the template)
   - Commit as `chore: prepare vX.Y.Z release`

3. **Merge to master.** Fast-forward any release branch into master and push.

4. **Tag and push:**
   ```sh
   git tag vX.Y.Z
   git push origin refs/tags/vX.Y.Z
   ```

5. **Create the Gitea release (via Claude + MCP).** Ask Claude to create the Gitea release using the Gitea MCP server:
   - `tag_name` = the version tag (e.g., `v6.1.0`)
   - `target` = `master`
   - `title` = the version tag
   - `body` = curated release notes (the CHANGELOG entry, or a commit-log summary)

### Gitea auto-release quirk

When a tag is pushed to Gitea, Gitea automatically creates a bare release row for it (tag name only, no title or body). The Gitea MCP's `create_release` sometimes succeeds anyway (appears to use upsert semantics in some cases) and sometimes fails with a UNIQUE constraint error. If it fails, delete the bare release row first via the Gitea MCP's `delete_release`, then retry `create_release`.

There is no `update_release` MCP tool at the time of writing; if one is added, prefer it over delete-then-create.

### Fallback: Claude unavailable

If Claude Code is unavailable and you need to cut a release:

1. Push the tag manually: `git tag vX.Y.Z && git push origin refs/tags/vX.Y.Z`
2. On Gitea, edit the auto-created bare release in the web UI to add a title and notes (or skip — the tag alone is enough for plugin consumers).

Rare path — not optimized for ergonomics, but always available.
