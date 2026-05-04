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

The following query will create 4 nodes, each with property `v` with the values from 1 to 4 corresponding to the elements in the list.

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
FOREACH(do_perform IN CASE WHEN b IS NULL THEN [1] ELSE [] END | MERGE (h)-[b2:BUYS_FROM]->(s:SUPPLIER {supplies_bread: true}) SET b2.direct = false)"
```
{% include faq_accordion.html title="Frequently Asked Questions" q1="What clauses can I use inside FOREACH?" a1="FOREACH only supports **updating clauses**: CREATE, MERGE, SET, REMOVE, DELETE, and nested FOREACH. Read clauses like MATCH and RETURN are not allowed inside FOREACH." q2="Can FOREACH access variables from the outer query?" a2="Yes. The sub-query inside FOREACH can read variables defined before the FOREACH clause. However, variables created inside FOREACH are local and not visible to later clauses." q3="How is FOREACH different from UNWIND?" a3="**UNWIND** creates new rows for each list element and allows any clause. **FOREACH** iterates over a list to perform side-effect updates without changing the number of result rows." q4="Can I use FOREACH for conditional updates?" a4="Yes. Use a CASE expression to produce a list with one element (execute) or empty list (skip): `FOREACH(x IN CASE WHEN condition THEN [1] ELSE [] END | SET n.flag = true)`." %}
