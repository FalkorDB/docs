---
title: "DELETE"
nav_order: 9
description: >
    FalkorDB implements a subset of the Cypher language, which is growing as development continues.
parent: "Cypher Language"
---

# DELETE

DELETE is used to remove both nodes and relationships.

Note that deleting a node also deletes all of its incoming and outgoing relationships.

To delete a node and all of its relationships:

```sh
GRAPH.QUERY DEMO_GRAPH "MATCH (p:Person {name:'Jim'}) DELETE p"
```

To delete relationship:

```sh
GRAPH.QUERY DEMO_GRAPH "MATCH (:Person {name:'Jim'})-[r:FRIENDS]->() DELETE r"
```

This query will delete all `friend` outgoing relationships from the node with the name 'Jim'.