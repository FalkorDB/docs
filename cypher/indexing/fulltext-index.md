---
title: "Full-text Index"
nav_order: 2
description: >
    FalkorDB leverages RediSearch indexing capabilities to provide full-text indices through procedure calls.
parent: "Indexing"
grand_parent: "Cypher Language"
---

# Full-text indexing

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
GRAPH.QUERY DEMO_GRAPH "DROP FULLTEXT INDEX FOR ()-[m:Manager]-() ON (m.name)"
{% endcapture %}

{% capture python_18 %}
graph.query("DROP FULLTEXT INDEX FOR ()-[m:Manager]-() ON (m.name)")
{% endcapture %}

{% capture javascript_18 %}
await graph.query("DROP FULLTEXT INDEX FOR ()-[m:Manager]-() ON (m.name)");
{% endcapture %}

{% capture java_18 %}
graph.query("DROP FULLTEXT INDEX FOR ()-[m:Manager]-() ON (m.name)");
{% endcapture %}

{% capture rust_18 %}
graph.query("DROP FULLTEXT INDEX FOR ()-[m:Manager]-() ON (m.name)").execute().await?;
{% endcapture %}

{% include code_tabs.html id="fulltext_relation_drop_tabs" shell=shell_18 python=python_18 javascript=javascript_18 java=java_18 rust=rust_18 %}
