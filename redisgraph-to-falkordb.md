---
title: "RedisGraph to FalkorDB"
nav_order: 13
description: "Migrate from RedisGraph to FalkorDB."
---

# FalkorDB is compatible with RedisGraph RDB files.

For the migration, execute the following steps:

1. Get the latest RDB file from your RedisGraph instance. Ensure you call SAVE or BGSAVE to capture the latest data snapshot.
2. Load the RDB file into FalkorDB. When using the FalkorDB Docker image, use the following command:

   ```bash
   docker run -it -p 6379:6379 -v $(pwd):/data -e REDIS_ARGS="--dir /data --dbfilename dump.rdb" falkordb/falkordb
   ```

   Make sure to place the RDB file in the directory mapped to the Docker volume.
   For FalkorDB Cloud, follow the cloud provider’s instructions for uploading and restoring from an RDB file.

## Additional Tips:

* Verify the integrity of the RDB file before and after transfer.
* Consider downtime and data consistency during the migration process.
* Test the migration process in a staging environment before applying it to production.
