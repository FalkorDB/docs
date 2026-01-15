---
title: "GRAPH.MEMORY"
description: >
    The GRAPH.MEMORY USAGE command returns detailed memory usage statistics for the specified graph. This command provides insight into how much memory is used by various internal data structures such as nodes, edges, schemas, and indices. It enables users to analyze memory consumption at the graph level, reporting statistics in megabytes (MB). This is useful for debugging, monitoring, performance optimization, and capacity planning in FalkorDB deployments.
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';


# GRAPH.MEMORY
The `GRAPH.MEMORY` command returns detailed memory consumption statistics for a specific graph in **megabytes (MB)**. It provides insight into how much memory is used by various internal data structures such as nodes, edges, schemas, indices, and matrix representations. This command can be used to monitor memory consumption at the graph level, making it especially useful for debugging, monitoring, performance optimization, and capacity planning in FalkorDB deployments.

## Syntax

```bash
GRAPH.MEMORY USAGE <graph-name> [SAMPLES <count>]
```

Usage: `GRAPH.MEMORY USAGE <graph_id> [SAMPLES <count>]`

## Arguments

| Argument       | Description                                                                                                                              |
|----------------|------------------------------------------------------------------------------------------------------------------------------------------|
| `<graph-name>` | The name of the graph to inspect (also referred to as `<graph_id>`).                                                                     |
| `SAMPLES <n>`  | *(Optional)* Number of samples to take when estimating memory usage. A higher number improves accuracy but increases computation time. The samples are averaged to estimate the total size. By default, this option is set to 100 if not specified. |

## Return

The command returns an array of key-value pairs, where each pair represents a specific memory metric and its value (in MB), corresponding to different components of the graph:

| Metric Name / Field                           | Type    | Description                                                       |
|-----------------------------------------------|---------|-------------------------------------------------------------------|
| `total_graph_sz_mb`                           | integer | Total memory consumed by the graph.                               |
| `label_matrices_sz_mb`                        | integer | Amount of memory used by label matrices (node labels tracking).   |
| `relation_matrices_sz_mb`                     | integer | Amount of memory used by relationship type matrices (graph topology tracking). |
| `amortized_node_block_sz_mb`                  | integer | Memory used by nodes (amortized node storage).                    |
| `amortized_node_storage_sz_mb`                | integer | Amount of memory used for nodes storage (alternative naming).     |
| `amortized_node_attributes_by_label_sz_mb`    | integer | Memory used by node attributes, split by node label.              |
| `amortized_unlabeled_nodes_attributes_sz_mb`  | integer | Memory used by node attributes with no label.                     |
| `amortized_edge_block_sz_mb`                  | integer | Memory used by edges (amortized edge storage).                    |
| `amortized_edge_storage_sz_mb`                | integer | Amount of memory used for relationships storage (alternative naming). |
| `amortized_edge_attributes_by_type_sz_mb`     | integer | Memory used by edge attributes, split by relationship type.       |
| `indices_sz_mb`                               | integer | Amount of memory consumed by indices (if any).                    |

*Note*: Metrics like `amortized_node_block_sz_mb` and `amortized_node_storage_sz_mb` are alternative names for the same data; both are included for clarity.

## Examples

### Basic Usage


<Tabs groupId="programming-language">
  <TabItem value="shell" label="Shell">

```bash
GRAPH.MEMORY USAGE myGraph
```

  </TabItem>
  <TabItem value="javascript" label="Javascript">

```javascript
import { FalkorDB } from 'falkordb';
const db = await FalkorDB.connect({
  socket: { host: 'localhost', port: 6379 }
});
const graph = db.selectGraph('myGraph');
const memoryInfo = await graph.memoryUsage();
console.log(memoryInfo);
```

  </TabItem>
</Tabs>

### With Sampling


<Tabs groupId="programming-language">
  <TabItem value="shell" label="Shell">

```bash
GRAPH.MEMORY USAGE myGraph SAMPLES 500
```

  </TabItem>
  <TabItem value="javascript" label="Javascript">

```javascript
const memoryInfo = await graph.memoryUsage({ samples: 500 });
console.log(memoryInfo);
```

  </TabItem>
</Tabs>

### Sample Output

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
