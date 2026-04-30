---
title: "Cypher Language"
nav_order: 7
description: >
    Complete Cypher query language reference for FalkorDB including clauses (MATCH, CREATE, DELETE), functions, procedures, algorithms, and indexing for graph queries.
has_children: true
---

# Comments

FalkorDB Cypher supports two comment styles that can be placed anywhere whitespace is allowed:

| Style | Syntax | Description |
|-------|--------|-------------|
| Single-line | `// comment text` | Everything from `//` to the end of the line is ignored |
| Multi-line  | `/* comment text */` | Everything between `/*` and `*/` is ignored (may span multiple lines) |

Multiple consecutive comments are fully supported, as are comments embedded mid-query:

```cypher
// Find all people named Alice
MATCH (a:Person {name: 'Alice'})
/* Return their
   friends */
RETURN a
```

# Clauses

A Cypher query consists of one or more clauses.

- [MATCH](/cypher/match)
- [OPTIONAL MATCH](/cypher/optional-match)
- [WHERE](/cypher/where)
- [RETURN](/cypher/return)
- [ORDER BY](/cypher/order-by)
- [SKIP](/cypher/skip)
- [LIMIT](/cypher/limit)
- [CREATE](/cypher/create)
- [MERGE](/cypher/merge)
- [DELETE](/cypher/delete)
- [REMOVE](/cypher/remove)
- [SET](/cypher/set)
- [WITH](/cypher/with)
- [UNION](/cypher/union)
- [UNWIND](/cypher/unwind)
- [FOREACH](/cypher/foreach)
- [CALL {}](/cypher/call)

## Functions

See the list of available [functions](/cypher/functions).

## Procedures

See the list of available [procedures](/cypher/procedures).

## Algorithms

See the list of available graph [algorithms](/algorithms).

## Indexing

See how to use [indexing](/cypher/indexing/).
