---
title: "GRAPH.INFO"
description: >
    Returns information and statistics about the current executing commands
parent: "Commands"
nav_order: 10
---

# GRAPH.INFO

Returns information and statistics about currently running and waiting queries.

## Syntax

```
GRAPH.INFO [RunningQueries | WaitingQueries]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `RunningQueries` | keyword | No | Return only currently executing queries |
| `WaitingQueries` | keyword | No | Return only queries waiting in the queue |

If no argument is provided, both running and waiting queries are returned.

## Returns

Returns an array containing two sections:

1. **Running queries** - List of queries currently being executed with details:
   - Query text
   - Graph name
   - Execution time (milliseconds)
   - Client information
2. **Waiting queries** - List of queries in the queue waiting to be executed

Each query entry includes metadata that helps identify long-running operations and monitor query performance.

## Examples

### Get All Query Information

{% capture shell_0 %}
GRAPH.INFO
{% endcapture %}

{% capture python_0 %}
from falkordb import FalkorDB
client = FalkorDB()
info = client.call_procedure('GRAPH.INFO')
print(info)
{% endcapture %}

{% capture javascript_0 %}
import { FalkorDB } from 'falkordb';
const client = await FalkorDB.connect();
const info = await client.info();
console.log(info);
{% endcapture %}

{% capture java_0 %}
FalkorDB client = new FalkorDB();
List<List<Object>> info = client.info();
System.out.println(info);
{% endcapture %}

{% capture rust_0 %}
let client = FalkorDB::connect_default();
let info = client.info()?;
println!("{:?}", info);
{% endcapture %}

{% include code_tabs.html id="info_all_tabs" shell=shell_0 python=python_0 javascript=javascript_0 java=java_0 rust=rust_0 %}

**Sample Output (when no queries are running):**
```sh
1) "# Running queries"
2) (empty array)
3) "# Waiting queries"
4) (empty array)
```

### Get Running Queries Only

{% capture shell_1 %}
GRAPH.INFO RunningQueries
{% endcapture %}

{% capture python_1 %}
from falkordb import FalkorDB
client = FalkorDB()
running = client.call_procedure('GRAPH.INFO', 'RunningQueries')
print(running)
{% endcapture %}

{% capture javascript_1 %}
import { FalkorDB } from 'falkordb';
const client = await FalkorDB.connect();
const running = await client.info('RunningQueries');
console.log(running);
{% endcapture %}

{% capture java_1 %}
FalkorDB client = new FalkorDB();
List<List<Object>> running = client.info("RunningQueries");
System.out.println(running);
{% endcapture %}

{% capture rust_1 %}
let client = FalkorDB::connect_default();
let running = client.info_running_queries()?;
println!("{:?}", running);
{% endcapture %}

{% include code_tabs.html id="running_tabs" shell=shell_1 python=python_1 javascript=javascript_1 java=java_1 rust=rust_1 %}

**Sample Output (with active query):**
```sh
1) "# Running queries"
2) 1) 1) "graph: my_graph"
      2) "query: MATCH (n)-[*]->() RETURN n"
      3) "elapsed time (ms): 1250"
      4) "client: 127.0.0.1:52341"
```

### Get Waiting Queries Only

{% capture shell_2 %}
GRAPH.INFO WaitingQueries
{% endcapture %}

{% capture python_2 %}
from falkordb import FalkorDB
client = FalkorDB()
waiting = client.call_procedure('GRAPH.INFO', 'WaitingQueries')
print(waiting)
{% endcapture %}

{% capture javascript_2 %}
import { FalkorDB } from 'falkordb';
const client = await FalkorDB.connect();
const waiting = await client.info('WaitingQueries');
console.log(waiting);
{% endcapture %}

{% capture java_2 %}
FalkorDB client = new FalkorDB();
List<List<Object>> waiting = client.info("WaitingQueries");
System.out.println(waiting);
{% endcapture %}

{% capture rust_2 %}
let client = FalkorDB::connect_default();
let waiting = client.info_waiting_queries()?;
println!("{:?}", waiting);
{% endcapture %}

{% include code_tabs.html id="waiting_tabs" shell=shell_2 python=python_2 javascript=javascript_2 java=java_2 rust=rust_2 %}

**Sample Output (with queued queries):**
```sh
1) "# Waiting queries"
2) 1) 1) "graph: analytics"
      2) "query: MATCH (n:User) WHERE n.age > 25 RETURN count(n)"
      3) "wait time (ms): 45"
```

## Use Cases

- **Performance Monitoring**: Identify slow queries that may need optimization
- **Debugging**: See what queries are currently executing when investigating issues
- **Capacity Planning**: Monitor query queue depth to understand server load
- **Query Optimization**: Track execution times to identify bottlenecks

## Notes

- The `CMD_INFO` configuration parameter controls whether this command is enabled
- Disabling `GRAPH.INFO` may improve performance and reduce memory usage
- See [`MAX_INFO_QUERIES`](/getting-started/configuration#max_info_queries) to control query history size
