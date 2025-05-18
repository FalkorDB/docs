# FalkorDB Algorithms Overview

FalkorDB offers a suite of graph algorithms optimized for high-performance graph analytics.  
These algorithms are accessible via the `CALL algo.<name>()` interface and are built for speed and scalability using matrix-based computation.

This overview summarizes the available algorithms and links to their individual documentation.

## Table of Contents

- [Pathfinding Algorithms](#pathfinding-algorithms)
- [Centrality Measures](#centrality-measures)
- [Community Detection](#community-detection)

---

## Pathfinding Algorithms

- **[BFS](./algo_bfs.md)**  
  Performs a breadth-first search starting from a source node and optionally stopping at target nodes or maximum depth.

- **[SPPATH](./algo_spath.md)**  
  Computes the shortest paths between a source and one or more destination nodes.

- **[SSPATH](./algo_sspath.md)**  
  Enumerates all paths from a single source node to other nodes, based on constraints like edge filters and depth.

## Centrality Measures

- **[PageRank](./algo_pagerank.md)**  
  Computes the PageRank score of each node in the graph, representing its influence based on the structure of incoming links.

## Community Detection

- **[WCC (Weakly Connected Components)](./algo_wcc.md)**  
  Finds weakly connected components in a graph, where each node is reachable from others ignoring edge directions.

---

These procedures are part of FalkorDB's built-in algorithm library and are invoked using the `CALL algo.<name>(config)` syntax.  
For path expressions like `shortestPath()` used directly in Cypher queries, refer to the [Cypher Path Functions section](../cypher).

For feedback or contributions, visit [FalkorDB on GitHub](https://github.com/FalkorDB/docs).