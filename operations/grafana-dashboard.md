---
title: "Grafana Dashboard Panels"
nav_order: 13
parent: Operations
description: "Understand the FalkorDB Cloud Grafana monitoring dashboard. Learn what each panel shows, the metric behind it, and how to read it to keep your graph database healthy."
redirect_from:
  - /operations/grafana-dashboard.html
  - /operations/grafana-dashboard
---

# Grafana Dashboard Panels Guide

FalkorDB Cloud ships with a pre-built [Grafana](https://grafana.com/) dashboard that
visualizes the health and workload of your instance. The metrics are collected with a
Prometheus-compatible exporter that scrapes the standard Redis `INFO` fields together
with FalkorDB graph statistics, so the same dashboard also works for self-hosted
deployments that expose those metrics.

This guide explains **what each panel shows**, **the metric behind it**, and **how to read
it** so you can tell the difference between a healthy instance and one that needs
attention.

## Overview

The dashboard is organized into rows that group related panels:

| Row | What it answers |
| :--- | :--- |
| [Overview](#overview-row) | Is the instance up and how busy is it right now? |
| [Memory](#memory-row) | How much memory is used and is fragmentation under control? |
| [Throughput & Commands](#throughput--commands-row) | How many operations is the instance serving? |
| [Clients & Connections](#clients--connections-row) | Are clients connecting cleanly? |
| [Network](#network-row) | How much data is flowing in and out? |
| [Keyspace & Cache](#keyspace--cache-row) | How effective is the keyspace and cache? |
| [Persistence](#persistence-row) | Are snapshots and the append-only file healthy? |
| [Replication](#replication-row) | Is the replica keeping up with the primary? |
| [Graph Queries](#graph-queries-row) | What is the Cypher query workload doing? |

Most panels are time-series graphs. Use the **time range picker** (top-right) to zoom in on
an incident, and the **variables / dropdowns** (top-left) to switch between instances or
graphs when several are reported.

> **Tip:** Hover over any point on a graph to see the exact value and timestamp, and
> click a series name in the legend to isolate it.

## Overview row

### Uptime

- **Shows:** how long the server has been running since its last restart, from the
  `uptime_in_seconds` field of `INFO`.
- **How to read it:** the value should grow steadily. A sudden drop to near zero means the
  instance restarted (planned maintenance, an out-of-memory kill, or a crash). Correlate a
  reset here with spikes in the Memory and Clients rows.

### Connected Clients

- **Shows:** the number of client connections currently open (`connected_clients`).
- **How to read it:** compare against your application's expected connection-pool size. A
  flat line near your pool maximum is normal; a steadily climbing line can indicate
  connection leaks, and a value near the configured `maxclients` limit risks new
  connections being rejected.

### Memory Used

- **Shows:** the current memory footprint (`used_memory`) as a single-stat or gauge,
  often next to the configured maximum (`maxmemory`).
- **How to read it:** as long as usage stays comfortably below `maxmemory` you are fine.
  When it approaches the limit, the eviction policy starts removing keys (or writes fail if
  eviction is disabled), so treat sustained high usage as a signal to scale up or reduce the
  dataset.

### CPU Usage

- **Shows:** processor time consumed by the server, derived from `used_cpu_sys` and
  `used_cpu_user` (typically displayed as a percentage or rate).
- **How to read it:** short spikes during heavy queries are expected. Sustained high CPU
  usually points to expensive Cypher queries or a high command rate — cross-check the
  [Graph Queries](#graph-queries-row) and [Throughput](#throughput--commands-row) rows to
  find the source.

## Memory row

### Memory Usage Over Time

- **Shows:** `used_memory` plotted over time, frequently overlaid with `used_memory_rss`
  (resident memory reported by the operating system) and `maxmemory`.
- **How to read it:** a slow, continuous climb that never falls can indicate a workload that
  keeps adding data, while a sawtooth pattern (rise then drop) is normal for workloads that
  create and delete keys. Watch the gap between `used_memory` and the `maxmemory` ceiling.

### Memory Fragmentation Ratio

- **Shows:** `mem_fragmentation_ratio`, the ratio of memory the operating system allocated
  to the memory FalkorDB actually requested.
- **How to read it:** a value around `1.0`–`1.5` is healthy. Significantly above `1.5`
  signals fragmentation (the process is holding more memory than it needs), while a value
  **below `1.0`** means part of the dataset has been swapped to disk — a serious performance
  risk that warrants adding memory.

## Throughput & Commands row

### Commands Per Second

- **Shows:** the rate of commands processed, calculated as the per-second change of
  `total_commands_processed` (also surfaced as `instantaneous_ops_per_sec`).
- **How to read it:** this is your primary workload indicator. Compare peaks against your
  expected traffic. An unexpected drop to zero while clients are connected suggests the
  server is blocked or unreachable; an unexpected spike may explain rising CPU or latency.

### Command Latency

- **Shows:** average or percentile latency per command (when the exporter exposes command
  statistics from `INFO commandstats`).
- **How to read it:** focus on the higher percentiles (p95/p99) rather than the average —
  they reveal the slow tail that users actually feel. Rising latency alongside flat
  throughput often means individual queries are getting heavier.

## Clients & Connections row

### Connected vs Blocked Clients

- **Shows:** `connected_clients` next to `blocked_clients` (clients waiting on a blocking
  command).
- **How to read it:** a non-zero blocked count is normal for blocking operations, but a
  growing number of blocked clients can indicate contention or long-running commands holding
  resources.

### Rejected Connections

- **Shows:** `rejected_connections`, the number of connections refused because the
  `maxclients` limit was reached.
- **How to read it:** this should stay at zero. Any increase means clients are being turned
  away — raise the connection limit or fix a client that is not releasing connections.

## Network row

### Network I/O

- **Shows:** inbound and outbound traffic, from `total_net_input_bytes` and
  `total_net_output_bytes` (often plotted as bytes per second).
- **How to read it:** use it to spot unusually large payloads or result sets. A large
  outbound rate with low command throughput suggests queries are returning very large
  results — consider adding `LIMIT` clauses or projecting fewer properties.

## Keyspace & Cache row

### Keys per Database

- **Shows:** the number of keys in each logical database from the `INFO keyspace` section.
  In FalkorDB each key is typically a graph, so this reflects how many graphs exist.
- **How to read it:** sudden jumps or drops show graphs being created or deleted in bulk.
  Track this against memory growth.

### Cache Hit Ratio

- **Shows:** the ratio of `keyspace_hits` to `keyspace_hits + keyspace_misses`.
- **How to read it:** a high hit ratio means most lookups find their key; a falling ratio
  means more requests are missing, which can increase load. Interpret it together with your
  access pattern — a low ratio is not always bad if you intentionally probe for missing keys.

### Evicted & Expired Keys

- **Shows:** the rate of `evicted_keys` (removed to free memory) and `expired_keys`
  (removed because their TTL elapsed).
- **How to read it:** expirations are normal if you use TTLs. Evictions, however, mean the
  instance hit its memory limit and is dropping data to stay within it — a strong signal to
  scale memory or reduce the dataset.

## Persistence row

### Changes Since Last Save

- **Shows:** `rdb_changes_since_last_save`, the number of write operations not yet captured
  in an RDB snapshot.
- **How to read it:** the value rises with writes and resets to zero after each successful
  snapshot. A continuously climbing value that never resets indicates snapshots are failing
  or are configured too infrequently, increasing the data you could lose on a crash.

### Last Save Status

- **Shows:** the timestamp of the last successful RDB save (`rdb_last_save_time`) and the
  status of the last background save (`rdb_last_bgsave_status`), plus AOF status when
  append-only persistence is enabled.
- **How to read it:** the last-save time should advance regularly. A status of anything
  other than `ok` means persistence is broken and needs immediate attention. See the
  [Data Durability](/operations/durability) guide for how RDB and AOF work together.

## Replication row

### Role & Connected Replicas

- **Shows:** whether the instance is a primary or a replica (`role`) and how many replicas
  are attached (`connected_slaves`).
- **How to read it:** confirm the topology matches your expectation. Losing a replica
  (count drops) reduces redundancy and read capacity.

### Replication Lag

- **Shows:** the offset difference between the primary (`master_repl_offset`) and each
  replica's acknowledged offset.
- **How to read it:** the lag should stay near zero. Growing lag means a replica is falling
  behind — usually due to network limits or a write-heavy primary — and reads from that
  replica may return stale data.

## Graph Queries row

These panels are specific to FalkorDB and reflect the Cypher workload, sourced from
[`GRAPH.INFO`](/commands/graph.info) and related graph statistics.

### Running Queries

- **Shows:** the number of Cypher queries currently being executed by worker threads.
- **How to read it:** brief peaks are expected under load. A value that stays pinned at the
  thread-pool size indicates the engine is saturated and new queries will start to queue.

### Waiting Queries

- **Shows:** queries received but queued, waiting for a worker thread to become available.
- **How to read it:** this should usually be zero or near it. A persistently non-zero
  waiting count means demand exceeds capacity — optimize slow queries (see
  [`GRAPH.EXPLAIN`](/commands/graph.explain) and [`GRAPH.PROFILE`](/commands/graph.profile))
  or scale the instance.

### Query Execution Time

- **Shows:** the duration of recent queries (for example, the slowest queries captured by
  [`GRAPH.SLOWLOG`](/commands/graph.slowlog)).
- **How to read it:** identify outliers and recurring slow queries. Pair this panel with the
  CPU and Waiting Queries panels to confirm whether slow queries are the root cause of a
  bottleneck.

## Putting it together

When investigating an issue, read the dashboard top-down:

1. **Overview** tells you if the instance restarted or is under memory/CPU pressure.
2. **Throughput** and **Graph Queries** reveal whether the workload changed.
3. **Memory**, **Persistence**, and **Replication** confirm whether the instance can
   sustain that workload safely.

A healthy FalkorDB instance shows steady uptime, memory comfortably below the limit, a
fragmentation ratio near `1.0`, zero rejected connections, regular successful saves, near-zero
replication lag, and a waiting-queries count at or close to zero.

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="Where do the dashboard metrics come from?"
  a1="They are scraped by a Prometheus-compatible exporter from the standard Redis `INFO` command and FalkorDB's `GRAPH.INFO` graph statistics, then visualized in Grafana. FalkorDB Cloud provides this dashboard out of the box under Advanced Monitoring."
  q2="My memory fragmentation ratio is below 1.0 — is that a problem?"
  a2="Yes. A ratio below 1.0 means part of the dataset has been swapped to disk, which severely degrades performance. Add memory or reduce the dataset so the working set fits in RAM."
  q3="What should I check first when queries get slow?"
  a3="Look at the Graph Queries row. A high Waiting Queries count with saturated Running Queries means the engine is at capacity. Use `GRAPH.EXPLAIN` and `GRAPH.PROFILE` to optimize the heaviest queries, then consider scaling up."
  q4="Why is my Changes Since Last Save panel climbing and never resetting?"
  a4="It resets to zero after each successful RDB snapshot. If it never resets, snapshots are failing or are scheduled too infrequently. Check the Last Save Status panel and review the [Data Durability](/operations/durability) guide."
  q5="Rejected Connections is above zero — what does that mean?"
  a5="The instance reached its `maxclients` limit and refused new connections. Increase the connection limit, enlarge or fix your client connection pool, and check the Connected Clients panel for leaks."
%}
