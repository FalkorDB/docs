---
title: "Maintenance Windows"
parent: "Cloud DBaaS"
nav_order: 6
description: "FalkorDB Cloud maintenance windows for Enterprise deployments. Learn when maintenance happens, what to expect during it, and how to coordinate a window with our team."
---

# Maintenance Windows

FalkorDB performs routine maintenance on Cloud deployments to keep them secure, stable and up to date. Our goal is to give Enterprise customers as much flexibility as possible while keeping every deployment on the latest version. Staying current matters for security and stability.

## Availability by tier

Maintenance window flexibility is an **Enterprise only** feature.

| Tier | Maintenance approach |
| :--- | :--- |
| Enterprise | Predefined maintenance window set by you with the FalkorDB account team |
| Pro and below | Maintenance performed by FalkorDB with advance notice. No custom window |

## Scheduling

Every Enterprise customer has a predefined maintenance window. You set it together with your FalkorDB account team so maintenance lands at a time that works for your workload.

| | |
| :--- | :--- |
| **Window length** | Up to 4 hours |
| **Available slots** | Sunday to Wednesday, 6 AM to 8 PM UTC* |
| **Coordination** | Your account manager or [support@falkordb.com](mailto:support@falkordb.com) |

\* If the regular slots do not fit your operations, talk to your account team. We can discuss and extend the available window for Enterprise customers.

Need a change? Contact **[support@falkordb.com](mailto:support@falkordb.com)** to update your window or push a planned maintenance to the next window.

## What maintenance includes

* FalkorDB version upgrades
* Security patches
* Infrastructure and operating system updates
* Configuration and capacity changes

## What to expect during maintenance

The impact depends on your deployment type.

| Deployment | Expected impact |
| :--- | :--- |
| Standalone | Short downtime while the instance restarts |
| Replication / Cluster | No downtime. A brief latency spike may occur while nodes restart and traffic fails over |

We recommend enabling retry logic in your application. Most FalkorDB clients reconnect automatically after a restart or failover.

## Urgent maintenance

Critical fixes such as security patches may require maintenance outside an agreed window. In that case we notify you as early as possible and keep the impact to a minimum.

## Getting Support

Questions about an upcoming maintenance window? Email **[support@falkordb.com](mailto:support@falkordb.com)** or contact your account manager. See the [Support page](/support/) for what to include in your request.

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="Which tiers can set a maintenance window?"
  a1="Maintenance windows are an **Enterprise only** feature. Pro and lower tiers are upgraded by FalkorDB with advance notice and cannot set a custom window."
  q2="Will my database be available during maintenance?"
  a2="Replication and Cluster deployments stay available. You may notice a **brief latency spike** while nodes restart. Standalone deployments experience a **short downtime** during the restart."
  q3="How long is a maintenance window?"
  a3="A window lasts **up to 4 hours**. Actual work is usually much shorter. The window gives us room to roll back safely if needed."
  q4="Can I change or postpone a planned maintenance?"
  a4="Yes. Contact [support@falkordb.com](mailto:support@falkordb.com) to update your predefined window or push a planned maintenance to the next window."
%}
