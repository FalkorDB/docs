---
title: "Startup Tier"
parent: "Cloud DBaaS"
nav_order: 2
description: "FalkorDB DBaaS Startup Tier"
---

![FalkorDB Cloud Startup Tier Banner](https://github.com/user-attachments/assets/a60eacb7-2af6-432e-84c8-7c3dbe98422c)


# Startup Tier
FalkorDB's **Startup Tier** gives you instant access to a production-ready graph database starting at **$73/Month**. This tier is designed to help you **Build a Powerful MVP** with standalone deployment, multi-graph support, and multi-tenancy capabilities. You can deploy on AWS, GCP, or Azure (BYOC) and rely on community support to grow your application.

The Startup Tier includes essential features like **TLS** and **Automated Backups (Every 12 Hours)**, making it a robust, secure choice for your first production workload. When your application requires High Availability, dedicated support, or advanced enterprise features like VPC networking, you can easily upgrade to a Pro or Enterprise plan.

## FalkorDB Pricing Plans Comparison

| Feature | FREE | STARTUP | PRO | ENTERPRISE |
| :--- | :---: | :---: | :---: | :---: |
| **Monthly Cost (from)** | **Free** | **$73** | **$350** | **Custom** |
| Multi-Graph / Multi-Tenancy | ✓ | **🟢** | ✓ | ✓ |
| Graph Access Control | ✓ | **🟢** | ✓ | ✓ |
| **TLS** | ✗ | **🟢** | ✓ | ✓ |
| VPC | ✗ | **🔴** | ✗ | ✓ |
| Cluster Deployment | ✗ | **🔴** | ✓ | ✓ |
| High Availability | ✗ | **🔴** | ✓ | ✓ |
| Multi-zone Deployment | ✗ | **🔴** | ✓ | ✓ |
| Scalability | ✗ | **🔴** | ✓ | ✓ |
| Continuous Persistence | ✗ | **🔴** | ✓ | ✓ |
| **Automated Backups** | ✗ | **Every 12 Hours** | Every 12 Hours | Every Hour |
| Advanced Monitoring | ✗ | **🔴** | ✗ | ✓ |
| **Support** | Community | **Community** | 24/7 | Dedicated |
| Dedicated Account Manager | ✗ | **🔴** | ✗ | ✓ |
| **Cloud Providers** | AWS, GCP | **AWS, GCP** | AWS, GCP | AWS, GCP, Azure (BYOC) |
| **Call-to-Action** | [Sign up](https://app.falkordb.cloud/signup) | [Sign up](https://app.falkordb.cloud/signup) | [Sign up](https://app.falkordb.cloud/signup) | [Contact Us](mailto:info@falkordb.com) |

## Terms
### Pricing Calculation
> We calculate deployment costs based on **Memory GB/Hour** usage. Each Memory GB/Hour costs **$0.100**.
>
> The table below shows approximate monthly costs for different instance sizes (based on 730 hours/month), along with max graph dataset size (75% of RAM):
>
> | Instance Size (RAM) | Max Graph Dataset (GB) | Hourly Cost | Monthly Cost |
> | :--- | ---: | ---: | ---: |
> | 1 GB | 0.75 | $0.100/hr | $73/month* |
> | 2 GB | 1.5 | $0.200/hr | $146/month* |
>
> Monthly Cost = Hourly Cost × 730 hours/month.
>
> You can estimate your monthly costs by multiplying your instance's memory allocation (in GB) by **$73**.
>
> Use our **[graph size calculator](https://www.falkordb.com/graph-database-graph-size-calculator/)** to further estimate your cost.
> 
> ⚠️ Prices are subject to change

## Getting Started

<a href="https://www.youtube.com/watch?v=z0XO4pb2t5Y" target="_blank">
  <img src="https://github.com/user-attachments/assets/ca458209-2354-4989-8b44-d5b5f6f0a445" alt="FalkorDB Graph DBaaS Startup Tier Tutorial Video" width="640" height="360">
</a>

⚙️ Spin up your first FalkorDB Cloud instance: 
[![Sign Up](https://img.shields.io/badge/Sign%20Up-8A2BE2?style=for-the-badge)](https://app.falkordb.cloud/signup)

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="How much does the Startup Tier cost?"
  a1="The Startup Tier starts at **$73/month** for 1GB of RAM. Pricing is calculated at **$0.100 per Memory GB/Hour**. You can estimate costs by multiplying your memory allocation (in GB) by $73."
  q2="Does the Startup Tier include backups?"
  a2="Yes, the Startup Tier includes **automated backups every 12 hours**, ensuring your data is regularly protected without manual intervention."
  q3="Is TLS encryption included?"
  a3="Yes, **TLS** is included in the Startup Tier, encrypting all data transmitted between your application and FalkorDB for secure production workloads."
  q4="Can I run multiple graphs on the Startup Tier?"
  a4="Yes, the Startup Tier supports **Multi-Graph / Multi-Tenancy**, allowing you to run multiple isolated graph databases within a single instance."
  q5="What is the maximum dataset size I can store?"
  a5="The max graph dataset size is approximately **75% of your instance RAM**. For example, a 1GB instance supports ~0.75GB of graph data, and a 2GB instance supports ~1.5GB. Use the [graph size calculator](https://www.falkordb.com/graph-database-graph-size-calculator/) for estimates."
%}
