---
title: Data types
description: FalkorDB supports a number of distinct data types, some of which can be persisted as property values and some of which are ephemeral.
sidebar_position: 5
sidebar_label: Data types
---


# Graph types

All graph types are either structural elements of the graph or projections thereof. None can be stored as a property value.

## Nodes

Nodes are persistent graph elements that can be connected to each other via relationships.

They can have any number of labels that describe their general type. For example, a node representing London may be created with the `Place` and `City` labels and retrieved by queries using either or both of them.

Nodes have sets of properties to describe all of their salient characteristics. For example, our London node may have the property set: `{name: 'London', capital: True, elevation: 11}`.

When querying nodes, multiple labels can be specified. Only nodes that hold all specified labels will be matched:

```sh
$ redis-cli GRAPH.QUERY G "MATCH (n:Place:Continent) RETURN n"
```

## Relationships

Relationships are persistent graph elements that connect one node to another.

They must have exactly one type that describes what they represent. For example, a `RESIDENT_OF` relationship may be used to connect a `Person` node to a `City` node.

Relationships are always directed, connecting a source node to its destination.

Like nodes, relationships have sets of properties to describe all of their salient characteristics.

When querying relationships, multiple types can be specified when separated by types. Relationships that hold any of the specified types will be matched:

```sh
$ redis-cli GRAPH.QUERY G "MATCH (:Person)-[r:RESIDENT_OF|:VISITOR_TO]->(:Place {name: 'London'}) RETURN r"
```

## Paths

Paths are alternating sequences of nodes and edges, starting and ending with a node.

They are not structural elements in the graph, but can be created and returned by queries.

For example, the following query returns all paths of any length connecting the node London to the node New York:

```sh
$ redis-cli GRAPH.QUERY G "MATCH p=(:City {name: 'London'})-[*]->(:City {name: 'New York'}) RETURN p"
```

## Scalar types

All scalar types may be provided by queries or stored as property values on node and relationship objects.

### Strings

FalkorDB strings are Unicode character sequences. When using Redis with a TTY (such as invoking FalkorDB commands from the terminal via `redis-cli`), some code points may not be decoded, as in:

```sh
$ redis-cli GRAPH.QUERY G "RETURN '日本人' as stringval"
1) 1) "stringval"
2) 1) 1) "\xe6\x97\xa5\xe6\x9c\xac\xe4\xba\xba"
```

Output decoding can be forced using the `--raw` flag:

```sh
$ redis-cli --raw GRAPH.QUERY G "RETURN '日本人' as stringval"
stringval
日本人
```

### Booleans

Boolean values are specified as `true` or `false`. Internally, they are stored as numerics, with 1 representing true and 0 representing false. As FalkorDB considers types in its comparisons, 1 is not considered equal to `true`:

```sh
$ redis-cli GRAPH.QUERY G "RETURN 1 = true"
1) 1) "1 = true"
2) 1) 1) "false"
```

### Integers

All FalkorDB integers are treated as 64-bit signed integers.

### Floating-point values

All FalkorDB floating-point values are treated as 64-bit signed doubles.

### Geospatial Points

The Point data type is a set of latitude/longitude coordinates, stored within FalkorDB as a pair of 32-bit floats. It is instantiated using the `point()` function (see [Cypher functions](/cypher/functions)).

### Nulls

In FalkorDB, `null` is used to stand in for an unknown or missing value.

Since we cannot reason broadly about unknown values, `null` is an important part of FalkorDB's 3-valued truth table. For example, the comparison `null = null` will evaluate to `null`, as we lack adequate information about the compared values. Similarly, `null in [1,2,3]` evaluates to `null`, since the value we're looking up is unknown.

Unlike all other scalars, `null` cannot be stored as a property value.

## Temporal Types

FalkorDB supports the following temporal types that allow modeling and querying time-related data:

1. [Date](#date) - Calendar dates (YYYY-MM-DD)
2. [Time](#time) - Time of day (HH:MM:SS)
3. [DateTime](#datetime) - Combined date and time
4. [Duration](#duration) - Time intervals

These types follow the ISO 8601 standard and can be used in properties, parameters, and expressions.

### Date

Represents a calendar date in the format YYYY-MM-DD.

**Purpose:**  
Use `Date` to store and compare dates without time information, such as birth dates, due dates, or deadlines.

**Example:**

```cypher
CREATE (:Event { name: "Conference", date: date("2025-09-15") })
```

**Interactions:**
* Compare using operators (`=`, `<`, `>`, etc.)
* Extract components using functions:

```cypher
RETURN date("2025-09-15").year      // 2025
RETURN date("2025-09-15").month     // 9
RETURN date("2025-09-15").day       // 15
```

### Time

Represents a time of day in the format HH:MM:SS.

**Purpose:**  
Use `Time` to store specific times (e.g., store hours, alarm times) without date context.

**Example:**

```cypher
CREATE (:Reminder { msg: "Wake up!", at: localtime("07:00:00") })
```

**Interactions:**

* Compare time values:

```cypher
RETURN localtime("07:00:00") < localtime("09:30:00")  // true
```

* Extract parts:

```cypher
RETURN localtime("15:45:20").hour      // 15
RETURN localtime("15:45:20").minute    // 45
RETURN localtime("15:45:20").second    // 20
```

### DateTime

Represents a point in time, combining both date and time. Format: YYYY-MM-DDTHH:MM:SS.

**Purpose:**  
Use `DateTime` when both date and time are relevant, such as logging events, scheduling, or timestamps.

**Example:**
```cypher
CREATE (:Log { message: "System rebooted", at: localdatetime("2025-06-29T13:45:00") })
```

**Interactions:**

* Compare with other `DateTime` values
* Extract parts:

```cypher
RETURN localdatetime("2025-06-29T13:45:00").year     // 2025
RETURN localdatetime("2025-06-29T13:45:00").hour     // 13
```

* Use `localdatetime()` with no arguments to get the current system time:

```cypher
RETURN localdatetime()
```

### Duration

Represents a span of time in ISO 8601 Duration format: `P[n]Y[n]M[n]DT[n]H[n]M[n]S`

**Purpose:**  
Use `Duration` to represent time intervals, such as "3 days", "2 hours", or "1 year and 6 months".

**Example:**
```cypher
CREATE (:Cooldown { period: duration("P3DT12H") })
```

**Interactions:**

* Add/subtract durations with dates or datetimes:

```cypher
RETURN date("2025-01-01") + duration("P1M")  // 2025-02-01
RETURN datetime("2025-06-29T13:00:00") - duration("PT30M") // 2025-06-29T12:30:00
```

* Add durations together:

```cypher
RETURN duration("P1D") + duration("PT12H")   // P1DT12H
```

* Extract fields:

```cypher
RETURN duration("P1Y2M3DT4H5M6S").years      // 1
RETURN duration("P1Y2M3DT4H5M6S").hours      // 4
```

## Collection types

### Arrays

Arrays are ordered lists of elements. They can be provided as literals or generated by functions like `collect()`. Nested arrays are supported, as are many functions that operate on arrays such as [list comprehensions](/commands/graph.query#list-comprehensions).

Arrays can be stored as property values provided that no array element is of an unserializable type, such as graph entities or `null` values.

### Maps

Maps are order-agnostic collections of key-value pairs. If a key is a string literal, the map can be accessed using dot notation. If it is instead an expression that evaluates to a string literal, bracket notation can be used:

```sh
$ redis-cli GRAPH.QUERY G "WITH {key1: 'stringval', key2: 10} AS map RETURN map.key1, map['key' + 2]"
1) 1) "map.key1"
   2) "map['key' + 2]"
2) 1) 1) "stringval"
      2) (integer) 10
```

This aligns with the way that the properties of nodes and relationships can be accessed.

Maps cannot be stored as property values.

#### Map projections

Maps can be constructed as projections using the syntax `alias {.key1 [, ...n]}`. This can provide a useful format for returning graph entities. For example, given a graph with the node `(name: 'Jeff', age: 32)`, we can build the projection:

```sh
$ redis-cli GRAPH.QUERY G "MATCH (n) RETURN n {.name, .age} AS projection"
1) 1) "projection"
2) 1) 1) "{name: Jeff, age: 32}"
```

#### Map merging

You can combine two maps, where values in the second map will override corresponding values in the first map.
For example:

```sh
$ redis-cli GRAPH.QUERY g "RETURN {a: 1, b: 2} + {a: 2, c: 3}"
1) 1) "{a: 1, b: 2} + {a: 2, c: 3}"
2) 1) 1) "{b: 2, a: 2, c: 3}"
3) 1) "Cached execution: 0"
   2) "Query internal execution time: 0.467666 milliseconds"
```

#### Function calls in map values

The values in maps and map projections are flexible, and can generally refer either to constants or computed values:

```sh
$ redis-cli GRAPH.QUERY G "RETURN {key1: 'constant', key2: rand(), key3: toLower('GENERATED') + '_string'} AS map"
1) 1) "map"
2) 1) 1) "{key1: constant, key2: 0.889656, key3: generated_string}"
```

The exception to this is aggregation functions, which must be computed in a preceding `WITH` clause instead of being invoked within the map. This restriction is intentional, as it helps to clearly disambiguate the aggregate function calls and the key values they are grouped by:

```sh
$ redis-cli GRAPH.QUERY G "
MATCH (follower:User)-[:FOLLOWS]->(u:User)
WITH u, COUNT(follower) AS count
RETURN u {.name, follower_count: count} AS user"
1) 1) "user"
2) 1) 1) "{name: Jeff, follower_count: 12}"
   2) 1) "{name: Roi, follower_count: 18}"
```
