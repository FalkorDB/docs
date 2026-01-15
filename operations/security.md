---
title: "Security Guide"
description: "Hardening FalkorDB deployments across auth, network, and secrets."
---

<!-- markdownlint-disable MD025 -->

# Security Guide

Use this checklist to keep FalkorDB environments production-ready. FalkorDB inherits Redis server security concepts (auth, ACLs, networking), so the same discipline applies here.

## Quick checklist

- Enforce authentication everywhere (cloud, containers, local).
- Prefer per-environment credentials; do not bake secrets into images.
- Restrict network access to private subnets and trusted workloads.
- Apply least-privilege ACLs for graph commands.
- Encrypt traffic in transit (TLS termination or private links).
- Keep images and client libraries up to date.

## Authentication and authorization

- **Global auth**: set a password at server start (for example via `--requirepass` in `REDIS_ARGS`).
- **ACLs**: define role-scoped permissions with [ACL commands](/commands/acl) to limit who can run graph operations. Grant only the commands your service needs.
- **Per-graph isolation**: use separate graph names for teams or tenants; pair with ACLs to restrict access to those keys.

## Network posture

- Run FalkorDB inside private networks or VPCs; avoid exposing ports directly to the internet.
- Limit inbound traffic with security groups/firewalls to application hosts, CI, and bastions.
- If you require TLS, terminate at a trusted proxy/load balancer or use a TLS-enabled Redis build, then connect to FalkorDB through that encrypted hop.
- Disable unused ports (for example, set `BOLT_PORT` to `-1` if you do not use Bolt; see [configuration](/getting-started/configuration#bolt_port)).

## Secrets handling

- Store credentials in secret managers (Vault, cloud secret stores, Kubernetes secrets) and inject via environment variables or runtime mounts.
- Rotate credentials regularly and on personnel changes; prefer short-lived tokens where possible.
- Avoid committing passwords or connection strings to repositories, images, or client logs.

## Auditing and observability

- Centralize logs from FalkorDB and your proxy/ingress. Watch for failed auth attempts and command spikes.
- Enable structured application logs for queries that mutate data; correlate with user identity from your auth layer.
- Set [query timeouts](/getting-started/configuration#timeout) to reduce the blast radius of runaway workloads.

## Backup and recovery

- Take regular snapshots of data volumes and configuration. Test restores in a separate environment.
- Document recovery runbooks, including how to re-apply ACLs and secrets after restore.

## Deployment-specific notes

- **Containers**: avoid running as root; prefer minimal images like `falkordb/falkordb-server`. Mount configuration and secrets read-only.
- **Kubernetes**: restrict Services to internal load balancers; use NetworkPolicies to limit pod-to-pod access; mount secrets with rotation.
- **Cloud**: prefer private endpoints and identity-aware access (IAM) over long-lived passwords when available.
