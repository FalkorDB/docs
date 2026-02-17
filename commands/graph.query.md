---
title: "GRAPH.QUERY"
nav_order: 1
description: >
    Executes the given query against a specified graph
parent: "Commands"    
---

# GRAPH.QUERY

Executes the given query against a specified graph.

## Syntax

```
GRAPH.QUERY graph_name "query" [TIMEOUT timeout_value]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `graph_name` | string | Yes | The name of the graph to query |
| `query` | string | Yes | A Cypher query to execute against the graph |
| `TIMEOUT` | integer | No | Query timeout in milliseconds. Overrides the default timeout. Cannot exceed `TIMEOUT_MAX` configuration |

## Returns

Returns a [result set](/design/result-structure) containing:

1. **Header** - Column names corresponding to the RETURN clause
2. **Data rows** - Query results as nested arrays containing:
   - Scalar values (integers, strings, booleans, floats, null)
   - Graph entities (nodes with IDs, labels, and properties)
   - Relationships (edges with IDs, types, source/destination nodes, and properties)
   - Collections (arrays and paths)
3. **Metadata** - Query execution statistics including:
   - Query execution time
   - Number of entities created, deleted, or modified
   - Cache status

### Queries and Parameterized Queries

The execution plans of queries, both regular and parameterized, are cached (up to [CACHE_SIZE](/configuration#cache_size) unique queries are cached). Therefore, it is recommended to use parameterized queries when executing many queries with the same pattern but different constants.

Query-level timeouts can be set as described in [the configuration section](/configuration#timeout).

#### Command structure

`GRAPH.QUERY graph_name "query"`

example:

{% capture shell_0 %}
GRAPH.QUERY us_government "MATCH (p:president)-[:born]->(:state {name:'Hawaii'}) RETURN p"
{% endcapture %}

{% capture python_0 %}
graph.query("MATCH (p:president)-[:born]->(:state {name:'Hawaii'}) RETURN p")
{% endcapture %}

{% capture javascript_0 %}
const result = await graph.query("MATCH (p:president)-[:born]->(:state {name:'Hawaii'}) RETURN p");
console.log(result);
{% endcapture %}

{% capture java_0 %}
ResultSet result = graph.query("MATCH (p:president)-[:born]->(:state {name:'Hawaii'}) RETURN p");
System.out.println(result);
{% endcapture %}

{% capture rust_0 %}
let result = graph.query(r#"MATCH (p:president)-[:born]->(:state {name:'Hawaii'}) RETURN p"#).execute().await?;
println!("{:?}", result);
{% endcapture %}

{% include code_tabs.html id="tabs_0" shell=shell_0 python=python_0 javascript=javascript_0 java=java_0 rust=rust_0 %}


#### Parametrized query structure:

`GRAPH.QUERY graph_name "CYPHER param=val [param=val ...] query"`

example:

{% capture shell_1 %}
GRAPH.QUERY us_government "CYPHER state_name='Hawaii' MATCH (p:president)-[:born]->(:state {name:$state_name}) RETURN p"
{% endcapture %}

{% capture python_1 %}
graph.query("MATCH (p:president)-[:born]->(:state {name:$state_name}) RETURN p", {'state_name': 'Hawaii'})
{% endcapture %}

{% capture javascript_1 %}
const result = await graph.query(
  "MATCH (p:president)-[:born]->(:state {name:$state_name}) RETURN p",
  { params: { state_name: "Hawaii" } }
);
console.log(result);
{% endcapture %}

{% capture java_1 %}
Map<String, Object> params = new HashMap<>();
params.put("state_name", "Hawaii");
ResultSet result = graph.query(
  "MATCH (p:president)-[:born]->(:state {name:$state_name}) RETURN p",
  params
);
System.out.println(result);
{% endcapture %}

{% capture rust_1 %}
let params = std::collections::HashMap::from([
    ("state_name", "Hawaii")
]);
let result = graph.query_with_params(
    r#"MATCH (p:president)-[:born]->(:state {name:$state_name}) RETURN p"#,
    &params
).execute().await?;
println!("{:?}", result);
{% endcapture %}

{% include code_tabs.html id="tabs_1" shell=shell_1 python=python_1 javascript=javascript_1 java=java_1 rust=rust_1 %}

## Query Timeout

Queries can be given a timeout to prevent long-running operations from blocking server resources. The timeout is specified in milliseconds using the optional `TIMEOUT` parameter.

### Timeout Configuration

- **Per-Query Timeout**: Use the `TIMEOUT` parameter to set a timeout for a specific query
- **Default Timeout**: Configured globally using [`TIMEOUT_DEFAULT`](/getting-started/configuration#timeout_default)
- **Maximum Timeout**: Limited by [`TIMEOUT_MAX`](/getting-started/configuration#timeout_max) configuration

### Example

{% capture shell_2 %}
GRAPH.QUERY wikipedia "MATCH p=()-[*]->() RETURN p" TIMEOUT 500
{% endcapture %}

{% capture python_2 %}
# Timeout in milliseconds
graph.query("MATCH p=()-[*]->() RETURN p", timeout=500)
{% endcapture %}

{% capture javascript_2 %}
// Timeout in milliseconds
const result = await graph.query(
  "MATCH p=()-[*]->() RETURN p",
  { timeout: 500 }
);
{% endcapture %}

{% capture java_2 %}
// Timeout in milliseconds
ResultSet result = graph.query(
  "MATCH p=()-[*]->() RETURN p",
  500  // timeout
);
{% endcapture %}

{% capture rust_2 %}
// Timeout in milliseconds
let result = graph.query(r#"MATCH p=()-[*]->() RETURN p"#)
    .timeout(500)
    .execute()
    .await?;
{% endcapture %}

{% include code_tabs.html id="timeout_tabs" shell=shell_2 python=python_2 javascript=javascript_2 java=java_2 rust=rust_2 %}

When a query exceeds its timeout, it is aborted and returns an error: `(error) Query timed out`. For write queries, any changes to the graph are rolled back (which may take additional time).

## Write Operations

`GRAPH.QUERY` supports both read and write operations. Write operations modify the graph structure and include:

- **CREATE**: Create new nodes and relationships
- **SET**: Update properties on existing entities
- **DELETE**: Remove nodes and relationships
- **MERGE**: Create entities if they don't exist, or match existing ones
- **REMOVE**: Remove properties or labels from entities

### Write Query Example

{% capture shell_3 %}
GRAPH.QUERY social "CREATE (u:User {name: 'Alice', age: 30})-[:FRIENDS_WITH]->(v:User {name: 'Bob', age: 28})"
{% endcapture %}

{% capture python_3 %}
result = graph.query(
  "CREATE (u:User {name: $name, age: $age})-[:FRIENDS_WITH]->(v:User {name: $friend, age: $friend_age})",
  {'name': 'Alice', 'age': 30, 'friend': 'Bob', 'friend_age': 28}
)
# Check metadata for created entities
print(result.nodes_created, result.relationships_created)
{% endcapture %}

{% capture javascript_3 %}
const result = await graph.query(
  "CREATE (u:User {name: $name, age: $age})-[:FRIENDS_WITH]->(v:User {name: $friend, age: $friend_age})",
  { params: { name: 'Alice', age: 30, friend: 'Bob', friend_age: 28 } }
);
console.log(`Created ${result.getStatistics().nodesCreated} nodes`);
{% endcapture %}

{% capture java_3 %}
Map<String, Object> params = new HashMap<>();
params.put("name", "Alice");
params.put("age", 30);
params.put("friend", "Bob");
params.put("friend_age", 28);
ResultSet result = graph.query(
  "CREATE (u:User {name: $name, age: $age})-[:FRIENDS_WITH]->(v:User {name: $friend, age: $friend_age})",
  params
);
System.out.println("Nodes created: " + result.getStatistics().nodesCreated());
{% endcapture %}

{% capture rust_3 %}
let params = std::collections::HashMap::from([
    ("name", "Alice"),
    ("age", "30"),
    ("friend", "Bob"),
    ("friend_age", "28")
]);
let result = graph.query_with_params(
    r#"CREATE (u:User {name: $name, age: $age})-[:FRIENDS_WITH]->(v:User {name: $friend, age: $friend_age})"#,
    &params
).execute().await?;
println!("Nodes created: {}", result.nodes_created);
{% endcapture %}

{% include code_tabs.html id="write_tabs" shell=shell_3 python=python_3 javascript=javascript_3 java=java_3 rust=rust_3 %}

Write operations return metadata indicating the number of entities created, deleted, or modified. Unlike read-only queries (which can use [`GRAPH.RO_QUERY`](/commands/graph.ro-query)), write queries can timeout and will rollback changes when they do.

## Error Handling

Common errors when executing queries:

| Error | Description | Resolution |
|-------|-------------|------------|
| `Query timed out` | Query execution exceeded the timeout limit | Increase timeout, optimize query, or check for infinite loops |
| `Max pending queries exceeded` | Too many concurrent queries | Wait and retry, or increase `MAX_QUEUED_QUERIES` configuration |
| `Query's mem consumption exceeded capacity` | Query used too much memory | Optimize query or increase `QUERY_MEM_CAPACITY` configuration |
| `Syntax error` | Invalid Cypher syntax | Check query syntax against [Cypher documentation](/cypher) |
| `Unknown graph` | Graph does not exist | Create the graph first or check graph name |

### Example Error Handling

{% capture python_4 %}
from falkordb import FalkorDB
from redis.exceptions import ResponseError

client = FalkorDB()
graph = client.select_graph('my_graph')

try:
    result = graph.query("MATCH (n) RETURN n", timeout=1000)
except ResponseError as e:
    if "timed out" in str(e):
        print("Query timed out, try optimizing or increasing timeout")
    elif "Syntax error" in str(e):
        print("Invalid query syntax")
    else:
        print(f"Query error: {e}")
{% endcapture %}

{% capture javascript_4 %}
import { FalkorDB } from 'falkordb';

const client = await FalkorDB.connect();
const graph = client.selectGraph('my_graph');

try {
  const result = await graph.query("MATCH (n) RETURN n", { timeout: 1000 });
} catch (error) {
  if (error.message.includes('timed out')) {
    console.log('Query timed out, try optimizing or increasing timeout');
  } else if (error.message.includes('Syntax error')) {
    console.log('Invalid query syntax');
  } else {
    console.error('Query error:', error.message);
  }
}
{% endcapture %}

{% capture java_4 %}
import com.falkordb.FalkorDB;
import com.falkordb.Graph;
import com.falkordb.ResultSet;
import redis.clients.jedis.exceptions.JedisDataException;

FalkorDB client = new FalkorDB();
Graph graph = client.selectGraph("my_graph");

try {
    ResultSet result = graph.query("MATCH (n) RETURN n", 1000);
} catch (JedisDataException e) {
    String message = e.getMessage();
    if (message.contains("timed out")) {
        System.out.println("Query timed out, try optimizing or increasing timeout");
    } else if (message.contains("Syntax error")) {
        System.out.println("Invalid query syntax");
    } else {
        System.err.println("Query error: " + message);
    }
}
{% endcapture %}

{% capture rust_4 %}
use falkordb::{FalkorDB, FalkorDBError};

let client = FalkorDB::connect_default();
let graph = client.select_graph("my_graph");

match graph.query(r#"MATCH (n) RETURN n"#).timeout(1000).execute().await {
    Ok(result) => println!("Query succeeded"),
    Err(e) => {
        let error_msg = e.to_string();
        if error_msg.contains("timed out") {
            println!("Query timed out, try optimizing or increasing timeout");
        } else if error_msg.contains("Syntax error") {
            println!("Invalid query syntax");
        } else {
            eprintln!("Query error: {}", error_msg);
        }
    }
}
{% endcapture %}

{% include code_tabs.html id="error_tabs" python=python_4 javascript=javascript_4 java=java_4 rust=rust_4 %}

## Query Language

The syntax is based on [Cypher](http://www.opencypher.org/). [Most](/cypher/cypher-support) of the language is supported. See [Cypher documentation](/cypher).