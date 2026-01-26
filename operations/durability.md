---
title: "Durability"
nav_order: 2
description: "Understanding Data Durability Options in FalkorDB"
parent: "Operations"
has_children: true
---

# Data Durability in FalkorDB

FalkorDB, built on Redis, provides multiple mechanisms for data durability to ensure your graph data persists across restarts and survives system failures. Understanding these options helps you balance performance requirements with data safety needs.

## Overview

FalkorDB supports two primary persistence mechanisms:

1. **RDB (Redis Database)** - Point-in-time snapshots
2. **AOF (Append-Only File)** - Operation logging

You can use either mechanism independently or combine both for enhanced durability.

## RDB Snapshots

### How RDB Works

RDB creates point-in-time snapshots of your entire dataset and writes them to a compact `.rdb` file on disk. This approach provides:

- Compact, single-file backups ideal for disaster recovery
- Fast restart times (faster than AOF for large datasets)
- Easy versioning and cloning of datasets

### RDB Configuration

Configure RDB through `redis.conf` or via `redis-cli`:

```conf
# Save the dataset every 60 seconds if at least 1000 keys changed
save 60 1000

# Save every 5 minutes if at least 100 keys changed
save 300 100

# Save every 15 minutes if at least 1 key changed
save 900 1

# Configure RDB file location and name
dir /var/lib/falkordb/data
dbfilename dump.rdb
```

### RDB Considerations

**Advantages:**
- Excellent for backups and disaster recovery
- Minimal impact on performance during normal operations
- Compact file format
- Fast data loading on restart

**Limitations:**
- Potential data loss between snapshots
- Forking can be time-consuming for large datasets
- May cause brief performance degradation (milliseconds to 1 second) during snapshot creation on very large datasets
- Requires significant disk I/O during snapshot operations

**Best for:** Use cases where losing a few minutes of data is acceptable, or as a backup mechanism alongside AOF.

## AOF (Append-Only File)

### How AOF Works

AOF logs every write operation as it happens, creating an append-only log that can replay all operations to reconstruct the dataset. This provides greater durability than RDB snapshots.

### AOF Configuration

```conf
# Enable AOF
appendonly yes

# AOF file location
appendfilename "appendonly.aof"

# fsync policy - choose one:
appendfsync always    # Safest but slowest
appendfsync everysec  # Good balance (default)
appendfsync no        # Fastest but less durable
```

### AOF fsync Policies

#### 1. `appendfsync always`
- **Durability:** Maximum - virtually no data loss
- **Performance:** Lowest - synchronous disk writes
- **Data Loss Risk:** Only the latest command in case of disaster
- **Best for:** Mission-critical data where no data loss is acceptable

#### 2. `appendfsync everysec` (Recommended)
- **Durability:** High - fsync performed asynchronously every second
- **Performance:** High - background thread handles disk writes
- **Data Loss Risk:** Up to 1 second of writes
- **Best for:** Most production use cases balancing performance and durability

#### 3. `appendfsync no`
- **Durability:** Depends on OS (typically 30 seconds on Linux)
- **Performance:** Highest - OS decides when to flush
- **Data Loss Risk:** Several seconds of data in case of crashes
- **Best for:** High-performance scenarios where some data loss is acceptable

### AOF Rewrite

Over time, AOF files can grow large. AOF rewrite creates a compact version:

```conf
# Automatically trigger rewrite when file grows 100% larger
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
```

Manual rewrite:
```bash
redis-cli BGREWRITEAOF
```

## Combining RDB and AOF

For maximum durability, enable both mechanisms:

```conf
# Enable both persistence methods
save 900 1
save 300 10
save 60 10000
appendonly yes
appendfsync everysec
```

On restart, FalkorDB will use the AOF file (if available) since it provides better durability guarantees.

## Graph-Specific Operations: DUMP and RESTORE

For graph-specific backup and migration scenarios, FalkorDB supports Redis's DUMP and RESTORE commands for individual keys (graphs).

### DUMP Command

Serialize a graph to a portable format:

```bash
redis-cli DUMP mygraph > mygraph.dump
```

The DUMP command:
- Returns a serialized representation of the value at the specified key
- The serialization format is opaque and specific to Redis/FalkorDB
- Contains the graph structure and all its data
- Does not include TTL information by default

Learn more: [Redis DUMP Documentation](https://redis.io/docs/latest/commands/dump/)

### RESTORE Command

Restore a serialized graph:

```bash
redis-cli --pipe < mygraph.dump
# Or directly:
redis-cli RESTORE mygraph 0 "<serialized-value>"
```

RESTORE options:
- `REPLACE` - Overwrite existing key (available since Redis 3.0.0)
- `ABSTTL` - TTL represents absolute Unix timestamp (since Redis 5.0.0)
- `IDLETIME` - Set the idle time for the object

Learn more: [Redis RESTORE Documentation](https://redis.io/docs/latest/commands/restore/)

### Use Cases for DUMP/RESTORE

- **Selective backup:** Back up specific graphs rather than entire database
- **Migration:** Move specific graphs between FalkorDB instances
- **Testing:** Clone production graphs to test environments
- **Archival:** Export graphs for long-term storage

**Note:** For full database backup, RDB snapshots are more efficient than individual DUMP operations.

## Choosing the Right Strategy

### High Performance, Some Data Loss Acceptable
```conf
save 900 1
save 300 10
appendonly no
```

### Balanced Performance and Durability (Recommended)
```conf
save 900 1
save 300 10
save 60 1000
appendonly yes
appendfsync everysec
```

### Maximum Durability
```conf
save 60 1
appendonly yes
appendfsync always
```

### Development/Testing
```conf
save ""
appendonly no
```

## Docker Environment Persistence

When running FalkorDB in Docker, proper volume configuration is essential for durability. See the [Persistence on Docker](/operations/persistence) guide for detailed instructions on:

- Creating persistent volumes
- Mounting data directories
- Verifying persistence configuration
- Best practices for Docker deployments

## Monitoring and Maintenance

### Check Persistence Status

```bash
redis-cli INFO persistence
```

### Manual Save Operations

```bash
# Create RDB snapshot immediately (blocking)
redis-cli SAVE

# Create RDB snapshot in background (non-blocking)
redis-cli BGSAVE

# Rewrite AOF file
redis-cli BGREWRITEAOF
```

### Backup Best Practices

1. **Regular Snapshots:** Schedule periodic RDB snapshots using cron or similar
2. **Off-site Backups:** Store backups in separate locations or cloud storage
3. **Test Restores:** Regularly verify backups can be restored successfully
4. **Monitor Disk Space:** Ensure sufficient space for both RDB and AOF files
5. **Automate:** Use scripts to automate backup, verification, and rotation

## Performance Considerations

- **RDB:** Brief CPU spike and memory overhead during fork; negligible impact between snapshots
- **AOF (everysec):** Minimal performance impact, ~1-2% overhead
- **AOF (always):** Significant performance impact due to synchronous disk I/O
- **Both RDB + AOF:** Cumulative overhead but maximum durability

## Further Reading

- [Persistence Options in Redis](https://redis.io/tutorials/operate/redis-at-scale/persistence-and-durability/persistence-options-in-redis/)
- [Redis Persistence Documentation](https://redis.io/docs/management/persistence/)
- [FalkorDB Docker Persistence Setup](/operations/persistence)
- [FalkorDB Replication](/operations/replication)
