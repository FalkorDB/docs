---
title: "CREATE"
nav_order: 8
description: >
    Use the CREATE clause to add new nodes and relationships to FalkorDB graphs. Create single or multiple entities, set properties and labels, and build complete graph patterns.
parent: "Cypher Language"
---

# CREATE

The `CREATE` clause is used to introduce new nodes and relationships into the graph.

## Creating Nodes

The simplest example creates a single node without any labels or properties:

```cypher
CREATE (n)
```

You can create multiple entities by separating them with commas:

```cypher
CREATE (n),(m)
```

Create a node with a label and properties:

```cypher
CREATE (:Person {name: 'Kurt', age: 27})
```

## Creating Relationships

To add relationships between nodes, you typically match existing nodes first, then create the relationship. In this example, we find an existing source node and create a new relationship with a new destination node:

```cypher
MATCH (a:Person)
WHERE a.name = 'Kurt'
CREATE (a)-[:MEMBER]->(:Band {name:'Nirvana'})
```

Here the source node `(a:Person)` is matched (bound), while the destination node `(:Band)` is unbound and will be created.

This query creates a new node representing the band Nirvana and a new `MEMBER` relationship connecting Kurt to the band.

## Creating Complete Patterns

You can create entire graph patterns in a single statement. All entities within the pattern that are not bound (matched) will be created:

```cypher
CREATE (jim:Person{name:'Jim', age:29})-[:FRIENDS]->(pam:Person {name:'Pam', age:27})-[:WORKS]->(:Employer {name:'Dunder Mifflin'})
```

This query creates three nodes (Jim, Pam, and an Employer) and two relationships (FRIENDS and WORKS), establishing a complete graph pattern in one operation.
