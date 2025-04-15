---
title: "GRAPH.COPY"
description: >
    creates a copy of the given graph
parent: "Commands"
---

# GRAPH.COPY

Usage: `GRAPH.COPY <src> <dest>`

The GRAPH.COPY command creates a copy of a graph while leaving the source graph fully accessible.

Example:

{% capture shell_0 %}
127.0.0.1:6379> GRAPH.LIST
(empty array)
127.0.0.1:6379> GRAPH.QUERY A "CREATE (:Account {number: 516637})"
1) 1) "Labels added: 1"
   2) "Nodes created: 1"
   3) "Properties set: 1"
   4) "Cached execution: 0"
   5) "Query internal execution time: 0.588084 milliseconds"
127.0.0.1:6379> GRAPH.COPY A Z
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
