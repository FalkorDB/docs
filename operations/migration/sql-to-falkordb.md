---
title: "SQL Sources to FalkorDB (Online Migration)"
description: "Online migration and incremental sync from SQL sources (PostgreSQL, Snowflake, Databricks) into FalkorDB using DM-SQL-to-FalkorDB loaders and control plane."
parent: "Migration"
nav_order: 5
---

# Online Data Migration from SQL Sources to FalkorDB

The [DM-SQL-to-FalkorDB](https://github.com/FalkorDB/DM-SQL-to-FalkorDB) repository provides Rust-based CLI tools to **perform an initial load** of data from SQL systems into FalkorDB and optionally keep it **continuously synchronized** (one-way sync) using **incremental watermarks**.

It also includes an optional **control plane** (web UI + REST API) for creating configurations, starting runs, and monitoring progress.

## Supported sources

- PostgreSQL
- Snowflake
- Databricks (Databricks SQL / warehouses)

## When to use this approach

Use these tools when you want:

- A one-time migration from SQL tables into a FalkorDB property graph
- **Ongoing sync** ("online migration") where FalkorDB stays updated as rows change in the source system

## Prerequisites

- Rust toolchain (Cargo)
- Network access to your SQL source
- A reachable FalkorDB endpoint (for example `falkor://127.0.0.1:6379`)
- Node.js + npm (optional; only needed for control plane UI development)

Most configurations reference environment variables for credentials/secrets (for example `$POSTGRES_URL`, `$DATABRICKS_TOKEN`, etc.).

## Getting the tools

```bash
git clone https://github.com/FalkorDB/DM-SQL-to-FalkorDB.git
cd DM-SQL-to-FalkorDB
```

## How the loaders work (high level)

Each loader uses a JSON/YAML configuration to define:

- How to read rows from the source system (table + optional filter, or a custom SELECT)
- How rows map to:
  - **Nodes** (labels, key properties, property mappings)
  - **Edges** (relationship type, direction, how to match `from` and `to` nodes)
- Whether a mapping is:
  - **full** (load everything every time)
  - **incremental** (load only changed rows using a watermark column such as `updated_at`)
- How to interpret optional **soft delete flags**
- Where to persist incremental sync **state** (typically a local `state.json` file)

### Common concepts

- **Declarative mapping**: you describe the mapping; the tool handles extraction + loading.
- **Idempotent upsert operations**: writes use Cypher `UNWIND` + `MERGE` based on configured keys.
- **Incremental watermarks**: for incremental mappings, the loader fetches only rows newer than the last successful run.
- **State safety**: watermarks are advanced after successful writes; if a run fails, the next run retries from the previous watermark.

## Option A: Run a loader directly (CLI)

### PostgreSQL → FalkorDB

- Tool docs: [PostgreSQL-to-FalkorDB/README.md](https://github.com/FalkorDB/DM-SQL-to-FalkorDB/tree/main/PostgreSQL-to-FalkorDB)

Build and run (from the crate directory):

```bash
cd PostgreSQL-to-FalkorDB/postgres-to-falkordb
cargo build --release

# One-shot run
cargo run --release -- --config path/to/config.yaml
```

Continuous sync (daemon mode):

```bash
cargo run --release -- --config path/to/config.yaml --daemon --interval-secs 60
```

### Snowflake → FalkorDB

- Tool docs: [Snowflake-to-FalkorDB/README.md](https://github.com/FalkorDB/DM-SQL-to-FalkorDB/tree/main/Snowflake-to-FalkorDB)

```bash
cd Snowflake-to-FalkorDB
cargo build --release

# One-shot run
cargo run --release -- --config path/to/config.yaml

# Continuous sync
cargo run --release -- --config path/to/config.yaml --daemon --interval-secs 300
```

### Databricks → FalkorDB

- Tool docs: [Databricks-to-FalkorDB/README.md](https://github.com/FalkorDB/DM-SQL-to-FalkorDB/tree/main/Databricks-to-FalkorDB)

```bash
cd Databricks-to-FalkorDB/databricks-to-falkordb
cargo build --release
cargo run --release -- --config path/to/config.yaml
```

## Option B: Use the control plane (web UI + API)

The control plane discovers tools in the repository by scanning for `tool.manifest.json` files and provides a UI to:

- Create and edit per-tool configs (YAML/JSON)
- Start runs (one-shot or daemon)
- Stream logs via Server-Sent Events (SSE)
- Keep run history and state in a local data directory (SQLite + file-backed artifacts)

Start the server:

```bash
cd control-plane/server

# Optional: require an API key for all /api routes (except /api/health)
export CONTROL_PLANE_API_KEY="..."

cargo run --release
# UI (if built) + API will be on http://localhost:3003
```

Configuration (environment variables):

- `CONTROL_PLANE_BIND` (default: `0.0.0.0:3003`)
- `CONTROL_PLANE_REPO_ROOT` (optional; repository root to scan for `tool.manifest.json`)
- `CONTROL_PLANE_DATA_DIR` (default: `control-plane/data/`)
- `CONTROL_PLANE_UI_DIST` (default: `control-plane/ui/dist/`; if missing, the API still works)
- `CONTROL_PLANE_API_KEY` (optional; if set, API calls must include `Authorization: Bearer <key>`)

Notes:

- Runs are executed locally on the machine running the control plane server (it spawns the underlying CLI tools).
- The run log endpoint uses Server-Sent Events (SSE).

UI development (optional):

```bash
cd control-plane/ui
npm install
npm run dev
```
Screenshots:
The following example shows how you manually execute a migration run, with visibility to the latest incremental watermark, and an option to clear it to restart incremental migration from scratch.
<img width="1422" height="861" alt="DM-UI--screenshot" src="https://github.com/user-attachments/assets/0c622f06-7b03-454c-a693-cd302d057343" />

The following example shows the log view after successful run.
<img width="1422" height="861" alt="DM-UI--logs" src="https://github.com/user-attachments/assets/e0b2c286-b857-44d4-887d-3aa3664744b9" />


## Operational tips

- Define **node mappings before edge mappings** (edges reference node mappings).
- Pick **stable keys** for `MERGE` (primary keys are usually ideal).
- Run with `RUST_LOG=info` (or `debug`) to get more detailed loader logs.
- Keep the state file/data directory somewhere durable if you rely on continuous sync.

## Additional resources

- DM-SQL-to-FalkorDB repository: https://github.com/FalkorDB/DM-SQL-to-FalkorDB
- FalkorDB docs: https://docs.falkordb.com/
