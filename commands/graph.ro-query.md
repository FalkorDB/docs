---
title: "GRAPH.RO_QUERY"
nav_order: 2
description: >
    Executes a given read only query against a specified graph
parent: "Commands"
redirect_from:
  - /commands/graph.ro_query.html
  - /commands/graph.ro_query
---

# GRAPH.RO_QUERY

Executes a given read only query against a specified graph.

Arguments: `Graph name, Query, Timeout [optional]`

Returns: [Result set](/design/result-structure) for a read only query or an error if a write query was given.

{% capture shell_0 %}
GRAPH.RO_QUERY us_government "MATCH (p:president)-[:born]->(:state {name:'Hawaii'}) RETURN p"
{% endcapture %}

{% capture python_0 %}
graph.ro_query("MATCH (p:president)-[:born]->(:state {name:'Hawaii'}) RETURN p")
{% endcapture %}

{% capture javascript_0 %}
const result = await graph.ro_query("MATCH (p:president)-[:born]->(:state {name:'Hawaii'}) RETURN p");
console.log(result);
{% endcapture %}

{% capture java_0 %}
ResultSet result = graph.readOnlyQuery("MATCH (p:president)-[:born]->(:state {name:'Hawaii'}) RETURN p");
System.out.println(result);
{% endcapture %}

{% capture rust_0 %}
let result = graph.ro_query(r#"MATCH (p:president)-[:born]->(:state {name:'Hawaii'}) RETURN p"#).execute().await?;
println!("{:?}", result);
{% endcapture %}

{% include code_tabs.html id="tabs_0" shell=shell_0 python=python_0 javascript=javascript_0 java=java_0 rust=rust_0 %}

Query-level timeouts can be set as described in [the configuration section](/configuration#timeout).
