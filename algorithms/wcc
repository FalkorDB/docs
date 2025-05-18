---
title: "Weakly Connected Components (WCC)"
description: "Weakly Connected Components (WCC)"
---

# Weakly Connected Components (WCC)

## Overview

The Weakly Connected Components (WCC) algorithm identifies sets of nodes that are connected to each other, regardless of the edge directions.
Each node in a weakly connected component can reach every other node in that component if edge directions are ignored.

WCC is a common algorithmic building block used in applications like:
- Community detection
- Data preprocessing
- Network analysis
- Identifying isolated subgraphs

## Algorithm Details

WCC begins with each node in its own component.
The algorithm repeatedly merges components when edges are found between them, ignoring edge directions.
This process continues until no more merges are possible, resulting in a set of disjoint communities.

### Performance

The time complexity of WCC is O(|V| + |E|) where:
- |V| is the number of nodes
- |E| is the number of edges

## Syntax

```cypher
CALL algo.wcc([config])
```

### Parameters

The procedure accepts an optional configuration `Map` with the following parameters:

| Name                | Type  | Default                | Description                                                                      |
|---------------------|-------|------------------------|----------------------------------------------------------------------------------|
| `nodeLabels`        | Array | All labels             | Array of strings listing which node labels will be considered                    |
| `relationshipTypes` | Array | All relationship types | Array of strings specifying which relationship types are allowed to be traversed |

### Return Values

| Name          | Type    | Description                          |
|---------------|---------|--------------------------------------|
| `node`        | Node    | The current node object              |
| `componentId` | Integer | The component ID the node belongs to |

## Examples

```cypher
CALL algo.wcc({
  nodeLabels: ["Person"],
  relationshipTypes: ["KNOWS"]
})
YIELD node, componentId
RETURN node.name, componentId
```

### Creating a Social Network Graph

```cypher
// Create users in different communities
CREATE 
  // Community 1
  (alice:User {name: 'Alice'}),
  (bob:User {name: 'Bob'}),
  (charlie:User {name: 'Charlie'}),
  
  // Community 2
  (david:User {name: 'David'}),
  (emma:User {name: 'Emma'}),
  
  // Community 3
  (frank:User {name: 'Frank'})

// Create relationships within communities
CREATE
  (alice)-[:FOLLOWS]->(bob),
  (bob)-[:FRIENDS_WITH]->(charlie),
  (charlie)-[:FOLLOWS]->(alice),
  
  (david)-[:FRIENDS_WITH]->(emma)
  
// Note that Frank is isolated and forms his own community
```

### Analyzing Social Networks

```cypher
// Find isolated communities in a social network
CALL algo.wcc({
  nodeLabels: ["User"],
  relationshipTypes: ["FOLLOWS", "FRIENDS_WITH"],
})
YIELD componentId

// Get community sizes
RETURN componentId AS communityId, count(*) AS communitySize
ORDER BY communitySize DESC
```
