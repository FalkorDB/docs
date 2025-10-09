---
title: "Replication"
nav_order: 2
description: "Configuring FalkorDB Docker for Replication"
parent: "Operations"
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
For that to work with Docker, we need to first set up a network.

### 1.1 Creating a Network

First, create a Docker network to allow communication between the FalkorDB nodes.

```bash
docker network create falkordb-network
```

### 1.1 Setting up the Master Instance

Start the master FalkorDB instance:

```bash
docker run -d \
  --name falkordb-master \
  -v falkordb_data:/data \
  -p 6379:6379 \
  --network falkordb-network \
  falkordb/falkordb
```

> **Production Tip:** For production deployments, use `falkordb/falkordb-server` instead of `falkordb/falkordb` for a lighter image without the Browser UI.

This instance will be created in the Standalone mode, as master.

### 1.2 Setting up the Replica Instance

Next, start the replica instance:

```bash
docker run -d \
  --name falkordb-replica1 \
  -p 6380:6379 \
  --network falkordb-network \
  falkordb/falkordb
```

> **Note:** For production, use `falkordb/falkordb-server` for both master and replica instances.

### 1.3 Configuring Replication

Connect to the replica instance and configure it to replicate data from the master:

```bash
docker exec -it falkordb-replica1 /bin/bash 
redis-cli replicaof falkordb-master 6379
```

This command tells the replica to replicate data from the master instance.

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
redis-cli graph.ro_query mygraph "MATCH (n) return n"
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

If you're interested in learning more about clustering and scaling out, be sure to check out the [Cluster](/operations/cluster) chapter in the documentation.