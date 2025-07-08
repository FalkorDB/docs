---
title: "GRAPH.EXPLAIN"
nav_order: 4
description: >
    Returns a query execution plan without running the query
parent: "Commands"    
---

# GRAPH.EXPLAIN

Constructs a query execution plan but does not run it. Inspect this execution plan to better
understand how your query will get executed.

Arguments: `Graph name, Query`

Returns: `String representation of a query execution plan`

{% capture shell_0 %}
GRAPH.EXPLAIN us_government "MATCH (p:President)-[:BORN]->(h:State {name:'Hawaii'}) RETURN p"
{% endcapture %}

{% capture python_0 %}
from falkordb import FalkorDB
client = FalkorDB()
graph = client.select_graph('us_government')
query = "MATCH (p:President)-[:BORN]->(h:State {name:'Hawaii'}) RETURN p"
result = graph.explain(query)
print(result)
{% endcapture %}

{% capture javascript_0 %}
import { FalkorDB } from 'falkordb';
const client = await FalkorDB.connect();
const graph = client.selectGraph('us_government');
const query = "MATCH (p:President)-[:BORN]->(h:State {name:'Hawaii'}) RETURN p";
const result = await graph.explain(query);
console.log(result);
{% endcapture %}

{% capture java_0 %}
FalkorDB client = new FalkorDB();
Graph graph = client.selectGraph("us_government");
String query = "MATCH (p:President)-[:BORN]->(h:State {name:'Hawaii'}) RETURN p";
String result = graph.explain(query);
System.out.println(result);
{% endcapture %}

{% capture rust_0 %}
let client = FalkorDB::connect_default();
let graph = client.select_graph("us_government");
let query = r#"MATCH (p:President)-[:BORN]->(h:State {name:'Hawaii'}) RETURN p"#;
let result = graph.explain(query)?;
println!("{}", result);
{% endcapture %}

{% include code_tabs.html id="explain_tabs" shell=shell_0 python=python_0 javascript=javascript_0 java=java_0 rust=rust_0 %}
