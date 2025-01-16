---
title: "MONITOR"
nav_order: 110
description: >
  Allows to observe all requests processed by the database in real-time. 
parent: "Commands"    
---

# MONITOR

Allows to observe all requests processed by the database in real-time. 
This feature is invaluable for debugging and understanding the sequence of operations occurring in the database.

Usage: `MONITOR`

## Example

```
> MONITOR
```

## Output

```sh
1673022405.123456 [0 127.0.0.1:6379] "GRAPH.QUERY" "MyGraph" "MATCH (n) return n"
1673022405.123789 [0 127.0.0.1:6379] "GRAPH.DELETE" "MyGraph"
```

Each line includes the following:

1. **Timestamp:** The precise time when the command was received.
2. **Database Index:** The database number where the command was executed (e.g., `[0]`).
3. **Client Info:** The IP address and port of the client that issued the command.
4. **Command:** The exact command and its arguments.

## Considerations

- **Security:** Ensure `MONITOR` is used only by trusted users. It exposes all incoming commands, including potentially sensitive data.
- **Overhead:** `MONITOR` can slow down the database, especially under high load, due to the additional I/O required to stream the logs.
- **Connection Restriction:** Typically, `MONITOR` should be run from a dedicated connection. Mixing it with other commands can result in undefined behavior.

## Terminating MONITOR

To stop the `MONITOR` stream, simply close the client connection (e.g., terminate the session or disconnect the client tool).

## Best Practices

- Use `MONITOR` sparingly in production environments.
- Combine `MONITOR` with logging or analysis tools for deeper insights.
- Restrict access to users who require diagnostic capabilities, see: [ACL](/commands/acl) for more details.
