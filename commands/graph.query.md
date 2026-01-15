---
title: "GRAPH.QUERY"
description: >
    Executes the given query against a specified graph
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<!-- markdownlint-disable MD033 -->


# GRAPH.QUERY

Executes the given query against a specified graph.

Arguments: `Graph name, Query, Timeout [optional]`

Returns: [Result set](/design/result-structure)

## Queries and Parameterized Queries

The execution plans of queries, both regular and parameterized, are cached (up to [CACHE_SIZE](/configuration#cache_size) unique queries are cached). Therefore, it is recommended to use parameterized queries when executing many queries with the same pattern but different constants.

Query-level timeouts can be set as described in [the configuration section](/configuration#timeout).

### Command structure

Use client libraries to send Cypher, rather than invoking `GRAPH.QUERY` directly. The raw Cypher pattern stays the same across languages:

<Tabs groupId="programming-language">
  <TabItem value="cypher" label="Cypher">

```cypher
MATCH (p:president)-[:born]->(:state {name:'Hawaii'})
RETURN p
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
graph.query("""
MATCH (p:president)-[:born]->(:state {name:'Hawaii'})
RETURN p
""")
```

  </TabItem>
  <TabItem value="javascript" label="JavaScript">

```javascript
const result = await graph.query(`
  MATCH (p:president)-[:born]->(:state {name:'Hawaii'})
  RETURN p
`);
console.log(result);
```

  </TabItem>
  <TabItem value="java" label="Java">

```java
ResultSet result = graph.query("""
MATCH (p:president)-[:born]->(:state {name:'Hawaii'})
RETURN p
""");
System.out.println(result);
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
let result = graph
    .query(
        r#"
MATCH (p:president)-[:born]->(:state {name:'Hawaii'})
RETURN p
"#,
    )
    .execute()
    .await?;
println!("{:?}", result);
```

  </TabItem>
</Tabs>

### Parameterized query structure

Use named parameters to let the server cache query plans while varying values. The Cypher stays the same across clients:

<Tabs groupId="programming-language">
  <TabItem value="cypher" label="Cypher">

```cypher
MATCH (p:president)-[:born]->(:state {name:$state_name})
RETURN p
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
graph.query(
    """
MATCH (p:president)-[:born]->(:state {name:$state_name})
RETURN p
""",
    {"state_name": "Hawaii"},
)
```

  </TabItem>
  <TabItem value="javascript" label="JavaScript">

```javascript
const result = await graph.query(
  `
  MATCH (p:president)-[:born]->(:state {name:$state_name})
  RETURN p
  `,
  { params: { state_name: "Hawaii" } }
);
console.log(result);
```

  </TabItem>
  <TabItem value="java" label="Java">

```java
Map<String, Object> params = new HashMap<>();
params.put("state_name", "Hawaii");
ResultSet result = graph.query(
    """
MATCH (p:president)-[:born]->(:state {name:$state_name})
RETURN p
""",
    params
);
System.out.println(result);
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
let params = std::collections::HashMap::from([(String::from("state_name"), "Hawaii")]);
let result = graph
    .query_with_params(
        r#"
MATCH (p:president)-[:born]->(:state {name:$state_name})
RETURN p
"#,
        &params,
    )
    .execute()
    .await?;
println!("{:?}", result);
```

  </TabItem>
</Tabs>

### Query language

The syntax is based on [Cypher](http://www.opencypher.org/). [Most](/cypher/cypher-support) of the language is supported. See [Cypher documentation](/cypher).
