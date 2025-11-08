---
title: "GRAPH.CONFIG-GET"
description: >
    Retrieves a FalkorDB configuration
parent: "Commands"
---

# GRAPH.CONFIG-GET

Retrieves the current value of a FalkorDB configuration parameter.

FalkorDB configuration parameters are detailed [here](/configuration).

`*` can be used to retrieve the value of all FalkorDB configuration parameters.

{% capture shell_0 %}
graph.config get *

# Output

# 1) 1) "TIMEOUT"

# 2) (integer) 0

# 

{% endcapture %}

{% capture python_0 %}
from falkordb import FalkorDB
client = FalkorDB()
config = client.get_config('*')
print(config)
{% endcapture %}

{% capture javascript_0 %}
import { FalkorDB } from 'falkordb';
const client = await FalkorDB.connect();
const config = await client.getConfig('*');
console.log(config);
{% endcapture %}

{% capture java_0 %}
FalkorDB client = new FalkorDB();
Map<String, Object> config = client.getConfig("*");
System.out.println(config);
{% endcapture %}

{% capture rust_0 %}
let client = FalkorDB::connect_default();
let config = client.get_config("*")?;
println!("{:?}", config);
{% endcapture %}

{% include code_tabs.html id="config_get_tabs" shell=shell_0 python=python_0 javascript=javascript_0 java=java_0 rust=rust_0 %}

{% capture shell_1 %}
graph.config get TIMEOUT

# Output

# 1) "TIMEOUT"

# 2) (integer) 0

{% endcapture %}

{% capture python_1 %}
timeout = client.get_config('TIMEOUT')
print(timeout)
{% endcapture %}

{% capture javascript_1 %}
const timeout = await client.getConfig('TIMEOUT');
console.log(timeout);
{% endcapture %}

{% capture java_1 %}
Object timeout = client.getConfig("TIMEOUT");
System.out.println(timeout);
{% endcapture %}

{% capture rust_1 %}
let timeout = client.get_config("TIMEOUT")?;
println!("{:?}", timeout);
{% endcapture %}

{% include code_tabs.html id="config_get_timeout_tabs" shell=shell_1 python=python_1 javascript=javascript_1 java=java_1 rust=rust_1 %}
