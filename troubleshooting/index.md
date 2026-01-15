---
title: "Troubleshooting & FAQ"
description: "Fast answers to common FalkorDB setup and query issues."
---

<!-- markdownlint-disable MD025 -->

# Troubleshooting & FAQ

Use this page to triage the most common problems before opening a ticket.

## Quick checks

- Verify the server is reachable: `redis-cli -h <host> -p <port> PING`.
- Confirm authentication works: `AUTH <password>` or your client’s auth call.
- Inspect server logs for rejections, timeouts, or OOM messages.
- Run a simple read-only query: `MATCH (n) RETURN n LIMIT 1`.

## Connection issues

- **Connection refused / timed out**: ensure ports are open only to allowed sources; check container or pod health. In Kubernetes, confirm the Service type and NetworkPolicy allow traffic.
- **TLS failures**: if using a TLS terminator, test plain TCP locally, then from the terminator; validate certificates and SNI.

## Authentication and ACLs

- **NOAUTH** or **NOPERM** errors: the user lacks rights. Revisit [ACL rules](/commands/acl) and ensure the client uses the correct username and password.
- Rotate credentials and re-deploy clients that cache connections to avoid using stale secrets.

## Query errors

- **SyntaxError**: run [`GRAPH.EXPLAIN`](/commands/graph.explain) on the query to spot syntax and planning issues early.
- **Parameter errors**: ensure parameter names match exactly; prefer parameterized queries in clients to avoid quoting mistakes.
- **Timeouts**: raise [`TIMEOUT_MAX`](/getting-started/configuration#timeout_max) cautiously or simplify the query. Use `LIMIT` while iterating on query shapes.

## Performance and memory

- **High latency**: profile with [`GRAPH.PROFILE`](/commands/graph.profile); add indexes ([range](/cypher/indexing/range-index), [full-text](/cypher/indexing/fulltext-index), [vector](/cypher/indexing/vector-index)) for selectivity.
- **Server busy / queued**: lower concurrency or set [`MAX_QUEUED_QUERIES`](/getting-started/configuration#max_queued_queries); add capacity if queues stay high.
- **Out of memory**: cap responses with [`RESULTSET_SIZE`](/getting-started/configuration#resultset_size) and [`QUERY_MEM_CAPACITY`](/getting-started/configuration#query_mem_capacity); split large writes into batches.

## Data and indexing

- **Missing results**: confirm labels and relationship types match your queries; indexes only apply when the label/property matches the index definition.
- **Index creation slow**: build indexes during off-peak hours and monitor resource usage; tune vector index options (`M`, `efConstruction`, `efRuntime`) per [vector indexing](/cypher/indexing/vector-index).

## When to ask for help

- Reproduce with the smallest possible dataset and query.
- Include server version, client language and version, config overrides, and a sample query when filing an issue.
