---
title: "GRAPH.CONFIG-SET"
description: >
    Updates a FalkorDB configuration
parent: "Commands"
nav_order: 7
---

# GRAPH.CONFIG-SET

Set the value of a FalkorDB configuration parameter.

Values set using `GRAPH.CONFIG SET` are not persisted after server restart.

FalkorDB configuration parameters are detailed [here](/configuration).

Note: As detailed in the link above, not all FalkorDB configuration parameters can be set at run-time.

{% capture shell_0 %}
graph.config get TIMEOUT
graph.config set TIMEOUT 10000
graph.config get TIMEOUT
# Output:
# 1) "TIMEOUT"
# 2) (integer) 0
# OK
# 1) "TIMEOUT"
# 2) (integer) 10000
{% endcapture %}

{% capture python_0 %}
from falkordb import FalkorDB
client = FalkorDB()
print(client.get_config('TIMEOUT'))
client.set_config('TIMEOUT', 10000)
print(client.get_config('TIMEOUT'))
{% endcapture %}

{% capture javascript_0 %}
import { FalkorDB } from 'falkordb';
const client = await FalkorDB.connect();
console.log(await client.getConfig('TIMEOUT'));
await client.setConfig('TIMEOUT', 10000);
console.log(await client.getConfig('TIMEOUT'));
{% endcapture %}

{% capture java_0 %}
FalkorDB client = new FalkorDB();
System.out.println(client.getConfig("TIMEOUT"));
client.setConfig("TIMEOUT", 10000);
System.out.println(client.getConfig("TIMEOUT"));
{% endcapture %}

{% capture rust_0 %}
let client = FalkorDB::connect_default();
println!("{:?}", client.get_config("TIMEOUT")?);
client.set_config("TIMEOUT", 10000)?;
println!("{:?}", client.get_config("TIMEOUT")?);
{% endcapture %}

{% include code_tabs.html id="config_set_tabs" shell=shell_0 python=python_0 javascript=javascript_0 java=java_0 rust=rust_0 %}

{% capture shell_1 %}
graph.config set THREAD_COUNT 10
# Output:
# (error) This configuration parameter cannot be set at run-time
{% endcapture %}

{% capture python_1 %}
try:
    client.set_config('THREAD_COUNT', 10)
except Exception as e:
    print(e)
{% endcapture %}

{% capture javascript_1 %}
try {
  await client.setConfig('THREAD_COUNT', 10);
} catch (e) {
  console.error(e);
}
{% endcapture %}

{% capture java_1 %}
try {
    client.setConfig("THREAD_COUNT", 10);
} catch (Exception e) {
    System.out.println(e);
}
{% endcapture %}

{% capture rust_1 %}
if let Err(e) = client.set_config("THREAD_COUNT", 10) {
    println!("{}", e);
}
{% endcapture %}

{% include code_tabs.html id="config_set_error_tabs" shell=shell_1 python=python_1 javascript=javascript_1 java=java_1 rust=rust_1 %}
