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
{% include faq_accordion.html title="Frequently Asked Questions" q1="What happens to relationships when I delete a node?" a1="Deleting a node **automatically deletes** all of its incoming and outgoing relationships. FalkorDB does not allow orphaned relationships in the graph." q2="What is the difference between DELETE and DETACH DELETE?" a2="In FalkorDB, DELETE actually implements DETACH DELETE behavior — relationships are automatically removed when their endpoint nodes are deleted. Both keywords work the same way." q3="How do I delete all data in a graph?" a3="Use `MATCH (n) DETACH DELETE n` to remove all nodes and their relationships. Alternatively, use the `GRAPH.DELETE` command to remove the entire graph key." q4="Can I delete specific relationships without deleting nodes?" a4="Yes. Match the relationship with an alias and delete only it: `MATCH (a)-[r:KNOWS]->(b) DELETE r`. The nodes remain intact." %}
