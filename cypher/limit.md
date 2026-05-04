---
title: "LIMIT"
nav_order: 7
description: >
    Can use the limit clause to limit the number of records returned by a query
parent: "Cypher Language"
---

# LIMIT

Although not mandatory, you can use the limit clause
to limit the number of records returned by a query:

```sql
LIMIT <max records to return>
```

If not specified, there's no limit to the number of records returned by a query.
{% include faq_accordion.html title="Frequently Asked Questions" q1="Is there a default limit on query results?" a1="No. If you do not specify a LIMIT clause, FalkorDB returns all matching records with no upper bound." q2="Does LIMIT improve query performance?" a2="LIMIT can reduce the amount of data transferred to the client, but due to a known limitation, it does not currently short-circuit eager operations like CREATE, SET, or DELETE. The full operation executes before LIMIT is applied." q3="Can I use LIMIT without ORDER BY?" a3="Yes, but the subset of results returned will be non-deterministic. Combine LIMIT with ORDER BY for predictable, repeatable results." %}
