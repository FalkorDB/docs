---
title: "Cluster"
nav_order: 2
description: "Configuring FalkorDB Docker for Cluster"
---

# Setting Up a FalkorDB Cluster

Setting up a FalkorDB cluster enables you to distribute your data across multiple nodes, providing horizontal scalability and improved fault tolerance. This guide will walk you through the steps to configure a FalkorDB cluster using Docker.

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

Next, you need to launch multiple FalkorDB instances that will form the cluster. For example, you can start three nodes:

### 2.1 Start the First Node

```bash
docker run -d \
  --name falkordb-node1 \
  --net falkordb-cluster-network \
  -e CLUSTER_MODE=enabled \
  -e CLUSTER_ID=node1 \
  falkordb/falkordb
```

### 2.2 Start the Second Node

```bash
docker run -d \
  --name falkordb-node2 \
  --net falkordb-cluster-network \
  -e CLUSTER_MODE=enabled \
  -e CLUSTER_ID=node2 \
  falkordb/falkordb
```

### 2.3 Start the Third Node

```bash
docker run -d \
  --name falkordb-node3 \
  --net falkordb-cluster-network \
  -e CLUSTER_MODE=enabled \
  -e CLUSTER_ID=node3 \
  falkordb/falkordb
```

In these commands:

* The --net falkordb-cluster-network flag connects the container to the network created in Step 1.
* The -e CLUSTER_MODE=enabled flag enables clustering mode.
* The -e CLUSTER_ID flag assigns a unique identifier to each node.

## Step 3: Configuring the Cluster

Once all nodes are up, you need to connect them to form a cluster. Use the falkordb-cli tool inside one of the nodes to initiate the cluster setup.

### 3.1 Connect to a Node

```bash
docker exec -it falkordb-node1 /bin/bash
```

### 3.2 Initiate the Cluster

Inside the container, use the following command to form the cluster:

```bash
redis-cli cluster create node1 node2 node3
```

This command will join node1, node2, and node3 into a cluster.

### 3.3 Verify Cluster Status

You can verify the status of the cluster with:

```bash
redis-cli cluster status
```

This command will display the status of each node and their roles (master/replica).

## Step 4: Scaling the Cluster

You can scale the cluster by adding more nodes as needed. Simply launch additional FalkorDB instances and add them to the cluster using the falkordb-cli tool.

For example, to add a new node:

### 4.1 Start a New Node

```bash
docker run -d \
  --name falkordb-node4 \
  --net falkordb-cluster-network \
  -e CLUSTER_MODE=enabled \
  -e CLUSTER_ID=node4 \
  falkordb/falkordb
```

### 4.2 Add the Node to the Cluster

```bash
docker exec -it falkordb-node1 /bin/bash
redis-cli cluster add node4
```

This will integrate node4 into the existing cluster.

## Conclusion

With your FalkorDB cluster set up, you now have a scalable, distributed environment that can handle increased loads and provide higher availability. 