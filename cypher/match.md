---
title: "MATCH"
description: >
    Match describes the relationship between queried entities, using ascii art to represent pattern(s) to match against.
---

# MATCH

The `MATCH` clause describes the relationship between queried entities using ASCII art to represent pattern(s) to match against.

**Syntax Overview:**
- Nodes are represented by parentheses `()`
- Relationships are represented by brackets `[]`
- Each graph entity (node/relationship) can contain an alias, a label/relationship type, and filters, but all are optional

**Entity Structure:** `alias:label {filters}`

Where:
- `alias` - Optional variable name to reference the entity
- `label` - Optional label for nodes or type for relationships  
- `{filters}` - Optional property filters

Example:

```cypher
(a:Actor)-[:ACT]->(m:Movie {title:"straight outta compton"})
```

`a` is an alias for the source node, which we'll be able to refer to at different places within our query.

`Actor` is the label under which this node is marked.

`ACT` is the relationship type.

`m` is an alias for the destination node.

`Movie` destination node is of "type" movie.

`{title:"straight outta compton"}` filters for nodes where the title property equals "straight outta compton".

In this example, we're querying for actor entities that have an "ACT" relationship with the movie entity "straight outta compton".

It is possible to describe broader relationships by composing a multi-hop query such as:

```cypher
(me {name:'swilly'})-[:FRIENDS_WITH]->()-[:FRIENDS_WITH]->(foaf)
```

Here we're interested in finding out who my friends' friends are.

Nodes can have more than one relationship coming in or out of them, for instance:

```cypher
(me {name:'swilly'})-[:VISITED]->(c:Country)<-[:VISITED]-(friend)<-[:FRIENDS_WITH]-(me)
```

Here we're interested in knowing which of my friends have visited at least one country I've been to.

## Variable length relationships

Nodes that are a variable number of relationship→node hops away can be found using the following syntax:

```cypher
-[:TYPE*minHops..maxHops]->
```

`TYPE`, `minHops` and `maxHops` are all optional and default to type agnostic, 1 and infinity, respectively.

When no bounds are given the dots may be omitted. The dots may also be omitted when setting only one bound and this implies a fixed length pattern.

Example:

```cypher
MATCH (charlie:Actor { name: 'Charlie Sheen' })-[:PLAYED_WITH*1..3]->(colleague:Actor)
RETURN colleague
```

Returns all actors related to 'Charlie Sheen' by 1 to 3 hops.

## Bidirectional path traversal

If a relationship pattern does not specify a direction, it will match regardless of which node is the source and which is the destination:

```cypher
-[:TYPE]-
```

Example:

```cypher
MATCH (person_a:Person)-[:KNOWS]-(person_b:Person)
RETURN person_a, person_b
```

Returns all pairs of people connected by a `KNOWS` relationship. Note that each pair will be returned twice, once with each node in the `person_a` field and once in the `person_b` field.

The syntactic sugar `(person_a)<-[:KNOWS]->(person_b)` will return the same results.

The bracketed edge description can be omitted if all relations should be considered: `(person_a)--(person_b)`.

## Named paths

Named path variables are created by assigning a path in a MATCH clause to a single alias with the syntax:
`MATCH named_path = (path)-[to]->(capture)`

The named path includes all entities in the path, regardless of whether they have been explicitly aliased. Named paths can be accessed using built-in functions such as `nodes()` or returned directly if using a language-specific client.

Example:

```cypher
MATCH p=(charlie:Actor { name: 'Charlie Sheen' })-[:PLAYED_WITH*1..3]->(:Actor)
RETURN nodes(p) as actors
```

This query will produce all the paths matching the pattern contained in the named path `p`. All of these paths will share the same starting point, the actor node representing Charlie Sheen, but will otherwise vary in length and contents. Though the variable-length traversal and `(:Actor)` endpoint are not explicitly aliased, all nodes and edges traversed along the path will be included in `p`. In this case, we are only interested in the nodes of each path, which we'll collect using the built-in function `nodes()`. The returned value will contain, in order, Charlie Sheen, between 0 and 2 intermediate nodes, and the unaliased endpoint.
