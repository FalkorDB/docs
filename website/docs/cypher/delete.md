---
title: DELETE
description: >
sidebar_position: 9
sidebar_label: DELETE
---



# DELETE
The `DELETE` clause is used to remove nodes and relationships from the graph.

## Important Behavior

**⚠️ Note:** Deleting a node automatically deletes all of its incoming and outgoing relationships. You cannot have orphaned relationships in the graph.

## Deleting Nodes

To delete a node and all of its relationships:

```sh
GRAPH.QUERY DEMO_GRAPH "MATCH (p:Person {name:'Jim'}) DELETE p"
```

## Deleting Relationships

To delete specific relationships:

```sh
GRAPH.QUERY DEMO_GRAPH "MATCH (:Person {name:'Jim'})-[r:FRIENDS]->() DELETE r"
```

This query deletes all outgoing `FRIENDS` relationships from the node with name 'Jim', while keeping the nodes intact.

## Common Patterns

### Delete all nodes and relationships in a graph

```sh
GRAPH.QUERY DEMO_GRAPH "MATCH (n) DETACH DELETE n"
```

The `DETACH DELETE` automatically removes all relationships before deleting the node.

### Conditional deletion

```sh
GRAPH.QUERY DEMO_GRAPH "MATCH (p:Person) WHERE p.age < 18 DELETE p"
```

Deletes all Person nodes where age is less than 18.