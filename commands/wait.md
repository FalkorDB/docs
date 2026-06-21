---
title: "WAIT"
nav_order: 101
description: > 
  Blocks the current client until all previous write commands are successfully transferred and acknowledged by at least the specified number of replicas
parent: "Commands"
---

# WAIT

The WAIT command in FalkorDB blocks the current client until all previous write commands are successfully transferred and acknowledged by at least the specified number of replicas. This command is useful for ensuring data durability across a FalkorDB deployment.

Usage: `WAIT numreplicas timeout`

## Arguments

* `numreplicas`: The number of replicas that must acknowledge the write operations.
* `timeout`: Maximum time to wait for the required number of replicas to acknowledge, specified in milliseconds.

## Return Value

The command returns the number of replicas that have acknowledged the write operations so far.

## Examples

### Basic Usage

```sh
> GRAPH.QUERY mygraph "CREATE (:Person {name: 'Alice'})"
OK
> WAIT 1 10000
(integer) 1
```

In this example, the client waits for at least 1 replica to acknowledge the GRAPH.QUERY command effect, 
with a timeout of 10 seconds (10000 milliseconds).

## Notes

* The WAIT command only applies to write commands issued by the current connection before the WAIT command.
* If the timeout is reached before the required number of replicas acknowledge, the command returns the number of replicas that acknowledged so far.
* A return value lower than the requested `numreplicas` indicates that the write operation may not be durable on all requested replicas.
* Setting `numreplicas` to 0 will cause the command to return immediately.
* The timeout value of 0 means to block indefinitely until the specified number of replicas acknowledge.
* In a non-replicated FalkorDB instance, the command will always return 0.