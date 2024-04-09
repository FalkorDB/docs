---
title: "MERGE"
nav_order: 11
description: >
    FalkorDB implements a subset of the Cypher language, which is growing as development continues.
parent: "Cypher Language"
---

# MERGE

The MERGE clause ensures that a path exists in the graph (either the path already exists, or it needs to be created).

MERGE either matches existing nodes and binds them, or it creates new data and binds that.

It’s like a combination of MATCH and CREATE that also allows you to specify what happens if the data was matched or created.

For example, you can specify that the graph must contain a node for a user with a certain name.

If there isn’t a node with the correct name, a new node will be created and its name property set.

Any aliases in the MERGE path that were introduced by earlier clauses can only be matched; MERGE will not create them.

When the MERGE path doesn't rely on earlier clauses, the whole path will always either be matched or created.

If all path elements are introduced by MERGE, a match failure will cause all elements to be created, even if part of the match succeeded.

The MERGE path can be followed by ON MATCH SET and ON CREATE SET directives to conditionally set properties depending on whether or not the match succeeded.

## Merging nodes

To merge a single node with a label:

```sh
GRAPH.QUERY DEMO_GRAPH "MERGE (robert:Critic)"
```

To merge a single node with properties:

```sh
GRAPH.QUERY DEMO_GRAPH "MERGE (charlie { name: 'Charlie Sheen', age: 10 })"
```

To merge a single node, specifying both label and property:

```sh
GRAPH.QUERY DEMO_GRAPH "MERGE (michael:Person { name: 'Michael Douglas' })"
```

## Merging paths

Because MERGE either matches or creates a full path, it is easy to accidentally create duplicate nodes.

For example, if we run the following query on our sample graph:

```sh
GRAPH.QUERY DEMO_GRAPH
"MERGE (charlie { name: 'Charlie Sheen '})-[r:ACTED_IN]->(wallStreet:Movie { name: 'Wall Street' })"
```

Even though a node with the name 'Charlie Sheen' already exists, the full pattern does not match, so 1 relation and 2 nodes - including a duplicate 'Charlie Sheen' node - will be created.

We should use multiple MERGE clauses to merge a relation and only create non-existent endpoints:

```sh
GRAPH.QUERY DEMO_GRAPH
"MERGE (charlie { name: 'Charlie Sheen' })
 MERGE (wallStreet:Movie { name: 'Wall Street' })
 MERGE (charlie)-[r:ACTED_IN]->(wallStreet)"
```

If we don't want to create anything if pattern elements don't exist, we can combine MATCH and MERGE clauses. The following query merges a relation only if both of its endpoints already exist:

```sh
GRAPH.QUERY DEMO_GRAPH
"MATCH (charlie { name: 'Charlie Sheen' })
 MATCH (wallStreet:Movie { name: 'Wall Street' })
 MERGE (charlie)-[r:ACTED_IN]->(wallStreet)"
```

## On Match and On Create directives

Using ON MATCH and ON CREATE, MERGE can set properties differently depending on whether a pattern is matched or created.

In this query, we'll merge paths based on a list of properties and conditionally set a property when creating new entities:

```sh
GRAPH.QUERY DEMO_GRAPH
"UNWIND ['Charlie Sheen', 'Michael Douglas', 'Tamara Tunie'] AS actor_name
 MATCH (movie:Movie { name: 'Wall Street' })
 MERGE (person {name: actor_name})-[:ACTED_IN]->(movie)
 ON CREATE SET person.first_role = movie.name"
```
