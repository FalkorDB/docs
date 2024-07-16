---
title: "Kubernetes support"
nav_order: 9
description: "Deploy FalkorDB to Kubernetes."
---

# Kubernetes support for FalkorDB

FalkorDB can be deployed on Kubernetes using Helm charts and Docker images. This guide will walk you through the process.

## Prerequisites

Before you begin, make sure you have Helm installed on your Kubernetes cluster.

To deploy FalkorDB to Kubernetes we need to use:

* [Helm charts](https://bitnami.com/stack/redis/helm)
* [Docker image](https://hub.docker.com/r/falkordb/falkordb)

And follow these steps:

## Step 1: Create a `values.yaml` File

Create a values.yaml file with the following content:

```yaml
image:
  registry: docker.io
  repository: falkordb/falkordb
  tag: "4.0"

master:
  extraFlags:
  - "--loadmodule /FalkorDB/bin/linux-x64-release/src/falkordb.so"

replica:
  extraFlags:
  - "--loadmodule /FalkorDB/bin/linux-x64-release/src/falkordb.so"
```

This file specify the FalkorDB image(you can choose different tags)
and configure the master and slave to load the FalkorDB module.
For additional configurations [see the official Helm chart documentation](https://github.com/bitnami/charts/blob/main/bitnami/redis/values.yaml)

## Step 2: Install FalkorDB Helm Charts
Install the helm charts using the following command:

```bash
helm install -f values.yaml my-falkordb oci://registry-1.docker.io/bitnamicharts/redis
```

This command deploys FalkorDB with the configuration from values.yaml.
After running this command, instructions on how to connect to the FalkorDB server will be displayed.

## Step 3: Retrieve the FalkorDB Password

To connect to FalkorDB, you need the Redis password. Retrieve it using the following command:

```bash
export REDIS_PASSWORD=$(kubectl get secret --namespace default my-release-redis -o jsonpath="{.data.redis-password}" | base64 -d)
```

## Step 4: Enable External Connections

In a new terminal, run the following command to port-forward to the FalkorDB server, allowing external connections:

```bash
kubectl port-forward --namespace default svc/my-falkordb-redis-master 6379:6379
```

## Step 5: Connect to FalkorDB Using `redis-cli`

You can now connect to FalkorDB using redis-cli with the following command:

```bash
REDISCLI_AUTH="$REDIS_PASSWORD" redis-cli -h 127.0.0.1 -p 6379
```

## Step 6: Run a Simple Cypher Query

To test your FalkorDB installation, run a simple Cypher query:

```
GRAPH.QUERY mygraph "UNWIND range(1, 10) AS i RETURN i"
```

The output should resemble the following:

```
127.0.0.1:6379> GRAPH.QUERY mygraph "UNWIND range(1, 10) AS i RETURN i"
1) 1) "i"
2)  1) 1) (integer) 1
    2) 1) (integer) 2
    3) 1) (integer) 3
    4) 1) (integer) 4
    5) 1) (integer) 5
    6) 1) (integer) 6
    7) 1) (integer) 7
    8) 1) (integer) 8
    9) 1) (integer) 9
   10) 1) (integer) 10
3) 1) "Cached execution: 0"
   2) "Query internal execution time: 0.290600 milliseconds"
```

In summary, this guide provides steps for deploying FalkorDB on Kubernetes using Helm charts and Docker images. It covers the creation of a values.yaml file for configuration, Helm chart installation, password retrieval, enabling external connections, connecting to FalkorDB with redis-cli, and running a basic Cypher query for verification. We hope this documentation helped you to set up FalkorDB in your Kubernetes environment. If you have any questions or encounter any issues during the process, please don't hesitate to reach out for assistance. Thank you for choosing FalkorDB!
