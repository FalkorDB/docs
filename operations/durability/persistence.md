---
title: "Persistence on Docker"
nav_order: 1
description: "Configure persistent data storage for FalkorDB in Docker using volumes to ensure your graph data remains intact across container restarts and system reboots."
parent: "Durability"
grand_parent: "Operations"
redirect_from:
  - /operations/persistence
  - /operations/persistence.html
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
docker run -d --name falkordb -v falkordb_data:/var/lib/falkordb/data -p 6379:6379 falkordb/falkordb
```

**Configuration details:**
- The `-v falkordb_data:/var/lib/falkordb/data` flag mounts the volume to the `/var/lib/falkordb/data` directory inside the container
- FalkorDB stores its data in the `/var/lib/falkordb/data` directory by default

## Step 2: Verifying the Setup

To verify that persistence is working correctly, follow these steps:

### 2.1 Create Test Data

```bash
redis-cli GRAPH.QUERY mygraph "CREATE (:Database {name:'falkordb'})"
```

### 2.2 Restart Container

```bash
docker stop falkordb
docker start falkordb
```

### 2.3 Verify Data Persists

```bash
redis-cli GRAPH.QUERY mygraph "MATCH (n) RETURN n"
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

## Best Practices

- **Backup Regularly:** Even with persistence, maintain regular backups of your data
- **Monitor Disk Space:** Ensure sufficient disk space is available for the volume
- **Use Named Volumes:** Named volumes are easier to manage than bind mounts

## Understanding Durability Options

Docker volume configuration ensures your data persists across container restarts, but FalkorDB also provides multiple durability mechanisms (RDB snapshots, AOF logging) to protect against data loss and optimize for different use cases.

For a comprehensive guide on configuring RDB, AOF, and graph-specific backup options, see [Data Durability](/operations/durability).

## ACL User Persistence

Docker volume configuration persists your graph data, but ACL users created with `ACL SETUSER` are stored separately in an ACL file. To persist users, passwords, and permissions across restarts, see [ACL Persistence on Docker](/operations/durability/acl-persistence).

## Next Steps

With persistence configured, FalkorDB is now set up for reliable data storage that remains intact across container restarts. 

For high availability and data redundancy, explore [Replication](/operations/replication) to set up multiple FalkorDB instances.

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="What directory does FalkorDB use for data inside the container?"
  a1="FalkorDB stores data in `/var/lib/falkordb/data` by default. Mount your Docker volume to this path: `-v falkordb_data:/var/lib/falkordb/data`."
  q2="Should I use named volumes or bind mounts?"
  a2="Named volumes are recommended for most cases as they are easier to manage and portable. Use bind mounts only when you need to map a specific host directory for backups or shared access."
  q3="How do I verify persistence is working after a restart?"
  a3="Create test data, stop and restart the container, then query the data again. If it returns your previously created nodes, persistence is configured correctly."
  q4="Does Docker volume persistence also save ACL users?"
  a4="No. ACL users are stored separately in memory by default. To persist ACL users, configure an ACL file with `--aclfile` and store it on the mounted volume. See [ACL Persistence](/operations/durability/acl-persistence)."
%}

