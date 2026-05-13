---
title: "UNION"
nav_order: 13
description: >
    Combine results from multiple Cypher queries using the UNION clause. Use UNION ALL to keep all rows or UNION to remove duplicates from the combined result set.
parent: "Cypher Language"
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

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="What is the difference between UNION and UNION ALL?"
  a1="**UNION** combines results and removes duplicates. **UNION ALL** keeps all rows including duplicates, which is typically faster since no deduplication is needed."
  q2="Do column names need to match in UNION queries?"
  a2="Yes. The number and names of columns must be identical across all queries combined with UNION. Use `AS` aliases to ensure column names match."
  q3="Can I use ORDER BY with UNION?"
  a3="ORDER BY can be applied to the final combined result set after the UNION. Each individual query in the union cannot have its own ORDER BY unless wrapped in a CALL {} subquery."
%}
