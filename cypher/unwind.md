---
title: "UNWIND clause"
nav_order: 14
description: >
    FalkorDB implements a subset of the Cypher language, which is growing as development continues.
parent: "Cypher Language"
---

# UNWIND

The UNWIND clause breaks down a given list into a sequence of records; each contains a single element in the list.

The order of the records preserves the original list order.

```sh
GRAPH.QUERY DEMO_GRAPH
"CREATE (p {array:[1,2,3]})"
```

```sh
GRAPH.QUERY DEMO_GRAPH
"MATCH (p) UNWIND p.array AS y RETURN y"
```