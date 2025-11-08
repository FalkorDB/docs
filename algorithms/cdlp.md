---
title: "Community Detection using Label Propagation (CDLP)"
description: "Community Detection using Label Propagation (CDLP)"
parent: "Algorithms"
---

# Community Detection using Label Propagation (CDLP)

## Overview

The Community Detection using Label Propagation (CDLP) algorithm identifies communities in networks by propagating labels through the graph structure.
Each node starts with a unique label, and through iterative propagation, nodes adopt the most frequent label among their neighbors, naturally forming communities where densely connected nodes share the same label.

CDLP serves as a powerful algorithm in scenarios such as:

* Social network community detection
* Biological network module identification
* Web page clustering and topic detection
* Market segmentation analysis
* Fraud detection networks

## Algorithm Details

CDLP initializes by assigning each node a unique label (typically its node ID).
The algorithm then iteratively updates each node's label to the most frequent label among its neighbors.
During each iteration, nodes are processed in random order to avoid deterministic bias.
The algorithm continues until labels stabilize (no changes occur) or a maximum number of iterations is reached.
The final labels represent community assignments, where nodes sharing the same label belong to the same community.

The algorithm's strength lies in its ability to discover communities without requiring prior knowledge of the number of communities or their sizes.
It runs in near-linear time and mimics epidemic contagion by spreading labels through the network.

### Performance

CDLP operates with a time complexity of **O(m + n)** per iteration, where:

* **n** represents the total number of nodes
* **m** represents the total number of edges

The algorithm typically converges within a few iterations, making it highly efficient for large-scale networks.

## Syntax

```cypher
CALL algo.labelPropagation([config])
```

### Parameters

The procedure accepts an optional configuration `Map` with the following parameters:

| Name                | Type    | Default                | Description                                                                      |
|---------------------|---------|------------------------|----------------------------------------------------------------------------------|
| `nodeLabels`        | Array   | All labels             | Array of node labels to filter which nodes are included in the computation       |
| `relationshipTypes` | Array   | All relationship types | Array of relationship types to define which edges are traversed                  |
| `maxIterations`     | Integer | 10                     | Maximum number of iterations to run the algorithm                                |

### Return Values

The procedure returns a stream of records with the following fields:

| Name          | Type    | Description                                                         |
|---------------|---------|---------------------------------------------------------------------|
| `node`        | Node    | The node entity included in the community                           |
| `communityId` | Integer | Identifier of the community the node belongs to                     |

## Examples

Let's take this Social Network as an example:

```text
    (Alice)---(Bob)---(Charlie)  (Kate)
       |       |         |
    (Diana)    |      (Eve)---(Frank)
       |       |         |      |
    (Grace)--(Henry)   (Iris)--(Jack)
```

There are 3 different communities that should emerge from this network:

* Alice, Bob, Charlie, Diana, Grace, Henry
* Eve, Frank, Iris, Jack
* Any isolated nodes

### Create the Graph

```cypher
CREATE 
  (alice:Person {name: 'Alice'}),
  (bob:Person {name: 'Bob'}),
  (charlie:Person {name: 'Charlie'}),
  (diana:Person {name: 'Diana'}),
  (eve:Person {name: 'Eve'}),
  (frank:Person {name: 'Frank'}),
  (grace:Person {name: 'Grace'}),
  (henry:Person {name: 'Henry'}),
  (iris:Person {name: 'Iris'}),
  (jack:Person {name: 'Jack'}),
  (kate:Person {name: 'Kate'}),

  (alice)-[:KNOWS]->(bob),
  (bob)-[:KNOWS]->(charlie),
  (alice)-[:KNOWS]->(diana),
  (bob)-[:KNOWS]->(henry),
  (diana)-[:KNOWS]->(grace),
  (grace)-[:KNOWS]->(henry),
  (charlie)-[:KNOWS]->(eve),
  (eve)-[:KNOWS]->(frank),
  (eve)-[:KNOWS]->(iris),
  (frank)-[:KNOWS]->(jack),
  (iris)-[:KNOWS]->(jack)
```

### Example: Detect all communities in the network

```cypher
CALL algo.labelPropagation() YIELD node, communityId RETURN node.name AS name, communityId ORDER BY communityId, name 
```

#### Expected Results

| name       | communityId |
|------------|-------------|
| `Alice`    | 0           |
| `Bob`      | 0           |
| `Charlie`  | 0           |
| `Diana`    | 0           |
| `Grace`    | 0           |
| `Henry`    | 0           |
| `Eve`      | 2           |
| `Frank`    | 2           |
| `Iris`     | 2           |
| `Jack`     | 2           |
| `Kate`     | 10          |

### Example: Detect communities with limited iterations

```cypher
CALL algo.labelPropagation({maxIterations: 5}) YIELD node, communityId
```

### Example: Focus on specific node types

```cypher
CALL algo.labelPropagation({nodeLabels: ['Person']}) YIELD node, communityId
```

### Example: Use only certain relationship types

```cypher
CALL algo.labelPropagation({relationshipTypes: ['KNOWS', 'FRIENDS_WITH']}) YIELD node, communityId
```

### Example: Combine node and relationship filtering

```cypher
CALL algo.labelPropagation({
  nodeLabels: ['Person'], 
  relationshipTypes: ['KNOWS']
}) YIELD node, communityId
```

### Example: Group communities together

```cypher
CALL algo.labelPropagation() YIELD node, communityId 
RETURN collect(node.name) AS community_members, communityId, count(*) AS community_size
ORDER BY community_size DESC
```

#### Expected Results

| community_members                                        | communityId | community_size |
|----------------------------------------------------------|-------------|----------------|
| `["Alice", "Bob", "Charlie", "Diana", "Grace", "Henry"]` | 0           | 6              |
| `["Eve", "Frank", "Iris", "Jack"]`                       | 2           | 4              |
| `["Kate"]`                                               | 10          | 1              |

### Example: Find the largest communities

```cypher
CALL algo.labelPropagation() YIELD node, communityId 
RETURN communityId, collect(node) AS nodes, count(*) AS size
ORDER BY size DESC
LIMIT 1
```
