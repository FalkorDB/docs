---
title: "Configuration Parameters"
nav_order: 2
description: >
    FalkorDB supports multiple module configuration parameters. 
---

# Configuration

FalkorDB supports [Redis configuration](https://redis.io/docs/management/config/) and multiple module configuration parameters. 
Some of these parameters can only be set at load-time, while other parameters can be set either on load-time or on run-time.

For example the following will run the server with global authentication password and 4 threads.

```sh
docker run -p 6379:6379 -p 3000:3000 -it -e REDIS_ARGS="--requirepass falkordb" -e FALKORDB_ARGS="THREAD_COUNT 4" --rm falkordb/falkordb:latest
```

> **Production Tip:** For production environments, use the lighter `falkordb/falkordb-server` image which doesn't include the FalkorDB Browser:
> ```sh
> docker run -p 6379:6379 -it -e REDIS_ARGS="--requirepass falkordb" -e FALKORDB_ARGS="THREAD_COUNT 4" --rm falkordb/falkordb-server:latest
> ```

## Setting configuration parameters on module load

Setting configuration parameters at load-time is done by appending arguments after the `--loadmodule` argument when starting a server from the command line or after the `loadmodule` directive in a Redis config file. For example:

In [redis.conf](https://redis.io/docs/manual/config/):

```sh
loadmodule ./falkordb.so [OPT VAL]...
```

From the [Redis CLI](https://redis.io/docs/manual/cli/), using the [MODULE LOAD](https://redis.io/commands/module-load/) command:

```sh
127.0.0.6379> MODULE LOAD falkordb.so [OPT VAL]...
```

From the command line:

```sh
$ redis-server --loadmodule ./falkordb.so [OPT VAL]...
```

When running a docker container

```sh
docker run -p 6379:6379 -p 3000:3000 -it -e FALKORDB_ARGS="[OPT VAL]" --rm falkordb/falkordb:latest
```

Or for production use:

```sh
docker run -p 6379:6379 -it -e FALKORDB_ARGS="[OPT VAL]" --rm falkordb/falkordb-server:latest
```

## Setting configuration parameters at run-time (for supported parameters)

FalkorDB exposes the `GRAPH.CONFIG` command to allowing for the setting and retrieval of configuration parameters at run-time.

To set the value of a configuration parameter at run-time (for supported parameters), simply run:

```sh
GRAPH.CONFIG SET OPT1 VAL1
```

Similarly, current configuration parameter values can be retrieved using:

```sh
GRAPH.CONFIG GET OPT1
GRAPH.CONFIG GET *
```

Values set using `GRAPH.CONFIG SET` are not persisted after server restart.

## FalkorDB configuration parameters

The following table summarizes which configuration parameters can be set at module load-time and which can also be set at run-time:

| Configuration Parameter                                      | Load-time| Run-time|
| :-------                                                     | :-----| :-----|
| [THREAD_COUNT](#thread_count)                                | V     | X     |
| [CACHE_SIZE](#cache_size)                                    | V     | X     |
| [OMP_THREAD_COUNT](#omp_thread_count)                        | V     | X     |
| [NODE_CREATION_BUFFER](#node_creation_buffer)                | V     | X     |
| [BOLT_PORT](#bolt_port)                                      | V     | X     |
| [MAX_QUEUED_QUERIES](#max_queued_queries)                    | V     | V     |
| [TIMEOUT](#timeout)                                          | V     | V     |
| [TIMEOUT_MAX](#timeout_max)                                  | V     | V     |
| [TIMEOUT_DEFAULT](#timeout_default)                          | V     | V     |
| [RESULTSET_SIZE](#resultset_size)                            | V     | V     |
| [QUERY_MEM_CAPACITY](#query_mem_capacity)                    | V     | V     |
| [VKEY_MAX_ENTITY_COUNT](#vkey_max_entity_count)              | V     | V     |
| [EFFECTS_THRESHOLD](#effects_threshold)                      | V     | V     |
| [CMD_INFO](#cmd_info)                                        | V     | V     |
| [MAX_INFO_QUERIES](#max_info_queries)                        | V     | V     |
| [IMPORT_FOLDER](#import_folder)                              | V     | X     |

---

### THREAD_COUNT

The number of threads in FalkorDB's thread pool. This is equivalent to the maximum number of queries that can be processed concurrently.

#### Default

`THREAD_COUNT` defaults to the system's hardware threads (logical cores).

#### Example

```sh
$ redis-server --loadmodule ./falkordb.so THREAD_COUNT 4
```

---

### CACHE_SIZE

The max number of queries for FalkorDB to cache. When a new query is encountered and the cache is full, meaning the cache has reached the size of `CACHE_SIZE`, it will evict the least recently used (LRU) entry.

#### Default

`CACHE_SIZE` default value is 25.

#### Example

```sh
$ redis-server --loadmodule ./falkordb.so CACHE_SIZE 10
```

---

### OMP_THREAD_COUNT

The maximum number of threads that OpenMP may use for computation per query. These threads are used for parallelizing GraphBLAS computations, so may be considered to control concurrency within the execution of individual queries.

#### Default

`OMP_THREAD_COUNT` is defined by GraphBLAS.

#### Example

```sh
$ redis-server --loadmodule ./falkordb.so OMP_THREAD_COUNT 1
```

---

### NODE_CREATION_BUFFER

The node creation buffer is the number of new nodes that can be created without resizing matrices. For example, when set to 16,384, the matrices will have extra space for 16,384 nodes upon creation. Whenever the extra space is depleted, the matrices' size will increase by 16,384.

Reducing this value will reduce memory consumption, but cause performance degradation due to the increased frequency of matrix resizes.

Conversely, increasing it might improve performance for write-heavy workloads but will increase memory consumption.

If the passed argument was not a power of 2, it will be rounded to the next-greatest power of 2 to improve memory alignment.

#### Default

`NODE_CREATION_BUFFER` is 16,384.

#### Minimum

The minimum value for `NODE_CREATION_BUFFER` is 128. Values lower than this will be accepted as arguments, but will internally be converted to 128.

#### Example

```sh
$ redis-server --loadmodule ./falkordb.so NODE_CREATION_BUFFER 200
```

---


### BOLT_PORT
The Bolt port configuration determines the port number on which FalkorDB handles the [bolt protocol](https://en.wikipedia.org/wiki/Bolt_(network_protocol))

#### Default
`BOLT_PORT` -1 (disabled).

#### Example
```sh
$ redis-server --loadmodule ./falkordb.so BOLT_PORT 7687
```

---


### MAX_QUEUED_QUERIES

Setting the maximum number of queued queries allows the server to reject incoming queries with the error message `Max pending queries exceeded`. This reduces the memory overhead of pending queries on an overloaded server and avoids congestion when the server processes its backlog of queries.

#### Default

`MAX_QUEUED_QUERIES` is effectively unlimited (config value of `UINT64_MAX`).

#### Example

```sh
$ redis-server --loadmodule ./falkordb.so MAX_QUEUED_QUERIES 500

$ redis-cli GRAPH.CONFIG SET MAX_QUEUED_QUERIES 500
```

---

### TIMEOUT

(Deprecated in FalkorDB v2.10 It is recommended to use `TIMEOUT_MAX` and `TIMEOUT_DEFAULT` instead)

The `TIMEOUT` configuration parameter specifies the default maximal execution time for read queries, in milliseconds. Write queries do not timeout.

When a read query execution time exceeds the maximal execution time, the query is aborted and the query reply is `(error) Query timed out`.

The `TIMEOUT` query parameter of the `GRAPH.QUERY`, `GRAPH.RO_QUERY`, and `GRAPH.PROFILE` commands can be used to override this value.

#### Default

- Before v2.10: `TIMEOUT` is off (set to `0`).
- Since v2.10: `TIMEOUT` is not specified; `TIMEOUT_MAX` and `TIMEOUT_DEFAULT` are specified instead.

#### Example

```sh
$ redis-server --loadmodule ./falkordb.so TIMEOUT 1000
```

---

### TIMEOUT_MAX

(Since v2.10)

The `TIMEOUT_MAX` configuration parameter specifies the maximum execution time for both read and write queries, in milliseconds.

The `TIMEOUT` query parameter value of the `GRAPH.QUERY`, `GRAPH.RO_QUERY`, and `GRAPH.PROFILE` commands cannot exceed the `TIMEOUT_MAX` value (the command would abort with a `(error) The query TIMEOUT parameter value cannot exceed the TIMEOUT_MAX configuration parameter value` reply). Similarly, the `TIMEOUT_DEFAULT` configuration parameter cannot exceed the `TIMEOUT_MAX` value.

When a query execution time exceeds the maximal execution time, the query is aborted and the query reply is `(error) Query timed out`. For a write query - any change to the graph is undone (which may take additional time).

#### Default

- Before v2.10: unspecified and unsupported.
- Since v2.10: `TIMEOUT_MAX` is off (set to `0`).

#### Example

```sh
$ redis-server --loadmodule ./falkordb.so TIMEOUT_MAX 1000
```

---

### TIMEOUT_DEFAULT

(Since v2.10)

The `TIMEOUT_DEFAULT` configuration parameter specifies the default maximal execution time for both read and write queries, in milliseconds.

For a given query, this default maximal execution time can be overridden by the `TIMEOUT` query parameter of the `GRAPH.QUERY`, `GRAPH.RO_QUERY`, and `GRAPH.PROFILE` commands. However, a query execution time cannot exceed `TIMEOUT_MAX`.

#### Default

- Before v2.10: unspecified and unsupported.
- Since v2.10: `TIMEOUT_DEFAULT` is equal to `TIMEOUT_MAX` (set to `0`).

#### Example

```sh
$ redis-server --loadmodule ./falkordb.so TIMEOUT_MAX 2000 TIMEOUT_DEFAULT 1000
```

---

### RESULTSET_SIZE

Result set size is a limit on the number of records that should be returned by any query. This can be a valuable safeguard against incurring a heavy IO load while running queries with unknown results.

#### Default

`RESULTSET_SIZE` is unlimited (negative config value).

#### Example

```sh
127.0.0.1:6379> GRAPH.CONFIG SET RESULTSET_SIZE 3
OK
127.0.0.1:6379> GRAPH.QUERY G "UNWIND range(1, 5) AS x RETURN x"
1) 1) "x"
2) 1) 1) (integer) 1
   2) 1) (integer) 2
   3) 1) (integer) 3
3) 1) "Cached execution: 0"
   2) "Query internal execution time: 0.445790 milliseconds"
```

---

### QUERY_MEM_CAPACITY

Setting the memory capacity of a query allows the server to kill queries that are consuming too much memory and return with the error message `Query's mem consumption exceeded capacity`. This helps to avoid scenarios when the server becomes unresponsive due to an unbounded query exhausting system resources.

The configuration argument is the maximum number of bytes that can be allocated by any single query.

#### Default

`QUERY_MEM_CAPACITY` is unlimited; this default can be restored by setting `QUERY_MEM_CAPACITY` to zero or a negative value.

#### Example

```sh
$ redis-server --loadmodule ./falkordb.so QUERY_MEM_CAPACITY 1048576 // 1 megabyte limit

$ redis-cli GRAPH.CONFIG SET QUERY_MEM_CAPACITY 1048576
```

---

### VKEY_MAX_ENTITY_COUNT

To lower the time Redis is blocked when replicating large graphs,
FalkorDB serializes the graph in a number of virtual keys.

One virtual key is created for every N graph entities,
where N is the value defined by this configuration.

This configuration can be set when the module loads or at runtime.

#### Default

`VKEY_MAX_ENTITY_COUNT` is 100,000.

### CMD_INFO

An on/off toggle for the `GRAPH.INFO` command. Disabling this command may increase performance and lower the memory usage and these are the main reasons for it to be disabled.

It's valid values are 'yes' and 'no' (i.e., on and off).

#### Default

`CMD_INFO` is `yes`.

### MAX_INFO_QUERIES

A limit for the number of previously executed queries stored in the telemetry stream.

A number within the range [0, 1000]

#### Default

`MAX_INFO_QUERIES` is 1000.

---

## Query Configurations

### Query Timeout

- Before v2.10, or if `TIMEOUT_DEFAULT` and `TIMEOUT_MAX` are not specified:

  `TIMEOUT` allows overriding the `TIMEOUT` configuration parameter for a single read query. Write queries do not timeout.

- Since v2.10, if either `TIMEOUT_DEFAULT` or `TIMEOUT_MAX` are specified:

  `TIMEOUT` allows overriding the `TIMEOUT_DEFAULT` configuration parameter value for a single `GRAPH.QUERY`, `GRAPH.RO_QUERY`, or `GRAPH.PROFILE` command. The `TIMEOUT` value cannot exceed the `TIMEOUT_MAX` value (the command would abort with a `(error) The query TIMEOUT parameter value cannot exceed the TIMEOUT_MAX configuration parameter value` reply).

#### Example

Retrieve all paths in a graph with a timeout of 500 milliseconds.

```sh
GRAPH.QUERY wikipedia "MATCH p=()-[*]->() RETURN p" TIMEOUT 500
```

---

### EFFECTS_THRESHOLD

Replicate modification via effect when average modification time > `EFFECTS_THRESHOLD`

#### Default

`EFFECTS_THRESHOLD` is 300 μs.

#### Example

Assume `MATCH (n) WHERE n.id < 100 SET n.v = n.v + 1` updated 5 nodes
and the query total execution time is 5ms, the average modification time is:
total execution time / number of changes:  5ms / 5 = 1ms.
if the average modification time is greater then `EFFECTS_THRESHOLD` the query
will be replicated to both replicas and AOF as a graph effect otherwise the original
query will be replicated.

---


### IMPORT_FOLDER

The import folder configuration specifies an absolute path to a folder from which
FalkorDB is allowed to load CSV files.

Defaults to: `/var/lib/FalkorDB/import/`

---
