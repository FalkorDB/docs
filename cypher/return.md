---
title: "RETURN"
nav_order: 4
description: >
    Define result-set properties with the RETURN clause in Cypher queries. Support for DISTINCT, aggregations (COUNT, SUM, AVG), and implicit GROUP BY functionality.
parent: "Cypher Language"
---

# RETURN

The `RETURN` clause defines which properties and values the result-set will contain.

## Basic Usage

The basic structure is a comma-separated list of `alias.property` expressions:

```cypher
RETURN person.name, person.age
```

For convenience, you can specify just the alias to return all properties of an entity:

```cypher
RETURN movie.title, actor
```

## Removing Duplicates

Use the `DISTINCT` keyword to remove duplicate values from the result-set:

```cypher
RETURN DISTINCT friend_of_friend.name
```

For example, if you have two friends (Joe and Miesha) who both know Dominick, `DISTINCT` ensures that Dominick appears only once in the final result set.


## Aggregations

The `RETURN` clause can also aggregate data, similar to SQL's GROUP BY functionality.

When an aggregation function is used in the RETURN list, all non-aggregated values become implicit grouping keys:

```cypher
RETURN movie.title, MAX(actor.age), MIN(actor.age)
```

This query groups data by movie title and, for each movie, returns the youngest and oldest actor ages.

### Supported Aggregation Functions

| Function | Description |
|----------|-------------|
| `avg` | Calculate average of numeric values |
| `collect` | Collect values into a list |
| `count` | Count number of values |
| `max` | Find maximum value |
| `min` | Find minimum value |
| `percentileCont` | Calculate continuous percentile |
| `percentileDisc` | Calculate discrete percentile |
| `stDev` | Calculate standard deviation |
| `sum` | Calculate sum of numeric values |

For detailed information on aggregation functions, see the [Functions documentation](/cypher/functions#aggregating-functions).