---
title: "Harmonic Centrality"
description: "Measures node importance by summing inverse shortest-path
distances to all reachable nodes, making it robust on disconnected graphs."
parent: "Algorithms"
nav_order: 8
---

# Harmonic Centrality

## Introduction

Harmonic Centrality is a graph algorithm that measures the "importance" of each
node based on its average closeness to all other reachable nodes in the graph.
Unlike traditional Closeness Centrality, which does not work on disconnected
graphs, Harmonic Centrality uses the **sum of inverse distances** and naturally
handles unreachable nodes by treating their contribution as zero.

This makes it the preferred centrality measure when working with graphs that
may not be fully connected.

## Algorithm Overview

For each node *u*, the harmonic centrality score is:

```
H(u) = Σ(v ≠ u) 1 / d(u, v)
```

where *d(u, v)* is the shortest-path distance from *u* to *v*. If *v* is
unreachable from *u*, the term is 0.

Nodes with high harmonic centrality scores are "close" to many other nodes on
average, making them effective hubs for information spread, influence, or
access within the graph.

> **Note:** FalkorDB computes harmonic centrality using an **approximate**
> algorithm based on HyperLogLog (HLL) sketches and GraphBLAS sparse matrix
> operations. Scores are estimates, not exact values, though they are
> typically very close to the true score for large graphs.

## Syntax

```cypher
CALL algo.HarmonicCentrality([config])
YIELD node, score, reachable
```

The configuration argument is optional. Pass `NULL` or omit the argument to run on the full graph.

### Parameters

| Name                | Type  | Default | Description                                                                                                                                            |
|---------------------|-------|---------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| `nodeLabels`        | Array | `[]`    | *(Optional)* List of node labels to include. Only nodes with these labels receive scores and are traversed. Raises an error if a label does not exist. |
| `relationshipTypes` | Array | `[]`    | *(Optional)* List of relationship types to traverse. Only edges of these types are followed. Raises an error if a type does not exist.                 |

### Yield

| Name         | Type    | Description                                                                                     |
|--------------|---------|-------------------------------------------------------------------------------------------------|
| `node`       | Node    | The node being evaluated.                                                                       |
| `score`      | Float   | The harmonic centrality score: sum of inverse shortest-path distances to all reachable nodes.   |
| `reachable`  | Integer | *(Optional)* Estimated number of nodes reachable from this node via HLL sketch. Only populated when yielded. |

## Examples

### Basic Usage — Full Graph

Create a small directed network:

```cypher
CREATE
  (a:Person {name: 'Alice'}),
  (b:Person {name: 'Bob'}),
  (c:Person {name: 'Charlie'}),
  (d:Person {name: 'David'}),
  (e:Person {name: 'Eve'}),
  (a)-[:KNOWS]->(b),
  (a)-[:KNOWS]->(c),
  (b)-[:KNOWS]->(d),
  (c)-[:KNOWS]->(d),
  (d)-[:KNOWS]->(e)
```

Run harmonic centrality across all nodes and relationships:

```cypher
CALL algo.HarmonicCentrality()
YIELD node, score
RETURN node.name AS person, score
ORDER BY score DESC
```

Expected results:

| person    | score |
|-----------|-------|
| `Alice`   | 2.83  |
| `Bob`     | 1.50  |
| `Charlie` | 1.50  |
| `David`   | 1.00  |
| `Eve`     | 0.00  |

Alice has the highest score because she can reach all other nodes, and directly
reaches two of them. Bob and Charlie each reach only David (d=1) and Eve (d=2),
giving `1/1 + 1/2 = 1.50`.

### Filtering by Label and Relationship Type

```cypher
CREATE
  (a:Station {name: 'Central'}),
  (b:Station {name: 'North'}),
  (c:Station {name: 'South'}),
  (d:Station {name: 'Island'}),
  (e:Person  {name: 'John'}),
  (a)-[:LINE]->(b),
  (a)-[:LINE]->(c),
  (c)-[:LINE]->(d),
  (a)-[:SERVICES]->(e)
```

```cypher
CALL algo.HarmonicCentrality({
    nodeLabels:        ['Station'],
    relationshipTypes: ['LINE']
})
YIELD node, score
RETURN node.name AS station, score
ORDER BY score DESC
```

Expected results:

| station   | score |
|-----------|-------|
| `Central` | 2.50  |
| `North`   | 0.00  |
| `South`   | 1.00  |
| `Island`  | 0.00  |

John is not given a score, and the connection to John does not affect the score of Central.

## Usage Notes

- **Directed graph**: The algorithm treats the graph as **directed**. A path from *u* to *v* does not imply a path from *v* to *u*.
- **Score interpretation**: Higher scores indicate nodes that are, on average, closer to more nodes. A score of 0 means the node cannot reach any other node.
- **`reachable` field**: The `reachable` yield provides an estimated count of nodes reachable from each node via HLL sketch. Yield it explicitly when you need this information.
- **Label/type filtering**: When `nodeLabels` or `relationshipTypes` are provided, only matching nodes and edges participate in the computation. All named labels and types must exist in the graph, or an error is returned.
- **Performance**: The algorithm uses sparse matrix operations and scales well on large graphs.

