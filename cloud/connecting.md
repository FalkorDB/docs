---
title: "Connecting to FalkorDB Cloud"
parent: "Cloud DBaaS"
nav_order: 6
description: "Step-by-step guide for connecting to FalkorDB Cloud using Python, Node.js, Java, Rust, Go, and redis-cli. Covers endpoint URL, TLS, authentication, and Bolt protocol connections."
---

# Connecting to FalkorDB Cloud

This guide walks you through obtaining your connection details from the FalkorDB Cloud dashboard and connecting using each supported client library.

---

## 1. Obtain Your Connection Details

After creating a FalkorDB Cloud instance:

1. Log in to the [FalkorDB Cloud Dashboard](https://app.falkordb.cloud)
2. Select your instance
3. Copy the **connection URL** from the instance details panel

Your connection URL follows this format:

```
falkordb://<username>:<password>@<host>:<port>
```

**Key details:**
- **Host** — Your instance's hostname (e.g., `my-instance-abc123.falkordb.cloud`)
- **Port** — Typically `6379`
- **Username / Password** — The credentials you set when creating the instance
- **TLS** — Enabled by default on Startup, Pro, and Enterprise tiers

> **Free Tier:** TLS is not available on the Free tier. Use `redis://` (unencrypted) connections.

---

## 2. Connect with Client Libraries

### Python

```bash
pip install falkordb
```

```python
from falkordb import FalkorDB

# TLS connection (Startup / Pro / Enterprise)
db = FalkorDB(
    host='my-instance.falkordb.cloud',
    port=6379,
    username='default',
    password='your-password',
    ssl=True
)

graph = db.select_graph('myGraph')
result = graph.query("MATCH (n) RETURN n LIMIT 5")
for record in result.result_set:
    print(record)
```

For the Free tier (no TLS):

```python
db = FalkorDB(
    host='my-instance.falkordb.cloud',
    port=6379,
    username='default',
    password='your-password'
)
```

### Node.js

```bash
npm install falkordb
```

```javascript
import { FalkorDB } from 'falkordb';

const db = await FalkorDB.connect({
    username: 'default',
    password: 'your-password',
    socket: {
        host: 'my-instance.falkordb.cloud',
        port: 6379,
        tls: true
    }
});

const graph = db.selectGraph('myGraph');
const result = await graph.query("MATCH (n) RETURN n LIMIT 5");
console.log(result);

await db.close();
```

### Java

```xml
<dependency>
    <groupId>com.falkordb</groupId>
    <artifactId>jfalkordb</artifactId>
    <version>0.5.0</version>
</dependency>
```

```java
import com.falkordb.FalkorDB;
import com.falkordb.Graph;

FalkorDB db = FalkorDB.driver()
    .host("my-instance.falkordb.cloud")
    .port(6379)
    .user("default")
    .password("your-password")
    .ssl(true)
    .build();

Graph graph = db.selectGraph("myGraph");
var result = graph.query("MATCH (n) RETURN n LIMIT 5");
```

### Rust

```toml
[dependencies]
falkordb = "0.3"
```

```rust
use falkordb::FalkorDB;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let db = FalkorDB::connect_async(
        "falkordb://default:your-password@my-instance.falkordb.cloud:6379?ssl=true"
    ).await?;

    let graph = db.select_graph("myGraph");
    let result = graph.query("MATCH (n) RETURN n LIMIT 5").execute().await?;
    println!("{:?}", result);

    Ok(())
}
```

### Go

```go
package main

import (
    "fmt"
    "github.com/FalkorDB/falkordb-go"
)

func main() {
    db, err := falkordb.Connect(
        "my-instance.falkordb.cloud:6379",
        falkordb.WithAuth("default", "your-password"),
        falkordb.WithTLS(nil),
    )
    if err != nil {
        panic(err)
    }

    graph := db.SelectGraph("myGraph")
    result, err := graph.Query("MATCH (n) RETURN n LIMIT 5")
    if err != nil {
        panic(err)
    }
    fmt.Println(result)
}
```

### redis-cli

```bash
# TLS connection
redis-cli -h my-instance.falkordb.cloud -p 6379 \
  --user default --pass your-password --tls \
  GRAPH.QUERY myGraph "MATCH (n) RETURN n LIMIT 5"

# Free tier (no TLS)
redis-cli -h my-instance.falkordb.cloud -p 6379 \
  --user default --pass your-password \
  GRAPH.QUERY myGraph "MATCH (n) RETURN n LIMIT 5"
```

---

## 3. Bolt Protocol

FalkorDB Cloud also supports the [Bolt protocol](/integration/bolt-support), commonly used by Neo4j-compatible tools and drivers.

Connect using Bolt on port **7687**:

```
bolt://my-instance.falkordb.cloud:7687
```

This allows you to use tools like Neo4j Desktop, Neo4j Browser, or any Bolt-compatible driver with your FalkorDB Cloud instance.

---

## Troubleshooting

| Issue | Solution |
|:---|:---|
| `Connection refused` | Verify the hostname and port; check your instance is running in the dashboard |
| `SSL/TLS error` | Ensure you're using TLS for paid tiers; Free tier does not support TLS |
| `Authentication failed` | Double-check username and password; reset credentials in the dashboard if needed |
| `Timeout` | Check network connectivity; ensure your firewall allows outbound connections on port 6379 |

For more help, see the [Troubleshooting guide](/operations/troubleshooting) or contact [FalkorDB Support](https://www.falkordb.com/contact-us/).

---

## Related Pages

- [Client Libraries](/getting-started/clients) — Full list of official and community clients
- [Getting Started](/getting-started) — Local setup and first queries
- [Cloud Overview](/cloud) — FalkorDB Cloud tiers and features
- [Bolt Support](/integration/bolt-support) — Bolt protocol details
