title: "RETURN clause"
nav_order: 4
description: >
    FalkorDB implements a subset of the Cypher language, which is growing as development continues.
parent: "Cypher Language"
---

# RETURN

In its simple form, Return defines which properties the returned result-set will contain.

Its structure is a list of `alias.property` separated by commas.

For convenience, it's possible to specify the alias only when you're interested in every attribute an entity possesses,
and don't want to specify each attribute individually. For example:

```sh
RETURN movie.title, actor
```

Use the DISTINCT keyword to remove duplications within the result-set:

```sh
RETURN DISTINCT friend_of_friend.name
```

In the above example, suppose we have two friends, Joe and Miesha,
and both know Dominick.

DISTINCT will make sure Dominick will only appear once
in the final result set.


Return can also be used to aggregate data, similar to group by in SQL.

Once an aggregation function is added to the return
list, all other "none" aggregated values are considered as group keys, for example:

```sh
RETURN movie.title, MAX(actor.age), MIN(actor.age)
```

Here we group data by movie title and for each movie, and we find its youngest and oldest actor age.

## Aggregations

Supported aggregation functions include:

* `avg`
* `collect`
* `count`
* `max`
* `min`
* `percentileCont`
* `percentileDisc`
* `stDev`
* `sum`