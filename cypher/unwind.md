---
title: "UNWIND"
nav_order: 14
description: >
    The UNWIND clause breaks down a given list into a sequence of records; each contains a single element in the list.
parent: "Cypher Language"
---

# UNWIND

The `UNWIND` clause transforms a list into individual rows, creating one row for each element in the list.

## Behavior

- Each element in the list becomes a separate row
- The order of rows preserves the original list order
- Useful for processing lists, creating multiple entities, or parameter expansion

## Basic Example

Create a node with an array property:

```cypher
CREATE (p {array:[1,2,3]})
```

Unwind the array into individual rows:

```cypher
MATCH (p) UNWIND p.array AS y RETURN y
```

**Result:**
```
y
1
2
3
```

## Practical Examples

### Create Multiple Nodes from a List

```cypher
UNWIND ['Alice', 'Bob', 'Charlie'] AS name
CREATE (:Person {name: name})
```

### Process Nested Data

```cypher
WITH [{name: 'Alice', age: 30}, {name: 'Bob', age: 25}] AS people
UNWIND people AS person
CREATE (:Person {name: person.name, age: person.age})
```

### Combine with Other Clauses

```cypher
MATCH (p:Person)
WITH collect(p.name) AS names
UNWIND names AS name
RETURN name ORDER BY name
```