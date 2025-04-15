---
title: "BOLT protocol support"
nav_order: 11
description: "Connecting to FalkorDB using BOLT protocol."
---

# [EXPERIMENTAL] BOLT protocol support for FalkorDB 

FalkorDB provides an experimental support for querying using BOLT drivers.
We intend to extend the support in the future versions, the current version is not meant to be used in production.
This guide will walk you through the process of connecting to FalkorDB using the [BOLT protocol](https://en.wikipedia.org/wiki/Bolt_(network_protocol))

## Prerequisites

Before you begin, ensure that you have a FalkorDB instance up and running.
You can use our Docker image for this purpose.

```bash
docker run -p 6379:6379 -p 7687:7687 -p 3000:3000 -it -e REDIS_ARGS="--requirepass falkordb" -e FALKORDB_ARGS="BOLT_PORT 7687" --rm falkordb/falkordb:latest
```

### Ports 
- 6379 - FalkorDB
- 7687 - Bolt
- 3000 - Falkor-Browser

Additionally, install the necessary BOLT drivers:

```bash
pip install neo4j
```

## Step 1: Create a `main.py` File

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

## Step 2: Run the script

Execute the script by running the following command in your terminal:

bash
```bash
python main.py
```
