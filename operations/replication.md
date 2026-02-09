---
title: "Replication"
nav_order: 2
description: "Configure FalkorDB replication in Docker for high availability and data redundancy. Set up master-replica architecture with step-by-step instructions for data synchronization."
parent: "Operations"
redirect_from:
  - /operation/replication
  - /operation/replication.html
---

# Configuring FalkorDB Docker for Replication

FalkorDB supports advanced configurations to enable replication, ensuring that your data is available and synchronized across multiple instances. This guide will walk you through setting up FalkorDB in Docker with replication enabled, providing high availability and data redundancy.

## Prerequisites

Before you begin, ensure you have the following:

* Docker installed on your machine.
* A working FalkorDB Docker image. You can pull it from Docker Hub.
* Basic knowledge of Docker commands and configurations.

## Step 1: Configuring Replication

Replication ensures that your data is available across multiple FalkorDB instances. You configure one instance as the primary (master) and others as replicas.

To enable communication between FalkorDB containers, we first need to set up a Docker network.

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

This instance runs in standalone mode and will serve as the primary (master) node.

### 1.2 Setting up the Replica Instance

Next, start the replica instance:

```bash
docker run -d \
  --name falkordb-replica1 \
  -p 6380:6379 \
  --network falkordb-network \
  falkordb/falkordb
```

### 1.3 Configuring Replication

Connect to the replica instance and configure it to replicate data from the master:

```bash
docker exec -it falkordb-replica1 /bin/bash 
redis-cli replicaof falkordb-master 6379
```

This command tells the replica to replicate data from the master instance.

## Step 2: Verifying the Setup

To verify that replication is working correctly:

### 2.1 Insert Data on Master

```bash
# Connect to the master
docker exec -it falkordb-master redis-cli
GRAPH.QUERY mygraph "CREATE (:Database {name:'falkordb'})"
exit
```

### 2.2 Verify Data on Replica

```bash
# Connect to the replica
docker exec -it falkordb-replica1 redis-cli
GRAPH.RO_QUERY mygraph "MATCH (n) RETURN n"
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

**Expected output:** The data created on the master should be available on the replica.

## Best Practices

- **Read-Only Queries on Replicas:** Use `GRAPH.RO_QUERY` for read operations on replicas to prevent accidental writes
- **Monitor Replication Lag:** Check replication status regularly using Redis `INFO replication` command
- **Multiple Replicas:** Configure multiple replicas for better read scalability and redundancy
- **Network Latency:** Place master and replicas in the same network or region for optimal performance

## Troubleshooting

If replication is not working:

1. Verify network connectivity between containers
2. Check that the master is accessible from the replica
3. Review logs for errors: `docker logs falkordb-replica1`

## Next Steps

With replication configured, FalkorDB provides high availability and data redundancy. Your data is now synchronized across multiple instances, creating a robust and fault-tolerant environment.

For horizontal scalability and distributed graph operations, explore [Clustering](/operations/cluster).
