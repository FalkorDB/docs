---
title: "Cypher Language"
nav_order: 7
description: >
    Complete Cypher query language reference for FalkorDB including clauses (MATCH, CREATE, DELETE), functions, procedures, algorithms, and indexing for graph queries.
has_children: true
---

# Cypher Language

FalkorDB supports the [OpenCypher](https://www.opencypher.org/) query language with proprietary extensions. Cypher is a declarative graph query language that allows you to express what data to retrieve from a graph using pattern matching, filtering, and projections.

This section provides a complete reference for all supported Cypher clauses, functions, procedures, and indexing capabilities.

> **See also:** [Data Types](/datatypes) — Reference for all node, relationship, scalar, temporal, and collection types used in Cypher queries.

## Comments

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

## Clauses

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

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="What version of Cypher does FalkorDB support?"
  a1="FalkorDB implements a subset of the **OpenCypher** specification (version 9) with proprietary extensions for indexing, vector search, and graph algorithms. See the [Cypher coverage](/cypher/cypher-support) page for full details."
  q2="How is FalkorDB Cypher different from Neo4j Cypher?"
  a2="FalkorDB supports the core OpenCypher clauses and functions but adds unique features like built-in **vector indexing**, **full-text search** via RediSearch, and native **graph algorithms** (PageRank, BFS, shortest paths). Some advanced Neo4j-specific features like label expressions are not yet supported."
  q3="Can I use parameterized queries in FalkorDB?"
  a3="Yes. Use the `CYPHER` prefix to set parameters, e.g. `CYPHER name='Alice' MATCH (n {name: $name}) RETURN n`. Each client library also provides its own method for passing parameters safely."
  q4="Does FalkorDB support comments in Cypher queries?"
  a4="Yes. FalkorDB supports single-line comments with `//` and multi-line comments with `/* ... */`. Comments can be placed anywhere whitespace is allowed."
  q5="What indexing options are available in FalkorDB?"
  a5="FalkorDB supports three index types: **Range indexes** for exact-match and comparison filters, **Full-text indexes** for text search with stemming and scoring, and **Vector indexes** for similarity search on embeddings."
%}
