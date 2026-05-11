---
title: "Harmonic Centrality"
description: "Measures node importance by summing inverse shortest-path distances to all reachable nodes, making it robust on disconnected graphs."
parent: "Algorithms"
nav_order: 8
---

# Harmonic Centrality

## Introduction

Harmonic Centrality is a graph algorithm that measures the importance of each node based on its average closeness to all other reachable nodes in the graph. Unlike traditional Closeness Centrality, which breaks down on disconnected graphs, Harmonic Centrality uses the **sum of inverse distances** and naturally handles unreachable nodes by treating their contribution as zero (since 1/∞ = 0).

This makes it the preferred centrality measure when working with graphs that may not be fully connected.

## Algorithm Overview

For each node *u*, the harmonic centrality score is:

```
H(u) = Σ(v ≠ u) 1 / d(u, v)
```

where *d(u, v)* is the shortest-path distance from *u* to *v*. If *v* is unreachable from *u*, the term is 0. The score is **not** normalized by default — the raw sum of inverse distances is returned.

Nodes with high harmonic centrality scores are "close" to many other nodes on average, making them effective hubs for information spread, influence, or access within the graph.

The algorithm is implemented using [LAGraph](https://lagraph.readthedocs.io/) and [GraphBLAS](https://graphblas.org/) sparse matrix operations for high-performance computation.

## Syntax

```cypher
CALL algo.HarmonicCentrality([config])
YIELD node, score, reachable
```

The configuration argument is optional. Pass `NULL` or omit the argument to run on the full graph.

### Parameters

| Name                | Type  | Default | Description                                                                                   |
|---------------------|-------|---------|-----------------------------------------------------------------------------------------------|
| `nodeLabels`        | Array | `[]`    | *(Optional)* List of node labels to include. Only nodes with these labels receive scores and are traversed. Raises an error if a label does not exist. |
| `relationshipTypes` | Array | `[]`    | *(Optional)* List of relationship types to traverse. Only edges of these types are followed. Raises an error if a type does not exist. |

### Yield

| Name         | Type    | Description                                                                                     |
|--------------|---------|-------------------------------------------------------------------------------------------------|
| `node`       | Node    | The node being evaluated.                                                                       |
| `score`      | Float   | The harmonic centrality score: sum of inverse shortest-path distances to all reachable nodes.   |
| `reachable`  | Integer | *(Optional)* Estimated number of nodes reachable from this node. Only populated when yielded.  |

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
| `Bob`     | 1.83  |
| `Charlie` | 1.83  |
| `David`   | 1.00  |
| `Eve`     | 0.00  |

Alice has the highest score because she has direct or short-path access to all other nodes.

### Filtering by Label and Relationship Type

```cypher
CALL algo.HarmonicCentrality({
    nodeLabels:        ['Person'],
    relationshipTypes: ['KNOWS']
})
YIELD node, score, reachable
RETURN node.name AS person, score, reachable
ORDER BY score DESC
```

### Handling Disconnected Graphs

Harmonic Centrality works correctly even when the graph has multiple disconnected components. Nodes in isolated components simply contribute 0 to the scores of nodes they cannot reach:

```cypher
CREATE
  (a:Station {name: 'Central'}),
  (b:Station {name: 'North'}),
  (c:Station {name: 'South'}),
  (d:Station {name: 'Island'}),  // disconnected
  (a)-[:LINE]->(b),
  (a)-[:LINE]->(c)
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
| `Central` | 2.00  |
| `North`   | 1.00  |
| `South`   | 1.00  |
| `Island`  | 0.00  |

`Island` has a score of 0 because it cannot reach any other node, not because the algorithm fails.

## Usage Notes

- **Directed graph**: The algorithm treats the graph as **directed**. A path from *u* to *v* does not imply a path from *v* to *u*.
- **Disconnected graphs**: Harmonic Centrality handles disconnected graphs correctly. Unreachable node pairs contribute 0 to the score rather than causing errors.
- **Score interpretation**: Higher scores indicate nodes that are, on average, closer to more nodes. A score of 0 means the node cannot reach any other node.
- **`reachable` field**: The `reachable` yield provides an estimated count of nodes reachable from each node. Yield it explicitly when you need this information, as it incurs additional computation.
- **Label/type filtering**: When `nodeLabels` or `relationshipTypes` are provided, only matching nodes and edges participate in the computation. All named labels and types must exist in the graph, or an error is returned.
- **Performance**: The algorithm uses sparse matrix operations (GraphBLAS/LAGraph) and scales well on large graphs.

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="What is the call syntax for Harmonic Centrality?"
  a1="Use `CALL algo.HarmonicCentrality() YIELD node, score`. Optionally pass a config map: `CALL algo.HarmonicCentrality({nodeLabels: ['Label'], relationshipTypes: ['TYPE']}) YIELD node, score, reachable`."
  q2="Why use Harmonic Centrality instead of Closeness Centrality?"
  a2="Classic Closeness Centrality divides by the total distance to all nodes, which becomes undefined (division by zero or infinity) when the graph is disconnected. Harmonic Centrality uses the **sum of inverse distances**, so unreachable nodes simply contribute 0 and the score remains well-defined for all nodes."
  q3="What does a score of 0 mean?"
  a3="A score of 0 means the node cannot reach any other node in the graph under the current label/relationship filters. This is common for sink nodes in directed graphs or for isolated nodes."
  q4="When should I use Harmonic Centrality vs Betweenness Centrality?"
  a4="Use **Harmonic Centrality** to find nodes that are close to many others (good hubs for spreading information quickly). Use **[Betweenness Centrality](./betweenness-centrality.md)** to find nodes that act as critical bridges between different parts of the graph."
  q5="Does the `reachable` yield slow down the query?"
  a5="Yes, slightly. The `reachable` field requires a second pass over the result vectors. Only include it in your `YIELD` clause when you actually need the reachability estimate."
%}
