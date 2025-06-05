---
title: "Betweenness Centrality"
description: "Measures the importance of nodes based on the number of shortest paths that pass through them."
parent: "Algorithms"
---

# Betweenness Centrality

## Introduction

Betweenness Centrality is a graph algorithm that quantifies the importance of a node based on the number of shortest paths that pass through it. Nodes that frequently occur on shortest paths between other nodes have higher betweenness centrality scores. This makes the algorithm useful for identifying **key connectors** or **brokers** within a network.

## Algorithm Overview

The core idea of Betweenness Centrality is that a node is more important if it lies on many of the shortest paths connecting other nodes. It’s particularly useful in understanding information flow or communication efficiency in a graph.

For example, in a social network, a person who frequently connects otherwise unconnected groups would have high betweenness centrality.

## Syntax

The procedure has the following call signature:
```cypher
CALL algo.betweenness({
  nodeLabels: [<node_label>],
  relationshipTypes: [<relationship_type>]
})
YIELD node, score
```

### Parameters

| Name                  | Type    | Description                                     | Default |
|-----------------------|---------|-------------------------------------------------|---------|
| `nodeLabels`          | Array   | *(Optional)* List of Strings representing node labels        | []      |
| `relationshipTypes`   | Array   | *(Optional)* List of Strings representing relationship types | []      |

### Yield

| Name    | Type  | Description                                   |
|---------|-------|-----------------------------------------------|
| `node`  | Node  | The node being evaluated                      |
| `score` | Float | The betweenness centrality score for the node |

## Example:

Lets take this Social Graph as an example:
![Social Graph](../images/between.png)

### Create the Graph

```cypher
CREATE 
  (a:Person {name: 'Alice'}),
  (b:Person {name: 'Bob'}),
  (c:Person {name: 'Charlie'}),
  (d:Person {name: 'David'}),
  (e:Person {name: 'Emma'}),
  (a)-[:FRIEND]->(b),
  (b)-[:FRIEND]->(c),
  (b)-[:FRIEND]->(d),
  (c)-[:FRIEND]->(e),
  (d)-[:FRIEND]->(e)
```

### Run Betweenness Centrality - Sort Persons by importance based on FRIEND relationship

```cypher
CALL algo.betweenness({
    'nodeLabels': ['Person'], 
    'relationshipTypes': ['FRIEND']
    })
YIELD node, score
RETURN node.name AS person, score
ORDER BY score DESC
```

Expected result:

| person    | score |
|-----------|--------|
| `Bob`     | 6      |
| `Charlie` | 2      |
| `David`   | 2      |
| `Alice`   | 0      |
| `Emma`    | 0      |

## Usage Notes

- Scores are based on **all shortest paths** between node pairs.
- Nodes that serve as bridges between clusters tend to score higher.
- Can be computationally expensive on large, dense graphs.