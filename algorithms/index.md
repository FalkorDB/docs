---
title: "Graph Algorithms"
description: Graph Algorithms
nav_order: 4
has_children: true
---

# FalkorDB Algorithms Documentation

Welcome to the FalkorDB Algorithms Documentation! This guide provides an overview of all algorithms available within FalkorDB, enabling powerful graph analytics and insights. Each algorithm is designed to help you process and analyze graph data efficiently for a variety of use cases.

## Available Algorithms

Below is the list of supported algorithms in FalkorDB. Click on an algorithm to view its detailed documentation, including syntax, examples, and practical use cases:

### Traversal Algorithms
- [BFS](algorithms/BFS)
  - Performs a Breadth-First Search traversal of the graph.

### Centrality Algorithms
- [PageRank](algorithms/page_rank)
  - Measures the importance of nodes based on incoming connections.

### Connectivity Algorithms
- [Degree](algorithms/degree)
  - Calculates the degree of nodes, focusing on connectivity based on edge direction and type.

### Pathfinding Algorithms
- [Shortest Path](algorithms/shortest_path)
  - Finds the shortest path between two nodes.

### Community Detection Algorithms
- [Label Propagation](algorithms/label_propagation)
  - Identifies communities based on label diffusion through the graph.

---

## Getting Started

To begin using any of the algorithms:
1. Ensure FalkorDB is installed and running.
2. Load your graph data into FalkorDB.
3. Refer to the detailed documentation for each algorithm to configure and execute it.

For example, to calculate node degrees:

```plaintext
CALL algo.degree({})
```

---

## Feedback and Contributions

We welcome feedback and contributions! If you encounter issues or have suggestions for new algorithms, please visit our [GitHub repository](https://github.com/FalkorDB/FalkorDB).

Happy graph analytics with FalkorDB!


