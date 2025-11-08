---
title: "FOREACH"
nav_order: 15
description: >
    The FOREACH clause feeds the components of a list to a sub-query comprised of updating clauses only
parent: "Cypher Language"
---

# FOREACH

The `FOREACH` clause feeds the components of a list to a sub-query comprised of **updating clauses only** (`CREATE`, `MERGE`, `SET`, `REMOVE`, `DELETE` and `FOREACH`), while passing on the records it receives without change.

The clauses within the sub-query recognize the bound variables defined prior to the `FOREACH` clause, but are local in the sense that later clauses are not aware of the variables defined inside them. In other words, `FOREACH` uses the current context, and does not affect it.

The `FOREACH` clause can be used for numerous purposes, such as: Updating and creating graph entities in a concise manner, marking nodes\edges that satisfy some condition or are part of a path of interest and performing conditional queries.

We show examples of queries performing the above 3 use-cases.

The following query will create 5 nodes, each with property `v` with the values from 0 to 4 corresponding to the appropriate index in the list.

```sh
GRAPH.QUERY DEMO_GRAPH
"FOREACH(i in [1, 2, 3, 4] | CREATE (n:N {v: i}))"
```

The following query marks the nodes of all paths of length up to 15 km from a hotel in Toronto to a steakhouse with at least 2 Michelin stars.

```sh
GRAPH.QUERY DEMO_GRAPH
"MATCH p = (hotel:HOTEL {City: 'Toronto'})-[r:ROAD*..5]->(rest:RESTAURANT {type: 'Steakhouse'}) WHERE sum(r.length) <= 15 AND hotel.stars >= 4 AND rest.Michelin_stars >= 2
FOREACH(n in nodes(p) | SET n.part_of_path = true)"
```

The following query searches for all the hotels, checks whether they buy directly from a bakery, and if not - makes sure they are marked as buying from a supplier that supplies bread, and that they do not buy directly from a bakery.

```sh
GRAPH.QUERY DEMO_GRAPH
"MATCH (h:HOTEL) OPTIONAL MATCH (h)-[b:BUYS_FROM]->(bakery:BAKERY)
FOREACH(do_perform IN CASE WHEN b = NULL THEN [1] ELSE [] END | MERGE (h)-[b2:BUYS_FROM]->(s:SUPPLIER {supplies_bread: true}) SET b2.direct = false)"
```
