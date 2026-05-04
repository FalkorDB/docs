---
title: "GRAPH.SLOWLOG"
description: >
    View the 10 slowest queries executed against a FalkorDB graph with GRAPH.SLOWLOG command. Monitor query performance, execution times, and optimize slow operations.
parent: "Commands"    
---

# GRAPH.SLOWLOG

Returns a list containing up to 10 of the slowest queries issued against the given graph ID.

Only queries with a latency of 10 milliseconds or more are logged.

Each item in the list has the following structure:

1. A Unix timestamp (double) at which the log entry was processed.
2. The issued command.
3. The issued query.
4. The amount of time needed for its execution, in milliseconds (double).
5. The query parameters (or (nil) if none were provided).

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
 1) 1) "1581932396.723"
    2) "GRAPH.QUERY"
    3) "MATCH (a:Person)-[:FRIEND]->(e) RETURN e.name"
    4) "12.831"
    5) (nil)
 2) 1) "1581932396.891"
    2) "GRAPH.QUERY"
    3) "MATCH (me:Person)-[:FRIEND]->(:Person)-[:FRIEND]->(fof:Person) RETURN fof.name"
    4) "10.288"
    5) (nil)
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

{% include faq_accordion.html title="Frequently Asked Questions" q1="What is the minimum latency for a query to appear in the slowlog?" a1="Only queries with a latency of **10 milliseconds or more** are logged in the slowlog." q2="How many entries does the slowlog store?" a2="The slowlog stores up to **10** of the slowest queries issued against the given graph. Older entries are evicted when new slower queries are recorded." q3="Can I reset the slowlog?" a3="Yes. Use `GRAPH.SLOWLOG graph_name RESET` to clear all entries. Note that once cleared, the information is lost permanently." q4="What information is included in each slowlog entry?" a4="Each entry contains: (1) Unix timestamp, (2) the issued command, (3) the query string, (4) execution time in milliseconds, and (5) query parameters or nil if none were provided." %}
