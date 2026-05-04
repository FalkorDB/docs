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
{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="What is the default sort order in ORDER BY?"
  a1="If no direction is specified, ORDER BY defaults to **ascending** (ASC) order."
  q2="Can I sort by multiple properties?"
  a2="Yes. List multiple properties separated by commas. The result is sorted by the first property, then ties are broken by subsequent properties in order."
  q3="Does ORDER BY work with expressions and aliases?"
  a3="Yes. You can order by any expression or alias that appears in the RETURN or WITH clause, including computed values and aggregations."
%}
