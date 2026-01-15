---
title: "Railway"
description: "Deploy FalkorDB on Railway"
---

# Deploy FalkorDB on Railway

[Railway](https://railway.com?referralCode=skt6b0&utm_medium=integration&utm_source=button&utm_campaign=generic) is a modern platform-as-a-service (PaaS) that makes it easy to deploy and manage applications. FalkorDB provides verified templates on Railway for quick deployment, enabling you to get started with a graph database in minutes without managing infrastructure.

## Available Templates

FalkorDB offers two verified deployment templates on Railway:

1. **Single Instance** - A standalone FalkorDB instance, ideal for development, testing, and small production workloads
2. **Cluster** - A multi-node FalkorDB cluster for high availability and horizontal scalability

## Prerequisites

Before deploying FalkorDB on Railway, ensure you have:

* A [Railway account](https://railway.com?referralCode=skt6b0&utm_medium=integration&utm_source=button&utm_campaign=generic) (free tier available)
* Basic understanding of FalkorDB and graph databases

## Option 1: Single Instance Deployment

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/new/template/falkordb-1?referralCode=skt6b0&utm_medium=integration&utm_source=button&utm_campaign=generic)

The single instance template deploys a standalone FalkorDB server with the browser interface enabled by default.

### Deploy the Template

1. Visit the [FalkorDB Single Instance template](https://railway.com/deploy/falkordb-1?referralCode=skt6b0&utm_medium=integration&utm_source=button&utm_campaign=generic)
2. Click the **Deploy** button
3. Sign in to your Railway account or create one if needed
4. Railway will automatically provision and deploy your FalkorDB instance
5. Once deployment completes, you'll receive connection details

<img width="722" height="502" alt="image" src="https://github.com/user-attachments/assets/573fbe4a-19a5-42c9-92fb-6c05b60f4d82" />
<img width="603" height="740" alt="image" src="https://github.com/user-attachments/assets/6b0ea2f6-7b85-44b7-80b6-345e811391f2" />

### Accessing Your Instance

After deployment, you can access your FalkorDB instance:

#### Using the Browser Interface

1. Navigate to your Railway project dashboard
2. Click on the FalkorDB service
3. Then click on the public domain to open the browser
<img width="2358" height="628" alt="image" src="https://github.com/user-attachments/assets/895a0039-2b23-4fb3-b9dc-273e94387a1d" />
   
4. Find the FALKORDB_PASSWORD in the service variables settings
5. Use the FALKORDB_PASSWORD in your browser to login to your database
   
Defaults are:
* Host: falkordb.railway.internal
* Port: 16379
* Username: default

<img width="560" height="655" alt="image" src="https://github.com/user-attachments/assets/30237fcc-64c3-45f0-a92e-6f6f6af22ec9" />

#### Connecting via Client

To connect from your application or command line:

Locate the FALKORDB_PRIVATE_URL or the FALKORDB_PUBLIC_URL: 

<img width="2411" height="1208" alt="image" src="https://github.com/user-attachments/assets/e355e2a7-d290-4cdc-b7e5-a3f593f72ecb" />

Connect using `redis-cli`:

```bash
redis-cli -u <FALKORDB_PUBLIC_URL>
```

## Option 2: Cluster Deployment

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/new/template/falkordb-cluster?referralCode=skt6b0&utm_medium=integration&utm_source=button&utm_campaign=generic)

The cluster template deploys a multi-node FalkorDB cluster for production workloads requiring high availability and horizontal scalability.

### Deploy the Template

1. Visit the [FalkorDB Cluster template](https://railway.com/deploy/falkordb-cluster?referralCode=skt6b0&utm_medium=integration&utm_source=button&utm_campaign=generic)
2. Click the **Deploy** button
3. Sign in to your Railway account
4. Railway will provision multiple FalkorDB nodes and configure them as a cluster
5. Wait for all nodes to be deployed and the cluster to be initialized

<img width="1958" height="707" alt="image" src="https://github.com/user-attachments/assets/ca2ab461-4312-4cec-b3b1-b6aeb2e4534f" />

### Cluster Architecture

The FalkorDB cluster template typically includes:

* **Multiple master nodes** - Distribute data across shards
* **Replica nodes** - Provide redundancy and failover capabilities
* **High availability** - Continues operating even if individual nodes fail

### Connecting to the Cluster

To connect to your FalkorDB cluster:

1. Get the cluster endpoint from your Railway project dashboard
2. Use FalkorDB cluster-aware clients for optimal performance

Example with Python:

```python
from falkordb import FalkorDB

# Create connection with cluster support
db = FalkorDB(
    host='<your-railway-cluster-host>',
    port=6379,
    password='<your-password>'
)

# Select a graph
g = db.select_graph('mygraph')

# Execute queries as normal
result = g.query("CREATE (n:Person {name: 'Bob', age: 25})")
result = g.query("MATCH (n:Person) RETURN n.name, n.age")
```

Using `redis-cli` with cluster mode:

```bash
export REDISCLI_AUTH="<your-password>"
redis-cli -c -h <your-railway-cluster-host> -p 6379
```

## Best Practices

### Data Persistence

The template provides persistent volumes for data storage:

* Data persists across deployments and restarts
* Regular backups are recommended for production workloads
* Consider implementing your own backup strategy for critical data

## Monitoring and Logs

Railway provides built-in monitoring and logging:

1. Navigate to your FalkorDB service in the Railway dashboard
2. View real-time logs in the **Logs** tab
3. Monitor metrics in the **Metrics** tab
4. Set up alerts for service health and resource usage
