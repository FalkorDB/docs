---
title: "GRAPH.CONFIG-SET"
description: >
    Updates a FalkorDB configuration
parent: "Commands"    
---

# GRAPH.CONFIG-SET

Set the value of a FalkorDB configuration parameter.

Values set using `GRAPH.CONFIG SET` are not persisted after server restart.

FalkorDB configuration parameters are detailed [here](/configuration).

Note: As detailed in the link above, not all FalkorDB configuration parameters can be set at run-time.

```
127.0.0.1:6379> graph.config get TIMEOUT
1) "TIMEOUT"
2) (integer) 0
127.0.0.1:6379> graph.config set TIMEOUT 10000
OK
127.0.0.1:6379> graph.config get TIMEOUT
1) "TIMEOUT"
2) (integer) 10000
```

```
127.0.0.1:6379> graph.config set THREAD_COUNT 10
(error) This configuration parameter cannot be set at run-time
```
