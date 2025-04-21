---
Command: "GRAPH.MEMORY"
Description: >
    Returns detailed memory usage statistics for a specified graph. Useful for monitoring and optimizing internal structures like nodes, edges, schemas, and indices within FalkorDB deployments.
    This information is useful for debugging, monitoring, and optimizing graph workloads in FalkorDB deployments.
Parent: "Commands"
---

# GRAPH.MEMORY

Returns detailed memory usage metrics for a given graph. This command helps diagnose memory bottlenecks and assess storage overhead across internal components such as:

- Label and relation matrices
- Node and edge storage
- Indices and schema allocations

You can optionally sample a subset of graph entities to estimate usage. The default sample size is 100 entities.

## Syntax

`GRAPH.MEMORY USAGE <graph_id> [SAMPLES <count>]`
- graph_id: ID of the target graph.
- SAMPLES <count> (optional): Number of entities to sample for estimation (default: 100).

## Example
```
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

The command returns an array of key-value pairs, each representing a specific memory metric and its value (in MB).

| Metric Name                    | Type    | Description                                        |
|:-------------------------------|:--------|:---------------------------------------------------|
| `total_graph_sz_mb`            | integer | Total memory consumed by the graph.                |
| `label_matrices_sz_mb`         | integer | Amount of memory used for node labels tracking.    |
| `relation_matrices_sz_mb`      | integer | Amount of memory used for graph topology tracking. |
| `amortized_node_storage_sz_mb` | integer | Amount of memory used for nodes storage.           |
| `amortized_edge_storage_sz_mb` | integer | Amount of memory used for relationships storage.   |
| `indices_sz_mb`                | integer | Amount of memory consumed by indices.              |
