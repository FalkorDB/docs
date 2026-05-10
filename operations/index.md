---
title: "Operations"
nav_order: 10
description: "Learn how to configure, deploy, and manage FalkorDB in production environments with Docker, persistence, replication, clustering, and Kubernetes support."
redirect_from:
  - /operation
  - /operation.html
---

# Operations

The Operations chapter provides essential guides for configuring and managing FalkorDB in production environments. These guides cover critical aspects like data persistence, replication for high availability, and setting up clusters for horizontal scalability.

> **Production Tip:** For production deployments, consider using the `falkordb/falkordb-server` Docker image which is optimized for production use and doesn't include the FalkorDB Browser, making it lighter and more efficient.

## 1. [Docker and Docker Compose](/operations/docker)

Learn how to run FalkorDB using Docker and Docker Compose, with examples for development and production environments including persistence, networking, and configuration options.

## 2. [Data Durability](/operations/durability)

Understand FalkorDB's durability mechanisms including RDB snapshots, AOF logging, and graph-specific backup options to balance performance and data safety.

## 3. [Configuring Replication](/operations/replication)

Set up replication in FalkorDB to achieve high availability and data redundancy across multiple nodes.

## 4. [Setting Up a Cluster](/operations/cluster)

Discover how to configure a FalkorDB cluster for horizontal scalability and improved fault tolerance, distributing your data across multiple nodes.

## 5. [Deploy FalkorDB to Kubernetes](/operations/k8s-support)

Learn how FalkorDB can be deployed on Kubernetes using Helm charts and Docker images.

## 6. [Deploy FalkorDB with KubeBlocks](/operations/kubeblocks)

Deploy and manage FalkorDB on Kubernetes using the KubeBlocks operator with automated Day-2 operations, high availability, and comprehensive backup solutions.

## 7. [Deploy FalkorDB on Railway](/operations/railway)

Deploy FalkorDB quickly using verified templates on Railway, a modern platform-as-a-service. Choose between single instance or cluster deployments.

## 8. [OpenTelemetry Integration with FalkorDB-py](/operations/opentelemetry)

Comprehensive guide for setting up OpenTelemetry observability and tracing with FalkorDB Python applications.

## 9. [FalkorDBLite](/operations/falkordblite)

Embedded FalkorDB runtime for local development with guides for [Python](/operations/falkordblite/falkordblite-py) and [TypeScript](/operations/falkordblite/falkordblite-ts).

## 10. [Deploy FalkorDB on Lightning.AI](/operations/lightning-ai)

Deploy FalkorDB on Lightning.AI to build fast, accurate GenAI applications using advanced RAG with graph databases.

## 11. [Migration Guides](/operations/migration)

Comprehensive guides for migrating your data to FalkorDB from RedisGraph, Neo4j, Kuzu, RDF-based systems, and SQL sources.

## 12. [Building Docker](/operations/building-docker)

Build custom FalkorDB Docker containers from source with platform-specific examples.

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="What Docker image should I use for production?"
  a1="Use `falkordb/falkordb-server` for production deployments. It excludes the browser UI, making it lighter and more efficient. Use `falkordb/falkordb` for development when you need the built-in browser."
  q2="How do I ensure my data survives container restarts?"
  a2="Mount a persistent volume to `/data` using Docker volumes or bind mounts, and enable AOF persistence. See the [Data Durability](/operations/durability) guide for full details."
  q3="Can FalkorDB scale horizontally?"
  a3="Yes. FalkorDB supports clustering via Redis Cluster, distributing graphs across multiple shards using hash slots. Each graph resides on one shard. See [Setting Up a Cluster](/operations/cluster) for setup instructions."
  q4="What is the easiest way to deploy FalkorDB to the cloud?"
  a4="Use [FalkorDB Cloud](https://app.falkordb.cloud) for a fully managed service, or deploy quickly using [Railway templates](/operations/railway) for single-instance or cluster configurations."
  q5="Does FalkorDB support high availability?"
  a5="Yes. Configure replication with a master and one or more replicas for read scaling. Note that standalone replication alone does not provide automatic failover — you need Redis Sentinel or a cluster manager for that. On Kubernetes, use Sentinel-based deployments via Helm charts or KubeBlocks for automated HA."
%}
