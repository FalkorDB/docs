---
title: "GRAPH.MEMORY"
description: >
    The GRAPH.MEMORY command returns detailed memory usage statistics for the specified graph.
    This command can be used to monitor memory consumption at the graph level,
    providing insight into how much memory is used by various internal data structures such as
    nodes, edges, schemas, and indices.

    This information is useful for debugging, monitoring, and optimizing graph workloads in FalkorDB deployments.
parent: "Commands"
---

# GRAPH.MEMORY

The GRAPH.MEMORY command returns detailed memory usage statistics for the specified graph.
This command can be used to monitor memory consumption at the graph level,
providing insight into how much memory is used by various internal data structures such as
nodes, edges, schemas, and indices.

This information is useful for debugging, monitoring, and optimizing graph workloads in FalkorDB deployments.

The optional `SAMPLES` option can be provided, where count is the number of sampled graph entities.
The samples are averaged to estimate the total size. By default, this option is set to 100.


Usage: `GRAPH.MEMORY USAGE <graph_id> [SAMPLES <count>]`

```sh
127.0.0.1:6379> GRAPH.MEMORY USAGE flights
 1) "total_graph_sz_mb"
 2) (integer) 1086
 3) "label_matrices_sz_mb"
 4) (integer) 96
 5) "relation_matrices_sz_mb"
 6) (integer) 64
 7) "amortized_node_storage_sz_mb"
 8) (integer) 120
 9) "amortized_edge_storage_sz_mb"
10) (integer) 54
11) "indices_sz_mb"
12) (integer) 752
```

## Output

The command returns an array of key-value pairs, where each pair represents a specific memory metric and its value (in MB).

| Metric Name                    | Type    | Description                                        |
|:-------------------------------|:--------|:---------------------------------------------------|
| `total_graph_sz_mb`            | integer | Total memory consumed by the graph.                |
| `label_matrices_sz_mb`         | integer | Amount of memory used for node labels tracking.    |
| `relation_matrices_sz_mb`      | integer | Amount of memory used for graph topology tracking. |
| `amortized_node_storage_sz_mb` | integer | Amount of memory used for nodes storage.           |
| `amortized_edge_storage_sz_mb` | integer | Amount of memory used for relationships storage.   |
| `indices_sz_mb`                | integer | Amount of memory consumed by indices.              |

