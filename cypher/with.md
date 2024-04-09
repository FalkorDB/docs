---
title: "WITH"
nav_order: 12
description: >
    FalkorDB implements a subset of the Cypher language, which is growing as development continues.
parent: "Cypher Language"
---

# WITH

The WITH clause allows parts of queries to be independently executed and have their results handled uniquely.

This allows for more flexible query composition as well as data manipulations that would otherwise not be possible in a single query.

If, for example, we wanted to find all children in our graph who are above the average age of all people:

```sh
GRAPH.QUERY DEMO_GRAPH
"MATCH (p:Person) WITH AVG(p.age) AS average_age MATCH (:Person)-[:PARENT_OF]->(child:Person) WHERE child.age > average_age return child
```

This also allows us to use modifiers like `DISTINCT`, `SKIP`, `LIMIT`, and `ORDER` that otherwise require `RETURN` clauses.

```sh
GRAPH.QUERY DEMO_GRAPH
"MATCH (u:User)  WITH u AS nonrecent ORDER BY u.lastVisit LIMIT 3 SET nonrecent.should_contact = true"
```