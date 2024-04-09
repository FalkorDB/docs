---
title: "WHERE"
nav_order: 3
description: >
    FalkorDB implements a subset of the Cypher language, which is growing as development continues.
parent: "Cypher Language"
---

# WHERE

This clause is not mandatory, but if you want to filter results, you can specify your predicates here.

Supported operations:

* `=`
* `<>`
* `<`
* `<=`
* `>`
* `>=`
* `CONTAINS`
* `ENDS WITH`
* `IN`
* `STARTS WITH`

Predicates can be combined using AND / OR / NOT.

Be sure to wrap predicates within parentheses to control precedence.

Examples:

```sql
WHERE (actor.name = "john doe" OR movie.rating > 8.8) AND movie.votes <= 250)
```

```sql
WHERE actor.age >= director.age AND actor.age > 32
```

It is also possible to specify equality predicates within nodes using the curly braces as such:

```sql
(:President {name:"Jed Bartlett"})-[:WON]->(:State)
```

Here we've required that the president node's name will have the value "Jed Bartlett".

There's no difference between inline predicates and predicates specified within the WHERE clause.

It is also possible to filter on graph patterns. The following queries, which return all presidents and the states they won in, produce the same results:

```sh
MATCH (p:President), (s:State) WHERE (p)-[:WON]->(s) RETURN p, s
```

and

```sh
MATCH (p:President)-[:WON]->(s:State) RETURN p, s
```

Pattern predicates can be also negated and combined with the logical operators AND, OR, and NOT. The following query returns all the presidents that did not win in the states where they were governors:

```sh
MATCH (p:President), (s:State) WHERE NOT (p)-[:WON]->(s) AND (p)->[:governor]->(s) RETURN p, s
```

Nodes can also be filtered by label:

```sh
MATCH (n)-[:R]->() WHERE n:L1 OR n:L2 RETURN n 
```

When possible, it is preferable to specify the label in the node pattern of the MATCH clause.
