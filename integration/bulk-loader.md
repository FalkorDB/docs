---
title: "Bulk Loader"
description: "Import large graphs from CSV files into FalkorDB using the falkordb-bulk-loader tool"
---

# Bulk Loader

The [falkordb-bulk-loader](https://github.com/falkordb/falkordb-bulk-loader) is a Python utility for building FalkorDB graphs from CSV files. It uses the `GRAPH.BULK` endpoint to import nodes and relationships efficiently in binary batches — much faster than issuing individual `CREATE` queries.

## Requirements

- Python 3.10 or later
- A running FalkorDB instance (see [Get Started](https://docs.falkordb.com))

## Installation

```sh
pip install falkordb-bulk-loader
```

## Quick Start

Given two CSV files — `Person.csv` (nodes) and `KNOWS.csv` (relationships) — import them into a graph named `SocialGraph`:

```sh
falkordb-bulk-insert SocialGraph \
  -n Person.csv \
  -r KNOWS.csv
```

The label (for nodes) and relationship type (for relationships) are derived from the CSV filename. Multiple node and relation files can be provided by repeating the flags:

```sh
falkordb-bulk-insert SocialGraph \
  -n Person.csv \
  -n Country.csv \
  -r KNOWS.csv \
  -r VISITED.csv
```

## Connecting to FalkorDB

By default the loader connects to `redis://127.0.0.1:6379`. Use `--redis-url` to point it at a different instance:

```sh
falkordb-bulk-insert SocialGraph \
  --redis-url redis://myhost:6379 \
  -n Person.csv
```

## Key Options

| Flag | Extended flag | Description |
|:----:|---------------|-------------|
| `-u` | `--redis-url TEXT` | Server URL (default: `redis://127.0.0.1:6379`) |
| `-n` | `--nodes TEXT` | Node CSV file (filename → label) |
| `-N` | `--nodes-with-label TEXT` | Explicit label followed by node CSV file |
| `-r` | `--relations TEXT` | Relationship CSV file (filename → type) |
| `-R` | `--relations-with-type TEXT` | Explicit type followed by relationship CSV file |
| `-o` | `--separator CHAR` | Field delimiter (default: `,`) |
| `-d` | `--enforce-schema` | Require typed column headers (see below) |
| `-j` | `--id-type TEXT` | Type of node ID property: `STRING` or `INTEGER` |
| `-s` | `--skip-invalid-nodes` | Skip duplicate node IDs instead of erroring |
| `-e` | `--skip-invalid-edges` | Skip edges with unknown endpoints instead of erroring |
| `-i` | `--index Label:Property` | Create a range index after import |
| `-f` | `--full-text-index Label:Property` | Create a full-text index after import |

## Enforcing a Schema

By default the loader infers each property's type. Use `--enforce-schema` (`-d`) when you want explicit control. Column headers must follow the `name:TYPE` format:

**User.csv**
```csv
:ID(User),name:STRING,rank:INT
0,"Alice",5
1,"Bob",8
```

**FOLLOWS.csv**
```csv
:START_ID(User),:END_ID(User),weight:DOUBLE
0,1,0.9
1,0,0.4
```

```sh
falkordb-bulk-insert SocialGraph \
  --enforce-schema \
  -n User.csv \
  -r FOLLOWS.csv
```

Accepted type strings: `ID`, `START_ID`, `END_ID`, `IGNORE`, `STRING`, `INT` / `INTEGER` / `LONG`, `DOUBLE` / `FLOAT`, `BOOL` / `BOOLEAN`, `ARRAY`.

## Bulk Updates

The companion command `falkordb-bulk-update` reads a CSV in batches and issues a parameterized Cypher query for each row — useful for incremental updates or when you want full control over the Cypher:

```sh
falkordb-bulk-update SocialGraph \
  --csv User.csv \
  --query "MERGE (:User {id: row[0], name: row[1], rank: row[2]})"
```

> **Note:** `falkordb-bulk-update` commits changes incrementally. Sanitize your CSV inputs beforehand to avoid leaving the graph in a partially-updated state.

## Further Reading

- [GitHub repository](https://github.com/falkordb/falkordb-bulk-loader) — full CLI reference, input constraints, and ID namespaces
- [GRAPH.BULK specification](/design/bulk-spec) — technical wire-format specification for the underlying endpoint
