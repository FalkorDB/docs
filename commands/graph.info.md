---
title: "GRAPH.INFO"
description: >
    Returns information and statistics about the current executing commands
parent: "Commands"
nav_order: 10
---

# GRAPH.INFO

Returns information and statistics about currently running queries, waiting queries, and the object pool.

## Syntax

```text
GRAPH.INFO [Section [Section ...]]
```

Where each `Section` is one of:

- `RunningQueries` — lists currently executing queries
- `WaitingQueries` — lists queries waiting to be executed
- `ObjectPool` — reports object pool statistics

Multiple sections can be specified simultaneously. If no section is provided, all sections are returned.

## Examples

```sh
127.0.0.1:6379> GRAPH.INFO
1) "# Running queries"
2) (empty array)
3) "# Waiting queries"
4) (empty array)
5) "Object Pool"
6) 1) 1) "Unique Objects in Pool"
      2) (integer) 0
   2) 1) "Average References per Object"
      2) (double) 0

127.0.0.1:6379> GRAPH.INFO RunningQueries
1) "# Running queries"
2) (empty array)

127.0.0.1:6379> GRAPH.INFO WaitingQueries
1) "# Waiting queries"
2) (empty array)

127.0.0.1:6379> GRAPH.INFO ObjectPool
1) "Object Pool"
2) 1) 1) "Unique Objects in Pool"
      2) (integer) 0
   2) 1) "Average References per Object"
      2) (double) 0

127.0.0.1:6379> GRAPH.INFO RunningQueries WaitingQueries ObjectPool
1) "# Running queries"
2) (empty array)
3) "# Waiting queries"
4) (empty array)
5) "Object Pool"
6) 1) 1) "Unique Objects in Pool"
      2) (integer) 0
   2) 1) "Average References per Object"
      2) (double) 0
```
