---
title: "SET"
nav_order: 10
description: >
    SET is used to create or update properties on nodes and relationships.
parent: "Cypher Language"
redirect_from:
  - /cypher/set.html
  - /cypher/set
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