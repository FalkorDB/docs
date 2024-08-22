---
title: "Cluster"
nav_order: 3
description: "Configuring FalkorDB Docker for Cluster"
parent: "Operations"
---

# Setting Up a FalkorDB Cluster

Setting up a FalkorDB cluster enables you to distribute your data across multiple nodes, providing horizontal scalability and improved fault tolerance. This guide will walk you through the steps to configure a FalkorDB cluster with 3 masters and 1 replica for each, using Docker.

## Prerequisites

Before you begin, ensure you have the following:

* Docker installed on your machine.
* A working FalkorDB Docker image. You can pull it from Docker Hub.
* Basic knowledge of Docker networking and commands.

## Step 1: Network Configuration

First, create a Docker network to allow communication between the FalkorDB nodes.

```bash
docker network create falkordb-cluster-network
```

This network will enable the containers to communicate with each other.

## Step 2: Launching FalkorDB Nodes

Next, you need to launch multiple FalkorDB instances that will form the cluster. For example, you can start six nodes:

### 2.1 Start the nodes

```bash
docker run -d \
  --name node1 \
  --network falkordb-cluster-network \
  -p 6379:6379 \
  -e 'FALKORDB_ARGS=--cluster-enabled yes' \
  falkordb/falkordb
```

```bash
docker run -d \
  --name node2 \
  --network falkordb-cluster-network \
  -p 6380:6379 \
  -e 'FALKORDB_ARGS=--cluster-enabled yes' \
  falkordb/falkordb
```

```bash
docker run -d \
  --name node3 \
  --network falkordb-cluster-network \
  -p 6381:6379 \
  -e 'FALKORDB_ARGS=--cluster-enabled yes' \
  falkordb/falkordb
```

```bash
docker run -d \
  --name node4 \
  --network falkordb-cluster-network \
  -p 6382:6379 \
  -e 'FALKORDB_ARGS=--cluster-enabled yes' \
  falkordb/falkordb
```

```bash
docker run -d \
  --name node5 \
  --network falkordb-cluster-network \
  -p 6383:6379 \
  -e 'FALKORDB_ARGS=--cluster-enabled yes' \
  falkordb/falkordb
```

```bash
docker run -d \
  --name node6 \
  --network falkordb-cluster-network \
  -p 6384:6379 \
  -e 'FALKORDB_ARGS=--cluster-enabled yes' \
  falkordb/falkordb
```

In this command, the --network falkordb-cluster-network flag connects the container to the network created in Step 1.

## Step 3: Configuring the Cluster

Once all nodes are up, you need to connect them to form a cluster. Use the redis-cli tool inside one of the nodes to initiate the cluster setup.

### 3.1 Connect to a Node

```bash
docker exec -it node1 /bin/bash
```

### 3.2 Initiate the Cluster

Inside the container, use the following command to form the cluster:

```bash
redis-cli --cluster create node1:6379 node2:6379 node3:6379 node4:6379 node5:6379 node6:6379 --cluster-replicas 1
```

This command will join node1, node2, and node3 into a cluster.

### 3.3 Verify Cluster Status

You can verify the status of the cluster with:

```bash
redis-cli --cluster check node1:6379
```
This command will display the status of each node and their roles (master/replica).

## Step 4: Scaling the Cluster

You can scale the cluster by adding more nodes as needed. Simply launch additional FalkorDB instances and add them to the cluster using the falkordb-cli tool.

For example, to add a new node:

### 4.1 Start a New Node

```bash
docker run -d \
  --name node7 \
  --network falkordb-cluster-network \
  -p 6385:6379 \
  -e 'FALKORDB_ARGS=--cluster-enabled yes' \
  falkordb/falkordb
```

### 4.2 Add the Node to the Cluster

```bash
docker exec -it node1 /bin/bash
redis-cli --cluster add-node node7:6379 node1:6379
```

This will add node7 into the existing cluster.

## Conclusion

With your FalkorDB cluster set up, you now have a scalable, distributed environment that can handle increased loads and provide higher availability. 