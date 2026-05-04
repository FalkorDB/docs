---
title: "BOLT protocol support"
nav_order: 4
description: "Connect to FalkorDB using the BOLT protocol with neo4j drivers. Experimental feature for compatibility with BOLT-based tools and Neo4j client libraries."
parent: "Integration"
redirect_from:
  - /bolt-support.html
  - /bolt-support
  - /bolt_support.html
  - /bolt_support
---

# [EXPERIMENTAL] BOLT protocol support for FalkorDB 

> **Note:** For production use cases, please use our [official client libraries](../getting-started/clients.md) instead.

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

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="Is the Bolt protocol support production-ready?"
  a1="No, Bolt protocol support in FalkorDB is currently **experimental** and not recommended for production use. For production workloads, use the official FalkorDB client libraries."
  q2="Which Neo4j driver versions are compatible with FalkorDB Bolt support?"
  a2="FalkorDB works with the standard `neo4j` Python driver. Install it via `pip install neo4j`. Other language drivers that support the Bolt protocol should also work, but Python is the primary tested client."
  q3="What port does FalkorDB use for Bolt connections?"
  a3="FalkorDB uses port **7687** for Bolt connections by default. You need to set the `BOLT_PORT` environment variable (e.g., `FALKORDB_ARGS='BOLT_PORT 7687'`) when starting the Docker container."
  q4="Can I use Bolt and the native FalkorDB protocol simultaneously?"
  a4="Yes, FalkorDB can expose both protocols at the same time. The native protocol runs on port 6379 (Redis protocol) while Bolt runs on port 7687. Both can be active concurrently."
  q5="How do I authenticate when using Bolt?"
  a5="Pass your credentials in the `auth` parameter of the driver constructor. For example: `GraphDatabase.driver('bolt://localhost:7687', auth=('falkordb', ''))`. The username is typically `falkordb` and the password matches your Redis `requirepass` setting."
%}
