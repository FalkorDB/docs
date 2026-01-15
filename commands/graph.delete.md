---
title: "GRAPH.DELETE"
description: >
    Completely removes the graph and all of its entities
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';


# GRAPH.DELETE

Completely removes a graph and all of its entities (nodes and relationships).

## Syntax

```
GRAPH.DELETE graph_name
```

**Arguments:**
- `graph_name` - Name of the graph to delete

**Returns:** String indicating if the operation succeeded or failed.

## Examples


<Tabs groupId="programming-language">
  <TabItem value="shell" label="Shell">

```bash
GRAPH.DELETE us_government
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
graph.delete()
```

  </TabItem>
  <TabItem value="javascript" label="Javascript">

```javascript
await graph.delete();
```

  </TabItem>
  <TabItem value="java" label="Java">

```java
graph.delete();
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
graph.delete()?;
```

  </TabItem>
</Tabs>

## Deleting Individual Nodes

**Note:** To delete specific nodes or relationships (not the entire graph), use the Cypher `DELETE` clause with a `MATCH` query:


<Tabs groupId="programming-language">
  <TabItem value="shell" label="Shell">

```bash
GRAPH.QUERY DEMO_GRAPH "MATCH (x:Y {propname: propvalue}) DELETE x"
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
graph.query("MATCH (x:Y {propname: propvalue}) DELETE x")
```

  </TabItem>
  <TabItem value="javascript" label="Javascript">

```javascript
await graph.query("MATCH (x:Y {propname: propvalue}) DELETE x");
```

  </TabItem>
  <TabItem value="java" label="Java">

```java
graph.query("MATCH (x:Y {propname: propvalue}) DELETE x");
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
graph.query("MATCH (x:Y {propname: propvalue}) DELETE x")?;
```

  </TabItem>
</Tabs>

**⚠️ Warning:** When you delete a node using the Cypher `DELETE` clause, all of the node's incoming and outgoing relationships are also automatically removed.

