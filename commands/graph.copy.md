---
title: "GRAPH.COPY"
description: >
    creates a copy of the given graph
parent: "Commands"
---

# GRAPH.COPY

Usage: `GRAPH.COPY <src> <dest>`

The `GRAPH.COPY` command creates a copy of a graph, while the copy is performed the `src` graph is fully accessible.

Example:

{% capture shell_0 %}
127.0.0.1:6379> GRAPH.LIST
(empty array)
127.0.0.1:6379> GRAPH.QUERY A "CREATE (:Account {number: 516637})"

1) 1) "Labels added: 1"
   2) "Nodes created: 1"
   3) "Properties set: 1"
   4) "Cached execution: 0"
   5) "Query internal execution time: 0.588084 milliseconds"
127.0.0.1:6379> GRAPH.COPY A Z
"OK"
127.0.0.1:6379> GRAPH.LIST
1) "Z"
2) "telemetry{A}"
3) "A"
127.0.0.1:6379> GRAPH.QUERY Z "MATCH (a:Account) RETURN a.number"
1) 1) "a.number"
2) 1) 1) (integer) 516637
3) 1) "Cached execution: 0"
   2) "Query internal execution time: 0.638375 milliseconds"
{% endcapture %}

{% capture python_0 %}

# Graphs list is empty

graph_list = db.list()

# Create Graph 'A'

graph_a = db.select_graph('A')
result = graph_a.query('CREATE (:Account {number: 516637})')

# Copy Graph 'A' to 'Z'

graph_z = graph_a.copy('Z')

# Graphs list including 'A' and 'Z'

graph_list = db.list()

# Query Graph 'Z'

result = graph_z.query('MATCH (a:Account) RETURN a.number')Query Graph 'Z'
{% endcapture %}

{% capture javascript_0 %}
import { FalkorDB } from 'falkordb';

const client = await FalkorDB.connect();

// Create Graph 'A'
const graphA = client.selectGraph('A');
await graphA.query("CREATE (:Account {number: 516637})");

// Copy Graph 'A' to 'Z'
await client.copyGraph('A', 'Z');

// Query Graph 'Z'
const graphZ = client.selectGraph('Z');
const result = await graphZ.query("MATCH (a:Account) RETURN a.number");
console.log(result);
{% endcapture %}

{% capture java_0 %}
FalkorDB client = new FalkorDB();

// Create Graph 'A'
Graph graphA = client.selectGraph("A");
graphA.query("CREATE (:Account {number: 516637})");

// Copy Graph 'A' to 'Z'
client.copyGraph("A", "Z");
Graph graphZ = client.selectGraph("Z");

// Query Graph 'Z'
ResultSet result = graphZ.query("MATCH (a:Account) RETURN a.number");
System.out.println(result);
{% endcapture %}

{% capture rust_0 %}
let client = FalkorDB::connect_default();
let graph_a = client.select_graph("A");

graph_a.query("CREATE (:Account {number: 516637})")?;
client.copy_graph("A", "Z")?;

let graph_z = client.select_graph("Z");
let result = graph_z.query("MATCH (a:Account) RETURN a.number")?;
println!("{:?}", result);
{% endcapture %}

{% include code_tabs.html id="copy_tabs" shell=shell_0 python=python_0 javascript=javascript_0 java=java_0 rust=rust_0 %}
