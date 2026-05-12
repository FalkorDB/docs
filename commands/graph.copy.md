---
title: "GRAPH.COPY"
description: >
    Creates a copy of the given graph
parent: "Commands"
nav_order: 9
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
result = graph_z.query('MATCH (a:Account) RETURN a.number')
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
import com.falkordb.*;

Driver driver = FalkorDB.driver("localhost", 6379);

// Create Graph 'A'
Graph graphA = driver.graph("A");
graphA.query("CREATE (:Account {number: 516637})");

// Copy Graph 'A' to 'Z'
graphA.copyGraph("Z");
Graph graphZ = driver.graph("Z");

// Query Graph 'Z'
ResultSet result = graphZ.query("MATCH (a:Account) RETURN a.number");
System.out.println(result);
{% endcapture %}

{% capture rust_0 %}
use falkordb::{FalkorClientBuilder, FalkorConnectionInfo};

let connection_info: FalkorConnectionInfo = "falkor://127.0.0.1:6379"
    .try_into().expect("Invalid connection info");
let client = FalkorClientBuilder::new()
    .with_connection_info(connection_info)
    .build().expect("Failed to build client");
let graph_a = client.select_graph("A");

graph_a.query("CREATE (:Account {number: 516637})")?;
client.copy_graph("A", "Z")?;

let graph_z = client.select_graph("Z");
let result = graph_z.query("MATCH (a:Account) RETURN a.number")?;
println!("{:?}", result);
{% endcapture %}

{% include code_tabs.html id="copy_tabs" shell=shell_0 python=python_0 javascript=javascript_0 java=java_0 rust=rust_0 %}

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="Can I still query the source graph while GRAPH.COPY is running?"
  a1="Yes. The source graph remains **fully accessible** for both reads and writes during the copy operation."
  q2="Does GRAPH.COPY also copy indexes and constraints?"
  a2="Yes. `GRAPH.COPY` creates a complete clone of the source graph including all nodes, relationships, properties, indexes, and constraints."
  q3="What happens if the destination graph already exists?"
  a3="The command will return an error. You must delete the destination graph first using `GRAPH.DELETE` before copying to that key name."
  q4="Is GRAPH.COPY atomic?"
  a4="The copy reflects a consistent snapshot of the source graph at the time the command begins. Modifications to the source graph during the copy will not affect the destination."
%}
