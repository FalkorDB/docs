---
title: "Social Network Tutorial"
description: "Build and query a small social network graph with FalkorDB."
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<!-- markdownlint-disable MD025 MD033 -->

# Social Network Tutorial

This tutorial walks through creating a small social graph, running core Cypher queries, and reusing the same statements across FalkorDB clients.

## 1) Create the graph

Use Cypher to seed users, friendships, and posts:

```cypher
CREATE (alice:User {id: 1, name: "Alice", email: "alice@example.com"})
CREATE (bob:User {id: 2, name: "Bob", email: "bob@example.com"})
CREATE (charlie:User {id: 3, name: "Charlie", email: "charlie@example.com"})

CREATE (post1:Post {id: 101, content: "Hello World!", date: 1701388800})
CREATE (post2:Post {id: 102, content: "Graph Databases are awesome!", date: 1701475200})

CREATE (alice)-[:FRIENDS_WITH {since: 1640995200}]->(bob)
CREATE (bob)-[:FRIENDS_WITH {since: 1684108800}]->(charlie)
CREATE (alice)-[:CREATED {time: 1701388800}]->(post1)
CREATE (bob)-[:CREATED {time: 1701475200}]->(post2)
```

## 2) Query the graph from your client

<Tabs groupId="programming-language">
  <TabItem value="python" label="Python">

```python
from falkordb import FalkorDB

client = FalkorDB(host="localhost", port=6379, password="your-password")
graph = client.select_graph("social")

result = graph.ro_query(
    """
MATCH (alice:User {name: 'Alice'})-[:FRIENDS_WITH]->(friend)
RETURN friend.name AS Friend
"""
).result_set

for row in result:
    print(row[0])
```

  </TabItem>
  <TabItem value="javascript" label="JavaScript">

```javascript
import { FalkorDB } from "falkordb";

const client = await FalkorDB.connect({ host: "localhost", port: 6379, password: "your-password" });
const graph = client.selectGraph("social");

const result = await graph.ro_query(`
  MATCH (alice:User {name: 'Alice'})-[:FRIENDS_WITH]->(friend)
  RETURN friend.name AS Friend
`);

for (const row of result) {
  console.log(row["Friend"]);
}
```

  </TabItem>
  <TabItem value="java" label="Java">

```java
import com.falkordb.*;

Driver driver = FalkorDB.driver("localhost", 6379);
Graph graph = driver.graph("social");

String query = """
MATCH (alice:User {name: 'Alice'})-[:FRIENDS_WITH]->(friend)
RETURN friend.name AS Friend
""";

ResultSet rows = graph.readOnlyQuery(query);
rows.forEach(row -> System.out.println(row.get("Friend")));
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
use falkordb::{FalkorClientBuilder, FalkorConnectionInfo};

let info: FalkorConnectionInfo = "falkor://127.0.0.1:6379".try_into()?;
let client = FalkorClientBuilder::new().with_connection_info(info).build()?;
let mut graph = client.select_graph("social");

let query = r#"
MATCH (alice:User {name: 'Alice'})-[:FRIENDS_WITH]->(friend)
RETURN friend.name AS Friend
"#;

let result = graph.ro_query(query).execute().await?;
for row in result.data.by_ref() {
    println!("{}", row["Friend"]);
}
```

  </TabItem>
</Tabs>

## 3) Next steps

- Add likes, comments, and groups to exercise more complex patterns.
- Experiment with `GRAPH.PROFILE` to see how indexes affect plan shape.
- Continue with the broader [Getting Started guide](/getting-started/index) for deployment and client setup details.
