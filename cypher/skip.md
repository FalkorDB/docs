title: "SKIP clause"
nav_order: 6
description: >
    FalkorDB implements a subset of the Cypher language, which is growing as development continues.
parent: "Cypher Language"
---

# SKIP

The optional skip clause allows a specified number of records to be omitted from the result set.

```sh
SKIP <number of records to skip>
```

This can be useful when processing results in batches. A query that would examine the second 100-element batch of nodes with the label `Person`, for example, would be:

```sh
GRAPH.QUERY DEMO_GRAPH "MATCH (p:Person) RETURN p ORDER BY p.name SKIP 100 LIMIT 100"
```