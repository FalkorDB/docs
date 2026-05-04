---
title: "algo.SPpaths"
description: "Find shortest paths between two nodes with advanced cost and length constraints."
parent: "Algorithms"
nav_order: 5
---

# `algo.SPpaths` - Shortest Path (Single Pair)

The `algo.SPpaths` procedure finds the shortest paths between a **source** and a **target** node, optionally constrained by cost, path length, and the number of paths to return.

It is designed for efficient and scalable computation of paths in large graphs, using properties like distance, time, or price as weights. 
For example, it can be used to find the fastest driving route between two cities, the cheapest shipping option in a logistics network, or the shortest communication path in a computer network.

## Syntax

```cypher
CALL algo.SPpaths({
  sourceNode: <node>,
  targetNode: <node>,
  relTypes: [<relationship_type>],
  weightProp: <property>,
  costProp: <property>,         // optional
  maxCost: <int>,               // optional
  maxLen: <int>,                // optional
  relDirection: "outgoing",    // or "incoming", "both"
  pathCount: <int>              // 0 = all, 1 = single (default), n > 1 = up to n
})
YIELD path, pathWeight, pathCost
```

## Parameters

| Name            | Type     | Description                                                                          |
|-----------------|----------|--------------------------------------------------------------------------------------|
| `sourceNode`    | Node     | Starting node                                                                        |
| `targetNode`    | Node     | Destination node                                                                     |
| `relTypes`      | Array    | List of relationship types to follow                                                 |
| `weightProp`    | String   | Property to minimize along the path (e.g., `dist`, `time`)                           |
| `costProp`      | String   | Property to constrain the total value (optional)                                     |
| `maxCost`       | Integer  | Upper bound on total cost (optional)                                                 |
| `maxLen`        | Integer  | Max number of relationships in the path (optional)                                   |
| `relDirection`  | String   | Traversal direction (`outgoing`, `incoming`, `both`)                                 |
| `pathCount`     | Integer  | Number of paths to return (0 = all shortest, 1 = default, n = max number of results) |

## Returns

| Name         | Type    | Description                                    |
|--------------|---------|------------------------------------------------|
| `path`       | Path    | Discovered path from source to target          |
| `pathWeight` | Integer | Sum of the weightProp across the path          |
| `pathCost`   | Integer | Sum of the costProp across the path (if used)  |


## Examples

Let's take this Road Network Graph as an example:

![Road network](../images/road_network.png)

### Example: Shortest Path by Distance from City A to City G

```cypher
MATCH (a:City{name:'A'}), (g:City{name:'G'})
CALL algo.SPpaths({
  sourceNode: a,
  targetNode: g,
  relTypes: ['Road'],
  weightProp: 'dist'
})
YIELD path, pathWeight
RETURN pathWeight, [n in nodes(path) | n.name] AS pathNodes
```

#### Expected Result:
| pathWeight | pathNodes     |
|------------|---------------|
| `12`       | [A, D, E, G]  | 


### Example: Bounded Cost Path from City A to City G

```cypher
MATCH (a:City{name:'A'}), (g:City{name:'G'})
CALL algo.SPpaths({
  sourceNode: a,
  targetNode: g,
  relTypes: ['Road'],
  weightProp: 'dist',
  costProp: 'time',
  maxCost: 12,
  pathCount: 2
})
YIELD path, pathWeight, pathCost
RETURN pathWeight, pathCost, [n in nodes(path) | n.name] AS pathNodes
```

#### Expected Result:
| pathWeight | pathCost | pathNodes        |
|------------|----------|------------------|
| `16`       | `10`     | [A, D, F, G]     |
| `14`       | `12`     | [A, D, C, F, G]  | 

---

{% include faq_accordion.html title="Frequently Asked Questions" q1="What is the difference between weightProp and costProp?" a1="**weightProp** is the property the algorithm *minimizes* (e.g. distance). **costProp** is a separate property used as a *constraint* — you can set `maxCost` to exclude paths whose total cost exceeds a threshold." q2="How do I get all shortest paths instead of just one?" a2="Set `pathCount: 0` to return all shortest paths. The default is `1` (single shortest path). You can also set a specific number like `pathCount: 5` to get up to 5 paths." q3="Can I search for paths in both directions?" a3="Yes. Set `relDirection` to `'both'` to traverse relationships regardless of direction. Other options are `'outgoing'` (default) and `'incoming'`." q4="When should I use algo.SPpaths vs algo.SSpaths?" a4="Use **algo.SPpaths** when you have a specific source *and* target node. Use **[algo.SSpaths](./sspath.md)** when you want shortest paths from one source to *all* reachable destinations." q5="What happens if no path exists between source and target?" a5="The procedure returns no results (empty result set). No error is raised." %}

