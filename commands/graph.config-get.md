---
title: "GRAPH.CONFIG-GET"
description: >
    Retrieves a FalkorDB configuration
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';


# GRAPH.CONFIG-GET

Retrieves the current value of a FalkorDB configuration parameter.

FalkorDB configuration parameters are detailed [here](/configuration).

`*` can be used to retrieve the value of all FalkorDB configuration parameters.


<Tabs groupId="programming-language">
  <TabItem value="shell" label="Shell">

```bash
graph.config get *
# Output:
# 1) 1) "TIMEOUT"
#    2) (integer) 0
# ...
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
from falkordb import FalkorDB
client = FalkorDB()
config = client.get_config('*')
print(config)
```

  </TabItem>
  <TabItem value="javascript" label="Javascript">

```javascript
import { FalkorDB } from 'falkordb';
const client = await FalkorDB.connect();
const config = await client.getConfig('*');
console.log(config);
```

  </TabItem>
  <TabItem value="java" label="Java">

```java
FalkorDB client = new FalkorDB();
Map<String, Object> config = client.getConfig("*");
System.out.println(config);
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
let client = FalkorDB::connect_default();
let config = client.get_config("*")?;
println!("{:?}", config);
```

  </TabItem>
</Tabs>


<Tabs groupId="programming-language">
  <TabItem value="shell" label="Shell">

```bash
graph.config get TIMEOUT
# Output:
# 1) "TIMEOUT"
# 2) (integer) 0
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
timeout = client.get_config('TIMEOUT')
print(timeout)
```

  </TabItem>
  <TabItem value="javascript" label="Javascript">

```javascript
const timeout = await client.getConfig('TIMEOUT');
console.log(timeout);
```

  </TabItem>
  <TabItem value="java" label="Java">

```java
Object timeout = client.getConfig("TIMEOUT");
System.out.println(timeout);
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
let timeout = client.get_config("TIMEOUT")?;
println!("{:?}", timeout);
```

  </TabItem>
</Tabs>
