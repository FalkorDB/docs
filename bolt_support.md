---
title: "BOLT protocol support"
nav_order: 10
description: "Connecting to FalkorDB using BOLT protocol."
---

## BOLT protocol support for FalkorDB

FalkorDB provides support for querying using BOLT drivers.
This guide will walk you through the process of connecting to FalkorDB using the [BOLT protocol](https://en.wikipedia.org/wiki/Bolt_(network_protocol))

### Prerequisites

Before you begin, ensure that you have a FalkorDB instance up and running.
You can use our Docker image for this purpose.

```bash
docker run -p 6379:6379 -p7678:7678 -it -e REDIS_ARGS="--requirepass falkordb" -e FALKORDB_ARGS="BOLT_PORT 7678" --rm falkordb/falkordb:edge
```

Additionally, install the necessary BOLT drivers:

```bash
pip install neo4j
```

### Step 1: Create a `main.py` File

Create a main.py file with the following content and adjust the connection uri, authentication parameters and database name according to your FalkorDB setup. This script demonstrates a simple query that returns the numbers from 1 to 10. Customize the query as needed for your specific use case.

```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("falkordb", ""))

records, summary, keys = driver.execute_query(
    "UNWIND range(1, $n) AS i RETURN i",
    n=10, database_="mygraph",
)

for record in records:
    print(record["i"])
```

### Step 2: Run the script

Execute the script by running the following command in your terminal:

bash
```bash
python main.py
```
