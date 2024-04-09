---
title: "CALL"
nav_order: 16
description: >
    FalkorDB implements a subset of the Cypher language, which is growing as development continues.
parent: "Cypher Language"
---

# CALL \{\}

The CALL {} (subquery) clause allows local execution of subqueries, which opens the door for many comfortable and efficient actions on a graph.

The subquery is executed once for each record in the input stream.

The subquery may be a returning or non-returning subquery. A returning subquery may change the amount of records, while a non-returning subquery will not.

The variables in the scope before the CALL {} clause are available after the clause, together with the variables returned by the subquery (in the case of a returning subquery).

Variables may be imported from the outer scope **only** in an opening `WITH` clause, via simple projections (e.g. `WITH n, m`), or via `WITH *` (which imports all bound variables). The variables returned from a subquery may not override existing variables in the outer scope.

The CALL {} clause may be used for numerous purposes, such as: Post-`UNION` processing, local environment for aggregations and actions on every input row, efficient operations using a limited namespace (via imports) and performing side-effects using non-returning subqueries. Let's see some examples.

* Post-`UNION` processing.

We can easily get the cheapest and most expensive items in a store and set their `of_interest` property to `true` (to keep monitoring the 'interesting' items) using post-`UNION` processing:
  
  ```sh
  GRAPH.QUERY DEMO_GRAPH
  CALL {
    MATCH (s:Store {name: 'Walmart'})-[:SELLS]->(i:Item)
    RETURN i AS item
    ORDER BY price ASC
    LIMIT 1
    UNION
    MATCH (s:Store {name: 'Walmart'})-[:SELLS]->(i:Item)
    RETURN i AS item
    ORDER BY price DESC
    LIMIT 1
  }
  SET item.of_interest = true
  RETURN item.name AS name, item.price AS price
  ```

We can utilize post-`UNION` processing to perform aggregations over differently-matched entities. For example, we can count the number of customers and vendors that a store interacts with:

  ```sh
  GRAPH.QUERY DEMO_GRAPH
  CALL {
    MATCH (s:Store {name: 'Walmart'})-[:SELLS_TO]->(c:Customer)
    RETURN c AS interface
    UNION
    MATCH (s:Store {name: 'Walmart'})-[:BUYS_FROM]->(v:Vendor)
    RETURN v AS interface
  }
  RETURN count(interface) AS interfaces
  ```

* Local environment for aggregations and actions on every input row.

Another key feature of the CALL {} clause is the ability to perform isolated aggregations on every input row. For example, let's check if there is any correlation between the amount of sales per-product and the advertisement-intensity implemented for it in a particular month.

  ```sh
  GRAPH.QUERY DEMO_GRAPH
  MATCH (item:Item)
  CALL {
    WITH item
    MATCH (item)-[s:SOLD_TO {advertisement_intensity: 10}]->(c:Customer)
    WHERE s.date > '01-01-2023' AND s.date < '01-02-2023'
    RETURN count(s) AS item_sales_ads_high
  }
  CALL {
    WITH item
    MATCH (item)-[s:SOLD_TO {advertisement_intensity: 5}]->(c:Customer)
    WHERE s.date > '01-01-2023' AND s.date < '01-02-2023'
    RETURN count(s) AS item_sales_ads_low
  }
  RETURN item.name AS name, item_sales_ads_high as high_ads_sales, item_sales_ads_low as low_ads_sales
  ```

<!-- * Observe changes from previous executions (on previous records).

We can form useful structures and connections like linked-lists via the CALL {} clause. Let's form a linked-list of all items in a store, from the cheapest to the priciest:

```sh
MATCH (i:Item)
WITH i order BY i.price ASC LIMIT 1
SET i:HEAD
WITH i
MATCH (next_item:Item) WHERE NOT next_item:HEAD
WITH next_item ORDER BY next_item.price ASC
CALL {
  WITH next_item
  MATCH (curr_head:HEAD)
  REMOVE curr_head:HEAD
  SET next_item:HEAD
  CREATE (curr_head)-[:IS_CHEAPER_THAN]->(next_item)
}
``` -->

<!-- This will be added to a "performance-enhancement" section in the near future.

* Efficient operations using a limited namespace (via imports).

Given a query holding a respectively large namespace (a lot of bound variables), we can execute a subquery on a sub-namespace, and by thus enhance performance significantly. Let's look at an example.

Without a CALL {} clause:

```sh
GRAPH.QUERY DEMO_GRAPH
"MATCH (n:N), (m:M), (x:X), (y:Y), (z:Z), (e:E), (q:Q)
MATCH (temp:TEMP)
SET temp.v = n.v
RETURN n, m, x, y, z, e, q"
```
Runtime: 256 ms.

With a CALL {} clause:

```sh
GRAPH.QUERY DEMO_GRAPH
"MATCH (n:N), (m:M), (x:X), (y:Y), (z:Z), (e:E), (q:Q)
CALL {
  WITH n
  MATCH (temp:TEMP)
  SET temp.v = n.v
}
RETURN n, m, x, y, z, e, q"
```
Runtime: 99 ms. -->

* Side-effects.

We can comfortably perform side-effects using non-returning subqueries. For example, we can mark a sub-group of nodes in the graph withholding some shared property. Let's mark all the items in a Walmart store that were sold more than 100 times as popular items, and return **all** items in the store:

  ```sh
  GRAPH.QUERY DEMO_GRAPH
  MATCH (item:Item)
  CALL {
    WITH item
    MATCH (item)-[s:SOLD_TO]->(c:Customer)
    WITH item, count(s) AS item_sales
    WHERE item_sales > 100
    SET item.popular = true
  }
  RETURN item
  ```