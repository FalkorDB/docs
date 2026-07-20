---
title: "Browser"
description: "FalkorDB Browser web UI for visualizing graphs, running Cypher queries, exploring data models, managing nodes and relationships, with query history and API documentation."
nav_order: 9
permalink: /browser/
has_children: true
---

# FalkorDB Browser

FalkorDB Browser is the web UI for working with FalkorDB graphs. It includes graph visualization, Cypher querying, graph management, role-aware administration, and built-in API docs.

## Run Browser with Docker

Run FalkorDB and Browser together:

```bash
docker run -p 6379:6379 -p 3000:3000 -it --rm falkordb/falkordb:latest
```

Open Browser at `http://localhost:3000`.

## LOAD CSV Storage Configuration

Browser CSV import (`Upload Data -> Load CSV`) stores a temporary CSV and then executes a server-built `LOAD CSV` query.

### Storage mode selection

| Setting | Behavior |
| :--- | :--- |
| `CSV_STORAGE=local` | Local filesystem storage for temp CSV files. |
| `CSV_STORAGE=s3` | S3/S3-compatible storage (presigned read URL). Requires `S3_BUCKET`. |
| `CSV_STORAGE=blob` | Vercel Blob storage. Requires `BLOB_READ_WRITE_TOKEN`. |
| `CSV_STORAGE` unset | Auto-select: S3 first, then Blob, else local. |

### Local mode notes

| Setting | Purpose |
| :--- | :--- |
| `CSV_LOCAL_LOAD_URI_MODE=file` | Recommended local/dev mode. Emits `file://` URI. |
| `IMPORT_FOLDER` | FalkorDB import root; must align with Browser temp path for `file://` mode. |
| `CSV_LOCAL_TEMP_DIR` | Optional Browser temp directory override. |
| `CSV_SERVE_BASE_URL` | Used only for served mode; must be `https://`. |

### URI requirement

FalkorDB `LOAD CSV` accepts only `https://` and `file://`. Plain `http://` URLs are rejected.

### Related limits

- `CSV_MAX_FILE_SIZE_MB`
- `CSV_TEMP_TTL_SECONDS`
- `CSV_TEMP_CLEANUP_SECRET`

## Main Features

### Graph workspace

- Graph selector and graph management
- Cypher editor with suggestions and diagnostics
- Graph, Table, and Metadata tabs
- Side panels for Graph Info, Data editing, Create element, and Chat

### Data operations

- Create, duplicate, and delete graphs
- Export graph as `.dump`
- Upload Cypher batch files (`.txt`, `.cql`, `.cypher`)
- Upload CSV and run `LOAD CSV`

### Security and access

- Login via manual host/port fields or URL mode
- Optional TLS with CA upload
- Role-aware features (`Admin`, `Read-Write`, `Read-Only`)
- Personal access token management

### API docs

- Swagger UI at `/docs`
- OpenAPI JSON at `/api/swagger`

## Browser UI Reference

- [UI Elements](./ui/)
- [Canvas](./canvas)
