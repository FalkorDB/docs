---
title: "GRAPH.SLOWLOG"
description: >
    Returns a list containing up to 10 of the slowest queries issued against the given graph
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';


# GRAPH.SLOWLOG

Returns a list containing up to 10 of the slowest queries issued against the given graph ID.

Each item in the list has the following structure:

1. A Unix timestamp at which the log entry was processed.
2. The issued command.
3. The issued query.
4. The amount of time needed for its execution, in milliseconds.

## Examples

### Get slowlog


<Tabs groupId="programming-language">
  <TabItem value="shell" label="Shell">

```bash
GRAPH.SLOWLOG graph_id
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
from falkordb import FalkorDB
db = FalkorDB(host='localhost', port=6379)
graph = db.select_graph('graph_id')
slowlog = graph.slowlog()
print(slowlog)
```

  </TabItem>
  <TabItem value="javascript" label="Javascript">

```javascript
import { FalkorDB } from 'falkordb';
const db = await FalkorDB.connect({
  socket: { host: 'localhost', port: 6379 }
});
const graph = db.selectGraph('graph_id');
const slowlog = await graph.slowLog();
console.log(slowlog);
```

  </TabItem>
</Tabs>

### Sample Output

```sh
GRAPH.SLOWLOG graph_id
 1) 1) "1581932396"
    2) "GRAPH.QUERY"
    3) "MATCH (a:Person)-[:FRIEND]->(e) RETURN e.name"
    4) "0.831"
 2) 1) "1581932396"
    2) "GRAPH.QUERY"
    3) "MATCH (me:Person)-[:FRIEND]->(:Person)-[:FRIEND]->(fof:Person) RETURN fof.name"
    4) "0.288"
```

### Reset slowlog


<Tabs groupId="programming-language">
  <TabItem value="shell" label="Shell">

```bash
GRAPH.SLOWLOG graph_id RESET
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
graph.slowlog_reset()
```

  </TabItem>
</Tabs>

Once cleared the information is lost forever.
