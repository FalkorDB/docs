---
title: "Range Index"
description: >
    FalkorDB supports single-property indexes for node labels and for relationship type. String, numeric, and geospatial data types can be indexed.
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Range Index

FalkorDB supports single-property indexes for node labels and for relationship type. String, numeric, and geospatial data types can be indexed.

## Supported Data Types

Range indexes support the following data types:
- **String**: Text values for exact matching and range queries
- **Numeric**: Integer and floating-point numbers for range comparisons
- **Geospatial**: Point data types for location-based queries
- **Arrays**: Single-property arrays containing scalar values (integers, floats, strings)

**Note**: Complex types like nested arrays, maps, or vectors are not supported for range indexing.

## Creating an index for a node label

For a node label, the index creation syntax is:

<Tabs groupId="programming-language">
  <TabItem value="shell" label="Shell">

```bash
GRAPH.QUERY DEMO_GRAPH "CREATE INDEX FOR (p:Person) ON (p.age)"
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
graph.query("CREATE INDEX FOR (p:Person) ON (p.age)")
```

  </TabItem>
  <TabItem value="javascript" label="JavaScript">

```javascript
await graph.query("CREATE INDEX FOR (p:Person) ON (p.age)");
```

  </TabItem>
  <TabItem value="java" label="Java">

```java
graph.query("CREATE INDEX FOR (p:Person) ON (p.age)");
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
graph.query("CREATE INDEX FOR (p:Person) ON (p.age)").execute().await?;
```

  </TabItem>
</Tabs>

An old syntax is also supported:

<Tabs groupId="programming-language">
  <TabItem value="shell" label="Shell">

```bash
GRAPH.QUERY DEMO_GRAPH "CREATE INDEX ON :Person(age)"
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
graph.query("CREATE INDEX ON :Person(age)")
```

  </TabItem>
  <TabItem value="javascript" label="JavaScript">

```javascript
await graph.query("CREATE INDEX ON :Person(age)");
```

  </TabItem>
  <TabItem value="java" label="Java">

```java
graph.query("CREATE INDEX ON :Person(age)");
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
graph.query("CREATE INDEX ON :Person(age)").execute().await?;
```

  </TabItem>
</Tabs>

After an index is explicitly created, it will automatically be used by queries that reference that label and any indexed property in a filter.

<Tabs groupId="programming-language">
  <TabItem value="shell" label="Shell">

```bash
GRAPH.EXPLAIN DEMO_GRAPH "MATCH (p:Person) WHERE p.age > 80 RETURN p"
1) "Results"
2) "    Project"
3) "        Index Scan | (p:Person)"
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
result = graph.explain("MATCH (p:Person) WHERE p.age > 80 RETURN p")
print(result)
# Output:
# Results
#     Project
#         Index Scan | (p:Person)
```

  </TabItem>
  <TabItem value="javascript" label="JavaScript">

```javascript
const result = await graph.explain("MATCH (p:Person) WHERE p.age > 80 RETURN p");
console.log(result);
// Output:
// Results
//     Project
//         Index Scan | (p:Person)
```

  </TabItem>
  <TabItem value="java" label="Java">

```java
String result = graph.explain("MATCH (p:Person) WHERE p.age > 80 RETURN p");
System.out.println(result);
// Output:
// Results
//     Project
//         Index Scan | (p:Person)
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
let result = graph.explain("MATCH (p:Person) WHERE p.age > 80 RETURN p").execute().await?;
println!("{}", result);
// Output:
// Results
//     Project
//         Index Scan | (p:Person)
```

  </TabItem>
</Tabs>

This can significantly improve the runtime of queries with very specific filters. An index on `:employer(name)`, for example, will dramatically benefit the query:

<Tabs groupId="programming-language">
  <TabItem value="shell" label="Shell">

```bash
GRAPH.QUERY DEMO_GRAPH
"MATCH (:Employer {name: 'Dunder Mifflin'})-[:EMPLOYS]->(p:Person) RETURN p"
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
result = graph.query("MATCH (:Employer {name: 'Dunder Mifflin'})-[:EMPLOYS]->(p:Person) RETURN p")
```

  </TabItem>
  <TabItem value="javascript" label="JavaScript">

```javascript
const result = await graph.query("MATCH (:Employer {name: 'Dunder Mifflin'})-[:EMPLOYS]->(p:Person) RETURN p");
```

  </TabItem>
  <TabItem value="java" label="Java">

```java
ResultSet result = graph.query("MATCH (:Employer {name: 'Dunder Mifflin'})-[:EMPLOYS]->(p:Person) RETURN p");
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
let result = graph.query("MATCH (:Employer {name: 'Dunder Mifflin'})-[:EMPLOYS]->(p:Person) RETURN p").execute().await?;
```

  </TabItem>
</Tabs>

An example of utilizing a geospatial index to find `Employer` nodes within 5 kilometers of Scranton are:

<Tabs groupId="programming-language">
  <TabItem value="shell" label="Shell">

```bash
GRAPH.QUERY DEMO_GRAPH
"WITH point({latitude:41.4045886, longitude:-75.6969532}) AS scranton MATCH (e:Employer) WHERE distance(e.location, scranton) < 5000 RETURN e"
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
result = graph.query("WITH point({latitude:41.4045886, longitude:-75.6969532}) AS scranton MATCH (e:Employer) WHERE distance(e.location, scranton) < 5000 RETURN e")
```

  </TabItem>
  <TabItem value="javascript" label="JavaScript">

```javascript
const result = await graph.query("WITH point({latitude:41.4045886, longitude:-75.6969532}) AS scranton MATCH (e:Employer) WHERE distance(e.location, scranton) < 5000 RETURN e");
```

  </TabItem>
  <TabItem value="java" label="Java">

```java
ResultSet result = graph.query("WITH point({latitude:41.4045886, longitude:-75.6969532}) AS scranton MATCH (e:Employer) WHERE distance(e.location, scranton) < 5000 RETURN e");
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
let result = graph.query("WITH point({latitude:41.4045886, longitude:-75.6969532}) AS scranton MATCH (e:Employer) WHERE distance(e.location, scranton) < 5000 RETURN e").execute().await?;
```

  </TabItem>
</Tabs>

Geospatial indexes can currently only be leveraged with `<` and `<=` filters; matching nodes outside the given radius are matched using conventional traversal.

## Creating an index for a relationship type

For a relationship type, the index creation syntax is:

<Tabs groupId="programming-language">
  <TabItem value="shell" label="Shell">

```bash
GRAPH.QUERY DEMO_GRAPH "CREATE INDEX FOR ()-[f:FOLLOW]-() ON (f.created_at)"
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
graph.query("CREATE INDEX FOR ()-[f:FOLLOW]-() ON (f.created_at)")
```

  </TabItem>
  <TabItem value="javascript" label="JavaScript">

```javascript
await graph.query("CREATE INDEX FOR ()-[f:FOLLOW]-() ON (f.created_at)");
```

  </TabItem>
  <TabItem value="java" label="Java">

```java
graph.query("CREATE INDEX FOR ()-[f:FOLLOW]-() ON (f.created_at)");
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
graph.query("CREATE INDEX FOR ()-[f:FOLLOW]-() ON (f.created_at)").execute().await?;
```

  </TabItem>
</Tabs>

Then the execution plan for using the index:

<Tabs groupId="programming-language">
  <TabItem value="shell" label="Shell">

```bash
GRAPH.EXPLAIN DEMO_GRAPH "MATCH (p:Person {id: 0})-[f:FOLLOW]->(fp) WHERE 0 < f.created_at AND f.created_at < 1000 RETURN fp"
1) "Results"
2) "    Project"
3) "        Edge By Index Scan | [f:FOLLOW]"
4) "            Node By Index Scan | (p:Person)"
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
result = graph.explain("MATCH (p:Person {id: 0})-[f:FOLLOW]->(fp) WHERE 0 < f.created_at AND f.created_at < 1000 RETURN fp")
print(result)
# Output:
# Results
#     Project
#         Edge By Index Scan | [f:FOLLOW]
#             Node By Index Scan | (p:Person)
```

  </TabItem>
  <TabItem value="javascript" label="JavaScript">

```javascript
const result = await graph.explain("MATCH (p:Person {id: 0})-[f:FOLLOW]->(fp) WHERE 0 < f.created_at AND f.created_at < 1000 RETURN fp");
console.log(result);
// Output:
// Results
//     Project
//         Edge By Index Scan | [f:FOLLOW]
//             Node By Index Scan | (p:Person)
```

  </TabItem>
  <TabItem value="java" label="Java">

```java
String result = graph.explain("MATCH (p:Person {id: 0})-[f:FOLLOW]->(fp) WHERE 0 < f.created_at AND f.created_at < 1000 RETURN fp");
System.out.println(result);
// Output:
// Results
//     Project
//         Edge By Index Scan | [f:FOLLOW]
//             Node By Index Scan | (p:Person)
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
let result = graph.explain("MATCH (p:Person {id: 0})-[f:FOLLOW]->(fp) WHERE 0 < f.created_at AND f.created_at < 1000 RETURN fp").execute().await?;
println!("{}", result);
// Output:
// Results
//     Project
//         Edge By Index Scan | [f:FOLLOW]
//             Node By Index Scan | (p:Person)
```

  </TabItem>
</Tabs>

This can significantly improve the runtime of queries that traverse super nodes or when we want to start traverse from relationships.

## Deleting an index for a node label

For a node label, the index deletion syntax is:

<Tabs groupId="programming-language">
  <TabItem value="shell" label="Shell">

```bash
GRAPH.QUERY DEMO_GRAPH "DROP INDEX ON :Person(age)"
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
graph.query("DROP INDEX ON :Person(age)")
```

  </TabItem>
  <TabItem value="javascript" label="JavaScript">

```javascript
await graph.query("DROP INDEX ON :Person(age)");
```

  </TabItem>
  <TabItem value="java" label="Java">

```java
graph.query("DROP INDEX ON :Person(age)");
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
graph.query("DROP INDEX ON :Person(age)").execute().await?;
```

  </TabItem>
</Tabs>

## Deleting an index for a relationship type

For a relationship type, the index deletion syntax is:

<Tabs groupId="programming-language">
  <TabItem value="shell" label="Shell">

```bash
GRAPH.QUERY DEMO_GRAPH "DROP INDEX ON :FOLLOW(created_at)"
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
graph.query("DROP INDEX ON :FOLLOW(created_at)")
```

  </TabItem>
  <TabItem value="javascript" label="JavaScript">

```javascript
await graph.query("DROP INDEX ON :FOLLOW(created_at)");
```

  </TabItem>
  <TabItem value="java" label="Java">

```java
graph.query("DROP INDEX ON :FOLLOW(created_at)");
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
graph.query("DROP INDEX ON :FOLLOW(created_at)").execute().await?;
```

  </TabItem>
</Tabs>

## Array Indices

FalkorDB supports indexing on array properties containing scalar values (e.g., integers, floats, strings), enabling efficient lookups for elements within such arrays.

Note: Complex types like nested arrays, maps, or vectors are not supported for indexing.

The following example demonstrates how to index and search an array property:

<Tabs groupId="programming-language">
  <TabItem value="shell" label="Shell">

```bash
# Create a node with an array property
GRAPH.QUERY DEMO_GRAPH "CREATE (:Person {samples: [-21, 30.5, 0, 90, 3.14]})"

# Create an index on the array property
GRAPH.QUERY DEMO_GRAPH "CREATE INDEX FOR (p:Person) ON (p.samples)"

# Use the index to search for nodes containing a specific value in the array
GRAPH.QUERY DEMO_GRAPH "MATCH (p:Person) WHERE 90 IN p.samples RETURN p"
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
# Create a node with an array property
graph.query("CREATE (:Person {samples: [-21, 30.5, 0, 90, 3.14]})")

# Create an index on the array property
graph.query("CREATE INDEX FOR (p:Person) ON (p.samples)")

# Use the index to search for nodes containing a specific value in the array
result = graph.query("MATCH (p:Person) WHERE 90 IN p.samples RETURN p")
```

  </TabItem>
  <TabItem value="javascript" label="JavaScript">

```javascript
// Create a node with an array property
await graph.query("CREATE (:Person {samples: [-21, 30.5, 0, 90, 3.14]})");

// Create an index on the array property
await graph.query("CREATE INDEX FOR (p:Person) ON (p.samples)");

// Use the index to search for nodes containing a specific value in the array
const result = await graph.query("MATCH (p:Person) WHERE 90 IN p.samples RETURN p");
```

  </TabItem>
  <TabItem value="java" label="Java">

```java
// Create a node with an array property
graph.query("CREATE (:Person {samples: [-21, 30.5, 0, 90, 3.14]})");

// Create an index on the array property
graph.query("CREATE INDEX FOR (p:Person) ON (p.samples)");

// Use the index to search for nodes containing a specific value in the array
ResultSet result = graph.query("MATCH (p:Person) WHERE 90 IN p.samples RETURN p");
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
// Create a node with an array property
graph.query("CREATE (:Person {samples: [-21, 30.5, 0, 90, 3.14]})").execute().await?;

// Create an index on the array property
graph.query("CREATE INDEX FOR (p:Person) ON (p.samples)").execute().await?;

// Use the index to search for nodes containing a specific value in the array
let result = graph.query("MATCH (p:Person) WHERE 90 IN p.samples RETURN p").execute().await?;
```

  </TabItem>
</Tabs>

## Verifying Index Usage

To verify that an index is being used by your query, use `GRAPH.EXPLAIN` before and after creating the index:

<Tabs groupId="programming-language">
  <TabItem value="shell" label="Shell">

```bash
# Before creating the index
GRAPH.EXPLAIN DEMO_GRAPH "MATCH (p:Person) WHERE p.age > 30 RETURN p"
# Output shows: Label Scan | (p:Person)

# Create the index
GRAPH.QUERY DEMO_GRAPH "CREATE INDEX FOR (p:Person) ON (p.age)"

# After creating the index
GRAPH.EXPLAIN DEMO_GRAPH "MATCH (p:Person) WHERE p.age > 30 RETURN p"
# Output now shows: Index Scan | (p:Person)
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
# Before creating the index
result = graph.explain("MATCH (p:Person) WHERE p.age > 30 RETURN p")
print(result)  # Shows: Label Scan | (p:Person)

# Create the index
graph.query("CREATE INDEX FOR (p:Person) ON (p.age)")

# After creating the index
result = graph.explain("MATCH (p:Person) WHERE p.age > 30 RETURN p")
print(result)  # Now shows: Index Scan | (p:Person)
```

  </TabItem>
  <TabItem value="javascript" label="JavaScript">

```javascript
// Before creating the index
let result = await graph.explain("MATCH (p:Person) WHERE p.age > 30 RETURN p");
console.log(result);  // Shows: Label Scan | (p:Person)

// Create the index
await graph.query("CREATE INDEX FOR (p:Person) ON (p.age)");

// After creating the index
result = await graph.explain("MATCH (p:Person) WHERE p.age > 30 RETURN p");
console.log(result);  // Now shows: Index Scan | (p:Person)
```

  </TabItem>
  <TabItem value="java" label="Java">

```java
// Before creating the index
String result = graph.explain("MATCH (p:Person) WHERE p.age > 30 RETURN p");
System.out.println(result);  // Shows: Label Scan | (p:Person)

// Create the index
graph.query("CREATE INDEX FOR (p:Person) ON (p.age)");

// After creating the index
result = graph.explain("MATCH (p:Person) WHERE p.age > 30 RETURN p");
System.out.println(result);  // Now shows: Index Scan | (p:Person)
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
// Before creating the index
let result = graph.explain("MATCH (p:Person) WHERE p.age > 30 RETURN p").execute().await?;
println!("{}", result);  // Shows: Label Scan | (p:Person)

// Create the index
graph.query("CREATE INDEX FOR (p:Person) ON (p.age)").execute().await?;

// After creating the index
let result = graph.explain("MATCH (p:Person) WHERE p.age > 30 RETURN p").execute().await?;
println!("{}", result);  // Now shows: Index Scan | (p:Person)
```

  </TabItem>
</Tabs>

## Index Management

### Listing Existing Indexes

To view all indexes in your graph, use the `db.indexes()` procedure:

```cypher
CALL db.indexes()
```

This returns information about all indexes including their type (RANGE), entity type (node/relationship), labels, and properties.

## Performance Tradeoffs and Best Practices

### When to Use Range Indexes

Range indexes are ideal for:
- **Filtering by specific values**: Queries with equality filters (e.g., `WHERE p.name = 'Alice'`)
- **Range queries**: Numeric or string comparisons (e.g., `WHERE p.age > 30`, `WHERE p.name >= 'A' AND p.name < 'B'`)
- **Geospatial queries**: Finding entities within a certain distance
- **Array membership**: Checking if a value exists in an array property

### Performance Considerations

**Benefits:**
- Dramatically improves query performance for filtered searches
- Reduces the number of nodes/relationships that need to be scanned
- Enables efficient range scans and point lookups

**Costs:**
- **Write overhead**: Every insert or update to an indexed property requires updating the index
- **Storage**: Indexes consume additional memory and disk space
- **Maintenance**: Index structures need to be maintained during graph modifications

**Recommendations:**
- Index properties that are frequently used in `WHERE` clauses
- Avoid indexing properties that are rarely queried or have high write frequency
- For properties with very few distinct values (low cardinality), indexes may not provide significant benefits
- Monitor query performance with `GRAPH.PROFILE` to validate index effectiveness

### Example: Profiling Index Performance

```cypher
# Profile query to see actual execution metrics
GRAPH.PROFILE DEMO_GRAPH "MATCH (p:Person) WHERE p.age > 30 RETURN p"
```

This shows detailed timing information and confirms whether the index was used.
