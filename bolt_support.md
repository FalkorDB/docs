---
title: "BOLT protocol support"
nav_order: 10
description: "Connecting FalkorDB using BOLT protocol."
---

## BOLT protocol support for FalkorDB

FalkorDB provides support for querying using BOLT drivers. This guide will walk you through the process of connecting to FalkorDB using the BOLT protocol.

### Prerequisites

Before you begin, ensure that you have a FalkorDB instance up and running. You can use either Docker or the FalkorDB sandbox for this purpose. Additionally, install the necessary BOLT drivers:

```bash
pip install neo4j
```

### Step 1: Create a `main.py` File

Create a main.py file with the following content:

```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("falkordb", ""))

records, _, _ = driver.execute_query(
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

Adjust the authentication parameters and database name according to your FalkorDB setup. This script demonstrates a simple query that returns the numbers from 1 to 10. Customize the query as needed for your specific use case.
