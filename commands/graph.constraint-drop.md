---
title: "GRAPH.CONSTRAINT DROP"
description: >
    Deletes a constraint from specified graph
---

# GRAPH.CONSTRAINT DROP

---
syntax: |
  GRAPH.CONSTRAINT DROP key 
    MANDATORY|UNIQUE
    NODE label | RELATIONSHIP reltype
    PROPERTIES propCount prop [prop...]  
---

Deleted a graph constraint.

[Examples](#examples)

For an introduction to constraints see [GRAPH.CONSTRAINT CREATE](/commands/graph.constraint-create)

## Required arguments

<details open><summary><code>key</code></summary>

is key name for the graph.
</details>

<details open><summary><code>constraintType</code></summary>

is the constraint type: either `MANDATORY` or `UNIQUE`.

</details>

<details open><summary><code>NODE label | RELATIONSHIP reltype</code></summary>
  
is the graph entity type (`NODE` or `RELATIONSHIP`) and the name of the node label or relationship type on which the constraint is enforced.

</details>

<details open><summary><code>propCount</code></summary>

is the number of properties following. Valid values are between 1 and 255.

</details>

<details open><summary><code>prop...</code></summary>

is a list of `propCount` property names.

</details>

## Return value

@simple-string-reply - `OK` if executed correctly, or @error-reply otherwise.

## Examples

To delete a unique constraint for all nodes with label `Person` enforcing uniqueness on the combination of values of attributes `first_name` and `last_name`, issue the following command:

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<Tabs groupId="programming-language">
  <TabItem value="shell" label="Shell">

```bash
redis> GRAPH.CONSTRAINT DROP g UNIQUE NODE Person PROPERTIES 2 first_name last_name
# Output: OK
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
from falkordb import FalkorDB
client = FalkorDB()
result = client.drop_constraint('g', 'UNIQUE', 'NODE', 'Person', ['first_name', 'last_name'])
print(result)
```

  </TabItem>
  <TabItem value="javascript" label="Javascript">

```javascript
import { FalkorDB } from 'falkordb';
const client = await FalkorDB.connect();
const result = await client.dropConstraint('g', 'UNIQUE', 'NODE', 'Person', ['first_name', 'last_name']);
console.log(result);
```

  </TabItem>
  <TabItem value="java" label="Java">

```java
FalkorDB client = new FalkorDB();
String result = client.dropConstraint("g", "UNIQUE", "NODE", "Person", Arrays.asList("first_name", "last_name"));
System.out.println(result);
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
let client = FalkorDB::connect_default();
let result = client.drop_constraint("g", "UNIQUE", "NODE", "Person", &["first_name", "last_name"])?;
println!("{}", result);
```

  </TabItem>
</Tabs>
