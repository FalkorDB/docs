---
title: "Performance Tuning"
description: "Practical knobs and query practices to keep FalkorDB fast."
---

<!-- markdownlint-disable MD025 -->

# Performance Tuning

Use these steps to size hardware, tune configuration, and keep query latency predictable.

## Tuning quick-start

- **Set concurrency**: Align [`THREAD_COUNT`](/getting-started/configuration#thread_count) with available CPU cores for write-heavy or analytical workloads.
- **Control cache churn**: Increase [`CACHE_SIZE`](/getting-started/configuration#cache_size) for highly diverse parameterized queries.
- **Bound work**: Use [`TIMEOUT_DEFAULT`](/getting-started/configuration#timeout_default) and [`TIMEOUT_MAX`](/getting-started/configuration#timeout_max) to cap long-running queries; set [`MAX_QUEUED_QUERIES`](/getting-started/configuration#max_queued_queries) to protect memory under load.
- **Size results**: Cap responses with [`RESULTSET_SIZE`](/getting-started/configuration#resultset_size) and [`QUERY_MEM_CAPACITY`](/getting-started/configuration#query_mem_capacity) so runaway queries fail fast.
- **Profile before shipping**: run [`GRAPH.PROFILE`](/commands/graph.profile) and [`GRAPH.EXPLAIN`](/commands/graph.explain) to validate query plans.

## Query patterns

- Prefer **parameterized queries** to maximize plan cache hit rate and reduce parse/plan overhead.
- Add indexes before tuning hardware: see [range indexes](/cypher/indexing/range-index), [full-text](/cypher/indexing/fulltext-index), and [vector indexes](/cypher/indexing/vector-index).
- Keep projections narrow: return only needed fields; paginate with `SKIP`/`LIMIT`.
- Avoid Cartesian products: ensure patterns are selective and anchored with labels/properties.

## Concurrency and scheduling

- Keep `THREAD_COUNT` near physical cores for balanced workloads; lower it if you see CPU saturation from many concurrent writes.
- Increase `MAX_QUEUED_QUERIES` cautiously to avoid memory bloat; combine with timeouts to shed load gracefully.
- For mixed workloads, reserve a dedicated FalkorDB instance for heavy analytics so OLTP queries stay predictable.

## Memory and result sizing

- Tune `RESULTSET_SIZE` to prevent accidental full-graph scans from overwhelming clients.
- For large bulk inserts, stage writes and batch in transactions rather than single huge queries to reduce peak memory.
- Monitor memory after raising `CACHE_SIZE`; higher caches improve plan reuse but consume RAM.

## Observability loop

- Track query latency, queue depth, and timeout counts in your monitoring stack.
- Re-run `GRAPH.PROFILE` after schema or index changes; plan shape and cost can shift when data distributions change.
- Baseline throughput for representative datasets and queries, then document expected SLOs for teams.
