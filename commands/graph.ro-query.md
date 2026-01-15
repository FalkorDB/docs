---
title: "GRAPH.RO_QUERY"
description: >
    Executes a given read only query against a specified graph
---

# GRAPH.RO_QUERY

Executes a given read only query against a specified graph.

Arguments: `Graph name, Query, Timeout [optional]`

Returns: [Result set](/design/result-structure) for a read only query or an error if a write query was given.

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<Tabs groupId="programming-language">
  <TabItem value="shell" label="Shell">

```bash
GRAPH.RO_QUERY us_government "MATCH (p:president)-[:born]->(:state {name:'Hawaii'}) RETURN p"
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
graph.ro_query("MATCH (p:president)-[:born]->(:state {name:'Hawaii'}) RETURN p")
```

  </TabItem>
  <TabItem value="javascript" label="Javascript">

```javascript
const result = await graph.ro_query("MATCH (p:president)-[:born]->(:state {name:'Hawaii'}) RETURN p");
console.log(result);
```

  </TabItem>
  <TabItem value="java" label="Java">

```java
ResultSet result = graph.readOnlyQuery("MATCH (p:president)-[:born]->(:state {name:'Hawaii'}) RETURN p");
System.out.println(result);
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
let result = graph.ro_query(r#"MATCH (p:president)-[:born]->(:state {name:'Hawaii'}) RETURN p"#).execute().await?;
println!("{:?}", result);
```

  </TabItem>
</Tabs>

Query-level timeouts can be set as described in [the configuration section](/configuration#timeout).
