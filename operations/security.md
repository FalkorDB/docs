---
title: "Security"
parent: "Operations"
nav_order: 13
description: "Security guide for FalkorDB covering authentication, ACL access control, TLS encryption, network isolation, and least-privilege patterns for production deployments."
---

# Security Guide

This guide consolidates FalkorDB's security features into a single reference. It covers authentication, access control lists (ACLs), TLS encryption, network isolation, and least-privilege design patterns for production environments.

---

## 1. Authentication

FalkorDB uses the Redis authentication mechanism. Enable a global password with the `requirepass` directive to prevent unauthenticated access.

### Docker

```bash
docker run -p 6379:6379 -p 3000:3000 -it \
  -e REDIS_ARGS="--requirepass <your-strong-password>" \
  --rm falkordb/falkordb:latest
```

### Docker Compose

```yaml
services:
  falkordb:
    image: falkordb/falkordb:latest
    ports:
      - "6379:6379"
      - "3000:3000"
    environment:
      - REDIS_ARGS=--requirepass <your-strong-password>
```

### Connecting with Authentication

When authentication is enabled, clients must provide the password before executing any commands:

```python
from falkordb import FalkorDB

db = FalkorDB(host='localhost', port=6379, password='<your-strong-password>')
```

> **Tip:** For production, use a strong, randomly generated password and store it in a secrets manager rather than in plain text configuration files.

---

## 2. Access Control Lists (ACLs)

ACLs provide fine-grained, per-user access control. Each user can be granted or restricted to specific commands and graph patterns.

### Creating Users

```
ACL SETUSER analyst on >analyst-password ~analytics_* +GRAPH.RO_QUERY +GRAPH.EXPLAIN -GRAPH.DELETE
```

This creates a user `analyst` who can only run read-only queries and explain plans on graphs matching `analytics_*`.

### Graph Permissions

FalkorDB extends ACL with graph-level read/write permissions:

| Permission | Description |
|:---|:---|
| `%R~<pattern>` | Read-only access to matching graphs |
| `%W~<pattern>` | Write-only access to matching graphs |
| `%RW~<pattern>` | Full access (equivalent to `~<pattern>`) |

**Example — read-only user for a specific graph:**

```
ACL SETUSER readonly_user on >secure-password %R~production_graph +GRAPH.RO_QUERY -GRAPH.QUERY -GRAPH.DELETE
```

### Persisting ACL Users

By default, `ACL SETUSER` only updates the in-memory user table. Users are lost on restart unless you persist them.

**Recommended approach — ACL file:**

1. Mount an ACL file into the container
2. Set the `aclfile` directive
3. Run `ACL SAVE` after any changes

See [ACL Persistence on Docker](/operations/durability/acl-persistence) for a complete step-by-step guide.

### Listing and Inspecting Users

```
ACL LIST                    # List all users and their rules
ACL GETUSER <username>      # Inspect a specific user's permissions
ACL DELUSER <username>      # Remove a user
```

For the full command reference, see [ACL Commands](/commands/acl).

---

## 3. TLS / SSL Encryption

TLS encrypts all communication between clients and the FalkorDB server, preventing eavesdropping and man-in-the-middle attacks.

### Self-Hosted TLS Configuration

FalkorDB supports TLS through Redis's native TLS support. You need:

- A **certificate** file (server.crt)
- A **private key** file (server.key)
- A **CA certificate** file (ca.crt) for client verification

**Docker example:**

```bash
docker run -p 6379:6379 -it \
  -v /path/to/certs:/tls:ro \
  -e REDIS_ARGS="--tls-port 6379 --port 0 \
    --tls-cert-file /tls/server.crt \
    --tls-key-file /tls/server.key \
    --tls-ca-cert-file /tls/ca.crt" \
  --rm falkordb/falkordb-server:latest
```

> **Note:** Setting `--port 0` disables the non-TLS port, ensuring all connections are encrypted.

**Connecting with TLS (Python):**

```python
from falkordb import FalkorDB

db = FalkorDB(
    host='localhost',
    port=6379,
    ssl=True,
    ssl_ca_certs='/path/to/ca.crt'
)
```

### FalkorDB Cloud

FalkorDB Cloud provides TLS on all paid tiers (Startup, Pro, Enterprise) with certificates managed automatically. No additional configuration is required — connect using the `rediss://` (note double `s`) URL scheme provided in your Cloud dashboard.

---

## 4. Network Isolation

Restrict which hosts and networks can reach your FalkorDB instance.

### Bind Address

By default, Redis binds to all interfaces (`0.0.0.0`). In production, restrict binding to specific interfaces:

```bash
docker run -p 127.0.0.1:6379:6379 -it \
  -e REDIS_ARGS="--bind 127.0.0.1" \
  --rm falkordb/falkordb-server:latest
```

### Docker Networks

Use Docker networks to isolate FalkorDB so only your application containers can reach it:

```yaml
services:
  app:
    image: your-app:latest
    networks:
      - backend

  falkordb:
    image: falkordb/falkordb-server:latest
    networks:
      - backend
    # No ports published to host — only accessible from the backend network

networks:
  backend:
    driver: bridge
```

### Kubernetes Network Policies

When deploying on Kubernetes, use NetworkPolicy resources to restrict which pods can communicate with FalkorDB:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: falkordb-access
spec:
  podSelector:
    matchLabels:
      app: falkordb
  ingress:
    - from:
        - podSelector:
            matchLabels:
              role: app-server
      ports:
        - port: 6379
```

### Firewall Rules

For self-hosted deployments, ensure:

- Port **6379** (FalkorDB server) is not exposed to the public internet
- Port **3000** (FalkorDB Browser) is restricted to trusted networks or VPN
- Use a reverse proxy with authentication for any web-facing access

---

## 5. Least-Privilege Patterns

Follow these patterns to minimize the blast radius of a compromised credential:

### Separate Read and Write Users

```
# Application user — read/write on its own graphs
ACL SETUSER app_user on >app-secret ~myapp_* +GRAPH.QUERY +GRAPH.RO_QUERY

# Analytics user — read-only across all graphs
ACL SETUSER analytics on >analytics-secret %R~* +GRAPH.RO_QUERY +GRAPH.EXPLAIN +GRAPH.PROFILE

# Admin user — full access (use sparingly)
ACL SETUSER admin on >admin-secret ~* +@all
```

### Disable the Default User

In production, disable the default (passwordless) user and create named users instead:

```
ACL SETUSER default off
```

> **Warning:** Make sure you have at least one admin user configured before disabling the default user, or you will lock yourself out.

### Restrict Dangerous Commands

Prevent non-admin users from running commands that could affect the whole server:

```
ACL SETUSER app_user ... -GRAPH.DELETE -FLUSHALL -FLUSHDB -CONFIG -SHUTDOWN -DEBUG
```

---

## 6. Security Checklist

Use this checklist when preparing a FalkorDB deployment for production:

- [ ] **Authentication enabled** — `requirepass` or ACL users configured
- [ ] **Default user disabled** — `ACL SETUSER default off`
- [ ] **TLS enabled** — non-TLS port disabled (`--port 0`)
- [ ] **Network isolated** — FalkorDB not exposed to public internet
- [ ] **ACL users persisted** — ACL file mounted and `ACL SAVE` run
- [ ] **Least-privilege applied** — each user has minimum required permissions
- [ ] **Browser access restricted** — port 3000 not publicly accessible, or using `falkordb-server` image
- [ ] **Secrets managed** — passwords stored in a secrets manager, not in code

---

## Related Pages

- [ACL Commands](/commands/acl) — Full ACL command reference
- [ACL Persistence on Docker](/operations/durability/acl-persistence) — Persist ACL users across restarts
- [Docker Deployment](/operations/docker) — Docker configuration including authentication
- [Configuration](/getting-started/configuration) — FalkorDB configuration parameters
- [FalkorDB Cloud](/cloud) — Managed deployment with built-in TLS and security
