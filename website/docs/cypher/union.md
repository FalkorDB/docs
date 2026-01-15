---
title: UNION
description: >
sidebar_position: 13
sidebar_label: UNION
---



# UNION
The UNION clause is used to combine the result of multiple queries.

UNION combines the results of two or more queries into a single result set that includes all the rows that belong to all queries in the union.

The number and the names of the columns must be identical in all queries combined by using UNION.

To keep all the result rows, use UNION ALL.

Using just UNION will combine and remove duplicates from the result set.

```sh
GRAPH.QUERY DEMO_GRAPH
"MATCH (n:Actor) RETURN n.name AS name
UNION ALL
MATCH (n:Movie) RETURN n.title AS name"
```
