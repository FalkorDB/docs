---
title: "Indexing"
nav_order: 21
description: >
    FalkorDB supports single-property indexes for node labels and for relationship type. String, numeric, and geospatial data types can be indexed.
parent: "Cypher Language"
---

# Indexing

## Range Index

FalkorDB supports single-property indexes for node labels and for relationship type. String, numeric, and geospatial data types can be indexed.

### Creating an index for a node label

For a node label, the index creation syntax is:

{% capture shell_0 %}
GRAPH.QUERY DEMO_GRAPH "CREATE INDEX FOR (p:Person) ON (p.age)"
{% endcapture %}

{% capture python_0 %}
graph.query("CREATE INDEX FOR (p:Person) ON (p.age)")
{% endcapture %}

{% capture javascript_0 %}
await graph.query("CREATE INDEX FOR (p:Person) ON (p.age)");
{% endcapture %}

{% capture java_0 %}
graph.query("CREATE INDEX FOR (p:Person) ON (p.age)");
{% endcapture %}

{% capture rust_0 %}
graph.query("CREATE INDEX FOR (p:Person) ON (p.age)").execute().await?;
{% endcapture %}

{% include code_tabs.html id="create_index_tabs" shell=shell_0 python=python_0 javascript=javascript_0 java=java_0 rust=rust_0 %}

An old syntax is also supported:

{% capture shell_1 %}
GRAPH.QUERY DEMO_GRAPH "CREATE INDEX ON :Person(age)"
{% endcapture %}

{% capture python_1 %}
graph.query("CREATE INDEX ON :Person(age)")
{% endcapture %}

{% capture javascript_1 %}
await graph.query("CREATE INDEX ON :Person(age)");
{% endcapture %}

{% capture java_1 %}
graph.query("CREATE INDEX ON :Person(age)");
{% endcapture %}

{% capture rust_1 %}
graph.query("CREATE INDEX ON :Person(age)").execute().await?;
{% endcapture %}

{% include code_tabs.html id="old_syntax_tabs" shell=shell_1 python=python_1 javascript=javascript_1 java=java_1 rust=rust_1 %}

After an index is explicitly created, it will automatically be used by queries that reference that label and any indexed property in a filter.

{% capture shell_2 %}
GRAPH.EXPLAIN DEMO_GRAPH "MATCH (p:Person) WHERE p.age > 80 RETURN p"
1) "Results"
2) "    Project"
3) "        Index Scan | (p:Person)"
{% endcapture %}

{% capture python_2 %}
result = graph.explain("MATCH (p:Person) WHERE p.age > 80 RETURN p")
print(result)
# Output:
# Results
#     Project
#         Index Scan | (p:Person)
{% endcapture %}

{% capture javascript_2 %}
const result = await graph.explain("MATCH (p:Person) WHERE p.age > 80 RETURN p");
console.log(result);
// Output:
// Results
//     Project
//         Index Scan | (p:Person)
{% endcapture %}

{% capture java_2 %}
String result = graph.explain("MATCH (p:Person) WHERE p.age > 80 RETURN p");
System.out.println(result);
// Output:
// Results
//     Project
//         Index Scan | (p:Person)
{% endcapture %}

{% capture rust_2 %}
let result = graph.explain("MATCH (p:Person) WHERE p.age > 80 RETURN p").execute().await?;
println!("{}", result);
// Output:
// Results
//     Project
//         Index Scan | (p:Person)
{% endcapture %}

{% include code_tabs.html id="explain_tabs" shell=shell_2 python=python_2 javascript=javascript_2 java=java_2 rust=rust_2 %}

This can significantly improve the runtime of queries with very specific filters. An index on `:employer(name)`, for example, will dramatically benefit the query:

{% capture shell_3 %}
GRAPH.QUERY DEMO_GRAPH
"MATCH (:Employer {name: 'Dunder Mifflin'})-[:EMPLOYS]->(p:Person) RETURN p"
{% endcapture %}

{% capture python_3 %}
result = graph.query("MATCH (:Employer {name: 'Dunder Mifflin'})-[:EMPLOYS]->(p:Person) RETURN p")
{% endcapture %}

{% capture javascript_3 %}
const result = await graph.query("MATCH (:Employer {name: 'Dunder Mifflin'})-[:EMPLOYS]->(p:Person) RETURN p");
{% endcapture %}

{% capture java_3 %}
ResultSet result = graph.query("MATCH (:Employer {name: 'Dunder Mifflin'})-[:EMPLOYS]->(p:Person) RETURN p");
{% endcapture %}

{% capture rust_3 %}
let result = graph.query("MATCH (:Employer {name: 'Dunder Mifflin'})-[:EMPLOYS]->(p:Person) RETURN p").execute().await?;
{% endcapture %}

{% include code_tabs.html id="employer_query_tabs" shell=shell_3 python=python_3 javascript=javascript_3 java=java_3 rust=rust_3 %}

An example of utilizing a geospatial index to find `Employer` nodes within 5 kilometers of Scranton are:

{% capture shell_4 %}
GRAPH.QUERY DEMO_GRAPH
"WITH point({latitude:41.4045886, longitude:-75.6969532}) AS scranton MATCH (e:Employer) WHERE distance(e.location, scranton) < 5000 RETURN e"
{% endcapture %}

{% capture python_4 %}
result = graph.query("WITH point({latitude:41.4045886, longitude:-75.6969532}) AS scranton MATCH (e:Employer) WHERE distance(e.location, scranton) < 5000 RETURN e")
{% endcapture %}

{% capture javascript_4 %}
const result = await graph.query("WITH point({latitude:41.4045886, longitude:-75.6969532}) AS scranton MATCH (e:Employer) WHERE distance(e.location, scranton) < 5000 RETURN e");
{% endcapture %}

{% capture java_4 %}
ResultSet result = graph.query("WITH point({latitude:41.4045886, longitude:-75.6969532}) AS scranton MATCH (e:Employer) WHERE distance(e.location, scranton) < 5000 RETURN e");
{% endcapture %}

{% capture rust_4 %}
let result = graph.query("WITH point({latitude:41.4045886, longitude:-75.6969532}) AS scranton MATCH (e:Employer) WHERE distance(e.location, scranton) < 5000 RETURN e").execute().await?;
{% endcapture %}

{% include code_tabs.html id="geospatial_tabs" shell=shell_4 python=python_4 javascript=javascript_4 java=java_4 rust=rust_4 %}

Geospatial indexes can currently only be leveraged with `<` and `<=` filters; matching nodes outside of the given radius is performed using conventional matching.

### Creating an index for a relationship type

For a relationship type, the index creation syntax is:

{% capture shell_5 %}
GRAPH.QUERY DEMO_GRAPH "CREATE INDEX FOR ()-[f:FOLLOW]-() ON (f.created_at)"
{% endcapture %}

{% capture python_5 %}
graph.query("CREATE INDEX FOR ()-[f:FOLLOW]-() ON (f.created_at)")
{% endcapture %}

{% capture javascript_5 %}
await graph.query("CREATE INDEX FOR ()-[f:FOLLOW]-() ON (f.created_at)");
{% endcapture %}

{% capture java_5 %}
graph.query("CREATE INDEX FOR ()-[f:FOLLOW]-() ON (f.created_at)");
{% endcapture %}

{% capture rust_5 %}
graph.query("CREATE INDEX FOR ()-[f:FOLLOW]-() ON (f.created_at)").execute().await?;
{% endcapture %}

{% include code_tabs.html id="relationship_index_tabs" shell=shell_5 python=python_5 javascript=javascript_5 java=java_5 rust=rust_5 %}

Then the execution plan for using the index:

{% capture shell_6 %}
GRAPH.EXPLAIN DEMO_GRAPH "MATCH (p:Person {id: 0})-[f:FOLLOW]->(fp) WHERE 0 < f.created_at AND f.created_at < 1000 RETURN fp"
1) "Results"
2) "    Project"
3) "        Edge By Index Scan | [f:FOLLOW]"
4) "            Node By Index Scan | (p:Person)"
{% endcapture %}

{% capture python_6 %}
result = graph.explain("MATCH (p:Person {id: 0})-[f:FOLLOW]->(fp) WHERE 0 < f.created_at AND f.created_at < 1000 RETURN fp")
print(result)
### Output:
### Results
####     Project
#####         Edge By Index Scan | [f:FOLLOW]
#####             Node By Index Scan | (p:Person)
{% endcapture %}

{% capture javascript_6 %}
const result = await graph.explain("MATCH (p:Person {id: 0})-[f:FOLLOW]->(fp) WHERE 0 < f.created_at AND f.created_at < 1000 RETURN fp");
console.log(result);
// Output:
// Results
//     Project
//         Edge By Index Scan | [f:FOLLOW]
//             Node By Index Scan | (p:Person)
{% endcapture %}

{% capture java_6 %}
String result = graph.explain("MATCH (p:Person {id: 0})-[f:FOLLOW]->(fp) WHERE 0 < f.created_at AND f.created_at < 1000 RETURN fp");
System.out.println(result);
// Output:
// Results
//     Project
//         Edge By Index Scan | [f:FOLLOW]
//             Node By Index Scan | (p:Person)
{% endcapture %}

{% capture rust_6 %}
let result = graph.explain("MATCH (p:Person {id: 0})-[f:FOLLOW]->(fp) WHERE 0 < f.created_at AND f.created_at < 1000 RETURN fp").execute().await?;
println!("{}", result);
// Output:
// Results
//     Project
//         Edge By Index Scan | [f:FOLLOW]
//             Node By Index Scan | (p:Person)
{% endcapture %}

{% include code_tabs.html id="relationship_explain_tabs" shell=shell_6 python=python_6 javascript=javascript_6 java=java_6 rust=rust_6 %}

This can significantly improve the runtime of queries that traverse super nodes or when we want to start traverse from relationships.

### Deleting an index for a node label

For a node label, the index deletion syntax is:

{% capture shell_7 %}
GRAPH.QUERY DEMO_GRAPH "DROP INDEX ON :Person(age)"
{% endcapture %}

{% capture python_7 %}
graph.query("DROP INDEX ON :Person(age)")
{% endcapture %}

{% capture javascript_7 %}
await graph.query("DROP INDEX ON :Person(age)");
{% endcapture %}

{% capture java_7 %}
graph.query("DROP INDEX ON :Person(age)");
{% endcapture %}

{% capture rust_7 %}
graph.query("DROP INDEX ON :Person(age)").execute().await?;
{% endcapture %}

{% include code_tabs.html id="drop_node_index_tabs" shell=shell_7 python=python_7 javascript=javascript_7 java=java_7 rust=rust_7 %}

### Deleting an index for a relationship type

For a relationship type, the index deletion syntax is:

{% capture shell_8 %}
GRAPH.QUERY DEMO_GRAPH "DROP INDEX ON :FOLLOW(created_at)"
{% endcapture %}

{% capture python_8 %}
graph.query("DROP INDEX ON :FOLLOW(created_at)")
{% endcapture %}

{% capture javascript_8 %}
await graph.query("DROP INDEX ON :FOLLOW(created_at)");
{% endcapture %}

{% capture java_8 %}
graph.query("DROP INDEX ON :FOLLOW(created_at)");
{% endcapture %}

{% capture rust_8 %}
graph.query("DROP INDEX ON :FOLLOW(created_at)").execute().await?;
{% endcapture %}

{% include code_tabs.html id="drop_relationship_index_tabs" shell=shell_8 python=python_8 javascript=javascript_8 java=java_8 rust=rust_8 %}

### Array Indices

FalkorDB supports indexing on array properties containing scalar values (e.g., integers, floats, strings), enabling efficient lookups for elements within such arrays.

Note: Complex types like nested arrays, maps, or vectors are not supported for indexing.

The following example demonstrates how to index and search an array property:

{% capture shell_9 %}
# Create a node with an array property
GRAPH.QUERY DEMO_GRAPH "CREATE (:Person {samples: [-21, 30.5, 0, 90, 3.14]})"

## Create an index on the array property
GRAPH.QUERY DEMO_GRAPH "CREATE INDEX FOR (p:Person) ON (p.samples)"

## Use the index to search for nodes containing a specific value in the array
GRAPH.QUERY DEMO_GRAPH "MATCH (p:Person) WHERE 90 IN p.samples RETURN p"
{% endcapture %}

{% capture python_9 %}
## Create a node with an array property
graph.query("CREATE (:Person {samples: [-21, 30.5, 0, 90, 3.14]})")

## Create an index on the array property
graph.query("CREATE INDEX FOR (p:Person) ON (p.samples)")

## Use the index to search for nodes containing a specific value in the array
result = graph.query("MATCH (p:Person) WHERE 90 IN p.samples RETURN p")
{% endcapture %}

{% capture javascript_9 %}
// Create a node with an array property
await graph.query("CREATE (:Person {samples: [-21, 30.5, 0, 90, 3.14]})");

// Create an index on the array property
await graph.query("CREATE INDEX FOR (p:Person) ON (p.samples)");

// Use the index to search for nodes containing a specific value in the array
const result = await graph.query("MATCH (p:Person) WHERE 90 IN p.samples RETURN p");
{% endcapture %}

{% capture java_9 %}
// Create a node with an array property
graph.query("CREATE (:Person {samples: [-21, 30.5, 0, 90, 3.14]})");

// Create an index on the array property
graph.query("CREATE INDEX FOR (p:Person) ON (p.samples)");

// Use the index to search for nodes containing a specific value in the array
ResultSet result = graph.query("MATCH (p:Person) WHERE 90 IN p.samples RETURN p");
{% endcapture %}

{% capture rust_9 %}
// Create a node with an array property
graph.query("CREATE (:Person {samples: [-21, 30.5, 0, 90, 3.14]})").execute().await?;

// Create an index on the array property
graph.query("CREATE INDEX FOR (p:Person) ON (p.samples)").execute().await?;

// Use the index to search for nodes containing a specific value in the array
let result = graph.query("MATCH (p:Person) WHERE 90 IN p.samples RETURN p").execute().await?;
{% endcapture %}

{% include code_tabs.html id="array_index_tabs" shell=shell_9 python=python_9 javascript=javascript_9 java=java_9 rust=rust_9 %}

## Full-text indexing

FalkorDB leverages the indexing capabilities of [RediSearch](https://redis.io/docs/interact/search-and-query/) to provide full-text indices through procedure calls.

## Creating a full-text index for a node label

To construct a full-text index on the `title` property of all nodes with label `Movie`, use the syntax:

{% capture shell_10 %}
GRAPH.QUERY DEMO_GRAPH "CALL db.idx.fulltext.createNodeIndex('Movie', 'title')"
{% endcapture %}

{% capture python_10 %}
graph.query("CALL db.idx.fulltext.createNodeIndex('Movie', 'title')")
{% endcapture %}

{% capture javascript_10 %}
await graph.query("CALL db.idx.fulltext.createNodeIndex('Movie', 'title')");
{% endcapture %}

{% capture java_10 %}
graph.query("CALL db.idx.fulltext.createNodeIndex('Movie', 'title')");
{% endcapture %}

{% capture rust_10 %}
graph.query("CALL db.idx.fulltext.createNodeIndex('Movie', 'title')").execute().await?;
{% endcapture %}

{% include code_tabs.html id="fulltext_create_tabs" shell=shell_10 python=python_10 javascript=javascript_10 java=java_10 rust=rust_10 %}

More properties can be added to this index by adding their names to the above set of arguments, or using this syntax again with the additional names.

{% capture shell_11 %}
GRAPH.QUERY DEMO_GRAPH "CALL db.idx.fulltext.createNodeIndex('Person', 'firstName', 'lastName')"
{% endcapture %}

{% capture python_11 %}
graph.query("CALL db.idx.fulltext.createNodeIndex('Person', 'firstName', 'lastName')")
{% endcapture %}

{% capture javascript_11 %}
await graph.query("CALL db.idx.fulltext.createNodeIndex('Person', 'firstName', 'lastName')");
{% endcapture %}

{% capture java_11 %}
graph.query("CALL db.idx.fulltext.createNodeIndex('Person', 'firstName', 'lastName')");
{% endcapture %}

{% capture rust_11 %}
graph.query("CALL db.idx.fulltext.createNodeIndex('Person', 'firstName', 'lastName')").execute().await?;
{% endcapture %}

{% include code_tabs.html id="fulltext_multi_property_tabs" shell=shell_11 python=python_11 javascript=javascript_11 java=java_11 rust=rust_11 %}

RediSearch provide 2 index configuration options:

1. Language - Define which language to use for stemming text, which is adding the base form of a word to the index. This allows the query for "going" to also return results for "go" and "gone", for example.
2. Stopwords - These are words that are usually so common that they do not add much information to search, but take up a lot of space and CPU time in the index.

To construct a full-text index on the `title` property using `German` language and using custom stopwords of all nodes with label `Movie`, use the syntax:

{% capture shell_12 %}
GRAPH.QUERY DEMO_GRAPH "CALL db.idx.fulltext.createNodeIndex({ label: 'Movie', language: 'German', stopwords: ['a', 'ab'] }, 'title')"
{% endcapture %}

{% capture python_12 %}
graph.query("CALL db.idx.fulltext.createNodeIndex({ label: 'Movie', language: 'German', stopwords: ['a', 'ab'] }, 'title')")
{% endcapture %}

{% capture javascript_12 %}
await graph.query("CALL db.idx.fulltext.createNodeIndex({ label: 'Movie', language: 'German', stopwords: ['a', 'ab'] }, 'title')");
{% endcapture %}

{% capture java_12 %}
graph.query("CALL db.idx.fulltext.createNodeIndex({ label: 'Movie', language: 'German', stopwords: ['a', 'ab'] }, 'title')");
{% endcapture %}

{% capture rust_12 %}
graph.query("CALL db.idx.fulltext.createNodeIndex({ label: 'Movie', language: 'German', stopwords: ['a', 'ab'] }, 'title')").execute().await?;
{% endcapture %}

{% include code_tabs.html id="fulltext_config_tabs" shell=shell_12 python=python_12 javascript=javascript_12 java=java_12 rust=rust_12 %}

RediSearch provide 3 additional field configuration options:

1. Weight - The importance of the text in the field
2. Nostem - Skip stemming when indexing text
3. Phonetic - Enable phonetic search on the text

To construct a full-text index on the `title` property with phonetic search of all nodes with label `Movie`, use the syntax:

{% capture shell_13 %}
GRAPH.QUERY DEMO_GRAPH "CALL db.idx.fulltext.createNodeIndex('Movie', {field: 'title', phonetic: 'dm:en'})"
{% endcapture %}

{% capture python_13 %}
graph.query("CALL db.idx.fulltext.createNodeIndex('Movie', {field: 'title', phonetic: 'dm:en'})")
{% endcapture %}

{% capture javascript_13 %}
await graph.query("CALL db.idx.fulltext.createNodeIndex('Movie', {field: 'title', phonetic: 'dm:en'})");
{% endcapture %}

{% capture java_13 %}
graph.query("CALL db.idx.fulltext.createNodeIndex('Movie', {field: 'title', phonetic: 'dm:en'})");
{% endcapture %}

{% capture rust_13 %}
graph.query("CALL db.idx.fulltext.createNodeIndex('Movie', {field: 'title', phonetic: 'dm:en'})").execute().await?;
{% endcapture %}

{% include code_tabs.html id="fulltext_phonetic_tabs" shell=shell_13 python=python_13 javascript=javascript_13 java=java_13 rust=rust_13 %}

## Utilizing a full-text index for a node label

An index can be invoked to match any whole words contained within:

{% capture shell_14 %}
GRAPH.QUERY DEMO_GRAPH
"CALL db.idx.fulltext.queryNodes('Movie', 'Book') YIELD node RETURN node.title"
1) 1) "node.title"
2) 1) 1) "The Jungle Book"
   2) 1) "The Book of Life"
3) 1) "Query internal execution time: 0.927409 milliseconds"
{% endcapture %}

{% capture python_14 %}
result = graph.query("CALL db.idx.fulltext.queryNodes('Movie', 'Book') YIELD node RETURN node.title")
for record in result:
    print(record["node.title"])
# Output:
# The Jungle Book
# The Book of Life
{% endcapture %}

{% capture javascript_14 %}
const result = await graph.query("CALL db.idx.fulltext.queryNodes('Movie', 'Book') YIELD node RETURN node.title");
for (const record of result.data) {
    console.log(record["node.title"]);
}
// Output:
// The Jungle Book
// The Book of Life
{% endcapture %}

{% capture java_14 %}
ResultSet result = graph.query("CALL db.idx.fulltext.queryNodes('Movie', 'Book') YIELD node RETURN node.title");
for (Record record : result) {
    System.out.println(record.get("node.title"));
}
// Output:
// The Jungle Book
// The Book of Life
{% endcapture %}

{% capture rust_14 %}
let result = graph.query("CALL db.idx.fulltext.queryNodes('Movie', 'Book') YIELD node RETURN node.title").execute().await?;
for record in result.data() {
    println!("{}", record["node.title"]);
}
// Output:
// The Jungle Book
// The Book of Life
{% endcapture %}

{% include code_tabs.html id="fulltext_query_tabs" shell=shell_14 python=python_14 javascript=javascript_14 java=java_14 rust=rust_14 %}

This CALL clause can be interleaved with other Cypher clauses to perform more elaborate manipulations:

```sh
GRAPH.QUERY DEMO_GRAPH
"CALL db.idx.fulltext.queryNodes('Movie', 'Book') YIELD node AS m
WHERE m.genre = 'Adventure'
RETURN m ORDER BY m.rating"
1) 1) "m"
2) 1) 1) 1) 1) "id"
            2) (integer) 1168
         2) 1) "labels"
            2) 1) "Movie"
         3) 1) "properties"
            2) 1) 1) "genre"
                  2) "Adventure"
               2) 1) "rating"
                  2) "7.6"
               3) 1) "votes"
                  2) (integer) 151342
               4) 1) "year"
                  2) (integer) 2016
               5) 1) "title"
                  2) "The Jungle Book"
3) 1) "Query internal execution time: 0.226914 milliseconds"
```

In addition to yielding matching nodes, full-text index scans will return the score of each node. This is the [TF-IDF](https://redis.io/docs/interact/search-and-query/advanced-concepts/scoring/#tfidf-default) score of the node, which is informed by how many times the search terms appear in the node and how closely grouped they are. This can be observed in the example:

```sh
GRAPH.QUERY DEMO_GRAPH
"CALL db.idx.fulltext.queryNodes('Node', 'hello world') YIELD node, score RETURN score, node.val"
1) 1) "score"
   2) "node.val"
2) 1) 1) "2"
      2) "hello world"
   2) 1) "1"
      2) "hello to a different world"
3) 1) "Cached execution: 1"
   2) "Query internal execution time: 0.335401 milliseconds"
```

## Deleting a full-text index for a node label

For a node label, the full-text index deletion syntax is:

{% capture shell_15 %}
GRAPH.QUERY DEMO_GRAPH "CALL db.idx.fulltext.drop('Movie')"
{% endcapture %}

{% capture python_15 %}
graph.query("CALL db.idx.fulltext.drop('Movie')")
{% endcapture %}

{% capture javascript_15 %}
await graph.query("CALL db.idx.fulltext.drop('Movie')");
{% endcapture %}

{% capture java_15 %}
graph.query("CALL db.idx.fulltext.drop('Movie')");
{% endcapture %}

{% capture rust_15 %}
graph.query("CALL db.idx.fulltext.drop('Movie')").execute().await?;
{% endcapture %}

{% include code_tabs.html id="fulltext_drop_tabs" shell=shell_15 python=python_15 javascript=javascript_15 java=java_15 rust=rust_15 %}

## Creating Full-Text indexing for Relation Labels
To create a full-text index on the name property of all relations with the label Manager and enable phonetic search, use the following syntax:

{% capture shell_16 %}
GRAPH.QUERY DEMO_GRAPH "CREATE FULLTEXT INDEX FOR ()-[m:Manager]-() on (m.name)"
{% endcapture %}

{% capture python_16 %}
graph.query("CREATE FULLTEXT INDEX FOR ()-[m:Manager]-() on (m.name)")
{% endcapture %}

{% capture javascript_16 %}
await graph.query("CREATE FULLTEXT INDEX FOR ()-[m:Manager]-() on (m.name)");
{% endcapture %}

{% capture java_16 %}
graph.query("CREATE FULLTEXT INDEX FOR ()-[m:Manager]-() on (m.name)");
{% endcapture %}

{% capture rust_16 %}
graph.query("CREATE FULLTEXT INDEX FOR ()-[m:Manager]-() on (m.name)").execute().await?;
{% endcapture %}

{% include code_tabs.html id="fulltext_relation_create_tabs" shell=shell_16 python=python_16 javascript=javascript_16 java=java_16 rust=rust_16 %}
## Querying with a Full-Text Index
To search for specific words within the indexed relations, use:

{% capture shell_17 %}
GRAPH.QUERY DEMO_GRAPH
"CALL db.idx.fulltext.queryRelationships('Manager', 'Charlie Munger') YIELD relationship RETURN relationship.name"
{% endcapture %}

{% capture python_17 %}
result = graph.query("CALL db.idx.fulltext.queryRelationships('Manager', 'Charlie Munger') YIELD relationship RETURN relationship.name")
{% endcapture %}

{% capture javascript_17 %}
const result = await graph.query("CALL db.idx.fulltext.queryRelationships('Manager', 'Charlie Munger') YIELD relationship RETURN relationship.name");
{% endcapture %}

{% capture java_17 %}
ResultSet result = graph.query("CALL db.idx.fulltext.queryRelationships('Manager', 'Charlie Munger') YIELD relationship RETURN relationship.name");
{% endcapture %}

{% capture rust_17 %}
let result = graph.query("CALL db.idx.fulltext.queryRelationships('Manager', 'Charlie Munger') YIELD relationship RETURN relationship.name").execute().await?;
{% endcapture %}

{% include code_tabs.html id="fulltext_relation_query_tabs" shell=shell_17 python=python_17 javascript=javascript_17 java=java_17 rust=rust_17 %}

## Deleting a Full-Text Index
To delete the full-text index for a specific relation label, use:

{% capture shell_18 %}
GRAPH.QUERY DEMO_GRAPH "CALL DROP FULLTEXT INDEX FOR ()-[m:Manager]-()  ON (m.name)"
{% endcapture %}

{% capture python_18 %}
graph.query("CALL DROP FULLTEXT INDEX FOR ()-[m:Manager]-()  ON (m.name)")
{% endcapture %}

{% capture javascript_18 %}
await graph.query("CALL DROP FULLTEXT INDEX FOR ()-[m:Manager]-()  ON (m.name)");
{% endcapture %}

{% capture java_18 %}
graph.query("CALL DROP FULLTEXT INDEX FOR ()-[m:Manager]-()  ON (m.name)");
{% endcapture %}

{% capture rust_18 %}
graph.query("CALL DROP FULLTEXT INDEX FOR ()-[m:Manager]-()  ON (m.name)").execute().await?;
{% endcapture %}

{% include code_tabs.html id="fulltext_relation_drop_tabs" shell=shell_18 python=python_18 javascript=javascript_18 java=java_18 rust=rust_18 %}

## Vector indexing

With the introduction of the `vector` data-type a new type of index was introduced.
A vector index is a dedicated index for indexing and searching through vectors.

To create this type of index use the following syntax:

```cypher
CREATE VECTOR INDEX FOR <entity_pattern> ON <entity_attribute> OPTIONS <options>
```

The options are:
```
{
   dimension: INT, // Requiered, length of the vector to be indexed
   similarityFunction: STRING, // Requiered, currently only euclidean or cosine are allowed
   M: INT, // Optional, maximum number of outgoing edges per node. default 16
   efConstruction: INT, // Optional, number of candidates during construction. default 200
   efRuntime: INT // Optional, number of candidates during search. default 10
}
```

For example, to create a vector index over all `Product` nodes `description` attribute
use the following syntax:

{% capture shell_19 %}
CREATE VECTOR INDEX FOR (p:Product) ON (p.description) OPTIONS {dimension:128, similarityFunction:'euclidean'}
{% endcapture %}

{% capture python_19 %}
graph.query("CREATE VECTOR INDEX FOR (p:Product) ON (p.description) OPTIONS {dimension:128, similarityFunction:'euclidean'}")
{% endcapture %}

{% capture javascript_19 %}
await graph.query("CREATE VECTOR INDEX FOR (p:Product) ON (p.description) OPTIONS {dimension:128, similarityFunction:'euclidean'}");
{% endcapture %}

{% capture java_19 %}
graph.query("CREATE VECTOR INDEX FOR (p:Product) ON (p.description) OPTIONS {dimension:128, similarityFunction:'euclidean'}");
{% endcapture %}

{% capture rust_19 %}
graph.query("CREATE VECTOR INDEX FOR (p:Product) ON (p.description) OPTIONS {dimension:128, similarityFunction:'euclidean'}").execute().await?;
{% endcapture %}

{% include code_tabs.html id="vector_create_node_tabs" shell=shell_19 python=python_19 javascript=javascript_19 java=java_19 rust=rust_19 %}

Similarly to create a vector index over all `Call` relationships `summary` attribute
use the following syntax:

{% capture shell_20 %}
CREATE VECTOR INDEX FOR ()-[e:Call]->() ON (e.summary) OPTIONS {dimension:128, similarityFunction:'euclidean'}
{% endcapture %}

{% capture python_20 %}
graph.query("CREATE VECTOR INDEX FOR ()-[e:Call]->() ON (e.summary) OPTIONS {dimension:128, similarityFunction:'euclidean'}")
{% endcapture %}

{% capture javascript_20 %}
await graph.query("CREATE VECTOR INDEX FOR ()-[e:Call]->() ON (e.summary) OPTIONS {dimension:128, similarityFunction:'euclidean'}");
{% endcapture %}

{% capture java_20 %}
graph.query("CREATE VECTOR INDEX FOR ()-[e:Call]->() ON (e.summary) OPTIONS {dimension:128, similarityFunction:'euclidean'}");
{% endcapture %}

{% capture rust_20 %}
graph.query("CREATE VECTOR INDEX FOR ()-[e:Call]->() ON (e.summary) OPTIONS {dimension:128, similarityFunction:'euclidean'}").execute().await?;
{% endcapture %}

{% include code_tabs.html id="vector_create_relation_tabs" shell=shell_20 python=python_20 javascript=javascript_20 java=java_20 rust=rust_20 %}

Please note, when creating a vector index, both the vector dimension and similarity function
must be provided. At the moment the only supported similarity functions are 'euclidean' or 'cosine'.

## Inserting vectors

To create a new vector use the [vecf32](/cypher/functions#vector-functions) function
as follows:

{% capture shell_21 %}
CREATE (p: Product {description: vecf32([2.1, 0.82, 1.3])})
{% endcapture %}

{% capture python_21 %}
graph.query("CREATE (p: Product {description: vecf32([2.1, 0.82, 1.3])})")
{% endcapture %}

{% capture javascript_21 %}
await graph.query("CREATE (p: Product {description: vecf32([2.1, 0.82, 1.3])})");
{% endcapture %}

{% capture java_21 %}
graph.query("CREATE (p: Product {description: vecf32([2.1, 0.82, 1.3])})");
{% endcapture %}

{% capture rust_21 %}
graph.query("CREATE (p: Product {description: vecf32([2.1, 0.82, 1.3])})").execute().await?;
{% endcapture %}

{% include code_tabs.html id="vector_insert_tabs" shell=shell_21 python=python_21 javascript=javascript_21 java=java_21 rust=rust_21 %}

The above query creates a new `Product` node with a `description` attribute containing a vector.

## Query vector index

Vector indices are used to search for similar vectors to a given query vector
using the similarity function as a measure of "distance".

To query the index use either `db.idx.vector.queryNodes` for node retrieval or
`db.idx.vector.queryRelationships` for relationships.

```cypher
CALL db.idx.vector.queryNodes(
    label: STRING,
    attribute: STRING,
    k: INTEGER,
    query: VECTOR
) YIELD node, score
```

```cypher
CALL db.idx.vector.queryRelationships(
    relationshipType: STRING,
    attribute: STRING,
    k: INTEGER,
    query: VECTOR
) YIELD relationship, score
```

To query up to 10 similar `Product` descriptions to a given query description vector
issue the following procedure call:

{% capture shell_22 %}
CALL db.idx.vector.queryNodes(
    'Product',
    'description',
    10,
    vecf32(<array_of_vector_elements>),
    ) YIELD node
{% endcapture %}

{% capture python_22 %}
result = graph.query("CALL db.idx.vector.queryNodes('Product', 'description', 10, vecf32(<array_of_vector_elements>)) YIELD node")
{% endcapture %}

{% capture javascript_22 %}
const result = await graph.query("CALL db.idx.vector.queryNodes('Product', 'description', 10, vecf32(<array_of_vector_elements>)) YIELD node");
{% endcapture %}

{% capture java_22 %}
ResultSet result = graph.query("CALL db.idx.vector.queryNodes('Product', 'description', 10, vecf32(<array_of_vector_elements>)) YIELD node");
{% endcapture %}

{% capture rust_22 %}
let result = graph.query("CALL db.idx.vector.queryNodes('Product', 'description', 10, vecf32(<array_of_vector_elements>)) YIELD node").execute().await?;
{% endcapture %}

{% include code_tabs.html id="vector_query_tabs" shell=shell_22 python=python_22 javascript=javascript_22 java=java_22 rust=rust_22 %}

The procedure can yield both the indexed entity assigned to the found similar vector
in addition to a similarity score of that entity.

## Deleting a vector index

To remove a vector index, simply issue the `drop index` command as follows:

```cypher
DROP VECTOR INDEX FOR <entity_pattern> (<entity_attribute>)
```

For example, to drop the vector index over Product description, invoke:

{% capture shell_23 %}
DROP VECTOR INDEX FOR (p:Product) ON (p.description)
{% endcapture %}

{% capture python_23 %}
graph.query("DROP VECTOR INDEX FOR (p:Product) ON (p.description)")
{% endcapture %}

{% capture javascript_23 %}
await graph.query("DROP VECTOR INDEX FOR (p:Product) ON (p.description)");
{% endcapture %}

{% capture java_23 %}
graph.query("DROP VECTOR INDEX FOR (p:Product) ON (p.description)");
{% endcapture %}

{% capture rust_23 %}
graph.query("DROP VECTOR INDEX FOR (p:Product) ON (p.description)").execute().await?;
{% endcapture %}

{% include code_tabs.html id="vector_drop_tabs" shell=shell_23 python=python_23 javascript=javascript_23 java=java_23 rust=rust_23 %}
