---
title: "Persistence"
nav_order: 1
description: "Configuring FalkorDB Docker for Persistence"
parent: "Operations"
---

# Configuring FalkorDB Docker for Persistence

FalkorDB supports advanced configurations to enable data persistence, ensuring that your data is safe and remains intact even after container restarts. This guide will walk you through setting up FalkorDB in Docker with persistence enabled.

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
docker run -d --name falkordb -v falkordb_data:/data -p 6379:6379 falkordb/falkordb
```

In this configuration:

The -v falkordb_data:/data flag mounts the volume to the /data directory inside the container.
FalkorDB will use the /data directory by default.

## Step 2: Verifying the Setup

To verify that your setup is working correctly:

* Persistence Check: Stop the FalkorDB container and start it again. The data should persist across restarts.

```bash
redis-cli graph.query mygraph "CREATE (:Database {name:'falkordb'})"

docker stop falkordb
docker start falkordb

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

With persistence configured, FalkorDB is now set up for reliable data storage that remains intact across container restarts. This setup ensures that your data is consistently saved, providing a stable and dependable environment for your applications. 

If you're interested in learning more about high availability and replication, be sure to check out the [replication](/operations/replication) chapter in the documentation.

