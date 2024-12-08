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

{% capture bash_0 %}
GRAPH.QUERY us_government "MATCH (p:president)-[:born]->(:state {name:'Hawaii'}) RETURN p"
{% endcapture %}

{% capture python_0 %}
graph.query("MATCH (p:president)-[:born]->(:state {name:'Hawaii'}) RETURN p")
{% endcapture %}

{% include code_tabs.html id="tabs_0" bash=bash_0 python=python_0 %}


#### Parametrized query structure:

`GRAPH.QUERY graph_name "CYPHER param=val [param=val ...] query"`

example:

{% capture bash_1 %}
GRAPH.QUERY us_government "CYPHER state_name='Hawaii' MATCH (p:president)-[:born]->(:state {name:$state_name}) RETURN p"
{% endcapture %}

{% capture python_1 %}
graph.query("MATCH (p:president)-[:born]->(:state {name:$state_name}) RETURN p", {'state_name': 'Hawaii'})
{% endcapture %}

{% include code_tabs.html id="tabs_1" bash=bash_1 python=python_1 %}

### Query language

The syntax is based on [Cypher](http://www.opencypher.org/). [Most](/cypher/cypher_support) of the language is supported. See [Cypher documentation](/cypher).