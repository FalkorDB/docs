---
title: "GRAPH.RO_QUERY"
nav_order: 2
description: >
    Executes a given read only query against a specified graph
parent: "Commands"    
---

# GRAPH.RO_QUERY

Executes a given read only query against a specified graph.

Arguments: `Graph name, Query, Timeout [optional]`

Returns: [Result set](/design/result_structure) for a read only query or an error if a write query was given.

{% capture shell_0 %}
GRAPH.RO_QUERY us_government "MATCH (p:president)-[:born]->(:state {name:'Hawaii'}) RETURN p"
{% endcapture %}

{% capture python_0 %}
graph.ro_query("MATCH (p:president)-[:born]->(:state {name:'Hawaii'}) RETURN p")
{% endcapture %}

{% include code_tabs.html id="tabs_0" shell=shell_0 python=python_0 %}

Query-level timeouts can be set as described in [the configuration section](/configuration#timeout).
