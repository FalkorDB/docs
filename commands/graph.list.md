---
title: "GRAPH.LIST"
nav_order: 5
description: >
    Lists all graph keys in the keyspace
parent: "Commands"
---

# GRAPH.LIST

Lists all graph keys in the keyspace.

## Examples

{% capture shell_0 %}
GRAPH.LIST
{% endcapture %}

{% capture python_0 %}
from falkordb import FalkorDB
client = FalkorDB()
graphs = client.list()
print(graphs)
{% endcapture %}

{% capture javascript_0 %}
import { FalkorDB } from 'falkordb';
const client = await FalkorDB.connect();
const graphs = await client.list();
console.log(graphs);
{% endcapture %}

{% capture java_0 %}
FalkorDB client = new FalkorDB();
List<String> graphs = client.list();
System.out.println(graphs);
{% endcapture %}

{% capture rust_0 %}
let client = FalkorDB::connect_default();
let graphs = client.list()?;
println!("{:?}", graphs);
{% endcapture %}

{% include code_tabs.html id="list_tabs" shell=shell_0 python=python_0 javascript=javascript_0 java=java_0 rust=rust_0 %}

### Sample Output

```sh
127.0.0.1:6379> GRAPH.LIST
2) G
3) resources
4) players
```
