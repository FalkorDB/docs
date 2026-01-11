---
title: "WITH"
nav_order: 12
description: >
    The WITH clause allows parts of queries to be independently executed and have their results handled uniquely.
parent: "Cypher Language"
---

# WITH

The `WITH` clause allows you to chain query parts together, passing results from one part to the next. This enables complex query composition and data manipulations.

## Use Cases

`WITH` is useful for:
- Chaining multiple query parts together
- Performing intermediate aggregations
- Filtering or transforming results before the next query part
- Using query modifiers (`DISTINCT`, `ORDER BY`, `LIMIT`, `SKIP`) mid-query

## Example: Filtering by Aggregated Values

Find all children above the average age of all people:

```sh
GRAPH.QUERY DEMO_GRAPH
"MATCH (p:Person) WITH AVG(p.age) AS average_age MATCH (:Person)-[:PARENT_OF]->(child:Person) WHERE child.age > average_age return child
```

## Example: Using Modifiers Mid-Query

You can use query modifiers with `WITH` to filter or sort before continuing:

```sh
GRAPH.QUERY DEMO_GRAPH
"MATCH (u:User)  WITH u AS nonrecent ORDER BY u.lastVisit LIMIT 3 SET nonrecent.should_contact = true"
```

This query:
1. Matches all users
2. Orders them by last visit (oldest first)
3. Limits to the 3 least recent visitors
4. Sets a flag on those users

## Key Points

- `WITH` acts like a pipeline between query parts
- Variables not included in `WITH` are not available in subsequent parts
- You can rename variables using `AS` in the `WITH` clause
- Aggregations in `WITH` cause implicit grouping (like `RETURN`)