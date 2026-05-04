---
title: "Algorithms"
description: "Explore FalkorDB's high-performance graph algorithms including pathfinding (BFS, shortest path), centrality measures (PageRank, betweenness), and community detection (WCC, CDLP)."
nav_order: 3
has_children: true
redirect_from:
  - /cypher/algorithms.html
  - /cypher/algorithms
---

# FalkorDB Algorithms Overview

FalkorDB offers a suite of graph algorithms optimized for high-performance graph analytics.  
These algorithms are accessible via the `CALL algo.<name>()` interface and are built for speed and scalability using matrix-based computation.

This overview summarizes the available algorithms and links to their individual documentation.

## Pathfinding Algorithms

- **[BFS](./bfs.md)**  
  Performs a breadth-first search starting from a source node and optionally stopping at target nodes or maximum depth.

- **[SPpath](./sppath.md)**  
  Computes the shortest paths between a source and one or more destination nodes.

- **[SSpath](./sspath.md)**  
  Enumerates all paths from a single source node to other nodes, based on constraints like edge filters and depth.

- **[MSF](./msf.md)**  
  Computes the Minimum Spanning Forest of a graph, finding the minimum spanning tree for each connected component.

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

{% include faq_accordion.html title="Frequently Asked Questions" q1="How do I call a graph algorithm in FalkorDB?" a1="All algorithms are invoked using the `CALL algo.<name>()` syntax within a Cypher query. Each algorithm returns results via `YIELD` clauses. See individual algorithm pages for specific syntax." q2="Are FalkorDB algorithms optimized for large graphs?" a2="Yes. FalkorDB algorithms use **matrix-based computation** for high performance and scalability, leveraging sparse matrix representations internally." q3="What is the difference between algo.SPpaths and algo.SSpaths?" a3="**algo.SPpaths** finds shortest paths between a single source and a single target node. **algo.SSpaths** finds shortest paths from a single source to *all* reachable nodes. Use SPpaths for point-to-point queries and SSpaths for broader exploration." q4="Can I filter which nodes and edges are included in an algorithm?" a4="Yes. Most algorithms accept optional `nodeLabels` and `relationshipTypes` parameters that let you restrict computation to specific subsets of the graph." q5="Which algorithm should I use for community detection?" a5="Use **WCC** to find disconnected components (groups of nodes connected by any path). Use **CDLP** (Label Propagation) to detect densely connected communities within a connected graph. See [WCC](./wcc.md) and [CDLP](./cdlp.md) for details." %}

