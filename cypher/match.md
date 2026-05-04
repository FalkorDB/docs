---
title: "MATCH"
nav_order: 1
description: >
    Match describes the relationship between queried entities, using ascii art to represent pattern(s) to match against.
parent: "Cypher Language"
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

```sh
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

```sh
(me {name:'swilly'})-[:FRIENDS_WITH]->()-[:FRIENDS_WITH]->(foaf)
```

Here we're interested in finding out who my friends' friends are.

Nodes can have more than one relationship coming in or out of them, for instance:

```sh
(me {name:'swilly'})-[:VISITED]->(c:Country)<-[:VISITED]-(friend)<-[:FRIENDS_WITH]-(me)
```

Here we're interested in knowing which of my friends have visited at least one country I've been to.

## Variable length relationships

Nodes that are a variable number of relationship→node hops away can be found using the following syntax:

```sh
-[:TYPE*minHops..maxHops]->
```

`TYPE`, `minHops` and `maxHops` are all optional and default to type agnostic, 1 and infinity, respectively.

When no bounds are given the dots may be omitted. The dots may also be omitted when setting only one bound and this implies a fixed length pattern.

Example:

```sh
GRAPH.QUERY DEMO_GRAPH
"MATCH (charlie:Actor { name: 'Charlie Sheen' })-[:PLAYED_WITH*1..3]->(colleague:Actor)
RETURN colleague"
```

Returns all actors related to 'Charlie Sheen' by 1 to 3 hops.

## Bidirectional path traversal

If a relationship pattern does not specify a direction, it will match regardless of which node is the source and which is the destination:

```sh
-[:TYPE]-
```

Example:

```sh
GRAPH.QUERY DEMO_GRAPH
"MATCH (person_a:Person)-[:KNOWS]-(person_b:Person)
RETURN person_a, person_b"
```

Returns all pairs of people connected by a `KNOWS` relationship. Note that each pair will be returned twice, once with each node in the `person_a` field and once in the `person_b` field.

The syntactic sugar `(person_a)<-[:KNOWS]->(person_b)` will return the same results.

The bracketed edge description can be omitted if all relations should be considered: `(person_a)--(person_b)`.

## Named paths

Named path variables are created by assigning a path in a MATCH clause to a single alias with the syntax:
`MATCH named_path = (path)-[to]->(capture)`

The named path includes all entities in the path, regardless of whether they have been explicitly aliased. Named paths can be accessed using [designated built-in functions](#path-functions) or returned directly if using a language-specific client.

Example:

```sh
GRAPH.QUERY DEMO_GRAPH
"MATCH p=(charlie:Actor { name: 'Charlie Sheen' })-[:PLAYED_WITH*1..3]->(:Actor)
RETURN nodes(p) as actors"
```

This query will produce all the paths matching the pattern contained in the named path `p`. All of these paths will share the same starting point, the actor node representing Charlie Sheen, but will otherwise vary in length and contents. Though the variable-length traversal and `(:Actor)` endpoint are not explicitly aliased, all nodes and edges traversed along the path will be included in `p`. In this case, we are only interested in the nodes of each path, which we'll collect using the built-in function `nodes()`. The returned value will contain, in order, Charlie Sheen, between 0 and 2 intermediate nodes, and the unaliased endpoint.

{% include faq_accordion.html title="Frequently Asked Questions" q1="What does the MATCH clause do in FalkorDB?" a1="The `MATCH` clause uses ASCII-art pattern syntax to find nodes and relationships in the graph that satisfy the specified pattern. It is the primary read operation in Cypher." q2="Can I traverse variable-length paths with MATCH?" a2="Yes. Use the syntax `-[:TYPE*minHops..maxHops]->` to match paths of varying length. Both bounds are optional and default to 1 and infinity respectively." q3="What is a bidirectional relationship pattern?" a3="A relationship pattern without a direction arrow (e.g. `-[:KNOWS]-`) matches regardless of which node is source or destination. The shorthand `<-[:KNOWS]->` produces the same result." q4="How do named paths work?" a4="Assign a MATCH pattern to a variable with `p = (a)-[r]->(b)`. The path variable `p` includes all nodes and relationships in the matched pattern and can be used with built-in functions like `nodes(p)` and `relationships(p)`." q5="Do I need to specify labels and aliases in MATCH?" a5="No. All parts of the entity structure (`alias:label {filters}`) are optional. However, specifying labels improves query performance by narrowing the search scope, especially when indexes exist on those labels." %}
