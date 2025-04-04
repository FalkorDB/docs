---
title: "Algorithms"
nav_order: 20
description: >
    FalkorDB supported algorithms like BFS.
parent: "Cypher Language"
---

# Algorithms

## BFS

Usage: `algo.BFS`

The breadth-first-search algorithm accepts 3 arguments:

`source-node (node)` - The root of the search.

`max-level (integer)` - If greater than zero, this argument indicates how many levels should be traversed by BFS. 1 would retrieve only the source's neighbors, 2 would retrieve all nodes within 2 hops, and so on.

`relationship-type (string)` - If this argument is NULL, all relationship types will be traversed. Otherwise, it specifies a single relationship type to perform BFS over.

It can yield two outputs:

`nodes` - An array of all nodes connected to the source without violating the input constraints.

`edges` - An array of all edges traversed during the search. This does not necessarily contain all edges connecting nodes in the tree, as cycles or multiple edges connecting the same source and destination do not have a bearing on the reachability this algorithm tests for. These can be used to construct the directed acyclic graph that represents the BFS tree. Emitting edges incurs a small performance penalty.

## Page Rank

Usage: `algo.pageRank`

The function executes the PageRank algorithm on nodes of a specified label, 
considering only edges of a given relationship type. 
PageRank is an algorithm originally developed by Google to rank web pages by 
measuring their relative importance within a linked network. 
It assigns a numerical weight to each node, indicating its significance based 
on the structure of incoming links.

Usage:

```cypher
CALL algo.pageRank(
  'source-node',      // The ID or name of the starting node
  max-level,          // The maximum depth to traverse
  'relationship-type' // The type of relationships to consider
)
YIELD nodes, edges
```

Arguments:

`source-node` - The ID or name of the starting node. This is the entry point for the PageRank computation.
`max-level` - The maximum depth or level to traverse from the starting node. Controls how far the algorithm propagates.
`relationship-type` - The type of relationships to consider. Only edges of this type will be included in the computation.

Yields:

`nodes` - The total number of nodes included in the computation.
`edges` - The total number of edges considered during the computation.

Example:

```cypher
CALL algo.pageRank('HomePage', 3, 'LINKS_TO')
YIELD nodes, edges
RETURN nodes, edges
```

In this example, the algo.pageRank function calculates PageRank starting from the 'HomePage' node, traversing up to 3 levels deep and considering only 'LINKS_TO' relationships. It returns the count of nodes and edges involved in the computation.

Notes:

    The PageRank algorithm assumes a directed graph; the direction of relationships is significant.
    Ensure the graph contains valid relationships of the specified type; otherwise, the computation may not yield meaningful results.
    You can customize traversal depth using the max-level argument to balance performance and accuracy.
