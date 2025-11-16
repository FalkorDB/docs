---
title: "GRAPH.INFO"
description: >
    Returns information and statistics about the current executing commands
parent: "Commands"
---

# GRAPH.INFO

Returns information and statistics about currently running and waiting queries.

## Syntax

```
GRAPH.INFO [RunningQueries | WaitingQueries]
```

If no argument is provided, both running and waiting queries are returned.

## Examples

### Get all query information

{% capture shell_0 %}
GRAPH.INFO
{% endcapture %}

{% capture python_0 %}
from falkordb import FalkorDB
client = FalkorDB()
info = client.info()
print(info)
{% endcapture %}

{% capture javascript_0 %}
import { FalkorDB } from 'falkordb';
const client = await FalkorDB.connect();
const info = await client.info();
console.log(info);
{% endcapture %}

{% capture java_0 %}
FalkorDB client = new FalkorDB();
String info = client.info();
System.out.println(info);
{% endcapture %}

{% capture rust_0 %}
let client = FalkorDB::connect_default();
let info = client.info()?;
println!("{}", info);
{% endcapture %}

{% include code_tabs.html id="info_all_tabs" shell=shell_0 python=python_0 javascript=javascript_0 java=java_0 rust=rust_0 %}

### Get running queries

{% capture shell_1 %}
GRAPH.INFO RunningQueries
{% endcapture %}

{% capture python_1 %}
info = client.info("RunningQueries")
print(info)
{% endcapture %}

{% capture javascript_1 %}
const info = await client.info("RunningQueries");
console.log(info);
{% endcapture %}

{% capture java_1 %}
String info = client.info("RunningQueries");
System.out.println(info);
{% endcapture %}

{% capture rust_1 %}
let info = client.info("RunningQueries")?;
println!("{}", info);
{% endcapture %}

{% include code_tabs.html id="info_running_tabs" shell=shell_1 python=python_1 javascript=javascript_1 java=java_1 rust=rust_1 %}

### Get waiting queries

{% capture shell_2 %}
GRAPH.INFO WaitingQueries
{% endcapture %}

{% capture python_2 %}
info = client.info("WaitingQueries")
print(info)
{% endcapture %}

{% capture javascript_2 %}
const info = await client.info("WaitingQueries");
console.log(info);
{% endcapture %}

{% capture java_2 %}
String info = client.info("WaitingQueries");
System.out.println(info);
{% endcapture %}

{% capture rust_2 %}
let info = client.info("WaitingQueries")?;
println!("{}", info);
{% endcapture %}

{% include code_tabs.html id="info_waiting_tabs" shell=shell_2 python=python_2 javascript=javascript_2 java=java_2 rust=rust_2 %}

### Sample Output

```sh
127.0.0.1:6379> GRAPH.INFO
1) "# Running queries"
2) (empty array)
3) "# Waiting queries"
4) (empty array)
```
