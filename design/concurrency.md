---
title: "Atomicity and Concurrency"
description: >
    How FalkorDB handles atomicity within queries and concurrency across multiple queries, including isolation guarantees and write serialization.
parent: "The FalkorDB Design"
nav_order: 5
---

# Atomicity and Concurrency

This page describes how FalkorDB handles atomicity within individual queries and concurrency when multiple clients issue queries simultaneously.

## Single Query Atomicity

Every query that modifies the graph — using any combination of `CREATE`, `SET`, `DELETE`, or `MERGE` — is **atomic**. The entire query either succeeds completely or fails without applying any partial changes. There is no scenario where a failed query leaves the graph in an intermediate state.

For example, a query that creates several nodes and relationships in one statement either creates all of them or none:

```cypher
CREATE (a:Person {name: 'Alice'})-[:KNOWS]->(b:Person {name: 'Bob'}),
       (b)-[:KNOWS]->(c:Person {name: 'Charlie'})
```

If an error occurs during execution (for example, a constraint violation), none of the nodes or relationships from this query are persisted.

## Compound Clauses

Atomicity extends to queries that use `WITH`, `UNION`, or other compound clauses. A query composed of multiple clauses is executed as a single atomic unit.

For example, the following query is fully atomic — either all changes are applied, or none:

```cypher
MATCH (p:Person {name: 'Alice'})
WITH p
SET p.updated = true
CREATE (p)-[:VISITED]->(c:City {name: 'Portland'})
```

Similarly, a `UNION` query that writes data in multiple branches is treated as one atomic operation.

## Write Ordering

Within a single query, write operations are applied in the order dictated by the Cypher clauses. Earlier clauses are evaluated before later ones, meaning results produced by a `CREATE` are available to a subsequent `SET` or `MATCH` in the same query:

```cypher
CREATE (p:Person {name: 'Dana'})
WITH p
SET p.created_at = timestamp()
RETURN p
```

In this example, the node is created first, then the property is set, and finally the node is returned.

When a single clause produces multiple write operations (for example, `CREATE` creating several nodes), those operations are applied as a batch within that clause.

## Concurrent Queries

FalkorDB uses a **reader-writer concurrency model** per graph. The key guarantees are:

### Multiple Concurrent Readers

Multiple read-only queries can execute in parallel against the same graph. Read queries do not block each other, enabling high throughput for analytics and traversal workloads.

The number of concurrent queries is governed by the [`THREAD_COUNT`](/configuration#thread_count) configuration parameter, which sets the size of the thread pool.

### Serialized Writers

Only **one write query** executes at a time on a given graph. If multiple write queries arrive concurrently, they are queued and executed one at a time in arrival order.

This serialization ensures that:

- Write queries always see the most recent committed state of the graph.
- No two write operations can interleave, preventing race conditions and data corruption.

### Readers and Writers

While a write query is executing, concurrent read queries observe the graph state as it was **before** the write began. Readers are never exposed to partially applied modifications from an in-progress write. Once the write completes, subsequent read queries see the updated state.

This provides an isolation level similar to **snapshot isolation** for readers: each read query sees a consistent view of the graph at the point the query began executing.

## Practical Implications

| Scenario | Behavior |
| :--- | :--- |
| Single write query with multiple clauses | Atomic — all changes apply or none |
| Multiple concurrent read queries | Run in parallel, no blocking |
| Concurrent read + write queries | Readers see the state before the write; no partial reads |
| Multiple concurrent write queries | Serialized — executed one at a time per graph |

### When You Need External Coordination

For most use cases, single-query atomicity combined with write serialization provides sufficient guarantees. However, if your application requires **multi-query transactions** — where several independent queries must all succeed or fail together — you should use Redis `MULTI`/`EXEC` blocks to group them. Note that `MULTI`/`EXEC` serializes all enclosed commands, so concurrent operations on other graphs will also be blocked for the duration of the transaction.

### Performance Considerations

- **Read-heavy workloads** scale well because multiple read queries execute concurrently.
- **Write-heavy workloads** are bottlenecked by write serialization. Consider batching multiple changes into a single query where possible.
- Tune [`THREAD_COUNT`](/configuration#thread_count) to match the parallelism your hardware supports and your workload requires.
