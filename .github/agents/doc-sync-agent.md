# Documentation Sync Agent Instructions

## Purpose
This agent automatically synchronizes documentation from source repositories in the FalkorDB organization to the docs repository, maintaining up-to-date documentation across the ecosystem.

## Core Responsibilities

### 1. Monitor Source Repositories
The agent monitors the following repositories for documentation changes:
- **FalkorDB** - Main graph database (commands, algorithms, design specs)
- **GraphRAG-SDK** - GenAI GraphRAG SDK
- **QueryWeaver** - Text-to-SQL tool
- **falkordb-py** - Python client library
- **falkordb-ts** - TypeScript client library
- **JFalkorDB** - Java client library
- **NFalkorDB** - .NET client library
- **flex** - JavaScript UDF library
- **falkordb-browser** - Browser visualization tool
- **FalkorDB-MCPServer** - Model Context Protocol server

### 2. Intelligent Content Mapping
The agent maps source documentation to appropriate locations in the docs repository:

| Source Repo | Source Path | Destination Path |
|-------------|-------------|------------------|
| FalkorDB | README.md | getting-started/overview.md |
| FalkorDB | docs/commands/*.md | commands/ |
| FalkorDB | docs/algorithms/*.md | algorithms/ |
| GraphRAG-SDK | README.md, docs/* | genai-tools/GraphRAG-SDK/ |
| QueryWeaver | README.md, docs/* | genai-tools/QueryWeaver/ |
| falkordb-py | README.md, docs/* | getting-started/client-libraries/python/ |
| falkordb-ts | README.md, docs/* | getting-started/client-libraries/typescript/ |
| JFalkorDB | README.md, docs/* | getting-started/client-libraries/java/ |
| NFalkorDB | README.md, docs/* | getting-started/client-libraries/dotnet/ |
| flex | README.md, docs/* | udfs/flex/ |
| falkordb-browser | README.md, docs/* | browser/ |
| FalkorDB-MCPServer | README.md, docs/* | agentic-memory/ |

### 3. Content Processing Rules

#### Jekyll Front Matter
- Add Jekyll front matter if not present
- Extract title from first heading or filename
- Determine appropriate parent page for navigation
- Preserve existing front matter if already present

#### Link Transformation
- Convert relative links to absolute GitHub URLs when necessary
- Maintain internal doc links where appropriate
- Ensure all images and assets are accessible

#### Attribution
- Add source repository attribution footer
- Include link back to original repository
- Mark content as automatically synchronized

### 4. Quality Assurance

#### Pre-PR Validation
- Run Jekyll build to ensure site builds correctly
- Execute spellcheck on modified files
- Verify no broken links introduced

#### Change Detection
- Only create PRs when actual content changes detected
- Skip sync if content is identical to existing
- Group related changes in single PR when possible

### 5. Pull Request Creation

#### PR Metadata
- Title format: `docs: sync documentation from {repo_name}`
- Label with: `documentation`, `automated`, `sync`
- Create as regular PR (not draft) requiring human review

#### PR Description Include
- Source repository and commit information
- Summary of changes made
- Validation results (build, spellcheck)
- Review checklist for human reviewers

### 6. Trigger Mechanisms

#### Real-time (Primary)
- Triggered via `repository_dispatch` event
- Payload includes: repository name, commit SHA, commit message
- Immediate sync when source repo changes

#### Scheduled (Fallback)
- Daily at 2 AM UTC
- Syncs all configured repositories
- Catches any missed real-time events

#### Manual (Testing)
- Triggered via `workflow_dispatch`
- Allows testing specific repository syncs
- Useful for debugging and validation

## Decision-Making Logic

### When to Create a PR
- ✅ Content has changed from existing documentation
- ✅ Jekyll build validation passes
- ✅ Source repository is in configured mappings
- ❌ No actual content changes detected
- ❌ Build validation fails (report error)

### Conflict Resolution
- Human review required for all PRs (no auto-merge)
- Conflicts must be resolved manually
- Agent will not force-push or overwrite manual edits

### Error Handling
- Log errors clearly in workflow output
- Continue processing other files if one fails
- Report summary of successes and failures
- Alert on build or validation failures

## Security Considerations

### Authentication
- Uses default `GITHUB_TOKEN` provided by GitHub Actions
- Read access to source repositories
- Write access to docs repository (content + PRs)
- No external authentication required

### Permissions Required
- `contents: write` - to create branches and commits
- `pull-requests: write` - to create PRs
- `issues: read` - to check existing issues if needed

### Safe Operations
- All changes go through PR review process
- No direct commits to main branch
- Branch protection rules enforced
- Audit trail maintained via PR history

## Maintenance

### Adding New Repositories
1. Add repository mapping to `REPO_MAPPINGS` in sync script
2. Test with manual workflow trigger
3. Configure source repository webhook (if needed)

### Modifying Mappings
1. Update `REPO_MAPPINGS` configuration
2. Test with manual workflow trigger
3. Document changes in this file

### Troubleshooting
- Check workflow run logs for detailed output
- Verify source repository accessibility
- Confirm mapping paths are correct
- Test Jekyll build locally if validation fails

## Human Oversight

This is an **assistant agent**, not an autonomous agent. All changes require:
- ✅ Human review of PR
- ✅ Explicit approval before merge
- ✅ Ability to modify or reject automated changes

The agent provides automation and efficiency while maintaining human control over documentation quality and accuracy.
