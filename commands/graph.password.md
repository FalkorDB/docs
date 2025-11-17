---
title: "GRAPH.PASSWORD"
description: >
  Securely sets or updates user passwords within FalkorDB.
parent: "Commands"    
---

## GRAPH.PASSWORD

### Description

The `GRAPH.PASSWORD` command securely sets or updates user passwords within FalkorDB. It complements `GRAPH.ACL` by allowing password changes without altering user privileges.

### Usage Patterns

The behavior of `GRAPH.PASSWORD` depends on the user context and argument count.

#### 1. Change Own Password (Single Argument)

A regular user can change their own password:
```text
GRAPH.PASSWORD <new_password>
```

This command updates the password only for the currently authenticated user.

**Example:**
```text
GRAPH.PASSWORD S3cureMyPass!
```

**Response:**
```text
OK
```
