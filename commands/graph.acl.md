---
title: "GRAPH.ACL"
description: >
  The GRAPH.ACL command manages user accounts and permissions for graph access.
parent: "Commands"    
---

## GRAPH.ACL

### Overview

The `GRAPH.ACL` command manages user accounts and permissions for graph access. It provides runtime control to create, modify, delete, and audit users with fine-grained privileges.

### Syntax
```text
GRAPH.ACL [SUBCOMMAND] [ARGUMENTS...]
```

### Subcommands

1. `GETUSER`
2. `SETUSER`
3. `DELUSER`
4. `LIST`

---

#### GRAPH.ACL SETUSER

Creates or updates users with specific rules and access privileges.
```text
GRAPH.ACL SETUSER <username> [rule1] [rule2] ...
```

**Supported Rules:**

- `on` / `off` - Enable or disable user login
- `nopass` - Allow access without password
- `>password` - Set user password
- `+COMMAND` - Grant command permission
- `~pattern` - Restrict access to graphs matching pattern

**Example:**
```text
GRAPH.ACL SETUSER john on >mySecret123 +GRAPH.QUERY +GRAPH.RO_QUERY ~sales*
```

This command creates user `john` with:
- Active status  
- Password `mySecret123`  
- Access limited to graphs starting with `sales`  
- Permission for read-only and query execution  

---

#### GRAPH.ACL GETUSER

Retrieves configuration for a specific user.
```text
GRAPH.ACL GETUSER <username>
```

**Example:**
```text
GRAPH.ACL GETUSER john
```

**Response:**
```text
"on"
">mySecret123"
"+GRAPH.QUERY"
"+GRAPH.RO_QUERY"
"~sales*"
```

---

#### GRAPH.ACL DELUSER

Deletes a user from the system.
```text
GRAPH.ACL DELUSER <username>
```

**Example:**
```text
GRAPH.ACL DELUSER john
```

---

#### GRAPH.ACL LIST

Lists all existing users.
```text
GRAPH.ACL LIST
```
