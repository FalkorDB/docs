[![Workflow](https://github.com/FalkorDB/docs/actions/workflows/pages/pages-build-deployment/badge.svg?branch=main)](https://github.com/FalkorDB/docs/actions/workflows/pages/pages-build-deployment)
[![Sync](https://github.com/FalkorDB/docs/actions/workflows/sync-docs-agentic.yml/badge.svg)](https://github.com/FalkorDB/docs/actions/workflows/sync-docs-agentic.yml)
[![Discord](https://img.shields.io/discord/1146782921294884966?style=flat-square)](https://discord.gg/ErBEqN9E)
[![Try Free](https://img.shields.io/badge/Try%20Free-FalkorDB%20Cloud-FF8101?labelColor=FDE900&style=flat-square)](https://app.falkordb.cloud)

[![Trendshift](https://trendshift.io/api/badge/repositories/14787)](https://trendshift.io/repositories/14787)

# https://docs.falkordb.com

> **📚 Official documentation for FalkorDB** - The fastest graph database, powered by GraphBLAS

## 🔄 Automated Documentation Sync

This repository uses an **Agentic Workflow** to automatically sync documentation from FalkorDB repositories. When documentation is updated in source repositories, a PR is automatically created here to keep the docs in sync.

**Monitored Repositories:**
- FalkorDB (core database)
- GraphRAG-SDK, QueryWeaver (GenAI tools)
- falkordb-py, falkordb-ts, JFalkorDB, NFalkorDB (client libraries)
- flex (UDF library), falkordb-browser (visualization)
- FalkorDB-MCPServer (agentic integrations)

📖 **Learn more:** [Sync Workflow Documentation](.github/SYNC_WORKFLOW.md)

## 🏗️ Development

### Build

```bash
bundle install
bundle exec jekyll build
```

### Run

```bash
bundle exec jekyll serve
```

## 📝 Contributing

Documentation contributions are welcome! You can either:
- **Edit directly**: Make changes via PR to this repository
- **Update source**: Modify docs in the source repository (automatically synced)

See [SYNC_WORKFLOW.md](.github/SYNC_WORKFLOW.md) for details on the automated sync process.

## 📄 License

See [References/license.md](References/license.md) for licensing information.
