---
title: "Redis Commands"
nav_order: 99
description: >
    Allowed Redis commands in FalkorDB and their availability on FalkorDB Cloud
parent: "Commands"
---

# Redis Commands

FalkorDB is built as a Redis module, which means it supports a subset of Redis commands alongside its graph database commands. This page documents the Redis commands that are available in FalkorDB.

## Available Redis Commands

The following Redis commands are supported in FalkorDB:

### Connection & Authentication
- **[AUTH](https://redis.io/commands/auth/)** - Authenticate to the server
- **[HELLO](https://redis.io/commands/hello/)** - Handshake with Redis server
- **[PING](https://redis.io/commands/ping/)** - Test connection to the server
- **[ECHO](https://redis.io/commands/echo/)** - Echo the given string

### Server Information
- **[INFO](https://redis.io/commands/info/)** - Get information and statistics about the server
- **[CLIENT](https://redis.io/commands/client/)** - Manage client connections
- **[DBSIZE](https://redis.io/commands/dbsize/)** - Return the number of keys in the database
- **[MEMORY](https://redis.io/commands/memory/)** - Memory usage information
- **[SLOWLOG](https://redis.io/commands/slowlog/)** - Manage the slowlog

### Key Management
- **[DEL](https://redis.io/commands/del/)** - Delete one or more keys
- **[DUMP](https://redis.io/commands/dump/)** - Return a serialized version of the value stored at the specified key
- **[EXISTS](https://redis.io/commands/exists/)** - Determine if a key exists
- **[EXPIRE](https://redis.io/commands/expire/)** - Set a key's time to live in seconds
- **[EXPIRETIME](https://redis.io/commands/expiretime/)** - Get the absolute Unix timestamp at which the key will expire
- **[PEXPIREAT](https://redis.io/commands/pexpireat/)** - Set the expiration for a key as a Unix timestamp specified in milliseconds
- **[PTTL](https://redis.io/commands/pttl/)** - Get the time to live for a key in milliseconds
- **[RENAME](https://redis.io/commands/rename/)** - Rename a key
- **[RENAMENX](https://redis.io/commands/renamenx/)** - Rename a key, only if the new key does not exist
- **[SCAN](https://redis.io/commands/scan/)** - Incrementally iterate over keys in the database
- **[TOUCH](https://redis.io/commands/touch/)** - Update the last access time of keys
- **[TTL](https://redis.io/commands/ttl/)** - Get the time to live for a key in seconds
- **[TYPE](https://redis.io/commands/type/)** - Determine the type stored at key
- **[UNLINK](https://redis.io/commands/unlink/)** - Delete a key asynchronously

### Transaction Commands
- **[DISCARD](https://redis.io/commands/discard/)** - Discard all commands issued after MULTI
- **[EXEC](https://redis.io/commands/exec/)** - Execute all commands issued after MULTI
- **[MULTI](https://redis.io/commands/multi/)** - Mark the start of a transaction block
- **[UNWATCH](https://redis.io/commands/unwatch/)** - Forget about all watched keys
- **[WATCH](https://redis.io/commands/watch/)** - Watch keys for conditional execution of a transaction

### Replication & Persistence
- **[WAIT](https://redis.io/commands/wait/)** - Wait for synchronous replication of writes
- **[WAITAOF](https://redis.io/commands/waitaof/)** - Wait for writes to be synchronized to AOF
- **[READONLY](https://redis.io/commands/readonly/)** ⚠️ - Enable read-only mode for a replica
- **[BGREWRITEAOF](https://redis.io/commands/bgrewriteaof/)** ⚠️ - Asynchronously rewrite the append-only file
- **[FLUSHALL](https://redis.io/commands/flushall/)** ⚠️ - Remove all keys from all databases

### Module Management
- **[MODULE LIST](https://redis.io/commands/module-list/)** - List all loaded modules

### FalkorDB Graph Commands
FalkorDB provides the following graph database commands:

- **GRAPH.BULK** - Bulk insert data into a graph (see [bulk loader specification](/design/bulk-spec))
- **[GRAPH.CONFIG](/commands/graph.config-get)** - Get or set graph configuration parameters
- **[GRAPH.CONSTRAINT](/commands/graph.constraint-create)** - Manage graph constraints
- **[GRAPH.COPY](/commands/graph.copy)** - Copy a graph to a new key
- **[GRAPH.DELETE](/commands/graph.delete)** - Delete a graph
- **[GRAPH.EXPLAIN](/commands/graph.explain)** - Show the execution plan for a query
- **[GRAPH.INFO](/commands/graph.info)** - Get information about a graph
- **[GRAPH.LIST](/commands/graph.list)** - List all graphs
- **[GRAPH.MEMORY](/commands/graph.memory)** - Report memory usage of a graph
- **[GRAPH.PROFILE](/commands/graph.profile)** - Profile a query execution
- **[GRAPH.QUERY](/commands/graph.query)** - Execute a graph query
- **[GRAPH.RO_QUERY](/commands/graph.ro-query)** - Execute a read-only graph query
- **[GRAPH.SLOWLOG](/commands/graph.slowlog)** - Get the graph slowlog

## Command Availability on FalkorDB Cloud

All Redis commands and FalkorDB graph commands listed above are generally available on FalkorDB Cloud. However, certain administrative commands are restricted on the managed cloud service for security and stability reasons:

### Commands with Restrictions on Cloud

Commands marked with ⚠️ have restrictions on FalkorDB Cloud:

- **READONLY** - This command is restricted as it affects replication behavior and is managed by the cloud infrastructure
- **BGREWRITEAOF** - Background persistence operations are automatically managed by FalkorDB Cloud
- **FLUSHALL** - Deleting all data across databases is restricted to prevent accidental data loss. Use `GRAPH.DELETE` for individual graphs instead

### Cloud-Managed Features

On FalkorDB Cloud, the following features are automatically managed:

- **Persistence**: Automated backups are configured based on your tier (every 12 hours for Startup/Pro, every hour for Enterprise)
- **Replication**: High availability configurations automatically handle read replicas
- **Security**: TLS encryption is enabled on Startup tier and above

For more information about FalkorDB Cloud features and tiers, see the [Cloud DBaaS documentation](/cloud/).

## See Also

- [FalkorDB Commands Overview](/commands/)
- [FalkorDB Cloud](/cloud/)
- [Configuration](/getting-started/configuration)
- [Access Control Lists (ACL)](/commands/acl)
