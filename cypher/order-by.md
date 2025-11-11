---
title: "ORDER BY"
nav_order: 5
description: >
    Order by specifies that the output be sorted and how.
parent: "Cypher Language"
redirect_from:
  - /cypher/order_by.html
  - /cypher/order_by
---

# ORDER BY

Order by specifies that the output be sorted and how.

You can order by multiple properties by stating each variable in the ORDER BY clause.

Each property may specify its sort order with `ASC`/`ASCENDING` or `DESC`/`DESCENDING`. If no order is specified, it defaults to ascending.

The result will be sorted by the first variable listed.

For equal values, it will go to the next property in the ORDER BY clause, and so on.

```sh
ORDER BY <alias.property [ASC/DESC] list>
```

Below we sort our friends by height. For equal heights, weight is used to break ties.

```sh
ORDER BY friend.height, friend.weight DESC
```
