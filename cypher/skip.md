---
title: "SKIP"
nav_order: 6
description: >
    The optional skip clause allows a specified number of records to be omitted from the result set.
parent: "Cypher Language"
---

# SKIP

The optional skip clause allows a specified number of records to be omitted from the result set.

```sh
SKIP <number of records to skip>
```

This can be useful when processing results in batches. A query that would examine the second 100-element batch of nodes with the label `Person`, for example, would be:

```sh
GRAPH.QUERY DEMO_GRAPH "MATCH (p:Person) RETURN p ORDER BY p.name SKIP 100 LIMIT 100"
```
{% include faq_accordion.html title="Frequently Asked Questions" q1="What does SKIP do in a Cypher query?" a1="SKIP omits a specified number of records from the beginning of the result set. It is typically used together with LIMIT for pagination." q2="Should I use ORDER BY with SKIP?" a2="Yes. Without ORDER BY, the order of results is non-deterministic, so SKIP may return different records on each execution. Always combine SKIP with ORDER BY for consistent pagination." q3="How do I paginate results in FalkorDB?" a3="Use `ORDER BY` with `SKIP` and `LIMIT` together. For example, to get page 3 with 100 items per page: `ORDER BY n.name SKIP 200 LIMIT 100`." %}
