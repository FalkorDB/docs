---
title: "Vector Index"
nav_order: 3
description: >
    FalkorDB supports vector indexes for similarity search on vector embeddings, essential for AI and machine learning applications.
parent: "Indexing"
grand_parent: "Cypher Language"
---

# Vector indexing

With the introduction of the `vector` data-type a new type of index was introduced.
A vector index is a dedicated index for indexing and searching through vectors.

To create this type of index use the following syntax:

```cypher
CREATE VECTOR INDEX FOR <entity_pattern> ON <entity_attribute> OPTIONS <options>
```

The options are:
```
{
   dimension: INT, // Required, length of the vector to be indexed
   similarityFunction: STRING, // Required, currently only euclidean or cosine are allowed
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
