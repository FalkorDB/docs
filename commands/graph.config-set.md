---
title: "GRAPH.CONFIG-SET"
description: >
    Updates a FalkorDB configuration
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';


# GRAPH.CONFIG-SET

Set the value of a FalkorDB configuration parameter.

Values set using `GRAPH.CONFIG SET` are not persisted after server restart.

FalkorDB configuration parameters are detailed [here](/configuration).

Note: As detailed in the link above, not all FalkorDB configuration parameters can be set at run-time.


<Tabs groupId="programming-language">
  <TabItem value="shell" label="Shell">

```bash
graph.config get TIMEOUT
graph.config set TIMEOUT 10000
graph.config get TIMEOUT
# Output:
# 1) "TIMEOUT"
# 2) (integer) 0
# OK
# 1) "TIMEOUT"
# 2) (integer) 10000
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
from falkordb import FalkorDB
client = FalkorDB()
print(client.get_config('TIMEOUT'))
client.set_config('TIMEOUT', 10000)
print(client.get_config('TIMEOUT'))
```

  </TabItem>
  <TabItem value="javascript" label="Javascript">

```javascript
import { FalkorDB } from 'falkordb';
const client = await FalkorDB.connect();
console.log(await client.getConfig('TIMEOUT'));
await client.setConfig('TIMEOUT', 10000);
console.log(await client.getConfig('TIMEOUT'));
```

  </TabItem>
  <TabItem value="java" label="Java">

```java
FalkorDB client = new FalkorDB();
System.out.println(client.getConfig("TIMEOUT"));
client.setConfig("TIMEOUT", 10000);
System.out.println(client.getConfig("TIMEOUT"));
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
let client = FalkorDB::connect_default();
println!("{:?}", client.get_config("TIMEOUT")?);
client.set_config("TIMEOUT", 10000)?;
println!("{:?}", client.get_config("TIMEOUT")?);
```

  </TabItem>
</Tabs>


<Tabs groupId="programming-language">
  <TabItem value="shell" label="Shell">

```bash
graph.config set THREAD_COUNT 10
# Output:
# (error) This configuration parameter cannot be set at run-time
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
try:
    client.set_config('THREAD_COUNT', 10)
except Exception as e:
    print(e)
```

  </TabItem>
  <TabItem value="javascript" label="Javascript">

```javascript
try {
  await client.setConfig('THREAD_COUNT', 10);
} catch (e) {
  console.error(e);
}
```

  </TabItem>
  <TabItem value="java" label="Java">

```java
try {
    client.setConfig("THREAD_COUNT", 10);
} catch (Exception e) {
    System.out.println(e);
}
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
if let Err(e) = client.set_config("THREAD_COUNT", 10) {
    println!("{}", e);
}
```

  </TabItem>
</Tabs>
