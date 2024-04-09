---
title: "MATCH"
nav_order: 1
description: >
    FalkorDB implements a subset of the Cypher language, which is growing as development continues.
parent: "Cypher Language"
---

# MATCH

Match describes the relationship between queried entities, using ascii art to represent pattern(s) to match against.

Nodes are represented by parentheses `()`,
and Relationships are represented by brackets `[]`.

Each graph entity node/relationship can contain an alias and a label/relationship type, but both can be left empty if necessary.

Entity structure: `alias:label {filters}`.

Alias, label/relationship type, and filters are all optional.

Example:

```sh
(a:Actor)-[:ACT]->(m:Movie {title:"straight outta compton"})
```

`a` is an alias for the source node, which we'll be able to refer to at different places within our query.

`Actor` is the label under which this node is marked.

`ACT` is the relationship type.

`m` is an alias for the destination node.

`Movie` destination node is of "type" movie.

`{title:"straight outta compton"}` requires the node's title attribute to equal "straight outta compton".

In this example, we're interested in actor entities which have the relation "act" with **the** entity representing the
"straight outta compton" movie.

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

## All shortest paths

The `allShortestPaths` function returns all the shortest paths between a pair of entities.

`allShortestPaths()` is a MATCH mode in which only the shortest paths matching all criteria are captured. Both the source and the target nodes must be bound in an earlier WITH-demarcated scope to invoke `allShortestPaths()`.

A minimal length (must be 1) and maximal length (must be at least 1) for the search may be specified. Zero or more relationship types may be specified (e.g. [:R|Q*1..3]). No property filters may be introduced in the pattern.

`allShortestPaths()` can have any number of hops for its minimum and maximum, including zero. This number represents how many edges can be traversed in fulfilling the pattern, with a value of 0 entailing that the source node will be included in the returned path.

Filters on properties are supported, and any number of labels may be specified.

Example:

```sh
GRAPH.QUERY DEMO_GRAPH
"MATCH (charlie:Actor {name: 'Charlie Sheen'}), (kevin:Actor {name: 'Kevin Bacon'})
WITH charlie, kevin
MATCH p=allShortestPaths((charlie)-[:PLAYED_WITH*]->(kevin))
RETURN nodes(p) as actors"
```

This query will produce all paths of the minimum length connecting the actor node representing Charlie Sheen to the one representing Kevin Bacon. There are several 2-hop paths between the two actors, and all of these will be returned. The computation of paths then terminates, as we are not interested in any paths of length greater than 2.

## Single-Pair minimal-weight bounded-cost bounded-length paths

The `algo.SPpaths` procedure returns one, _n_, or all minimal-weight, [optionally] bounded-cost, [optionally] bounded-length distinct paths between a pair of entities. Each path is a sequence of distinct nodes connected by distinct edges.

`algo.SPpaths()` is a MATCH mode in which only the paths matching all criteria are captured. Both the source and the target nodes must be bound in an earlier WITH-demarcated scope to invoke `algo.SPpaths()`.

Input arguments:

* A map containing:
  * `sourceNode`: Mandatory. Must be of type node
  * `targetNode`: Mandatory. Must be of type node
  * `relTypes`: Optional. Array of zero or more relationship types. A relationship must have one of these types to be part of the path. If not specified or empty: the path may contain any relationship.
  * `relDirection`: Optional. string. one of `'incoming'`, `'outgoing'`, `'both'`. If not specified: `'outgoing'`.
  * `pathCount`: Optional. Number of minimal-weight paths to retrieve. Non-negative integer. If not specified: 1

    * `0`: retrieve all minimal-weight paths (all reported paths have the same weight)

      Order: 1st : minimal cost, 2nd: minimal length.

    * `1`: retrieve a single minimal-weight path

      When multiple equal-weight paths exist: (preferences: 1st : minimal cost, 2nd: minimal length)

    * _n_ > 1: retrieve up to _n_ minimal-weight paths (reported paths may have different weights)

      When multiple equal-weight paths exist: (preferences: 1st : minimal cost, 2nd: minimal length)

  * `weightProp`: Optional. If not specified: use the default weight: 1 for each relationship.

    The name of the property that represents the weight of each relationship (integer / float)

    If such property doesn’t exist, of if its value is not a positive numeric - use the default weight: 1

    Note: when all weights are equal: minimal-weight ≡ shortest-path.

  * `costProp`: Optional. If not specified: use the default cost: 1 for each relationship.

    The name of the property that represents the cost of each relationship (integer / float)

    If such property doesn't exist, or if its value is not a positive numeric - use the default cost: 1

  * `maxLen`: Optional. Maximal path length (number of relationships along the path). Positive integer. 

    If not specified: no maximal length constraint.

  * `maxCost`: Optional. Positive numeric. If not specified: no maximal cost constraint.

    The maximal cumulative cost for the relationships along the path.

Result:

* Paths conforming to the input arguments. For each reported path:

  * `path` - the path

  * `pathWeight` - the path’s weight

  * `pathCost` - the path’s cost

  To retrieve additional information:

  * The path’s length can be retrieved with `length(path)`

  * An array of the nodes along the path can be retrieved with `nodes(path)`

  * The path’s first node can be retrieved with `nodes(path)[0]`

  * The path’s last node can be retrieved with `nodes(path)[-1]`

  * An array of the relationship's costs along the path can be retrieved with `[r in relationships(path) | r.cost]` where cost is the name of the cost property

  * An array of the relationship's weights along the path can be retrieved with `[r in relationships(path) | r.weight]` where weight is the name of the weight property

Behavior in presence on multiple-edges:

* multi-edges are two or more edges connecting the same pair of vertices (possibly with different weights and costs). 

* All matching edges are considered. Paths with identical vertices and different edges are different paths. The following are 3 different paths ('n1', 'n2', and 'n3' are nodes; 'e1', 'e2', 'e3', and 'e4' are edges): (n1)-[e1]-(n2)-[e2]-(n3),  (n1)-[e1]-(n2)-[e3]-(n3),  (n1)-[e4]-(n2)-[e3]-(n3)

Example:

```sh
GRAPH.QUERY DEMO_GRAPH 
"MATCH (s:Actor {name: 'Charlie Sheen'}), (t:Actor {name: 'Kevin Bacon'}) 
CALL algo.SPpaths( {sourceNode: s, targetNode: t, relTypes: ['r1', 'r2', 'r3'], relDirection: 'outgoing', pathCount: 1, weightProp: 'weight', costProp: 'cost', maxLen: 3, maxCost: 100} ) 
YIELD path, pathCost, pathWeight
RETURN path ORDER BY pathCost"
```

## Single-Source minimal-weight bounded-cost bounded-length paths

The `algo.SSpaths` procedure returns one, _n_, or all minimal-weight, [optionally] bounded-cost, [optionally] bounded-length distinct paths from a given entity. Each path is a sequence of distinct nodes connected by distinct edges.

`algo.SSpaths()` is a MATCH mode in which only the paths matching all criteria are captured. The source node must be bound in an earlier WITH-demarcated scope to invoke `algo.SSpaths()`.

Input arguments:

* A map containing:
  * `sourceNode`: Mandatory. Must be of type node
  * `relTypes`: Optional. Array of zero or more relationship types. A relationship must have one of these types to be part of the path. If not specified or empty: the path may contain any relationship.
  * `relDirection`: Optional. string. one of `'incoming'`, `'outgoing'`, `'both'`. If not specified: `'outgoing'`.
  * `pathCount`: Optional. Number of minimal-weight paths to retrieve. Non-negative integer. If not specified: 1

    This number is global (not per source-target pair); all returned paths may be with the same target.

    * `0`: retrieve all minimal-weight paths (all reported paths have the same weight)

      Order: 1st : minimal cost, 2nd: minimal length.

    * `1`: retrieve a single minimal-weight path

      When multiple equal-weight paths exist: (preferences: 1st : minimal cost, 2nd: minimal length)

    * _n_ > 1: retrieve up to _n_ minimal-weight paths (reported paths may have different weights)

      When multiple equal-weight paths exist: (preferences: 1st : minimal cost, 2nd: minimal length)

  * `weightProp`: Optional. If not specified: use the default weight: 1 for each relationship.

    The name of the property that represents the weight of each relationship (integer / float)

    If such property doesn’t exist, of if its value is not a positive numeric - use the default weight: 1

    Note: when all weights are equal: minimal-weight ≡ shortest-path.

  * `costProp`: Optional. If not specified: use the default cost: 1 for each relationship.

    The name of the property that represents the cost of each relationship (integer / float)

    If such property doesn't exist, or if its value is not a positive numeric - use the default cost: 1

  * `maxLen`: Optional. Maximal path length (number of relationships along the path). Positive integer. 

    If not specified: no maximal length constraint.

  * `maxCost`: Optional. Positive numeric. If not specified: no maximal cost constraint.

    The maximal cumulative cost for the relationships along the path.

Result:

* Paths conforming to the input arguments. For each reported path:
  * `path` - the path
  * `pathWeight` - the path’s weight
  * `pathCost` - the path’s cost

  To retrieve additional information:

  * The path’s length can be retrieved with `length(path)`
  * An array of the nodes along the path can be retrieved with `nodes(path)`
  * The path’s first node can be retrieved with `nodes(path)[0]`
  * The path’s last node can be retrieved with `nodes(path)[-1]`
  * An array of the relationship's costs along the path can be retrieved with `[r in relationships(path) | r.cost]` where cost is the name of the cost property
  * An array of the relationship's weights along the path can be retrieved with `[r in relationships(path) | r.weight]` where weight is the name of the weight property

Behavior in presence on multiple-edges:
---
* multi-edges are two or more edges connecting the same pair of vertices (possibly with different weights and costs). 
* All matching edges are considered. Paths with identical vertices and different edges are different paths. The following are 3 different paths ('n1', 'n2', and 'n3' are nodes; 'e1', 'e2', 'e3', and 'e4' are edges): (n1)-[e1]-(n2)-[e2]-(n3), (n1)-[e1]-(n2)-[e3]-(n3), (n1)-[e4]-(n2)-[e3]-(n3)

Example:

```sh
GRAPH.QUERY DEMO_GRAPH 
"MATCH (s:Actor {name: 'Charlie Sheen'})
CALL algo.SSpaths( {sourceNode: s, relTypes: ['r1', 'r2', 'r3'], relDirection: 'outgoing', pathCount: 1, weightProp: 'weight', costProp: 'cost', maxLen: 3, maxCost: 100} ) 
YIELD path, pathCost, pathWeight
RETURN path ORDER BY pathCost"
```
