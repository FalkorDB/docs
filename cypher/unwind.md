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

```sh
GRAPH.QUERY DEMO_GRAPH "CREATE (p {array:[1,2,3]})"
```

Unwind the array into individual rows:

```sh
GRAPH.QUERY DEMO_GRAPH "MATCH (p) UNWIND p.array AS y RETURN y"
```

**Result:**
```text
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
{% include faq_accordion.html title="Frequently Asked Questions" q1="What does UNWIND do?" a1="UNWIND transforms a list into individual rows, creating one row per element. It is the inverse of the `collect()` aggregation function." q2="Can I UNWIND a literal list?" a2="Yes. You can unwind inline lists directly: `UNWIND ['Alice', 'Bob'] AS name CREATE (:Person {name: name})`. This is useful for batch operations." q3="What happens if I UNWIND an empty list?" a3="If the list is empty, UNWIND produces zero rows, effectively eliminating that record from the result stream. No subsequent clauses will execute for that record." q4="Can I UNWIND nested lists or maps?" a4="Yes. You can unwind lists of maps and access their properties: `UNWIND [{name: 'Alice'}, {name: 'Bob'}] AS person CREATE (:Person {name: person.name})`." %}
