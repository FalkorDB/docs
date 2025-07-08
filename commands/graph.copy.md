---
title: "GRAPH.COPY"
description: >
    creates a copy of the given graph
parent: "Commands"
---

# GRAPH.COPY

Usage: `GRAPH.COPY <src> <dest>`

<<<<<<< HEAD
The GRAPH.COPY command creates a copy of a graph while leaving the source graph fully accessible.
=======
The `GRAPH.COPY` command creates a copy of a graph, while the copy is performed the `src` graph is fully accessible.
>>>>>>> 4ce9d9d (add code examples in different langs)

Example:

{% capture shell_0 %}
<<<<<<< HEAD
127.0.0.1:6379> GRAPH.LIST
(empty array)
=======
# Create a graph and copy it
>>>>>>> 4ce9d9d (add code examples in different langs)
127.0.0.1:6379> GRAPH.QUERY A "CREATE (:Account {number: 516637})"
127.0.0.1:6379> GRAPH.COPY A Z
<<<<<<< HEAD
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

{% include code_tabs.html id="tabs_0" shell=shell_0 python=python_0 %}
=======
127.0.0.1:6379> GRAPH.QUERY Z "MATCH (a:Account) RETURN a.number"
# Output: 516637
{% endcapture %}

{% capture python_0 %}
from falkordb import FalkorDB
client = FalkorDB()
graph_a = client.select_graph('A')
graph_a.query("CREATE (:Account {number: 516637})")
client.copy_graph('A', 'Z')
graph_z = client.select_graph('Z')
result = graph_z.query("MATCH (a:Account) RETURN a.number")
print(result)
{% endcapture %}

{% capture javascript_0 %}
import { FalkorDB } from 'falkordb';
const client = await FalkorDB.connect();
const graphA = client.selectGraph('A');
await graphA.query("CREATE (:Account {number: 516637})");
await client.copyGraph('A', 'Z');
const graphZ = client.selectGraph('Z');
const result = await graphZ.query("MATCH (a:Account) RETURN a.number");
console.log(result);
{% endcapture %}

{% capture java_0 %}
FalkorDB client = new FalkorDB();
Graph graphA = client.selectGraph("A");
graphA.query("CREATE (:Account {number: 516637})");
client.copyGraph("A", "Z");
Graph graphZ = client.selectGraph("Z");
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
>>>>>>> 4ce9d9d (add code examples in different langs)
