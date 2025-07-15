---
title: "Minimum Spanning Tree (MST)"
description: "Minimum Spanning Tree (MST)"
parent: "Algorithms"
---

# Minimum Spanning Tree (MST)

## Overview

The Minimum Spanning Tree (MST) identifies the minimum weight acyclic graph (tree) spanning every node in each weakly connected component in the graph, disregarding edge directions. Any nodes that shared a weakly connected component still share that component in the MST sub-graph. 

MST serves as a common algorithm in scenarios such as:
- Designing a cost-effective road network connecting several cities.
- Power Grid / Utility cost optimization.
- Identifying redundancies in networks.

## Algorithm Details

MST first assigns each node to its own component. It iteratively scans for the minimum edges linking nodes across different components and merges them, ignoring the direction of edges throughout the process. The algorithm terminates when no further merges occur, producing a collection of trees.

The procedure finds a minimum or maximum weight spanning tree based on the specified attribute. If no attribute is given, returns any spanning tree. If any specified edges do not have the given weight attribute, or the value of the attribute is non-numeric, then they are treated as if they had infinite weight. Such an edge would only be included in the minimum spanning tree if no other edges with a valid weight attribute bridge the components it connects.

## Syntax

```cypher
CALL algo.mst([config])
```

### Parameters

The procedure accepts an optional configuration `Map` with the following parameters:

| Name                | Type   | Default                | Description                                                                |
|---------------------|--------|------------------------|----------------------------------------------------------------------------|
| `nodeLabels`        | Array  | All labels             | Array of node labels to filter which nodes are included in the computation |
| `relationshipTypes` | Array  | All relationship types | Array of relationship types to define which edges are traversed            |
| `objective`         | string | 'minimize'             | 'minimize' or 'maximize' what to optimize in the spanning tree             |
| `weightAttribute`   | string | Unweighted             | the attribute to use as the tree weight.                                   |

### Return Values
The procedure returns a stream of records with the following fields:

| Name     | Type   | Description                                   |
|----------|--------|-----------------------------------------------|
| `edge`   | Edge   | An edge entity which is part of the MST graph |
| `weight` | Double | The weight of the Edge                        |

## Examples:

Lets take this City as an example:

![City Graph](../images/city_plan.png)



### Create the Graph

```cypher
CREATE 
  (CityHall:GOV),
  (CourtHouse:GOV),
  (FireStation:GOV),
  (Electricity:UTIL),
  (Water:UTIL),
  (Building_A:RES),
  (Building_B:RES),
  (CityHall)-[rA:ROAD {cost: 2.2}]->(CourtHouse),
  (CityHall)-[rB:ROAD {cost: 8.0}]->(FireStation),
  (CourtHouse)-[rC:ROAD {cost: 3.4}]->(Building_A),
  (FireStation)-[rD:ROAD {cost: 3.0}]->(Building_B),
  (Building_A)-[rF:ROAD {cost: 5.2}]->(Building_B),
  (Electricity)-[rG:ROAD {cost: 0.7}]->(Building_A),
  (Water)-[rH:ROAD {cost: 2.3}]->(Building_B),
  (CityHall)-[tA:TRAM {cost: 1.5}]->(Building_A),
  (CourtHouse)-[tB:TRAM {cost: 7.3}]->(Building_B),
  (FireStation)-[tC:TRAM {cost: 1.2}]->(Electricity)
```
### Example: Find cheapest road network:
```cypher
CALL algo.mst({weightAttribute: 'cost'}) YIELD edge, weight
```

#### Expected Results
| Edge      | weight |
|-----------|--------|
| `[:ROAD]` | 0.7    |
| `[:TRAM]` | 1.2    |
| `[:TRAM]` | 1.5    |
| `[:ROAD]` | 2.2    |
| `[:ROAD]` | 2.3    |
| `[:ROAD]` | 3.0    |
