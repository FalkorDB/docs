---
title: "Features"
description: "FalkorDB DBaaS Features"
---

# Features

## Multi-Tenancy
Multi-tenancy lets you run multiple isolated graph databases within a single FalkorDB instance. Each tenant operates independently with its own data, queries, and access controls while sharing the underlying infrastructure.

Developers building SaaS applications need multi-tenancy to serve multiple customers without deploying separate database instances for each one. This approach reduces operational overhead and infrastructure costs while maintaining strict data isolation between tenants.

In practice, you create distinct graph databases for each customer or project, and FalkorDB handles the isolation automatically.

## Cloud Providers
### AWS
FalkorDB runs on Amazon Web Services infrastructure, giving you access to AWS's global network of data centers and integration with other AWS services. You can deploy FalkorDB instances in several AWS regions and connect them to your existing AWS resources.

Teams already using AWS benefit from keeping their graph database in the same cloud environment as their applications. This setup reduces latency and simplifies network configuration since your services communicate within the AWS network.

When you deploy on AWS, you choose your preferred region, and FalkorDB provisions the necessary compute and storage resources in that location.

### Google Cloud Platform (GCP)
FalkorDB integrates with Google Cloud Platform, allowing you to run graph databases on Google's infrastructure. You gain access to GCP's global network and can combine FalkorDB with other Google Cloud services.

Organizations using GCP for their applications should deploy FalkorDB in the same cloud to maintain consistent infrastructure management. Keeping your database and applications on GCP reduces cross-cloud data transfer costs and latency.

You select a GCP region during deployment, and FalkorDB sets up your graph database instance within Google's infrastructure.

> Note: Microsoft Azure is currently available in a Bring-Your-Own-Cloud configuration

## TLS
TLS (Transport Layer Security) encrypts all data transmitted between your application and FalkorDB. This encryption prevents anyone intercepting network traffic from reading your queries or results.

Applications handling sensitive data must use TLS to protect information in transit. Without encryption, credentials, personal data, and business logic become vulnerable when traveling across networks.

When you enable TLS, FalkorDB requires encrypted connections. Your application must configure its database client to use TLS, and all communication happens over secure channels.

## VPC
A Virtual Private Cloud (VPC) creates an isolated network environment where your FalkorDB instance runs separately from the public internet. Only resources within your VPC or those you explicitly authorize can reach your database.

Organizations with security requirements need VPC deployment to control network access to their databases. VPCs prevent unauthorized connection attempts and give you granular control over which services can communicate with FalkorDB.

You deploy FalkorDB into your existing VPC, and the database becomes accessible only through your private network. Your applications connect using private IP addresses instead of public endpoints.

## Persistence
Persistence ensures your graph data survives system restarts, crashes, or failures by writing changes to disk. Without persistence, you lose all data when the database stops.

Any application storing important data requires persistence to maintain durability. In-memory-only databases lose everything during unexpected shutdowns, making them unsuitable for production workloads.

FalkorDB persists data through regular snapshots and transaction logs. These mechanisms guarantee that committed transactions remain safe even if the system crashes immediately afterward.

## Graph Browser
You can connect to the falkordb browser (integrated into your web browser) from the cloud console. The browser allows visualizing query results, allows you to traverse the graph and more. Multi Graph support is enabled by default in the browser which simplifies navigation and data management.

### Solution Architecture
Solution architecture support helps you design how FalkorDB integrates with your broader application infrastructure. This guidance covers connection patterns, data modeling approaches, and best practices for specific use cases.

Teams building complex systems benefit from architectural advice to avoid common pitfalls and optimize their graph database implementation. Poor architectural decisions early in development create technical debt that becomes expensive to fix later.

Architecture consultations provide recommendations on graph schema design, query optimization strategies, and integration patterns that match your application requirements.
