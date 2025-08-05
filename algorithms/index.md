---
title: "Algorithms"
description: Graph Algorithms Overview
nav_order: 3
has_children: true
---

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

- **[BFS](./bfs.md)**  
  Performs a breadth-first search starting from a source node and optionally stopping at target nodes or maximum depth.

- **[SPpath](./sppath.md)**  
  Computes the shortest paths between a source and one or more destination nodes.

- **[SSpath](./sspath.md)**  
  Enumerates all paths from a single source node to other nodes, based on constraints like edge filters and depth.

For path expressions like `shortestPath()` used directly in Cypher queries, refer to the [Cypher Path Functions section](../cypher/functions.md#path-functions).

## Centrality Measures

- **[PageRank](./pagerank.md)**  
  Computes the PageRank score of each node in the graph, representing its influence based on the structure of incoming links.

- **[Betweenness Centrality](./betweenness-centrality.md)**  
  Calculates the number of shortest paths that pass through each node, indicating its importance as a connector in the graph.

## Community Detection

- **[WCC (Weakly Connected Components)](./wcc.md)**  
  Finds weakly connected components in a graph, where each node is reachable from others ignoring edge directions.

- **[CDLP (Community Detection Label Propagation)](./cdlp.md)**
  Detects communities in a network, by propagating labels through the graph structure.

