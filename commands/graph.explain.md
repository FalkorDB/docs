---
title: "GRAPH.EXPLAIN"
description: >
    Returns a query execution plan without running the query
---

# GRAPH.EXPLAIN

Constructs a query execution plan but does not run it. Inspect this execution plan to better
understand how your query will get executed.

Arguments: `Graph name, Query`

Returns: `String representation of a query execution plan`

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<Tabs groupId="programming-language">
  <TabItem value="shell" label="Shell">

```bash
GRAPH.EXPLAIN us_government "MATCH (p:President)-[:BORN]->(h:State {name:'Hawaii'}) RETURN p"
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
from falkordb import FalkorDB
client = FalkorDB()
graph = client.select_graph('us_government')
query = "MATCH (p:President)-[:BORN]->(h:State {name:'Hawaii'}) RETURN p"
result = graph.explain(query)
print(result)
```

  </TabItem>
  <TabItem value="javascript" label="Javascript">

```javascript
import { FalkorDB } from 'falkordb';
const client = await FalkorDB.connect();
const graph = client.selectGraph('us_government');
const query = "MATCH (p:President)-[:BORN]->(h:State {name:'Hawaii'}) RETURN p";
const result = await graph.explain(query);
console.log(result);
```

  </TabItem>
  <TabItem value="java" label="Java">

```java
FalkorDB client = new FalkorDB();
Graph graph = client.selectGraph("us_government");
String query = "MATCH (p:President)-[:BORN]->(h:State {name:'Hawaii'}) RETURN p";
String result = graph.explain(query);
System.out.println(result);
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
let client = FalkorDB::connect_default();
let graph = client.select_graph("us_government");
let query = r#"MATCH (p:President)-[:BORN]->(h:State {name:'Hawaii'}) RETURN p"#;
let result = graph.explain(query)?;
println!("{}", result);
```

  </TabItem>
</Tabs>
