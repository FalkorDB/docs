---
title: "REMOVE"
nav_order: 23
description: >
    REMOVE is used to remove attributes from node and relationships, in addition to
    removing labels from nodes.
parent: "Cypher Language"
---

# REMOVE

## Example graph

```cypher
CREATE
    (billy :Player {name: 'Billy', score: 84}),
    (andy :Player {name: 'Andy', score: 21}),
    (lori :Player:Admin {name: 'Lori', score: 90})
```

## Remove attributes

The following query removes the 'score' attribute from the node
representing Andy.

```cypher
MATCH (n {name: 'Andy'})
REMOVE n.score
RETURN n.name, n.score
```

Result:

|n.name|n.score|
|------|-------|
|"Andy"| Null  |


## Remove a label from a node

To remove a label from a node use the REMOVE clause as follows:

```cypher
MATCH (n {name: 'Lori'})
REMOVE n:Admin
RETURN n.name, labels(n)
```

Result:

|n.name|labels(n)|
|------|--------|
|"Lori"|[Player]|


## Removing multiple labels from a node

Similar to removing a single label from a node we can use the REMOVE clause
to remove multiple labels in one go

```cypher
MATCH (n :Player {name: 'Lori'})
REMOVE n:Admin:Player
RETURN n.name, labels(n)
```

Result:

|n.name|labels(n)|
|------|--------|
|"Lori"|[]      |

{% include faq_accordion.html title="Frequently Asked Questions" q1="What is the difference between REMOVE and DELETE?" a1="**DELETE** removes entire nodes or relationships from the graph. **REMOVE** removes properties from entities or labels from nodes without deleting the entity itself." q2="How do I remove a property from a node?" a2="Use `MATCH (n {name: 'Andy'}) REMOVE n.score` to remove the `score` property. The property will return null after removal." q3="Can I remove multiple labels at once?" a3="Yes. Use the syntax `REMOVE n:Label1:Label2` to remove multiple labels from a node in a single operation." q4="What is the difference between REMOVE and SET property = NULL?" a4="Both achieve the same result — they remove the property from the entity. `REMOVE n.prop` and `SET n.prop = NULL` are functionally equivalent." %}
