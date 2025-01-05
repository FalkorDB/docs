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
for i in {1..6}; do
  docker run -d \
    --name node$i \
    --hostname node$i \
    --network falkordb-cluster-network \
    -p $((6379 + i - 1)):$((6379 + i - 1)) \
    -e BROWSER=0 \
    -e "FALKORDB_ARGS=--port $((6379 + i - 1)) --cluster-enabled yes --cluster-announce-ip node$i --cluster-announce-port $((6379 + i - 1))" \
    falkordb/falkordb
done
```

### 2.2 Edit the /etc/hosts file and add the node container hostnames

For the Redis-cli to be able to connect and automatically switch between nodes for an example when the (MOVED) operation happens,
we have to edit the /etc/hosts file to include the container hostnames.

```bash
for i in {1..6};do
  sudo echo "127.0.0.1 node$i" | sudo tee -a /etc/hosts
done
```


## Step 3: Configuring the Cluster

Once all nodes are up, you need to connect them to form a cluster. Use the redis-cli tool inside one of the nodes to initiate the cluster setup.

### 3.1 Initiate the Cluster

This command will join node1-node6 into a cluster.

```bash
docker exec -it node1 redis-cli --cluster create node1:6379 node2:6380 node3:6381 node4:6382 node5:6383 node6:6384 --cluster-replicas 1 --cluster-yes
```

### 3.3 Verify Cluster Status

You can verify the status of the cluster with:

```bash
docker exec -it node1 redis-cli --cluster check node1:6379
```
This command will display the status of each node and their roles (master/replica).

### 3.4 Create a Graph to test deployment

This will create a graph called testGraph and create nodes with different ids.

We can directly execute the command (does not show that the redis-cli moved):

```bash
redis-cli -c GRAPH.QUERY testGraph "UNWIND range(1, 100) AS id CREATE (n:Person {id: id, name: 'Person ' + toString(id), age: 20 + id % 50})"
```

Or we can run:
A):

```bash
redis-cli -c
```
B):

```bash
GRAPH.QUERY testGraph "UNWIND range(1, 100) AS id CREATE (n:Person {id: id, name: 'Person ' + toString(id), age: 20 + id % 50})"
```
The out put will show that it was moved to the right node:

```
-> Redirected to slot [15841] located at node3:6381
1) 1) "Nodes created: 100"
   2) "Properties set: 300"
   3) "Cached execution: 1"
   4) "Query internal execution time: 0.505416 milliseconds"
```

## Step 4: Scaling the Cluster

You can scale the cluster by adding more nodes as needed. Simply launch additional FalkorDB instances and add them to the cluster using the falkordb-cli tool.

For example, to add a new node:

### 4.1 Start a New Node

```bash
docker run -d \
    --name node7 \
    --hostname node7 \
    --network falkordb-cluster-network \
    -p 6385:6385 \
    -e BROWSER=0 \
    -e "FALKORDB_ARGS=--port 6385 --cluster-enabled yes --cluster-announce-ip node7 --cluster-announce-port 6385" \
    falkordb/falkordb
```

### 4.2 Add the new node to the /etc/hosts file

```bash
sudo echo "127.0.0.1 node7" | sudo tee -a /etc/hosts
```

### 4.3 Add the Node to the Cluster

```bash
docker exec -it node1 redis-cli --cluster add-node node7:6385 node1:6379
```

This will add node7 into the existing cluster.

## Conclusion

With your FalkorDB cluster set up, you now have a scalable, distributed environment that can handle increased loads and provide higher availability. 