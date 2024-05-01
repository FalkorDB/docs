---
title: "Indexing"
nav_order: 20
description: >
    FalkorDB supports single-property indexes for node labels and for relationship type. String, numeric, and geospatial data types can be indexed.
parent: "Cypher Language"
---

# Indexing

FalkorDB supports single-property indexes for node labels and for relationship type. String, numeric, and geospatial data types can be indexed.

## Creating an index for a node label

For a node label, the index creation syntax is:

```sh
GRAPH.QUERY DEMO_GRAPH "CREATE INDEX FOR (p:Person) ON (p.age)"
```

An old syntax is also supported:

```sh
GRAPH.QUERY DEMO_GRAPH "CREATE INDEX ON :Person(age)"
```

After an index is explicitly created, it will automatically be used by queries that reference that label and any indexed property in a filter.

```sh
GRAPH.EXPLAIN DEMO_GRAPH "MATCH (p:Person) WHERE p.age > 80 RETURN p"
1) "Results"
2) "    Project"
3) "        Index Scan | (p:Person)"
```

This can significantly improve the runtime of queries with very specific filters. An index on `:employer(name)`, for example, will dramatically benefit the query:

```sh
GRAPH.QUERY DEMO_GRAPH
"MATCH (:Employer {name: 'Dunder Mifflin'})-[:EMPLOYS]->(p:Person) RETURN p"
```

An example of utilizing a geospatial index to find `Employer` nodes within 5 kilometers of Scranton is:

```sh
GRAPH.QUERY DEMO_GRAPH
"WITH point({latitude:41.4045886, longitude:-75.6969532}) AS scranton MATCH (e:Employer) WHERE distance(e.location, scranton) < 5000 RETURN e"
```

Geospatial indexes can currently only be leveraged with `<` and `<=` filters; matching nodes outside of the given radius is performed using conventional matching.

## Creating an index for a relationship type

For a relationship type, the index creation syntax is:

```sh
GRAPH.QUERY DEMO_GRAPH "CREATE INDEX FOR ()-[f:FOLLOW]-() ON (f.created_at)"
```

Then the execution plan for using the index:

```sh
GRAPH.EXPLAIN DEMO_GRAPH "MATCH (p:Person {id: 0})-[f:FOLLOW]->(fp) WHERE 0 < f.created_at AND f.created_at < 1000 RETURN fp"
1) "Results"
2) "    Project"
3) "        Edge By Index Scan | [f:FOLLOW]"
4) "            Node By Index Scan | (p:Person)"
```

This can significantly improve the runtime of queries that traverse super nodes or when we want to start traverse from relationships.

## Deleting an index for a node label

For a node label, the index deletion syntax is:

```sh
GRAPH.QUERY DEMO_GRAPH "DROP INDEX ON :Person(age)"
```

## Deleting an index for a relationship type

For a relationship type, the index deletion syntax is:

```sh
GRAPH.QUERY DEMO_GRAPH "DROP INDEX ON :FOLLOW(created_at)"
```

# Full-text indexing

FalkorDB leverages the indexing capabilities of [RediSearch](https://redis.io/docs/interact/search-and-query/) to provide full-text indices through procedure calls.

## Creating a full-text index for a node label

To construct a full-text index on the `title` property of all nodes with label `Movie`, use the syntax:

```sh
GRAPH.QUERY DEMO_GRAPH "CALL db.idx.fulltext.createNodeIndex('Movie', 'title')"
```

More properties can be added to this index by adding their names to the above set of arguments, or using this syntax again with the additional names.

```sh
GRAPH.QUERY DEMO_GRAPH "CALL db.idx.fulltext.createNodeIndex('Person', 'firstName', 'lastName')"
```

RediSearch provide 2 index configuration options:

1. Language - Define which language to use for stemming text which is adding the base form of a word to the index. This allows the query for "going" to also return results for "go" and "gone", for example.
2. Stopwords - These are words that are usually so common that they do not add much information to search, but take up a lot of space and CPU time in the index.

To construct a full-text index on the `title` property using `German` language and using custom stopwords of all nodes with label `Movie`, use the syntax:

```sh
GRAPH.QUERY DEMO_GRAPH "CALL db.idx.fulltext.createNodeIndex({ label: 'Movie', language: 'German', stopwords: ['a', 'ab'] }, 'title')"
```

RediSearch provide 3 additional field configuration options:

1. Weight - The importance of the text in the field
2. Nostem - Skip stemming when indexing text
3. Phonetic - Enable phonetic search on the text

To construct a full-text index on the `title` property with phonetic search of all nodes with label `Movie`, use the syntax:

```sh
GRAPH.QUERY DEMO_GRAPH "CALL db.idx.fulltext.createNodeIndex('Movie', {field: 'title', phonetic: 'dm:en'})"
```

## Utilizing a full-text index for a node label

An index can be invoked to match any whole words contained within:

```sh
GRAPH.QUERY DEMO_GRAPH
"CALL db.idx.fulltext.queryNodes('Movie', 'Book') YIELD node RETURN node.title"
1) 1) "node.title"
2) 1) 1) "The Jungle Book"
   2) 1) "The Book of Life"
3) 1) "Query internal execution time: 0.927409 milliseconds"
```

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

```sh
GRAPH.QUERY DEMO_GRAPH "CALL db.idx.fulltext.drop('Movie')"
```

# Vector indexing

With the introduction of the `vector` data-type a new type of index was introduce.
A vector index is a dedicated index for indexing and searching through vectors

To create this type of index use the following syntax:

```cypher
CREATE VECTOR INDEX FOR <entity_pattern> ON <entity_attribute> OPTIONS <options>
```

For example, to create a vector index over all `Product` nodes `description` attribute
use the following syntax:

```cypher
CREATE VECTOR INDEX FOR (p:Product) ON (p.description) OPTIONS {dimension:128, similarityFunction:'euclidean'}
```

Similarly to create a vector index over all `Call` relationships `summary` attribute
use the following syntax:

```cypher
CREATE VECTOR INDEX FOR ()-[e:Call]->() ON (e.summary) OPTIONS {dimension:128, similarityFunction:'euclidean'}
```

Please note when creating a vector index both the vector dimension and similarity function
must be provided. At the moment the only supported similarity function is 'euclidean'.

## Inserting vectors

To create a new vector use the [vecf32](/cypher/functions#vector-functions) function
as follows:

```cypher
CREATE (p: Product {description: vecf32([2.1, 0.82, 1.3])})
```

The above query creates a new `Product` node with a `description` attribute containing a vector.

## Query vector index

Vector indices are used to search for similar vectors to a given query vector
using the similarity function as a measure of "distance"

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

```cypher
CALL db.idx.vector.queryNodes(
    'Product',
    'description',
    10,
    vecf32(<array_of_vector_elements>),
    ) YIELD node
```

The procedure can yield both the indexed entity assigned to the found similar vector
in addition to a similarity score of that entity.

## Deleting a vector index

To remove a vector index simply issue the `drop index` command as follows:

```cypher
DROP VECTOR INDEX FOR <entity_pattern> (<entity_attribute>)
```

For example to drop the vector index over Product description invoke:

```cypher
DROP VECTOR INDEX FOR (p:Product) ON (p.description)
```
