---
title: "SQL Sources to FalkorDB (Online Migration)"
description: "Online migration and incremental sync from SQL sources (BigQuery, ClickHouse, Databricks, MariaDB, MySQL, PostgreSQL, Snowflake, Spark SQL, SQL Server) into FalkorDB using DM-SQL-to-FalkorDB loaders and control plane."
parent: "Migration"
nav_order: 5
---

# Online Data Migration from SQL Sources to FalkorDB

The [DM-SQL-to-FalkorDB](https://github.com/FalkorDB/DM-SQL-to-FalkorDB) repository provides Rust-based CLI loaders for initial load and ongoing sync from SQL sources into FalkorDB.

It also includes an optional control plane (web UI + REST API) for config authoring, schema/template scaffolding, run orchestration, state management, and persisted metrics/log history.

## Supported sources

- BigQuery
- ClickHouse
- Databricks (Databricks SQL / warehouses)
- MariaDB
- MySQL
- PostgreSQL
- Snowflake
- Spark SQL (via Livy sessions)
- SQL Server

## When to use this approach

Use these tools when you want:

- A one-time migration from SQL tables into a FalkorDB property graph
- Ongoing one-way sync so FalkorDB stays updated as rows change in the source system

## Prerequisites

- Rust toolchain (Cargo)
- Network access to your source system
- A reachable FalkorDB endpoint (for example `falkor://127.0.0.1:6379`)
- Node.js + npm (optional; only needed for control plane UI)

Configurations typically reference environment variables for credentials/secrets (for example `$BIGQUERY_ACCESS_TOKEN`, `$DATABRICKS_TOKEN`, `$MYSQL_URL`, `$POSTGRES_URL`, `$SNOWFLAKE_PASSWORD`, `$SPARK_AUTH_TOKEN`, `$SQLSERVER_CONNECTION_STRING`).

## Getting the tools

```bash
git clone https://github.com/FalkorDB/DM-SQL-to-FalkorDB.git
cd DM-SQL-to-FalkorDB
```

## How the loaders work (high level)

Each loader uses JSON/YAML configuration to define:

- How to read rows from the source (`table` + optional filter, or custom query)
- How rows map to graph entities:
  - Nodes (labels, keys, property mappings)
  - Edges (relationship type, direction, endpoint matching rules)
- Per-mapping execution mode (`full` or `incremental`)
- Optional soft-delete behavior
- State backend for incremental watermarks (typically file-backed JSON)

### Common concepts

- Declarative mapping: mappings define extraction + graph writes.
- Idempotent writes: loaders use Cypher `UNWIND` + `MERGE`.
- Incremental safety: watermarks move only after successful writes.
- Restart safety: failed runs can resume from persisted state.
- Index handling: loaders apply explicit `falkordb.indexes` plus inferred indexes for node keys and edge endpoint matches.
- Observability: loaders expose Prometheus-style metrics with global and per-mapping counters.

## Option A: Run a loader directly (CLI)

### BigQuery → FalkorDB

- Docs: [BigQuery-to-FalkorDB/README.md](https://github.com/FalkorDB/DM-SQL-to-FalkorDB/tree/main/BigQuery-to-FalkorDB)

```bash
cd BigQuery-to-FalkorDB/bigquery-to-falkordb
cargo build --release

# One-shot run
cargo run --release -- --config ../bigquery_sample.yaml

# Continuous sync
cargo run --release -- --config ../bigquery_sample.yaml --daemon --interval-secs 60
```

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

Note: Databricks currently supports one-shot runs only (no daemon/purge flags).

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

Note: PostgreSQL currently supports daemon mode but not purge flags.

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

### Spark SQL (Livy) → FalkorDB

- Docs: [Spark-to-FalkorDB/README.md](https://github.com/FalkorDB/DM-SQL-to-FalkorDB/tree/main/Spark-to-FalkorDB)

```bash
cd Spark-to-FalkorDB/spark-to-falkordb
cargo build --release
cargo run --release -- --config path/to/config.yaml
```

Note: Spark currently supports one-shot runs only (no daemon/purge flags).

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

## Schema introspection + template scaffolding

Supported by: BigQuery, ClickHouse, Databricks, MariaDB, MySQL, PostgreSQL, Snowflake, Spark, SQL Server.

```bash
# Print normalized source schema summary
cargo run --release -- --config path/to/config.yaml --introspect-schema

# Generate starter mapping template
cargo run --release -- --config path/to/config.yaml --generate-template --output scaffold.yaml
```

Notes:

- Generated templates are scaffolds and should be reviewed before production use.
- For tools that support daemon/purge modes, scaffold flags cannot be combined with daemon/purge flags in the same run.

## Option B: Use the control plane (web UI + API)

The control plane discovers tools by scanning for `tool.manifest.json` and provides UI/API features to:

- Create and edit per-tool YAML/JSON configurations
- Preview extracted source schema
- Generate scaffold templates from source metadata
- Visualize graph topology from mappings
- Start runs (one-shot and daemon where supported)
- Stop active runs
- Stream live logs (SSE) and view persisted logs for historical runs
- Inspect and clear per-config incremental state/watermarks
- Persist and view per-tool/per-mapping metrics snapshots in SQLite

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

Selected API endpoints:

- `GET /api/health`
- `GET /api/tools`, `GET /api/tools/:tool_id`
- `POST /api/tools/:tool_id/scaffold-template`
- `POST /api/tools/:tool_id/schema-graph-preview`
- `GET /api/configs`, `POST /api/configs`
- `GET /api/configs/:config_id`, `PUT /api/configs/:config_id`
- `GET /api/configs/:config_id/state`, `POST /api/configs/:config_id/state/clear`
- `GET /api/runs`, `POST /api/runs`
- `GET /api/runs/:run_id`, `POST /api/runs/:run_id/stop`
- `GET /api/runs/:run_id/events` (SSE)
- `GET /api/runs/:run_id/logs`
- `GET /api/metrics` (optional `?config_id=<uuid>`)
- `GET /api/metrics/:tool_id` (optional `?config_id=<uuid>`)

Notes:

- Runs execute locally on the host machine running the control plane server.
- Runtime artifacts are persisted under `CONTROL_PLANE_DATA_DIR`, including a SQLite DB and per-run files.
- SSE auth with API key may use query-string token fallback because browser `EventSource` does not support custom auth headers. Be aware of the associated security risks:
  - Query-string tokens can appear in browser history, server access logs, and `Referer` headers on subsequent requests.
  - Mitigate by: using HTTPS, issuing short-lived tokens, filtering or minimizing access logging, or adopting a cookie/session-based approach or SSE polyfill where possible.

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

The following shows the metrics view summarizing a run:
<img width="1403" height="832" alt="DM-UI--metrics" src="https://github.com/user-attachments/assets/af09d6ff-c1ed-4148-b1ab-6fa2500887dc" />

## Metrics feature

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

- BigQuery: `9995`
- ClickHouse: `9991`
- Databricks: `9994`
- MariaDB: `9997`
- MySQL: `9995`
- PostgreSQL: `9993`
- Snowflake: `9992`
- Spark: `9997`
- SQL Server: `9996`

Note: BigQuery and MySQL share the same default metrics port (`9995`); MariaDB and Spark share `9997`. When running either of these pairs concurrently on the same host, configure distinct metrics ports for each loader.

Use `--metrics-port` (or each loader's corresponding `*_TO_FALKORDB_METRICS_PORT` environment variable) to override defaults, especially when running multiple loaders concurrently.

## Operational tips

- Define node mappings before edge mappings (edges depend on nodes).
- Choose stable keys for `MERGE` (primary keys are usually best).
- Treat scaffold-generated mappings as a starting point; always review relationship semantics and incremental/delete logic.
- Use `RUST_LOG=info` (or `debug`) for richer loader diagnostics.
- Keep state files and control-plane data on durable storage for long-running sync setups.

## Additional resources

- DM-SQL-to-FalkorDB repository: https://github.com/FalkorDB/DM-SQL-to-FalkorDB
- FalkorDB docs: https://docs.falkordb.com/
