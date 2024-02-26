---
title: "GRAPH.COPY"
description: >
    creates a copy of the given graph
parent: "Commands"
---

Usage: `GRAPH.COPY <src> <dest>`

The `GRAPH.COPY` command creates a copy of a graph asynchronously, while the copy is performed
the `src` graph is fully accessible.

Overall memory overhead is proportional to the `src` graph size.

Example:
```
127.0.0.1:6379> keys *
(empty array)
127.0.0.1:6379> GRAPH.QUERY A "CREATE (:Account {number: 516637})"
1) 1) "Labels added: 1"
   2) "Nodes created: 1"
   3) "Properties set: 1"
   4) "Cached execution: 0"
   5) "Query internal execution time: 0.588084 milliseconds"
127.0.0.1:6379> GRAPH.COPY A Z
"OK"
127.0.0.1:6379> keys *
1) "Z"
2) "telemetry{A}"
3) "A"
127.0.0.1:6379> GRAPH.QUERY Z "MATCH (a:Account) RETURN a.number"
1) 1) "a.number"
2) 1) 1) (integer) 516637
3) 1) "Cached execution: 0"
   2) "Query internal execution time: 0.638375 milliseconds"
```
