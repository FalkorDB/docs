---
title: "Replication"
nav_order: 2
description: "Configuring FalkorDB Docker for Replication"
---

# Configuring FalkorDB Docker for Replication

FalkorDB supports advanced configurations to enable replication, ensuring that your data is available and synchronized across multiple instances. This guide will walk you through setting up FalkorDB in Docker with replication enabled, providing high availability and data redundancy.

## Prerequisites

Before you begin, ensure you have the following:

* Docker installed on your machine.
* A working FalkorDB Docker image. You can pull it from Docker Hub.
* Basic knowledge of Docker commands and configurations.

## Step 1: Configuring Replication

Replication ensures that your data is available across multiple FalkorDB instances. You can configure one instance as the master and others as replicas.

### 1.1 Setting Up the Master Instance

Start the master FalkorDB instance:

```bash
docker run -d \
  --name falkordb-master \
  -v falkordb_data:/data \
  -e REPLICATION_MODE=master \
  -e REPLICATION_ID=master1 \
  -p 6379:6379 \
  falkordb/falkordb
```
Here:

The -e REPLICATION_MODE=master flag sets this instance as the master.
The -e REPLICATION_ID=master1 assigns a unique ID to the master.

### 1.2 Configuring the Replica Instances

Next, start the replica instances that will replicate data from the master:

```bash
docker run -d \
  --name falkordb-replica1 \
  -e REPLICATION_MODE=replica \
  -e REPLICATION_MASTER_HOST=falkordb-master \
  -e REPLICATION_ID=replica1 \
  -p 6379:6379 \
  falkordb/falkordb
```

In this setup:

* The -e REPLICATION_MODE=replica flag sets the instance as a replica.
* The -e REPLICATION_MASTER_HOST=falkordb-master flag specifies the master instance's hostname or IP address.
* The -e REPLICATION_ID=replica1 assigns a unique ID to this replica.

You can add additional replicas by repeating the command with different container names and REPLICATION_IDs.

## Step 2: Verifying the Setup

To verify that your setup is working correctly:

* Replication Check: Insert some data into the master instance and check if it is available in the replica.

```bash
# Connect to the master
docker exec -it falkordb-master /bin/bash
redis-cli graph.query mygraph "CREATE (:Database {name:'falkordb'})"
exit

# Connect to the replica
docker exec -it falkordb-replica1 /bin/bash
redis-cli graph.query mygraph "MATCH (n) return n"
# Output should be:
# 1) 1) "n"
# 2) 1) 1) 1) 1) "id"
#             2) (integer) 0
#          2) 1) "labels"
#             2) 1) "Database"
#          3) 1) "properties"
#             2) 1) 1) "name"
#                   2) "falkordb"
# 3) 1) "Cached execution: 1"
#    2) "Query internal execution time: 0.122645 milliseconds"
```

## Conclusion

With replication configured, FalkorDB is now set up for high availability and data redundancy, ensuring that your data is synchronized across multiple instances. This setup provides a robust and fault-tolerant environment for your applications.

If you're interested in learning more about clustering and scaling out, be sure to check out the [Cluster](/operation/cluster) chapter in the documentation.