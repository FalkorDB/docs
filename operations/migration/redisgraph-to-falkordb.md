---
title: "RedisGraph to FalkorDB"
description: "Migrate from RedisGraph to FalkorDB."
parent: "Migration"
nav_order: 1
redirect_from:
  - /redisgraph-to-falkordb.html
  - /redisgraph-to-falkordb
---

# RedisGraph to FalkorDB Migration

FalkorDB is fully compatible with RedisGraph RDB (Redis Database) files, making migration straightforward.

## Migration Steps

### Step 1: Create RDB Snapshot from RedisGraph

Create a snapshot of your RedisGraph database using the `SAVE` or `BGSAVE` command:

```bash
# Connect to your RedisGraph instance
redis-cli

# Create snapshot (blocks server during save)
SAVE

# Or create snapshot in background (recommended for production)
BGSAVE
```

This creates a `dump.rdb` file in your Redis data directory.

### Step 2: Load RDB File into FalkorDB

#### Using Docker

When using the FalkorDB Docker image, mount your RDB file and configure Redis to load it:

   ```bash
   docker run -it -p 6379:6379 -v $(pwd):/data -e REDIS_ARGS="--dir /data --dbfilename dump.rdb" falkordb/falkordb
   ```

   Make sure to place the RDB file in the directory mapped to the Docker volume.
   For FalkorDB Cloud, follow the cloud provider’s instructions for uploading and restoring from an RDB file.

**Important:** Ensure your `dump.rdb` file is placed in the directory mapped to the Docker volume (`$(pwd)` in the example above).

#### Using FalkorDB Cloud

For FalkorDB Cloud deployments, follow the cloud provider's instructions for uploading and restoring from an RDB file.

## Verification

After loading the RDB file, verify your data:

```bash
# Connect to FalkorDB
redis-cli

# List all graphs
GRAPH.LIST

# Query a graph to verify data
GRAPH.QUERY your_graph_name "MATCH (n) RETURN count(n)"
```

## Best Practices

* **Verify RDB Integrity:** Check the RDB file integrity before and after transfer
* **Plan for Downtime:** Consider downtime requirements and data consistency during migration
* **Test First:** Always test the migration in a staging environment before production
* **Backup:** Keep backups of both the source RedisGraph data and the RDB file
* **Monitor:** After migration, monitor FalkorDB performance and verify queries work correctly
