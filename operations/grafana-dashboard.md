---
title: "Grafana Dashboard Panels"
nav_order: 13
parent: Operations
description: "Understand the FalkorDB Grafana monitoring dashboard. Learn what each panel shows, the Prometheus metric behind it, and how to read it to keep your graph database healthy."
redirect_from:
  - /operations/grafana-dashboard.html
  - /operations/grafana-dashboard
---

# Grafana Dashboard Panels Guide

FalkorDB Cloud ships with a pre-built **FalkorDB Dashboard** in [Grafana](https://grafana.com/)
that visualizes the health and workload of your instances. Metrics are scraped by a
Prometheus-compatible Redis exporter (the `redis_*` and FalkorDB-specific
`redis_falkordb_*` series), combined with Kubernetes container metrics
(`container_*` and `kube_pod_*`), and logs from the service container.

This guide explains **what each panel shows**, **the metric behind it**, and **how to read
it** so you can tell the difference between a healthy instance and one that needs attention.

## Filtering the dashboard

At the top of the dashboard a set of variables let you scope every panel:

| Variable | Purpose |
| :--- | :--- |
| **datasource** | Selects which Prometheus data source to query. |
| **namespace** | Filters to a Kubernetes namespace. |
| **pod** | Filters to one or more FalkorDB pods. |
| **container** | Filters to a specific container in the pod. |
| **graph** | Selects an individual graph for the per-graph panels. |

> **Tip:** Use the **time range picker** (top-right) to zoom in on an incident, hover over a
> graph to read the exact value and timestamp, and click a series in the legend to isolate it.

## Overview stats

The top row shows single-stat panels that summarize the current state of the selected
pods.

### Pod Info

- **Shows:** identifying information for the running instance, from `redis_instance_info`
  (version, role, and related labels).
- **How to read it:** confirm the version and role match what you expect. This panel is the
  quickest way to verify which build is deployed.

### Clients

- **Shows:** the total number of connected clients across the selected pods
  (`sum(redis_connected_clients)`).
- **How to read it:** compare against your application's connection-pool size. A value that
  keeps climbing can indicate a connection leak; a value near the configured `maxclients`
  limit risks new connections being rejected.

### Max Uptime

- **Shows:** the longest uptime among the selected pods, from
  `max_over_time(redis_uptime_in_seconds)`.
- **How to read it:** the value should grow steadily. A drop toward zero means a pod
  restarted (planned maintenance, an out-of-memory kill, or a crash) — correlate it with the
  Memory and Clients panels.

### Memory Usage

- **Shows:** a gauge of memory used as a percentage of the configured maximum
  (`100 * redis_memory_used_bytes / redis_memory_max_bytes`).
- **How to read it:** the gauge turns red as it approaches the limit (the threshold is set at
  80%). Sustained high usage means the eviction policy will start removing keys, so treat it
  as a signal to scale up or reduce the dataset.

### Graph count

- **Shows:** the number of graphs stored on the selected instance
  (`redis_falkordb_total_graph_count`).
- **How to read it:** sudden jumps or drops reflect graphs being created or deleted in bulk.
  Track it alongside memory growth.

## Per-Graph Memory row

These panels break memory consumption down per graph, using FalkorDB's
`redis_falkordb_graph_*` metrics (reported in megabytes).

### Memory by Graph

- **Shows:** the top 10 graphs by total memory
  (`topk(10, redis_falkordb_graph_memory_total_mb)`).
- **How to read it:** identify which graphs dominate memory. A single graph growing far
  faster than the rest is the first place to look when overall memory climbs.

### Memory Distribution by Component

- **Shows:** a pie chart splitting total memory across **node blocks**
  (`redis_falkordb_graph_node_block_mb`), **edge blocks**
  (`redis_falkordb_graph_edge_block_mb`), **matrices** (label + relation matrices), and
  **indices** (`redis_falkordb_graph_indices_mb`).
- **How to read it:** use it to understand *where* memory goes. A large indices slice, for
  example, suggests you have many or large indexes; a dominant matrices slice reflects dense
  connectivity.

### Graph Memory Components (by $graph)

- **Shows:** the same component breakdown over time for the single graph selected with the
  **graph** variable (node block, edge block, label matrices, relation matrices, indices).
- **How to read it:** watch which component drives growth for a specific graph. This is the
  drill-down companion to the distribution pie chart.

## Memory Analysis row

### Memory Fragmentation Ratio

- **Shows:** `redis_mem_fragmentation_ratio` — the ratio of memory the allocator holds to
  the memory FalkorDB actually uses. A red reference line marks the **1.5 alert threshold**
  (the `FalkorDBMemoryFragmentationHigh` alert fires if the ratio stays above it for more
  than 10 minutes).
- **How to read it:** a value around `1.0`–`1.5` is healthy. Sustained values above `1.5`
  signal fragmentation, while a value **below `1.0`** means part of the dataset has been
  swapped to disk — a serious performance risk that warrants adding memory.

### Redis Memory Breakdown (Dataset vs Overhead vs Allocator Waste)

- **Shows:** `redis_memory_used_dataset_bytes` (your actual data),
  `redis_memory_used_overhead_bytes` (server bookkeeping), and allocator waste
  (`redis_allocator_active_bytes - redis_allocator_allocated_bytes`).
- **How to read it:** a healthy instance is dominated by the dataset series. Rising overhead
  or allocator waste relative to the dataset points to fragmentation or many small
  connections/buffers rather than real data growth.

### Container Memory (Working Set, RSS, Limits, Requests)

- **Shows:** Kubernetes container memory — `container_memory_working_set_bytes`,
  `container_memory_rss`, and the configured `kube_pod_container_resource_limits` and
  `requests`.
- **How to read it:** the working set should stay comfortably below the limit line. When the
  working set approaches the limit, the pod is at risk of being OOM-killed by Kubernetes —
  cross-check with Max Uptime for restarts.

## Commands & Queries row

### Total Commands / sec

- **Shows:** the rate of all commands processed, broken down by command and pod
  (`rate(redis_commands_total[1m])`).
- **How to read it:** this is your primary workload indicator. An unexpected drop to zero
  while clients are connected suggests the server is blocked; an unexpected spike may explain
  rising CPU or latency.

### Graph Commands / sec

- **Shows:** throughput of `GRAPH.*` commands only (the metric filters `cmd` to commands
  starting with `graph.`), by pod and command.
- **How to read it:** isolates the graph workload from background Redis traffic. Use it to
  see which graph commands (`GRAPH.QUERY`, `GRAPH.RO_QUERY`, etc.) drive load.

### Top Graph Commands by Time-Spent Rate

- **Shows:** the top 20 user-facing graph commands ranked by total time spent
  (`topk(20, rate(redis_commands_duration_seconds_total[5m]))`). Internal Redis
  infrastructure commands are excluded.
- **How to read it:** the commands at the top consume the most engine time. These are your
  best optimization targets — profile them with
  [`GRAPH.PROFILE`](/commands/graph.profile) and [`GRAPH.EXPLAIN`](/commands/graph.explain).

### Avg Query Latency (Graph Commands)

- **Shows:** average latency per graph command per pod, computed as the duration rate divided
  by the call rate across all `GRAPH.*` commands.
- **How to read it:** rising average latency while throughput stays flat means individual
  queries are getting heavier. Pair it with the time-spent panels to find the culprit.

### Total Time Spent by Command / sec

- **Shows:** the instantaneous rate of time spent per command
  (`irate(redis_commands_duration_seconds_total[1m])`), excluding idle commands.
- **How to read it:** highlights which commands are currently consuming engine time, even if
  they are infrequent. A command with low call rate but high time-spent is expensive per
  call.

### Average Time Spent by Command / sec

- **Shows:** the average time per call for each command (total time-spent rate divided by the
  call rate).
- **How to read it:** complements the total time-spent panel by normalizing for frequency,
  surfacing commands that are individually slow.

### Slowlog

- **Shows:** the 10 most recent entries from the FalkorDB slow log
  (`redis_slowlog_history_last_ten`), shown as a table.
- **How to read it:** these are the slowest recent commands captured by the server. Use them
  as concrete starting points for optimization. The
  [`GRAPH.SLOWLOG`](/commands/graph.slowlog) command exposes the same data directly.

## System & Clients row

### CPU

- **Shows:** container CPU usage as a percentage
  (`rate(container_cpu_usage_seconds_total)`), with a reference line at **80%**.
- **How to read it:** short spikes during heavy queries are normal. Sustained usage near or
  above the 80% line indicates the pod is CPU-bound — look at the Commands & Queries row to
  find the expensive workload.

### Total Memory Usage

- **Shows:** `redis_memory_used_bytes` plotted against the configured maximum
  (`redis_memory_max_bytes`) and a warning line at **80% of the max**.
- **How to read it:** watch the gap between the used series and the max line. Crossing the
  80% warning line is your cue to scale memory before evictions begin.

### Network I/O

- **Shows:** inbound and outbound traffic rates (`rate(redis_net_input_bytes_total)` and
  `rate(redis_net_output_bytes_total)`).
- **How to read it:** a high outbound rate with low command throughput suggests queries are
  returning very large results — consider adding `LIMIT` clauses or projecting fewer
  properties.

### Connected/Blocked Clients

- **Shows:** `redis_connected_clients` alongside `redis_blocked_clients` (clients waiting on
  a blocking command), per pod.
- **How to read it:** a growing blocked-clients count can indicate contention or
  long-running commands holding resources, while a climbing connected count may point to a
  connection leak.

## Databases & Keys row

### Graph Count Trend

- **Shows:** `redis_falkordb_total_graph_count` over time for the selected pods.
- **How to read it:** the time-series view of the Graph count stat. Use it to correlate
  graph creation/deletion with memory and workload changes.

### Total Items per DB

- **Shows:** the number of keys in each logical database (`redis_db_keys`, grouped by `db`).
- **How to read it:** in FalkorDB each key is typically a graph, so this reflects how graphs
  are distributed across databases. Sudden jumps or drops show bulk changes.

## Logs row

### Logs (service container)

- **Shows:** live log lines from the FalkorDB service container, queried from the logs data
  source (SSL handshake noise is filtered out).
- **How to read it:** use this panel to correlate metric anomalies with log messages — for
  example, matching a memory spike or restart to an error in the logs at the same timestamp.

## Putting it together

When investigating an issue, read the dashboard top-down:

1. **Overview stats** tell you if a pod restarted or is under memory pressure.
2. **Commands & Queries** reveal whether the workload changed and which commands are heavy.
3. **Memory** and **System** rows confirm whether the instance can sustain that workload, and
   the **Logs** row helps pin down the root cause.

A healthy FalkorDB instance shows steady uptime, memory comfortably below the limit, a
fragmentation ratio near `1.0`, CPU below the 80% line, and no unexpected gaps in command
throughput.

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="Where do the dashboard metrics come from?"
  a1="They are scraped by a Prometheus-compatible Redis exporter (the `redis_*` and FalkorDB-specific `redis_falkordb_*` series) plus Kubernetes container metrics (`container_*`, `kube_pod_*`), and visualized in Grafana. FalkorDB Cloud provides this dashboard out of the box under Advanced Monitoring."
  q2="My memory fragmentation ratio is above 1.5 — is that a problem?"
  a2="The dashboard marks 1.5 as the alert threshold, and the `FalkorDBMemoryFragmentationHigh` alert fires if the ratio stays above it for more than 10 minutes. A ratio below 1.0 is worse still — it means part of the dataset has been swapped to disk. In both cases, consider adding memory."
  q3="Which panel should I check first when queries get slow?"
  a3="Look at the Commands & Queries row. **Top Graph Commands by Time-Spent Rate** and **Avg Query Latency** show which commands consume the most engine time, and the **Slowlog** table lists the slowest recent commands. Optimize them with [`GRAPH.EXPLAIN`](/commands/graph.explain) and [`GRAPH.PROFILE`](/commands/graph.profile)."
  q4="How do I find which graph is using the most memory?"
  a4="Use the **Per-Graph Memory** row. **Memory by Graph** ranks the top 10 graphs, and **Graph Memory Components** breaks a single selected graph into node blocks, edge blocks, matrices, and indices."
  q5="Why did one of my pods reset its uptime?"
  a5="A drop in **Max Uptime** means a pod restarted. Check the **Container Memory** panel for an OOM-kill (working set hitting the limit) and the **Logs** panel for errors around the same timestamp."
%}
