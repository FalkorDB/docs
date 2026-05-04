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

Arguments: `Graph name, Query, [timeout], [--compact], [version]`

Returns: [Result set](/design/result-structure) for a read only query or an error if a write query was given.

| Optional argument | Description |
| --- | --- |
| `timeout` | Query-level timeout in milliseconds. See [the configuration section](/configuration#timeout). |
| `--compact` | Returns results in [compact format](/design/client-spec#retrieving-the-compact-result-set). |
| `version` | Graph version number. When provided, the server rejects the query with a `version mismatch` error if the current graph version doesn't match, allowing clients to invalidate cached schema mappings. |

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

{% include faq_accordion.html title="Frequently Asked Questions" q1="What is the difference between GRAPH.QUERY and GRAPH.RO_QUERY?" a1="**GRAPH.RO_QUERY** only executes read operations and will return an error if you attempt a write query (CREATE, SET, DELETE, MERGE with creation). **GRAPH.QUERY** supports both read and write operations." q2="Why should I use GRAPH.RO_QUERY instead of GRAPH.QUERY for reads?" a2="GRAPH.RO_QUERY can be distributed to read replicas in a clustered setup, improving read scalability. It also provides a safety guarantee that data will not be accidentally modified." q3="What happens if I pass a write query to GRAPH.RO_QUERY?" a3="The command will return an error indicating that write queries are not permitted. The graph data will remain unchanged." q4="Does GRAPH.RO_QUERY support the same optional parameters as GRAPH.QUERY?" a4="Yes. GRAPH.RO_QUERY accepts the same optional parameters: `timeout`, `--compact`, and `version`." %}
