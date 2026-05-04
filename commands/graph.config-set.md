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

Multiple parameters can be set in a single command:

```sh
GRAPH.CONFIG SET key1 val1 key2 val2 ...
```

{% capture shell_0 %}
graph.config get TIMEOUT_DEFAULT
graph.config set TIMEOUT_DEFAULT 10000
graph.config get TIMEOUT_DEFAULT
# Output:
# 1) "TIMEOUT_DEFAULT"
# 2) (integer) 0
# OK
# 1) "TIMEOUT_DEFAULT"
# 2) (integer) 10000
{% endcapture %}

{% capture python_0 %}
from falkordb import FalkorDB
client = FalkorDB()
print(client.get_config('TIMEOUT_DEFAULT'))
client.set_config('TIMEOUT_DEFAULT', 10000)
print(client.get_config('TIMEOUT_DEFAULT'))
{% endcapture %}

{% capture javascript_0 %}
import { FalkorDB } from 'falkordb';
const client = await FalkorDB.connect();
console.log(await client.getConfig('TIMEOUT_DEFAULT'));
await client.setConfig('TIMEOUT_DEFAULT', 10000);
console.log(await client.getConfig('TIMEOUT_DEFAULT'));
{% endcapture %}

{% capture java_0 %}
FalkorDB client = new FalkorDB();
System.out.println(client.getConfig("TIMEOUT_DEFAULT"));
client.setConfig("TIMEOUT_DEFAULT", 10000);
System.out.println(client.getConfig("TIMEOUT_DEFAULT"));
{% endcapture %}

{% capture rust_0 %}
let client = FalkorDB::connect_default();
println!("{:?}", client.get_config("TIMEOUT_DEFAULT")?);
client.set_config("TIMEOUT_DEFAULT", 10000)?;
println!("{:?}", client.get_config("TIMEOUT_DEFAULT")?);
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

{% include faq_accordion.html title="Frequently Asked Questions" q1="Are configuration changes persisted after a server restart?" a1="No. Values set using `GRAPH.CONFIG SET` are **not persisted** after server restart. To make changes permanent, update the server configuration file or use startup arguments." q2="Can all configuration parameters be changed at runtime?" a2="No. Some parameters like `THREAD_COUNT` can only be set at server startup. Attempting to change them at runtime will return an error: 'This configuration parameter cannot be set at run-time'." q3="Can I set multiple configuration parameters in a single command?" a3="Yes. You can set multiple parameters at once: `GRAPH.CONFIG SET key1 val1 key2 val2 ...`" q4="What happens if I set an invalid value?" a4="The command will return an error and the configuration parameter will retain its previous value. No partial changes are applied." %}
