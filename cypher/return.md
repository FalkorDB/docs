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

```sh
RETURN person.name, person.age
```

For convenience, you can specify just the alias to return all properties of an entity:

```sh
RETURN movie.title, actor
```

## Removing Duplicates

Use the `DISTINCT` keyword to remove duplicate values from the result-set:

```sh
RETURN DISTINCT friend_of_friend.name
```

For example, if you have two friends (Joe and Miesha) who both know Dominick, `DISTINCT` ensures that Dominick appears only once in the final result set.


## Aggregations

The `RETURN` clause can also aggregate data, similar to SQL's GROUP BY functionality.

When an aggregation function is used in the RETURN list, all non-aggregated values become implicit grouping keys:

```sh
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
{% include faq_accordion.html title="Frequently Asked Questions" q1="How do I remove duplicate results?" a1="Use `RETURN DISTINCT` followed by the expression or alias to eliminate duplicate rows from the result set." q2="How does GROUP BY work in FalkorDB?" a2="FalkorDB uses **implicit grouping**. When an aggregation function (like `count`, `sum`, `avg`) appears in RETURN, all non-aggregated expressions automatically become grouping keys, similar to SQL GROUP BY." q3="Can I return all properties of a node?" a3="Yes. Simply return the alias without a property accessor, e.g. `RETURN movie`. This returns the full entity including all labels and properties." q4="What aggregation functions are available?" a4="FalkorDB supports `avg`, `collect`, `count`, `max`, `min`, `percentileCont`, `percentileDisc`, `stDev`, and `sum`." %}
