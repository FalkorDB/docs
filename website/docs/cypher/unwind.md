---
title: UNWIND
description: >
sidebar_position: 14
sidebar_label: UNWIND
---



# UNWIND
The `UNWIND` clause transforms a list into individual rows, creating one row for each element in the list.

## Behavior

- Each element in the list becomes a separate row
- The order of rows preserves the original list order
- Useful for processing lists, creating multiple entities, or parameter expansion

## Basic Example

Create a node with an array property:

```sh
GRAPH.QUERY DEMO_GRAPH "CREATE (p {array:[1,2,3]})"
```

Unwind the array into individual rows:

```sh
GRAPH.QUERY DEMO_GRAPH "MATCH (p) UNWIND p.array AS y RETURN y"
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

```sh
GRAPH.QUERY DEMO_GRAPH
"UNWIND ['Alice', 'Bob', 'Charlie'] AS name
CREATE (:Person {name: name})"
```

### Process Nested Data

```sh
GRAPH.QUERY DEMO_GRAPH
"WITH [{name: 'Alice', age: 30}, {name: 'Bob', age: 25}] AS people
UNWIND people AS person
CREATE (:Person {name: person.name, age: person.age})"
```

### Combine with Other Clauses

```sh
GRAPH.QUERY DEMO_GRAPH
"MATCH (p:Person)
WITH collect(p.name) AS names
UNWIND names AS name
RETURN name ORDER BY name"
```