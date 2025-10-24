---
title: "Railway"
nav_order: 5
description: "Deploy FalkorDB on Railway"
parent: "Operations"
---

# Deploy FalkorDB on Railway

[Railway](https://railway.app) is a modern platform-as-a-service (PaaS) that makes it easy to deploy and manage applications. FalkorDB provides verified templates on Railway for quick deployment, enabling you to get started with a graph database in minutes without managing infrastructure.

## Available Templates

FalkorDB offers two verified deployment templates on Railway:

1. **Single Instance** - A standalone FalkorDB instance, ideal for development, testing, and small production workloads
2. **Cluster** - A multi-node FalkorDB cluster for high availability and horizontal scalability

## Prerequisites

Before deploying FalkorDB on Railway, ensure you have:

* A [Railway account](https://railway.app) (free tier available)
* Basic understanding of FalkorDB and graph databases

## Option 1: Single Instance Deployment

The single instance template deploys a standalone FalkorDB server with the browser interface enabled by default.

### Deploy the Template

1. Visit the [FalkorDB Single Instance template](https://railway.com/deploy/falkordb-1)
2. Click the **Deploy** button
3. Sign in to your Railway account or create one if needed
4. Railway will automatically provision and deploy your FalkorDB instance
5. Once deployment completes, you'll receive connection details

### Accessing Your Instance

After deployment, you can access your FalkorDB instance:

#### Using the Browser Interface

1. Navigate to your Railway project dashboard
2. Click on the FalkorDB service
3. Find the public URL in the service settings
4. Open the URL in your browser to access the FalkorDB Browser interface

#### Connecting via Client

To connect from your application or command line:

1. Get your connection details from Railway:
   - **Host**: Available in the service's public domain
   - **Port**: Default is `6379`
   - **Password**: Set via the `REDIS_PASSWORD` environment variable

2. Connect using `redis-cli`:

```bash
redis-cli -h <your-railway-host> -p 6379 -a <your-password>
```

3. Test with a simple Cypher query:

```
GRAPH.QUERY mygraph "CREATE (n:Person {name: 'Alice', age: 30})"
GRAPH.QUERY mygraph "MATCH (n:Person) RETURN n"
```

### Configuration

You can customize your deployment through Railway environment variables:

* `REDIS_PASSWORD` - Set a custom password for your instance
* `BROWSER` - Enable/disable the browser interface (default: `1` for enabled)
* `FALKORDB_ARGS` - Pass additional FalkorDB configuration arguments

To modify environment variables:
1. Go to your Railway project dashboard
2. Click on the FalkorDB service
3. Navigate to the **Variables** tab
4. Add or modify variables as needed

## Option 2: Cluster Deployment

The cluster template deploys a multi-node FalkorDB cluster for production workloads requiring high availability and horizontal scalability.

### Deploy the Template

1. Visit the [FalkorDB Cluster template](https://railway.com/deploy/falkordb-cluster)
2. Click the **Deploy** button
3. Sign in to your Railway account
4. Railway will provision multiple FalkorDB nodes and configure them as a cluster
5. Wait for all nodes to be deployed and the cluster to be initialized

### Cluster Architecture

The FalkorDB cluster template typically includes:

* **Multiple master nodes** - Distribute data across shards
* **Replica nodes** - Provide redundancy and failover capabilities
* **Automatic sharding** - Data is automatically distributed across nodes
* **High availability** - Continues operating even if individual nodes fail

### Connecting to the Cluster

To connect to your FalkorDB cluster:

1. Get the cluster endpoint from your Railway project dashboard
2. Use Redis cluster-aware clients for optimal performance

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
redis-cli -c -h <your-railway-cluster-host> -p 6379 -a <your-password>
```

The `-c` flag enables cluster mode, allowing the client to follow redirections between nodes.

### Cluster Configuration

Configure your cluster through Railway environment variables:

* `REDIS_PASSWORD` - Cluster-wide authentication password
* `FALKORDB_ARGS` - Additional configuration for cluster nodes
* Node-specific settings available in the template configuration

## Best Practices

### Security

* **Set a strong password** - Always configure `REDIS_PASSWORD` with a secure value
* **Use private networking** - When possible, keep your database on Railway's private network
* **Enable TLS** - Use encrypted connections for production workloads
* **Restrict access** - Configure Railway's networking rules to limit access to trusted sources

### Performance

* **Choose the right plan** - Select a Railway plan that matches your workload requirements
* **Monitor resources** - Use Railway's monitoring tools to track CPU, memory, and network usage
* **Scale appropriately** - Start with a single instance for development, use clusters for production
* **Connection pooling** - Implement connection pooling in your application for better performance

### Data Persistence

Railway provides persistent volumes for data storage:

* Data persists across deployments and restarts
* Regular backups are recommended for production workloads
* Consider implementing your own backup strategy for critical data

## Monitoring and Logs

Railway provides built-in monitoring and logging:

1. Navigate to your FalkorDB service in the Railway dashboard
2. View real-time logs in the **Logs** tab
3. Monitor metrics in the **Metrics** tab
4. Set up alerts for service health and resource usage

## Scaling

### Vertical Scaling (Single Instance)

To scale a single instance vertically:

1. Go to your Railway project
2. Select your FalkorDB service
3. Navigate to **Settings**
4. Upgrade your Railway plan for more resources

### Horizontal Scaling (Cluster)

The cluster template provides built-in horizontal scaling:

* Data is automatically sharded across nodes
* Add more replicas for read scalability
* Modify the cluster configuration to add nodes

## Troubleshooting

### Connection Issues

If you can't connect to your FalkorDB instance:

1. Verify the service is running in the Railway dashboard
2. Check that you're using the correct host, port, and password
3. Ensure your network/firewall allows outbound connections to Railway
4. Review service logs for error messages

### Performance Issues

If experiencing slow performance:

1. Check resource usage in Railway metrics
2. Consider upgrading to a higher-tier plan
3. For clusters, ensure your client is cluster-aware
4. Review query performance using `GRAPH.PROFILE`

### Data Loss

If data appears to be lost:

1. Check that persistent volumes are properly configured
2. Review service logs for errors during startup
3. Verify the service didn't restart with a fresh volume
4. Contact Railway support for assistance with volume recovery

## Cost Optimization

* **Start small** - Begin with the free tier or basic plan for development
* **Scale as needed** - Upgrade only when your workload requires it
* **Use clusters wisely** - Reserve cluster deployments for production needs
* **Monitor usage** - Keep track of resource consumption to avoid unexpected costs

## Migration from Railway

If you need to migrate your data from Railway to another environment:

1. **Export your data** - Use `GRAPH.DUMP` or backup commands
2. **Set up destination** - Prepare your new FalkorDB instance
3. **Transfer data** - Use FalkorDB import tools or restore from backup
4. **Verify** - Test your application with the new instance
5. **Switch** - Update connection strings and decommission Railway instance

## Additional Resources

* [Railway Documentation](https://docs.railway.app)
* [FalkorDB Documentation](/index)
* [FalkorDB Docker Setup](/getting-started)
* [FalkorDB Kubernetes Deployment](/operations/k8s_support)
* [FalkorDB Cluster Setup](/operations/cluster)
* [FalkorDB Cloud](https://app.falkordb.cloud) - Managed alternative

## Getting Help

If you encounter issues deploying FalkorDB on Railway:

1. Check the [Railway Community Forum](https://help.railway.app)
2. Review the [FalkorDB GitHub Issues](https://github.com/FalkorDB/FalkorDB/issues)
3. Join the [FalkorDB Discord](https://discord.gg/ErBEqN9E) for community support
4. Contact Railway support for platform-specific issues

Railway makes it simple to deploy FalkorDB for development and production use cases. Choose the template that matches your needs and get started with graph databases in minutes!
