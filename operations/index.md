---
title: "Operations"
nav_order: 10
description: "Configuring FalkorDB Docker"
---

# Operations

The Operations chapter provides essential guides for configuring and managing FalkorDB in production environments. These guides cover critical aspects like data persistence, replication for high availability, and setting up clusters for horizontal scalability.

> **Production Tip:** For production deployments, consider using the `falkordb/falkordb-server` Docker image which is optimized for production use and doesn't include the FalkorDB Browser, making it lighter and more efficient.

Table of Contents

## 1. [Configuring Persistence](/operations/persistence)

Learn how to set up FalkorDB with data persistence, ensuring that your data remains intact even after server restarts.

## 2. [Configuring Replication](/operations/replication)

Set up replication in FalkorDB to achieve high availability and data redundancy across multiple nodes.

## 3. [Setting Up a Cluster](/operations/cluster)

Discover how to configure a FalkorDB cluster for horizontal scalability and improved fault tolerance, distributing your data across multiple nodes.

## 4. [Deploy FalkorDB to Kubernetes](/operations/k8s_support)

Learn how falkorDB can be deployed on Kubernetes using Helm charts and Docker images.

## 5. [Deploy FalkorDB on Railway](/operations/railway)

Deploy FalkorDB quickly using verified templates on Railway, a modern platform-as-a-service. Choose between single instance or cluster deployments.

## 6. [OpenTelemetry Integration with FalkorDB-py](/operations/opentelemetry)

Comprehensive guide for setting up OpenTelemetry observability and tracing with FalkorDB Python applications.

## 7. [FalkorDBLite](/operations/falkordblite)

Self-contained Python interface to FalkorDB with embedded Redis server, ideal for development and testing.

## 8. [Building Docker](/operations/building-docker)

Build custom FalkorDB Docker containers from source with platform-specific examples.
