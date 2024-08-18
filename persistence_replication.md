---
title: "Persistence and Replication"
nav_order: 8
description: "Configuring FalkorDB Docker for Persistence and Replication
"
---

# Configuring FalkorDB Docker for Persistence and Replication

FalkorDB supports advanced configurations to enable data persistence and replication, ensuring that your data is safe and available across different instances. This guide will walk you through setting up FalkorDB in Docker with persistence and replication enabled.

## Prerequisites

Before you begin, ensure you have the following:

    * Docker installed on your machine.
    * A working FalkorDB Docker image. You can pull it from Docker Hub.
    * Basic knowledge of Docker commands and configurations.

## Step 1: Setting Up Persistence

Persistence in FalkorDB allows you to store your data on the host machine, ensuring that it is not lost when the container restarts.

### 1.1 Create a Persistent Volume

First, create a Docker volume to store the data:

```bash
docker volume create falkordb_data
```

This volume will be used to store the database files.

### 1.2 Start FalkorDB with the Persistent Volume

You can now run FalkorDB with the volume attached:

```bash
docker run -d \
  --name falkordb \
  -v falkordb_data:/data \
  falkordb/falkordb
```

In this configuration:

    The -v falkordb_data:/data flag mounts the volume to the /data directory inside the container.
    FalkorDB will use this directory to store its data.

## Step 2: Configuring Replication

Replication ensures that your data is available across multiple FalkorDB instances. You can configure one instance as the master and others as replicas.

### 2.1 Setting Up the Master Instance

Start the master FalkorDB instance:

```bash
docker run -d \
  --name falkordb-master \
  -v falkordb_data:/data \
  -e REPLICATION_MODE=master \
  -e REPLICATION_ID=master1 \
  falkordb/falkordb
```

Here:

    The -e REPLICATION_MODE=master flag sets this instance as the master.
    The -e REPLICATION_ID=master1 assigns a unique ID to the master.

### 2.2 Configuring the Replica Instances

Next, start the replica instances that will replicate data from the master:

```bash
docker run -d \
  --name falkordb-replica1 \
  -e REPLICATION_MODE=replica \
  -e REPLICATION_MASTER_HOST=falkordb-master \
  -e REPLICATION_ID=replica1 \
  falkordb/falkordb
```

In this setup:

    * The -e REPLICATION_MODE=replica flag sets the instance as a replica.
    * The -e REPLICATION_MASTER_HOST=falkordb-master flag specifies the master instance's hostname or IP address.
    * The -e REPLICATION_ID=replica1 assigns a unique ID to this replica.

You can add additional replicas by repeating the command with different container names and REPLICATION_IDs.

## Step 3: Verifying the Setup

To verify that your setup is working correctly:

    * Persistence Check: Stop the FalkorDB container and start it again. The data should persist across restarts.

```bash
    docker stop falkordb
    docker start falkordb
```

   * Replication Check: Insert some data into the master instance and check if it is available in the replica.

```bash
    # Connect to the master
    docker exec -it falkordb-master /bin/bash
    falkordb-cli set key "Hello, FalkorDB!"
    exit

    # Connect to the replica
    docker exec -it falkordb-replica1 /bin/bash
    falkordb-cli get key
    # Output should be "Hello, FalkorDB!"
```

## Conclusion

With persistence and replication configured, FalkorDB is now set up for reliable data storage and high availability. You can scale this setup by adding more replicas or by implementing Redis Sentinel for automatic failover.