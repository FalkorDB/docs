---
title: "GRAPH.SLOWLOG"
description: >
    Returns a list containing up to 10 of the slowest queries issued against the given graph
parent: "Commands"    
---

# GRAPH.SLOWLOG

Returns a list containing up to 10 of the slowest queries issued against the given graph ID.

Each item in the list has the following structure:

1. A Unix timestamp at which the log entry was processed.
2. The issued command.
3. The issued query.
4. The amount of time needed for its execution, in milliseconds.

## Examples

### Get slowlog

{% capture shell_0 %}
GRAPH.SLOWLOG graph_id
{% endcapture %}

{% capture python_0 %}
from falkordb import FalkorDB
db = FalkorDB(host='localhost', port=6379)
graph = db.select_graph('graph_id')
slowlog = graph.slowlog()
print(slowlog)
{% endcapture %}

{% capture javascript_0 %}
import { FalkorDB } from 'falkordb';
const db = await FalkorDB.connect({
  socket: { host: 'localhost', port: 6379 }
});
const graph = db.selectGraph('graph_id');
const slowlog = await graph.slowLog();
console.log(slowlog);
{% endcapture %}

{% include code_tabs.html id="slowlog_tabs" shell=shell_0 python=python_0 javascript=javascript_0 %}

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

{% capture shell_1 %}
GRAPH.SLOWLOG graph_id RESET
{% endcapture %}

{% capture python_1 %}
graph.slowlog_reset()
{% endcapture %}

{% include code_tabs.html id="slowlog_reset_tabs" shell=shell_1 python=python_1 %}

Once cleared the information is lost forever.
