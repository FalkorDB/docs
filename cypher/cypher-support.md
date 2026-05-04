---
title: "Cypher coverage"
nav_order: 22
description: >
    FalkorDB implements a subset of the Cypher language, which is growing as development continues.
parent: "Cypher Language"
redirect_from:
  - /cypher/cypher_support.html
  - /cypher/cypher_support
---

# Cypher coverage

This document is based on the Cypher Query Language Reference (version 9), available at [OpenCypher Resources](https://www.opencypher.org/resources).

## Patterns

Patterns are fully supported.

## Types

### Structural types

+ Nodes
+ Relationships
+ Path variables (alternating sequence of nodes and relationships).


### Composite types

+ Lists
+ Maps
+ Temporal types (Date, DateTime, LocalDateTime, Time, LocalTime, Duration)

### Literal types

+ Numeric types (64-bit doubles and 64-bit signed integer representations)
+ String literals
+ Booleans

  **Unsupported:**

- Hexadecimal and octal numerics

### Other

NULL is supported as a representation of a missing or undefined value.

## Comparability, equality, orderability, and equivalence

This is a somewhat nebulous area in Cypher itself, with a lot of edge cases.
Broadly speaking, FalkorDB behaves as expected with string and numeric values.
There are likely some behaviors involving the numerics NaN, -inf, inf, and possibly -0.0 that deviate from the Cypher standard.
We do not support any of these properties at the type level, meaning nodes and relationships are not internally comparable.

## Clauses

### Reading Clauses

+ MATCH
+ OPTIONAL MATCH

  **Unsupported:**
  
- Label expressions

### Projecting Clauses

+ RETURN
+ AS
+ WITH
+ UNWIND

### Reading sub-clauses

+ WHERE
+ ORDER BY
+ SKIP
+ LIMIT

### Writing Clauses

+ CREATE
+ DELETE
    + We actually implement DETACH DELETE, the distinction being that relationships invalidated by node deletions are automatically deleted.
+ SET
+ REMOVE (to modify properties and labels). See [REMOVE](/cypher/remove) for details.

### Reading/Writing Clauses

+ MERGE
+ CALL (procedures)
    - The currently-supported procedures are listed in [the Procedures documentation](/commands/graph.query#procedures).

### Set Operations

+ UNION
+ UNION ALL

## Functions

The currently-supported functions are listed in [the Functions documentation](/commands/graph.query#functions).

  **Unsupported:**

- Temporal arithmetic functions
- User-defined functions

## Operators

### Mathematical operators

The currently-supported functions are listed in [the mathematical operators documentation](/commands/graph.query#mathematical-operators).

### String operators

+ String operators (STARTS WITH, ENDS WITH, CONTAINS) are supported.

  **Unsupported:**

- Regex operator

### Boolean operators

+ AND
+ OR
+ NOT
+ XOR

## Parameters

Parameters may be specified to allow for more flexible query construction:

```sh
CYPHER name_param = "Niccolò Machiavelli" birth_year_param = 1469 MATCH (p:Person {name: $name_param, birth_year: $birth_year_param}) RETURN p
```

The example above shows the syntax used by `redis-cli` to set parameters, but
each FalkorDB client introduces a language-appropriate method for setting parameters,
and is described in their documentation.

## Non-Cypher queries

+ FalkorDB provides the `GRAPH.EXPLAIN` command to print the execution plan of a provided query.
+ `GRAPH.DELETE` will remove a graph and all Redis keys associated with it.
- We do not currently provide support for queries that retrieve schemas, though the LABELS and TYPE scalar functions may be used to get a graph overview.

{% include faq_accordion.html title="Frequently Asked Questions" q1="What Cypher specification does FalkorDB follow?" a1="FalkorDB is based on the **OpenCypher Query Language Reference version 9**, available at opencypher.org. It implements a growing subset of the specification with proprietary extensions." q2="Does FalkorDB support regular expressions?" a2="No. The regex operator is not currently supported. Use the string operators `STARTS WITH`, `ENDS WITH`, and `CONTAINS` for pattern matching on strings." q3="Are user-defined functions supported?" a3="No. FalkorDB does not currently support user-defined functions. Use the built-in functions and procedures available in the system." q4="How do I use query parameters?" a4="Use the CYPHER prefix: `CYPHER name='Alice' MATCH (n {name: $name}) RETURN n`. Each FalkorDB client library also provides its own method for passing parameters." q5="What data types are supported?" a5="FalkorDB supports 64-bit doubles, 64-bit signed integers, strings, booleans, NULL, lists, maps, and temporal types (Date, DateTime, LocalDateTime, Time, LocalTime, Duration). Hexadecimal and octal numerics are not supported." %}
