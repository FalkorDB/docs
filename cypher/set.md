---
title: "SET"
nav_order: 10
description: >
    SET is used to create or update properties on nodes and relationships.
parent: "Cypher Language"
---

# SET

The `SET` clause is used to create or update properties on nodes and relationships.

## Setting a Single Property

To set a property on a node:

```sh
GRAPH.QUERY DEMO_GRAPH "MATCH (n { name: 'Jim' }) SET n.name = 'Bob'"
```

## Setting Multiple Properties

You can set multiple properties in a single `SET` clause by separating them with commas:

```sh
GRAPH.QUERY DEMO_GRAPH
"MATCH (n { name: 'Jim', age:32 })
SET n.age = 33, n.name = 'Bob'"
```

## Setting Properties from a Map

You can set properties using a map. There are two operators with different behaviors:

### Replace All Properties (`=`)

Replaces **all** existing properties with the map properties:

```sh
GRAPH.QUERY DEMO_GRAPH
"MATCH (n { name: 'Jim', age:32 })
SET n = {age: 33, name: 'Bob'}"
```

**Result:** The node will have only the properties `age` and `name`. Any other existing properties are removed.

### Merge Properties (`+=`)

Updates only the specified properties while keeping other existing properties:

```sh
GRAPH.QUERY DEMO_GRAPH
"MATCH (n { name: 'Jim', age:32 })
SET n += {age: 33}"
```

**Result:** The node's `age` is updated to 33, but `name` and any other properties remain unchanged.

## Copying Properties Between Entities

You can copy all properties from one entity to another:

```sh
GRAPH.QUERY DEMO_GRAPH
"MATCH (jim {name: 'Jim'}), (pam {name: 'Pam'})
SET jim = pam"
```

After executing this query, the `jim` node will have exactly the same properties as the `pam` node (all of Jim's original properties are replaced).

## Removing Properties

To remove a property, set its value to `NULL`:

```sh
GRAPH.QUERY DEMO_GRAPH "MATCH (n { name: 'Jim' }) SET n.name = NULL"
```

This removes the `name` property from the node entirely.
{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="What is the difference between SET n = map and SET n += map?"
  a1="The `=` operator **replaces all** existing properties with the map values. The `+=` operator **merges** properties, updating only specified keys while keeping other existing properties intact."
  q2="Can I remove a property using SET?"
  a2="Yes. Setting a property to NULL removes it: `SET n.name = NULL`. This is equivalent to using the REMOVE clause."
  q3="Can I copy properties from one node to another?"
  a3="Yes. Use `MATCH (a), (b) SET a = b` to copy all of `b`s properties to `a`, replacing any existing properties on `a`."
  q4="Can I SET multiple properties at once?"
  a4="Yes. Separate property assignments with commas: `SET n.age = 33, n.name = 'Bob'`. All assignments are applied in a single operation."
%}
