---
title: "DELETE"
nav_order: 9
description: >
    Use the DELETE clause to remove nodes and relationships from FalkorDB graphs. Deleting a node automatically removes all its incoming and outgoing relationships.
parent: "Cypher Language"
---

# DELETE

The `DELETE` clause is used to remove nodes and relationships from the graph.

## Important Behavior

**⚠️ Note:** Deleting a node automatically deletes all of its incoming and outgoing relationships. You cannot have orphaned relationships in the graph.

## Deleting Nodes

To delete a node and all of its relationships:

```cypher
MATCH (p:Person {name:'Jim'}) DELETE p
```

## Deleting Relationships

To delete specific relationships:

```cypher
MATCH (:Person {name:'Jim'})-[r:FRIENDS]->() DELETE r
```

This query deletes all outgoing `FRIENDS` relationships from the node with name 'Jim', while keeping the nodes intact.

## Common Patterns

### Delete all nodes and relationships in a graph

```cypher
MATCH (n) DETACH DELETE n
```

The `DETACH DELETE` automatically removes all relationships before deleting the node.

### Conditional deletion

```cypher
MATCH (p:Person) WHERE p.age < 18 DELETE p
```

Deletes all Person nodes where age is less than 18.