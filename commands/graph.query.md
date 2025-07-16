---
title: "GRAPH.QUERY"
nav_order: 1
description: >
    Executes the given query against a specified graph
parent: "Commands"    
---

# GRAPH.QUERY

Executes the given query against a specified graph.

Arguments: `Graph name, Query, Timeout [optional]`

Returns: [Result set](/design/result_structure)

### Queries and Parameterized Queries

The execution plans of queries, both regular and parameterized, are cached (up to [CACHE_SIZE](/configuration#cache_size) unique queries are cached). Therefore, it is recommended to use parameterized queries when executing many queries with the same pattern but different constants.

Query-level timeouts can be set as described in [the configuration section](/configuration#timeout).

#### Command structure

`GRAPH.QUERY graph_name "query"`

example:

{% capture shell_0 %}
GRAPH.QUERY us_government "MATCH (p:president)-[:born]->(:state {name:'Hawaii'}) RETURN p"
{% endcapture %}

{% capture python_0 %}
graph.query("MATCH (p:president)-[:born]->(:state {name:'Hawaii'}) RETURN p")
{% endcapture %}

{% capture javascript_0 %}
const result = await graph.query("MATCH (p:president)-[:born]->(:state {name:'Hawaii'}) RETURN p");
console.log(result);
{% endcapture %}

{% capture java_0 %}
ResultSet result = graph.query("MATCH (p:president)-[:born]->(:state {name:'Hawaii'}) RETURN p");
System.out.println(result);
{% endcapture %}

{% capture rust_0 %}
let result = graph.query(r#"MATCH (p:president)-[:born]->(:state {name:'Hawaii'}) RETURN p"#).execute().await?;
println!("{:?}", result);
{% endcapture %}

{% include code_tabs.html id="tabs_0" shell=shell_0 python=python_0 javascript=javascript_0 java=java_0 rust=rust_0 %}


#### Parametrized query structure:

`GRAPH.QUERY graph_name "CYPHER param=val [param=val ...] query"`

example:

{% capture shell_1 %}
GRAPH.QUERY us_government "CYPHER state_name='Hawaii' MATCH (p:president)-[:born]->(:state {name:$state_name}) RETURN p"
{% endcapture %}

{% capture python_1 %}
graph.query("MATCH (p:president)-[:born]->(:state {name:$state_name}) RETURN p", {'state_name': 'Hawaii'})
{% endcapture %}

{% capture javascript_1 %}
const result = await graph.query(
  "MATCH (p:president)-[:born]->(:state {name:$state_name}) RETURN p",
  { params: { state_name: "Hawaii" } }
);
console.log(result);
{% endcapture %}

{% capture java_1 %}
Map<String, Object> params = new HashMap<>();
params.put("state_name", "Hawaii");
ResultSet result = graph.query(
  "MATCH (p:president)-[:born]->(:state {name:$state_name}) RETURN p",
  params
);
System.out.println(result);
{% endcapture %}

{% capture rust_1 %}
let params = std::collections::HashMap::from([
    ("state_name", "Hawaii")
]);
let result = graph.query_with_params(
    r#"MATCH (p:president)-[:born]->(:state {name:$state_name}) RETURN p"#,
    &params
).execute().await?;
println!("{:?}", result);
{% endcapture %}

{% include code_tabs.html id="tabs_1" shell=shell_1 python=python_1 javascript=javascript_1 java=java_1 rust=rust_1 %}

### Query language

The syntax is based on [Cypher](http://www.opencypher.org/). [Most](/cypher/cypher_support) of the language is supported. See [Cypher documentation](/cypher).