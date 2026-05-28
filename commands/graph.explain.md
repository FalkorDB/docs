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
import com.falkordb.*;

Driver driver = FalkorDB.driver("localhost", 6379);
Graph graph = driver.graph("us_government");
String query = "MATCH (p:President)-[:BORN]->(h:State {name:'Hawaii'}) RETURN p";
String result = graph.explain(query);
System.out.println(result);
{% endcapture %}

{% capture rust_0 %}
use falkordb::{FalkorClientBuilder, FalkorConnectionInfo};

let connection_info: FalkorConnectionInfo = "falkor://127.0.0.1:6379"
    .try_into().expect("Invalid connection info");
let client = FalkorClientBuilder::new()
    .with_connection_info(connection_info)
    .build().expect("Failed to build client");
let graph = client.select_graph("us_government");
let query = r#"MATCH (p:President)-[:BORN]->(h:State {name:'Hawaii'}) RETURN p"#;
let result = graph.explain(query)?;
println!("{}", result);
{% endcapture %}

{% include code_tabs.html id="explain_tabs" shell=shell_0 python=python_0 javascript=javascript_0 java=java_0 rust=rust_0 %}

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="Does GRAPH.EXPLAIN actually execute the query?"
  a1="No. `GRAPH.EXPLAIN` only constructs the execution plan without running the query. No data is read or modified. Use `GRAPH.PROFILE` if you want to execute the query and see runtime metrics."
  q2="What can I learn from the execution plan?"
  a2="The execution plan shows the sequence of operations (scans, filters, traversals, projections) the engine will perform. This helps you understand whether indexes are being used and identify potential performance bottlenecks."
  q3="How do I know if my query is using an index?"
  a3="In the execution plan output, look for operations like `Index Scan` instead of `Node By Label Scan`. An index scan indicates the query is leveraging an index for faster lookups."
  q4="Can I use GRAPH.EXPLAIN with parameterized queries?"
  a4="Yes. You can pass parameterized queries to `GRAPH.EXPLAIN` using the same `CYPHER param=val` syntax as `GRAPH.QUERY`."
%}
