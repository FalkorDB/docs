title: "Algorithms"
nav_order: 19
description: >
    FalkorDB implements a subset of the Cypher language, which is growing as development continues.
parent: "Cypher Language"
---

# Algorithms

## BFS

The breadth-first-search algorithm accepts 3 arguments:

`source-node (node)` - The root of the search.

`max-level (integer)` - If greater than zero, this argument indicates how many levels should be traversed by BFS. 1 would retrieve only the source's neighbors, 2 would retrieve all nodes within 2 hops, and so on.

`relationship-type (string)` - If this argument is NULL, all relationship types will be traversed. Otherwise, it specifies a single relationship type to perform BFS over.

It can yield two outputs:

`nodes` - An array of all nodes connected to the source without violating the input constraints.

`edges` - An array of all edges traversed during the search. This does not necessarily contain all edges connecting nodes in the tree, as cycles or multiple edges connecting the same source and destination do not have a bearing on the reachability this algorithm tests for. These can be used to construct the directed acyclic graph that represents the BFS tree. Emitting edges incurs a small performance penalty.
