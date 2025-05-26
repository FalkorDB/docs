---
title: "GRAPH.MEMORY USAGE"
description: "Report memory consumption statistics for a specific graph"
---

# GRAPH.MEMORY USAGE

The `GRAPH.MEMORY USAGE` command returns memory consumption details for a specific graph in **megabytes (MB)**. It enables users to analyze how much memory is being used by different components of the graph, including nodes, edges, indices, and matrix representations.

This is especially useful for debugging, performance optimization, and capacity planning.

## Syntax

```bash
GRAPH.MEMORY USAGE <graph-name> [SAMPLES <count>]
```

## Arguments

| Argument       | Description                                                                                                                              |
|----------------|------------------------------------------------------------------------------------------------------------------------------------------|
| `<graph-name>` | The name of the graph to inspect.                                                                                                        |       
| `SAMPLES <n>`  | *(Optional)* Number of samples to take when estimating memory usage. A higher number improves accuracy but increases computation time.   |

## Return

Returns an array of memory usage values, in **MB**, corresponding to different components:

| Field                                         | Description                                                   |
|-----------------------------------------------|---------------------------------------------------------------|
| `total_graph_sz_mb`                           | Total memory used by the graph                                |
| `label_matrices_sz_mb`                        | Memory used to hold label matrices                            |
| `relation_matrices_sz_mb`                     | Memory used to hold relation matrices                         |
| `amortized_node_block_sz_mb`                  | Memory used to hold nodes matrices                            |
| `amortized_node_attributes_by_label_sz_mb`    | Memory used to hold labeled node attributes, split by label   |
| `amortized_unlabeled_nodes_attributes_sz_mb`  | Memory used to hold non-labeled node attributes               |
| `amortized_edge_block_sz_mb`                  | Memory used to hold edges matrices                            |
| `amortized_edge_attributes_by_type_sz_mb`     | Memory used to hold lebeld edge attributes, split by label    |
| `indices_sz_mb`                               | Memory used by indices (if any)                               |

## Example

### Basic Usage
```bash
GRAPH.MEMORY USAGE myGraph
```

expected results
### With Sampling
```bash
GRAPH.MEMORY USAGE myGraph SAMPLES 500
```

## Notes

- If `SAMPLES` is not specified, the engine uses a default capped value internally.
- This command does not have side effects.
