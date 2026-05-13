---
title: "Railway"
nav_order: 5
description: "Deploy FalkorDB on Railway with verified templates for single-instance or cluster configurations. Includes connection, persistence, and production guidance."
parent: "Operations"
---

# Deploy FalkorDB on Railway

[Railway](https://railway.com?referralCode=skt6b0&utm_medium=integration&utm_source=button&utm_campaign=generic) is a modern platform-as-a-service (PaaS) that makes it easy to deploy and manage applications. FalkorDB provides verified Railway templates so you can start a graph database in minutes without managing infrastructure.

## Available Templates

FalkorDB offers two verified deployment templates on Railway. Choose the template that matches your workload:

| Template | Best for | Notes |
| --- | --- | --- |
| **Single Instance** | Development, testing, demos, and small production workloads | Runs one FalkorDB instance with the Browser enabled by default. Use Railway volumes and backups for persistence. |
| **Cluster** | Production workloads that need high availability or horizontal scaling across multiple graphs | Runs multiple FalkorDB nodes. Each graph is stored as a single Redis key and belongs to one hash slot, so a single large graph is not automatically split across shards. |

## Prerequisites

Before deploying FalkorDB on Railway, ensure you have:

* A [Railway account](https://railway.com?referralCode=skt6b0&utm_medium=integration&utm_source=button&utm_campaign=generic)
* Basic understanding of FalkorDB and graph databases
* A Redis-compatible client, such as `redis-cli`, for command-line testing

## Option 1: Single Instance Deployment

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/new/template/falkordb-1?referralCode=skt6b0&utm_medium=integration&utm_source=button&utm_campaign=generic)

The single instance template deploys a standalone FalkorDB server with the browser interface enabled by default.

### Deploy the Template

1. Visit the [FalkorDB Single Instance template](https://railway.com/deploy/falkordb-1?referralCode=skt6b0&utm_medium=integration&utm_source=button&utm_campaign=generic)
2. Click the **Deploy** button
3. Sign in to your Railway account or create one if needed
4. Railway will automatically provision and deploy your FalkorDB instance
5. Once deployment completes, open the service **Variables** tab to review the generated connection details

<img width="722" height="502" alt="Railway template deployment screen for FalkorDB" src="https://github.com/user-attachments/assets/573fbe4a-19a5-42c9-92fb-6c05b60f4d82" />
<img width="603" height="740" alt="Railway deployment progress screen for FalkorDB" src="https://github.com/user-attachments/assets/6b0ea2f6-7b85-44b7-80b6-345e811391f2" />

### Accessing Your Instance

After deployment, you can access FalkorDB through the Browser UI, from another Railway service, or from your local machine. These paths use different endpoints:

| Endpoint or variable | Use it for | Reachability |
| --- | --- | --- |
| `RAILWAY_PUBLIC_DOMAIN` | Opening the FalkorDB Browser over HTTPS | Public internet |
| `FALKORDB_PRIVATE_URL` | Application services running in the same Railway project and environment | Railway private network only |
| `FALKORDB_PUBLIC_URL` | Local development, external clients, or `redis-cli` outside Railway | Public TCP proxy, if enabled |
| `FALKORDB_PASSWORD` | Browser login and client authentication | Secret value in Railway service variables |

#### Using the Browser Interface

1. Navigate to your Railway project dashboard
2. Click on the FalkorDB service
3. Click the public domain to open the FalkorDB Browser

<img width="2358" height="628" alt="Railway service page showing the public domain for the FalkorDB Browser" src="https://github.com/user-attachments/assets/895a0039-2b23-4fb3-b9dc-273e94387a1d" />

4. Find `FALKORDB_PASSWORD` in the service **Variables** tab
5. Use `FALKORDB_PASSWORD` in your browser to log in to your database

If the Browser prompts for connection fields, copy the current values from your Railway service **Variables** tab (`FALKORDB_HOST`, `FALKORDB_PORT`, and the username shown there) and authenticate with `FALKORDB_PASSWORD`.

<img width="560" height="655" alt="FalkorDB Browser login screen with host, port, username, and password fields" src="https://github.com/user-attachments/assets/30237fcc-64c3-45f0-a92e-6f6f6af22ec9" />

#### Connecting from Another Railway Service

Use the private URL when your application runs in the same Railway project and environment as FalkorDB. Private networking keeps database traffic inside Railway and avoids exposing the FalkorDB protocol port to the public internet.

1. Open the FalkorDB service **Variables** tab
2. Copy `FALKORDB_PRIVATE_URL`
3. Add it as a variable to your application service, or reference it from the application service

Example with Python:

```python
import os

from falkordb import FalkorDB

db = FalkorDB.from_url(os.environ["FALKORDB_PRIVATE_URL"])
graph = db.select_graph("mygraph")

result = graph.query("RETURN 'connected' AS status")
print(result.result_set)
```

Private URLs are not reachable from your laptop or from services in other Railway projects or environments.

#### Connecting from Your Local Machine

For local development or external clients, use `FALKORDB_PUBLIC_URL`.

<img width="2411" height="1208" alt="Railway Variables tab showing FalkorDB private and public connection URLs" src="https://github.com/user-attachments/assets/e355e2a7-d290-4cdc-b7e5-a3f593f72ecb" />

Connect using `redis-cli` and run a test query in a single invocation:

```bash
redis-cli -u "$FALKORDB_PUBLIC_URL" GRAPH.QUERY mygraph "RETURN 'connected' AS status"
```

If `FALKORDB_PUBLIC_URL` is not available, enable a [Railway TCP Proxy](https://docs.railway.com/networking/tcp-proxy) for the FalkorDB service and expose the internal FalkorDB protocol port.

## Option 2: Cluster Deployment

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/new/template/falkordb-cluster?referralCode=skt6b0&utm_medium=integration&utm_source=button&utm_campaign=generic)

The cluster template deploys a multi-node FalkorDB cluster for production workloads requiring high availability and horizontal scalability across graph keys.

### Deploy the Template

1. Visit the [FalkorDB Cluster template](https://railway.com/deploy/falkordb-cluster?referralCode=skt6b0&utm_medium=integration&utm_source=button&utm_campaign=generic)
2. Click the **Deploy** button
3. Sign in to your Railway account
4. Railway will provision multiple FalkorDB nodes and configure them as a cluster
5. Wait for all nodes to be deployed and the cluster to be initialized

<img width="1958" height="707" alt="Railway project canvas showing the FalkorDB cluster template services" src="https://github.com/user-attachments/assets/ca2ab461-4312-4cec-b3b1-b6aeb2e4534f" />

### Cluster Architecture

FalkorDB Cluster uses Redis Cluster hash slots to distribute graph keys across primary nodes:

* **Primary nodes** - Own hash slot ranges and serve writes for the graphs assigned to those slots
* **Replica nodes** - Provide redundancy and failover for primaries
* **Cluster-aware clients** - Follow Redis Cluster redirects and route commands to the node that owns the target graph key

Each graph lives on one shard. Clustering helps when you have many graphs or workloads that can be distributed across graph names; it does not partition a single graph across multiple shards. For more details, see [Setting Up a FalkorDB Cluster](/operations/cluster).

### Connecting to the Cluster

To connect to your FalkorDB cluster:

1. **Apps deployed within Railway** – use `FALKORDB_PRIVATE_URL`. Traffic stays inside Railway's private network and never touches the public internet.
2. **External clients and local development** – use `FALKORDB_PUBLIC_URL`. This requires a Railway TCP Proxy to be enabled for the FalkorDB service.
3. Use cluster-aware clients so `MOVED` redirects are handled correctly.

Example with Python (internal app — swap in `FALKORDB_PUBLIC_URL` for external access):

```python
import os

from falkordb import FalkorDB

# Internal: use FALKORDB_PRIVATE_URL for apps running inside the same Railway project
# External: replace with FALKORDB_PUBLIC_URL for local development or external clients
# FalkorDB.from_url() automatically detects cluster mode at connection time
# (probes INFO server) so no extra cluster flag is needed.
db = FalkorDB.from_url(os.environ["FALKORDB_PRIVATE_URL"])

graph = db.select_graph("mygraph")

graph.query("CREATE (:Person {name: 'Bob', age: 25})")
result = graph.query("MATCH (n:Person) RETURN n.name, n.age")
```

Using `redis-cli` in cluster mode:

```bash
# From inside Railway (private endpoint)
redis-cli -c -u "$FALKORDB_PRIVATE_URL"

# From your local machine or an external client (public endpoint)
redis-cli -c -u "$FALKORDB_PUBLIC_URL"
```

## Best Practices

### Security

* Use `FALKORDB_PRIVATE_URL` for production application traffic whenever possible
* Expose `FALKORDB_PUBLIC_URL` only when you need local or external access
* Treat `FALKORDB_PASSWORD` and connection URLs as secrets
* Rotate credentials if they are copied into logs, tickets, or shared terminals
* Disable public access paths that are not required for your workload

### Data Persistence

The template provides persistent Railway volumes for FalkorDB data storage:

* Data persists across deployments and restarts
* Volumes are mounted when the service starts, not during build time
* Regular backups are recommended for production workloads
* Persistence protects against container restarts, but it is not a replacement for backups

For production deployments:

1. Confirm the FalkorDB data directory is backed by a Railway volume
2. Configure manual or automated Railway volume backups
3. Review FalkorDB durability settings for RDB snapshots and AOF logging in [Data Durability](/operations/durability)

## Monitoring and Logs

Railway provides built-in monitoring and logging:

1. Navigate to your FalkorDB service in the Railway dashboard
2. View real-time logs in the **Logs** tab
3. Monitor metrics in the **Metrics** tab
4. Set up alerts for service health and resource usage

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| Browser login fails | Confirm the username is `default`, copy the latest `FALKORDB_PASSWORD`, and use the `FALKORDB_HOST` and `FALKORDB_PORT` values from your Railway service **Variables** tab. |
| Local `redis-cli` cannot connect | Use `FALKORDB_PUBLIC_URL`, not `FALKORDB_PRIVATE_URL`. Private URLs only work inside the same Railway project and environment. |
| `FALKORDB_PUBLIC_URL` is missing | Enable Railway TCP Proxy for the FalkorDB service and expose the internal FalkorDB protocol port. |
| Application cannot connect from Railway | Confirm both services are in the same project and environment, then use `FALKORDB_PRIVATE_URL`. |
| Cluster client receives `MOVED` replies | Use a cluster-aware client or `redis-cli -c`. |
| Data is missing after redeploy | Confirm the FalkorDB data directory is mounted on a Railway volume and review the service logs for startup errors. |

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="How long does it take to deploy FalkorDB on Railway?"
  a1="Deployment typically completes in under 2 minutes. Railway provisions the service, pulls the Docker image, and starts FalkorDB automatically from the verified template."
  q2="What is the difference between FALKORDB_PRIVATE_URL and FALKORDB_PUBLIC_URL?"
  a2="**Private URLs** only work within the same Railway project and environment (service-to-service). **Public URLs** use a Railway TCP Proxy and are reachable from your local machine or external clients."
  q3="Does my data persist across Railway redeployments?"
  a3="Yes, if the FalkorDB data directory is mounted on a Railway volume. Volumes persist across deployments and restarts. Without a volume, data is lost on redeploy."
  q4="Can I deploy a FalkorDB cluster on Railway?"
  a4="Yes. Use the [FalkorDB Cluster template](https://railway.com/deploy/falkordb-cluster) which provisions multiple nodes. You need a cluster-aware client to handle `MOVED` redirects."
  q5="How do I connect from my local machine to Railway FalkorDB?"
  a5="Use `FALKORDB_PUBLIC_URL` with `redis-cli -u`. If the public URL is not available, enable Railway TCP Proxy for the FalkorDB service and expose the internal FalkorDB protocol port."
%}
