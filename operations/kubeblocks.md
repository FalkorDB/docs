---
title: "KubeBlocks"
nav_order: 10
description: "Deploy FalkorDB on Kubernetes with KubeBlocks"
parent: "Operations"
---

# Deploy FalkorDB with KubeBlocks

[KubeBlocks](https://kubeblocks.io) is a cloud-native database management operator that simplifies the deployment and management of databases on Kubernetes. This guide demonstrates how to deploy and manage FalkorDB using the KubeBlocks operator.

## What is KubeBlocks?

KubeBlocks is an open-source Kubernetes operator designed to manage stateful workloads, particularly databases. It provides:

* **Unified Management**: Manage multiple database engines through a consistent API
* **Day-2 Operations**: Automated scaling, backup, restore, monitoring, and failover
* **Production-Ready**: Built for production environments with high availability
* **Multi-Topology Support**: Standalone, replication, and sharding configurations

## Prerequisites

Before you begin, ensure you have:

* Kubernetes cluster >= v1.21
* `kubectl` installed - [Installation Guide](https://kubernetes.io/docs/tasks/tools/)
* `helm` installed - [Installation Guide](https://helm.sh/docs/intro/install/)
* KubeBlocks installed and running

## Installing KubeBlocks

If you haven't installed KubeBlocks yet, follow these steps:

### Step 1: Install KubeBlocks Operator

```bash
# Add the KubeBlocks Helm repository
helm repo add kubeblocks https://apecloud.github.io/helm-charts
helm repo update

# Install KubeBlocks
helm install kubeblocks kubeblocks/kubeblocks --namespace kb-system --create-namespace
```

Wait for KubeBlocks to be ready:

```bash
kubectl get pods -n kb-system
```

### Step 2: Install FalkorDB Addon

Enable the FalkorDB addon for KubeBlocks. You can use either the kbcli command-line tool or Helm.

#### Option A: Using kbcli (Recommended)

First, install kbcli:

```bash
# Install kbcli
curl -fsSL https://kubeblocks.io/installer/install_cli.sh | bash

# Verify installation
kbcli version
```

Then install the FalkorDB addon:

```bash
# Install the FalkorDB addon
kbcli addon install falkordb

# Verify the addon is enabled
kbcli addon list | grep falkordb
```

#### Option B: Using Helm

```bash
# Add the KubeBlocks addons Helm repository
helm repo add kubeblocks-addons https://apecloud.github.io/helm-charts
helm repo update

# Install the FalkorDB addon
helm install falkordb-addon kubeblocks-addons/falkordb

# Verify the addon is installed
helm list -A | grep falkordb
```

### Step 3: Create a Namespace

Create a dedicated namespace for your FalkorDB instances:

```bash
kubectl create namespace demo
```

## Deployment Options

KubeBlocks supports three deployment topologies for FalkorDB:

1. **Standalone** - Single instance for development and testing
2. **Replication** - High availability with primary/secondary nodes and Sentinel
3. **Sharding** - Horizontal scalability with multiple shards (Redis Cluster mode)

## Option 1: Standalone Deployment

A standalone deployment is ideal for development, testing, or small workloads.

### Create a Standalone Cluster

Create a file named `falkordb-standalone.yaml`:

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: falkordb-standalone
  namespace: demo
spec:
  terminationPolicy: Delete
  clusterDef: falkordb
  topology: standalone
  componentSpecs:
  - name: falkordb
    replicas: 1
    resources:
      limits:
        cpu: "0.5"
        memory: "0.5Gi"
      requests:
        cpu: "0.5"
        memory: "0.5Gi"
    volumeClaimTemplates:
    - name: data
      spec:
        accessModes:
        - ReadWriteOnce
        resources:
          requests:
            storage: 20Gi
```

Apply the configuration:

```bash
kubectl apply -f falkordb-standalone.yaml
```

Monitor the cluster creation:

```bash
# Check cluster status
kubectl get cluster -n demo falkordb-standalone

# View pods
kubectl get pods -n demo -l app.kubernetes.io/instance=falkordb-standalone
```

## Option 2: Replication Deployment (Recommended)

A replication deployment provides high availability with automatic failover using Redis Sentinel.

### Understanding the Architecture

The replication topology includes:

* **FalkorDB Component**: Primary and secondary nodes for data storage and queries
* **Sentinel Component**: Monitors FalkorDB nodes and manages automatic failover
* **Minimum of 3 Sentinel Replicas**: Required for quorum-based failover decisions

### Create a Replication Cluster

Create a file named `falkordb-replication.yaml`:

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: falkordb-replication
  namespace: demo
spec:
  terminationPolicy: Delete
  clusterDef: falkordb
  topology: replication
  componentSpecs:
  - name: falkordb
    serviceVersion: "4.12.5"
    disableExporter: false
    replicas: 2
    resources:
      limits:
        cpu: "0.5"
        memory: "0.5Gi"
      requests:
        cpu: "0.5"
        memory: "0.5Gi"
    volumeClaimTemplates:
    - name: data
      spec:
        storageClassName: ""
        accessModes:
        - ReadWriteOnce
        resources:
          requests:
            storage: 20Gi
  - name: falkordb-sent
    serviceVersion: "4.12.5"
    replicas: 3
    resources:
      limits:
        cpu: "0.5"
        memory: "0.5Gi"
      requests:
        cpu: "0.5"
        memory: "0.5Gi"
    volumeClaimTemplates:
    - name: data
      spec:
        storageClassName: ""
        accessModes:
        - ReadWriteOnce
        resources:
          requests:
            storage: 20Gi
```

Apply the configuration:

```bash
kubectl apply -f falkordb-replication.yaml
```

### Why Does Sentinel Start First?

KubeBlocks ensures that Sentinel instances start before FalkorDB replicas. This is because:

1. Each FalkorDB replica queries Sentinel on startup to determine if a primary node exists
2. If no primary exists, the replica configures itself as the primary
3. If a primary exists, the replica configures itself as a secondary and begins replication

This startup sequence is defined in the ClusterDefinition and ensures proper cluster initialization.

### Verify the Deployment

Check the cluster status:

```bash
# View cluster information
kubectl get cluster -n demo falkordb-replication

# View all pods
kubectl get pods -n demo -l app.kubernetes.io/instance=falkordb-replication

# Check roles of FalkorDB pods
kubectl get pods -n demo -l app.kubernetes.io/instance=falkordb-replication,apps.kubeblocks.io/component-name=falkordb -L kubeblocks.io/role
```

Expected output shows one `primary` and one or more `secondary` pods.

## Option 3: Sharding Deployment

A sharding deployment distributes data across multiple shards for horizontal scalability.

### Create a Sharding Cluster

Create a file named `falkordb-sharding.yaml`:

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: falkordb-sharding
  namespace: demo
spec:
  terminationPolicy: Delete
  clusterDef: falkordb
  topology: sharding
  shardings:
  - name: shard
    shards: 3
    template:
      name: falkordb
      componentDef: falkordb-cluster-4
      replicas: 2
      serviceVersion: "4.12.5"
      resources:
        limits:
          cpu: "0.5"
          memory: "0.5Gi"
        requests:
          cpu: "0.5"
          memory: "0.5Gi"
      volumeClaimTemplates:
      - name: data
        spec:
          accessModes:
          - ReadWriteOnce
          resources:
            requests:
              storage: 20Gi
```

Apply the configuration:

```bash
kubectl apply -f falkordb-sharding.yaml
```

This creates a cluster with 3 shards, each having 2 replicas (1 primary + 1 secondary).

## Connecting to FalkorDB

### Step 1: Get Connection Credentials

Retrieve the password for your FalkorDB instance:

```bash
# For replication cluster
kubectl get secret -n demo falkordb-replication-conn-credential -o jsonpath='{.data.password}' | base64 -d
```

### Step 2: Port Forward to the Cluster

Enable local access to the FalkorDB service:

```bash
# For standalone
kubectl port-forward -n demo svc/falkordb-standalone-falkordb 6379:6379

# For replication
kubectl port-forward -n demo svc/falkordb-replication-falkordb 6379:6379

# For sharding
kubectl port-forward -n demo svc/falkordb-sharding-shard-5rf-falkordb 6379:6379
```

### Step 3: Connect Using redis-cli

Connect to your FalkorDB instance:

```bash
redis-cli -h 127.0.0.1 -p 6379 -a <your-password>
```

### Step 4: Run a Test Query

Execute a simple Cypher query to verify the connection:

```
GRAPH.QUERY social "CREATE (:Person {name: 'Alice', age: 30})-[:KNOWS]->(:Person {name: 'Bob', age: 25})"
GRAPH.QUERY social "MATCH (p:Person) RETURN p.name, p.age"
```

## Day-2 Operations

KubeBlocks provides comprehensive Day-2 operations for managing your FalkorDB clusters.

### Horizontal Scaling

#### Scale Out

Add more replicas to your cluster:

```yaml
apiVersion: operations.kubeblocks.io/v1alpha1
kind: OpsRequest
metadata:
  name: falkordb-scale-out
  namespace: demo
spec:
  clusterName: falkordb-replication
  type: HorizontalScaling
  horizontalScaling:
  - componentName: falkordb
    scaleOut:
      replicaChanges: 1
```

Apply the scaling operation:

```bash
kubectl apply -f scale-out.yaml
```

#### Scale In

Remove replicas from your cluster:

```yaml
apiVersion: operations.kubeblocks.io/v1alpha1
kind: OpsRequest
metadata:
  name: falkordb-scale-in
  namespace: demo
spec:
  clusterName: falkordb-replication
  type: HorizontalScaling
  horizontalScaling:
  - componentName: falkordb
    scaleIn:
      replicaChanges: 1
```

Alternatively, update the cluster directly:

```bash
kubectl patch cluster -n demo falkordb-replication --type merge -p '{"spec":{"componentSpecs":[{"name":"falkordb","replicas":3}]}}'
```

### Vertical Scaling

Update CPU and memory resources:

```yaml
apiVersion: operations.kubeblocks.io/v1alpha1
kind: OpsRequest
metadata:
  name: falkordb-vertical-scale
  namespace: demo
spec:
  clusterName: falkordb-replication
  type: VerticalScaling
  verticalScaling:
  - componentName: falkordb
    requests:
      cpu: "1"
      memory: "2Gi"
    limits:
      cpu: "2"
      memory: "4Gi"
```

### Volume Expansion

Expand storage volume (requires storage class with volume expansion support):

```yaml
apiVersion: operations.kubeblocks.io/v1alpha1
kind: OpsRequest
metadata:
  name: falkordb-volume-expand
  namespace: demo
spec:
  clusterName: falkordb-replication
  type: VolumeExpansion
  volumeExpansion:
  - componentName: falkordb
    volumeClaimTemplates:
    - name: data
      storage: 30Gi
```

### Restart Cluster

Restart all components:

```yaml
apiVersion: operations.kubeblocks.io/v1alpha1
kind: OpsRequest
metadata:
  name: falkordb-restart
  namespace: demo
spec:
  clusterName: falkordb-replication
  type: Restart
  restart:
  - componentName: falkordb
```

### Stop and Start

Stop the cluster (releases pods but retains storage):

```bash
kubectl patch cluster -n demo falkordb-replication --type merge -p '{"spec":{"componentSpecs":[{"name":"falkordb","stop":true},{"name":"falkordb-sent","stop":true}]}}'
```

Start the cluster:

```bash
kubectl patch cluster -n demo falkordb-replication --type merge -p '{"spec":{"componentSpecs":[{"name":"falkordb","stop":false},{"name":"falkordb-sent","stop":false}]}}'
```

## Configuration Management

### Reconfigure Parameters

Update FalkorDB configuration dynamically:

```yaml
apiVersion: operations.kubeblocks.io/v1alpha1
kind: OpsRequest
metadata:
  name: falkordb-reconfigure
  namespace: demo
spec:
  clusterName: falkordb-replication
  type: Reconfiguring
  reconfigure:
    componentName: falkordb
    configurations:
    - name: falkordb-config
      keys:
      - key: redis.conf
        parameters:
        - key: maxclients
          value: "10001"
```

Some parameters (like `maxclients`) require a restart. KubeBlocks will handle this automatically.

Verify the configuration:

```bash
kubectl exec -it -n demo falkordb-replication-falkordb-0 -- redis-cli CONFIG GET maxclients
```

## Backup and Restore

### Create a Backup Repository

Before creating backups, configure a backup repository:

```yaml
apiVersion: dataprotection.kubeblocks.io/v1alpha1
kind: BackupRepo
metadata:
  name: my-backup-repo
spec:
  storageProviderRef: s3
  config:
    bucket: my-falkordb-backups
    endpoint: s3.amazonaws.com
    region: us-west-2
  credential:
    name: s3-credentials
    namespace: demo
```

### Full Backup

Create a full backup using Redis BGSAVE:

```yaml
apiVersion: dataprotection.kubeblocks.io/v1alpha1
kind: Backup
metadata:
  name: falkordb-backup
  namespace: demo
spec:
  backupPolicyName: falkordb-replication-falkordb-backup-policy
  backupMethod: datafile
```

Apply the backup:

```bash
kubectl apply -f backup.yaml
```

Check backup status:

```bash
kubectl get backup -n demo falkordb-backup
```

### Continuous Backup (Point-in-Time Recovery)

Enable continuous backup using AOF (Append-Only File):

1. Enable AOF timestamps:

```yaml
apiVersion: operations.kubeblocks.io/v1alpha1
kind: OpsRequest
metadata:
  name: enable-aof-timestamps
  namespace: demo
spec:
  clusterName: falkordb-replication
  type: Reconfiguring
  reconfigure:
    componentName: falkordb
    configurations:
    - name: falkordb-config
      keys:
      - key: redis.conf
        parameters:
        - key: aof-timestamp-enabled
          value: "yes"
```

2. Update the BackupSchedule to enable AOF backup:

```bash
kubectl edit backupschedule -n demo falkordb-replication-falkordb-backup-schedule
```

Set `enabled: true` for the `aof` backup method.

### Restore from Backup

Restore a new cluster from a backup:

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: falkordb-restored
  namespace: demo
  annotations:
    kubeblocks.io/restore-from-backup: '{"falkordb":{"name":"falkordb-backup","namespace":"demo"}}'
spec:
  clusterDef: falkordb
  topology: replication
  componentSpecs:
  - name: falkordb
    serviceVersion: "4.12.5"
    replicas: 2
    resources:
      limits:
        cpu: "0.5"
        memory: "0.5Gi"
      requests:
        cpu: "0.5"
        memory: "0.5Gi"
    volumeClaimTemplates:
    - name: data
      spec:
        accessModes:
        - ReadWriteOnce
        resources:
          requests:
            storage: 20Gi
```

## Exposing Services

### Expose via LoadBalancer

Expose FalkorDB to external clients:

```yaml
apiVersion: operations.kubeblocks.io/v1alpha1
kind: OpsRequest
metadata:
  name: falkordb-expose
  namespace: demo
spec:
  clusterName: falkordb-replication
  type: Expose
  expose:
  - componentName: falkordb
    services:
    - name: external
      serviceType: LoadBalancer
      annotations:
        # Add cloud-specific annotations as needed
        service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
```

For different cloud providers, use appropriate annotations:

```yaml
# AWS
service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
service.beta.kubernetes.io/aws-load-balancer-internal: "false"

# Azure
service.beta.kubernetes.io/azure-load-balancer-internal: "false"

# GCP
cloud.google.com/l4-rbs: "enabled"

# Alibaba Cloud
service.beta.kubernetes.io/alibaba-cloud-loadbalancer-address-type: "internet"
```

### Expose via NodePort

For on-premises or development environments:

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: falkordb-replication
  namespace: demo
spec:
  # ... other fields ...
  componentSpecs:
  - name: falkordb
    services:
    - name: falkordb-advertised
      serviceType: NodePort
      podService: true
```

## Monitoring with Prometheus

### Enable Metrics Export

Ensure metrics are enabled when creating the cluster:

```yaml
spec:
  componentSpecs:
  - name: falkordb
    disableExporter: false  # Enable metrics exporter
```

### Create PodMonitor

Create a PodMonitor to scrape metrics:

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: falkordb-replication-pod-monitor
  namespace: demo
  labels:
    app.kubernetes.io/instance: falkordb-replication
spec:
  selector:
    matchLabels:
      app.kubernetes.io/instance: falkordb-replication
      apps.kubeblocks.io/component-name: falkordb
  podMetricsEndpoints:
  - port: http-metrics
    path: /metrics
    scheme: http
```

Apply the PodMonitor:

```bash
kubectl apply -f pod-monitor.yaml
```

### Access Grafana Dashboard

1. Access your Grafana instance
2. Import a Redis/FalkorDB dashboard from the [Grafana dashboard store](https://grafana.com/grafana/dashboards/)
3. Configure the dashboard to use the correct job label (e.g., `monitoring/falkordb-replication-pod-monitor`)

## Best Practices

### High Availability

* Use the **replication** topology with at least 3 Sentinel replicas
* Distribute pods across availability zones using pod anti-affinity
* Configure appropriate resource requests and limits
* Enable automated backups with appropriate retention policies

### Security

* Use Kubernetes secrets for storing passwords
* Enable TLS for client connections (if required)
* Use Network Policies to restrict access to FalkorDB pods
* Regularly rotate credentials

### Performance

* Choose appropriate storage class with good I/O performance
* Monitor resource usage and scale vertically/horizontally as needed
* For write-heavy workloads, consider disabling AOF timestamps
* Use sharding topology for large datasets

### Storage

* Ensure storage class supports volume expansion
* Configure appropriate storage size based on expected data growth
* Use persistent volumes with replication for data durability
* Test backup and restore procedures regularly

## Troubleshooting

### Cluster Not Ready

If the cluster status remains `Creating` for an extended period:

```bash
# Check pod status
kubectl get pods -n demo -l app.kubernetes.io/instance=falkordb-replication

# Check pod logs
kubectl logs -n demo <pod-name>

# Describe the cluster for events
kubectl describe cluster -n demo falkordb-replication
```

### Connection Issues

If you cannot connect to FalkorDB:

```bash
# Verify service exists
kubectl get svc -n demo

# Check if pods are running
kubectl get pods -n demo -l app.kubernetes.io/instance=falkordb-replication

# Verify credentials
kubectl get secret -n demo falkordb-replication-conn-credential -o yaml
```

### Backup Failures

If backups fail:

```bash
# Check backup status
kubectl describe backup -n demo <backup-name>

# Check backup policy
kubectl get backuppolicy -n demo -o yaml

# Verify BackupRepo configuration
kubectl describe backuprepo my-backup-repo
```

## Deleting the Cluster

To delete a cluster and all its resources:

```bash
# Change termination policy to allow deletion
kubectl patch cluster -n demo falkordb-replication -p '{"spec":{"terminationPolicy":"WipeOut"}}' --type="merge"

# Delete the cluster
kubectl delete cluster -n demo falkordb-replication
```

**Note**: `WipeOut` policy deletes all data including backups. Use `Delete` policy to retain backups.

## Additional Resources

* [KubeBlocks Official Documentation](https://kubeblocks.io/docs/preview/user_docs/overview/introduction)
* [KubeBlocks FalkorDB Examples](https://github.com/apecloud/kubeblocks-addons/tree/main/examples/falkordb)
* [FalkorDB Documentation](https://docs.falkordb.com)
* [Redis Sentinel Documentation](https://redis.io/docs/latest/operate/oss_and_stack/management/sentinel/)
* [Kubernetes Operators](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/)

## Summary

KubeBlocks provides a powerful, production-ready solution for deploying and managing FalkorDB on Kubernetes. With support for multiple topologies, comprehensive Day-2 operations, and automated backup/restore capabilities, KubeBlocks simplifies the operational complexity of running FalkorDB in Kubernetes environments. Whether you need a simple standalone instance for development or a highly available sharded cluster for production, KubeBlocks has you covered.
