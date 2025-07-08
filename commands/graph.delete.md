---
title: "GRAPH.DELETE"
nav_order: 3
description: >
    Completely removes the graph and all of its entities
parent: "Commands"    
---

# GRAPH.DELETE

Completely removes the graph and all of its entities.

Arguments: `Graph name`

Returns: `String indicating if operation succeeded or failed.`

{% capture shell_0 %}
GRAPH.DELETE us_government
{% endcapture %}

{% capture python_0 %}
graph.delete()
{% endcapture %}

{% capture javascript_0 %}
await graph.delete();
{% endcapture %}

{% capture java_0 %}
graph.delete();
{% endcapture %}

{% capture rust_0 %}
graph.delete()?;
{% endcapture %}

{% include code_tabs.html id="tabs_0" shell=shell_0 python=python_0 javascript=javascript_0 java=java_0 rust=rust_0 %}

Note: To delete a node from the graph (not the entire graph), execute a `MATCH` query and pass the alias to the `DELETE` clause:

{% capture shell_1 %}
GRAPH.QUERY DEMO_GRAPH "MATCH (x:Y {propname: propvalue}) DELETE x"
{% endcapture %}

{% capture python_1 %}
graph.query("MATCH (x:Y {propname: propvalue}) DELETE x")
{% endcapture %}

{% capture javascript_1 %}
await graph.query("MATCH (x:Y {propname: propvalue}) DELETE x");
{% endcapture %}

{% capture java_1 %}
graph.query("MATCH (x:Y {propname: propvalue}) DELETE x");
{% endcapture %}

{% capture rust_1 %}
graph.query("MATCH (x:Y {propname: propvalue}) DELETE x")?;
{% endcapture %}

{% include code_tabs.html id="tabs_1" shell=shell_1 python=python_1 javascript=javascript_1 java=java_1 rust=rust_1 %}

WARNING: When you delete a node, all of the node's incoming/outgoing relationships are also removed.

