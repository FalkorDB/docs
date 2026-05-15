---
title: "Pro Tier"
parent: "Cloud DBaaS"
nav_order: 3
description: "FalkorDB Cloud Pro Tier starting at $350/month with high availability, multi-zone deployment, cluster support, continuous persistence, and 24/7 dedicated support for production workloads."
---

![FalkorDB Cloud Pro Tier Banner](https://github.com/user-attachments/assets/2d39df96-f932-4cba-a124-bfff93f9a0ca)


# Pro Tier
FalkorDB's **Pro Tier** is your solution for high-performance, production-ready graph database workloads, starting at **$350/Month**. This tier is designed for applications requiring **High Availability (HA)**, **Multi-zone Deployment**, and robust **Scalability**. It includes essential infrastructure features like **Cluster Deployment** and **Continuous Persistence (AOF + Snapshot)**, backed by **24-hour Dedicated Support**.

The Pro Tier provides a robust environment to scale your application with confidence. When your needs extend to features like VPC Peering, Advanced Monitoring, or a Dedicated Account Manager, you can easily upgrade to the Enterprise plan.

## FalkorDB Pricing Plans Comparison

| Feature | FREE | STARTUP | PRO | ENTERPRISE |
| :--- | :---: | :---: | :---: | :---: |
| **Monthly Cost (from)** | **Free** | **$73** | **$350** | **Custom** |
| Multi-Graph / Multi-Tenancy | ✓ | ✓ | **🟢** | ✓ |
| Graph Access Control | ✓ | ✓ | **🟢** | ✓ |
| **TLS** | ✗ | ✓ | **🟢** | ✓ |
| VPC | ✗ | ✗ | **🔴** | ✓ |
| Cluster Deployment | ✗ | ✗ | **🟢** | ✓ |
| High Availability | ✗ | ✗ | **🟢** | ✓ |
| Multi-zone Deployment | ✗ | ✗ | **🟢** | ✓ |
| Scalability | ✗ | ✗ | **🟢** | ✓ |
| Continuous Persistence | ✗ | ✗ | **🟢** | ✓ |
| **Automated Backups** | ✗ | Every 12 Hours | **Every 12 Hours** | Every Hour |
| Advanced Monitoring | ✗ | ✗ | **🔴** | ✓ |
| **Support** | Community | Community | **24/7** | Dedicated |
| Dedicated Account Manager | ✗ | ✗ | **🔴** | ✓ |
| **Cloud Providers** | AWS, GCP | AWS, GCP | **AWS, GCP** | AWS, GCP, Azure (BYOC) |
| **Get started** | [Sign up](https://app.falkordb.cloud/signup) | [Sign up](https://app.falkordb.cloud/signup) | [Sign up](https://app.falkordb.cloud/signup) | [Contact Us](mailto:info@falkordb.com) |

## Terms
### Pricing Calculation
> We charge deployments based on **Core/Hour** and **Memory GB/Hour** usage. You pay **$0.200 per Core/Hour** and **$0.01 per Memory GB/Hour**.

## Standalone

| Instance Type | Cores | Memory (GB) | Max Graph Dataset (GB) | Monthly Cost |
| :--- | :---: | :---: | :---: | ---: |
| E2-medium | 1 | 4 | 2 | $175.20 |
| t2.medium | 2 | 4 | 2 | $321.20 |
| E2-standard-2 / m6i.large (Starting Instance) | 2 | 8 | 6 | $350.40 |
| E2-standard-4 / m6i.xlarge | 4 | 16 | 12 | $700.80 |
| E2-standard-8 / m6i.2xlarge | 8 | 32 | 24 | $1,401.60 |
| E2-highmem-2 / r6i.large | 2 | 16 | 12 | $408.80 |
| E2-highmem-4 / r6i.xlarge | 4 | 32 | 24 | $817.60 |
| E2-highmem-8 / r6i.2xlarge | 8 | 64 | 48 | $1,635.20 |
| m6i.4xlarge | 16 | 64 | 48 | $2,803.20 |
| m6i.8xlarge | 32 | 128 | 96 | $5,606.40 |
| r6i.4xlarge | 16 | 128 | 96 | $3,270.40 |
| E2-custom-4-8192 / c6i.xlarge | 4 | 8 | 6 | $642.40 |
| E2-custom-8-16384 / c6i.2xlarge | 8 | 16 | 12 | $1,284.80 |
| E2-custom-16-32768 / c6i.4xlarge | 16 | 32 | 24 | $2,569.60 |
| E2-custom-32-65536 / c6i.8xlarge | 32 | 64 | 48 | $5,139.20 |

## Replicated (High Availability, Master (x1), Replica (x1))


| Instances Type                                 | Cores | Memory (GB) | Max Graph Dataset (GB) | Monthly Cost |
| :--------------------------------------------- | :---: | :---------: | :--------------------: | -----------: |
| E2-medium                                      |   1   |      4      |           2            |     \$657.00 |
| t2.medium                                      |   2   |      4      |           2            |     \$949.00 |
| E2-standard-2 / m6i.large (Starting Instance)  |   2   |      8      |           6            |   \$1,007.40 |
| E2-standard-4 / m6i.xlarge                     |   4   |     16      |           12           |   \$1,708.20 |
| E2-standard-8 / m6i.2xlarge                    |   8   |     32      |           24           |   \$3,109.80 |
| E2-highmem-2 / r6i.large                       |   2   |     16      |           12           |   \$1,124.20 |
| E2-highmem-4 / r6i.xlarge                      |   4   |     32      |           24           |   \$1,941.80 |
| E2-highmem-8 / r6i.2xlarge                     |   8   |     64      |           48           |   \$3,577.00 |
| m6i.4xlarge                                    |  16   |     64      |           48           |   \$5,913.00 |
| m6i.8xlarge                                    |  32   |    128      |           96           |  \$11,519.40 |
| r6i.4xlarge                                    |  16   |    128      |           96           |   \$6,847.40 |
| E2-custom-4-8192 / c6i.xlarge                  |   4   |      8      |           6            |   \$1,591.40 |
| E2-custom-8-16384 / c6i.2xlarge                |   8   |     16      |           12           |   \$2,876.20 |
| E2-custom-16-32768 / c6i.4xlarge               |  16   |     32      |           24           |   \$5,445.80 |
| E2-custom-32-65536 / c6i.8xlarge               |  32   |     64      |           48           |  \$10,585.00 |

> Note: In the Replicated table, **Cores** and **Memory (GB)** are per instance. **Max Graph Dataset (GB)** is calculated as 2 GB for 4 GB containers and 75% of memory for containers larger than 4 GB. We charge an additional 2 cores and 2 GB for replication and cluster since they require an extra component (sentinel for replication and rebalancer for cluster).

> Use our **[graph size calculator](https://www.falkordb.com/graph-database-graph-size-calculator/)** to further estimate your cost.
> ⚠️ Prices are subject to change

## Getting Started

<a href="https://www.youtube.com/watch?v=UIzrW9otvYM" target="_blank">
  <img src="https://github.com/user-attachments/assets/e19fdb04-e8fd-45c5-8361-97691ff3362a" alt="FalkorDB Graph DBaaS Pro Tier Tutorial Video" width="640" height="360">
</a>

⚙️ Spin up your first FalkorDB Cloud instance: 
[![Sign Up](https://img.shields.io/badge/Sign%20Up-8A2BE2?style=for-the-badge)](https://app.falkordb.cloud/signup)

## Getting Support

Pro Tier customers receive **24/7 support**. Open a support ticket by emailing **[support@falkordb.com](mailto:support@falkordb.com)**. See the [Support page]({{ site.baseurl }}/support/) for what to include in your request.

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="What does High Availability mean in the Pro Tier?"
  a1="High Availability (HA) uses a **master-replica** architecture with automatic failover. If the primary node fails, the replica takes over, minimizing downtime for your application."
  q2="How is Pro Tier pricing calculated?"
  a2="Pro Tier charges are based on **$0.200 per Core/Hour** and **$0.01 per Memory GB/Hour**. The starting configuration (2 cores, 8GB RAM) costs approximately **$350/month**."
  q3="What is continuous persistence?"
  a3="Continuous persistence combines **AOF (Append-Only File) and Snapshots** to minimize data loss. With the default `appendfsync everysec` policy, at most ~1 second of writes may be lost during an unexpected crash. This provides strong durability without significant performance overhead."
  q4="Does the Pro Tier include dedicated support?"
  a4="Yes, the Pro Tier includes **24/7 dedicated support**. For a dedicated account manager, you would need to upgrade to the Enterprise tier."
  q5="Can I deploy across multiple availability zones?"
  a5="Yes, the Pro Tier supports **multi-zone deployment**, distributing your database across multiple availability zones for resilience against zone-level failures on AWS or GCP."
%}
