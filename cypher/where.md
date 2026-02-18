---
title: "WHERE"
nav_order: 3
description: >
    Optional clause used to filter results based on predicates.
parent: "Cypher Language"
redirect_from:
  - /cypher/where.html
  - /cypher/where
---

# WHERE

The `WHERE` clause is optional and is used to filter results based on predicates (conditions).

## Supported Comparison Operators

| Operator | Description |
|----------|-------------|
| `=` | Equal to |
| `<>` | Not equal to |
| `<` | Less than |
| `<=` | Less than or equal to |
| `>` | Greater than |
| `>=` | Greater than or equal to |
| `CONTAINS` | String contains substring |
| `ENDS WITH` | String ends with substring |
| `IN` | Value is in list |
| `STARTS WITH` | String starts with substring |

## Combining Predicates

Predicates can be combined using the logical operators `AND`, `OR`, and `NOT`.

Use parentheses to control precedence when combining multiple predicates.

### Examples:

```sql
WHERE (actor.name = "john doe" OR movie.rating > 8.8) AND movie.votes <= 250
```

```sql
WHERE actor.age >= director.age AND actor.age > 32
```

## Inline Property Filters

You can specify equality predicates directly within node patterns using curly braces:

```sql
(:President {name:"Jed Bartlett"})-[:WON]->(:State)
```

This requires that the president node's `name` property equals "Jed Bartlett".

Inline predicates are functionally equivalent to predicates specified in the WHERE clause.

## Pattern Predicates

You can also filter based on graph patterns. These two queries are equivalent and both return presidents and the states they won:

```sh
MATCH (p:President), (s:State) WHERE (p)-[:WON]->(s) RETURN p, s
```

```sh
MATCH (p:President)-[:WON]->(s:State) RETURN p, s
```

Pattern predicates can be negated and combined with logical operators. This query returns presidents who did not win in states where they were governors:

```sh
MATCH (p:President), (s:State) WHERE NOT (p)-[:WON]->(s) AND (p)-[:GOVERNOR]->(s) RETURN p, s
```

## Label Filtering

Nodes can be filtered by label in the WHERE clause:

```sh
MATCH (n)-[:R]->() WHERE n:L1 OR n:L2 RETURN n 
```

**Best Practice:** When possible, specify labels directly in the node pattern of the MATCH clause for better performance.
