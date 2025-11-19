---
title: "Range Index"
nav_order: 1
description: >
    FalkorDB supports single-property indexes for node labels and for relationship type. String, numeric, and geospatial data types can be indexed.
parent: "Indexing"
grand_parent: "Cypher Language"
---

# Range Index

FalkorDB supports single-property indexes for node labels and for relationship type. String, numeric, and geospatial data types can be indexed.

## Creating an index for a node label

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

Geospatial indexes can currently only be leveraged with `<` and `<=` filters; matching nodes outside the given radius are matched using conventional traversal.

## Creating an index for a relationship type

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
# Output:
# Results
#     Project
#         Edge By Index Scan | [f:FOLLOW]
#             Node By Index Scan | (p:Person)
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

## Deleting an index for a node label

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

## Deleting an index for a relationship type

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

## Array Indices

FalkorDB supports indexing on array properties containing scalar values (e.g., integers, floats, strings), enabling efficient lookups for elements within such arrays.

Note: Complex types like nested arrays, maps, or vectors are not supported for indexing.

The following example demonstrates how to index and search an array property:

{% capture shell_9 %}
# Create a node with an array property
GRAPH.QUERY DEMO_GRAPH "CREATE (:Person {samples: [-21, 30.5, 0, 90, 3.14]})"

# Create an index on the array property
GRAPH.QUERY DEMO_GRAPH "CREATE INDEX FOR (p:Person) ON (p.samples)"

# Use the index to search for nodes containing a specific value in the array
GRAPH.QUERY DEMO_GRAPH "MATCH (p:Person) WHERE 90 IN p.samples RETURN p"
{% endcapture %}

{% capture python_9 %}
# Create a node with an array property
graph.query("CREATE (:Person {samples: [-21, 30.5, 0, 90, 3.14]})")

# Create an index on the array property
graph.query("CREATE INDEX FOR (p:Person) ON (p.samples)")

# Use the index to search for nodes containing a specific value in the array
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
