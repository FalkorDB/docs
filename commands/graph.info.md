---
title: "GRAPH.INFO"
description: >
    Returns information and statistics about the current executing commands
parent: "Commands"
---

# GRAPH.INFO

Returns information and statistics about currently running and waiting queries.

## Syntax

```
GRAPH.INFO [RunningQueries | WaitingQueries]
```

If no argument is provided, both running and waiting queries are returned.

## Examples

```sh
127.0.0.1:6379> GRAPH.INFO
1) "# Running queries"
2) (empty array)
3) "# Waiting queries"
4) (empty array)

127.0.0.1:6379> GRAPH.INFO RunningQueries
1) "# Running queries"
2) (empty array)

127.0.0.1:6379> GRAPH.INFO WaitingQueries
1) "# Waiting queries"
2) (empty array)
```
