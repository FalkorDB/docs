---
title: "GRAPH.MEMORY"
description: >
    The GRAPH.MEMORY USAGE command returns detailed memory usage statistics for the specified graph. This command provides insight into how much memory is used by various internal data structures such as nodes, edges, schemas, and indices. It enables users to analyze memory consumption at the graph level, reporting statistics in megabytes (MB). This is useful for debugging, monitoring, performance optimization, and capacity planning in FalkorDB deployments.
parent: "Commands"
nav_order: 11
---

# GRAPH.MEMORY
The `GRAPH.MEMORY` command returns detailed memory consumption statistics for a specific graph in **megabytes (MB)**. It provides insight into how much memory is used by various internal data structures such as nodes, edges, schemas, indices, and matrix representations. This command can be used to monitor memory consumption at the graph level, making it especially useful for debugging, monitoring, performance optimization, and capacity planning in FalkorDB deployments.

## Syntax

```bash
GRAPH.MEMORY USAGE <graph-name> [SAMPLES <count>]
```

## Arguments

| Argument       | Description                                                                                                                              |
|----------------|------------------------------------------------------------------------------------------------------------------------------------------|
| `<graph-name>` | The name of the graph to inspect.                                                                                                        |
| `SAMPLES <n>`  | *(Optional)* Number of samples to take when estimating memory usage. A higher number improves accuracy but increases computation time. The samples are averaged to estimate the total size. Defaults to 100 if not specified. The value is clamped to the range [1, 10000]. |

## Return

The command returns a set of key-value pairs, where each pair represents a specific memory metric and its value (in MB), corresponding to different components of the graph. In RESP2, this is encoded as a flat array of alternating field names and values:

| Metric Name / Field                           | Type    | Description                                                       |
|-----------------------------------------------|---------|-------------------------------------------------------------------|
| `total_graph_sz_mb`                           | integer | Total memory consumed by the graph.                               |
| `label_matrices_sz_mb`                        | integer | Amount of memory used by label matrices (node labels tracking).   |
| `relation_matrices_sz_mb`                     | integer | Amount of memory used by relationship type matrices (graph topology tracking). |
| `amortized_node_block_sz_mb`                  | integer | Memory used by node blocks (amortized node storage).              |
| `amortized_node_attributes_by_label_sz_mb`    | map     | Memory used by node attributes, broken down by label. Each key is a label name and its value is the memory in MB. |
| `amortized_unlabeled_nodes_attributes_sz_mb`  | integer | Memory used by attributes of nodes with no label.                 |
| `amortized_edge_block_sz_mb`                  | integer | Memory used by edge blocks (amortized edge storage).              |
| `amortized_edge_attributes_by_type_sz_mb`     | map     | Memory used by edge attributes, broken down by relationship type. Each key is a relationship type name and its value is the memory in MB. |
| `indices_sz_mb`                               | integer | Amount of memory consumed by indices (if any).                    |

## Examples

### Basic Usage

{% capture shell_0 %}
GRAPH.MEMORY USAGE myGraph
{% endcapture %}

{% capture javascript_0 %}
import { FalkorDB } from 'falkordb';
const db = await FalkorDB.connect({
  socket: { host: 'localhost', port: 6379 }
});
const graph = db.selectGraph('myGraph');
const memoryInfo = await graph.memoryUsage();
console.log(memoryInfo);
{% endcapture %}

{% include code_tabs.html id="memory_basic_tabs" shell=shell_0 javascript=javascript_0 %}

### With Sampling

{% capture shell_1 %}
GRAPH.MEMORY USAGE myGraph SAMPLES 500
{% endcapture %}

{% capture javascript_1 %}
const memoryInfo = await graph.memoryUsage({ samples: 500 });
console.log(memoryInfo);
{% endcapture %}

{% include code_tabs.html id="memory_samples_tabs" shell=shell_1 javascript=javascript_1 %}

### Sample Output

```sh
127.0.0.1:6379> GRAPH.MEMORY USAGE flights
 1) "total_graph_sz_mb"
 2) (integer) 1086
 3) "label_matrices_sz_mb"
 4) (integer) 96
 5) "relation_matrices_sz_mb"
 6) (integer) 64
 7) "amortized_node_block_sz_mb"
 8) (integer) 120
 9) "amortized_node_attributes_by_label_sz_mb"
10) 1) "Airport"
    2) (integer) 35
    3) "City"
    4) (integer) 12
11) "amortized_unlabeled_nodes_attributes_sz_mb"
12) (integer) 0
13) "amortized_edge_block_sz_mb"
14) (integer) 54
15) "amortized_edge_attributes_by_type_sz_mb"
16) 1) "ROUTE"
    2) (integer) 68
17) "indices_sz_mb"
18) (integer) 752
```

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="What units does GRAPH.MEMORY report in?"
  a1="All memory values are reported in **megabytes (MB)**."
  q2="What does the SAMPLES parameter do?"
  a2="The `SAMPLES` parameter controls how many samples are taken when estimating memory usage. Higher values improve accuracy but increase computation time. The default is 100, and valid range is 1 to 10000."
  q3="What is the most useful metric for capacity planning?"
  a3="The `total_graph_sz_mb` metric gives the total memory consumed by the graph. For more detailed analysis, examine per-label and per-relationship-type breakdowns to identify which parts of your graph use the most memory."
  q4="Why might indices_sz_mb be large relative to the graph?"
  a4="Indexes store additional data structures for fast lookups. If you have many indexes or indexes on high-cardinality properties, the index memory can be significant. Only create indexes that are actually used by your queries."
  q5="Can I run GRAPH.MEMORY on a production system?"
  a5="Yes, but be aware that higher `SAMPLES` values increase computation time. Use a moderate sample count for routine monitoring and higher counts only for detailed analysis during maintenance windows."
%}
