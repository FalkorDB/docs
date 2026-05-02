---
title: "Troubleshooting"
parent: "Operations"
nav_order: 14
description: "Common FalkorDB issues and solutions covering connection errors, query timeouts, out-of-memory problems, replication, cluster, Docker, and Kubernetes troubleshooting."
---

# Troubleshooting

This page covers the most common issues encountered when running FalkorDB, along with their solutions. Issues are grouped by category for quick reference.

---

## Connection Issues

### Connection Refused

**Symptom:** Client throws `Connection refused` or `Could not connect to FalkorDB at localhost:6379`.

**Possible Causes:**
1. FalkorDB is not running
2. The port is not exposed or mapped incorrectly
3. A firewall is blocking the connection

**Solutions:**

```bash
# Check if FalkorDB is running
docker ps | grep falkordb

# Verify port mapping
docker port <container_id>

# Test connectivity
redis-cli -h localhost -p 6379 ping
```

If using Docker Compose, ensure the `ports` section maps the correct host port:

```yaml
ports:
  - "6379:6379"
```

### Authentication Required / NOAUTH

**Symptom:** `NOAUTH Authentication required` or `ERR invalid password`.

**Solutions:**
- Ensure your client provides the correct password set via `--requirepass`
- If using ACL users, authenticate with both username and password
- Check that the ACL file is mounted correctly if users are not persisting

```python
# Python — provide password
db = FalkorDB(host='localhost', port=6379, password='yourpassword')

# With ACL user
db = FalkorDB(host='localhost', port=6379, username='myuser', password='mypassword')
```

### MOVED Redirect (Cluster Mode)

**Symptom:** `MOVED 12345 10.0.0.2:6379` error when executing queries.

**Cause:** Your client is connecting to a cluster node that doesn't own the hash slot for the requested graph.

**Solution:** Use a cluster-aware client that handles MOVED redirections automatically, or connect to the correct node. See [Setting Up a Cluster](/operations/cluster) for details.

---

## Query Issues

### Query Timeout Exceeded

**Symptom:** `Query timed out` error.

**Cause:** The query execution exceeded the configured timeout.

**Solutions:**

1. **Check the current timeout settings:**

   ```
   GRAPH.CONFIG GET TIMEOUT_DEFAULT
   GRAPH.CONFIG GET TIMEOUT_MAX
   ```

2. **Increase the timeout** (if the query legitimately needs more time):

   ```
   GRAPH.CONFIG SET TIMEOUT_DEFAULT 10000
   ```

3. **Optimize the query** — use [GRAPH.EXPLAIN](/commands/graph.explain) to inspect the query plan and add indexes where needed:

   ```
   GRAPH.EXPLAIN myGraph "MATCH (n:Person {name: 'Alice'}) RETURN n"
   ```

4. **Override timeout per-query:**

   ```
   GRAPH.QUERY myGraph "MATCH (n) RETURN n LIMIT 100" TIMEOUT 30000
   ```

See [Configuration — Timeouts](/getting-started/configuration#timeout_default) for more details.

### Graph Not Found

**Symptom:** `ERR Invalid graph operation on empty key` or similar.

**Cause:** The graph key does not exist — it may not have been created yet, or the name is misspelled.

**Solution:**

```
# List all graphs
GRAPH.LIST
```

Verify the graph name matches exactly (graph names are case-sensitive).

### Slow Queries

**Symptom:** Queries take longer than expected.

**Diagnostic Steps:**

1. **Check the slow log:**

   ```
   GRAPH.SLOWLOG myGraph
   ```

   This shows queries that took ≥ 10 ms.

2. **Profile the query:**

   ```
   GRAPH.PROFILE myGraph "MATCH (n:Person)-[:KNOWS]->(m) WHERE n.name = 'Alice' RETURN m"
   ```

   Look for full graph scans — these indicate a missing index.

3. **Add an index** if the query filters on a property:

   ```
   GRAPH.QUERY myGraph "CREATE INDEX FOR (n:Person) ON (n.name)"
   ```

See [Range Indexes](/cypher/indexing/range-index) and [GRAPH.PROFILE](/commands/graph.profile) for more details.

---

## Memory Issues

### Out of Memory

**Symptom:** `OOM command not allowed when used memory > maxmemory` or query fails with memory allocation error.

**Possible Causes:**
1. The graph exceeds available memory
2. A single query allocates too much memory

**Solutions:**

1. **Check memory usage:**

   ```
   GRAPH.MEMORY myGraph
   INFO memory
   ```

2. **Limit per-query memory:**

   ```
   GRAPH.CONFIG SET QUERY_MEM_CAPACITY 1073741824   # 1 GB
   ```

3. **Increase the server memory limit** (if resources are available):

   ```
   CONFIG SET maxmemory 8gb
   ```

4. **Optimize your data model** — remove unnecessary properties, use shorter string values, or split into multiple graphs.

See [GRAPH.MEMORY](/commands/graph.memory) and [Configuration — QUERY_MEM_CAPACITY](/getting-started/configuration#query_mem_capacity) for details.

---

## Docker Issues

### Container Exits Immediately

**Symptom:** Container starts and stops within seconds.

**Diagnostic Steps:**

```bash
# Check container logs
docker logs <container_id>

# Run interactively to see errors
docker run -it --rm falkordb/falkordb:latest
```

**Common causes:**
- Invalid `REDIS_ARGS` or `FALKORDB_ARGS` environment variables
- Missing ACL file when `aclfile` directive is set
- Port conflicts with another service

### Data Lost After Container Restart

**Cause:** Data is stored inside the container filesystem, which is ephemeral.

**Solution:** Mount a persistent volume:

```bash
docker run -p 6379:6379 -p 3000:3000 \
  -v falkordb-data:/data \
  --rm falkordb/falkordb:latest
```

See [Data Durability](/operations/durability) and [Docker Deployment](/operations/docker) for full persistence configuration.

### Browser Not Accessible

**Symptom:** Cannot reach the FalkorDB Browser at `http://localhost:3000`.

**Check:**
1. Ensure port 3000 is mapped: `-p 3000:3000`
2. If using `falkordb/falkordb-server` image — this image does **not** include the Browser. Use `falkordb/falkordb` instead.
3. Check firewall rules if accessing remotely.

---

## Replication Issues

### Replica Not Syncing

**Symptom:** Replica shows stale data or `master_link_status:down`.

**Diagnostic Steps:**

```bash
# On the replica
redis-cli INFO replication
```

**Check:**
- Network connectivity between primary and replica
- Authentication — replica must use the primary's password via `--masterauth`
- The primary is not at max memory / max clients

See [Configuring Replication](/operations/replication) for setup details.

---

## Kubernetes Issues

### Pod CrashLoopBackOff

**Symptom:** FalkorDB pod repeatedly crashes.

**Diagnostic Steps:**

```bash
kubectl logs <pod-name> --previous
kubectl describe pod <pod-name>
```

**Common causes:**
- Insufficient memory requests/limits — FalkorDB needs enough memory for the graph data
- PersistentVolumeClaim not bound
- Incorrect module path in `--loadmodule` flag

See [Deploy FalkorDB to Kubernetes](/operations/k8s-support) and [KubeBlocks](/operations/kubeblocks) for deployment guides.

---

## Getting More Help

If your issue is not covered here:

1. **Check the logs** — FalkorDB and Redis logs often contain detailed error messages
2. **Search existing issues** on [GitHub](https://github.com/FalkorDB/FalkorDB/issues)
3. **Join the community** on [Discord](https://discord.gg/ErBEqN9E)
4. **Contact support** — [FalkorDB Support](https://www.falkordb.com/contact-us/)
