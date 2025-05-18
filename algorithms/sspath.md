---

title: "algo.SSpaths"
description: "Explore all shortest paths from a single source node with weight, cost, and length constraints."
---

# `algo.SSpaths` - Single Source Paths

The `algo.SSpaths` procedure returns all shortest paths from a **source node** to multiple reachable nodes, subject to constraints like cost, path length, and number of paths to return.

## Syntax

```cypher
CALL algo.SSpaths({
  sourceNode: <node>,
  relTypes: [<relationship_type>],
  weightProp: <property>,         // optional
  costProp: <property>,           // optional
  maxCost: <int>,                 // optional
  maxLen: <int>,                  // optional
  relDirection: "outgoing",      // or "incoming", "both"
  pathCount: <int>
})
YIELD path, pathWeight, pathCost
```

## Parameters

Same as `algo.SPpaths`, except `targetNode` is omitted.

## Example: All Shortest Paths by Distance (up to 10 km)

```cypher
MATCH (a:City{name:'A'})
CALL algo.SSpaths({
  sourceNode: a,
  relTypes: ['Road'],
  costProp: 'dist',
  maxCost: 10,
  pathCount: 1000
})
YIELD path, pathCost
RETURN pathCost, [n in nodes(path) | n.name] AS pathNodes
ORDER BY pathCost
```

## Example: Top 5 Shortest Paths from A by Distance

```cypher
MATCH (a:City{name:'A'})
CALL algo.SSpaths({
  sourceNode: a,
  relTypes: ['Road'],
  weightProp: 'dist',
  pathCount: 5
})
YIELD path, pathWeight, pathCost
RETURN pathWeight, pathCost, [n in nodes(path) | n.name] AS pathNodes
ORDER BY pathWeight