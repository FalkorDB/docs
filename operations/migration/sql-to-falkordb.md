---
title: "SQL Sources to FalkorDB (Online Migration)"
description: "Online migration and incremental sync from SQL sources (MySQL, MariaDB, SQL Server, Databricks, PostgreSQL, Snowflake, ClickHouse) into FalkorDB using DM-SQL-to-FalkorDB loaders and control plane."
parent: "Migration"
nav_order: 5
---

# Online Data Migration from SQL Sources to FalkorDB

The [DM-SQL-to-FalkorDB](https://github.com/FalkorDB/DM-SQL-to-FalkorDB) repository provides Rust-based CLI loaders to perform an initial load from SQL systems into FalkorDB and optionally keep FalkorDB continuously synchronized using incremental watermarks.

It also includes an optional control plane (web UI + REST API) for creating configurations, starting runs, monitoring progress, and viewing persisted metrics snapshots.

## Supported sources

- MySQL
- MariaDB
- SQL Server
- PostgreSQL
- Snowflake
- Databricks (Databricks SQL / warehouses)
- ClickHouse

## When to use this approach

Use these tools when you want:

- A one-time migration from SQL tables into a FalkorDB property graph
- Ongoing one-way sync so FalkorDB stays updated as rows change in the source system

## Prerequisites

- Rust toolchain (Cargo)
- Network access to your SQL source (MySQL, MariaDB, SQL Server, PostgreSQL, Snowflake, Databricks SQL warehouse, or ClickHouse)
- A reachable FalkorDB endpoint (for example `falkor://127.0.0.1:6379`)
- Node.js + npm (optional; only needed for control plane UI)

Most configurations reference environment variables for secrets and credentials, for example: `$MYSQL_URL`, `$MARIADB_URL`, `$SQLSERVER_CONNECTION_STRING`, `$POSTGRES_URL`, `$SNOWFLAKE_PASSWORD`, `$DATABRICKS_TOKEN`, `$CLICKHOUSE_URL`.

## Getting the tools

```bash
git clone https://github.com/FalkorDB/DM-SQL-to-FalkorDB.git
cd DM-SQL-to-FalkorDB
```

## How the loaders work (high level)

Each loader uses JSON/YAML configuration to define:

- How to read rows from the source (`table` + optional filter, or custom `SELECT`)
- How rows map to:
  - Nodes (labels, keys, property mappings)
  - Edges (relationship type, direction, and endpoint matching rules)
- Whether each mapping is full or incremental
- Optional soft-delete behavior
- Where incremental state/watermarks are persisted (typically a file-backed `state.json`)

### Common concepts

- Declarative mapping: you define mappings, and the loader handles extraction + load.
- Idempotent writes: loaders use Cypher `UNWIND` + `MERGE` patterns.
- Incremental safety: watermarks advance only after successful writes.
- Restart safety: after failures, reruns continue from the last successful watermark.

## Option A: Run a loader directly (CLI)

### ClickHouse → FalkorDB

- Docs: [ClickHouse-to-FalkorDB/readme.md](https://github.com/FalkorDB/DM-SQL-to-FalkorDB/tree/main/ClickHouse-to-FalkorDB)

```bash
cd ClickHouse-to-FalkorDB
cargo build --release

# One-shot run
cargo run --release -- --config clickhouse.incremental.yaml

# Continuous sync
cargo run --release -- --config clickhouse.incremental.yaml --daemon --interval-secs 60
```

### Databricks → FalkorDB

- Docs: [Databricks-to-FalkorDB/README.md](https://github.com/FalkorDB/DM-SQL-to-FalkorDB/tree/main/Databricks-to-FalkorDB)

```bash
cd Databricks-to-FalkorDB/databricks-to-falkordb
cargo build --release
cargo run --release -- --config path/to/config.yaml
```

Note: this loader currently supports one-shot execution (no daemon/purge flags in the manifest).

### MariaDB → FalkorDB

- Docs: [MariaDB-to-FalkorDB/readme.md](https://github.com/FalkorDB/DM-SQL-to-FalkorDB/tree/main/MariaDB-to-FalkorDB)

```bash
cd MariaDB-to-FalkorDB
cargo build --release

# One-shot run
cargo run --release -- --config mariadb.incremental.yaml

# Continuous sync
cargo run --release -- --config mariadb.incremental.yaml --daemon --interval-secs 60
```

### MySQL → FalkorDB

- Docs: [MySQL-to-FalkorDB/readme.md](https://github.com/FalkorDB/DM-SQL-to-FalkorDB/tree/main/MySQL-to-FalkorDB)

```bash
cd MySQL-to-FalkorDB
cargo build --release

# One-shot run
cargo run --release -- --config mysql.incremental.yaml

# Continuous sync
cargo run --release -- --config mysql.incremental.yaml --daemon --interval-secs 60
```

### PostgreSQL → FalkorDB

- Docs: [PostgreSQL-to-FalkorDB/README.md](https://github.com/FalkorDB/DM-SQL-to-FalkorDB/tree/main/PostgreSQL-to-FalkorDB)

```bash
cd PostgreSQL-to-FalkorDB/postgres-to-falkordb
cargo build --release

# One-shot run
cargo run --release -- --config path/to/config.yaml

# Continuous sync
cargo run --release -- --config path/to/config.yaml --daemon --interval-secs 60
```

### Snowflake → FalkorDB

- Docs: [Snowflake-to-FalkorDB/README.md](https://github.com/FalkorDB/DM-SQL-to-FalkorDB/tree/main/Snowflake-to-FalkorDB)

```bash
cd Snowflake-to-FalkorDB
cargo build --release

# One-shot run
cargo run --release -- --config path/to/config.yaml

# Continuous sync
cargo run --release -- --config path/to/config.yaml --daemon --interval-secs 300
```

### SQL Server → FalkorDB

- Docs: [SQLServer-to-FalkorDB/readme.md](https://github.com/FalkorDB/DM-SQL-to-FalkorDB/tree/main/SQLServer-to-FalkorDB)

```bash
cd SQLServer-to-FalkorDB
cargo build --release

# One-shot run
cargo run --release -- --config sqlserver.incremental.yaml

# Continuous sync
cargo run --release -- --config sqlserver.incremental.yaml --daemon --interval-secs 60
```

Optional purge modes (supported by ClickHouse, MariaDB, MySQL, Snowflake, and SQL Server):

```bash
# Purge full graph before loading
cargo run --release -- --config path/to/config.yaml --purge-graph

# Purge selected mappings
cargo run --release -- --config path/to/config.yaml --purge-mapping customers
```

## Option B: Use the control plane (web UI + API)

The control plane discovers tools by scanning for `tool.manifest.json` files and provides a UI/API to:

- Create and edit per-tool YAML/JSON configurations
- Start runs (one-shot or daemon where supported)
- Stop running jobs
- Stream logs live (SSE)
- Store run history and artifacts (SQLite + file-backed data directory)
- Auto-wire tool metrics ports for metrics-capable tools
- Persist per-tool/per-mapping metrics snapshots

Start the server:

```bash
cd control-plane/server

# Optional: require API key on /api (except /api/health)
export CONTROL_PLANE_API_KEY="..."

cargo run --release
```

Default server URL: `http://localhost:3003`

Configuration (environment variables):

- `CONTROL_PLANE_BIND` (default `0.0.0.0:3003`)
- `CONTROL_PLANE_REPO_ROOT` (optional; repository root for manifest scan)
- `CONTROL_PLANE_DATA_DIR` (default `control-plane/data/`)
- `CONTROL_PLANE_UI_DIST` (default `control-plane/ui/dist/`)
- `CONTROL_PLANE_API_KEY` (optional bearer token requirement)

Selected metrics API endpoints:

- `GET /api/metrics`
- `GET /api/metrics/:tool_id`

Notes:

- Runs execute locally on the machine hosting the control plane server.
- Log streaming uses SSE.
- For `supports_metrics: true` tools, the control plane injects `--metrics-port` and persists snapshots in SQLite.
- The Metrics UI uses persisted snapshots and does not expose internal scrape endpoint/port settings.

UI development (optional):

```bash
cd control-plane/ui
npm install
npm run dev
```

**Screenshots:**
The main tools menu with migration selection options.
<img width="1403" height="832" alt="DM-UI-7-tools" src="https://github.com/user-attachments/assets/e0100f17-caa0-495c-8914-e4a38ab44fc9" />

The following example shows how you manually execute a migration run, with visibility to the latest incremental watermark, and an option to clear it to restart incremental migration from scratch.
<img width="1422" height="861" alt="DM-UI--screenshot" src="https://github.com/user-attachments/assets/0c622f06-7b03-454c-a693-cd302d057343" />

The following example shows the log view after a successful run.
<img width="1422" height="861" alt="DM-UI--logs" src="https://github.com/user-attachments/assets/e0b2c286-b857-44d4-887d-3aa3664744b9" />

THe following shows the metrics view summarizing a run:
<img width="1403" height="832" alt="DM-UI--metrics" src="https://github.com/user-attachments/assets/af09d6ff-c1ed-4148-b1ab-6fa2500887dc" />

## Metrics feature (all SQL loaders)

All current SQL loaders expose Prometheus-style metrics with:

- Global counters:
  - total runs
  - failed runs
  - rows fetched
  - rows written
  - rows deleted
- Per-mapping counters:
  - runs
  - failed runs
  - rows fetched
  - rows written
  - rows deleted

Default metrics ports:

- ClickHouse: `9991`
- Snowflake: `9992`
- PostgreSQL: `9993`
- Databricks: `9994`
- MySQL: `9995`
- SQL Server: `9996`
- MariaDB: `9997`

You can override ports with `--metrics-port` (or each tool's corresponding environment variable).

## Operational tips

- Define node mappings before edge mappings (edges depend on nodes).
- Choose stable keys for `MERGE` (primary keys are usually best).
- Use `RUST_LOG=info` (or `debug`) for richer loader diagnostics.
- Keep state and control-plane data on durable storage for long-running sync setups.

## Additional resources

- DM-SQL-to-FalkorDB repository: https://github.com/FalkorDB/DM-SQL-to-FalkorDB
- FalkorDB docs: https://docs.falkordb.com/
