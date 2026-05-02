---
title: "Performance & Query Optimization"
parent: "Operations"
nav_order: 15
description: "Guide to optimizing FalkorDB query performance: index selection, GRAPH.EXPLAIN and GRAPH.PROFILE output interpretation, cache tuning, parameterized queries, and best practices."
---

# Performance & Query Optimization

This guide helps you understand and improve FalkorDB query performance. It covers when and how to create indexes, how to read execution plans, cache tuning, parameterized queries, and general best practices.

---

## 1. Understanding Query Execution

Every Cypher query goes through these stages:

1. **Parsing** — The query string is parsed into an abstract syntax tree
2. **Planning** — An execution plan is generated (or retrieved from cache)
3. **Execution** — The plan is executed against the graph data

You can inspect the plan without executing using [GRAPH.EXPLAIN](/commands/graph.explain), or execute and see per-operation metrics using [GRAPH.PROFILE](/commands/graph.profile).

---

## 2. Using GRAPH.EXPLAIN

`GRAPH.EXPLAIN` shows the execution plan **without running** the query. Use it to check whether your query uses indexes or falls back to full scans.

```
GRAPH.EXPLAIN myGraph "MATCH (p:Person {name: 'Alice'})-[:KNOWS]->(friend) RETURN friend.name"
```

**Example output:**

```
1) "Results"
2) "    Project"
3) "        Conditional Traverse | (p)->(friend:Person)"
4) "            Index Scan | (p:Person)"
```

### What to look for

| Operation | Meaning | Performance Impact |
|:---|:---|:---|
| **Index Scan** | Uses an index to find starting nodes | ✅ Fast |
| **Node By Label Scan** | Scans all nodes with a given label | ⚠️ Slow on large graphs |
| **All Node Scan** | Scans every node in the graph | ❌ Very slow |
| **Conditional Traverse** | Follows relationships from known nodes | ✅ Generally efficient |
| **Filter** | Applies a WHERE predicate | Depends on position in plan |

**Rule of thumb:** If you see `Node By Label Scan` or `All Node Scan` for a query that filters on a property, you need an index.

---

## 3. Using GRAPH.PROFILE

`GRAPH.PROFILE` **executes** the query and returns per-operation metrics: records produced and execution time.

```
GRAPH.PROFILE myGraph "MATCH (p:Person {name: 'Alice'})-[:KNOWS]->(friend) RETURN friend.name"
```

**Example output:**

```
1) "Results | Records produced: 3, Execution time: 0.25 ms"
2) "    Project | Records produced: 3, Execution time: 0.02 ms"
3) "        Conditional Traverse | Records produced: 3, Execution time: 0.15 ms"
4) "            Index Scan | (p:Person) | Records produced: 1, Execution time: 0.05 ms"
```

### Interpreting the output

- **Records produced** shows how many intermediate results flow through each operation
- **Execution time** shows where the query spends most of its time
- High record counts at early stages indicate the query is processing too much data — consider adding filters or indexes to narrow results earlier

> **Important:** `GRAPH.PROFILE` actually executes the query, including any write operations. Use `GRAPH.EXPLAIN` for write queries you want to inspect without executing.

---

## 4. Index Selection

Indexes dramatically speed up queries that filter on node properties. FalkorDB supports three index types:

### Range Index

Best for equality checks, comparisons, and range queries on scalar properties.

```cypher
CREATE INDEX FOR (p:Person) ON (p.name)
CREATE INDEX FOR (p:Person) ON (p.age)
```

**When to create a range index:**
- You frequently filter by `WHERE n.property = value`
- You use range comparisons (`<`, `>`, `<=`, `>=`)
- You use `ORDER BY` on the property

See [Range Index](/cypher/indexing/range-index) for full details.

### Full-Text Index

Best for text search with stemming, fuzzy matching, and relevance scoring.

```cypher
CALL db.idx.fulltext.createNodeIndex('Document', 'content')
```

See [Full-Text Index](/cypher/indexing/fulltext-index) for details.

### Vector Index

Best for similarity search on embedding vectors.

```cypher
CALL db.idx.vector.createNodeIndex('Document', 'embedding', 768, 'cosine')
```

See [Vector Index](/cypher/indexing/vector-index) for details.

### Index best practices

- **Index properties you filter on** — if a query has `WHERE n.prop = value`, index `prop`
- **Don't over-index** — each index consumes memory and adds write overhead
- **Check with GRAPH.EXPLAIN** — verify your index is actually being used
- **Composite filtering** — if you filter on multiple properties, index the most selective one (the one with the most distinct values)

---

## 5. Parameterized Queries

Always use parameterized queries instead of string interpolation. This improves both **security** (prevents injection) and **performance** (enables query cache reuse).

**❌ Bad — string interpolation (new plan compiled every time):**

```python
name = "Alice"
graph.query(f"MATCH (p:Person {{name: '{name}'}}) RETURN p")
```

**✅ Good — parameterized (plan is cached and reused):**

```python
graph.query("MATCH (p:Person {name: $name}) RETURN p", params={"name": "Alice"})
```

With parameters, FalkorDB caches the compiled execution plan and reuses it for subsequent calls with different parameter values.

---

## 6. Cache Tuning

FalkorDB caches compiled query execution plans to avoid re-parsing and re-planning repeated queries.

### CACHE_SIZE

Controls the maximum number of cached query plans (LRU eviction):

```
GRAPH.CONFIG SET CACHE_SIZE 100
```

**Default:** 25

**Tuning guidance:**
- Increase `CACHE_SIZE` if your application uses many distinct query patterns
- Monitor cache effectiveness using `GRAPH.SLOWLOG` — if the same queries appear repeatedly, the cache may be too small
- Each cached plan consumes memory, so balance cache size against available RAM

See [Configuration — CACHE_SIZE](/getting-started/configuration#cache_size) for details.

---

## 7. Query Optimization Patterns

### Use LIMIT for exploration

When exploring data, always add `LIMIT` to avoid processing the entire graph:

```cypher
MATCH (n:Person)-[:KNOWS]->(m) RETURN n.name, m.name LIMIT 25
```

### Filter early with WHERE

Place filtering conditions as early as possible in the query to reduce intermediate result sets:

```cypher
// ✅ Good — filter narrows results early
MATCH (p:Person {name: 'Alice'})-[:KNOWS]->(friend)
RETURN friend

// ⚠️ Less efficient — filter applied after full traversal
MATCH (p:Person)-[:KNOWS]->(friend)
WHERE p.name = 'Alice'
RETURN friend
```

### Use read-only queries when possible

Use `GRAPH.RO_QUERY` instead of `GRAPH.QUERY` for read-only operations. Read-only queries can be distributed to replicas, reducing load on the primary.

### Avoid unbounded variable-length paths

```cypher
// ❌ Dangerous — unbounded path can explode combinatorially
MATCH (a)-[*]->(b) RETURN a, b

// ✅ Better — bound the path length
MATCH (a)-[*1..3]->(b) RETURN a, b
```

### Use WITH to break complex queries

Break complex queries into stages using `WITH`. This helps the query planner optimize each stage independently:

```cypher
MATCH (p:Person {name: 'Alice'})-[:KNOWS]->(friend)
WITH friend
MATCH (friend)-[:WORKS_AT]->(company)
RETURN friend.name, company.name
```

---

## 8. Monitoring Query Performance

### GRAPH.SLOWLOG

View queries that took ≥ 10 ms:

```
GRAPH.SLOWLOG myGraph
```

Each entry shows: timestamp, command, query, latency, and query parameters (if any).

See [GRAPH.SLOWLOG](/commands/graph.slowlog) for details.

### Key metrics to watch

| Metric | How to check | What it tells you |
|:---|:---|:---|
| Query latency | `GRAPH.SLOWLOG` | Which queries are slow |
| Memory usage | `GRAPH.MEMORY myGraph` | Graph memory footprint |
| Thread utilization | `GRAPH.CONFIG GET THREAD_COUNT` | Parallelism capacity |
| Cache size | `GRAPH.CONFIG GET CACHE_SIZE` | Plan cache capacity |

---

## Quick Reference Checklist

- [ ] **Indexes created** for properties used in WHERE filters
- [ ] **GRAPH.EXPLAIN** shows Index Scan (not Label/All Node Scan) for filtered queries
- [ ] **Parameterized queries** used (not string interpolation)
- [ ] **LIMIT** applied to exploratory and UI-facing queries
- [ ] **GRAPH.RO_QUERY** used for read-only operations
- [ ] **Variable-length paths bounded** with min/max hop limits
- [ ] **CACHE_SIZE** tuned for the number of distinct query patterns
- [ ] **GRAPH.SLOWLOG** reviewed periodically for regression

---

## Related Pages

- [GRAPH.EXPLAIN](/commands/graph.explain) — View execution plan without running
- [GRAPH.PROFILE](/commands/graph.profile) — Execute and view plan with metrics
- [GRAPH.SLOWLOG](/commands/graph.slowlog) — View slow query log
- [Range Index](/cypher/indexing/range-index) — Create and manage range indexes
- [Vector Index](/cypher/indexing/vector-index) — Vector similarity search indexes
- [Full-Text Index](/cypher/indexing/fulltext-index) — Text search indexes
- [Configuration](/getting-started/configuration) — CACHE_SIZE, THREAD_COUNT, TIMEOUT, and more
