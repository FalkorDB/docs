---
title: "GRAPH.DELETE"
nav_order: 3
description: >
    Completely remove a graph and all its entities (nodes and relationships) from FalkorDB using the GRAPH.DELETE command with examples for multiple programming languages.
parent: "Commands"    
---

# GRAPH.DELETE

Completely removes a graph and all of its entities (nodes and relationships).

## Syntax

```text
GRAPH.DELETE graph_name
```

**Arguments:**
- `graph_name` - Name of the graph to delete

**Returns:** String indicating if the operation succeeded or failed.

## Examples

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

## Deleting Individual Nodes

**Note:** To delete specific nodes or relationships (not the entire graph), use the Cypher `DELETE` clause with a `MATCH` query:

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

**⚠️ Warning:** When you delete a node using the Cypher `DELETE` clause, all of the node's incoming and outgoing relationships are also automatically removed.

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="Can I undo a GRAPH.DELETE operation?"
  a1="No. `GRAPH.DELETE` permanently removes the entire graph and all its data. There is no undo. Make sure to back up your data before deleting a graph."
  q2="What is the difference between GRAPH.DELETE and the Cypher DELETE clause?"
  a2="`GRAPH.DELETE` removes the **entire graph** key and all its entities. The Cypher `DELETE` clause within a `GRAPH.QUERY` removes specific nodes or relationships matched by a pattern."
  q3="Does GRAPH.DELETE block other operations?"
  a3="The delete operation acquires a write lock on the graph. Any queries running against the graph will complete before the deletion proceeds, but new queries will be blocked until the deletion finishes."
  q4="What happens to relationships when I delete a node with Cypher DELETE?"
  a4="All incoming and outgoing relationships connected to the deleted node are automatically removed. You do not need to delete them separately."
%}
