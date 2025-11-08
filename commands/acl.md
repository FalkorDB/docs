---
title: "ACL"
nav_order: 100
description: >
    Managing Access Control Lists, enabling administrators to control user permissions at a granular level
parent: "Commands"    
---

# ACL

The ACL command in FalkorDB provides tools for managing Access Control Lists,
enabling administrators to control user permissions at a granular level.
This command is crucial for maintaining secure access to your FalkorDB instances.

Usage: `ACL [SUBCOMMAND] [arg1] [arg2] ...`

## Subcommands

### ACL HELP

Returns a list of all available `ACL` subcommands and their syntax.

Usage: `ACL HELP`

#### Example

```text
> ACL HELP
```text

#### Output

```text
1) "GETUSER"
2) "SETUSER"
3) "DELUSER"
4) "LIST"
...
```text

### ACL SETUSER

Defines or updates a user's permissions.

Usage: `ACL SETUSER <username> [rule1] [rule2] ...`

#### Rules

    * on / off: Enables or disables the user account.
    * nopass: Allows access without a password.
    * password:<password>: Sets a password for the user.
    * ~<pattern>: Restricts access to graphs matching the given pattern.
    * +<command>: Grants permission to execute specific commands.
    * -<command>: Denies permission to execute specific commands.

#### Example

```text
> ACL SETUSER john on >password123 +GRAPH.LIST +GRAPH.RO_QUERY ~*
```text

### ACL GETUSER

Retrieves details about a specific user, including permissions and settings.
Syntax

Usage: `ACL GETUSER <username>`

#### Example

```text
> ACL GETUSER john
```text

#### Output

```text
1) "on"
2) ">password123"
3) "+GRAPH.LIST"
4) "+GRAPH.RO_QUERY"
5) "~*"
```text

### ACL DELUSER

Deletes a user from the ACL.

Usage: `ACL DELUSER <username>`

#### Example

```text
> ACL DELUSER john
```text

### ACL LIST

Lists all users currently configured in the ACL.

Usage: `ACL LIST`

#### Example

```text
> ACL LIST
```text

#### Output

```text
1) "admin"
2) "john"
3) "guest"
```text

### ACL LOG

Displays a log of recent ACL-related events, such as user authentication attempts or rule changes.

Usage: `ACL LOG [count]`

    * count: (Optional) Limits the number of entries in the log.

#### Example

```text
> ACL LOG 10
```text

## Notes

    The ACL command is available only to users with administrative privileges.
    Be cautious when using the nopass rule, as it may compromise security.
    Use specific patterns and commands to enforce the principle of least privilege.
