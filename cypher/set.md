---
title: "SET clause"
nav_order: 10
description: >
    FalkorDB implements a subset of the Cypher language, which is growing as development continues.
parent: "Cypher Language"
---

# SET

SET is used to create or update properties on nodes and relationships.

To set a property on a node, use `SET`.

```sh
GRAPH.QUERY DEMO_GRAPH "MATCH (n { name: 'Jim' }) SET n.name = 'Bob'"
```

If you want to set multiple properties in one go, simply separate them with a comma to set multiple properties using a single SET clause.

```sh
GRAPH.QUERY DEMO_GRAPH
"MATCH (n { name: 'Jim', age:32 })
SET n.age = 33, n.name = 'Bob'"
```

The same can be accomplished by setting the graph entity variable to a map:

```sh
GRAPH.QUERY DEMO_GRAPH
"MATCH (n { name: 'Jim', age:32 })
SET n = {age: 33, name: 'Bob'}"
```

Using `=` in this way replaces all of the entity's previous properties, while `+=` will only set the properties it explicitly mentions.

In the same way, the full property set of a graph entity can be assigned or merged:

```sh
GRAPH.QUERY DEMO_GRAPH
"MATCH (jim {name: 'Jim'}), (pam {name: 'Pam'})
SET jim = pam"
```

After executing this query, the `jim` node will have the same property set as the `pam` node.

To remove a node's property, simply set property value to NULL.

```sh
GRAPH.QUERY DEMO_GRAPH "MATCH (n { name: 'Jim' }) SET n.name = NULL"
```