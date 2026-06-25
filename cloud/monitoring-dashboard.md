---
title: "Monitoring Dashboard"
parent: "Cloud DBaaS"
nav_order: 6
description: "Guide to the FalkorDB Cloud Grafana monitoring dashboard. Learn what each panel shows and how to read it, including memory, commands, latency, system, and client metrics."
---

# Monitoring Dashboard

FalkorDB Cloud ships with a Grafana monitoring dashboard that gives you a real-time view of how your instance is performing. This page explains what each panel shows and how to interpret what you see.

## Dashboard Variables

The controls at the top of the dashboard filter every panel. Most are pre-selected for your deployment and you can leave them as they are — the only ones you'll typically change are **pod** and **graph**.

| Variable | What it selects |
| :--- | :--- |
| **pod** | The FalkorDB instance to inspect. A deployment may have a master and one or more replicas. |
| **graph** | A specific graph (database) used by the per-graph memory panels. |

The remaining controls (**datasource**, **vl_datasource**, **namespace**, and **container**) come pre-configured for your deployment — you don't need to touch them.

The top bar also has an **Active Defrag Running** toggle. When enabled, the **Memory Fragmentation Ratio** panel shows a **blue vertical line** at each moment FalkorDB started an active-defragmentation pass (the annotation is scoped to that panel only). Hovering over the line shows an "Active Defrag Running" tooltip. This lets you line up dips in fragmentation with the defrag runs that caused them. Toggle it off to hide the lines.

> Tip: The **pod** control accepts multiple selections. Selecting all pods is useful for comparing a master against its replicas side by side.

---

## Overview (Top Row)

These single-value panels give you an at-a-glance health summary.

### Pod Info
Shows instance metadata from `redis_instance_info` — the instance mode and the pod role (`master` or `replica`). Use it to confirm you are looking at the right node and to verify which pod is currently the master.

> For an accurate reading, make sure the **service** container and a single **pod** are selected.

### Clients
The total number of connected clients (`redis_connected_clients`) across the selected pods. A sudden jump can indicate a connection leak in your application or a spike in traffic; a drop to zero usually means clients can no longer reach the instance.

### Max Uptime 
The longest uptime in seconds across the selected pods (`redis_uptime_in_seconds`). A reset to a low value means the process restarted — useful for spotting unexpected crashes or restarts.

### Memory Usage
A gauge showing used memory as a percentage of the configured maximum (`redis_memory_used_bytes / redis_memory_max_bytes`). As this approaches 100% the instance is close to its `maxmemory` limit, after which writes may be rejected or keys evicted depending on the policy. Treat sustained high values as a signal to scale up or reduce data size.

### Graph count
The number of graphs (databases) on the master (`redis_falkordb_total_graph_count`). It only counts the master to avoid double-counting replicas. Use it to track how many tenants/graphs live on the instance.

---

## Per-Graph Memory

This row breaks memory down by individual graph, which is essential in multi-tenant deployments.

### Memory by Graph
The top 10 graphs by total memory in MB (`redis_falkordb_graph_memory_total_mb`). Use it to identify which graphs consume the most memory and which tenant is driving growth.

### Memory Distribution by Component
A pie chart splitting total memory across the major FalkorDB internal structures:

- **Nodes** — storage for nodes (node blocks).
- **Edges** — storage for relationships (edge blocks).
- **Matrices** — label and relation matrices combined (the sparse-matrix representation of the graph).
- **Indices** — memory used by indexes.

This tells you *where* memory goes. Large matrix or index consumption, for example, points to highly connected data or heavy indexing.

> This panel aggregates across all graphs on the instance, so it is **not** affected by the **graph** variable. To see the breakdown for a single graph, use **Graph Memory Components** below.

### Graph Memory Components (by $graph)
The same breakdown as the pie chart, but as a time series for a single graph selected with the **graph** variable. Node blocks, edge blocks, label matrices, relation matrices, and indices are each plotted over time so you can see which component grows as your data changes.

> This panel draws one series per pod, so if more than one **pod** is selected (master + replica) each component appears twice — once per pod. Select a single pod (typically the master) to collapse it to one entry per component.

---

## Memory Analysis

This row helps you diagnose memory health and fragmentation.

### Memory Fragmentation Ratio
The ratio of memory allocated by the OS to memory actually used by FalkorDB (`redis_mem_fragmentation_ratio`). The green line is the actual ratio; a red reference line marks the 1.5 alert threshold.

- **Around 1.0–1.5** — healthy.
- **Above 1.5 (the red threshold line)** — fragmentation is high; worth investigating if it stays there.
- **Below 1.0** — more memory is reported as used than the allocator holds as active, which is common for small or memory-efficient datasets; it only signals a problem (swap usage) when paired with low available system memory.

> **A high ratio doesn't always mean a problem.** The ratio is `RSS / used_memory`, and RSS includes fixed overhead (code pages, stacks, allocator arenas) that doesn't shrink with your data. On a small instance this overhead can push the ratio well above 1.5 even though only a few MB are actually reclaimable.
>
> For example, an instance with a ~420 MiB dataset can show a ratio of ~1.67 while the **Redis Memory Breakdown** panel reports only ~5 MiB of allocator waste. That's inflated overhead, not real heap fragmentation.
>
> This is also why you may see no defrag activity despite a high ratio: active defrag only runs once the *absolute* wasted memory exceeds `active-defrag-ignore-bytes` (100 MB by default). With just a few MB wasted, defrag correctly stays idle — so the high ratio is expected and harmless. Cross-check the **Redis Memory Breakdown** panel before treating a high ratio as a real issue.

### Redis Memory Breakdown (Dataset vs Overhead vs Allocator Waste)
Splits total memory (in bytes) into three parts:

- **Dataset** (`redis_memory_used_dataset_bytes`) — memory holding your actual data.
- **Overhead** (`redis_memory_used_overhead_bytes`) — internal bookkeeping, buffers, and client connections.
- **Allocator waste** (`redis_allocator_active_bytes - redis_allocator_allocated_bytes`) — memory held by the allocator but not in active use.

A growing overhead or allocator-waste share relative to the dataset indicates memory pressure that is not caused by your data growing.

### Container Memory (Working Set, RSS, Limits, Requests)
Compares actual memory consumption against the Kubernetes resource configuration, broken out per container in the pod — the FalkorDB `service` container alongside its sidecars (`sidecar-exporter`, `sidecar-healthcheck`, `sidecar-oom-guard`, `monitor-sidecar`):

- **Working set** (`container_memory_working_set_bytes`) — the memory Kubernetes counts toward the limit (and uses for OOM decisions).
- **RSS** (`container_memory_rss`) — resident memory.
- **Limit** (`kube_pod_container_resource_limits`) — the hard cap; crossing it triggers an OOM kill.
- **Request** (`kube_pod_container_resource_requests`) — the guaranteed reservation.

Focus on the `service` series and watch the gap between its working set and its limit. When they converge, the pod is at risk of being OOM-killed and you should scale up.

---

## Commands & Queries

This row shows command throughput and latency — the core of query performance monitoring.

### Total Commands / sec
The per-second rate of all commands (`rate(redis_commands_total[1m])`), broken out by command and pod. This is overall instance throughput.

### Graph Commands / sec
The same as above but filtered to `GRAPH.*` commands only. This isolates your application's graph workload from internal Redis traffic, broken out by command and pod.

### Top Graph Commands by Time-Spent Rate
The top 20 graph commands ranked by total time spent (`rate(redis_commands_duration_seconds_total[5m])`). Whereas the throughput panels show *how often* commands run, this shows *where time goes*. A command with modest throughput can still dominate if each call is expensive.

### Avg Query Latency (Graph Commands)
Average latency per graph command, per pod — total time spent divided by number of calls. This covers all `GRAPH.*` commands (`QUERY`, `RO_QUERY`, `LIST`, `MEMORY`, `PROFILE`, `EXPLAIN`, etc.). Rising average latency is the clearest signal that queries are getting slower. Pair it with the **Slowlog** panel to find the offending queries.

### Total Time Spent by Command / sec
The instantaneous rate of cumulative time spent per command (`irate(redis_commands_duration_seconds_total[1m])`), across all commands (not just graph). Zero-value series are filtered out. Use it to see which command currently consumes the most server time.

### Average Time Spent by Command / sec
Time spent divided by command count per command and pod, across all commands. This is the per-command average latency for the whole instance, complementing the graph-only latency panel.

### Slowlog
A table of the last ten slow commands recorded by FalkorDB (`redis_slowlog_history_last_ten`). When latency panels spike, this is where you find the specific queries responsible so you can optimize them.

---

## System & Clients

This row covers the underlying resources and client connectivity.

### CPU
CPU usage as a percentage of the container's CPU limit (`container_cpu_usage_seconds_total / kube_pod_container_resource_limits`), with a reference line at 80%. Sustained values near the limit mean the workload is CPU-bound and the instance may need more cores.

> The percentage is relative to the **whole CPU limit**, not a single core. On a 4 vCPU instance, 100% means all 4 cores are fully saturated, 50% means the equivalent of 2 cores in use, and 25% means roughly 1 core. So a value sitting near the 80% line on a 4 vCPU instance means about 3.2 cores of sustained load.

### Total Memory Usage
Used memory in bytes (`redis_memory_used_bytes`) plotted against the configured maximum and an 80% warning line. Use it to see how close you are to the `maxmemory` limit over time, in absolute terms.

### Network I/O
Inbound and outbound network throughput in bytes/sec (`rate(redis_net_input_bytes_total[5m])` and `rate(redis_net_output_bytes_total[5m])`). High outbound traffic often corresponds to large query result sets; high inbound traffic corresponds to heavy writes or large requests.

### Connected/Blocked Clients
Plots connected clients against blocked clients (`redis_connected_clients` and `redis_blocked_clients`). A rising **blocked** count means clients are waiting (for example, on blocking commands), which can indicate contention or a stuck operation.

---

## Databases & Keys

### Graph Count Trend
The number of graphs on the master over time (`redis_falkordb_total_graph_count`). Unlike the **Graph count** stat panel, this shows the trend so you can watch tenant growth or spot mass deletions.

### Total Items per DB
The number of keys per logical database, per pod (`redis_db_keys`). Use it to track how your keyspace is distributed and how it grows over time.

---

## Logs

### Logs (service container)
Streams logs from the FalkorDB service container via the logs datasource, filtered to the selected namespace and pod. Use this panel to correlate metric anomalies with what the instance was logging at the same moment.

---

## How to Use the Dashboard

A practical workflow when investigating an issue:

1. **Scope the view.** Select the **pod** you want to inspect (and a **graph**, for the per-graph panels).
2. **Check the overview row.** Confirm uptime hasn't reset (no crash), and check memory usage and client counts.
3. **Follow the symptom:**
   - *Slow queries* → **Avg Query Latency** and **Top Graph Commands by Time-Spent Rate**, then drill into **Slowlog**.
   - *High memory* → **Memory Usage**, **Container Memory**, and the per-graph panels to find the heaviest graph.
   - *Instability* → **Memory Fragmentation Ratio**, **CPU**, and **Connected/Blocked Clients**.
4. **Correlate with logs.** Use the **Logs** panel to line up metric spikes with log events.
