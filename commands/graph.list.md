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
db = FalkorDB(host='localhost', port=6379)
graphs = db.list_graphs()
print(graphs)
{% endcapture %}

{% capture javascript_0 %}
import { FalkorDB } from 'falkordb';
const db = await FalkorDB.connect({
  socket: { host: 'localhost', port: 6379 }
});
const graphs = await db.list();
console.log(graphs);
{% endcapture %}

{% capture java_0 %}
import com.falkordb.*;

Driver driver = FalkorDB.driver("localhost", 6379);
List<String> graphs = driver.listGraphs();
System.out.println(graphs);
{% endcapture %}

{% capture rust_0 %}
use falkordb::{FalkorClientBuilder, FalkorConnectionInfo};

let connection_info: FalkorConnectionInfo = "falkor://127.0.0.1:6379"
    .try_into()
    .expect("Invalid connection info");
let client = FalkorClientBuilder::new()
    .with_connection_info(connection_info)
    .build()
    .expect("Failed to build client");
let graphs = client.list_graphs();
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

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="Does GRAPH.LIST require a graph name argument?"
  a1="No. `GRAPH.LIST` takes no arguments. It scans the entire keyspace and returns all keys that contain graph data."
  q2="Does GRAPH.LIST return graphs from all databases?"
  a2="No. `GRAPH.LIST` only returns graph keys from the currently selected Redis database (the one selected with the `SELECT` command)."
  q3="What is returned if no graphs exist?"
  a3="An empty array is returned if no graph keys exist in the current keyspace."
  q4="Are internal telemetry graphs included in the output?"
  a4="Yes. Internal telemetry graphs (e.g., `telemetry{A}`) may appear in the list. These are automatically created by FalkorDB for internal tracking purposes."
%}
