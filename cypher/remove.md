---
title: "REMOVE"
nav_order: 23
description: >
    REMOVE is used to remove attributes from node and relationships, in addition to
    removing labels from nodes.
parent: "Cypher Language"
redirect_from:
  - /cypher/remove.html
  - /cypher/remove
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
