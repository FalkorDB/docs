---
title: "GRAPH.EXPLAIN"
nav_order: 4
description: >
    Returns a query execution plan without running the query
parent: "Commands"    
---

# GRAPH.EXPLAIN

Constructs a query execution plan but does not run it. Inspect this execution plan to better
understand how your query will get executed.

Arguments: `Graph name, Query`

Returns: `String representation of a query execution plan`

```sh
GRAPH.EXPLAIN us_government "MATCH (p:President)-[:BORN]->(h:State {name:'Hawaii'}) RETURN p"
```
