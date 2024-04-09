---
title: "CREATE"
nav_order: 8
description: >
    FalkorDB implements a subset of the Cypher language, which is growing as development continues.
parent: "Cypher Language"
---

# CREATE

CREATE is used to introduce new nodes and relationships.

The simplest example of CREATE would be a single node creation:

```sh
CREATE (n)
```

It's possible to create multiple entities by separating them with a comma.

```sh
CREATE (n),(m)
```

```sh
CREATE (:Person {name: 'Kurt', age: 27})
```

To add relations between nodes, in the following example we first find an existing source node. After it's found, we create a new relationship and destination node.

```sh
GRAPH.QUERY DEMO_GRAPH
"MATCH (a:Person)
WHERE a.name = 'Kurt'
CREATE (a)-[:MEMBER]->(:Band {name:'Nirvana'})"
```

Here the source node is a bounded node, while the destination node is unbounded.

As a result, a new node is created representing the band Nirvana and a new relation connects Kurt to the band.

Lastly we create a complete pattern.

All entities within the pattern which are not bounded will be created.

```sh
GRAPH.QUERY DEMO_GRAPH
"CREATE (jim:Person{name:'Jim', age:29})-[:FRIENDS]->(pam:Person {name:'Pam', age:27})-[:WORKS]->(:Employer {name:'Dunder Mifflin'})"
```

This query will create three nodes and two relationships.
