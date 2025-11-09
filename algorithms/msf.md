---
title: "MSF"
description: "Minimum Spanning Forest Algorithm"
parent: "Algorithms"
nav_order: 9
---

# Minimum Spanning Forest (MSF)

The Minimum Spanning Forest algorithm computes the minimum spanning forest of a graph. A minimum spanning forest is a collection of minimum spanning trees, one for each connected component in the graph.

## What is a Minimum Spanning Forest?

- For a **connected graph**, the MSF is a single minimum spanning tree (MST) that connects all nodes with the minimum total edge weight
- For a **disconnected graph**, the MSF consists of multiple MSTs, one for each connected component
- The forest contains no cycles and has exactly `N - C` edges, where `N` is the number of nodes and `C` is the number of connected components

## Use Cases

- **Network Design**: Minimize cable/pipeline costs when connecting multiple locations
- **Clustering**: Identify natural groupings in data by analyzing the forest structure
- **Image Segmentation**: Group similar pixels using edge weights as similarity measures
- **Road Networks**: Optimize road construction to connect all cities with minimum cost

## Syntax

```cypher
CALL algo.MSF(
    config: MAP
) YIELD src, dest, weight, relationshipType
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `config` | MAP | Configuration map containing algorithm parameters |

#### Configuration Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `sourceNodes` | List of Nodes | No | All nodes | Starting nodes for the algorithm. If not provided, all nodes in the graph are considered |
| `relationshipTypes` | List of Strings | No | All types | Relationship types to traverse. If not provided, all relationship types are considered |
| `relationshipWeightProperty` | String | No | `null` | Property name containing edge weights. If not specified, all edges have weight 1.0 |
| `defaultValue` | Float | No | `1.0` | Default weight for edges that don't have the weight property |

### Returns

| Field | Type | Description |
|-------|------|-------------|
| `src` | Node | Source node of the edge in the spanning forest |
| `dest` | Node | Destination node of the edge in the spanning forest |
| `weight` | Float | Weight of the edge |
| `relationshipType` | String | Type of the relationship |

## Examples

### Example 1: Basic MSF with Unweighted Graph

Find the minimum spanning forest treating all edges equally:

```cypher
CALL algo.MSF({}) YIELD src, dest, weight, relationshipType
RETURN src.name AS source, dest.name AS destination, weight, relationshipType
```

### Example 2: MSF with Weighted Edges

Consider a graph representing cities connected by roads with distances:

```cypher
// Create a weighted graph
CREATE (a:City {name: 'A'}), (b:City {name: 'B'}), (c:City {name: 'C'}),
       (d:City {name: 'D'}), (e:City {name: 'E'})
CREATE (a)-[:ROAD {distance: 2}]->(b),
       (a)-[:ROAD {distance: 3}]->(c),
       (b)-[:ROAD {distance: 1}]->(c),
       (b)-[:ROAD {distance: 4}]->(d),
       (c)-[:ROAD {distance: 5}]->(d),
       (d)-[:ROAD {distance: 6}]->(e)

// Find minimum spanning forest using distance weights
CALL algo.MSF({
    relationshipWeightProperty: 'distance'
}) YIELD src, dest, weight
RETURN src.name AS from, dest.name AS to, weight AS distance
ORDER BY weight
```

**Result:**
```
from | to | distance
-----|----|---------
B    | C  | 1.0
A    | B  | 2.0
A    | C  | 3.0
B    | D  | 4.0
D    | E  | 6.0
```

### Example 3: MSF on Specific Relationship Types

Find the spanning forest considering only specific relationship types:

```cypher
CALL algo.MSF({
    relationshipTypes: ['ROAD', 'HIGHWAY'],
    relationshipWeightProperty: 'distance'
}) YIELD src, dest, weight, relationshipType
RETURN src.name AS from, dest.name AS to, weight, relationshipType
```

### Example 4: MSF Starting from Specific Nodes

Compute the spanning forest starting from a subset of nodes:

```cypher
MATCH (start:City) WHERE start.name IN ['A', 'B']
WITH collect(start) AS startNodes
CALL algo.MSF({
    sourceNodes: startNodes,
    relationshipWeightProperty: 'distance'
}) YIELD src, dest, weight
RETURN src.name AS from, dest.name AS to, weight
```

### Example 5: Disconnected Graph

For a graph with multiple components, MSF returns multiple trees:

```cypher
// Create two disconnected components
CREATE (a:Node {name: 'A'})-[:CONNECTED {weight: 1}]->(b:Node {name: 'B'}),
       (b)-[:CONNECTED {weight: 2}]->(c:Node {name: 'C'}),
       (x:Node {name: 'X'})-[:CONNECTED {weight: 3}]->(y:Node {name: 'Y'})

// Find MSF
CALL algo.MSF({
    relationshipWeightProperty: 'weight'
}) YIELD src, dest, weight
RETURN src.name AS from, dest.name AS to, weight
```

**Result:** Two separate trees (A-B-C and X-Y)

## Algorithm Details

FalkorDB's MSF implementation uses an efficient matrix-based approach optimized for graph databases:

1. **Connected Components**: First identifies all connected components in the graph
2. **MST per Component**: Computes a minimum spanning tree for each component using a variant of Kruskal's or Prim's algorithm
3. **Edge Selection**: Selects edges in order of increasing weight, avoiding cycles

### Performance Characteristics

- **Time Complexity**: O(E log V) where E is the number of edges and V is the number of vertices
- **Space Complexity**: O(V + E)
- **Optimized**: Uses sparse matrix representation for efficient computation

## Best Practices

1. **Weight Properties**: Ensure weight properties are numeric (integers or floats)
2. **Missing Weights**: Use `defaultValue` to handle edges without weight properties
3. **Large Graphs**: For very large graphs, consider filtering by `sourceNodes` or `relationshipTypes`
4. **Directed vs Undirected**: The algorithm treats relationships as undirected for spanning forest purposes

## Related Algorithms

- **[WCC (Weakly Connected Components)](./wcc.md)**: Identify connected components before running MSF
- **[BFS](./bfs.md)**: Traverse the resulting spanning forest
- **[SPpath](./sppath.md)**: Find shortest paths using the spanning forest structure

## See Also

- [Cypher Procedures](../cypher/procedures.md)
- [Graph Algorithms Overview](./index.md)
