# Documentation Sync Integration Template

This template helps source repositories integrate with the FalkorDB docs agentic sync workflow.

## Quick Setup

Add this workflow file to your repository to enable automatic documentation sync.

### File: `.github/workflows/sync-to-docs.yml`

```yaml
name: Sync Documentation to Docs Repo

on:
  push:
    branches:
      - main
      - master
    paths:
      - 'README.md'
      - 'docs/**'
      - '*.md'

  # Allow manual trigger
  workflow_dispatch:

jobs:
  notify-docs-sync:
    runs-on: ubuntu-latest
    steps:
      - name: Notify docs repository
        uses: peter-evans/repository-dispatch@v3
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          repository: FalkorDB/docs
          event-type: docs-sync
          client-payload: |
            {
              "repository": "${{ github.event.repository.name }}",
              "ref": "${{ github.ref_name }}",
              "sha": "${{ github.sha }}",
              "commit_message": "${{ github.event.head_commit.message || 'Manual sync trigger' }}"
            }
```

## Alternative: Using cURL (No Additional Action)

```yaml
name: Sync Documentation to Docs Repo

on:
  push:
    branches:
      - main
      - master
    paths:
      - 'README.md'
      - 'docs/**'

jobs:
  notify-docs-sync:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger docs sync via API
        run: |
          curl -X POST \
            -H "Accept: application/vnd.github+json" \
            -H "Authorization: Bearer ${{ secrets.GITHUB_TOKEN }}" \
            -H "X-GitHub-Api-Version: 2022-11-28" \
            https://api.github.com/repos/FalkorDB/docs/dispatches \
            -d '{
              "event_type": "docs-sync",
              "client_payload": {
                "repository": "${{ github.event.repository.name }}",
                "ref": "${{ github.ref_name }}",
                "sha": "${{ github.sha }}",
                "commit_message": "${{ github.event.head_commit.message }}"
              }
            }'
```

## Configuration Options

### Customize Trigger Paths

Only sync when specific files change:

```yaml
on:
  push:
    branches: [main]
    paths:
      - 'README.md'           # Main readme
      - 'docs/**/*.md'        # Documentation folder
      - 'API.md'              # Specific API docs
      - '!docs/internal/**'   # Exclude internal docs
```

### Add Condition Checks

Only sync if certain conditions are met:

```yaml
jobs:
  notify-docs-sync:
    runs-on: ubuntu-latest
    # Only sync if commit message doesn't contain [skip-docs]
    if: "!contains(github.event.head_commit.message, '[skip-docs]')"
    steps:
      # ... rest of workflow
```

### Include More Metadata

Send additional information to the docs sync workflow:

```yaml
client-payload: |
  {
    "repository": "${{ github.event.repository.name }}",
    "ref": "${{ github.ref_name }}",
    "sha": "${{ github.sha }}",
    "commit_message": "${{ github.event.head_commit.message }}",
    "author": "${{ github.event.head_commit.author.name }}",
    "timestamp": "${{ github.event.head_commit.timestamp }}",
    "modified_files": "${{ toJson(github.event.head_commit.modified) }}"
  }
```

## Testing

### Manual Test

1. Go to **Actions** tab in your repository
2. Select **Sync Documentation to Docs Repo**
3. Click **Run workflow**
4. Check the **Actions** tab in FalkorDB/docs for the triggered sync

### Verify Integration

After pushing a documentation change:
1. Check your repository's Actions tab for successful run
2. Check FalkorDB/docs Actions tab for triggered sync
3. Look for PR created in FalkorDB/docs repository

## Troubleshooting

### Workflow Not Triggering

**Problem:** Push to main branch doesn't trigger sync

**Solutions:**
- Verify file paths match the `paths:` filter
- Check that changes are in tracked files
- Ensure branch name matches (`main` vs `master`)

### Permission Denied

**Problem:** `403 Forbidden` or permission errors

**Solutions:**
- Verify `GITHUB_TOKEN` has correct permissions
- Check workflow permissions in repository settings
- Ensure repository is public or token has access

### Sync Workflow Not Running in Docs Repo

**Problem:** Event sent but docs sync doesn't run

**Solutions:**
- Verify event type is `docs-sync` (exact match)
- Check docs repository workflow file is on main branch
- Review docs repository Actions tab for errors

## Best Practices

### 1. Skip Unnecessary Syncs

Use commit message flags to skip sync:

```bash
git commit -m "Update internal docs [skip-docs]"
```

Then add condition:
```yaml
if: "!contains(github.event.head_commit.message, '[skip-docs]')"
```

### 2. Sync Only on Release

Trigger sync only when creating releases:

```yaml
on:
  release:
    types: [published]
```

### 3. Batch Changes

Instead of syncing every commit, sync on schedule:

```yaml
on:
  schedule:
    - cron: '0 0 * * 1'  # Weekly on Monday
```

### 4. Separate Internal Docs

Exclude internal documentation:

```yaml
paths:
  - 'docs/**'
  - '!docs/internal/**'
  - '!docs/private/**'
```

## Example Repositories

See these repositories for working examples:
- FalkorDB/GraphRAG-SDK
- FalkorDB/falkordb-py
- FalkorDB/falkordb-ts

## Support

Questions? Check the [Sync Workflow Documentation](SYNC_WORKFLOW.md) or open an issue.
