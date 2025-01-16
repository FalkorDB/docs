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

```
CALL algo.pageRank(
  'NodeLabel',        // The label of the nodes to include in the computation
  'RELATIONSHIP_TYPE' // The type of relationships to consider
)
YIELD nodeId, score
```

Parameters:

    'NodeLabel': The label of the nodes to include in the computation.
    'RELATIONSHIP_TYPE': The type of relationships to consider. Only edges of this type will be used in the PageRank calculation.

YIELD:

    nodeId: The internal ID of the node.
    score: The PageRank score assigned to the node.

Example:

```
CALL algo.pageRank('Page', 'LINKS_TO')
YIELD nodeId, score
RETURN nodeId, score
ORDER BY score DESC
```

In this example, the algo.pageRank function computes the PageRank scores for all nodes labeled 'Page', considering only 'LINKS_TO' relationships. The results are returned with nodes ordered by their PageRank score in descending order.

Note:

    Ensure that the graph contains nodes with the specified label and relationships of the specified type; otherwise, the function may return an empty result set.
    The PageRank algorithm assumes that the graph is directed; thus, the direction of relationships is taken into account during computation.
    The damping factor, which represents the probability of continuing from one node to another, is typically set to 0.85. This value can influence the distribution of PageRank scores.
    Wikipedia

For more detailed information on the PageRank algorithm, refer to the Wikipedia article on PageRank.

