---
title: "FalkorDBLite"
description: "Embedded FalkorDB runtime with Python and TypeScript bindings for embedded graph, local development, testing, and CI/CD pipelines without managing external servers."
nav_order: 6
parent: "Operations"
has_children: true
redirect_from:
  - /operations/falkordblite.html

---

# FalkorDBLite

FalkorDBLite bundles Redis with the FalkorDB module into an embedded runtime that your application controls. It is ideal for local development, prototyping, offline demos, and CI/CD pipelines where you need a lightweight graph database without managing an external server.

## Choose your SDK

- [FalkorDBLite for Python](./falkordblite-py.md) — `pip install falkordblite`
- [FalkorDBLite for TypeScript](./falkordblite-ts.md) — `npm install falkordblite`

## What you get

- Embedded Redis + FalkorDB server started by your app with sensible defaults
- Full FalkorDB graph capabilities via the language SDKs
- Data persistence when a database path is provided
- Easy migration to remote FalkorDB by swapping the connection line in your code

## When to use FalkorDBLite

- Local feature development and unit/integration testing
- Prototyping graph features without provisioning infrastructure
- Demos, workshops, and CI jobs that need a disposable graph database
- Small apps that prefer a single process runtime

For production workloads or multi-user deployments, move to [FalkorDB Cloud](https://app.falkordb.cloud) or self-hosted FalkorDB using [Docker](/operations/docker) or [Kubernetes](/operations/k8s-support).

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="What is FalkorDBLite?"
  a1="FalkorDBLite is an embedded FalkorDB runtime that bundles Redis with the FalkorDB module into a single process your application controls. No external server management is needed."
  q2="When should I use FalkorDBLite vs. a full FalkorDB server?"
  a2="Use FalkorDBLite for local development, prototyping, CI/CD pipelines, and demos. For production workloads, multi-user access, or high availability, use FalkorDB Cloud, Docker, or Kubernetes deployments."
  q3="Does FalkorDBLite support data persistence?"
  a3="Yes. Provide a database file path when creating the instance and data persists between sessions. Without a path, data is stored in a temporary directory and may be lost."
  q4="Can I migrate from FalkorDBLite to a remote FalkorDB server?"
  a4="Yes. Simply swap the connection line in your code from `FalkorDB(path)` (embedded) to connecting to a remote host. The graph API and Cypher queries remain identical."
%}
