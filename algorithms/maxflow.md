---
title: "Max Flow"
description: "Max Flow"
parent: "Algorithms"
nav_order: 8
---

# Max Flow

## Overview

The Max Flow algorithm computes the maximum amount of flow that can be routed through a directed, weighted graph from one or more **source** nodes to one or more **sink** (target) nodes. Edge weights represent capacities — the upper bound on how much flow an edge can carry.

Max Flow is commonly applied in scenarios such as:
- Network throughput optimization (bandwidth, pipelines, logistics)
- Traffic routing and congestion analysis
- Supply chain and distribution planning
- Bipartite matching and scheduling problems

## Algorithm Details

The procedure implements a capacity-scaling max-flow algorithm over the subgraph induced by the specified node labels and relationship types. It builds a residual graph from the selected edges (using the configured capacity property), then repeatedly finds augmenting paths from the source super-node to the sink super-node and pushes flow along them until no augmenting path exists.

Multiple source or sink nodes are supported by introducing a virtual super-source connected to every source node, and a virtual super-sink connected from every sink node, each with infinite capacity.

The algorithm returns the set of nodes and edges that carry positive flow, together with the per-edge flow values and the total maximum flow.

### Performance

The algorithm operates with a time complexity of **O(V · E²)**, where:
- **|V|** represents the total number of nodes in the subgraph
- **|E|** represents the total number of edges in the subgraph

For sparse graphs this is typically much faster in practice.

## Syntax

```cypher
CALL algo.maxFlow(config)
YIELD nodes, edges, edgeFlows, maxFlow
```

### Parameters

The procedure accepts a required configuration `Map` with the following parameters:

| Name                 | Type   | Default       | Description                                                                 |
|----------------------|--------|---------------|-----------------------------------------------------------------------------|
| `sourceNodes`        | Array  | *(required)*  | One or more node objects that act as flow sources                           |
| `targetNodes`        | Array  | *(required)*  | One or more node objects that act as flow sinks                             |
| `relationshipTypes`  | Array  | *(required)*  | Relationship types that define the edges of the flow network                |
| `capacityProperty`   | String | `'capacity'`  | Name of the numeric edge property used as the edge capacity                 |
| `nodeLabels`         | Array  | All labels    | Array of node labels used to restrict which nodes are included              |

### Return Values

The procedure yields a single record with the following fields:

| Name        | Type    | Description                                                                        |
|-------------|---------|------------------------------------------------------------------------------------|
| `nodes`     | Array   | All node entities that participate in the max-flow solution (carry positive flow)  |
| `edges`     | Array   | All edge entities that carry positive flow                                         |
| `edgeFlows` | Array   | Numeric flow value for each edge in `edges`, in the same order                    |
| `maxFlow`   | Integer | The total maximum flow from all source nodes to all sink nodes                     |

## Examples

Consider this pipeline network:

```
(A) --[cap:10]--> (B) --[cap:8]--> (C)
 \                                  ^
  \----------[cap:5]---------------/
```

Node **A** is the source, node **C** is the sink. There are two routes from A to C:
- **A → C** directly, with capacity 5
- **A → B → C**, with a bottleneck of 8 (min of 10 and 8)

The maximum flow is therefore **13**.

### Create the Graph

```cypher
CREATE
  (a:Node {name: 'A'}),
  (b:Node {name: 'B'}),
  (c:Node {name: 'C'}),

  (a)-[:PIPE {cap: 10}]->(b),
  (a)-[:PIPE {cap: 5}]->(c),
  (b)-[:PIPE {cap: 8}]->(c)
```

### Example: Compute the maximum flow between two nodes

```cypher
MATCH (s:Node {name: 'A'}), (t:Node {name: 'C'})
CALL algo.maxFlow({
    sourceNodes:       [s],
    targetNodes:       [t],
    capacityProperty:  'cap',
    relationshipTypes: ['PIPE']
})
YIELD nodes, edges, edgeFlows, maxFlow
RETURN maxFlow
```

#### Expected Results

| maxFlow |
|---------|
| `13`    |

### Example: Inspect per-edge flow on the solution

```cypher
MATCH (s:Node {name: 'A'}), (t:Node {name: 'C'})
CALL algo.maxFlow({
    sourceNodes:       [s],
    targetNodes:       [t],
    capacityProperty:  'cap',
    relationshipTypes: ['PIPE']
})
YIELD edges, edgeFlows
UNWIND range(0, size(edges) - 1) AS i
RETURN
    startNode(edges[i]).name AS from,
    endNode(edges[i]).name   AS to,
    edgeFlows[i]             AS flow
```

#### Expected Results

| from | to  | flow |
|------|-----|------|
| `A`  | `B` | `8`  |
| `A`  | `C` | `5`  |
| `B`  | `C` | `8`  |

### Example: Restrict the subgraph by node label

When the graph contains multiple node labels, use `nodeLabels` to limit the algorithm to a specific subset of nodes:

```cypher
MATCH (s:Intersection {name: 'Source'}), (t:Intersection {name: 'Sink'})
CALL algo.maxFlow({
    sourceNodes:       [s],
    targetNodes:       [t],
    capacityProperty:  'bandwidth',
    nodeLabels:        ['Intersection'],
    relationshipTypes: ['CONNECTS']
})
YIELD nodes, maxFlow
RETURN size(nodes) AS participatingNodes, maxFlow
```

### Example: Multiple sources and multiple sinks

`sourceNodes` and `targetNodes` each accept arrays, allowing multi-commodity-style problems to be modelled with virtual super-nodes:

```cypher
MATCH
    (s1:Node {name: 'SourceA'}),
    (s2:Node {name: 'SourceB'}),
    (t:Node  {name: 'Sink'})
CALL algo.maxFlow({
    sourceNodes:       [s1, s2],
    targetNodes:       [t],
    capacityProperty:  'cap',
    relationshipTypes: ['PIPE']
})
YIELD maxFlow
RETURN maxFlow
```
