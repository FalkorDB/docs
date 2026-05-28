---
title: "WHERE"
nav_order: 3
description: >
    Optional clause used to filter results based on predicates.
parent: "Cypher Language"
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

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="What comparison operators does WHERE support?"
  a1="FalkorDB supports `=`, `<>`, `<`, `<=`, `>`, `>=`, plus string operators `CONTAINS`, `STARTS WITH`, `ENDS WITH`, and the list operator `IN`."
  q2="Can I combine multiple conditions in WHERE?"
  a2="Yes. Use `AND`, `OR`, and `NOT` logical operators to combine predicates. Parentheses control evaluation precedence."
  q3="What are inline property filters?"
  a3="Inline filters use curly braces within node patterns, e.g. `(n:Person {name: 'Alice'})`. They are functionally equivalent to a WHERE clause equality check but offer more concise syntax."
  q4="Do WHERE predicates benefit from indexes?"
  a4="Yes. When a WHERE clause filters on a property that has a **range index**, FalkorDB automatically uses an index scan instead of a full label scan. Use `GRAPH.EXPLAIN` to verify index usage."
  q5="Can I filter by graph patterns in WHERE?"
  a5="Yes. Pattern predicates like `WHERE (a)-[:KNOWS]->(b)` or negated patterns `WHERE NOT (a)-[:KNOWS]->(b)` can be used directly in the WHERE clause."
%}
