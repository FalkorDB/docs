---
title: "LIMIT clause"
nav_order: 7
description: >
    FalkorDB implements a subset of the Cypher language, which is growing as development continues.
parent: "Cypher Language"
---

# LIMIT

Although not mandatory, you can use the limit clause
to limit the number of records returned by a query:

```sql
LIMIT <max records to return>
```

If not specified, there's no limit to the number of records returned by a query.